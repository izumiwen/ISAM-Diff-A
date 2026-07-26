# A_environment_and_asset_candidate_discovery_20260726：固定環境與官方資產候選發現

- 日期：2026-07-26
- 計畫類型：Engineering Discovery
- 狀態：Approved
- 上位計畫：附件 `ISAM-A`（`A_feasibility_and_contract_plan.md`）之 A0：資產、來源與方法契約
- 前序證據：[A_feasibility_contract_discovery_20260726 計劃](A_feasibility_contract_discovery_20260726_plan.md)、[實作稽核（INCOMPLETE／CONTRACT_ESCALATION）](../audits/A_feasibility_contract_discovery_20260726_implementation_audit.md)、[實驗帳本](../experiment_log.md)
- 授權依據：使用者已授權本專案固定使用 project-local `env/`，並授權代理查找 ZigMa 等資產的官方候選、交由使用者決定。使用者尚未授權 Git 初始化、source clone／下載、checkpoint／VAE／資料的選定或下載，亦未明確授權補發前序 registry 修復額度。

## 目標

在不改變研究底座與不取得大型資產的條件下，完成兩件可稽核的工程前置工作：

1. 建立或確認唯一的專案本機 Python 環境 `env/`，記錄可重現的建立命令、Python 與 pip 基線 fingerprint；不安裝未明示的研究依賴。
2. 查找並保存官方 ZigMa source、論文、checkpoint metadata，以及原配 VAE／資料來源所需的候選 URL 證據與差異，供使用者選定唯一資產契約。

本階段只可支持「固定環境的基線已被如實記錄」與「候選已提交使用者決定」；不是 A0 strict-load／contract formalization，不產生模型、資料或研究證據。

## 凍結的研究邊界

- 凍結研究問題、baseline、模型架構、checkpoint 身分、VAE、transport、conditioning、資料來源與 split、主要指標、門檻與 ISAM-A 的 A1--A4 範圍。
- 不選定任何候選，不宣稱候選相容、官方、可用、已授權或可重現；在使用者選定且後續獨立驗證前，所有候選均為 **Unproven**。
- 禁止訓練、fine-tuning、推論、評估、dataset validation、strict-load、VAE encode/decode、forward、ODE、tensor／hook／scan 檢查與任何研究指標。
- 禁止 `git init`、匯入 Git 歷史、將本治理工作區冒充 ZigMa source、clone source、下載論文／程式／checkpoint／VAE／資料、建立或選擇 cache、及任何外部上傳或發佈。
- 禁止安裝、升級或鎖定 PyTorch、CUDA、driver、系統套件或任何未由使用者明示且已選定的研究依賴；禁止 CPU fallback 或裝置相容性宣稱。
- 前序 audit 的 `CONTRACT_ESCALATION`（registry 的 checksum／大小／license／provenance／schema 驗證與 repair-evidence 缺口）**不在本階段的修復範圍**。不得修改 registry、schema、CLI、測試、歷史 receipt、前序計劃、audit 或實驗帳本，也不得以新 `env/`、候選 URL 或新輸出冒充該修復的證據。

## 起始狀態與假設

| 項目 | 已觀測證據 | 本計畫處置 |
|---|---|---|
| Git | `git status --short --branch` 回報 `fatal: not a git repository` | 只保留 probe；不初始化 Git。 |
| 前序 bootstrap | 稽核確認第二份 receipt 完整，但 registry 靜態驗證與 repair budget 稽核不足 | 保持 **INCOMPLETE**；不修復。 |
| `env/` | 前序稽核時未建立，且系統 Python 沒有 pip | 先重新 probe；僅建立唯一 `env/` 或記錄既有者。 |
| 研究資產 | 工作區未有可驗證 source、checkpoint、VAE、資料或 manifest | 僅收集外部候選的 URL-level 證據，交由使用者選擇。 |

「project-local `env/` 固定使用」指環境位置固定為工作區根目錄的 `env/`，不代表現有系統 Python、CUDA、PyTorch 或未來依賴版本已獲選定或已相容。

## Discovery Envelope 與允許工作

### 1. 唯一 `env/` 基線

