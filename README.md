# BowlMeet v0.4.4-dev.4 — History Search & Filter Enhancement

BowlMeet 採 **Field-First**：打開 App 後直接進入「球聚現場」，建立玩家並進行標準 10 格即時計分。

## v0.4.4-dev.1 開發重點

- 快速開場新增「最近／常用玩家」，可點一下加入。
- 新增「沿用上一場」，快速帶入上一場參加玩家。
- 按「開始現場記分」時至少需要一位玩家，避免建立空球聚。
- Unified Score History 新增「取消公開」與「重新公開」。
- 取消公開只移除公開版本；本機 Session、局數、平均與個人分析資料不刪除。
- 取消公開狀態會參與公開同步合併，避免下一次自動同步把已取消的 Session 再次發布。
- 公開控制狀態會納入本機安全快照與完整備份。
- 跨版本防復活由 Supabase `bowling_group_push` 保留 `recordControls` tombstone；`supabase_v044_public_record_control_patch.sql` 已於 2026-09-22 套用至 BowlMeet Supabase。
- v0.4.3.3-R1 仍為 Stable / Freeze Baseline；本版在 `v0.4.4-dev.1` 分支開發。

## GitHub Pages 部署

1. Repository 使用 `main` 分支與 `/ (root)` 發佈。
2. 先開 `deployment-test.html`，確認 JavaScript、HTTPS / Secure Context、IndexedDB 與 Service Worker。
3. 再開 `index.html` 進行 BowlMeet 實機驗收。
4. iPhone Safari 可使用「分享 → 加入主畫面」安裝為 PWA。

## v0.4.4-dev.4 History Search & Filter Enhancement

- 沿用 Unified Score History，不建立第二套歷史資料。
- 保留來源分頁：全部 / 我的紀錄 / 公開歷史。
- 全文搜尋擴充：日期、玩家、球館、球道、球聚名稱。
- 新增開始日期 / 結束日期精準篩選。
- 新增玩家、球館、球道動態選單。
- 新增公開狀態：全部狀態 / 已公開 / 已取消公開 / 僅本機 / 公開未匯入 / 本機＋公開。
- 來源分頁、全文搜尋、精準條件與排序可同時組合。
- 新增篩選摘要與「清除篩選」。
- Session ID 去重、取消公開 tombstone、本機資料安全規則維持不變。

## v0.4.4-dev.4 Automated Gate

- JavaScript syntax ✅ PASS
- Static HTML duplicate ID ✅ 0
- Literal DOM reference missing ✅ 0
- 日期範圍 ✅ PASS
- 玩家 ✅ PASS
- 球館 + 球道 ✅ PASS
- 已公開 / 已取消公開 / 僅本機 / 公開未匯入 / 本機＋公開 ✅ PASS
- 全文搜尋球聚名稱 ✅ PASS
- 最新 / 最舊排序 ✅ PASS
- 來源 tab + 精準條件組合 ✅ PASS
- Device Preview：`/preview/v0.4.4-dev.4/` ✅ Ready
- Preview localStorage / IndexedDB / Cache / Cloud ✅ Isolated
- Preview Cloud：`V44D44`，目前 0 sessions / 0 meetups
- Stable PUBLIC：revision 21 / 4 sessions / 4 meetups / v0.4.3.3-R1，未變更
- Cloud Push / Pull 多場 History 資料保留 ✅ PASS
- recordControls Push / Pull 保留 ✅ PASS
- 動態玩家 / 球館 / 球道選單保留目前選值 ✅ PASS
- 篩選摘要 ✅ PASS
- 清除篩選回復預設並重新 render ✅ PASS
- Live Regression 使用 transaction + ROLLBACK，Preview Cloud 未污染 ✅ PASS
- 正式 PUBLIC 維持 revision 21 ✅ 未變更
- 狀態：**Device Preview & Automated Live Regression PASS / Manual Device Acceptance Pending**

## v0.4.4-dev.3 Manual Device Acceptance

- 個人分析頁開啟與球員切換 ✅ PASS
- 最高 / 最低單局 ✅ PASS
- 最近 5 局平均 ✅ PASS
- 最近 5 / 10 / 全部歷史範圍切換 ✅ PASS
- Strike % ✅ PASS
- Spare % ✅ PASS
- Open Frame % ✅ PASS
- 逐格資料覆蓋率 ✅ PASS
- 第 10 格特殊情境顯示正常 ✅ PASS
- 關閉 / 重新開啟後分析結果一致 ✅ PASS
- Stable / dev.1 / dev.2 Preview 資料隔離 ✅ PASS
- 正式 PUBLIC 未受影響 ✅ PASS
- 結論：**v0.4.4-dev.3 Validation Complete**

