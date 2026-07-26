# A_source_git_registry_discovery_20260726：來源、Git、依賴與 registry 契約探索

- 日期：2026-07-26
- 計畫類型：Engineering Discovery
- 狀態：Approved
- 上位計畫：附件 `ISAM-A`（`A_feasibility_and_contract_plan.md`）A0：資產、來源與方法契約
- 前序證據：[bootstrap 計畫](A_feasibility_contract_discovery_20260726_plan.md)、[前序工程稽核（INCOMPLETE／CONTRACT_ESCALATION）](../audits/A_feasibility_contract_discovery_20260726_implementation_audit.md)、[固定環境與候選交接](A_environment_and_asset_candidate_discovery_20260726_plan.md)、[實驗帳本](../experiment_log.md)
- 使用者授權：
  - 唯一 ZigMa source 為 `https://github.com/CompVis/zigma.git`；可 clone 並固定已預先觀測的 remote HEAD `37d837bfb787cbd2c349d8bc37596c2009443187`。
  - 可讀取該 source 的 README、設定與程式，以抽取明示的原配 VAE／scaling、transport 與 conditioning 證據；可讀取原始 checkpoint 的 metadata，及做下載前驗證。
  - 固定使用 project-local `env/`，並以 source 原始 repository 的明示依賴為唯一依賴候選；可在相容且不需變動 Python、CUDA 或 PyTorch 契約時安裝並產生 lock／receipt。
  - 可對 `https://github.com/izumiwen/ISAM-Diff-A.git` 進行 Git 初始化、設定 remote、建立初始 commit 與 push。
  - 可另立本計畫，補發前序 registry `CONTRACT_ESCALATION` 的有限修復額度。

## 目標

建立一條可稽核、可維護而且不把治理專案冒充為 ZigMa 的 A0 工程交接路徑：

1. 以安全條件建立本專案的第一個 Git 歷史並推送到使用者指定 remote。
2. 將唯一官方 source 固定至可重驗的 commit 與 tree 證據，並與本專案工作樹隔離。
3. 以原始 ZigMa repository 的宣告為唯一候選，判定固定 `env/` 能否形成真正的 dependency lock；不以自行猜測的相依套件取代原始宣告。
4. 從固定 source 抽取、而非推定，VAE/scaling、transport、time direction、prediction target 與 conditioning 的 evidence。
5. 修復前序 `AssetRegistry` 的靜態驗證、schema 路徑與 repair-evidence 缺口，讓「已宣告」資產必須通過 hash、大小、license、provenance 及適用 schema 的檢查。

本計畫只可產生工程相容性證據；不會 strict-load、建立模型、forward、VAE encode/decode、ODE、資料驗證、訓練、推論、評估或研究指標。工程稽核接受不代表 A0 hard gate 或任何研究結論。

## 凍結的研究邊界與已知狀態

- 凍結研究問題、baseline、checkpoint 身分、VAE 身分、資料來源與 split、transport/solver/endpoint、conditioning、主要指標、門檻及 A1--A4。除已指定的 source URL/commit 外，developer 不得自動選定、替換或降級任何研究資產或方法設定。
- **Observed**：工作區目前不是 Git repository；`env/` 為 Python `3.12.3`／pip `24.0`，僅有 pip；指定 project remote 的預先觀測 `ls-remote` 沒有 ref；指定 source remote 的預先觀測 HEAD 是 `37d837bfb787cbd2c349d8bc37596c2009443187`。
- **Observed**：前序工程稽核為 **INCOMPLETE**，唯一處置為 `CONTRACT_ESCALATION`；兩份歷史 bootstrap receipt 均為不可改寫的證據。
- **Unproven**：指定 commit 的可 clone 性、source tree hash、source 依賴與 Python 3.12 相容性、checkpoint metadata、VAE/scaling、transport/conditioning、license、資料 manifest/split 與任何 runtime 相容性。
- **Blocked（直到另獲明確授權）**：checkpoint、VAE 權重及資料的任何大型下載；資料下載與 dataset validation；任何替代 source/checkpoint/VAE/data/split/solver；Python、CUDA、PyTorch、driver 或系統層變更。

