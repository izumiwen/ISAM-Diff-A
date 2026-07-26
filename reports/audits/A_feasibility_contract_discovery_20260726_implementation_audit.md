# A_feasibility_contract_discovery_20260726：Engineering Discovery 實作稽核

## 稽核狀態

**INCOMPLETE**

本結論僅稽核「可審計的 bootstrap 與資產發現介面」；不構成 A0、模型、資料、指標或任何研究主張的接受。

## 稽核範圍與獨立性

- 稽核對象：`reports/plans/A_feasibility_contract_discovery_20260726_plan.md` 所定義的標準函式庫 bootstrap、AssetRegistry、CLI、schema、receipt、既有輸出及測試。
- 稽核者未參與此階段的規劃或開發，且未修復程式、改動設定或既有輸出；本檔為本次稽核唯一持久化寫入。
- 未執行：訓練、評估、推論、資料集驗證、模型/ checkpoint 載入、strict-load、tensor/ODE 檢查、下載、安裝、`git init`、環境建立或任何正式實驗。

## 已檢視的證據

- Approved 計畫：`reports/plans/A_feasibility_contract_discovery_20260726_plan.md`
- 實作：`src/project_name/bootstrap.py`、`src/project_name/registry.py`、`scripts/audit_project.py`、`scripts/discover_assets.py`
- 設定與 schema：`configs/base.yaml`、`references/{asset_registry,checkpoint_metadata,dataset_manifest}.schema.json`
- 測試：`tests/test_bootstrap.py`、`tests/test_asset_registry.py`、`tests/test_blocked_states.py`
- 既有 receipts：
  - `outputs/A_feasibility_contract_discovery_20260726_20260726T000001Z/`
  - `outputs/A_feasibility_contract_discovery_20260726_20260726T000002Z/`

## 獨立驗證

| 檢查 | 命令／方法 | Observed 結果 |
|---|---|---|
| 單元測試 | `PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 -m unittest discover -s tests -v` | 6/6 通過（0.112 s）。測試的 receipt 寫入使用系統暫存目錄。 |
| CLI 說明 | `... /usr/bin/python3 scripts/audit_project.py --help`；`... scripts/discover_assets.py --help` | 兩者 exit 0；說明列出輸入、輸出與拒絕條件。 |
| CLI 輸出隔離 | 系統暫存目錄內以相同 `--output-dir` 呼叫 `audit_project.py --prepare-run` 兩次 | 首次 exit 0 且輸出 `BLOCKED_SOURCE_AMBIGUITY`；第二次 exit 2 且 stderr 含「拒絕覆寫既有 output 目錄」。 |
| Receipt 完整性 | 在兩個既有 receipt 內執行 `sha256sum -c checksums.sha256` | 所列 11 個（第一份）及 17 個（第二份）檔案均為 `OK`。 |
| 無網路／模型執行面 | 檢視 `src/`、`scripts/`、`tests/` 的 imports 與呼叫 | 僅見標準函式庫與本地 subprocess（Git probe、CLI `--help`）；未見 HTTP client、下載、PyTorch 或模型載入。 |
| 研究欄位與 empty registry | 檢視 `configs/base.yaml`、既有 `asset_registry.json`，並重跑測試 | config 的 19 個研究欄位均為 `null` 且 contract status 為 `blocked`；既有 registry 具七個 `BLOCKED_*` code。 |

## 通過的實作契約

- `configs/base.yaml` 在 `load_config()` 中要求所有已列研究欄位完整、全為 `null`，且狀態為 `blocked`；沒有以空欄位宣稱成功。
- 空 registry 會 machine-readable 地輸出 `BLOCKED_SOURCE_AMBIGUITY`、`BLOCKED_CHECKPOINT_IDENTITY`、`BLOCKED_VAE_IDENTITY`、`BLOCKED_TRANSPORT_CONTRACT`、`BLOCKED_CONDITIONING_CONTRACT`、`BLOCKED_DATA_CONTRACT`、`BLOCKED_LICENSE`。
- `prepare_run()` 以 `Path.mkdir(..., exist_ok=False)` 保護已存在 run 目錄；獨立 CLI smoke 已驗證拒絕覆寫。兩個既有輸出目錄名稱不同，且未發現覆寫證據。
- 第二份 receipt（`...T000002Z`）包含計畫要求的 `resolved_config.yaml`、`run_metadata.json`、`environment.txt`、registry、差異表、handoff、checksum 與 `00`--`03` 診斷。metadata 記有實際命令、UTC 時間、Python、Git probe、config SHA-256、host/device probe、blocked codes 與診斷相對路徑。
- 兩份 receipt 的 Git probe 都如實記錄 exit 128 及「not a git repository」；未見偽造 commit、hidden source、下載或模型 fallback。所有目前研究資產狀態仍為 **Blocked**，不是 **Supported**。
- `environment.txt` 明確記錄沒有安裝或變更 dependencies、沒有 device 選擇；系統 `/usr/bin/python3 -m pip --version` 仍回報 `No module named pip`，未建立 `env/`。這不被解讀為深度學習環境已可重現。