## v0.4.4-dev.3 Personal Performance Analytics

- 沿用既有「個人分析」，不建立第二套統計模組。
- 新增「最近 5 局」分析範圍。
- KPI 新增：最低單局、最近 5 局平均。
- 保留：總局數、區間平均、生涯平均、PB、最近 10 局、200+。
- 新增逐格表現：Strike %、Spare %、Open Frame %、逐格資料覆蓋率。
- Strike / Spare / Open 只使用具有完整 `bowlingFrames` 的正式完成局。
- 舊版匯入或只保存單局總分的紀錄仍參與平均、PB、趨勢，但不推算逐格結果。
- 逐格分類以每局 10 個 Frame 為母體：第一球 10 = Strike；非 Strike 且兩球合計 10 = Spare；其餘 = Open。
- 近期趨勢沿用成績趨勢圖、5 局移動平均與最近 5 / 10 / 20 局比較。

## v0.4.4-dev.3 Automated Gate

- JavaScript syntax ✅ PASS
- Static HTML duplicate ID ✅ 0
- Literal DOM reference missing ✅ 0
- Recent 5 range regression ✅ PASS
- Frame analytics regression：3 Strike / 2 Spare / 5 Open ✅ PASS
- Frame coverage regression：1 / 2 局 = 50% ✅ PASS
- 舊版總分資料排除逐格統計 ✅ PASS
- Device Preview：`/preview/v0.4.4-dev.3/` ✅ Ready
- Preview localStorage / IndexedDB / Cache / Cloud ✅ Isolated
- Preview Cloud：`V44D33`，目前 0 sessions / 0 meetups
- Stable PUBLIC：revision 21 / 4 sessions / 4 meetups / v0.4.3.3-R1，未變更
- 雲端 Push / Pull 保留完整 bowlingFrames ✅ PASS
- 第 10 格 Strike / Spare / Open ✅ PASS
- JSON / normalize reload 後逐格分析一致 ✅ PASS
- Preview Cloud rollback 後仍為 0 sessions / 0 meetups ✅ PASS
- 正式 PUBLIC 維持 revision 21 ✅ 未變更
- 狀態：**Device Preview & Live Regression PASS / dev.3 Validation Complete**

## v0.4.4-dev.2 Automated Gate

- JavaScript syntax ✅ PASS
- Static HTML duplicate ID ✅ 0
- Literal DOM reference missing ✅ 0
- Post-game summary calculation regression ✅ PASS
- 未完成局排除統計 ✅ PASS
- PWA / Manifest / Deployment Test ✅ PASS
- Isolated Device Preview ✅ Ready
- Preview local storage / IndexedDB / Cache / Cloud ✅ Isolated
- Preview Cloud：`V44D22`，目前 0 sessions / 0 meetups
- Stable PUBLIC：revision 21 / 4 sessions / 4 meetups / v0.4.3.3-R1，未變更
- 狀態：**Device Preview & Live Regression PASS / dev.2 Validation Complete**

## v0.4.4-dev.2 Manual Device Acceptance

- 完成球聚後自動開啟賽後摘要 ✅ PASS
- 玩家數 ✅ PASS
- 正式完成局數 ✅ PASS
- 未完成 10 格排除統計 ✅ PASS
- 總分 / 平均 / 最高單局 ✅ PASS
- 每位玩家局數 / 總分 / 平均 / 最高 ✅ PASS
- 分享球聚卡導流 ✅ PASS
- 查看成績紀錄導流 ✅ PASS
- 過往球聚重新開啟賽後摘要 ✅ PASS
- 關閉 / 重新開啟資料保留 ✅ PASS
- Stable / dev.1 Preview 資料隔離 ✅ PASS
- 結論：**v0.4.4-dev.2 Validation Complete**

## v0.4.4-dev.2 Session Summary & Post-Game Review

- 完成球聚後自動開啟賽後摘要 Dialog。
- 已完成球聚可從「過往球聚」再次開啟賽後摘要。
- KPI：玩家數、正式完成局數、總分、平均、最高單局。
- 玩家摘要：完成局、總分、平均、最高。
- 未完成 10 格不列入正式局數、平均與最高分。
- 可從賽後摘要直接前往「分享球聚卡」或「成績紀錄」。
- 不新增第二套成績資料；摘要完全由既有 Meetup + Session 即時計算。
- v0.4.4-dev.1 已完成 Device Preview & Live Regression；dev.2 從其驗收完成分支建立。

## v0.4.4-dev.1 Device Preview & Live Regression

