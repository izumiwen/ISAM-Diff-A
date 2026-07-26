"""建立可稽核但不執行研究工作的 discovery run receipt。"""

from __future__ import annotations

import hashlib
import json
import platform
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Sequence

from .registry import ASSET_FIELDS, AssetRegistry


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_config(config_path: Path) -> dict[str, Any]:
    """讀取 JSON-in-YAML；拒絕任何未確認研究值。"""
    try:
        config = json.loads(config_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError(f"無法解析只限 JSON 子集的設定檔: {error}") from error
    fields = config.get("research_contract", {}).get("fields")
    if config.get("research_contract", {}).get("status") != "blocked" or not isinstance(fields, dict):
        raise ValueError("research_contract 必須明確為 blocked")
    missing = set(ASSET_FIELDS) - set(fields)
    unknown = set(fields) - set(ASSET_FIELDS)
    if missing or unknown or any(value is not None for value in fields.values()):
        raise ValueError("研究契約欄位必須完整且全部為 null")
    return config


def _git_probe(project_root: Path) -> dict[str, Any]:
    result = subprocess.run(
        ["git", "-C", str(project_root), "rev-parse", "--is-inside-work-tree"],
        capture_output=True,
        text=True,
        check=False,
    )
    return {"command": result.args, "exit_code": result.returncode, "stdout": result.stdout, "stderr": result.stderr}


def _write_diagnostic(directory: Path, name: str, stdout: str, stderr: str, exit_code: int) -> list[str]:
    directory.mkdir(parents=True, exist_ok=True)
    (directory / f"{name}.stdout").write_text(stdout, encoding="utf-8")
    (directory / f"{name}.stderr").write_text(stderr, encoding="utf-8")
    (directory / f"{name}.exitcode").write_text(f"{exit_code}\n", encoding="utf-8")
    return [str(Path("diagnostics") / f"{name}.{extension}") for extension in ("stdout", "stderr", "exitcode")]


def _write_checksums(output_dir: Path) -> None:
    entries = []
    for path in sorted(item for item in output_dir.rglob("*") if item.is_file() and item.name != "checksums.sha256"):
        entries.append(f"{sha256_file(path)}  {path.relative_to(output_dir)}")
    (output_dir / "checksums.sha256").write_text("\n".join(entries) + "\n", encoding="utf-8")


def prepare_run(config_path: Path, output_dir: Path, command: Sequence[str]) -> dict[str, Any]:
    """只在全新的目錄寫入 receipt；絕不覆寫或啟動模型。"""
    if output_dir.exists():
        raise FileExistsError(f"拒絕覆寫既有 output 目錄: {output_dir}")
    config = load_config(config_path)
    output_dir.mkdir(parents=True, exist_ok=False)
    project_root = config_path.resolve().parents[1]
    diagnostics_dir = output_dir / "diagnostics"
    git_probe = _git_probe(project_root)
    inventory = "\n".join(
        [
            f"project_root={project_root}",
            "git_repository=false" if git_probe["exit_code"] else "git_repository=true",
            f"python={sys.version}",
            "pip_status=blocked_not_probed_for_installation",
            "asset_status=blocked_no_registry_evidence",
        ]
    ) + "\n"
    diagnostic_paths = _write_diagnostic(
        diagnostics_dir,
        "00_workspace_inventory",
        inventory + "git_stdout:\n" + git_probe["stdout"],
        git_probe["stderr"],
        git_probe["exit_code"],
    )
    import venv
    import ensurepip

    venv_probe = f"venv_module={venv.__file__}\nensurepip_module={ensurepip.__file__}\nprobe_only=true\n"
    diagnostic_paths += _write_diagnostic(diagnostics_dir, "01_python_venv_probe", venv_probe, "", 0)
    help_stdout: list[str] = []
    help_stderr: list[str] = []
    help_exit_code = 0
    for script_name in ("audit_project.py", "discover_assets.py"):
        command_for_help = [sys.executable, str(project_root / "scripts" / script_name), "--help"]
        result = subprocess.run(command_for_help, capture_output=True, text=True, check=False)
        help_stdout.append("$ " + " ".join(command_for_help) + "\n" + result.stdout)
        if result.stderr:
            help_stderr.append("$ " + " ".join(command_for_help) + "\n" + result.stderr)
        help_exit_code = max(help_exit_code, result.returncode)
    diagnostic_paths += _write_diagnostic(
        diagnostics_dir,
        "02_cli_help",
        "\n".join(help_stdout),
        "\n".join(help_stderr),
        help_exit_code,
    )
    registry = AssetRegistry.empty().to_dict()
    AssetRegistry.validate_schema_document(registry, AssetRegistry.schema_document())
    diagnostic_paths += _write_diagnostic(
        diagnostics_dir,
        "03_schema_and_receipt_smoke",
        "asset_registry_schema=valid\nconfig_sha256_length=64\noutput_is_new=true\n",
        "",
        0,
    )
    registry["diagnostic_paths"] = diagnostic_paths
    (output_dir / "asset_registry.json").write_text(json.dumps(registry, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (output_dir / "resolved_config.yaml").write_text(json.dumps(config, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    environment = "\n".join(
        [
            f"python_version={sys.version}",
            f"implementation={platform.python_implementation()}",
            f"platform={platform.platform()}",
            "dependency_environment=ENVIRONMENT_BLOCKED (pip/dependencies not installed or changed)",
            "device_probe=not_probed (no CUDA/PyTorch/device selection authorized)",
        ]
    ) + "\n"
    (output_dir / "environment.txt").write_text(environment, encoding="utf-8")
    (output_dir / "contract_diff_table.md").write_text(
        "# Contract difference table\n\n| Contract | Paper evidence | Implementation evidence | Checkpoint evidence | Status |\n|---|---|---|---|---|\n"
        "| Source, checkpoint, VAE, transport, conditioning, data | none provided | none provided | none provided | Blocked |\n",
        encoding="utf-8",
    )
    (output_dir / "compatibility_handoff.md").write_text(
        "# Compatibility handoff\n\n"
        "- Status: **Blocked**. This receipt records only a standard-library bootstrap.\n"
        "- Git/source provenance: not a Git repository; no official source evidence.\n"
        "- Assets: source, checkpoint, VAE, transport, conditioning, dataset, and licenses are unprovided.\n"
        f"- Blocked codes: {', '.join(registry['blocked_codes'])}, ENVIRONMENT_BLOCKED.\n"
        f"- Diagnostics: {', '.join(diagnostic_paths)}.\n"
        "- Not executed: downloads, installations, model loading, strict-load, tensors, data validation, training, evaluation, inference.\n"
        "- Required user authorization: choose/provide source, checkpoint, VAE, data/license provenance; authorize Git/environment changes only if desired.\n",
        encoding="utf-8",
    )
    metadata = {
        "format_version": "1.0",
        "experiment_id": config["experiment_id"],
        "created_at_utc": datetime.now(UTC).isoformat(),
        "command": list(command),
        "config_path": str(config_path.resolve()),
        "config_sha256": sha256_file(config_path),
        "python_version": sys.version,
        "git_probe": git_probe,
        "host_probe": {"platform": platform.platform(), "device": "not_probed"},
        "blocked_codes": registry["blocked_codes"] + ["ENVIRONMENT_BLOCKED"],
        "diagnostic_paths": diagnostic_paths,
        "research_execution": "not_executed",
    }
    (output_dir / "run_metadata.json").write_text(json.dumps(metadata, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    _write_checksums(output_dir)
    return metadata
