# BowlMeet v0.4.7.0-dev.4 — Accessibility & Theme Hardening

- 基線：`v0.4.7.0-dev.3` accepted commit `adf2db460c6181f8985bbbbb8a7c26df552e498b`。
- 新增 `assets/theme-center-dev4-accessibility.css`，最後載入 Accessibility / Theme Hardening layer。
- 新增 Skip Link 與 `main#mainContent` landmark。
- Desktop tabs、Mobile Dock、More Sheet 由 JavaScript 維護 `aria-current="page"`。
- More Sheet 補上 `role="dialog"`、`aria-modal`、標題／說明關聯、Tab focus trap 與 focus return。
- Player Session / Post-game Review / PWA Update / Restore 四個 Dialog 補齊 modal semantics；PWA / Restore Esc 關閉後會返回原焦點。
- 全域 `:focus-visible` 使用 Theme Token；Dark Night / High Contrast 另有可讀性 hardening。
- Status feedback 除顏色外加入文字／形狀 cue；Safety / PWA feedback 使用 live-region。
- 新增 `prefers-contrast: more` 與 `forced-colors: active` 支援。
- Reduced Motion / Reduced Transparency 與 dev.1～dev.3 Theme Center 保持相容。
- pointer coarse 互動目標至少 44px。
- `DB_VERSION = 2`、`PUBLIC_HISTORY_CODE = PUBLIC`、PUBLIC / Sync / Backup / Restore / Supabase Schema 不變。
- Accessibility Automated Gate：**45 PASS / 0 FAIL**。
- Preview Isolation Gate：**25 PASS / 0 FAIL**。
- Preview-only PR：#65，已合併到 main；只新增 `/preview/v0.4.7.0-dev.4/`。
- Preview Cloud：OFF；LocalStorage / IndexedDB / PWA Cache 使用 `v0470d4` 隔離 namespace。
- 正式 root `index.html` blob 與 `stable/v0.4.6.7` 完全一致。
- 下一關：Keyboard / iPhone / PWA / High Contrast 實機驗收。

# BowlMeet v0.4.7.0-dev.3-R2 — More Sheet Readability Fix

- 依 iPhone 實機截圖修正「更多功能」直向 3 欄過擠與第三欄裁切問題。
- Phone portrait <=680px 固定 **2 欄**；landscape 維持 4 欄。
- 功能名稱最多 2 行，不再使用 ellipsis 裁切。
- icon 調整為 28px，卡片 min-height 82px，padding / gap 重整。
- 最後「設定」維持滿寬，降低視覺重量。
- 關閉按鈕重新置中。
- R2 Source Gate：**23 PASS / 0 FAIL**。
- JavaScript delta：**0**。
- DB / PUBLIC / Sync / Backup / Restore / Supabase Schema：**無變更**。
- Preview Isolation Gate：**17 PASS / 0 FAIL**。
- Preview-only PR：#64，已更新原 `/preview/v0.4.7.0-dev.3/`。
- Preview merge commit：`61d9a253c984d46513d3a94b6b46751fbe1ac7f2`。
- 正式 root 仍與 `stable/v0.4.6.7` 完全一致。
- dev.3 R2 Manual Acceptance：**5 PASS / 0 FAIL**。
- iPhone 實機驗收：**PASS**。
- `v0.4.7.0-dev.3｜Mobile / PWA Theme Optimization` 階段正式完成。
- 下一版：`v0.4.7.0-dev.4｜Accessibility & Theme Hardening`。

# BowlMeet v0.4.7.0-dev.3-R1 — Mobile Navigation Alignment Fix

- 修正手機下方 Dock 與「更多」選單位移。
- Dock 依實際 4 個主要按鈕固定為 4 等分。
- Dock / Backdrop / More Sheet mount 到 `body`，不再受 90～120% `.app` layout zoom 影響。
- 更多選單：直向 3 欄＋最後「設定」滿寬；<=420px 2 欄；短螢幕橫向 4 欄。
- R1 Source Gate：**23 PASS / 0 FAIL**。
- R1 Preview Isolation Gate：**16 PASS / 0 FAIL**。
- UI-only JavaScript delta：364 bytes；移除 mount helper 後核心 JS drift = **0**。
- Preview-only PR：#63，已更新原 `/preview/v0.4.7.0-dev.3/`。
- 正式 root 仍與 `stable/v0.4.6.7` 完全一致。

# BowlMeet v0.4.7.0-dev.3 — Mobile / PWA Theme Optimization

- 基線：`v0.4.7.0-dev.2` commit `2802ed5a722c5eb0bc2d0683d3710ac977d25cb0`。
- 新增 `assets/theme-center-dev3-mobile.css`，只處理 Mobile / PWA Responsive 與主題呈現。
- Safe Area 統一：top / right / bottom / left 使用 `env(safe-area-inset-*)`。
- Mobile Dock / More Sheet：固定不受 90～120% 版面縮放影響，並避開 Home Indicator。
- More Sheet 使用 `dvh` 最大高度與內層捲動，改善短螢幕及鍵盤彈出。
- iPhone 表單控制強制 16px，避免 Safari focus 自動放大。
- 成績／歷史／排行榜／玩家表格統一手機水平滑動，Sticky 球員欄使用 Theme Token 背景。
- Live Scoring 觸控目標、輸入框與 Mobile Bar 重新對齊 Dock / Safe Area。
- PWA / Dialog / Post-game Review / Player Session 使用 Dynamic Viewport Height。
- 420px / 360px / landscape phone 皆有專屬 Responsive Gate。
- Standalone PWA 由 `display-mode: standalone` 與 `navigator.standalone` 雙路徑識別。
- Dark Night 與 High Contrast 另補 Mobile Dock / Sticky 欄／Active State 可讀性。
- `prefers-reduced-motion`、Transparency OFF 與 dev.2 Theme Tokens 保持相容。
- `DB_VERSION = 2`、PUBLIC、Sync、Backup / Restore、Supabase Schema 不變。
- Mobile / PWA Automated Gate：**30 PASS / 0 FAIL**。
- Preview Isolation Gate：**21 PASS / 0 FAIL**。
- UI-only JavaScript delta：**206 bytes**；移除 Standalone 標記後核心 JS drift = **0**。
- Preview-only PR：#62，已合併到 main；只新增 `/preview/v0.4.7.0-dev.3/`。
- Preview Cloud：OFF；LocalStorage / IndexedDB / PWA Cache 使用 `v0470d3` 隔離 namespace。
- 正式 root `index.html` blob 與 `stable/v0.4.6.7` 完全一致。
- 下一關：iPhone Safari / PWA Standalone 實機驗收。

# BowlMeet v0.4.7.0-dev.2 — Theme Token & Full Component Coverage