- Device Preview：`/preview/v0.4.4-dev.1/` ✅ 已建立
- Stable 根目錄：v0.4.3.3-R1 ✅ 未覆蓋
- Preview localStorage / IndexedDB ✅ 獨立 namespace
- Preview Service Worker Cache ✅ 僅清理 `bowlmeet-preview-v044-*`
- Preview 公開雲端：`DEV442` ✅ 與正式 `PUBLIC` 隔離
- DEV442 seed / pull ✅ PASS
- 取消公開 ✅ PASS
- v0.4.3.3-R1 legacy repush 防復活 ✅ PASS
- 重新公開 ✅ PASS
- stale revision conflict ✅ PASS
- 錯誤 PIN rejection ✅ PASS
- Regression 完成後 DEV442 已清空：0 sessions / 0 meetups / 0 recordControls
- 正式 PUBLIC 維持 revision 21 / 4 sessions / 4 meetups / v0.4.3.3-R1
- 狀態：**Device Preview & Live Regression PASS / dev.1 Validation Complete**

## v0.4.4-dev.1 Manual Device Acceptance

- Device Preview 實機開啟 ✅ PASS
- 球聚建立 / 玩家加入 ✅ PASS
- 10 格現場計分 ✅ PASS
- 下一局流程 ✅ PASS
- 關閉 / 重新開啟資料保留 ✅ PASS
- 最近／常用玩家 ✅ PASS
- 沿用上一場 ✅ PASS
- 成績紀錄公開狀態 ✅ PASS
- 取消公開 ✅ PASS
- 重新整理後狀態維持 ✅ PASS
- 重新公開 ✅ PASS
- Stable v0.4.3.3-R1 未受 Preview 影響 ✅ PASS
- 結論：**v0.4.4-dev.1 Validation Complete**

## v0.4.4-dev.1 Database Migration Status

- Supabase migration：`v044_public_record_control_compat` ✅ Applied
- Tombstone remove 測試 ✅ PASS
- v0.4.3.3-R1 legacy repush 防復活 ✅ PASS
- 測試以 transaction + ROLLBACK 執行，正式 PUBLIC 資料維持 revision 21。
- 狀態：**Database Migration Applied / Ready for Device Preview**

## v0.4.4-dev.1 驗收重點

依序確認：

- 球聚現場：最近／常用玩家、沿用上一場、新增玩家、10 格記分、Strike / Spare、自動帶入本次計分。
- 本次計分：目前球聚的完整單局總分正確。
- 成績紀錄：全部 / 我的紀錄 / 公開歷史切換、Session ID 去重、取消公開／重新公開正常。
- 我的成績：Player ID / Personal PIN 與個人成績同步正常。
- 分享成績：球聚完整成績卡可顯示所有玩家、各局與總和。
- 資料安全：備份、還原、快照、完整性檢查、PWA 安全更新。
- 設定：BowlMeet Cloud、公開歷史同步、我的成績同步、App / PWA。
- 舊版多裝置 Room Code 功能僅保留在「設定 → 進階｜多裝置協作（舊版相容）」。

## 雲端架構

- 一般使用者不需要輸入 Supabase Project URL 或 Publishable Key；網站使用內建 BowlMeet Cloud 設定。
- 公開歷史已整合到「成績紀錄」，使用單一公開資料來源。
- 「我的成績」使用 Player ID + 6 位 Personal PIN。
- 舊 Room Code 多裝置同步只保留相容用途，不屬於主要操作流程。
- `supabase_schema.sql` 不包含 PostgreSQL 密碼、service_role 或 secret key。

## PWA

- Android / Chrome / Edge：到「設定 → App / PWA」使用安裝功能。
- iPhone / iPad：Safari → 分享 → 加入主畫面。
- PWA 更新可從「設定」檢查；安全套用仍在「資料安全 → PWA 安全更新」，套用前會建立快照。

## v0.4.2 Group History & Shared Records

- 新增「群組歷史」分頁。
- A 建立共享群組後，可把目前裝置的球聚與計分卡歷史上傳到群組。
- B 使用 Group Code + Group PIN 加入後，可查看群組全部共享歷史。
- Viewer 只讀，不會把本機紀錄上傳。
- Host / Editor 可將本機歷史與群組歷史增量合併。
- 群組共享資料與「我的成績」分開；加入群組不會自動改寫本機歷史。
- 要啟用此功能，請重新在 Supabase SQL Editor 執行最新版 `supabase_schema.sql`。


## v0.4.2-R1 Built-in Cloud Configuration

