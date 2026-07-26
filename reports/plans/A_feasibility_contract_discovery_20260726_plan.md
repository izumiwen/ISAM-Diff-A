# A_feasibility_contract_discovery_20260726：ISAM-A A0 可行性與契約探索

- 日期：2026-07-26
- 計畫類型：Engineering Discovery
- 狀態：Approved
- 上位計畫：附件 `ISAM-A`（`A_feasibility_and_contract_plan.md`）之 A0：資產、來源與方法契約
- 授權依據：使用者已明確要求建立可重現、方便檢視維護的環境並執行附件計畫；本計畫僅授權非正式的 bootstrap、資產發現與介面契約工作。

## 目標與背景

將 ISAM-A 的 A0 落地為一個可重現、可稽核、方便維護的環境 bootstrap 與資產發現階段，判定是否能唯一識別並相容地取得 ZigMa source、checkpoint、原配 VAE、SiT-derived transport、conditioning 與資料契約的必要前提。

本階段的產出只可支持「工程相容性交接是否完整」。它不是正式實驗，不量測或比較研究指標，不得產生任何 ISAM、LLIE、DiMSUM、Gaussian-AdaIN、anchoring、feature injection、wavelet、frequency、fusion、recurrent Mamba state 或品質改善的研究主張。

## 研究邊界與不可變識別

- 研究問題、baseline、資料 split、主要指標、門檻、模型架構與方法身分一律凍結；不得由本階段決定或變更。
- 唯一允許研究底座候選為附件指定的官方 ZigMa image model 與其可追溯 checkpoint；checkpoint 若未能唯一識別或 strict-load，必須停止為 `BLOCKED_CHECKPOINT_IDENTITY`。
- 只有經 source、config 與 checkpoint metadata 三方一致核對的原配 VAE、latent scaling、transport/interpolant、prediction target、時間端點與 conditioning 才可進入交接；未核對者不得以名稱、論文敘述或相似實作推定。
- 不得執行訓練、fine-tuning、正式評估、正式推論、資料集驗證或 ODE round-trip；後續 A1--A4 和任何正式實驗需另有計畫與授權。
- 不得更換 checkpoint 至 FacesHQ、Church、Landscape 或任何其他模型；不得以替代 VAE、替代 transport、隨機權重、mock checkpoint、captioner、CPU fallback 或降級 kernel 取代必要資產。
- 不得下載大型資產、checkpoint、資料集、論文或來源程式，也不得安裝、升級或更改 CUDA、PyTorch、系統環境；需要此類行為時停止並請求使用者授權。
- 所有重大決策必須先詢問使用者；本計畫的 Approved 狀態只授權既定範圍內的非正式 bootstrap 與診斷，並不授權開發者選擇研究資產、建立版本歷史或改變依賴環境。
- 不得修改來源資料，不得覆寫既有輸出、歷史、計畫、結果或稽核檔案；每次 bootstrap 嘗試必須使用新的 run 目錄。

## 已觀測的起始狀態

下列為 2026-07-26 的 **Observed** 環境盤點，並非對外部資產不存在的結論：

| 項目 | 觀測證據 | 本階段含義 |
|---|---|---|
| Git provenance | `git rev-parse --is-inside-work-tree` 回報 `fatal: not a git repository`；`git` 執行檔存在 | 無 source commit 與 working-tree provenance；不得宣稱專案 source 已定位。 |
| 可執行專案骨架 | `rg --files -uu .` 僅列治理文件、schema 與報告範本 | 實際無 `src/`、`scripts/`、`configs/`、`tests/`。 |
| Python packaging | 無 `pyproject.toml`、`requirements*.txt`、lock file 或 `setup.py`；`python3 -m pip --version` 回報 `No module named pip` | 目前無可重現依賴契約；不得安裝依賴或假稱環境已建立。 |
| Python 與虛擬環境 | 有 `/usr/bin/python3`（3.12.3）；未發現 `env/`、`.venv/` 或 `venv/` | 僅可作為 bootstrap 前檢查結果；是否建立 `env/` 必須依本計畫的受限流程與實際可用性記錄。 |
| 研究資產 | 工作區與所提供附件中無 ZigMa source、論文 PDF、checkpoint、VAE、資料或 dataset manifest | 資產身分、授權與相容性均為 **Blocked**，不得假稱任何一項存在。 |