- 基線：`v0.4.7.0-dev.1` commit `114b148d9700f720ccd9a4a0e6bdc7f576148b64`。
- 新增 `assets/theme-center-dev2.css` Semantic Theme Token Layer，最後載入以覆蓋歷史硬編碼視覺。
- Semantic Tokens：surface / text / border / focus / status / chart / overlay / sticky surface。
- 完整覆蓋：Score Table、Unified History、OCR / Verification、Meetup / Roster、Player Analytics、Live Scoring、Settings、PWA / Sync / Safety、Awards、Share、Dialog / Backdrop。
- 六主題與 5 組快速預設沿用 dev.1；Theme / Layout LocalStorage key 不變。
- Dark Night 補強 legacy glass / sticky / form / status 對比。
- High Contrast 補強 focus outline、狀態 border 與非純色彩識別。
- Transparency OFF / Reduced Transparency 擴大到 History / Player Hub / Live Mobile Bar 等玻璃元件。
- 分享輸出的 `.share-canvas` 保持白底，避免主題污染可分享／列印成績卡。
- `DB_VERSION = 2`、`PUBLIC_HISTORY_CODE = PUBLIC`、PUBLIC payload、Backup / Restore、Sync、Supabase Schema 均不變。
- PWA Cache 更新為 `v0.4.7.0-dev.2`，並加入 Theme Token stylesheet。
- Theme Coverage Gate：**40 PASS / 0 FAIL**。
- Legacy hardcoded-color selector coverage：**342 / 342**。
- JavaScript logic drift from dev.1：**0**。
- 隔離 Preview Gate：**16 PASS / 0 FAIL**。
- Preview-only PR：#61，已合併到 main；只新增 `/preview/v0.4.7.0-dev.2/`。
- Preview Cloud：OFF；LocalStorage / IndexedDB / PWA Cache 使用 `v0470d2` 隔離 namespace。
- 正式 root `index.html` blob 與 `stable/v0.4.6.7` 完全一致。
- 下一關：iPhone / PWA / Desktop 跨模組視覺與互動驗收。

# BowlMeet v0.4.7.0-dev.1 — Theme Center Foundation

- 基線：`stable/v0.4.6.7` / `main` commit `bf6054deeaa0658ab807c3c60ad095d7060d0de7`。
- 版面設定正式升級為 **版面設計｜Layout & Theme Design**。
- 新增 6 組主題：Default / Liquid Glass / Clear Blue / Soft Violet / Dark Night / High Contrast。
- 新增 5 組快速套用：標準工作 / 行動瀏覽 / 現場大字 / 玻璃展示 / 夜間模式。
- 新增卡片圓角、陰影強度、色彩強度、Motion、Transparency 本機偏好。
- 支援 `prefers-reduced-motion`、`prefers-reduced-transparency` 與無 backdrop-filter fallback。
- `THEME_PREFS_KEY = bowlingMeetup.themePreferences.v1`；`LAYOUT_PREFS_KEY` 沿用 `bowlingMeetup.layoutPreferences.v1`。
- Theme / Layout 只屬於 Local UI Preferences，不進 PUBLIC / Sync / Backup / Restore / Snapshot payload。
- `DB_VERSION = 2`、`PUBLIC_HISTORY_CODE = PUBLIC` 保持不變。
- Theme Center Static Gate：**39/39 PASS / 0 FAIL**。
- JavaScript Parse / CSS Brace / PWA Manifest / Service Worker Cache / Local-only Data Isolation：**PASS**。
- iPhone / PWA Manual Device Acceptance：**PENDING**（10 項）。
- 舊 dev.1 已封存：`archive/v0.4.7.0-dev.1-pre-v0.4.6.7-refresh-20260926`。
- Theme Center Foundation Static Gate：**33 PASS / 0 FAIL**。
- 隔離 Preview Gate：**15 PASS / 0 FAIL**。
- Preview-only PR：#60，已合併到 main；只新增 `/preview/v0.4.7.0-dev.1/`。
- Preview Cloud：OFF；LocalStorage / IndexedDB / PWA Cache 均使用 `v0470d1` 隔離 namespace。
- 正式 root `index.html` blob 與 `stable/v0.4.6.7` 完全一致；正式版未升級。
- 下一關：iPhone / PWA / Desktop Theme Center 視覺與互動驗收。

# BowlMeet v0.4.6.7-dev.1 — Preview Deployment

- 基線：`stable/v0.4.6.6`。
- 修正完成球聚後現場狀態未清空。
- 新增動態局數：現場自動增加下一局、＋局／−局，最高維持 6 局。
- Source Gate：45/45 PASS。
- Preview：`/preview/v0.4.6.7-dev.1/`。
- 此段更新同時作為 GitHub Pages Preview 重新部署觸發紀錄。

# BowlMeet v0.4.6.2.1 — Stable Hotfix

基線：`stable/v0.4.6.2`。

- 修正 iPhone Safari / PWA「成績紀錄」每局表格欄位垂直掉成單欄。
- 根因：新版 HTML 與舊版 Liquid Glass CSS Cache 不同步。
- CSS URL 加入版本指紋，強制重新抓取。
- HTML 加入 Critical Grid fallback，即使外部 CSS cache 異常仍維持 9 欄。
- 表格欄位：球員 / 1 / 2 / 3 / 4 / 5 / 6 / 總分 / 平均。
- 手機水平滑動與 sticky 球員欄維持正常。
- Root Fix Gate：**16/16 PASS**
- Isolated Preview Gate：**21/21 PASS**
- Device Acceptance：**2/2 PASS**
- Stable Hotfix Promotion Gate：**24/24 PASS**
- Function-body drift：**0**
- `DB_VERSION = 2`
- `PUBLIC_HISTORY_CODE = PUBLIC`
- Supabase / IndexedDB / PUBLIC payload migration：**NONE**

# BowlMeet v0.4.6.2 — Stable / PUBLIC

正式認證來源：`v0.4.6.2-RC.1`。

- Full Automated Regression：**103/103 PASS**
- Preview Cloud Configuration Gate：**12/12 PASS**
- RC Device Smoke：**6/6 PASS**
- Stable Promotion & PUBLIC Release Gate：**PASS**
- APP_VERSION：`0.4.6.2`
- PWA Cache：`bowlmeet-v0.4.6.2-stable-*`
- 公開成績表：球員 / 1～6 / 總分 / 平均
- 取消公開後保留本機卡片，並可直接重新公開
- Republish 狀態使用 Public Control tombstone `removed`
- 排行榜／分享／獎項：**Public-only**
- iPhone 水平滑動＋sticky 球員欄：**PASS**
- PWA 關閉重開／Cache refresh：**PASS**
- `DB_VERSION = 2`
- `PUBLIC_HISTORY_CODE = PUBLIC`
- `PUBLIC_HISTORY_PIN = 042042`
- `LAYOUT_PREFS_KEY = bowlingMeetup.layoutPreferences.v1`
- Supabase migration：**NONE**
- IndexedDB migration：**NONE**
- PUBLIC payload migration／release-time rewrite：**NONE**
- Backup / Restore / Snapshot / Sync contracts：**UNCHANGED**

# BowlMeet v0.4.6.2-RC.1 — Full Regression & Release Candidate Gate

基線：`v0.4.6.2-dev.1-R2`。

- Full Automated Regression：**103/103 PASS**
- Preview Cloud Configuration Gate：**12/12 PASS**
- RC Device Smoke：**6/6 PASS**
- Release Candidate Validation Complete：**YES**
- R2 的 Republish Visibility 問題已修正：取消公開後自動切到「我的紀錄／已取消公開」，重新公開按鈕保持可見。
- Republish 狀態改由 Public Control tombstone `removed` 判斷。
- RC Preview Cloud Code 已由無效 7 碼 `V462RC1` 修正為合法 6 碼 `V46RC2`；PR #29 已發布。
- 排行榜／分享／獎項：**Public-only 實機 PASS**
- 每局成績表水平滑動＋sticky 球員欄：**PASS**
- PWA 關閉重開／最新 RC cache：**PASS**
- R2 → RC function delta：0 missing / 0 added / 0 body drift。
- DB_VERSION 2、PUBLIC code / payload、Backup / Restore、同步資料格式維持不變。
- Supabase / IndexedDB / PUBLIC payload migration：NONE。
- Stable Promotion：**尚未執行**。

