# BowlMeet v0.4.1-R3 — iPhone Safari Deployment Test

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
