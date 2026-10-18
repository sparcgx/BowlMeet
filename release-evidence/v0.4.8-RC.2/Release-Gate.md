# v0.4.8-RC.2 — 完整回歸與發布候選凍結

整合基線：v0.4.8-dev.3 / 7b11081c0b1edfd972f8008f70b570b694b2f567。
使用者於 2026-10-18 14:27:17 Asia/Taipei 回覆「測試ok」，記為 PASS_USER_REPORTED；未另提供裝置或逐項操作證據。

## 範圍

- dev.1 球道分組／現場順序管理
- dev.2 球聚賽制／個人與團體系列賽排名／公開系列賽分享
- dev.3 玩家進步摘要／10 格唯讀明細與第 10 格加投
- RC.2 僅調整執行版本識別與文字，合入 main 既有 Preview。等價檢查驗證資產與 SQL 原封不動。

## 測試與限制

完整結果見同目錄 Gate.json 及各 suite JSON。原生儲存使用 localhost 合成資料；Chromium／Playwright WebKit 不代表真實 iPhone Safari、安裝式 PWA 或正式 Supabase。Service Worker gate 為模擬邏輯與 shell 靜態檢查，不宣稱真實裝置更新驗收。

## RC.2 實機驗收（PENDING）

1. iPhone Safari 開啟 RC.2 Preview，確認版本與畫面。
2. 建立測試球聚，調整球道分組／順序，設定系列賽局數。
3. 完成一局測試分數，檢查系列賽結果、玩家摘要，點擊單局分數核對 10 格與第 10 格加投。
4. Reload 確認成績及設定仍在；加入主畫面後關閉 PWA 再開確認。
5. 僅在隔離 Preview 使用測試資料；不清除網站資料、不填滿儲存空間、不碰正式 PUBLIC。

正式 Stable promotion 維持 BLOCKED，需另完成 RC 實機驗收與正式發布程序。既有 freeze/v0.4.8-RC.1、stable/v0.4.7.4 與 freeze/v0.4.7.4 不修改。freeze/v0.4.8-RC.2 將指向完整回歸通過且附證據的候選提交。
