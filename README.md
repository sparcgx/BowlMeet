# BowlMeet v0.4.2 — Group History & Shared Records

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