根目錄 `README.md` 描述的是目標骨架，與上述實際檔案盤點不一致；本計畫以可列舉的現有檔案及每次執行保留的原始診斷為準。

## Discovery Envelope 與允許的最小技術工作

開發者僅可執行下列工作，且必須保留每次命令、退出碼與標準輸出/錯誤：

1. 建立無研究內容的可維護專案 bootstrap：最小 `pyproject.toml`、宣告性 `requirements.txt`、`configs/`、`src/`、`scripts/`、`tests/`、`.gitignore` 與各目錄 README；所有研究欄位必須明確為 `blocked` 或 `null`，不可填入猜測值。
2. 建立只使用標準函式庫的 CLI：環境盤點、資產 registry/schema 驗證與 run metadata/diagnostic receipt 寫入；缺少必要資產必須輸出明確 blocked code，不得模擬成功或啟動模型。
3. 以 Python 3.12 建立專案內 `env/` 的可行性檢查；僅當建立流程本身不下載、不改動 Python/CUDA/PyTorch/系統環境且成功時，才可建立它。若 `ensurepip` 缺失或失敗，保留診斷並標記 `ENVIRONMENT_BLOCKED`；不可自行安裝 pip。
4. 建立 schema 驅動的 `AssetRegistry`、checkpoint metadata、dataset manifest 及 paper/implementation/checkpoint 差異表的空白、可驗證模板；它們只能記錄已提供或已驗證的資料。
5. 對使用者已放入工作區、且不需下載的 source/checkpoint/VAE/metadata 執行檔案存在性、SHA-256、大小、授權欄位與結構化 metadata 檢查；只有全部必要檔案已存在時，才可進行不載入模型的靜態契約檢查。
6. 新增最小單元測試與短 synthetic smoke checks，僅覆蓋 CLI、schema、receipt、hash、blocked-state、config 解析與目錄隔離；不得測試或聲稱模型 forward、strict-load、VAE encode/decode 或 transport。

## 禁止 Fallback 與明確 blocked 行為

| 缺少或不相容項目 | 必要結果 | 禁止行為 |
|---|---|---|
| Git repository、官方 source URL 或不可變 commit | `BLOCKED_SOURCE_AMBIGUITY` | 初始化/偽造 Git commit、以本治理骨架充當 ZigMa source。 |
| checkpoint、hash、license、strict-load 對象 | `BLOCKED_CHECKPOINT_IDENTITY` | 選用其他 checkpoint、random weights 或 non-strict load。 |
| VAE ID/revision/hash/scaling | `BLOCKED_VAE_IDENTITY` | Stable Diffusion 任意 VAE、預設 scaling 或自行猜測。 |
| transport、endpoint、prediction、solver、conditioning | `BLOCKED_TRANSPORT_CONTRACT` 或 `BLOCKED_CONDITIONING_CONTRACT` | 依函式名稱推定 direction、以 generic ODE sampler 取代 native contract。 |
| 資料 manifest 或使用條件 | `BLOCKED_DATA_CONTRACT` 或 `BLOCKED_LICENSE` | 使用未記錄影像、變更 split、下載或以合成資料冒充 A0。 |
| pip、依賴或要求的系統/CUDA/PyTorch 環境 | `ENVIRONMENT_BLOCKED` | 安裝套件、變更系統、切換 CPU/不同 runtime 後仍宣稱相容。 |

## 產物與目錄映射

所有本階段執行產物必須放於新的目錄：

