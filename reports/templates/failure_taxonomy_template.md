# 失敗案例分類模板

每個可重現的失敗案例另存為 `reports/results/{experiment_id}_failure_<number>.md`，並保留其原始 run 與視覺化產物。

```md
# F-<number>: <失敗名稱>

- 類別：
- 資料集與影像 ID：
- 重現命令：
- 預期行為：
- 觀察到的行為：
- No-anchor 輸出：
- Anchored 輸出：
- Ground truth（若有）：
- Difference map 與 state drift 證據：
- 推測機制：
- 已確認機制：
- 嚴重度與發生頻率：
- 已測試的緩解措施：
- 狀態：`Observed | Supported | Unproven | Blocked`
```
