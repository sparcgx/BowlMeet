import fs from 'node:fs';

const read = p => fs.readFileSync(p, 'utf8');
const root = read('index.html');
const preview = read('preview/v0.4.6.2-dev.1-R2/index.html');
const sw = read('sw.js');
const previewSw = read('preview/v0.4.6.2-dev.1-R2/sw.js');
const manifestText = read('manifest.webmanifest');
const deploy = read('deployment-test.html');
const previewDeploy = read('preview/v0.4.6.2-dev.1-R2/deployment-test.html');

const checks = [];
const check = (name, ok) => checks.push({ name, ok: Boolean(ok) });

check('01 APP_VERSION unchanged', root.includes("const APP_VERSION='0.4.6.2-dev.1'"));
check('02 DB_VERSION remains 2', root.includes('const DB_VERSION=2'));
check('03 DB_NAME unchanged', root.includes("const DB_NAME='bowlingMeetup.local'"));
check('04 PUBLIC code unchanged', root.includes("const PUBLIC_HISTORY_CODE='PUBLIC'"));
check('05 PUBLIC PIN unchanged', root.includes("const PUBLIC_HISTORY_PIN='042042'"));
check('06 layout key unchanged', root.includes("const LAYOUT_PREFS_KEY='bowlingMeetup.layoutPreferences.v1'"));
check('07 first publish confirm copy', root.includes("published?'確定重新公開這張本機成績？':'確定公開這張本機成績？'"));
check('08 first publish offline copy', root.includes("published?'離線 · 重新公開等待同步':'離線 · 公開等待同步'"));
check('09 first publish sync reason', root.includes("published?'public-republish':'public-publish'"));
check('10 first publish success copy', root.includes("published?'已重新公開。':'已公開。'"));

check('11 preview APP_VERSION R2', preview.includes("const APP_VERSION='0.4.6.2-dev.1-R2'"));
check('12 preview publish confirm copy', preview.includes("published?'確定重新公開這張本機成績？':'確定公開這張本機成績？'"));
check('13 preview publish success copy', preview.includes("published?'已重新公開。':'已公開。'"));
check('14 preview cloud isolated', preview.includes("const PUBLIC_HISTORY_CODE='V462D12'"));
check('15 preview PIN isolated', preview.includes("const PUBLIC_HISTORY_PIN='046212'"));
check('16 preview DB isolated', preview.includes("const DB_NAME='bowlmeet.preview.v0462d1r2.local'"));
check('17 preview layout isolated', preview.includes("const LAYOUT_PREFS_KEY='bowlmeet.preview.v0462d1r2.layoutPreferences.v1'"));
check('18 preview sync reason isolated', preview.includes("published?'public-republish':'public-publish'"));

check('19 production SW namespace scoped', sw.includes("const PRODUCTION_CACHE_ROOT='bowlmeet-v'"));
check('20 production SW current-only matcher', sw.includes('async function matchProductionCache'));
check('21 production SW no global caches.match', !/\bcaches\.match\(/.test(sw));
check('22 production SW scoped cleanup', sw.includes('k.startsWith(PRODUCTION_CACHE_ROOT)'));
check('23 production SW current shell', sw.includes("bowlmeet-v0.4.6.2-dev.1-pergame-shell"));
check('24 production SW leaves preview namespace unmanaged', !sw.includes('bowlmeet-preview-'));

check('25 preview SW cache root R2', previewSw.includes("const PREVIEW_CACHE_ROOT='bowlmeet-preview-v0462d1r2-'"));
check('26 preview SW R2 namespace', previewSw.includes("const PREVIEW_CACHE_PREFIX=PREVIEW_CACHE_ROOT+'r2-'"));
check('27 preview SW old namespace cleanup', previewSw.includes('k.startsWith(PREVIEW_CACHE_ROOT)'));
check('28 preview SW current-only matcher', previewSw.includes('async function matchPreviewCache'));
check('29 preview SW no global caches.match', !/\bcaches\.match\(/.test(previewSw));
check('30 preview SW isolated shell path', previewSw.includes("./assets/liquid-glass-dev4.css"));

let manifest = null;
try { manifest = JSON.parse(manifestText); } catch {}
check('31 manifest valid JSON', Boolean(manifest));
check('32 manifest version current', manifest?.name?.includes('v0.4.6.2-dev.1'));
check('33 manifest per-game description', manifest?.description?.includes('公開成績每局 1～6 分數展開表'));
check('34 manifest no false Stable wording', !manifestText.includes('Stable：版面預設'));

check('35 deployment copy current', deploy.includes('R2 驗收重點'));
check('36 deployment no dev.3 stale copy', !deploy.includes('dev.3 驗收重點'));
check('37 deployment no HF1 stale copy', !deploy.includes('HF1 實機測試'));
check('38 deployment no old 6/7/8 retest instruction', !deploy.includes('請重新整理後重測 6／7／8'));
check('39 preview deployment cache hardening', previewDeploy.includes('R2 Cache Hardening'));
check('40 preview deployment records R1 10/10', previewDeploy.includes('R1 已完成 10/10 PASS'));

const pass = checks.filter(x => x.ok).length;
const fail = checks.length - pass;
for (const x of checks) console.log(`${x.ok ? 'PASS' : 'FAIL'} ${x.name}`);
console.log(`\nR2 cleanup gate: ${pass} PASS / ${fail} FAIL`);
if (fail) process.exit(1);