Developer 僅可先 probe `/usr/bin/python3`、`venv`、`ensurepip`、現有 `env/` 與 pip 可用性，並保存原始 stdout、stderr、exit code 與版本輸出。

- 若 `env/` 不存在，僅可一次以已記錄的 Python 執行 `python -m venv env`；該 Python 的完整版本與二進位路徑必須寫入 receipt。
- 若 `env/` 已存在，絕不可刪除、重建、移動或覆寫；僅可 fingerprint 其 Python 與 pip。若它不是由已記錄的 Python 建立、無法啟動或無 pip，結果為 `ENVIRONMENT_BLOCKED`，不得建立第二個 `.venv/`、`venv/` 或替代環境。
- 可使用 venv 內建的 pip 基礎工具，並記錄其版本與 `pip list --format=freeze` 基線；不得 `pip install`、`pip upgrade`、下載 wheel、產生研究依賴 lock，或將 pip baseline 誤稱為 dependency lock。
- 唯一允許的環境候選是工作區根目錄 `env/` 加上已 probe 的系統 Python；不得嘗試 Conda、uv、Poetry、Docker、其他 Python、CPU/GPU runtime 或第二個 virtual environment。

### 2. 官方候選 URL 證據

Developer 可使用可追溯的唯讀網頁／metadata 查找，僅查找下列四類候選，並在 receipt 中記錄查詢字串、存取時間（UTC）、URL、頁面／發布者可辨識名稱、可見的 release／commit／revision／license 指標、HTTP 或工具診斷，以及「未驗證」欄位。不得下載、clone、快取或解析任何模型、source tree、PDF 或資料檔。

| 類別 | 可列候選 | 必要候選證據 | 不可推定事項 |
|---|---|---|---|
| ZigMa source | 作者／組織明示的 repository 或 release 頁面 | repository URL、擁有者／發布者、可見 commit/tag/release 與 license 指標 URL | 唯一 commit、tree hash、working-tree 狀態、程式相容性 |
| ZigMa 論文 | 作者、arXiv 或正式出版頁 | 論文 landing-page URL、版本／日期與與 ZigMa 關聯的可見資料 | 實作、checkpoint 或 sampler 設定等同論文描述 |
| checkpoint metadata | source 作者或所連結正式 hosting 的 model-card／release metadata 頁 | URL、checkpoint ID／檔名、宣稱 domain／resolution／license 指標、連回 source／paper 的連結 | 檔案 hash、大小、可下載性、strict-load、VAE／conditioning 相容性 |
| 原配 VAE 與資料候選 | checkpoint metadata 或官方 source 明示的上游頁面／資料頁 | URL、ID／revision（若可見）、license／使用條件指標與關聯說明 | VAE hash、latent scaling、資料 manifest、任何 split 或取得授權 |

搜尋輸出必須清楚區分「第一方／作者連結」與「第三方索引或鏡像」。第三方頁面只可作線索，不得作為官方性或契約一致性的證明。若無法取得第一方候選，保持相應 `BLOCKED_*` 狀態，不得以名稱相近資產替代。

## 禁止 Fallback 與 machine-readable 狀態

| 條件 | 必要狀態 | 禁止 fallback |
|---|---|---|
| 無法建立或 fingerprint 唯一 `env/` | `ENVIRONMENT_BLOCKED` | 第二個 env、安裝系統 pip、改用 Conda／其他 Python。 |
| 無作者／組織可辨識的 ZigMa source 候選 | `BLOCKED_SOURCE_AMBIGUITY` | GitHub 搜尋結果、治理工作區或 fork 冒充官方 source。 |
| 無可辨識 checkpoint metadata／license | `BLOCKED_CHECKPOINT_IDENTITY`、必要時 `BLOCKED_LICENSE` | 依論文名稱選用另一資料域 checkpoint。 |
| 無原配 VAE 或 scaling 證據 | `BLOCKED_VAE_IDENTITY` | 任意 Stable Diffusion VAE 或慣例 scaling。 |
| 無 source／metadata 的 transport 或 conditioning 佐證 | `BLOCKED_TRANSPORT_CONTRACT`、`BLOCKED_CONDITIONING_CONTRACT` | 由 SiT 或函式名稱推定 ZigMa 的實際設定。 |
| 無資料來源／license／manifest | `BLOCKED_DATA_CONTRACT`、必要時 `BLOCKED_LICENSE` | 選擇、下載、抽樣或合成資料。 |

