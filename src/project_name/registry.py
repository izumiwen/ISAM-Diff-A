"""只使用標準函式庫的資產 registry、schema 與 blocked-state 檢查。"""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any


ASSET_FIELDS = (
    "repository_url",
    "source_commit",
    "source_tree_sha256",
    "source_dirty_status",
    "checkpoint_path",
    "checkpoint_sha256",
    "checkpoint_size_bytes",
    "checkpoint_license",
    "vae_id",
    "vae_revision",
    "vae_sha256",
    "latent_scaling_factor",
    "interpolant",
    "prediction_parameterization",
    "time_endpoints",
    "solver",
    "conditioning_contract",
    "dataset_manifest_path",
    "dataset_license",
)

PROJECT_SOURCE_URL = "https://github.com/CompVis/zigma.git"
_HEX_SHA256 = re.compile(r"^[0-9a-f]{64}$")
_HEX_GIT_OBJECT = re.compile(r"^[0-9a-f]{40,64}$")
_SCHEMA_KEYWORDS = {
    "$schema",
    "title",
    "description",
    "type",
    "required",
    "properties",
    "additionalProperties",
    "enum",
    "const",
    "minimum",
    "items",
}


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _json_kind(value: Any) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "boolean"
    if isinstance(value, int):
        return "integer"
    if isinstance(value, float):
        return "number"
    if isinstance(value, str):
        return "string"
    if isinstance(value, list):
        return "array"
    if isinstance(value, dict):
        return "object"
    return "unknown"


