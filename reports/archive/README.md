# 封存 Dossier 結構

本目錄只保存 `docs/experiment_protocol.md` 定義的 material outcome；中間局部修復失敗、重複 smoke test、非重大發現與格式修正不各自建立 dossier。

| 類型 | 路徑 |
|---|---|
| 已接受的工程相容性 handoff、重大工程 blocker/incident 或目標環境/工具鏈 transition | `implementation/{status}/{experiment_id}/` |
| Formal Experiment `Blocked` 或 Research Audit **BLOCKED** | `blocked/{experiment_id}/` |
| 研究稽核 **REJECTED** | `rejected/{experiment_id}/` |
| 研究稽核 **INCOMPLETE** | `incomplete/{experiment_id}/` |
| Formal Experiment `Failure` 或 `Interrupted` | `failed/{experiment_id}/` |

每個 dossier 必須記錄精確狀態、其 materiality、canonical 計畫/結果/稽核/output 的路徑及必要後續工作。dossier 只能連結既有證據，不得搬移、覆寫、補寫或重新詮釋 canonical artifacts。
