# ISAM-Diff

ISAM-Diff 是深度學習研究專案。此 repository 將程式、設定、治理文件、研究證據與執行產物分開保存，以維持可重現性、來源追溯與研究主張邊界。

## 專案結構

| 路徑 | 用途 |
|---|---|
| [`src/project_name/`](src/project_name/) | 專案 Python package 與研究實作 |
| [`configs/`](configs/README.md) | 可解析的實驗與工程設定 |
| [`scripts/`](scripts/README.md) | 訓練、評估、推論、驗證與稽核入口 |
| [`docs/`](docs/README.md) | Canonical 實驗、角色與 run 治理規範 |
| [`reports/`](reports/README.md) | 計畫、結果、稽核、決策、帳本與 review/archive surface |
| [`references/`](references/) | 資料 manifest 與 checkpoint metadata schema |
| [`tests/`](tests/README.md) | 自動化回歸、契約與 smoke checks |
| `outputs/` | 唯一 run 與診斷產物；不作為版本控制的治理文件 |
| `external_sources/` | 只讀外部來源；不屬於本專案程式碼 |

## 治理入口

先閱讀 [`AGENTS.md`](AGENTS.md)，再依工作責任選擇 canonical 文件：

- Formal/非正式範圍、material deviation、研究證據、接受、帳本與封存觸發：[`docs/experiment_protocol.md`](docs/experiment_protocol.md)
- 角色分工、獨立性、委派順序與稽核狀態：[`docs/subagent_workflow.md`](docs/subagent_workflow.md)
- run 身分、執行證據、retry、資料執行安全與環境/工具鏈操作：[`docs/run_standard.md`](docs/run_standard.md)

[`docs/governance.md`](docs/governance.md) 只提供 non-normative 導覽摘要。`governance/` 保存舊版治理文件，不是現行規則來源。

## 研究證據

Formal Experiment 的計畫、結果與稽核分別保存於 `reports/plans/`、`reports/results/` 與 `reports/audits/`。`reports/experiment_log.md` 是 append-only 的精簡研究帳本；`reports/accepted/` 僅收錄獨立 Research Audit 為 **ACCEPTED** 的正式實驗；符合 material trigger 的其他 outcome 依 [`reports/archive/README.md`](reports/archive/README.md) 封存。

Routine engineering 與已授權的 local repair 不需要為每次嘗試建立新 plan、audit、ledger entry 或 dossier。是否需要升級為 Engineering Discovery 或 Formal Experiment，以 canonical 治理文件的 scope 與 materiality 規則判定。

## 驗證

先使用相關 CLI 的 `--help` 檢查實際可用入口，再執行與變更範圍相稱的最小測試或 smoke check。專案結構與基本治理檢查入口為：

```bash
python3 scripts/audit_project.py --help
```

Python 測試應使用專案既有虛擬環境；若不存在，依 `AGENTS.md` 建立 `env`。