# BowlMeet v0.4.6.2-dev.1-R2 — Post-R1 Cleanup & Cache Hardening

基線：`v0.4.6.2-dev.1-R1`（Device Manual 10/10 PASS）。

本版不新增資料功能，集中清理 R1 後續風險：
- 首次「公開」與「重新公開」確認文字、離線狀態、同步 reason、成功訊息正確分流
- R1 相容 Preview 修正舊 cache namespace 清理與 current-cache-only matching
- Production Service Worker 只管理 production cache，不再刪除或讀取 Preview cache
- 建立獨立 R2 Device Preview：`preview/v0.4.6.2-dev.1-R2/`
- R2 Preview 使用獨立 Cloud code `V462D12`、PIN `046212`、IndexedDB、Layout key 與 Cache namespace
- 修正 v0.4.6.2 PWA manifest 舊版 Stable／Layout Presets 描述
- 清理 deployment-test.html 的 dev.3／HF1／6-8 待重測殘留文字
- R1 Evidence 改為精確描述 production root 與 main Preview-only commits
- 舊 v0.4.6.1 PR #8 / #9 / #11 / #12 / #15 已依 stable/v0.4.6.1 完整取代關閉
- 新增可重跑 Gate：`node tools/v0.4.6.2-dev.1-r2-cleanup-gate.mjs`

R2 最終靜態／差異 Regression：**44/44 PASS**。
- `DB_VERSION = 2`
- `PUBLIC_HISTORY_CODE = PUBLIC`
- `DB_NAME = bowlingMeetup.local`
- 無 Supabase / IndexedDB / PUBLIC payload migration
- 正式 root `index.html` 僅 4 行預期的公開狀態文案／reason 變更
- `main` 相對 `stable/v0.4.6.1` 的差異仍全部位於 `preview/`
- Isolated R2 Preview 已由 Preview-only PR #25 / #26 發布（正式 root 未變）

> R2 尚未 Stable Promotion；目前只差 4 項實機 Device Acceptance。

# BowlMeet v0.4.6.2-dev.1 — Per-Game Public Score Table Foundation

基線：`stable/v0.4.6.1`。

本版只調整「成績紀錄／公開歷史」卡片的成績呈現，不修改資料結構或雲端契約。

- 表格欄位改為：**球員 / 1 / 2 / 3 / 4 / 5 / 6 / 總分 / 平均**
- 不足 6 局的欄位顯示 `—`
- 總分／平均沿用既有 `playerCalc()`
- 公開紀錄與本機紀錄共用相同歷史卡 renderer，視覺一致
- 手機版表格可左右滑動
- 手機版球員欄 sticky，滑動時保留玩家識別
- 不修改排行榜、分享、獎項、同步、Backup / Restore
- `DB_VERSION = 2`
- `PUBLIC_HISTORY_CODE = PUBLIC`
- 無 Supabase migration
- 無 IndexedDB migration
- 無 PUBLIC payload migration

# BowlMeet v0.4.6.1 — Stable / PUBLIC

正式基線：`v0.4.6.1-RC.1`，已完成 Full Automated **125/125 PASS**、RC Device Smoke **8/8 PASS**，且 dev.2-R1 Device Acceptance **12/12 PASS**。

本次 Stable Promotion 不新增功能，只將已驗證 RC 升為正式版本。

- APP_VERSION：`0.4.6.1`
- 顯示狀態：`Stable`
- PWA Cache：`bowlmeet-v0.4.6.1-stable-*`
- 版面設定：90 / 100 / 110 / 120%、密度、寬度、排行榜、計分區
- 快速版面：標準／緊湊／現場大字
- Mobile Optimization：Glass Dock 保持固定尺寸，≤420px 版面最佳化
- Layout Preferences 維持 `bowlingMeetup.layoutPreferences.v1`
- IndexedDB `DB_VERSION = 2`
- PUBLIC code 維持 `PUBLIC`
- 排行榜與分享維持 Public-only
- 無 Supabase migration
- 無 IndexedDB migration
- 無 PUBLIC payload migration／release-time rewrite

# BowlMeet v0.4.6.1-RC.1 — Full Regression & Release Candidate Gate

基線：`v0.4.6.1-dev.2`，其 R1 已完成 Automated **35/35 PASS** 與 Device **12/12 PASS**。

RC.1 不新增功能，僅進行候選版升版、PWA Cache 換版、完整跨模組回歸與 Release Gate。

- APP_VERSION：`0.4.6.1-RC.1`
- PWA Cache：`bowlmeet-v0.4.6.1-RC.1-*`
- 版面設定與 Preset 資料格式維持 `bowlingMeetup.layoutPreferences.v1`
- IndexedDB `DB_VERSION = 2`
- 正式 PUBLIC code 維持 `PUBLIC`
- 無 Supabase migration
- 無 IndexedDB migration
- 無 PUBLIC payload migration
- 計分、排行榜、分享、Player Hub、同步、Backup / Restore 契約不得變更

# BowlMeet v0.4.6.1-dev.2 — Layout Presets & Mobile Optimization

基線：`v0.4.6.1-dev.1-R2`（功能程式承接 dev.1/R1；R2 僅新增驗收 Evidence）。

本版新增三組一鍵快速版面，點選後會立即套用並儲存在既有 `bowlingMeetup.layoutPreferences.v1`；不新增資料 schema。

- **標準**：100%／標準密度／標準寬度／標準排行榜／標準計分區。
- **緊湊**：90%／緊湊密度／寬版／緊湊排行榜／標準計分區。
- **現場大字**：110%／寬鬆密度／標準寬度／標準排行榜／加大計分區。
- 快速預設與進階自訂可互相切換；符合預設組合時會自動標示目前預設。
- 手機維持固定 Glass Dock 不跟隨 90～120% 縮放。
- 420px 以下縮小 Dock 外框、按鈕與 More Sheet 佔用空間；版面自訂欄位改為單欄。
- 現場大字模式進一步提高球員名稱、格分、局總分與手機計分輸入可讀性。
- 保留 reduced-transparency fallback。

資料隔離：Session、Meetup、Roster、Personal、Backup、Supabase schema、PUBLIC payload、PUBLIC-only 排行榜／分享邏輯均不變。

# BowlMeet v0.4.6.1-dev.1 — Layout Settings Foundation

開發基線：`stable/v0.4.6`（Liquid Glass Stable）。

本版重新以 v0.4.6 主線實作「設定 → 版面設定」，不沿用 v0.4.5.3-dev.1 的舊基線程式碼。

- 介面大小：90% / 100% / 110% / 120%
- 內容密度：緊湊 / 標準 / 寬鬆
- 內容寬度：標準 / 寬版 / 滿版
- 排行榜顯示：標準 / 緊湊
- 計分區大小：標準 / 加大
- 即時預覽、套用設定、恢復 v0.4.6 預設版面
- 設定以 `bowlingMeetup.layoutPreferences.v1` 儲存在目前裝置
- Liquid Glass、Mobile Glass Dock、History / Player Hub / Share Glass 保持 v0.4.6 架構