```text
outputs/A_feasibility_contract_discovery_20260726_<timestamp>/
├── resolved_config.yaml
├── run_metadata.json
├── environment.txt
├── diagnostics/
│   ├── 00_workspace_inventory.{stdout,stderr,exitcode}
│   ├── 01_python_venv_probe.{stdout,stderr,exitcode}
│   ├── 02_cli_help.{stdout,stderr,exitcode}
│   ├── 03_schema_and_receipt_smoke.{stdout,stderr,exitcode}
│   └── repair_attempt_<n>.*
├── asset_registry.json
├── contract_diff_table.md
├── compatibility_handoff.md
└── checksums.sha256
```

預期由開發者新增、但不代表已具研究資產的受控檔案如下：

```text
pyproject.toml                         # 僅 package/tooling metadata
requirements.txt                       # 僅宣告；未安裝前不得視為環境 lock
configs/base.yaml                      # 研究欄位全部 blocked/null
src/project_name/                      # 僅 bootstrap、registry、receipt 邏輯
scripts/{audit_project,discover_assets}.py
tests/test_{bootstrap,asset_registry,blocked_states}.py
references/asset_registry.schema.json  # 不修改既有兩個 schema
```

若 `env/` 成功建立，它是本機環境，不得提交版本控制。任何依賴 lock、source snapshot、checkpoint、VAE、資料、快取、模型輸出或正式 run 產物均不在此計畫的預設產物中。

## 實作契約

### AssetRegistry

必須接受並明確驗證下列欄位；未知值使用 `null` 或缺欄錯誤，不得填入推測值：

```text
repository_url, source_commit, source_tree_sha256, source_dirty_status,
checkpoint_path, checkpoint_sha256, checkpoint_size_bytes, checkpoint_license,
vae_id, vae_revision, vae_sha256, latent_scaling_factor,
interpolant, prediction_parameterization, time_endpoints, solver,
conditioning_contract, dataset_manifest_path, dataset_license
```

registry 必須能輸出 machine-readable status、blocked code 與可追溯診斷路徑。它不得載入 checkpoint、建立模型、呼叫網路、產生 tensor 或以空欄位回傳 success。

### Bootstrap CLI 與 receipts

- 每個 CLI 都必須提供 `--help`，輸入路徑、輸出目錄與拒絕條件均可見。
- `--prepare-run` 只可建立新的 output 目錄、解析設定與 metadata；禁止訓練、評估、推論、資料處理或自動下載。
- metadata 必須記錄實際命令、時間、Python 版本、Git probe 結果、config SHA-256、host/device probe 結果與每項 blocked code。
- 對已存在 output 目錄必須失敗，不得覆寫或附加為同一 run。

## 有限 Local-repair Authority 與預算

開發者可直接修復本計畫列出的 bootstrap 介面內之 import、工作目錄、CLI argument、config/schema 驗證、輸出目錄、receipt 寫入、hash 計算與既宣告資料結構問題。每次修復必須先有可重現失敗的測試或診斷，再新增/更新最小 regression test，並保存修復前後的原始輸出。

修復上限為：

- 最多 2 次 local repair attempts；
- 最多 90 分鐘累積 discovery 執行時間；
- 最多 6 項短 smoke checks；
- 僅 Python 3.12 與不需第三方套件的 bootstrap 候選一組；`env/` 建立至多探測一次。

到達任一上限即停止，不得藉由新增候選環境、套件、模型、資料或命令繞過。任何修復若觸及 source/模型/VAE/transport 介面、資料 split、指標、門檻、研究問題或架構，均不在 local-repair authority 內。

## 必要 Smoke Checks 與驗證方法

所有檢查均屬非正式工程 smoke check，且不得將輸出解讀為研究證據：

