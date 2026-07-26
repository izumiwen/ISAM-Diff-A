#!/usr/bin/env python3
"""建立無研究副作用的 bootstrap receipt。"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from project_name.bootstrap import prepare_run


PROJECT_REMOTE = "https://github.com/izumiwen/ISAM-Diff-A.git"


def _run(command: list[str]) -> dict[str, object]:
    result = subprocess.run(command, capture_output=True, text=True, check=False)
    return {
        "command": command,
        "exit_code": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
    }


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _write_checksums(output_dir: Path) -> None:
    rows = []
    for path in sorted(item for item in output_dir.rglob("*") if item.is_file() and item.name != "checksums.sha256"):
        rows.append(f"{_sha256(path)}  {path.relative_to(output_dir)}")
    (output_dir / "checksums.sha256").write_text("\n".join(rows) + "\n", encoding="utf-8")


def capture_git_preflight(output_dir: Path) -> dict[str, object]:
    """保存初始 Git 操作前的原始安全檢查；不初始化或改動 Git。"""
    if output_dir.exists():
        raise FileExistsError(f"拒絕覆寫既有 output 目錄: {output_dir}")
    output_dir.mkdir(parents=True, exist_ok=False)
    diagnostics = output_dir / "diagnostics"
    diagnostics.mkdir()
    probes = {
        "git_status": _run(["git", "-C", str(ROOT), "status", "--short", "--branch"]),
        "user_name": _run(["git", "config", "--get", "user.name"]),
        "user_email": _run(["git", "config", "--get", "user.email"]),
        "remote_refs": _run(["git", "ls-remote", "--heads", "--tags", PROJECT_REMOTE]),
    }
    for name, result in probes.items():
        (diagnostics / f"00_git_remote_safety_{name}.stdout").write_text(str(result["stdout"]), encoding="utf-8")
        (diagnostics / f"00_git_remote_safety_{name}.stderr").write_text(str(result["stderr"]), encoding="utf-8")
        (diagnostics / f"00_git_remote_safety_{name}.exitcode").write_text(f"{result['exit_code']}\n", encoding="utf-8")
    payload = {
        "format_version": "1.0",
        "created_at_utc": datetime.now(UTC).isoformat(),
        "project_root": str(ROOT),
        "project_remote": PROJECT_REMOTE,
        "git_directory_present": (ROOT / ".git").exists(),
        "probes": probes,
        "operation": "preflight_only_no_git_init_or_push",
    }
    (output_dir / "git_remote_safety.json").write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (output_dir / "run_metadata.json").write_text(
        json.dumps(
            {
                "experiment_id": "A_source_git_registry_discovery_20260726",
                "created_at_utc": payload["created_at_utc"],
                "operation": payload["operation"],
                "raw_diagnostic_directory": "diagnostics",
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    _write_checksums(output_dir)
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(description="只建立新的 bootstrap receipt；既有目錄會被拒絕。")
    parser.add_argument("--prepare-run", action="store_true", help="建立新的 output receipt；不執行研究工作。")
    parser.add_argument("--capture-git-preflight", action="store_true", help="保存 Git 初始化前的原始安全檢查；不初始化或推送。")
    parser.add_argument("--config", type=Path, default=ROOT / "configs" / "base.yaml", help="JSON-in-YAML 設定檔路徑。")
    parser.add_argument("--output-dir", type=Path, help="必須尚不存在的 output 目錄。")
    args = parser.parse_args()
    if args.prepare_run == args.capture_git_preflight:
        parser.error("必須且只能指定 --prepare-run 或 --capture-git-preflight。")
    if args.output_dir is None:
        parser.error("所選操作需要 --output-dir")
    try:
        if args.capture_git_preflight:
            metadata = capture_git_preflight(args.output_dir)
        else:
            metadata = prepare_run(args.config, args.output_dir, sys.argv)
    except (FileExistsError, ValueError, OSError) as error:
        print(f"BLOCKED: {error}", file=sys.stderr)
        return 2
    print(f"OBSERVED: receipt 已建立於 {args.output_dir}")
    if "blocked_codes" in metadata:
        print("BLOCKED: " + ", ".join(metadata["blocked_codes"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