## 明確禁止的 fallback

| 條件 | 必要結果 | 禁止行為 |
|---|---|---|
| project remote 有既有 ref、remote URL 不一致、Git identity/auth 不可用、或 push 被拒 | 保存原始 Git 診斷並停止，請使用者決定 | force push、刪改 remote history、以不同 remote 或帳號推送 |
| source commit 無法從指定 origin checkout，或 origin/HEAD/tree 不一致 | `BLOCKED_SOURCE_AMBIGUITY` | 改用 fork、tag、不同 commit 或把本專案當 source |
| source 未明示 VAE/scaling、transport、prediction/endpoint/solver 或 conditioning | 相應 `BLOCKED_VAE_IDENTITY`、`BLOCKED_TRANSPORT_CONTRACT`、`BLOCKED_CONDITIONING_CONTRACT` | 任意 Stable Diffusion VAE、慣例 scaling、generic ODE sampler、依函式名稱推定 |
| checkpoint metadata 無法取得、license/provenance/hash/size 未齊 | `BLOCKED_CHECKPOINT_IDENTITY` 和／或 `BLOCKED_LICENSE` | 下載 checkpoint、改用其他資料域 checkpoint、non-strict load |
| 原始 dependency 宣告與 Python 3.12 不相容，或需改變 Python/CUDA/PyTorch/系統契約 | `ENVIRONMENT_BLOCKED`，保存 resolver／宣告證據並詢問使用者 | 重建 `env/`、第二個 environment、變更 Python/CUDA/PyTorch、任意版本 pin 或 CPU fallback |
| registry hash、大小、license、provenance 或 schema 驗證失敗 | 對應 `BLOCKED_*`，且不得移除 blocked code | 只檢查欄位非空、忽略 mismatch、以空檔或 mock 冒充真資產 |

## 實作分段、驗證與停止條件

### 第 1 段：Git remote safety recheck、初始化與初始 push

**允許工作**

1. 在任何寫入前，保存 `git status`（預期 non-repository）、`git config --get user.name`／`user.email`、以及 `git ls-remote --heads --tags https://github.com/izumiwen/ISAM-Diff-A.git` 的 stdout、stderr 與 exit code 到新的本階段 receipt。
2. 僅在 remote URL 完全相同、列出的 heads/tags 為空、local Git identity 可用、且工作區仍無 `.git/` 時，執行 `git init -b main`、以 `origin` 設定指定 URL、再次驗證 remote，並建立一個初始 commit。
3. 初始 commit 只能包含目前治理專案的受控文字／程式／計畫檔；必須先檢查 `.gitignore` 排除 `env/`、`outputs/`、Python cache、clone source 位置及所有資產／cache。不得加入 `env/`、outputs、checkpoint、VAE、資料、source clone 或 credential。保存 `git status --short`、commit SHA、tree SHA、remote -v 與 `git check-ignore` 的診斷。
4. 僅以 `git push -u origin main` 推送新 branch；保留完整結果。不得使用 `--force`、`--mirror` 或修改 remote 預設分支。

**驗證**

- 初始 commit 前後均以 `git status --short` 記錄；`git ls-tree -r --name-only HEAD` 不得列出被排除的環境、輸出、資產或 source clone。
- remote recheck 與 push 後 `git ls-remote --heads origin main` 的 commit 必須等於本地 `HEAD`。

**停止／升級**

- remote 出現任何 ref、GitHub authentication/authorization 失敗、local name/email 未設定、工作區在初始化前出現未知檔案或 push 的 remote HEAD 與本地不符時，立刻停止。保留診斷並請使用者決定；不得設定 global credential、讀取或要求貼出 access token。
- GitHub CLI 登入由使用者在互動終端執行 `gh auth login`，選擇 GitHub.com、HTTPS 與瀏覽器登入；完成後以 `gh auth status` 自行確認。若只使用 Git Credential Manager，使用者亦可先完成 `git ls-remote` 的互動登入。developer 不處理、顯示或保存 token。

### 第 2 段：唯一 source clone 與不可變 provenance

