# 報告導覽

本目錄保存可追溯的研究決策與實驗證據；歷史計畫、結果與稽核結論不得覆寫或刪除。

| 路徑 | 用途 |
|---|---|
| [`experiment_log.md`](experiment_log.md) | 附加式研究帳本；記錄正式實驗的規劃、開始、結束、稽核與影響研究決策的新證據 |
| [`plans/`](plans/) | 每個正式實驗各自一份計畫 |
| [`plans/template_plan.md`](plans/template_plan.md) | 建立實驗計畫的範本 |
| [`results/`](results/) | 每個完成、中止、失敗或中斷的 run 結果 |
| [`results/template_result.md`](results/template_result.md) | 建立結果報告的範本 |
| [`audits/`](audits/) | 由未參與規劃或執行的獨立稽核者撰寫驗收報告 |
| [`templates/`](templates/) | 實驗帳本、決策、失敗分類與最終主張的可重複使用格式 |
| [`decisions/`](decisions/) | 影響研究設計的獨立決策紀錄 |

## 命名與流程

1. 先建立 `plans/{experiment_id}_plan.md`，明確寫出目標、資料與 split、baseline、指標、成功條件與停止條件。
2. 執行期間，所有產物保留在唯一的 `outputs/<run_id>/` 目錄；解析後設定、環境資訊、日誌、指標與 checkpoint 需可回溯。
3. 結束後建立 `results/{experiment_id}_result.md`，如實記錄結果及其限制；不得把 **Observed** 或 **Unproven** 寫成 **Supported**。
4. 獨立稽核者在 `audits/{experiment_id}_audit.md` 記錄驗收；詳細角色邊界見 [`docs/subagent_workflow.md`](../docs/subagent_workflow.md)。
5. 將正式事件與影響研究決策的新證據附加到 `experiment_log.md`；日常文件整理不記入帳本。

目前尚無正式實驗紀錄。此狀態是 **Observed**，不代表研究設計已核准或結果已被支持。
