# Candidate research questions and scoring

Scoring: importance 15; gap 15; testability 15; feasibility 15; reproducibility 10; reuse 10; innovation 10; growth 5; maintenance 5. The index is `data/design/candidates.json`; its three referenced shards hold the full 15-field records and evidence labels.

| Rank | Slug | Score | Question | Largest failure mode |
|---:|---|---:|---|---|
| 1 | `agent-completion-ledger` | **96** | 在公開 SWE-bench Verified 執行中，把「已產生修補」視為完成，會造成多高的錯誤完成率；要求可執行驗證證據的最小 ledger 能否消除此報告錯誤？ | 問題可能只是對成功率的重新命名，或 oracle 本身不代表真實完成。 |
| 2 | `figure-lineage` | **89** | 論文/報告中的輸出圖檔是否能被可驗證地連回資料與生成命令；輕量 sidecar manifest 能否偵測圖檔與來源漂移？ | 問題已由 workflow 工具充分解決，sidecar 只是較弱重做。 |
| 3 | `notebook-freshness` | **89** | 公開研究 notebook 中，輸出是否常與目前程式碼/輸入雜湊不一致，且輕量 freshness 標記能否可靠抓出 stale output？ | 變更不一定影響輸出，ground truth 容易主觀。 |
| 4 | `offline-oer-dependency-audit` | **88** | 標示可離線使用的開放教材包，有多少必要圖片、字型、腳本或影片仍依賴外部 URL；靜態檢查能否預測離線失效？ | 「可離線」定義與必要資產標註可能不一致。 |
| 5 | `data-unit-contract` | **83** | 公開環境 CSV 中，欄名或說明宣告的單位與數值量級/轉換關係是否矛盾；unit contract 能否找出可確認的錯誤而非僅異常值？ | 缺乏真實 ground truth，規則可能只是常識範圍。 |
| 6 | `public-data-receipts` | **82** | 政府公開資料 URL 的「仍可下載」是否掩蓋內容類型、schema 或雜湊漂移；每日 receipt 能否比單純 HTTP 200 更早發現破壞性變更？ | 短期觀察期沒有事件，無法回答價值。 |
| 7 | `release-artifact-drift` | **82** | 開源研究軟體的 release archive/wheel 是否與對應 tag source 可重建一致；deterministic audit 能找到多少 artifact drift？ | build backend 正常加入 generated files，差異未必有害。 |
| 8 | `research-actions-permissions` | **82** | 研究軟體 repository 的 GitHub Actions 是否普遍授予超出 job 實際需求的 token permissions，靜態最小權限分析能否找出可行修正？ | 現有 Scorecard 已足夠，或無法建立可靠 ground truth。 |
| 9 | `research-readme-smoketest` | **81** | 研究軟體 README 的主要重現命令，在乾淨 CPU 環境中有多少能成功產生所宣稱 artifact；結構化 smoketest 能否降低人工重現時間？ | 目前 sandbox/網路不足以安全重跑多 repo。 |
| 10 | `ro-crate-minimum-validator` | **81** | 只符合 RO-Crate 語法的研究包，有多少仍缺少實際重現所需的 command、environment 與 checksum；最小 reproducibility profile 是否可提高可用性？ | 新 profile 只是主觀偏好，或已被 Workflow Run Crate 處理。 |
| 11 | `data-license-mesh` | **80** | 同一公開資料集在入口頁、API metadata、下載檔與 repository 中的 license 宣告有多常衝突？ | 衝突多為合法的 scope 差異，難以 ground truth。 |
| 12 | `sensor-metadata` | **79** | 公開低成本環境感測資料是否缺少足以比較的單位、校正、偵測極限與時間基準 metadata？ | rubric 主觀且樣本異質。 |
| 13 | `hxl-sheet-guard` | **78** | 人道資料試算表的 HXL 標籤與實際欄位值有多少語義不一致，值級檢查能否超越 header validation？ | 值級規則造成高誤判。 |
| 14 | `cff-version-drift` | **77** | CITATION.cff 的 version 是否與 package manifest 漂移，且保守 checker 能否找出無歧義錯誤？ | eligible 樣本太少，且題目已在既有 repo 完成。 |
| 15 | `research-pdf-a11y` | **77** | 公開研究 PDF 中的圖表是否缺少可提取文字替代、標題與 reading order；靜態 preflight 能否可靠識別高風險頁面？ | 文字替代品質是語義問題，靜態特徵不足。 |
| 16 | `government-schema-drift` | **76** | 同一政府 API 在未改版 URL 下有多少次欄位增刪/型別改變，consumer-driven contract 能否提早阻擋破壞性更新？ | 缺少可靠歷史快照，單回合無法觀察。 |
| 17 | `sbom-diff-auditor` | **76** | 對同一小型開源專案，不同 SBOM 產生器輸出的元件集合與版本有多不一致，最小 consensus schema 能否辨識高信心差異？ | 無法建立完整 ground truth，工具安裝受限。 |
| 18 | `climate-cf-quickcheck` | **75** | 小型氣候/環境 NetCDF 資料在通過基本解析後，仍有多少會因 CF convention 的單位、座標或 missing-value 問題導致錯誤分析？ | 成熟工具已完整解決，沒有研究新意。 |
| 19 | `dataset-privacy-lite` | **72** | 公開 tabular datasets 的高精度低召回 PII heuristic，能否在不讀取內容語義的情況下找出明顯個資欄位而維持低誤報？ | 只能用合成資料，無法證明真實效能；成熟工具已足夠。 |
| 20 | `example-secret-guard` | **69** | 文件與範例設定中的「看似範例」字串，有多少其實符合有效 credential 結構；context-aware detector 能否降低 secret scanner 誤報？ | 無法安全取得真實 ground truth；成熟工具已處理。 |
| 21 | `open-textbook-linkrot` | **69** | 開放教材中的外部引用失效是否集中在特定資源類型，且 archive-aware repair 建議能否提高可恢復率？ | 網路當下狀態波動，且 archive 配對可能錯。 |

## Selection

Selected: `agent-completion-ledger` (96/100). The post-experiment red team later reduced the novelty claim: the primary rate is the complement of benchmark support among generated patches, and generic agent-evidence ledgers already exist. The retained contribution is the frozen adapter, evidence-state contract, reproducible outputs, and falsification record.