## 未完成項與不符合處

### 1. AssetRegistry 未驗證已宣告資產的身分與完整性

`AssetRegistry.validate()`（`src/project_name/registry.py`）只檢查欄位是否為 `null` 及 checkpoint/manifest 路徑是否為一般檔案；未比較 checkpoint 的 SHA-256 或大小、未驗證 VAE SHA-256、license/provenance、source tree、dataset manifest schema，亦未對 transport/conditioning 的結構化契約建立證據。這不符合計畫對「已提供資產」的存在性、SHA-256、大小、license 與結構化 metadata 靜態檢查要求。

獨立負向測試在系統暫存目錄建立兩個小型檔案，並提供刻意錯誤的 checksum 與大小（`999999`）。結果為：`{'status': 'unproven', 'blocked_codes': [], 'diagnostics': []}`。因此未驗證的宣告可移除所有 blocked code，雖然它未被標示為 success，仍無法提供計畫要求的明確 blocked 診斷或可靠的資產交接。

### 2. 第一份 bootstrap receipt 未滿足每次 run 的必要診斷集合

`outputs/...T000001Z/` 沒有 `diagnostics/02_cli_help.*` 與 `diagnostics/03_schema_and_receipt_smoke.*`，metadata 的 `diagnostic_paths` 也只列 `00`、`01`。第二份 receipt 完整並且 checksum 正確，不能補足計畫「每次 bootstrap 嘗試」必須保存完整產物／診斷的要求。第一份仍是應保存、不可覆寫的歷史產物。

### 3. 修復預算與修復證據不可稽核

工作區存在兩個 bootstrap receipt（建立時間相距約 68.5 秒），但所有 `outputs/A_feasibility_contract_discovery_20260726_*/` 之下均無 `repair_attempt_*`，也沒有可追溯的修復前失敗、修復後命令、迴歸測試輸出或累積時間記錄。故無法證實「修復預算為 2/2」是否已使用、是否未超限，或第二份 receipt 是否是針對第一份缺漏的合規修復。計畫要求保留每次 repair 的原始診斷與 regression evidence；現有 6 個測試的當前成功結果不能反向證明歷史修復預算合規。

### 4. Schema 的執行覆蓋不足

bootstrap 僅對 asset registry 的自製型別檢查呼叫 `validate_schema_document()`；`checkpoint_metadata.schema.json` 與 `dataset_manifest.schema.json` 沒有對使用者提供 metadata/manifest 的驗證路徑或測試。這使計畫所列「schema 驅動的 checkpoint metadata、dataset manifest」尚未形成可稽核的靜態契約檢查。

## Receipt、checksum 與研究邊界評估

- **Observed**：兩份現存 checksum 清單均可驗證；第二份具完整已列 diagnostics，且所有缺失資產在該 receipt 內有明確 blocked code。
- **Observed**：輸出隔離、CLI help、config blocked/null 與 empty-registry 行為可獨立重跑。
- **Unproven**：任何來源、checkpoint、VAE、latent scaling、transport、conditioning、資料、license 或深度學習 runtime 的身分／相容性。
- **Blocked**：A0 strict-load／contract formalization 與所有後續研究階段，直到使用者提供或決定必要 source、asset、license 與資料 provenance，且另行規劃。
- 未發現 hidden fallback、網路存取、模型建構、tensor 生成、資料處理、訓練、評估或推論；但因上述 registry 靜態驗證缺口，不能接受 compatibility handoff。

## 唯一 Repair Disposition

**CONTRACT_ESCALATION**

不可直接要求 developer 修復：現有證據無法稽核修復次數，且已要求特別核對的 2/2 修復預算沒有可驗證紀錄。Planner 必須先釐清／修訂 repair-budget 狀態與允許的後續處置；若需新增修復額度，屬計畫變更，須取得使用者明確授權。之後才可在新授權範圍內補上資產靜態驗證、schema 驗證，以及完整可追溯的 repair evidence。不得以替代資產、下載、安裝、CPU fallback、`git init` 或修改歷史 receipt 迴避此處置。

## Required Follow-up

1. Planner 向使用者呈報並取得對 repair-budget／後續計畫的明確決策；保留兩份既有 receipt，不得覆寫第一份。
2. 在獲准的修復或新 discovery plan 中，新增 SHA-256、大小、路徑、license/provenance、source tree 與 checkpoint/dataset metadata schema 的負向／正向靜態測試；未驗證或不一致時必須維持對應 `BLOCKED_*` code。
3. 對每次未來 repair 保存修復前診斷、後續命令、exit code、最小 regression test 與累積 budget；不可把單純的新 run 目錄當作 repair evidence。
4. Recorder 僅能依本稽核的 **INCOMPLETE** 與 `CONTRACT_ESCALATION` 建立 implementation archive／附加帳本；不得產生 accepted entry 或研究結論。
