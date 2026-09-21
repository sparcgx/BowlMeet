# BowlMeet v0.4.2-R3 — Personal PIN Change

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