資料隔離：不修改 Session、Meetup、Roster、Personal Data、Backup、Supabase schema、PUBLIC payload、PUBLIC revision 或 PUBLIC-only 排行榜／分享邏輯。

# BowlMeet v0.4.5.2 — Version Display Consistency Fix

`v0.4.5.2` 修正正式站頁首、設定與頁尾殘留的舊版標示。所有可見版本均由 `APP_VERSION` 統一產生，PWA 快取亦換版；`v0.4.5.1` 的公開成績限定維持不變。

## v0.4.5.1 — Public Results Only Hotfix

`v0.4.5.1` 將「排行榜」與「分享成績」鎖定為單一公開歷史資料源：只使用 `groupRemote` 中仍為 published 的 Session；本機未公開、等待同步與已取消公開的成績不列入排行榜，也不能產生分享卡。

- 排行榜的全部歷史、單一球聚、KPI 與排名均由公開 Session 計算。
- 分享卡的排行榜、完整成績、總覽與獎項均由公開 Session 計算。
- 球聚選單只顯示包含公開 Session 的球聚。
- 從現場、賽後摘要或本機歷史分享尚未公開的球聚時，會要求先完成公開同步。
- 不修改 Session / Backup / Roster / Personal Data 格式。
- 不修改 Supabase schema，不執行 migration，也不改寫既有 PUBLIC payload。

## v0.4.5 — Stable / PUBLIC

`v0.4.5` 已由 Freeze Certified `v0.4.5-RC.1` 正式升版，並通過 Stable Promotion & PUBLIC Release Gate。正式應用維持既有 `PUBLIC` Cloud、Storage 與資料格式；本次 promotion 不執行 Supabase migration，也不改寫既有 PUBLIC 資料。

## v0.4.5 Stable Release

- 認證來源：`v0.4.5-RC.1`，Automated 22/22、R2 Manual 10/10、RC Device 8/8，合計 40/40 PASS。
- 正式版本：`APP_VERSION = 0.4.5`。
- PWA Cache：`bowlmeet-v0.4.5-stable-*`。
- 正式 Cloud：沿用 `PUBLIC`；Preview `V45D41` 保持隔離與唯讀保存。
- Session / Backup / Roster / Personal Data / Public tombstone 格式不變。
- Supabase schema 與 production patch 維持 promotion 前 `main` 基線，未部署 migration。
- 發佈治理：經 `release/v0.4.5` PR 合併至 `main`，並建立 `stable/v0.4.5` recovery branch。

## Development history

BowlMeet 採 **Field-First**：打開 App 後直接進入「球聚現場」，建立玩家並進行標準 10 格即時計分。

## v0.4.5-dev.3 Player Hub & History

- 開發基線：`v0.4.5-dev.2`（Validation Complete）。
- 新增 runtime-only Unified Player Context；不寫入 Session / Backup / Roster metadata / Supabase schema。
- 「成績紀錄 → 球員」升級為 Player Hub，整合總局數、AVG、PB、最近 5 局、最近球聚。
- Player Hub 可進入既有 Analytics 或 Unified Player History；不建立第二套歷史或分析資料。
- Unified History 的球員名稱可直接進 Player Hub；返回會回原球員／原成績位置。
- Analytics 球員切換改由 Player Context 驅動，分析範圍保留 all / 5 / 10 / 20 / 50 / year。
- PUBLIC-only Player Hub / History / Analytics 維持唯讀；Roster 寫入亦加入 guard。
- Legacy `switchView('statsView')` 繼續相容。
- 正式 `main` 與正式 PUBLIC 不在本 branch 修改。

### v0.4.5-dev.3 Automated Gate

- JavaScript syntax ✅ PASS
- Static HTML duplicate ID ✅ 0
- Literal DOM reference missing ✅ 0
- Duplicate function declaration ✅ 0
- Unified Player Context fixture regression ✅ PASS
- LOCAL / PUBLIC / MIXED identity state ✅ PASS
- Analytics year / recent-N range regression ✅ PASS
- Player Hub → Analytics → 返回 Player Hub ✅ Contract PASS
- Player Hub → History → Session → 返回 ✅ Contract PASS
- PUBLIC-only Player Hub / Roster action guard ✅ PASS
- Legacy `switchView('statsView')` alias ✅ PASS
- Supabase schema SHA 與 dev.2 相同 ✅ `33689e39edcee5b25250a83ec472fa30dce379c9`
- Supabase Performance Advisor ✅ 0 findings
- Device Preview：`/preview/v0.4.5-dev.3/` ✅ Pages deployment success
- Preview Cloud：`V45D31`，由 dev.2 Preview `V45D23` 複製測試快照
- Preview IndexedDB：`bowlmeet.preview.v045d3.local` ✅ Isolated
- Preview Cache：`bowlmeet-preview-v045d3-` ✅ Isolated
- Preview localStorage：`bowlmeet.preview.v045d3.*` ✅ Isolated
- 真實快照回歸：千淯 8 / AVG 146.5 / PB 184；志強 8 / 122.0 / 166；軒豪 8 / 118.8 / 152；雅 3 / 163.7 / 188；毅雯 3 / 78.0 / 82
- 正式 `main` APP_VERSION ✅ `0.4.4-R1-HF1`
- 正式 PUBLIC ✅ revision 23 未變更
- 狀態：**Device Preview & Automated Live Regression PASS / Manual Device Acceptance Pending**



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

## v0.4.5-dev.2 Player Analytics Integration

- 開發基線：`v0.4.5-dev.1`（Validation Complete）。
- 移除頂層「個人分析」主選單。
- 球員分析正式整合到「成績紀錄 → 球員」流程。
- 操作路徑改為：球員總覽 → 分析 → 返回球員。
- 分析畫面沿用既有 KPI、PB、趨勢、近期狀態、逐格表現與個人歷史。
- 球員切換與分析範圍仍可在分析頁直接調整。
- 舊 `switchView('statsView')` 保留相容 alias，會導向「成績紀錄 → 球員分析」。
- 不建立第二套分析資料；沿用 dev.1 的 Unified History / Player Directory。
- 不修改 Session / Roster metadata / Backup / Supabase 正式資料模型。

### v0.4.5-dev.2 Automated Gate

- JavaScript syntax ✅ PASS
- Static HTML duplicate ID ✅ 0
- Literal DOM reference missing ✅ 0
- 頂層「個人分析」主選單移除 ✅ PASS
- 獨立 `statsView` 移除 ✅ PASS
- 球員分析內嵌 History ✅ PASS
- 球員總覽 → 分析 ✅ PASS
- 分析 → 返回球員 ✅ PASS
- 成績 / 球員模式切換不互相污染 ✅ PASS
- Legacy `statsView` route alias ✅ PASS
- Public-only 球員分析資料來源維持 Unified History ✅ PASS
- Device Preview：`/preview/v0.4.5-dev.2/` ✅ Ready
- Preview Cloud：`V45D23`，已複製目前 PUBLIC 歷史快照
- Preview localStorage / IndexedDB / Cache ✅ Isolated
- 真實快照球員分析：千淯 8 局 / AVG 146.5 / PB 184；志強 8 / 122.0 / 166；軒豪 8 / 118.8 / 152；雅 3 / 163.7 / 188；毅雯 3 / 78.0 / 82
- 球員總覽 → 分析 → 返回球員 ✅ Automated State Regression PASS
- 正式 `main` 仍為 `v0.4.4-R1-HF1` ✅ 未變更
- 正式 PUBLIC revision 23 ✅ 未由 dev.2 改寫
- 狀態：**Device Preview & Automated Live Regression PASS / Manual Device Acceptance Pending**

