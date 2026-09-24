import fs from 'node:fs';

const read = p => fs.readFileSync(p, 'utf8');
const root = read('index.html');
const preview = read('preview/v0.4.6.2-dev.1-R2/index.html');
const sw = read('sw.js');
const previewSw = read('preview/v0.4.6.2-dev.1-R2/sw.js');
const manifest = read('manifest.webmanifest');
const deploy = read('deployment-test.html');
const previewDeploy = read('preview/v0.4.6.2-dev.1-R2/deployment-test.html');

const checks = [];
const check = (name, ok) => checks.push({ name, ok: Boolean(ok) });

function htmlAudit(source){
  const html = source.split('<script>')[0];
  const ids = [...html.matchAll(/\bid=["']([^"']+)["']/g)].map(m => m[1]);
  const counts = new Map();
  for (const id of ids) counts.set(id, (counts.get(id) || 0) + 1);
  const refs = [...source.matchAll(/\$\(['"]([^'"]+)['"]\)/g)].map(m => m[1]);
  return {
    duplicateIds: [...counts.entries()].filter(([, n]) => n > 1),
    missingDollarRefs: [...new Set(refs.filter(id => !counts.has(id)))]
  };
}

const rootHtml = htmlAudit(root);
const previewHtml = htmlAudit(preview);

check('APP_VERSION unchanged', root.includes("const APP_VERSION='0.4.6.2-dev.1'"));
check('DB_VERSION remains 2', root.includes('const DB_VERSION=2'));
check('DB_NAME unchanged', root.includes("const DB_NAME='bowlingMeetup.local'"));
check('PUBLIC code unchanged', root.includes("const PUBLIC_HISTORY_CODE='PUBLIC'"));
check('PUBLIC PIN unchanged', root.includes("const PUBLIC_HISTORY_PIN='042042'"));
check('layout key unchanged', root.includes("const LAYOUT_PREFS_KEY='bowlingMeetup.layoutPreferences.v1'"));

check('first publish confirm copy', root.includes("published?'確定重新公開這張本機成績？':'確定公開這張本機成績？'"));
check('first publish offline copy', root.includes("published?'離線 · 重新公開等待同步':'離線 · 公開等待同步'"));
check('first publish sync reason', root.includes("published?'public-republish':'public-publish'"));
check('first publish success copy', root.includes("published?'已重新公開。':'已公開。'"));

check('preview publish confirm copy', preview.includes("published?'確定重新公開這張本機成績？':'確定公開這張本機成績？'"));
check('preview publish offline copy', preview.includes("published?'離線 · 重新公開等待同步':'離線 · 公開等待同步'"));
check('preview publish sync reason', preview.includes("published?'public-republish':'public-publish'"));
check('preview publish success copy', preview.includes("published?'已重新公開。':'已公開。'"));

check('preview APP_VERSION R2', preview.includes("const APP_VERSION='0.4.6.2-dev.1-R2'"));
check('preview cloud isolated', preview.includes("const PUBLIC_HISTORY_CODE='V462D12'"));
check('preview PIN isolated', preview.includes("const PUBLIC_HISTORY_PIN='046212'"));
check('preview DB isolated', preview.includes("const DB_NAME='bowlmeet.preview.v0462d1r2.local'"));
check('preview layout isolated', preview.includes("const LAYOUT_PREFS_KEY='bowlmeet.preview.v0462d1r2.layoutPreferences.v1'"));
check('preview old R1 storage namespace absent', !preview.includes('v0462d1r1'));

check('production SW namespace scoped', sw.includes("const PRODUCTION_CACHE_ROOT='bowlmeet-v'"));
check('production SW scoped delete', sw.includes('k.startsWith(PRODUCTION_CACHE_ROOT)'));
check('production SW current-only matcher', sw.includes('async function matchProductionCache'));
check('production SW no global caches.match', !/\bcaches\.match\(/.test(sw));

check('preview SW cache root', previewSw.includes("const PREVIEW_CACHE_ROOT='bowlmeet-preview-v0462d1r2-'"));
check('preview SW R2 namespace', previewSw.includes("const PREVIEW_CACHE_PREFIX=PREVIEW_CACHE_ROOT+'r2-'"));
check('preview SW old namespace cleanup', previewSw.includes('k.startsWith(PREVIEW_CACHE_ROOT)'));
check('preview SW current-only matcher', previewSw.includes('async function matchPreviewCache'));
check('preview SW no global caches.match', !/\bcaches\.match\(/.test(previewSw));
check('preview SW R1 namespace absent', !previewSw.includes('v0462d1r1'));

check('manifest per-game description', manifest.includes('公開成績每局 1～6 分數展開表'));
check('manifest no false Stable wording', !manifest.includes('Stable：版面預設'));
check('deployment copy current', deploy.includes('R2 驗收重點'));
check('deployment no dev.3 stale copy', !deploy.includes('dev.3 驗收重點'));
check('deployment no HF1 stale acceptance', !deploy.includes('HF1 實機測試'));

check('preview deployment cache hardening', previewDeploy.includes('R2 Cache Hardening'));
check('preview deployment no old retest instruction', !previewDeploy.includes('請重新整理後重測 6／7／8'));
check('preview deployment records R1 10/10', previewDeploy.includes('R1 已完成 10/10 PASS'));

check('root duplicate static IDs = 0', rootHtml.duplicateIds.length === 0);
check('root missing literal DOM refs = 0', rootHtml.missingDollarRefs.length === 0);
check('preview duplicate static IDs = 0', previewHtml.duplicateIds.length === 0);
check('preview missing literal DOM refs = 0', previewHtml.missingDollarRefs.length === 0);

const pass = checks.filter(x => x.ok).length;
const fail = checks.length - pass;
for (const x of checks) console.log(`${x.ok ? 'PASS' : 'FAIL'} ${x.name}`);
console.log(`\nR2 cleanup gate: ${pass} PASS / ${fail} FAIL`);
if (fail) process.exit(1);