**允許工作**

1. clone 只能放在工作區根目錄 `external_sources/CompVis-zigma/`；此目錄是唯讀的外部 reference，不是本專案 source，必須被 `.gitignore` 排除且在根目錄／該目錄 README 明確標示此身分。
2. clone URL 必須完全等於 `https://github.com/CompVis/zigma.git`。checkout 必須精確為 `37d837bfb787cbd2c349d8bc37596c2009443187`，不得追蹤浮動 branch；使用 detached HEAD。
3. 保存 clone command、origin URL、`git rev-parse HEAD`、`git status --porcelain=v1`、`git rev-parse HEAD^{tree}`、`git show --no-patch --format=fuller HEAD` 與 source license 檔路徑/sha256。另以「所有 Git tracked regular files 的相對路徑、檔案大小與 SHA-256 依 bytewise sorted manifest」產生 `source_tree_sha256`；manifest 本身與 command 均放入新的 receipt，避免把 Git SHA-1 tree object 冒充 SHA-256。
4. 僅當 origin、commit、乾淨 detached worktree、Git tree ID 與上述 SHA-256 manifest 都一致時，才可在新 registry/contract evidence 中列為已驗證 source provenance。

**驗證**

- `git -C external_sources/CompVis-zigma remote get-url origin`、`rev-parse HEAD`、`status --porcelain=v1`、tracked-file manifest 與 receipt checksum 可由稽核者獨立重跑。
- 計算 source tree manifest 時不得存取網路、下載 LFS/sparse 資產或執行 source 程式。

**停止／升級**

- checkout、origin、commit、worktree clean status、license evidence 或 tree-manifest 任何一項不符時，保存原始診斷，維持 `BLOCKED_SOURCE_AMBIGUITY` 或 `BLOCKED_LICENSE`，不再嘗試其他 source。不得在此階段 cherry-pick、patch 或執行 source。

### 第 3 段：原始 dependency 宣告、固定 `env/` 與 lock

**允許工作**

1. 只讀稽核固定 commit 中 README、`requirements*.txt`、`environment*.yml|yaml`、`pyproject.toml`、`setup.*`、install scripts 與直接引用的 lock/constraints；逐檔記錄 SHA-256、行號、明示 Python/OS/CUDA/PyTorch 條件及 top-level requirements。不得由 imports、網頁或慣例補出套件。
2. 產生 machine-readable `source_dependency_contract.json`：每個要求要有 source path、line、specifier、hash、是否為 Python/CUDA/PyTorch/系統層、及與現有 `env` Python/pip 的判定。產生供人讀的 `dependency_decision.md`，明示它是否為可安裝的完整 cohort；不是 partial lock。
3. 先在不改動 `env/` 的模式驗證 Python `3.12.3` 是否滿足 source 的明示 Python 範圍。若 source 沒有明示 Python 3.12 支援、明示拒絕它、或宣告/解析要求變更 Python、CUDA、PyTorch 或系統層，立刻標記 `ENVIRONMENT_BLOCKED`，保存證據並詢問使用者；不得安裝任何「剩餘」套件來偽造完整環境。
4. 僅在第 3.3 的完整相容性成立，且宣告 cohort 不要求改變 Python、CUDA、PyTorch 或系統層時，才能對既有 `env/` 一次執行 source 宣告的唯一安裝命令。保存安裝前的 `pip freeze`、exact command、pip resolver stdout/stderr/exit code、安裝後 `pip check`、`pip freeze --all` 與 `pip inspect`（若該 pip 支援）。
5. lock 必須由安裝後 environment 的完整、排序後 `pip freeze --all` 加上 source dependency contract、Python binary SHA-256、source commit/tree SHA-256、pip version 與 lock SHA-256 組成；儲存在受版本控制的 `requirements.lock`／相應 provenance JSON，並在 receipt 另存副本。它必須明確標示平台與 Python；若宣告不含 distribution hashes，不得聲稱可跨平台 bitwise 重建。

**驗證**