## v0.4.5-dev.1 Manual Device Acceptance

- 獨立「球員名冊」主選單已移除 ✅ PASS
- 成績紀錄內「成績 / 球員」切換 ✅ PASS
- 歷史球員不需同步即可自動出現 ✅ PASS
- PUBLIC-only 球員可直接顯示 ✅ PASS
- 球員局數 / AVG / PB 顯示正常 ✅ PASS
- 球員分析可直接開啟 ✅ PASS
- 新增暱稱 / 備註等 Metadata ✅ PASS
- Metadata 移除後歷史球員仍保留 ✅ PASS
- 關閉 / 重新開啟 Preview 後資料一致 ✅ PASS
- Preview / Stable / PUBLIC 資料隔離 ✅ PASS
- 結論：**v0.4.5-dev.1 Validation Complete**

## v0.4.5-dev.1 Unified History & Player Directory

- 開發基線：`stable/v0.4.4-R1-HF1`。
- 移除獨立「球員名冊」主選單。
- 「成績紀錄」新增二級頁籤：**成績 / 球員**。
- 球員頁直接由 Unified History（本機＋公開、Session ID 去重）與 Legacy 成績衍生，不需要手動同步。
- Roster 不再作為歷史球員來源，只保留暱稱、備註、常用等附加資料。
- 新成績、公開匯入與舊資料 migration 不再自動複製姓名到 Roster。
- 歷史球員沒有 Roster metadata 仍會出現在球員頁。
- 移除 Roster metadata 不會移除球員，也不會刪除歷史成績。
- 手動建立、尚無成績的常用球員仍會出現在球員頁。
- 球員總覽顯示局數、平均、PB、最近 5 局與資料狀態。
- Public-only 球員可以直接進個人分析；總分型統計與 PB 使用 Unified History。
- Strike / Spare / Open 逐格分析可讀取 Unified History 中有完整 bowlingFrames 的 Session。
- 舊 `switchView('rosterView')` 保留相容 alias，會導向「成績紀錄 → 球員」。
- 完整備份仍保存 Roster metadata；History / Session 資料模型不變。

### v0.4.5-dev.1 Automated Gate

- JavaScript syntax ✅ PASS
- Static HTML duplicate ID ✅ 0
- Literal DOM reference missing ✅ 0
- 獨立球員名冊主選單移除 ✅ PASS
- 成績 / 球員二級切換 ✅ PASS
- PUBLIC-only 歷史球員自動出現 ✅ PASS
- Local + Public + Legacy 球員整合 ✅ PASS
- 無正式分數的純歷史姓名不誤列 ✅ PASS
- Roster metadata 與歷史統計合併 ✅ PASS
- Metadata 移除後歷史球員仍存在 ✅ PASS
- Public-only 個人分析 ✅ PASS
- Public-only 連續 3 局 PB ✅ PASS
- 歷史姓名自動寫入 Roster 行為 ✅ 已移除
- Device Preview：`/preview/v0.4.5-dev.1/` ✅ Ready
- Preview Cloud：`V45D22`，已複製目前 PUBLIC 歷史快照
- Preview localStorage / IndexedDB / Cache ✅ Isolated
- 正式 `main` 維持 `v0.4.4-R1-HF1` ✅ 未變更
- 正式 PUBLIC revision 23 / 2 sessions / 2 meetups ✅ 未由 dev.1 改寫
- 真實 Preview Cloud `V45D22` 快照：5 位歷史球員 / 30 局正式分數 ✅
- 球員頁無需同步即可直接由 Unified History 產生 ✅ PASS
- 真實快照基準：千淯 8 局 / AVG 147 / PB 184；志強 8 / 122 / 166；軒豪 8 / 119 / 152；雅 3 / 164 / 188；毅雯 3 / 78 / 82
- Branch / Preview JavaScript syntax ✅ PASS
- Branch / Preview Duplicate ID ✅ 0
- Branch / Preview Missing DOM reference ✅ 0
- 正式 `main` 仍為 `v0.4.4-R1-HF1` ✅ 未變更
- 狀態：**Device Preview & Live Regression PASS / dev.1 Validation Complete**

## GitHub Pages 部署

1. Repository 使用 `main` 分支與 `/ (root)` 發佈。
2. 先開 `deployment-test.html`，確認 JavaScript、HTTPS / Secure Context、IndexedDB 與 Service Worker。
3. 再開 `index.html` 進行 BowlMeet 實機驗收。
4. iPhone Safari 可使用「分享 → 加入主畫面」安裝為 PWA。

## v0.4.4-R1 Regression & Data Safety

R1 不新增日常功能，目標是把 v0.4.4-dev.1 ～ dev.4 已實機通過的功能整合成 Release Candidate，並封住資料安全與跨版本還原邊界。

### R1 Data Safety Fix

- Full Backup 改由 `captureState()` 核心狀態輸出，除了成績、球聚、名冊、Personal Data、Public Control，也包含 active meetup、draft、settings、liveState。
- Replace Restore：新版完整備份可恢復 workspace。
- Merge / Add Restore：不覆蓋目前裝置 workspace。
- Legacy Backup：若舊備份不存在 `personalData`、`publicControl` 或 workspace 欄位，保留目前裝置的現代狀態，不再誤清資料。
- 舊備份缺少 `publicControl` 時，不會清除現有取消公開 tombstone。
- Snapshot / state restore 遇到空 draft 時會移除舊 draft，避免殘留。

### R1 Automated Gate

- JavaScript syntax ✅ PASS
- Static HTML duplicate ID ✅ 0
- Literal DOM reference missing ✅ 0
- v0.4.4-dev.1 Quick Session / Public Record Control markers ✅ PASS
- v0.4.4-dev.2 Post-Game Review markers ✅ PASS
- v0.4.4-dev.3 Personal Analytics markers ✅ PASS
- v0.4.4-dev.4 History Filter markers ✅ PASS
- Perfect Game 300 ✅ PASS
- 未完成第 10 格不寫正式分數 ✅ PASS
- Post-Game Review 正式局統計 ✅ PASS
- Frame Analytics / Legacy coverage ✅ PASS
- History 組合篩選 ✅ PASS
- PWA 更新順序：Snapshot → persist → SKIP_WAITING ✅ PASS
- Legacy Backup Replace 保留 Personal / tombstone / workspace ✅ PASS
- Modern Full Backup Replace 恢復完整 workspace ✅ PASS
- Modern Merge 保留目前 workspace ✅ PASS
- Supabase 核心 tables RLS ✅ Enabled
- Direct table ACL：anon / authenticated 無直接 table 權限 ✅
- RPC ACL：PUBLIC execute = false；anon / authenticated / service_role 明確授權 ✅
- Supabase Performance Advisor ✅ 0 findings
- 狀態：**v0.4.4-R1 Stable / Freeze Baseline**

### R1 Final Cloud Gate