1. 工作區 inventory：列出受控檔案、Git probe、Python/pip/venv probe；驗證已觀測缺項仍被如實記錄。
2. Bootstrap config parse：解析 `configs/base.yaml`；驗證研究欄位皆為 `blocked`/`null`。
3. CLI help：對 `audit_project.py` 與 `discover_assets.py` 執行 `--help`；驗證可用且無網路/模型副作用。
4. New-output isolation：連續建立兩個唯一 run directory，並對既存目錄重試；驗證後者明確失敗且未覆寫。
5. Registry/schema negative cases：缺 source、checkpoint、VAE、transport、conditioning、dataset manifest 各自回傳指定 blocked code；驗證無 fallback。
6. Hash/receipt integrity：對受控小型測試檔計算 SHA-256，驗證 metadata、診斷路徑、exit code 與 checksum 一致。

若有任何可提供的真實資產，靜態檢查僅可驗證檔案存在、hash、大小、license 欄位與 metadata schema；strict-load、forward、tensor shape、ODE、hook、scan 或 cache checks 明確延後至 assets 完整後的另一份計畫。

## 成功條件與相容性交接

本計畫的 engineering **ACCEPTED** 僅在下列條件全數成立時，表示可交接「可審計的 bootstrap 與資產發現介面」，不表示 A0 或任何研究假設通過：

- Bootstrap 檔案、CLI、schema 與測試可由記錄命令重建與執行；所有 smoke checks 通過。
- 每次 run 皆有唯一目錄、resolved config、environment、metadata、診斷、checksum 與不可覆寫保護。
- 每個缺失必要資產都有確定的 blocked code、原始診斷與無 fallback 測試。
- AssetRegistry、差異表與 compatibility handoff 沒有任何未驗證的 source/checkpoint/VAE/transport/資料宣稱。
- 工程稽核者能獨立重跑上述 smoke checks，並確認本計畫的修復預算與研究邊界未被超越。

`compatibility_handoff.md` 必須逐項列示：實際 Python/environment fingerprint、package/lock 狀態、Git/source provenance 狀態、asset registry 狀態、每個 contract 欄位的 evidence path、所有 blocked code、成功 smoke check 及其診斷、未執行事項、以及下一階段所需的使用者授權。只有 source、checkpoint、VAE、transport、conditioning、資料與 license 都有可驗證證據時，後續 planner 才可另寫 A0 strict-load/contract formalization 或 A1 計畫；否則 handoff 狀態為 **Blocked**。

## 失敗、停止與升級標準

立即停止並保存證據的情況：

- 必要資產、授權、provenance、環境權限或網路存取缺失；使用相應 `BLOCKED_*` 或 `ENVIRONMENT_BLOCKED` 狀態。
- 需要下載大型資產、安裝 dependency、變更 CUDA/PyTorch/系統環境、啟動超過 smoke check 的 GPU/CPU 工作，或進行任何正式 run。
- 發現 README、附件、外部 metadata 與實際資產對 source、checkpoint、VAE、latent scaling、transport、conditioning 或資料契約有歧義。
- 任何 smoke check 顯示 hidden fallback、輸出覆寫、未記錄的網路/模型副作用、schema 允許猜測欄位，或超過 repair budget。

升級路徑如下：

| 情況 | 狀態與處置 |
|---|---|
| 本地 bootstrap 缺陷且尚在預算內 | `LOCAL_REPAIR`：由 developer 修復並回到 smoke check。 |
| 需要另一個工具鏈候選但不改研究邊界 | `DISCOVERY_ENVELOPE` 不適用；本計畫僅允許一組候選，需 planner/user 核准新計畫。 |
| 模組介面或資料/tensor contract 不清楚 | `CONTRACT_ESCALATION`：由 planner 釐清。 |
| baseline、模型、split、指標、門檻或研究問題受影響 | `RESEARCH_ESCALATION`：需 planner 與必要時使用者授權。 |
| 缺資產、授權、下載/安裝權限或環境變更權限 | `ENVIRONMENT_BLOCKED`：不得 fallback，請使用者提供資產或明確授權。 |

## 必須由使用者決策的升級點