## 可重現產物與目錄映射

每次開發執行必須使用新的、不存在的目錄；不得覆寫前序 receipt：

```text
outputs/A_environment_and_asset_candidate_discovery_20260726_<timestamp>/
├── run_metadata.json
├── environment_fingerprint.json
├── pip_baseline.txt
├── asset_candidate_evidence.json
├── asset_candidate_comparison.md
├── compatibility_handoff.md
├── diagnostics/
│   ├── 00_preflight_and_git_probe.{stdout,stderr,exitcode}
│   ├── 01_env_creation_or_existing_env_probe.{stdout,stderr,exitcode}
│   ├── 02_env_python_and_pip_fingerprint.{stdout,stderr,exitcode}
│   ├── 03_official_candidate_discovery.{stdout,stderr,exitcode}
│   └── repair_attempt_<n>.*
└── checksums.sha256
```

`asset_candidate_evidence.json` 的每筆候選至少包含：`category`、`url`、`retrieved_at_utc`、`query_or_referrer`、`publisher_or_owner`、`first_party_status`、`visible_identifiers`、`license_evidence_url`、`source_relation_url`、`raw_diagnostic_path`、`unverified_fields`。不可用猜測值填補欄位；未知值為 `null`，且須附 blocked code。

`environment_fingerprint.json` 至少包含：`env_path`、建立或既有狀態、建立命令（若執行）、Python binary／version、venv／ensurepip probe、pip version、pip baseline checksum、OS／host probe、Git probe、CUDA／PyTorch「未安裝／未探測」狀態，以及明確的 lock 狀態。它不得記錄或宣稱 checkpoint、模型或 GPU 相容性。

## 有限 Local-repair Authority 與預算

本計畫只授權與 `env/` 的單一建立流程及 receipt 輸出直接相關的局部修復，且不得修改任何前序 bootstrap 或 registry 路徑。

- 最多 1 次 local repair attempt，且只限於已重現的 `env/` 建立命令、receipt 路徑、fingerprint 命令或候選證據序列化缺陷。
- 最多 45 分鐘累積 discovery 執行時間。
- 最多 4 項短 smoke checks（如下）；`env/` 建立或既有環境驗證合計只可嘗試一次。
- 官方候選查找最多四個類別，每類最多三個 URL；到達上限即提交現有候選，不得擴張到其他模型、VAE、資料或工具鏈。

每次 repair 必須先保存可重現的失敗診斷，再保存修復命令、變更說明、exit code、最小 regression check 與累積預算。需要安裝依賴、重建 env、變更 Python／CUDA／PyTorch／系統環境、修改 registry/schema/CLI/test、擴張候選類別，或任何資產選擇時，一律停止並升級。

## 必要 Smoke Checks 與驗證方法

以下皆為非正式工程 smoke checks，不可作為研究證據：

1. **Preflight／唯一性**：確認 `env/`、`.venv/`、`venv/` 的存在狀態，並記錄 Git、Python、venv、ensurepip probe；驗證未建立替代環境。
2. **環境建立或既有 fingerprint**：一次建立 `env/` 或僅 probe 既有 `env/`；驗證 `env/bin/python --version` 與 `env/bin/python -m pip --version` 的結果如實寫入，無任何額外 dependency 安裝。
3. **環境可重現描述完整性**：驗證 fingerprint、pip baseline、建立命令／狀態、checksum 與 `ENVIRONMENT_BLOCKED`（若適用）相互一致；`pip baseline` 不得標示為 lock。
4. **候選證據完整性**：驗證每一 URL record 有 UTC 時間、原始診斷、第一方狀態、未知欄位與對應 blocked code；驗證沒有下載、clone、模型載入或資產選定的命令。

## 成功條件與 compatibility handoff