- lock 可由新建 receipt 的 checksum 驗證，並能與 `env/bin/python -m pip freeze --all` 完全比對。
- `pip check` 必須成功；任何 install 中的 resolver conflict、unresolved requirement、wheel/source build failure 或未記錄下載都使本段未通過。
- 不執行 import、模型初始化、CUDA probe 或任何 source provided training/inference command。

**停止／升級**

- Python 3.12 相容性不足、原始 source 沒有可辨識完整依賴宣告、或需安裝/升降 PyTorch、CUDA、driver、系統套件時停止並向使用者呈示精確 source 檔案與版本差異。此計畫不授權重建 `env/`、建立第二個 environment 或改變 Python/CUDA/PyTorch。
- `env/` 不可啟動、pip 不可用或其既有 fingerprint 與前序 receipt 不一致時保存診斷並停止；不重建、移動或替代環境。

### 第 4 段：source 明示的 VAE、transport 與 conditioning evidence

**允許工作**

1. 在固定 source commit 內以可重現文字搜尋，檢視 README、config、model/sampler 建構碼、checkpoint metadata reference 及直接引用的常數；每個結論都要有 commit、relative path、line range、檔案 SHA-256、原始摘錄路徑與 evidence type。
2. 建立 `source_contract_evidence.json` 及更新 contract difference table，分別列示 repository evidence、checkpoint metadata evidence、paper evidence（若已在 source/先前 receipt 可追溯）與最終狀態。VAE identity/revision、latent scaling、interpolant、prediction parameterization、time endpoints/direction、native solver 與 conditioning 必須逐欄呈現 `Observed`、`Unproven` 或 `Blocked`。
3. checkpoint 只可讀取指定第一方 metadata/model-card 或 source 明示 metadata URI，記錄 HTTP status、retrieval UTC、ID/filename、license/source relation、可見 revision、可見 size/hash 欄位。這是 metadata／下載前驗證，不得抓取 checkpoint blob、LFS object、VAE weight 或資料。

**驗證**

- 每一個非空契約值均可回溯到固定 commit 的原始行與檔案 hash，或 checkpoint metadata 的 raw response/URL/time；沒有證據的欄位必須保留 null/blocked。
- 稽核者能只讀地重新執行搜尋與檔案 hash，不載入模型或建立 tensor。

**停止／升級**

- source、metadata 與既有 paper evidence 相衝突，或 checkpoint metadata 仍被 rate limit／未提供 license/provenance/hash/size 時，不嘗試鏡像、第三方 checkpoint 或權重下載。列出差異並請使用者決定下一步。
- source 若只明示 VAE family、未明示 exact ID/revision/scaling，仍為 `BLOCKED_VAE_IDENTITY`；不得把 family 名稱當成已選定 VAE。

### 第 5 段：registry/schema repair 與可稽核 repair evidence

**修復範圍**

本段是使用者明確授權、對前序 `CONTRACT_ESCALATION` 的新 repair authority；不追溯宣稱修復舊 receipt，也不修改它們。Developer 只可修改：

- `src/project_name/registry.py` 與必要的標準函式庫 helper；
- `references/asset_registry.schema.json`、`references/checkpoint_metadata.schema.json`、`references/dataset_manifest.schema.json`，以及有明確版本識別的新 schema；
- `configs/base.yaml`、`scripts/audit_project.py`、`scripts/discover_assets.py`；
- 直接覆蓋上述契約的既有或新增 `tests/test_*.py`；
- `.gitignore`、受控依賴 lock/provenance 檔與本計畫指定的新 receipts。

不得改寫前序 plan、audit、log 或 outputs；不得在這一段下載、strict-load、處理資料或改變研究介面。

**契約設計與必須修復事項**

