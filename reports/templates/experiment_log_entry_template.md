# 實驗帳本條目模板

[`../experiment_log.md`](../experiment_log.md) 是精簡、append-only 的研究帳本，不是完整工程 transaction log。只有 `docs/experiment_protocol.md` 定義的 Formal Experiment milestone、獨立 Research Audit、accepted engineering compatibility handoff、material blocker 或 decision-changing evidence 才追加條目。

```md
## YYYY-MM-DD — [Experiment ID or Task ID] — [Status]

- **Objective:**
- **Change or decision:**
- **Evidence:**
- **Interpretation:**
- **Artifacts:**
- **Next action:**
```

不要為 intermediate discovery attempt、局部修復、unit/import/CLI/parser/fixture/smoke failure、格式修正、receipt finalization 或重複狀態更新建立獨立帳本條目。歷史錯誤以新的日期化更正條目處理，不得改寫或刪除原條目。