class AssetRegistry:
    """Registry 不載入資產；僅驗證已存在的靜態宣告及其證據。"""

    def __init__(self, values: dict[str, Any] | None = None) -> None:
        source = dict(values or {field: None for field in ASSET_FIELDS})
        self.format_version = source.get("format_version", "1.0")
        self.values = source if self.format_version == "2.0" else {
            field: source.get(field) for field in ASSET_FIELDS
        }

    @classmethod
    def empty(cls) -> "AssetRegistry":
        return cls()

    @classmethod
    def from_path(cls, path: Path) -> "AssetRegistry":
        data = json.loads(path.read_text(encoding="utf-8"))
        schema = cls.schema_v2_document() if data.get("format_version") == "2.0" else cls.schema_document()
        cls.validate_schema_document(data, schema)
        return cls(data)

    @staticmethod
    def _reference_path(filename: str) -> Path:
        return Path(__file__).resolve().parents[2] / "references" / filename

    @classmethod
    def schema_document(cls) -> dict[str, Any]:
        return json.loads(cls._reference_path("asset_registry.schema.json").read_text(encoding="utf-8"))

    @classmethod
    def schema_v2_document(cls) -> dict[str, Any]:
        return json.loads(cls._reference_path("asset_registry_v2.schema.json").read_text(encoding="utf-8"))

    @classmethod
    def checkpoint_metadata_schema(cls) -> dict[str, Any]:
        return json.loads(cls._reference_path("checkpoint_metadata.schema.json").read_text(encoding="utf-8"))

    @classmethod
    def dataset_manifest_schema(cls) -> dict[str, Any]:
        return json.loads(cls._reference_path("dataset_manifest.schema.json").read_text(encoding="utf-8"))

    @classmethod
    def validate_checkpoint_metadata(cls, data: dict[str, Any]) -> None:
        cls.validate_schema_document(data, cls.checkpoint_metadata_schema())

    @classmethod
    def validate_dataset_manifest(cls, data: dict[str, Any]) -> None:
        cls.validate_schema_document(data, cls.dataset_manifest_schema())

    @classmethod
    def validate_schema_document(cls, data: Any, schema: dict[str, Any]) -> None:
        cls._validate_schema_definition(schema, "$")
        cls._validate_value(data, schema, "$")

    @classmethod
    def _validate_schema_definition(cls, schema: Any, location: str) -> None:
        if not isinstance(schema, dict):
            raise ValueError(f"schema {location} 必須是 object")
        unknown = sorted(set(schema) - _SCHEMA_KEYWORDS)
        if unknown:
            raise ValueError(f"schema {location} 含未支援 keyword: {', '.join(unknown)}")
        if "type" in schema:
            declared = schema["type"]
            allowed = declared if isinstance(declared, list) else [declared]
            if not allowed or any(item not in {"null", "boolean", "integer", "number", "string", "array", "object"} for item in allowed):
                raise ValueError(f"schema {location}.type 不合法")
        if "required" in schema and (not isinstance(schema["required"], list) or any(not isinstance(item, str) for item in schema["required"])):
            raise ValueError(f"schema {location}.required 不合法")
        if "properties" in schema:
            if not isinstance(schema["properties"], dict):
                raise ValueError(f"schema {location}.properties 必須是 object")
            for name, child in schema["properties"].items():
                cls._validate_schema_definition(child, f"{location}.properties.{name}")
        if "additionalProperties" in schema:
            extra = schema["additionalProperties"]
            if not isinstance(extra, (bool, dict)):
                raise ValueError(f"schema {location}.additionalProperties 必須是 boolean 或 schema")
            if isinstance(extra, dict):
                cls._validate_schema_definition(extra, f"{location}.additionalProperties")
        if "items" in schema:
            cls._validate_schema_definition(schema["items"], f"{location}.items")
        if "minimum" in schema and (not isinstance(schema["minimum"], (int, float)) or isinstance(schema["minimum"], bool)):
            raise ValueError(f"schema {location}.minimum 必須是 number")
        if "enum" in schema and not isinstance(schema["enum"], list):
            raise ValueError(f"schema {location}.enum 必須是 array")

    @classmethod
    def _validate_value(cls, value: Any, schema: dict[str, Any], location: str) -> None:
        if "type" in schema:
            allowed = schema["type"] if isinstance(schema["type"], list) else [schema["type"]]
            kind = _json_kind(value)
            compatible = kind in allowed or (kind == "integer" and "number" in allowed)
            if not compatible:
                raise ValueError(f"{location} 型別必須是 {allowed}，實際為 {kind}")
        if "const" in schema and value != schema["const"]:
            raise ValueError(f"{location} 必須等於 const 值")
        if "enum" in schema and value not in schema["enum"]:
            raise ValueError(f"{location} 不在 enum 範圍內")
        if "minimum" in schema and isinstance(value, (int, float)) and not isinstance(value, bool) and value < schema["minimum"]:
            raise ValueError(f"{location} 不得小於 {schema['minimum']}")
        if isinstance(value, dict):
            properties = schema.get("properties", {})
            missing = sorted(set(schema.get("required", [])) - set(value))
            if missing:
                raise ValueError(f"{location} 缺少欄位: {', '.join(missing)}")
            extras = sorted(set(value) - set(properties))
            additional = schema.get("additionalProperties", True)
            if extras and additional is False:
                raise ValueError(f"{location} 不允許未知欄位: {', '.join(extras)}")
            for name, descriptor in properties.items():
                if name in value:
                    cls._validate_value(value[name], descriptor, f"{location}.{name}")
            if isinstance(additional, dict):
                for name in extras:
                    cls._validate_value(value[name], additional, f"{location}.{name}")
        if isinstance(value, list) and "items" in schema:
            for index, item in enumerate(value):
                cls._validate_value(item, schema["items"], f"{location}[{index}]")

    @staticmethod
    def source_tree_sha256(checkout_path: Path) -> str:
        """計算 Git tracked regular files 的可重驗 SHA-256 manifest digest。"""
        raw = subprocess.check_output(
            ["git", "-C", str(checkout_path), "ls-files", "-s", "-z"],
            stderr=subprocess.STDOUT,
        )
        entries: list[tuple[bytes, str]] = []
        for entry in raw.split(b"\0"):
            if not entry:
                continue
            header, relative_bytes = entry.split(b"\t", 1)
            mode = header.split()[0]
            if mode not in (b"100644", b"100755"):
                continue
            relative = relative_bytes.decode("utf-8", "surrogateescape")
            path = checkout_path / relative
            if not path.is_file() or path.is_symlink():
                raise ValueError(f"source tracked file 不是一般檔案: {relative}")
            entries.append((relative_bytes, f"{relative}\t{path.stat().st_size}\t{_sha256_file(path)}\n"))
        entries.sort(key=lambda item: item[0])
        return hashlib.sha256("".join(row for _, row in entries).encode("utf-8")).hexdigest()

    def to_dict(self) -> dict[str, Any]:
        if self.format_version == "2.0":
            result = dict(self.values)
        else:
            result = {field: self.values.get(field) for field in ASSET_FIELDS}
        result.update(self.validate())
        return result

    def validate(self) -> dict[str, Any]:
        if self.format_version == "2.0":
            return self._validate_v2()
        return self._validate_v1()

    def _validate_v1(self) -> dict[str, Any]:
        codes: list[str] = []
        diagnostics: list[str] = []
        self._require(("repository_url", "source_commit", "source_tree_sha256", "source_dirty_status"), "BLOCKED_SOURCE_AMBIGUITY", codes, diagnostics)
        self._require(("checkpoint_path", "checkpoint_sha256", "checkpoint_size_bytes", "checkpoint_license"), "BLOCKED_CHECKPOINT_IDENTITY", codes, diagnostics)
        checkpoint_path = self.values.get("checkpoint_path")
        if checkpoint_path and not self._regular_file(Path(str(checkpoint_path))):
            self._add("BLOCKED_CHECKPOINT_IDENTITY", "checkpoint_path 不存在或不是一般檔案", codes, diagnostics)
        self._require(("vae_id", "vae_revision", "vae_sha256", "latent_scaling_factor"), "BLOCKED_VAE_IDENTITY", codes, diagnostics)
        self._require(("interpolant", "prediction_parameterization", "time_endpoints", "solver"), "BLOCKED_TRANSPORT_CONTRACT", codes, diagnostics)
        self._require(("conditioning_contract",), "BLOCKED_CONDITIONING_CONTRACT", codes, diagnostics)
        self._require(("dataset_manifest_path",), "BLOCKED_DATA_CONTRACT", codes, diagnostics)
        manifest_path = self.values.get("dataset_manifest_path")
        if manifest_path and not self._regular_file(Path(str(manifest_path))):
            self._add("BLOCKED_DATA_CONTRACT", "dataset_manifest_path 不存在或不是一般檔案", codes, diagnostics)
        self._require(("checkpoint_license", "dataset_license"), "BLOCKED_LICENSE", codes, diagnostics)
        return {"status": "blocked" if codes else "unproven", "blocked_codes": codes, "diagnostics": diagnostics}

    def _validate_v2(self) -> dict[str, Any]:
        codes: list[str] = []
        diagnostics: list[str] = []
        try:
            self.validate_schema_document(self.values, self.schema_v2_document())
        except ValueError as error:
            self._add("BLOCKED_SOURCE_AMBIGUITY", f"v2 schema 無法驗證: {error}", codes, diagnostics)
            return {"status": "blocked", "blocked_codes": codes, "diagnostics": diagnostics}
        self._validate_source(self.values["source"], codes, diagnostics)
        self._validate_binary_asset(self.values["checkpoint"], "checkpoint", "BLOCKED_CHECKPOINT_IDENTITY", codes, diagnostics, metadata=True)
        self._validate_binary_asset(self.values["vae"], "vae", "BLOCKED_VAE_IDENTITY", codes, diagnostics, metadata=False)
        self._validate_dataset(self.values["dataset"], codes, diagnostics)
        self._validate_licenses(codes, diagnostics)
        return {"status": "blocked" if codes else "unproven", "blocked_codes": codes, "diagnostics": diagnostics}

    def _validate_source(self, source: dict[str, Any], codes: list[str], diagnostics: list[str]) -> None:
        required = ("repository_url", "checkout_path", "commit", "git_tree_id", "source_tree_sha256", "worktree_clean", "license", "license_path", "license_sha256", "provenance_evidence")
        if self._missing_values(source, required, "BLOCKED_SOURCE_AMBIGUITY", codes, diagnostics):
            return
        if source["repository_url"] != PROJECT_SOURCE_URL:
            self._add("BLOCKED_SOURCE_AMBIGUITY", "repository_url 不等於唯一授權來源", codes, diagnostics)
        for field in ("commit", "git_tree_id"):
            if not isinstance(source[field], str) or not _HEX_GIT_OBJECT.fullmatch(source[field]):
                self._add("BLOCKED_SOURCE_AMBIGUITY", f"{field} 不是完整 hex Git object ID", codes, diagnostics)
        if not isinstance(source["source_tree_sha256"], str) or not _HEX_SHA256.fullmatch(source["source_tree_sha256"]):
            self._add("BLOCKED_SOURCE_AMBIGUITY", "source_tree_sha256 格式無效", codes, diagnostics)
        checkout = Path(str(source["checkout_path"]))
        if not checkout.is_dir():
            self._add("BLOCKED_SOURCE_AMBIGUITY", "checkout_path 不存在或不是目錄", codes, diagnostics)
        else:
            try:
                origin = subprocess.check_output(["git", "-C", str(checkout), "remote", "get-url", "origin"], text=True, stderr=subprocess.STDOUT).strip()
                head = subprocess.check_output(["git", "-C", str(checkout), "rev-parse", "HEAD"], text=True, stderr=subprocess.STDOUT).strip()
                tree = subprocess.check_output(["git", "-C", str(checkout), "rev-parse", "HEAD^{tree}"], text=True, stderr=subprocess.STDOUT).strip()
                dirty = subprocess.check_output(["git", "-C", str(checkout), "status", "--porcelain=v1"], text=True, stderr=subprocess.STDOUT)
                if origin != source["repository_url"] or head != source["commit"] or tree != source["git_tree_id"]:
                    self._add("BLOCKED_SOURCE_AMBIGUITY", "clone origin、HEAD 或 Git tree 與宣告不一致", codes, diagnostics)
                if bool(dirty.strip()) or source["worktree_clean"] is not True:
                    self._add("BLOCKED_SOURCE_AMBIGUITY", "source worktree 不乾淨", codes, diagnostics)
                if self.source_tree_sha256(checkout) != source["source_tree_sha256"]:
                    self._add("BLOCKED_SOURCE_AMBIGUITY", "source tracked-file manifest SHA-256 不一致", codes, diagnostics)
            except (OSError, subprocess.CalledProcessError, ValueError) as error:
                self._add("BLOCKED_SOURCE_AMBIGUITY", f"無法驗證 source clone: {error}", codes, diagnostics)
        license_path = Path(str(source["license_path"]))
        if not self._regular_file(license_path) or _sha256_file(license_path) != source["license_sha256"]:
            self._add("BLOCKED_LICENSE", "source license path 或 SHA-256 不一致", codes, diagnostics)
        if not self._evidence_exists(source["provenance_evidence"]):
            self._add("BLOCKED_SOURCE_AMBIGUITY", "source provenance evidence 不存在或不是 HTTPS/local file", codes, diagnostics)

    def _validate_binary_asset(self, asset: dict[str, Any], name: str, code: str, codes: list[str], diagnostics: list[str], *, metadata: bool) -> None:
        required = ("path", "sha256", "size_bytes", "license", "provenance_evidence")
        if name == "vae":
            required = ("id", "revision") + required
        missing = self._missing_values(asset, required, code, codes, diagnostics)
        if missing:
            return
        path = Path(str(asset["path"]))
        if not self._regular_file(path):
            self._add(code, f"{name}.path 不存在或不是一般檔案", codes, diagnostics)
        else:
            if not isinstance(asset["sha256"], str) or not _HEX_SHA256.fullmatch(asset["sha256"]):
                self._add(code, f"{name}.sha256 格式無效", codes, diagnostics)
            elif _sha256_file(path) != asset["sha256"]:
                self._add(code, f"{name}.sha256 與檔案不一致", codes, diagnostics)
            if not isinstance(asset["size_bytes"], int) or isinstance(asset["size_bytes"], bool) or path.stat().st_size != asset["size_bytes"]:
                self._add(code, f"{name}.size_bytes 與檔案不一致", codes, diagnostics)
        if not self._evidence_exists(asset["provenance_evidence"]):
            self._add(code, f"{name}.provenance_evidence 不存在或不是 HTTPS/local file", codes, diagnostics)
        if metadata:
            metadata_path = asset.get("metadata_path")
            if self._missing(metadata_path) or not self._regular_file(Path(str(metadata_path))):
                self._add(code, "checkpoint.metadata_path 不存在或不是一般檔案", codes, diagnostics)
            else:
                try:
                    self.validate_checkpoint_metadata(json.loads(Path(str(metadata_path)).read_text(encoding="utf-8")))
                except (OSError, json.JSONDecodeError, ValueError) as error:
                    self._add(code, f"checkpoint metadata schema 無法驗證: {error}", codes, diagnostics)

    def _validate_dataset(self, dataset: dict[str, Any], codes: list[str], diagnostics: list[str]) -> None:
        required = ("manifest_path", "license", "provenance_evidence")
        if self._missing_values(dataset, required, "BLOCKED_DATA_CONTRACT", codes, diagnostics):
            return
        manifest = Path(str(dataset["manifest_path"]))
        if not self._regular_file(manifest):
            self._add("BLOCKED_DATA_CONTRACT", "dataset.manifest_path 不存在或不是一般檔案", codes, diagnostics)
        else:
            try:
                self.validate_dataset_manifest(json.loads(manifest.read_text(encoding="utf-8")))
            except (OSError, json.JSONDecodeError, ValueError) as error:
                self._add("BLOCKED_DATA_CONTRACT", f"dataset manifest schema 無法驗證: {error}", codes, diagnostics)
        if not self._evidence_exists(dataset["provenance_evidence"]):
            self._add("BLOCKED_DATA_CONTRACT", "dataset.provenance_evidence 不存在或不是 HTTPS/local file", codes, diagnostics)

    def _validate_licenses(self, codes: list[str], diagnostics: list[str]) -> None:
        for scope in ("source", "checkpoint", "vae", "dataset"):
            if self._missing(self.values[scope].get("license")):
                self._add("BLOCKED_LICENSE", f"{scope}.license 缺少非空值", codes, diagnostics)

    def _missing_values(self, values: dict[str, Any], fields: tuple[str, ...], code: str, codes: list[str], diagnostics: list[str]) -> bool:
        absent = [field for field in fields if self._missing(values.get(field))]
        if absent:
            self._add(code, f"缺少已驗證欄位: {', '.join(absent)}", codes, diagnostics)
        return bool(absent)

    def _require(self, fields: tuple[str, ...], code: str, codes: list[str], diagnostics: list[str]) -> None:
        absent = [field for field in fields if self._missing(self.values.get(field))]
        if absent:
            self._add(code, f"缺少已驗證欄位: {', '.join(absent)}", codes, diagnostics)

    @staticmethod
    def _missing(value: Any) -> bool:
        return value is None or (isinstance(value, str) and not value.strip())

    @staticmethod
    def _regular_file(path: Path) -> bool:
        return path.is_file() and not path.is_symlink()

    @classmethod
    def _evidence_exists(cls, value: Any) -> bool:
        if not isinstance(value, str) or not value.strip():
            return False
        return value.startswith("https://") or cls._regular_file(Path(value))

    @staticmethod
    def _add(code: str, message: str, codes: list[str], diagnostics: list[str]) -> None:
        if code not in codes:
            codes.append(code)
        diagnostics.append(f"{code}: {message}")