1. 將 registry schema 版本化：保留歷史 receipt 對其既有 v1 形狀的可讀性；為新 evidence 建立明確 v2 contract，而不是讓新 required fields 使歷史 receipt 看似損壞。v2 必須包含可追溯的 source、checkpoint、VAE 與 dataset evidence reference（本地 evidence path 或 HTTPS URL）、license 值及其 evidence、以及 schema/version 識別。
2. 實作標準函式庫的 schema validator，明確覆蓋本專案實際採用的 JSON Schema 子集：`type`、`required`、`properties`、`additionalProperties`（布林及 schema map）、`enum`、`const`、`minimum`、nested object/array；不支援的 keyword 必須明確拒絕，不能靜默略過。讓 checkpoint metadata 與 dataset manifest 有真正的 loading/validation path，而非只保存 schema 檔。
3. 對 source：驗證 repository URL 等於唯一授權 URL、commit 是完整 hex object ID 且等於 clone HEAD、Git tree/manifest SHA-256 格式和值、worktree 為乾淨、license/evidence path 存在且可 hash。
4. 對 checkpoint/VAE/dataset 的已宣告本機檔案：驗證一般檔案、實際 SHA-256、精確 byte size、metadata/manifest schema、非空 license 與可追溯 provenance evidence。任何不存在、格式不合法、checksum/size mismatch、schema failure、license/provenance 缺失均須保留該範圍 `BLOCKED_*`，附精確診斷；不得把所有 blocked code 清空後回報 `unproven`。
5. 對未下載資產：v2 registry 必須能正確表達「已驗證 source，但 checkpoint/VAE/data 仍 Blocked」；不可要求不存在 blob 才能驗證 source，也不可把 metadata-only 視為檔案 hash/strict-load 已通過。
6. 新測試至少覆蓋：正向小型受控 source/checkpoint/manifest；每一種 checksum/size/path/license/provenance failure；v1 historical compatibility；checkpoint metadata 與 dataset manifest 的 valid/invalid schema；未知/unsupported schema keyword；partial registry 不得清空必要 blocked code；CLI/receipt output isolation與checksum。所有 fixture 都必須是小型 synthetic text/binary，不能是模型、真 checkpoint 或資料集。

**有限 repair budget 與證據**

- 最多 **3 次** local repair attempts、**150 分鐘**累積 discovery 執行時間、**8 項**短 smoke checks；這是新的獨立預算，與不可稽核的舊 2/2 預算無關。
- 每一次 repair 之前，必須在新 receipt `diagnostics/repair_attempt_<01-03>/before/` 保存失敗測試或診斷、命令、exit code、時間與失敗原因；修復後保存 diff 摘要、最小 regression command/output、時間與累積計數。未有 before evidence 的改動不得計為合格 repair。
- 在任何一次 repair 發現需要改變研究資產、A0 schema 的研究語義、模型/transport/VAE/data interface、baseline、split、solver、metric/threshold，立即停止並 `CONTRACT_ESCALATION` 或 `RESEARCH_ESCALATION`；不得用剩餘額度繼續。

**必要 smoke checks**

1. Git source/remote provenance recheck（第 1、2 段所列精確 ID）。
2. `.gitignore`／初始 commit tree 檢查，不含 `env/`、outputs、external source 或資產。
3. `env` fingerprint 與 dependency contract/lock consistency（僅在安裝契約通過時）。
4. source evidence extraction 的路徑、行、hash 與 null/blocked 狀態完整性。
5. AssetRegistry v2 正向小型 fixture 驗證。
6. SHA-256、size、path、license、provenance 的負向驗證，逐一保留 blocked code。
7. checkpoint metadata 與 dataset manifest 的正向／負向 schema 驗證，以及不支援 keyword 的明確拒絕。
8. CLI `--help`、新 output isolation、receipt checksum 及 repair-ledger consistency。

## Receipt、產物與 compatibility handoff

本階段每一執行批次使用新的目錄，命名為：

```text
outputs/A_source_git_registry_discovery_20260726_<timestamp>/
├── run_metadata.json
├── git_remote_safety.json
├── git_provenance.json
├── source_tree_manifest.sha256
├── source_dependency_contract.json
├── dependency_decision.md
├── requirements.lock                    # 僅在完整 cohort 安裝成功時存在
├── environment_fingerprint.json
├── source_contract_evidence.json
├── checkpoint_metadata_evidence.json
├── asset_registry_v2.json
├── contract_diff_table.md
├── compatibility_handoff.md
├── diagnostics/
│   ├── 00_git_remote_safety.*
│   ├── 01_git_init_commit_push.*
│   ├── 02_source_clone_and_provenance.*
│   ├── 03_source_dependency_audit.*
│   ├── 04_env_install_or_blocked.*
│   ├── 05_source_contract_evidence.*
│   ├── 06_checkpoint_metadata_probe.*
│   ├── 07_registry_schema_smoke.*
│   └── repair_attempt_<01-03>/
└── checksums.sha256
```

