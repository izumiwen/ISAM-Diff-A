#!/usr/bin/env python3
"""驗證使用者已提供的 registry，不載入或下載任何資產。"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from project_name.registry import AssetRegistry


def main() -> int:
    parser = argparse.ArgumentParser(description="只驗證已存在 registry 的結構與 blocked 狀態。")
    parser.add_argument("--registry", type=Path, required=True, help="使用者已提供的 asset_registry.json 路徑。")
    parser.add_argument("--output", type=Path, help="尚不存在的 JSON 結果檔；不指定則只印出結果。")
    args = parser.parse_args()
    if args.output is not None and args.output.exists():
        print(f"BLOCKED: 拒絕覆寫既有輸出: {args.output}", file=sys.stderr)
        return 2
    try:
        result = AssetRegistry.from_path(args.registry).to_dict()
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"BLOCKED: registry 無法驗證: {error}", file=sys.stderr)
        return 2
    payload = json.dumps(result, indent=2, sort_keys=True)
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload + "\n", encoding="utf-8")
    print(payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