工程稽核者只能在下列條件全部成立時，將本計畫判為 **ACCEPTED**；此接受只表示環境基線與候選決策交接完整，不表示 A0 或任何研究假設成立：

- 僅有工作區根目錄 `env/` 作為專案環境，或其無法建立／使用的 `ENVIRONMENT_BLOCKED` 證據完整；沒有第二個環境或未記錄的依賴安裝。
- `env/` 的 Python、venv、ensurepip、pip、pip baseline、建立命令（如有）與 checksums 可由獨立稽核重驗。
- 每類候選的 URL-level evidence 及其限制清楚，沒有將第三方索引、論文敘述或推測資料冒充官方／相容／已選定資產。
- `compatibility_handoff.md` 列出環境 fingerprint、pip／lock 狀態、Git 未初始化狀態、候選清單、各資產欄位仍缺的 evidence、所有 blocked code、四項 smoke check、未執行事項、前序 registry audit 仍為 `CONTRACT_ESCALATION` 的界線，以及使用者待決事項。
- 沒有下載、clone、Git init、依賴安裝、模型／資料操作或修改前序檔案的證據。

無論 audit 結果為何，A0 strict-load、source tree hash、checkpoint／VAE hash 與大小、latent scaling、transport／conditioning、dataset manifest／split、深度學習 dependency lock 與 CUDA/PyTorch 相容性都維持 **Unproven** 或 **Blocked**。

## 停止與升級條件

| 情況 | 必要處置 |
|---|---|
| `env/` 已存在但壞損、與記錄 Python 不一致或缺 pip | 保存診斷，標記 `ENVIRONMENT_BLOCKED`；不重建或替代。 |
| `python -m venv env` 失敗或 require system package／network | 保存診斷，標記 `ENVIRONMENT_BLOCKED`；不安裝或修復系統。 |
| 需要任一研究依賴或 lock 以繼續 | 停止，要求使用者先選定 source／asset 與依賴契約；另立或修訂計劃。 |
| 候選來源不一致、無第一方關聯、license 不明或超過 URL 預算 | 保留候選差異與 `BLOCKED_*`；提交使用者決定，不擴搜或選定。 |
| 需要 clone、下載、Git init、選定 source/checkpoint/VAE/資料、資料 split 或 GPU／CPU 選擇 | 停止並向使用者詢問明確授權。 |
| 發現要修復前序 registry audit 缺口 | 停止；此計畫不提供修復額度。須由 planner 另提已明示 repair authority 的計劃。 |
| 達任一 repair、時間、smoke-check 或 URL 預算 | 保存所有診斷並停止，不得改變候選或環境繞過。 |

## 使用者下一個決策

完成候選交接後，使用者必須以可辨識的 URL／release／commit／ID 決定下列事項；代理不得替代決定：

1. 唯一官方 ZigMa source URL 與 tag／release／commit（並是否授權 clone／下載）。
2. 唯一 checkpoint ID／檔案、取得方式與 license。
3. 原配 VAE 的 ID、revision、權重／license 與是否允許取得其 metadata／檔案。
4. 資料來源、license、manifest，以及 smoke／pilot／holdout split。
5. 是否授權 Git 初始化或提供既有歷史來源；目前答案仍為未授權。
6. 選定 source 後，是否授權針對該明示依賴契約安裝並鎖定依賴；目前不因建立 `env/` 而自動授權。
7. 是否另行授權針對前序 audit 的 `CONTRACT_ESCALATION` 補發有邊界的 registry 修復額度。

## 預定角色與記錄

1. Developer 只能依本 Approved 計劃建立／fingerprint `env/`、收集 URL-level 候選證據並保存新的 receipt。
2. 獨立 Engineering Auditor 僅檢查本計畫的環境唯一性、禁止行為、候選證據、預算與 handoff，不修復任何檔案。
3. 獨立 Recorder 僅依 audit 實際結果追加實驗帳本並建立 implementation archive dossier；本 planner 不執行開發、稽核或記錄。

在獨立 engineering audit 前，本階段所有結論僅為 **Observed**、**Unproven** 或 **Blocked**；不得使用 **Supported** 描述研究結論。
