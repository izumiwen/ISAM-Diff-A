# A_environment_and_asset_candidate_discovery_20260726：Engineering Discovery 實作稽核

## 稽核狀態

**ACCEPTED**

本接受僅表示 Approved Engineering Discovery 計畫所要求的固定 `env/` 基線、URL-level 候選交接、禁止行為邊界與 receipt 可由獨立稽核重驗。它**不**接受 A0 strict-load、資產相容性、任何模型／資料契約或研究假設。

## 稽核範圍與獨立性

- 稽核對象：`reports/plans/A_environment_and_asset_candidate_discovery_20260726_plan.md`、receipt `outputs/A_environment_and_asset_candidate_discovery_20260726_20260726T080342Z/`，以及其對應的 project-local `env/`。
- 稽核者未參與此階段的規劃或開發；未修復、改動設定、重建環境、安裝依賴、執行 Git 操作、下載資產或執行研究操作。本檔是本次稽核唯一持久化寫入。
- 此工作區尚未是 Git repository，故無法以 Git diff 證明所有歷史檔案變更；本稽核改以 receipt 原始診斷、現在的工作區環境目錄與 checksum 做限定範圍的獨立重驗。

## 已檢視證據

- Approved 計畫：`reports/plans/A_environment_and_asset_candidate_discovery_20260726_plan.md`
- 前序狀態：[A_feasibility_contract_discovery_20260726 實作稽核](A_feasibility_contract_discovery_20260726_implementation_audit.md)（**INCOMPLETE**／`CONTRACT_ESCALATION`）及 `reports/experiment_log.md`
- 本階段 receipt：
  - `run_metadata.json`
  - `environment_fingerprint.json`、`pip_baseline.txt`
  - `asset_candidate_evidence.json`、`asset_candidate_comparison.md`
  - `compatibility_handoff.md`、`checksums.sha256`
  - `diagnostics/00_preflight_and_git_probe.*` 至 `diagnostics/05_candidate_evidence_and_checksum.*`
- 現有環境：`env/pyvenv.cfg`、`env/bin/python`、`env/bin/pip`

## Code and CLI Checks

| 檢查 | 獨立方法 | Observed 結果 |
|---|---|---|
| Git／替代環境現況 | `find . -maxdepth 2 ...`、`git rev-parse --is-inside-work-tree` | 只見 `./env`；`.venv`、`venv` 與 `.git` 均不存在。Git 仍回報 `fatal: not a git repository`。 |
| 唯一環境與建立來源 | 檢視 `env/pyvenv.cfg`、解析 `env/bin/python` | `include-system-site-packages = false`；建立命令是 `/usr/bin/python3 -m venv /home/izumiwen/projects/ISAM-Diff/env`；Python 解析至 `/usr/bin/python3.12`。 |
| 現有 Python／pip fingerprint | `env/bin/python --version`、`env/bin/python -m pip --version`、`... pip list --format=freeze` | Python `3.12.3`、pip `24.0`；freeze 僅有 `pip==24.0`，與 receipt baseline 一致。 |
| 二進位 fingerprint | `sha256sum env/bin/python env/bin/pip` | 分別為 `1643dacd...e61118`、`708512af...f2dc`，與 `environment_fingerprint.json` 一致。 |
| Receipt 完整性 | 在 receipt 目錄執行 `sha256sum -c checksums.sha256` | 24 個列入項目均為 `OK`。 |
| machine-readable receipt contract | 使用 `env/bin/python` 只讀解析三份 JSON | 必要候選欄位、UTC 時間、raw diagnostic path、每個未驗證欄位的 blocked code、0/1 repair budget 與 4/4 smoke budget 均通過斷言。 |

## Configuration Contract

- `environment_fingerprint.json` 的 `environment_status` 是 `CREATED`、`creation_attempt_count` 是 `1`；其 system Python、venv／ensurepip、pip baseline SHA-256、Git probe 與明確的「非 dependency lock」狀態，都可由 receipt 和現有 `env/` 重驗。
- `pip_baseline.txt` 明確標示為觀測基線而非 lock；本稽核的 freeze 亦未發現 pip 之外的已安裝套件。因此本階段沒有把 venv 內建 pip 冒充研究依賴或可重現的深度學習 lock。
- receipt 的 `run_metadata.json` 列出 0 次 repair、4 項 smoke check，未宣稱 CUDA、PyTorch、GPU、checkpoint 或模型相容性。這符合計畫的固定環境邊界。

## Data and Tensor Shape Checks

不適用且未執行。此 Engineering Discovery 明確禁止模型／VAE／資料載入、strict-load、forward、ODE、tensor shape、hook、scan、訓練、推論、評估與 dataset validation；receipt 和本稽核未將任何未執行事項當成已驗證。

## Tests and Smoke Checks

