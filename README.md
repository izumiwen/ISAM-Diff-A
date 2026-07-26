# project_name

可重現、可擴充的 Python 深度學習研究專案骨架。本階段只提供工程治理、設定、run 產物與稽核工具；沒有模型、資料集、權重或訓練實作。

## 目錄約定

- `src/project_name/`：唯一 Python package；資料、模型、engine、loss、metrics 與工具皆收納於此。
- [`configs/`](configs/README.md)：YAML 設定；`base.yaml` 只含工程預設，研究欄位保持 `blocked` 或 `null`。
- `scripts/`：CLI 入口；訓練、評估與推論會明確拋出 `NotImplementedError`。
- [`docs/`](docs/README.md)：正式實驗、委派與 run 的治理規範。
- [`reports/`](reports/README.md)：實驗帳本、計畫、結果與獨立稽核報告。
- `references/`：資料 manifest 與 checkpoint metadata 的 JSON Schema。
- `tests/`：不依賴模型或資料集的骨架測試。
- `changelogs/`：變更紀錄範本。
- `outputs/`：每次 run 的唯一目錄；不納入 Git。
- `external_sources/`：只讀外部來源參考；不屬於本專案程式碼。固定的 ZigMa clone 位於
  `external_sources/CompVis-zigma/`，必須維持 Git 忽略、detached HEAD 與未修改狀態。

## 文件導覽

| 目的 | 入口 |
|---|---|
| 專案治理、正式實驗與 run 規範 | [`docs/README.md`](docs/README.md) |
| ISAM-Diff 候選研究計畫 | [`docs/isam_diff/README.md`](docs/isam_diff/README.md) |
| 建立或選擇實驗設定 | [`configs/README.md`](configs/README.md) |
| 規劃、記錄及查閱實驗證據 | [`reports/README.md`](reports/README.md) |
| 專案層級工作規則 | [`AGENTS.md`](AGENTS.md) |
| 查閱資料與 checkpoint 中繼資料格式 | [`references/`](references/) |

目前沒有已定義的研究問題、資料集、模型或正式實驗結果；這些狀態在設定與報告中應維持為 **Blocked**，直到有明確且可追溯的決策。

## 最小驗證

目前系統僅有 Python 3；尚未安裝 pip、PyTorch 或 pytest。因此可先執行不依賴第三方套件的命令：

```bash
python3 scripts/train.py --help
python3 scripts/evaluate.py --help
python3 scripts/inference.py --help
python3 scripts/validate_dataset.py --help
python3 scripts/audit_project.py
python3 scripts/train.py --prepare-run --experiment-name dummy
```

最後一個命令只建立獨立 run、`resolved_config.yaml`、`run_metadata.json` 與 `environment.json`，不會訓練。

## 依賴與 lock file

本專案使用 setuptools 的 `pyproject.toml`，其本身沒有原生 lock file；目前環境也沒有 pip、uv、Poetry 或其他可用鎖定工具，且本階段未獲授權安裝它們。因此尚未產生 lock file。

替代方案是在獲得安裝授權後，建立 `env/`，以固定 Python 版本安裝 `pip-tools`，再從 `requirements.txt` 產生並提交 `requirements.lock`；所有正式 run 應記錄該 lock 的雜湊與 Python/CUDA 環境。`requirements.txt` 現為宣告性相依清單，不能單獨保證位元級重現。

## 開始研究前的必要決策

請先明確指定研究問題、資料集與 split、模型/baseline、指標與監測方向、運算資源限制。建立 `reports/plans/{experiment_id}_plan.md` 後，才可實作資料與模型流程。