開發者、工程稽核者與後續 planner 均不得替使用者選擇下列事項。發現需求時必須停止，提供已記錄的選項、provenance、相容性影響與原始診斷，等待明確指示：

| 重大決策 | 為何需使用者決策 | 允許的等待前工作 |
|---|---|---|
| 官方 ZigMa source 的唯一 URL、release/tag/commit | 決定不可變 source identity 與後續所有可重現性證據 | 僅記錄候選與差異；不得 clone、選定或初始化替代 source。 |
| checkpoint 的唯一 ID/檔案、授權與取得方式 | 決定 baseline/model identity，且可能需要下載大型資產 | 僅驗證使用者已提供的 metadata/檔案；不得選用任何替代 checkpoint。 |
| 原配 VAE 的 ID、revision、權重、license 與 latent scaling 證據 | 影響 A0 契約及後續 VAE ceiling，不能由猜測或慣例決定 | 只報告缺欄與候選差異；不得使用任意 Stable Diffusion VAE。 |
| 資料來源、license、manifest 與 smoke/pilot/holdout split | 是研究資料與 split 決策；禁止由工程發現階段自行選取 | 只建立空白 schema/template；不得下載、抽樣、合成或更換資料。 |
| Git 初始化、既有歷史匯入或將何處視為 repository root | 會建立/改變版本歷史與 provenance；在目前非 Git 目錄屬重大決策 | 保留 `not a git repository` 診斷；不得執行 `git init`。 |
| 安裝 pip、建立可含 pip 的 `env/`、安裝任何 dependency 或產生 lock | 會改變可執行環境，並可能牽涉網路、PyTorch/CUDA 相容性 | 僅探測 Python/`venv`/`ensurepip` 可用性，不得安裝或升級。 |
| 任何 CUDA、PyTorch、driver、系統套件、GPU 裝置或 CPU fallback 選擇 | 會改變研究運算契約與結果可比性 | 僅記錄 probe；不得變更或將替代裝置視為相容。 |
| 由多個契約候選中選定 transport、solver、time endpoint、prediction target 或 conditioning | 會決定方法與 A0/A1--A4 的正式技術契約 | 僅列 paper/implementation/checkpoint 差異；不得依名稱或經驗選擇。 |

收到使用者決策後，如決策改變本計畫的凍結邊界、候選集合或 repair 預算，planner 必須先修訂或另立計畫；不得把回覆直接視為 local repair authority。

## 風險與有效性威脅

- 目前無 Git repository，故 bootstrap 的 provenance 不能冒充官方 ZigMa source provenance。
- 無 pip、lock file 或可驗證依賴，故任何「環境可重現」僅限標準函式庫 bootstrap；深度學習 runtime 的可重現性仍為 **Unproven**。
- 無來源程式、論文、checkpoint、VAE、資料或 manifest，故附件中關於架構與候選設定的敘述在本工作區均未被實作/資產驗證。
- 即使工程 audit 接受本計畫，A0 hard gate（source commit、strict-load、VAE/scaling、forward、time/conditioning、license）仍為 **Blocked**，更不構成 A1--A4 或研究接受。

## 預定角色與記錄

1. Developer 依本 Approved 計畫實作最小 bootstrap 並保存診斷與測試證據。
2. 獨立 Engineering Auditor 只讀檢查本計畫界定的 CLI、schema、receipts、輸出隔離與 smoke checks，於 `reports/audits/A_feasibility_contract_discovery_20260726_implementation_audit.md` 記錄結果與 repair disposition。
3. 獨立 Recorder 依 audit 結果附加 `reports/experiment_log.md`，並建立 `reports/archive/implementation/{status}/A_feasibility_contract_discovery_20260726/` dossier；本 planner 不執行這兩項工作。

在工程 audit 接受前，所有狀態維持 **Observed**、**Unproven** 或 **Blocked**；不得使用 **Supported** 描述任何研究結論。