- R1 Preview：`/preview/v0.4.4-R1/` ✅ Ready
- Preview localStorage / IndexedDB / Cache / Cloud ✅ Isolated
- Preview Cloud：`V44R22`，rollback 後 0 sessions / 0 meetups / 0 recordControls
- 取消公開 ✅ PASS
- Legacy repush 防復活 ✅ PASS
- 重新公開 ✅ PASS
- stale revision conflict ✅ PASS
- 錯誤 PIN rejection ✅ PASS
- PUBLIC 正式資料：revision 21 / 4 sessions / 4 meetups / v0.4.3.3-R1 ✅ 未變更
- RPC ACL：PUBLIC execute=false；anon / authenticated / service_role 明確授權 ✅
- Core tables：RLS enabled；anon / authenticated 無直接 table ACL ✅
- Performance Advisor ✅ 0 findings
- Security Advisor 的 SECURITY DEFINER 提示屬匿名 PWA RPC 架構預期警告；RPC 內仍以 PIN / revision 驗證存取。

### R1 Freeze Decision

- v0.4.4-dev.1 ～ dev.4 均已完成實機驗收。
- R1 僅做 Regression / Data Safety 修正，不新增一般功能。
- Full Backup / Legacy Restore 相容修正已通過自動回歸。
- PUBLIC tombstone 與 legacy repush 防復活已再次通過 transaction + ROLLBACK。
- 正式 main 根目錄仍維持 v0.4.3.3-R1；v0.4.4-R1 尚未合併至正式站。
- 最後 Gate：R1 Preview 實機驗收。

## v0.4.4-R1-HF1 Final Freeze & Stable Promotion

- Frame focus / horizontal scroll regression ✅ PASS
- Manual Device Acceptance ✅ PASS
- Scoring logic / Session schema / Supabase schema ✅ unchanged
- PUBLIC production payload ✅ unchanged
- Previous Stable preserved at `stable/v0.4.4-R1`
- Promotion target：`main`
- Freeze baseline：`v0.4.4-R1-HF1`
- 結論：**Hotfix Stable / Freeze Baseline**

## v0.4.4-R1-HF1 Manual Device Acceptance

- 第 1～10 格連續輸入 ✅ PASS
- 第 6～10 格水平捲動後輸入不回第 1 格 ✅ PASS
- 一般儲存不搶焦點 ✅ PASS
- Enter 前進下一個可輸入球 ✅ PASS
- Strike 後正確跳過停用第二球 ✅ PASS
- 第 10 格操作正常 ✅ PASS
- PWA Preview 重開後操作正常 ✅ PASS
- Stable / Preview / PUBLIC 隔離 ✅ PASS
- 結論：**v0.4.4-R1-HF1 Validation Complete / Hotfix Stable Candidate**

## v0.4.4-R1-HF1 Frame Input Focus & Scroll Hotfix

- Hotfix base：`stable/v0.4.4-R1`
- 修正現場 10 格記分每次儲存後 `.live-frame-scroll` 被重設到第 1 格。
- 儲存前記錄目前玩家、格、球與水平 scrollLeft。
- `renderLive()` 後恢復該玩家的水平位置。
- 一般 change 儲存只恢復畫面位置，不強制搶回焦點。
- Enter 儲存維持原本「前進到下一個可輸入球」行為。
- 使用 `focus({preventScroll:true})` 避免瀏覽器再次把水平捲動拉回。
- 不修改 Session / bowlingFrames / Supabase schema / PUBLIC payload。

### HF1 Automated Gate

- JavaScript syntax ✅ PASS
- Duplicate static ID ✅ 0
- Missing DOM reference ✅ 0
- 一般儲存後水平 scrollLeft 保留 ✅ PASS
- 一般儲存不強制搶焦點 ✅ PASS
- Enter 後前進下一個可輸入球 ✅ PASS
- Strike 後跳過 disabled 第二球 ✅ PASS
- Preview PWA cache isolation ✅ PASS
- Stable root 維持 v0.4.4-R1 ✅ 未變更
- 狀態：**v0.4.4-R1-HF1 Hotfix Stable / Freeze Baseline**

## v0.4.4-R1 Final Freeze & Stable Promotion

- Automated Regression ✅ PASS
- Cloud Gate ✅ PASS
- Manual Device Acceptance ✅ PASS
- Full Backup / Replace / Merge Restore ✅ PASS
- PWA Update Safety ✅ PASS
- PUBLIC tombstone / legacy repush protection ✅ PASS
- Supabase RLS / RPC ACL / Performance Gate ✅ PASS
- Previous Stable archived at `stable/v0.4.3.3-R1`
- Promotion target：`main`
- Freeze baseline：`v0.4.4-R1`
- 結論：**Stable / Freeze Baseline**

## v0.4.4-R1 Manual Device Acceptance

- 建立球聚 / 玩家 / 10 格正式計分 ✅ PASS
- 賽後摘要 ✅ PASS
- 個人分析 ✅ PASS
- History Filter ✅ PASS
- 取消公開 → 重開 App 狀態維持 ✅ PASS
- 重新公開 ✅ PASS
- 進行中 Draft / Live State ✅ PASS
- Full Backup ✅ PASS
- Replace Restore：成績 / bowlingFrames / publicControl / workspace ✅ PASS
- Merge Restore：目前 workspace 不被覆蓋 ✅ PASS
- PWA 關閉 / 重開後資料完整 ✅ PASS
- Preview / Stable / PUBLIC 資料隔離 ✅ PASS
- 結論：**v0.4.4-R1 Validation Complete / Stable Candidate**

## v0.4.4-dev.4 Manual Device Acceptance

- 日期起 / 迄篩選 ✅ PASS
- 玩家篩選 ✅ PASS
- 球館篩選 ✅ PASS
- 球道篩選 ✅ PASS
- 公開狀態篩選 ✅ PASS
- 全文搜尋 ✅ PASS
- 最新 / 最舊排序 ✅ PASS
- 來源 Tab + 精準條件組合 ✅ PASS
- 動態選單選值保留 ✅ PASS
- 篩選摘要 ✅ PASS
- 清除篩選 ✅ PASS
- 關閉 / 重新開啟後資料與篩選邏輯正常 ✅ PASS
- Stable / dev.1 / dev.2 / dev.3 / dev.4 Preview 隔離 ✅ PASS
- 正式 PUBLIC 未受影響 ✅ PASS
- 結論：**v0.4.4-dev.4 Validation Complete**

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
- 狀態：**Device Preview & Live Regression PASS / dev.4 Validation Complete**

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


## v0.4.5-dev.4 Player Experience & Session Navigation Polish

**Status: DEV4-06-R3 Final Regression Evidence & Release Gate — 20/20 Automated PASS + 10/10 Manual PASS / RC Candidate Ready**

### Scope
- DEV4-01 — Player Navigation State Polish ✅ Architecture / Integration Complete
- DEV4-02 — Player Hub Quick Actions & Compact UX ✅ Integration Complete
- DEV4-03 — Player History Session Navigation Polish ✅ Integration Complete
- DEV4-04 — Analytics Return / Player Switch Context Polish ✅ Integration Complete
- DEV4-05 — Mobile Interaction & Accessibility Polish ✅ Integration Complete
- DEV4-06 — PUBLIC Guard / Regression / RC Readiness ✅ Automated Gate Complete

### DEV4-01 Result
- Added one canonical Player navigation state for Players / Player Hub / Player History / Analytics / Session Detail / Unified Score History.
- Player Hub now remembers whether it was entered from the player list or a score-history session.
- Analytics and Player History return to the same Player Hub and preserve the Hub parent return target.
- Session Detail returns to the same Player History position without resetting player, search, range, or sort state.
- Player History scroll position is captured before Session Detail opens and restored after close.
- Missing origin session falls back safely to the player list.
- Navigation state remains UI/session-only; no Backup, Roster, IndexedDB schema, or Supabase schema changes.

