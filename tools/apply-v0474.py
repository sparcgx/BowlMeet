"""Apply the exact audited index patch. Never run against a frozen or production branch."""
from pathlib import Path
import hashlib,json,subprocess
META = {'base_commit': '1d7ea21ea2654e989545974dcd3987281710c6fc', 'base_index_sha256': '97ce352f3a3d883562152d6aa444c8bfde9bf5325bc536ead0fd25afc59db7c1', 'result_index_sha256': '9b4ed29c8ea232c6ffd09331f953dd5ecc09736ed31402f7c236128e5d0e235a', 'version': '0.4.7.4-dev.1', 'channel': 'development', 'native_device_gate': 'PENDING'}
EDITS = [[5, 6, '<title>保齡球球聚｜BowlMeet v0.4.7.4-dev.1</title>\n'], [12, 14, '<link rel="manifest" href="./manifest.webmanifest?v=0474d1" />\n<link rel="apple-touch-icon" href="./icons/icon-192.png?v=0474d1" />\n'], [1138, 1139, '<link rel="stylesheet" href="./assets/liquid-glass-dev4.css?v=0474d1" />\n'], [1564, 1572, '<link rel="stylesheet" href="./assets/theme-center-v0470.css?v=0474d1" />\n<link rel="stylesheet" href="./assets/theme-center-v0470-mobile.css?v=0474d1" />\n<link rel="stylesheet" href="./assets/theme-center-v0470-accessibility.css?v=0474d1" />\n<link rel="stylesheet" href="./assets/liquid-motion-v0470.css?v=0474d1" />\n<link rel="stylesheet" href="./assets/score-card-v0471.css?v=0474d1" />\n<link rel="stylesheet" href="./assets/score-card-mobile-v0471.css?v=0474d1" />\n<link rel="stylesheet" href="./assets/score-card-accessibility-v0471.css?v=0474d1" />\n<link rel="stylesheet" href="./assets/rc-mobile-repair-v0471.css?v=0474d1" />\n<link rel="stylesheet" href="./assets/ui-hardening-v0474.css?v=0474d1" />\n<script defer src="./assets/ui-lifecycle-v0474.js?v=0474d1"></script>\n'], [1577, 1578, '  <div class="brand"><img class="brand-icon" src="./icons/icon-192.png?v=0474d1" alt="" width="42" height="42" /><div><h1>保齡球球聚｜BowlMeet</h1><p>BowlMeet <span data-app-version></span> · Performance & UI Hardening · 開發測試</p></div></div>\n'], [2524, 2525, '  <div class="footer-note">保齡球球聚｜BowlMeet · <span data-app-version></span> · 開發測試</div>\n'], [2548, 2549, "const APP_VERSION='0.4.7.4-dev.1';\n"], [3163, 3163, "  const invalid=[...$('scoreBody').querySelectorAll('.score-in')].find(input=>\n    input.validity.badInput||(!input.checkValidity())||(input.value!==''&&normalizeScore(input.value)===null));\n  if(invalid){invalid.focus();return {ok:false,msg:'分數需為 0～300 的整數；請修正標示欄位後再儲存。'};}\n"], [4743, 4744, "function renderAll(){\n  validateCurrentMeetupContext();renderKpis();renderMeetups();\n  // Hidden history/analytics are rendered on entry, not on every live update.\n  // Preserve renderRoster's separate roster-picker side effect for setup forms.\n  if(document.getElementById('historyView')?.classList.contains('active')){\n    renderHistory();renderRoster();renderHistoryMode();\n  }else{\n    renderMeetupRosterPicker($('meetupEditId').value?(meetups.find(m=>m.id===$('meetupEditId').value)?.participantIds||[]):[]);\n  }\n  renderLeaderboard();renderAwards();renderRosterQuickSelect();renderQuickPlayerSuggestions();\n  refreshSheetCalcs();renderShareOptions();renderSafety();renderSync();renderFieldSettings();renderPersonal();\n  if(document.getElementById('meetupView')?.classList.contains('active'))renderLive();\n}\n"], [4786, 4787, "  if(viewId==='historyView'){renderHistory();renderRoster();renderHistoryMode()}\n"]]
if Path('.git').exists():
    branch=subprocess.check_output(['git','branch','--show-current'],text=True).strip()
    if branch!='v0.4.7.4-dev.1':
        raise SystemExit('Refusing to patch any branch other than v0.4.7.4-dev.1')
p=Path('index.html');data=p.read_bytes();actual=hashlib.sha256(data).hexdigest()
if actual!=META['result_index_sha256']:
    if actual!=META['base_index_sha256']:
        raise SystemExit('Input index changed; re-audit required, no write performed')
    lines=data.decode('utf-8').splitlines(keepends=True)
    for start,end,text in reversed(EDITS): lines[start:end]=[text]
    output=''.join(lines).encode('utf-8')
    if hashlib.sha256(output).hexdigest()!=META['result_index_sha256']:
        raise SystemExit('Output integrity check failed')
    p.write_bytes(output)
Path('release-identity.json').write_text(json.dumps(META,indent=2)+'\n')
readme=Path('README.md');r=readme.read_text()
heading='# BowlMeet v0.4.7.4-dev.1 — Performance & UI Hardening (DRAFT)'
if not r.startswith(heading):
    readme.write_text(heading+'\n\n正式基線仍為 v0.4.7.3；本分支未 Promotion。修正快取身份、手動分數驗證、隱藏頁面渲染及導覽介面。\n\n驗證分成 Source/Node 模擬、離線 Chromium DOM，以及待驗收的 iOS/PWA/IndexedDB/雲端。數據詳見 release-evidence/v0.4.7.4-dev.1_Audit.md。\n\n以下為歷史版本紀錄，不代表本分支目前版本。\n\n'+r)
print('Applied/verified',META['version'],META['result_index_sha256'])