| 計畫 smoke check | 可稽核證據 | 結果 |
|---|---|---|
| 1. Preflight／唯一性 | `diagnostics/00_*` 記錄 preflight 時 `env`、`.venv`、`venv` 皆 absent，並記錄 Python、venv、ensurepip、host 與 Git `not a git repository`；目前目錄重驗只見 `env/`。 | **PASS (Observed)** |
| 2. 唯一環境建立與 fingerprint | `diagnostics/01_*`、`02_*` 均 exit 0；`pyvenv.cfg`、Python/pip 的版本、freeze 與二進位 SHA-256 可在現有 `env/` 重驗。 | **PASS (Observed)** |
| 3. 可重現描述完整性 | `diagnostics/04_*` 為 `receipt-core-consistency=PASS`；本稽核重新驗證所有 24 個 SHA-256，並確認 baseline 非 lock。 | **PASS (Observed)** |
| 4. 候選證據完整性 | `diagnostics/03_*`、`05_*` 與 JSON 重驗顯示每筆 record 均具所需欄位、UTC、原始診斷、第一方界線、未知欄位與 blocked code；`05_*` 為 `candidate-evidence-contract=PASS`。 | **PASS (Observed)** |

## Findings

1. **環境唯一性與無額外依賴安裝已通過本階段重驗。** preflight 記錄三個候選環境均不存在；目前僅有根目錄 `env/`。該環境的 venv 設定、Python/pip 版本、二進位 checksum 與 freeze 都和 receipt 一致，且 freeze 僅有 `pip==24.0`。
2. **禁止 Git／下載／clone／模型動作的範圍證據一致。** receipt 的 raw diagnostics 僅記錄 venv/pip fingerprint 與 URL-level discovery；工作區目前不存在 `.git` 或 source clone 目錄，且 `run_metadata.json`、handoff 和 raw diagnostic 都明確列為未執行 Git init/remote/clone、下載、pip install/upgrade、model/data operation 或研究操作。這是此 receipt 的工程行為證據，不是對外部資產可用性的證明。
3. **URL-level 候選資料完整地維持第一方與未驗證界線。** 共有四個有 URL 的 record（source、paper、checkpoint metadata、dataset），每個類別至多一個 URL；`paired_vae` 是明示的「無第一方候選」record，而非以任意 Stable Diffusion VAE 補替。計畫中的「原配 VAE 與資料」同一候選類別在 JSON 中拆成兩個 record 以分別保存 blocked 狀態，並未增加第五個 URL 類別或超出每類三 URL 的限制。
4. **未把 URL 候選視為選定或相容。** source record 有作者 project page 直接連結與 Apache-2.0 指標，但 selected commit/tree hash/program compatibility 仍是 blocked；paper record 明示不是 source provenance；checkpoint hosting record 因 HTTP 429 保持 model-card、license、hash、size、strict-load 未驗；dataset record 沒有 manifest／split／access-license chain。所有相關欄位均是 `null` 或對應 **Unproven**／**Blocked** code。
5. **AnySearch 與 Hugging Face 的失敗沒有被靜默繞過。** `diagnostics/03_official_candidate_discovery.stderr` 保留 `BLOCKED_ANYSEARCH_SCRIPT_INTEGRITY` 的理由（無可比對的 original manifest/signature/Git worktree，CLI 未執行）以及 Hugging Face HTTP 429。receipt 以使用者授權的唯讀 web fallback 取代搜尋工具，不將 fallback 偽稱為 AnySearch integrity 驗證或 HF metadata 成功。
6. **前序 registry 問題確實隔離。** `compatibility_handoff.md` 及此計畫均保留前序 audit 的 **INCOMPLETE**／`CONTRACT_ESCALATION`；本 receipt 未修改 registry、schema、CLI、測試、歷史 receipt、前序計畫、audit 或實驗帳本，也未將環境／URL evidence 冒充為 registry checksum、大小、license、provenance 或 schema 修復。

## Repair Disposition

不適用：稽核狀態為 **ACCEPTED**，因此不存在非接受狀態所需的唯一 repair disposition。

## Research-Claim Boundary

- **Observed**：單一 project-local `env/` 的 Python/pip 基線、receipt checksum、四項非正式 smoke checks、以及受限的 URL-level 候選交接。
- **Unproven**：唯一 source commit／tree hash、checkpoint 與 VAE 的 hash／大小／license／strict-load、latent scaling、transport、conditioning、dataset manifest／split，以及 CUDA/PyTorch/GPU 相容性。
- **Blocked**：原配 VAE 的第一方 identity、checkpoint hosting metadata 的 HTTP 429 欄位、資料 access-license chain，及未獲選定／授權的 clone、下載、依賴安裝與真正 dependency lock。
- 本工程接受不是任何 A0 strict-load 或研究結果的接受；不得用於方法、指標、模型相容性、資料可用性或論文主張。

## Required Follow-up

1. 由獨立 Recorder 依本 **ACCEPTED** 工程稽核追加 `reports/experiment_log.md`，並建立 `reports/archive/implementation/accepted/A_environment_and_asset_candidate_discovery_20260726/` dossier；不得建立 `reports/accepted/` 的研究接受項目。
2. 請使用者選定唯一 ZigMa source URL 與 commit/tag/release、checkpoint ID／license、原配 VAE identity／revision／license、資料來源／manifest／split，並個別授權 clone/download 或後續 metadata 取得。
3. 在資產與依賴契約被選定後，另行規劃依賴安裝與真正 lock；固定 `env/` 的位置不等同已授權安裝任何研究依賴。
4. 前序 `A_feasibility_contract_discovery_20260726` 的 registry `CONTRACT_ESCALATION` 仍需要另一份取得明示 repair authority 的計畫；本 audit 不解除或修復該缺口。