### DEV4-02 Result
- Reduced Player Hub KPI cards from five to four core metrics: games, career average, PB, and recent-5 average.
- Moved latest meetup into one compact context strip instead of a full KPI card.
- Added direct “查看最近一場” quick action when a valid session exists.
- Direct latest-session detail returns to the same Player Hub instead of detouring through Player History.
- Consolidated primary actions to “分析” and “歷史紀錄”; player metadata editing is a compact secondary action.
- PUBLIC-only players still hide local player metadata editing while retaining read-only analytics/history/session viewing.
- Player Hub back label now reflects its real parent: 球員 or 成績紀錄.
- Mobile Hub uses a compact 2×2 KPI layout and sticky two-action bar with safe-area support.
- No Player / History / Analytics data duplication and no storage/schema format changes.

### DEV4-03 Result
- Player History and Session Detail now share one grouped-session sequence derived from the current player history filters.
- Added previous / next session navigation inside Session Detail without closing and reopening the history page.
- Session position shows the current place in the active sequence (for example 2 / 5 場).
- Session Detail now includes compact game count, session average, and session-high summary.
- Returning from Session Detail preserves player, search, range, sort, and original Player History scroll position.
- Direct “查看最近一場” from Player Hub uses the same Session Detail but returns directly to Player Hub.
- Session Detail close label reflects the actual parent: 返回歷史 or 返回 Player Hub.
- Dialog backdrop / Escape close use the same controlled return path; desktop Left / Right arrow keys switch sessions.
- Mobile Session Detail navigation is sticky with safe-area support.
- No new history/session data source, no Backup/IndexedDB/Supabase schema change.

### DEV4-04 Result
- Analytics now shows the active player and LOCAL / MIXED / PUBLIC source directly in the analysis header.
- Player switching stays inside Analytics, preserves the selected analytics range, and resets only the Analytics scroll position.
- Old-player presentation is hidden before a player/range context change and restored only after the new render completes, preventing stale metric flashes.
- Analytics back always returns to the same switched player's Player Hub; the Hub still retains its original parent return target.
- Added compact section navigation for Trend / PB / Recent / Frame / History to reduce long-page navigation cost.
- Mobile Analytics keeps player/range context and section navigation sticky while scrolling, with compact two-column controls.
- Analytics range remains independent from Player History range.
- PUBLIC-only analytics remains read-only and continues to show unavailable frame metrics as insufficient data rather than inferred zeroes.
- No analytics data store, Backup/IndexedDB format, Roster metadata, or Supabase schema change.

### DEV4-05 Result
- Player Hub / History / Analytics / Session Detail mobile controls now use a minimum 44px touch target for primary interactive buttons.
- Player History search/range/sort and Analytics player/range controls use 16px mobile input text to avoid unintended iOS form zoom.
- Added safe-area-aware top/bottom spacing for iPhone PWA use and corrected Analytics sticky offsets so controls do not sit underneath the app header.
- Session Detail is now a contained mobile scroll surface with sticky header/navigation, overscroll containment, and safe-area bottom padding.
- Added visible keyboard focus treatment across Player surfaces plus controlled focus transfer between Player Hub, History, Analytics, and Session Detail.
- Session Detail restores focus to its originating action when possible after close.
- Player History filter summary, Session position, and Analytics player context expose polite live-region updates; History filters now have accessible labels.
- Analytics section jumps move keyboard focus to the selected section and respect prefers-reduced-motion.
- Added reduced-motion handling for Player workflow transitions without changing data or navigation state.
- No Player / History / Analytics data source, Backup/IndexedDB format, Roster metadata, or Supabase schema change.

### DEV4-06 Result
- Re-ran root and isolated Preview JavaScript/static DOM regression: Syntax PASS, Duplicate ID 0, Missing DOM Ref 0.
- Confirmed PUBLIC-only Player Hub/Roster local-mutation controls remain hidden and action-layer guards reject PUBLIC-only roster edits.
- Session edit/delete still resolve only from the local session store; PUBLIC-only sessions remain view/import/public-control surfaces rather than local editable records.
- Unified History continues to deduplicate LOCAL + PUBLIC by Session ID before Player History / Analytics consumption.
- Legacy statsView compatibility remains active.
- Created isolated dev.4 Device Preview at `/preview/v0.4.5-dev.4/`.
- Preview isolation: Cloud `V45D41`, PIN `045023`, IndexedDB `bowlmeet.preview.v045d4.local`, localStorage prefix `bowlmeet.preview.v045d4.*`, Cache prefix `bowlmeet-preview-v045d4-`.
- Seeded V45D41 from validated dev.3 fixture: 2 sessions / 2 meetups / 2 record controls; appVersion is `0.4.5-dev.4`.
- Preview RPC pull succeeds with the Preview PIN and rejects an incorrect PIN.
- Formal PUBLIC remains revision 23 with 2 sessions / 2 meetups / 2 record controls and appVersion `0.4.4-R1`.
- Formal main remains `v0.4.4-R1-HF1`.
- Supabase schema/patch blobs are byte-identical to dev.3; no schema migration was introduced.
- Supabase Performance Advisor: 0 findings.
- Supabase Security Advisor reports the existing PIN-RPC architecture warnings (RLS tables intentionally have no direct policies; callable SECURITY DEFINER RPCs validate room/player/group PINs). These are baseline architecture findings, not a dev.4 schema change; no security schema change is included in this UX branch.
- RC promotion is blocked only on Manual Device Acceptance for the dev.4 Player workflow.

### Manual Device Acceptance — DEV4
1. 球員列表 → Player Hub → 返回：回原球員列表位置。
2. 成績紀錄 → 球員 → Player Hub → 返回：回原成績紀錄來源。
3. Hub → 分析 → 切換球員/範圍 → 返回：回切換後球員 Hub，無舊 KPI 閃現。
4. Hub → 歷史 → 查看本場 → 上一場/下一場 → 返回：搜尋、範圍、排序、捲動位置保留。
5. Hub → 查看最近一場 → 返回：直接回同一 Player Hub。
6. PUBLIC-only 球員：分析/歷史/單場可讀；本機球員資料編輯不可用。
7. iPhone 直向：按鈕易點、輸入不自動放大、sticky 區域不互相遮擋、Dialog 不超出安全區。
8. iPhone PWA：頂部/底部 safe area 正常，Session Dialog 可捲動且返回焦點正常。
9. PUBLIC Preview：取消公開/重新公開只影響 V45D41，不影響正式 PUBLIC。
10. 重新整理 Preview：正式 main / PUBLIC / 本機正式 Storage 均不被 Preview 污染。

