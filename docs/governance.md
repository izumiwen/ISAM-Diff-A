# 專案治理總覽

> 本文件是 non-normative navigation overview，不是獨立規則來源。
> 規範性要求只由根目錄 `AGENTS.md`、`docs/experiment_protocol.md`、
> `docs/subagent_workflow.md` 與 `docs/run_standard.md` 定義。

本文件只協助選擇正確的治理入口，不重複實驗生命週期、角色限制、run 要求、稽核狀態、帳本觸發或封存規則。若本文件與 canonical 文件有差異，以負責該主題的 canonical 文件為準。

## Canonical 文件責任

| 文件 | 責任範圍 |
|---|---|
| `AGENTS.md` | repository-wide 工作邊界、權限、不可違反的研究規則與規則優先順序 |
| `docs/experiment_protocol.md` | Formal/非正式範圍、material deviation、研究證據、接受、帳本與封存觸發 |
| `docs/subagent_workflow.md` | 角色分工、角色組合、獨立性、委派順序與稽核狀態 |
| `docs/run_standard.md` | run 身分、執行證據、retry、資料執行安全與環境/工具鏈操作 |

同一主題出現重疊時，使用負責該主題的文件，不把所有要求累加成更嚴格的新規則。

## 工作入口

| 工作類型 | 入口 |
|---|---|
| 例行工程或已授權的局部修復 | `AGENTS.md`，再依實際風險讀取相關 canonical 文件 |
| Engineering Discovery | `docs/experiment_protocol.md` 與 `docs/subagent_workflow.md`；涉及環境、工具鏈或 final compatibility handoff 時再讀 `docs/run_standard.md` |
| Formal Experiment 規劃 | `AGENTS.md`、`docs/experiment_protocol.md` 與最新相關帳本；若委派規劃再讀 `docs/subagent_workflow.md` |
| Formal Experiment 執行 | `AGENTS.md`、三份 canonical 細則與最新相關帳本 |
| 工程或研究稽核 | `docs/subagent_workflow.md`，並依稽核範圍讀取 experiment/run 規範 |
| 帳本、accepted surface 或 archive dossier | `docs/experiment_protocol.md`、`docs/subagent_workflow.md` 與 `reports/archive/README.md` |

## 文件與證據位置

| 路徑 | 用途 |
|---|---|
| `reports/plans/` | Formal Experiment 或必要的 Engineering Discovery 計畫 |
| `reports/results/` | 已開始產生正式研究證據的 Formal Experiment 結果 |
| `reports/audits/` | Engineering Audit 與 Research Audit |
| `reports/experiment_log.md` | append-only、只記錄 meaningful research events 與 decision-changing blockers 的精簡帳本 |
| `reports/accepted/` | 僅供獨立 Research Audit 為 **ACCEPTED** 的 Formal Experiment |
| `reports/archive/` | 符合 material trigger 的工程或正式研究 outcome dossier |
| `outputs/` | run 與診斷的原始執行產物；不以治理摘要取代 |

`governance/` 是舊版治理文件的歷史快照，不屬於目前 canonical governance set，也不應作為現行代理工作的規則來源。
