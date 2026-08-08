# 報告導覽

本目錄保存可追溯的研究決策與實驗證據；歷史計畫、結果、稽核與 output 不得覆寫、搬移或刪除。事件是否需要記帳或封存，依 [`../docs/experiment_protocol.md`](../docs/experiment_protocol.md) 的 material trigger 判定。

| 路徑 | 用途 |
|---|---|
| [`experiment_log.md`](experiment_log.md) | 附加式帳本；只記錄 Formal Experiment 授權/實質開始/終態、獨立研究稽核、accepted engineering compatibility handoff 與改變研究決策的重大證據 |
| [`plans/`](plans/) | Formal Experiment 與需要時的 Engineering Discovery Plan |
| [`plans/template_plan.md`](plans/template_plan.md) | 建立實驗計畫的範本 |
| [`results/`](results/) | 已開始產生正式研究證據的 Formal Experiment 結果 |
| [`results/template_result.md`](results/template_result.md) | 建立結果報告的範本 |
| [`audits/`](audits/) | 工程與研究稽核；角色獨立性與狀態定義見 `docs/subagent_workflow.md` |
| [`accepted/`](accepted/) | 僅收錄獨立 Research Audit 為 **ACCEPTED** 的 Formal Experiment |
| [`archive/README.md`](archive/README.md) | material outcome 的封存路徑與 dossier 規則 |
| [`templates/`](templates/) | 實驗帳本、決策、失敗分類與最終主張的可重複使用格式 |
| [`decisions/`](decisions/) | 影響研究設計的獨立決策紀錄 |

## 使用規則

1. Formal Experiment 先建立 `plans/{experiment_id}_plan.md`；例行局部修復不必為了文件形式而新建計畫。
2. 所有正式 run 使用唯一的 `outputs/<run_id>/`，保存設定、環境、命令、資料/模型來源、日誌、指標與 checkpoint 的可追溯證據。
3. 結束後依需要建立 `results/{experiment_id}_result.md`，如實區分 **Observed**、**Supported**、**Unproven** 與 **Blocked**。
4. 工程與研究稽核的角色、必要獨立性及 status，依 [`docs/subagent_workflow.md`](../docs/subagent_workflow.md)；工程 readiness 不能替代研究 acceptance。
5. 僅在 material trigger 發生時追加 `experiment_log.md` 或建立 archive dossier；中間診斷、局部修復、格式修正與重複 smoke test 不各自記帳或封存。

只有獨立 Research Audit 的 **ACCEPTED** 可進入 `accepted/` 並支持完成的研究主張。
