# 失敗案例分類模板

本範本只用於需要形成長期研究或重大工程證據的 material failure case。Intermediate local repair、routine smoke failure、parser/fixture/Markdown defect、receipt finalization 與 non-blocking audit correction 保留在相關診斷或任務證據中，不各自建立 failure report。

```md
# F-<number>: <失敗名稱>

- 類別：
- 關聯 experiment／run／task：
- Materiality trigger：
- 影響的研究、相容性或 claim boundary：
- 重現命令：
- 預期行為：
- 觀察到的行為：
- 原始診斷與 artifact 路徑：
- 資料、模型、checkpoint、VAE、設定與環境身分（如適用）：
- 推測機制：
- 已確認機制：
- 嚴重度與發生頻率：
- 已測試的緩解措施：
- 狀態：`Observed | Supported | Unproven | Blocked`
- Required follow-up：
```
