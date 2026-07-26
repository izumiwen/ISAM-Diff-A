"""只使用標準函式庫的資產 registry 與 blocked-state 檢查。"""

from __future__ import annotations

import json
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


class AssetRegistry:
    """Registry 不會載入任何資產；僅檢查已提供的靜態宣告。"""

    def __init__(self, values: dict[str, Any] | None = None) -> None:
        self.values = dict(values or {field: None for field in ASSET_FIELDS})

    @classmethod
    def empty(cls) -> "AssetRegistry":
        return cls()

    @classmethod
    def from_path(cls, path: Path) -> "AssetRegistry":
        data = json.loads(path.read_text(encoding="utf-8"))
        cls.validate_schema_document(data, cls.schema_document())
        return cls({field: data[field] for field in ASSET_FIELDS})

    @staticmethod
    def schema_document() -> dict[str, Any]:
        schema_path = Path(__file__).resolve().parents[2] / "references" / "asset_registry.schema.json"
        return json.loads(schema_path.read_text(encoding="utf-8"))

    @staticmethod
    def validate_schema_document(data: dict[str, Any], schema: dict[str, Any]) -> None:
        if not isinstance(data, dict):
            raise ValueError("asset registry 必須是 JSON object")
        required = set(schema["required"])
        properties = schema["properties"]
        missing = sorted(required - set(data))
        unknown = sorted(set(data) - set(properties))
        if missing:
            raise ValueError(f"asset registry 缺少欄位: {', '.join(missing)}")
        if unknown:
            raise ValueError(f"asset registry 不允許未知欄位: {', '.join(unknown)}")
        for field, descriptor in properties.items():
            if field not in data:
                continue
            value = data[field]
            allowed = descriptor["type"]
            allowed_types = set(allowed if isinstance(allowed, list) else [allowed])
            kind = "null" if value is None else "integer" if isinstance(value, int) and not isinstance(value, bool) else "number" if isinstance(value, (int, float)) and not isinstance(value, bool) else "string" if isinstance(value, str) else "object" if isinstance(value, dict) else "array" if isinstance(value, list) else "boolean" if isinstance(value, bool) else "unknown"
            if kind not in allowed_types:
                raise ValueError(f"asset registry 欄位 {field} 型別必須是 {sorted(allowed_types)}")

    def to_dict(self) -> dict[str, Any]:
        result = {field: self.values.get(field) for field in ASSET_FIELDS}
        result.update(self.validate())
        return result

    def validate(self) -> dict[str, Any]:
        codes: list[str] = []
        diagnostics: list[str] = []

        self._require(("repository_url", "source_commit", "source_tree_sha256", "source_dirty_status"), "BLOCKED_SOURCE_AMBIGUITY", codes, diagnostics)
        self._require(("checkpoint_path", "checkpoint_sha256", "checkpoint_size_bytes", "checkpoint_license"), "BLOCKED_CHECKPOINT_IDENTITY", codes, diagnostics)
        checkpoint_path = self.values.get("checkpoint_path")
        if checkpoint_path and not Path(str(checkpoint_path)).is_file():
            self._add("BLOCKED_CHECKPOINT_IDENTITY", "checkpoint_path 不存在或不是一般檔案", codes, diagnostics)

        self._require(("vae_id", "vae_revision", "vae_sha256", "latent_scaling_factor"), "BLOCKED_VAE_IDENTITY", codes, diagnostics)
        self._require(("interpolant", "prediction_parameterization", "time_endpoints", "solver"), "BLOCKED_TRANSPORT_CONTRACT", codes, diagnostics)
        self._require(("conditioning_contract",), "BLOCKED_CONDITIONING_CONTRACT", codes, diagnostics)
        self._require(("dataset_manifest_path",), "BLOCKED_DATA_CONTRACT", codes, diagnostics)
        manifest_path = self.values.get("dataset_manifest_path")
        if manifest_path and not Path(str(manifest_path)).is_file():
            self._add("BLOCKED_DATA_CONTRACT", "dataset_manifest_path 不存在或不是一般檔案", codes, diagnostics)
        self._require(("checkpoint_license", "dataset_license"), "BLOCKED_LICENSE", codes, diagnostics)
        return {"status": "blocked" if codes else "unproven", "blocked_codes": codes, "diagnostics": diagnostics}

    def _require(self, fields: tuple[str, ...], code: str, codes: list[str], diagnostics: list[str]) -> None:
        absent = [field for field in fields if self.values.get(field) is None]
        if absent:
            self._add(code, f"缺少已驗證欄位: {', '.join(absent)}", codes, diagnostics)

    @staticmethod
    def _add(code: str, message: str, codes: list[str], diagnostics: list[str]) -> None:
        if code not in codes:
            codes.append(code)
        diagnostics.append(f"{code}: {message}")
