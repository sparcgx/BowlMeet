# BowlMeet v0.4.2-R7 — Live ↔ Current Score Sync

這個目錄可直接放到 GitHub Pages。

## GitHub Pages 部署

1. 建立一個 GitHub repository，例如 `BowlMeet`。
2. 將本目錄所有檔案放到 repository 根目錄。
3. GitHub → Repository → Settings → Pages。
4. Build and deployment 選 `Deploy from a branch`。
5. Branch 選 `main`，Folder 選 `/ (root)`，按 Save。
6. GitHub Pages 完成後，用 iPhone Safari 開啟 Pages 網址。
7. 先開 `deployment-test.html`，確認 JavaScript、Secure Context、IndexedDB、Service Worker API 都正常。
8. 再開 `index.html` 測試 BowlMeet 手機功能選單。

## iPhone 驗收

依序切換：

- 球聚活動
- 我的成績
- 成績紀錄
- 多人同步
- 現場模式

每次切換後，下方應只顯示對應功能。

## PWA

在 iPhone Safari 開啟 `index.html` → 分享 → 加入主畫面。

## Supabase

多人同步／Player Claim 仍需在 BowlMeet「多人同步」頁輸入自己的 Supabase Project URL 與 Anon Key。`supabase_schema.sql` 不包含你的專案密鑰。


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