### DEV4-06-R1 Result
- Manual DEV4 acceptance was reported OK, then a cross-module integration defect was found: 排行榜 / 獎項 / 分享成績 did not consistently follow the same active meetup context.
- Fixed the three modules to share the canonical current Meetup context instead of preserving unrelated selector state.
- Selecting a single meetup in 排行榜, 獎項, or 分享成績 now updates the current meetup and synchronizes the other two module selectors.
- Entering 排行榜 / 獎項 / 分享成績 from the current meetup now opens on that same meetup.
- 現場「分享成績」、球聚獎項「分享獎項卡」、Post-game Review「分享球聚卡」、History「分享」 now explicitly carry the source Meetup ID into Share.
- “全部歷史” remains available for Ranking / Share without clearing the current live meetup context.
- APP_VERSION advanced to `0.4.5-dev.4-R1`; no data schema or storage format change.
- Isolated Preview remains `V45D41` / PIN `045023`; Preview payload appVersion advanced to `0.4.5-dev.4-R1`.
- Formal PUBLIC remains revision 23 / appVersion `0.4.4-R1`; formal main root remains `v0.4.4-R1-HF1`.
- Static regression after the fix: JavaScript Syntax PASS, Duplicate ID 0, Missing DOM Ref 0.
- RC promotion remains blocked until the targeted cross-module retest passes.
- Automated targeted contract retest: PASS — canonical Meetup context, Ranking/Awards/Share selector synchronization, source Meetup carry-over, and `全部歷史` non-destructive behavior all verified; manual cross-module device retest remains.

### Targeted Retest — DEV4-06-R1
1. 現場球聚輸入並完成一局後，開啟排行榜：應自動顯示同一球聚與最新完成局分數。
2. 從排行榜切到獎項：應維持同一球聚，冠軍／平均王／單局王依同一批成績計算。
3. 從獎項按「分享獎項卡」：分享頁應維持同一球聚。
4. 從現場按「分享成績」：分享頁應直接選中目前球聚，而不是全部歷史或上一場球聚。
5. 在分享成績切換另一場單一球聚後，再開排行榜／獎項：兩者應跟著該球聚。
6. 排行榜或分享選「全部歷史」時，不應清除目前現場球聚；再按「目前球聚」應能立即回到目前場次。

### DEV4-06-R2｜Cross-Module Sync Regression & Context Safety
- Hardened the canonical Meetup context so only an existing Meetup ID can be persisted as `activeMeetupId`.
- Startup, restore, sync, or deletion paths now clear a stale / deleted active Meetup ID before cross-module rendering.
- Leaderboard and Share always fall back to a valid current Meetup or `全部歷史`; they no longer enter an empty selector state when a stale ID is encountered.
- Awards falls back to the valid current Meetup or the newest available Meetup.
- Selecting `全部歷史` in Leaderboard or Share remains display-only and does not clear the canonical current Meetup.
- APP_VERSION advanced to `0.4.5-dev.4-R2`; no Session / Backup / Roster metadata / Supabase schema change.
- Isolated Preview remains Cloud `V45D41`, IndexedDB `bowlmeet.preview.v045d4.local`, localStorage `bowlmeet.preview.v045d4.*`; PWA cache revision advanced to the R2 shell/runtime.
- Formal root `main`, Stable branch, and formal PUBLIC remain unchanged.
- Root / Preview JavaScript Syntax ✅ PASS
- Root / Preview Static Duplicate ID ✅ 0
- Root / Preview Literal DOM Reference Missing ✅ 0
- Root / Preview Duplicate Function Declaration ✅ 0
- Canonical Meetup validation / selector synchronization / stale Context cleanup contract ✅ PASS
- Manifest JSON / `git diff --check` ✅ PASS
- Supabase schema and patch files ✅ unchanged from dev.3

### Regression Matrix — DEV4-06-R2
1. 排行榜選單一球聚後，獎項與分享同步相同 Meetup ID。
2. 獎項選單一球聚後，排行榜與分享同步相同 Meetup ID。
3. 分享選單一球聚後，排行榜與獎項同步相同 Meetup ID。
4. 排行榜／分享選「全部歷史」後，`activeMeetupId` 與目前現場球聚保持不變。
5. 按「目前球聚」可從全部歷史立即返回 canonical Meetup。
6. 現場、獎項、Post-game Review、成績紀錄分享均攜帶來源 Meetup ID 與正確卡片類型。
7. 重新整理後，有效 `activeMeetupId` 可恢復並同步三個模組。
8. 無效／已刪除 `activeMeetupId` 會清除；排行榜與分享回到「全部歷史」，獎項回到有效球聚。
9. Root 與 isolated Preview：JavaScript Syntax、Duplicate ID、Missing DOM Ref、Context Contract 均須 PASS。
10. Preview Storage / Cloud / Cache 仍與正式 Stable / PUBLIC 隔離。

### DEV4-06-R3｜Final Regression Evidence & Release Gate
- Locked the tested artifact to remote Commit `6f8462d89545948bffd35b520d793858565efd72` (`v0.4.5-dev.4-R2`).
- User device acceptance completed on 2026-09-22: DEV4-06-R2 10-item regression matrix ✅ 10/10 PASS.
- Re-runnable automated gate: `node tools/dev4-06-r3-release-gate.mjs`.
- Automated Release Gate ✅ 20/20 PASS / 0 FAIL.
- Final evidence: `release-evidence/DEV4-06-R3_Final_Regression_Evidence.md` and `.json`.
- Release decision: `RC_CANDIDATE_READY`.
- No application code, APP_VERSION, Session / Backup / Roster metadata, Supabase schema, Stable branch, `main`, or formal PUBLIC change is included in R3.
- Next governed stage: `v0.4.5-RC.1｜Release Candidate Integration & Freeze Gate`; no additional dev.4 feature scope.

## v0.4.5-RC.1｜Release Candidate Integration & Freeze Gate

**Status: FREEZE CERTIFIED — Automated 22/22 PASS + Inherited Manual 10/10 PASS + RC Device 8/8 PASS**

- Promoted only the R3-approved artifact into the dedicated `v0.4.5-RC.1` branch.
- APP_VERSION, titles, manifests, deployment checks, and PWA cache names advanced to `0.4.5-RC.1`.
- Created isolated RC Preview at `/preview/v0.4.5-RC.1/`.
- RC Preview local isolation: IndexedDB `bowlmeet.preview.v045rc1.local`, localStorage `bowlmeet.preview.v045rc1.*`, cache `bowlmeet-preview-v045rc1-*`.
- RC Preview retains the validated Cloud test environment `V45D41`; no Supabase schema or patch change.
- Executable application logic is byte-equivalent to the accepted R2 logic after version and isolation constants are normalized.
- Automated Freeze Gate: 22 PASS / 0 FAIL.
- R2 manual device acceptance remains inherited as 10 PASS / 0 FAIL.
- RC-specific device smoke acceptance completed on 2026-09-22: 8 PASS / 0 FAIL.
- Freeze decision: `FREEZE_CERTIFIED`; P0 / P1 / P2 blockers = 0.
- This RC.1 branch is now frozen. Future changes require a new version or an explicitly scoped hotfix branch.
- `main`, Stable branches, and formal PUBLIC remain unchanged.
- Re-runnable gate: `node tools/v0.4.5-rc1-freeze-gate.mjs`.
- RC application candidate Commit: `0faf86a59e206b4f6fbfecdca666bb12248c58cd`.
- Freeze evidence: `release-evidence/v0.4.5-RC.1_Integration_Freeze_Gate.md` and `.json`.

### Guardrails
- Keep Unified History as the single score/history source.
- Do not add a second Player / History / Analytics data store.
- No Supabase schema change.
- No Session / Backup / Roster metadata format change unless explicitly required.
- PUBLIC-only players remain read-only.
- Formal root main and formal PUBLIC are not modified by this development branch.
- Preserve legacy statsView compatibility until RC regression is complete.