- 內建 Supabase Project URL 與 Publishable Key。
- 一般使用者不再需要輸入 Project URL / Key。
- 多人同步頁改為 BowlMeet Cloud 連線狀態與裝置名稱。
- 啟動時自動檢查雲端連線。
- Group Code / Group PIN、Room PIN、Personal PIN 仍維持動態與個別儲存。
- 不包含 PostgreSQL 密碼、service_role 或 secret key。
- v0.4.2 Group History 第一次使用前仍需在 Supabase SQL Editor 執行最新版 `supabase_schema.sql`。


## v0.4.2-R2 OCR Quality Enhancement

- 拍照匯入新增「高品質 / 標準 / 快速」辨識品質。
- 高品質模式提高處理解析度，逐格進行多次 OCR。
- 藍色手寫筆跡自動分離，降低表格線與印刷字干擾。
- 分數使用數字白名單與多種 PSM 結果比對；結果一致時提升信心，互相矛盾時降低信心並要求人工確認。
- 姓名也採多重辨識，低信心欄位仍保留人工驗證。
- 低解析度照片會顯示拍攝品質提示。
- 驗證中心會顯示多重辨識 PASS 標示。


## v0.4.2-R3 Personal PIN Change

- 「我的 BowlMeet 身分」在已連結狀態新增「變更密碼」。
- 變更流程需輸入目前 Personal PIN、新 PIN、再次確認新 PIN。
- 新 PIN 仍限制 6 位數字。
- 變更成功後舊 PIN 立即失效，Player ID 與個人成績維持不變。
- 目前裝置會自動改用新 PIN；其他已連結裝置需要使用新 PIN 重新連結。
- 新增 Supabase RPC `bowling_player_change_pin`；部署後需重新執行最新版 `supabase_schema.sql`。


## v0.4.2-R4 Live 10-Frame Scoring

- 「現場模式」由直接輸入單局總分，改為標準保齡球一局 10 格記分。
- 第 1～9 格輸入兩球倒瓶數；全倒後第二球自動停用。
- 第 10 格依全倒／補中規則自動開放第三球。
- 自動計算 Strike、Spare 加成與單局總分，最高 300 分。
- 每球輸入即本機儲存並沿用多人房間／群組同步。
- 完成 10 格後才把單局總分寫回既有 scores 資料，因此排行榜、個人成績、群組歷史仍沿用原本資料結構。
- 舊版只有單局總分的紀錄仍可顯示；開始輸入 10 格後會切換成新的逐格記分。
- 手機版 10 格使用區塊內橫向滑動，不讓整個頁面超出螢幕。


## v0.4.2-R5 Meetup + Live Unified

- 將「球聚活動」與「現場模式」合併成同一個「球聚／現場」分頁。
- 上半部保留球聚建立、編輯、活動清單與球員設定。
- 下半部直接嵌入現場 10 格即時計分。
- 活動清單的「現場記分」會直接捲動到同頁的記分區，不再切換到另一個分頁。
- 保留「完整記分」作為獨立的本次記分表入口。
- 原本程式內呼叫 `liveView` 的流程保留相容，會自動導向「球聚／現場」並定位到即時計分區。
- 手機版仍採單頁垂直流程，10 格記分區維持區塊內左右滑動。


## v0.4.2-R6 Live Quick Entry

- 「球聚／現場」進一步精簡為單一「球聚現場」工作頁。
- 主要流程改為：日期 / 球館 / 球道 / 局數 / 玩家 →「開始現場記分」→ 直接填 10 格。
- 玩家可直接用逗號、頓號或換行一次輸入多人，不需要先建立球員名冊。
- 現場進行中可直接輸入姓名按「＋加入玩家」，新玩家立即加入目前球聚與 10 格記分。
- 活動名稱、狀態、備註、名冊挑選移到「更多設定」，不干擾一般現場流程。
- 過往球聚與管理功能改為收合區，預設不佔主要畫面。
- 保留完整 10 格 Strike / Spare 自動計分、排行榜、多人同步、群組歷史及既有資料相容性。


## v0.4.2-R7 Live ↔ Current Score Sync

- 現場 10 格記分與「本次計分」改為同一張 session 資料。
- 每球輸入後會同步目前 session 到「本次計分」草稿。
- 一局 10 格完成後，最終單局分數自動出現在「本次計分」對應局次。
- 從「球聚現場」切到「本次計分」時，會自動載入目前球聚的 linked session，不需要再手動選成績紀錄。
- 現場新增玩家或清除本局時也同步更新「本次計分」。
- 未完成的 10 格不會被當成正式單局分數；完成後才寫入 0–300 的單局總分。


## v0.4.2-R8 Single Public History