`compatibility_handoff.md` 必須逐項連結 Git commit/remote、source commit/tree/manifest、env/lock 決定、VAE/transport/conditioning raw evidence、registry v1/v2 validation 結果、每項 blocked code、repair ledger、未執行操作與下一個使用者決策。所有檔案 checksum 要能在該 receipt 內重新驗證；對於未執行或被停止的階段，必須有 raw diagnostic 與原因而非虛構產物。

## 成功條件

本 Engineering Discovery 僅能在獨立 engineering audit 確認下列條件時被 **ACCEPTED**：

- 指定 project remote 的安全 recheck、無 force 的 initial push、commit/tree 對應與忽略規則皆有可重驗證據。若 Git 階段必須 stop，整個 engineering audit 必須如實為 **BLOCKED** 或 **INCOMPLETE**，不得以其他子項完成宣稱本計畫 **ACCEPTED**。
- source clone 的 origin、精確 commit、clean detached worktree、Git tree ID、SHA-256 tree manifest 和 license evidence 全部一致，且外部 source 與本專案隔離。
- dependency outcome 是完整、誠實的 source-declared cohort：相容時有可比對 lock/receipt；不相容時有 `ENVIRONMENT_BLOCKED` 證據。partial 安裝絕不可冒充 lock。
- VAE/scaling、transport、conditioning 與 checkpoint metadata 僅陳述可回溯的 source/metadata evidence；未知值仍為 `Blocked`，不以名稱或推論填補。
- registry v2、三份 schema 的執行路徑、正負測試、receipt isolation/checksum 與 repair ledger 均通過；歷史 receipt 未被修改且可保留其 v1 界線。
- engineering audit 明確界定：這不是 checkpoint strict-load、forward、A0 hard gate、資料可用性或研究接受。

達成上述工程交接，仍不解除 checkpoint/VAE/data 大型下載、strict-load、資料 split、模型 execution 和 A1--A4 的後續計畫與使用者決策。

## 風險、停止與使用者待決事項

- 需要下載任何 checkpoint、VAE weight、dataset、LFS blob 或進行資料驗證時，停止並向使用者詢問；本計畫的 metadata 授權不等於 blob download 授權。
- Python 3.12 或 source declared runtime 若與所需 PyTorch/CUDA 不相容，須向使用者報告原始 source 版本證據、現有 env fingerprint 與可選修訂方向，再取得決策；不得自行切換 Python、CUDA 或 PyTorch。
- checkpoint 的唯一 ID、檔案、license 和取得方式，VAE exact identity/revision/license（若 source 無法唯一明示），資料來源/license/manifest/split，以及任何 transport/solver 最終選定，均仍需使用者決定。
- 初始 Git push 若發生 authentication 或 remote history 風險，使用者需先以互動 GitHub CLI 登入；不需要、也不得將 token 提供給 agent。

## 角色、順序與記錄

1. Developer 只能在本 Approved plan 的邊界、budget 與停止條件內實作；保留每段的原始診斷與每次 repair evidence。
2. 獨立 Engineering Auditor 不得參與規劃或開發，只讀驗證 Git/source/env/registry/schema/receipt 及本計畫界線，寫入 `reports/audits/A_source_git_registry_discovery_20260726_implementation_audit.md`。
3. 獨立 Recorder 依 audit 的精確狀態追加 `reports/experiment_log.md`，並建立 `reports/archive/implementation/{status}/A_source_git_registry_discovery_20260726/` dossier；不得建立研究 accepted entry。

在獨立工程稽核前，所有結論只可標示 **Observed**、**Unproven** 或 **Blocked**；不得把本計畫的任何完成項標為研究 **Supported**。