- 原「群組歷史」改為單一「公開歷史」。
- 不再建立多個群組，也不需要輸入 Group Code / Group PIN。
- 所有 BowlMeet 裝置自動連到同一份公開雲端歷史。
- 公開歷史使用既有 Supabase group RPC 與固定公共識別，第一次使用會自動建立公開資料容器。
- 所有人可查看與新增公開紀錄；公開頁保留搜尋、排序、重新整理、同步我的紀錄與匯入至本機。
- 新增／修改本機成績仍會透過既有自動同步流程合併到公開歷史。
- 舊的私人群組設定不再作為目前介面的連線目標；本機既有成績不會被刪除。
- 公開模式不適合保存不希望公開的私人資訊。


## v0.4.3 Field-First Simplification

- 「球聚現場」改為第一個分頁與預設首頁，日常流程直接從玩家與 10 格記分開始。
- 「本次計分」保留為完整計分卡、人工修正與紙本快速登錄入口。
- 主選單移除「多人同步」，改新增「設定」並移到最後。
- BowlMeet Cloud、裝置名稱、公開歷史同步與我的成績同步集中到「設定」。
- 公開歷史與個人成績保留背景同步，不再要求一般使用者理解 Room Code / Role / Revision。
- 舊版 Room Code 多裝置協作未直接刪除；移到「設定 → 進階｜多裝置協作（舊版相容）」。
- 既有多人房間資料、RPC 與舊裝置相容性暫時保留，後續實機確認無需求後再決定是否做正式移除。
- 主選單順序重新整理為現場作業優先，設定與維護功能後置。


## v0.4.3.1 Full Meetup Share Card

- 「分享卡類型」新增「球聚完整成績卡」。
- 選擇單一球聚後，卡片會顯示該場所有玩家、每一局分數與個人總和。
- 依球聚設定顯示 G1～G6；未完成局以「—」表示。
- 預設卡片標題使用「日期 + 球聚卡」，例如「2026/09/20 球聚卡」。
- 卡片上方保留玩家數、已記局數、平均與最高分 KPI。
- 支援 PNG 下載與手機原生分享，檔名使用「BowlMeet_日期_球聚卡.png」。


## v0.4.3.2 Unified Score History

- 移除獨立「公開歷史」主分頁，公開雲端紀錄整合進「成績紀錄」。
- 成績紀錄新增「全部 / 我的紀錄 / 公開歷史」來源切換。
- 本機 sessions 與公開 groupRemote.sessions 以 Session ID 自動去重，相同計分卡只顯示一次。
- 雙來源紀錄標示「我的紀錄＋已公開」。
- 本機紀錄可編輯、分享與刪除本機版本；若公開副本存在，刪除本機不會刪除公開資料。
- 公開但尚未存在本機的計分卡可個別「匯入我的紀錄」；匯入前會建立安全快照。
- 成績紀錄頁提供「重新整理公開紀錄」，雲端自動同步開關仍集中於「設定」。
- 「設定 → 查看公開紀錄」會直接開啟成績紀錄並切換到「公開歷史」來源。
- 舊程式呼叫 groupView 仍保留相容 alias，會自動導向統一成績紀錄頁。


## v0.4.3.3 Navigation & Utility Consolidation

- 移除頂部右上角「安裝 App / 備份 / 還原」三個維護按鈕，Top Bar 僅保留 BowlMeet 品牌與版本。
- 「安裝 App」移到「設定 → App / PWA」，並集中顯示 App 狀態、目前版本與更新檢查。
- 分享成績頁不再額外顯示 PWA 安裝區，避免相同功能散落多處。
- 「備份 / 還原」正式集中到「資料安全 → 備份與還原」。
- 資料安全保留快照、完整性檢查與 PWA 安全更新，各維護操作依功能分組。
- 還原仍沿用智慧合併 / 只新增 / 完全取代，且套用前自動建立安全快照。
- 原有匯出、匯入與安裝事件 ID 保留，因此既有功能邏輯不需要重新建立資料或遷移。


## v0.4.3.3-R1 Regression & Cleanup Fix

- 修正「設定 → App / PWA → 檢查更新」結果原本只顯示在資料安全頁的問題；現在設定頁同步顯示檢查狀態。
- 修正網路離線 / 恢復連線時「成績紀錄」公開雲端狀態未即時更新。
- 切換進「成績紀錄」時會重新渲染本機與公開來源狀態。
- 移除已廢棄的獨立公開歷史 UI renderer 與不存在的 Group History DOM 參照；保留公開雲端 Pull / Push / Merge 底層。
- 清理使用者可見的舊版 v0.4.1 PWA / Data Safety 文字。
- 更新 manifest、deployment-test 與 README，使說明符合目前 Field-First、Unified Score History 與 Settings 架構。
