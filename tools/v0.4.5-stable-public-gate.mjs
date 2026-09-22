import fs from 'node:fs';
import crypto from 'node:crypto';
import { execFileSync } from 'node:child_process';

const certifiedRcCommit = '03e7da4d4d77e283e4f3b8544e36ebc71af4204f';
const frozenCandidateCommit = '0faf86a59e206b4f6fbfecdca666bb12248c58cd';
const expectedVersion = '0.4.5';
const files = {
  root: 'index.html',
  frozenPreview: 'preview/v0.4.5-RC.1/index.html',
  rootManifest: 'manifest.webmanifest',
  frozenPreviewManifest: 'preview/v0.4.5-RC.1/manifest.webmanifest',
  rootSw: 'sw.js',
  frozenPreviewSw: 'preview/v0.4.5-RC.1/sw.js',
};
const frozenHashes = {
  'preview/v0.4.5-RC.1/index.html': 'a9958e336869771daddf5e0924efd8f241ceb5ea5e017c4ff09a9d22067063f2',
  'preview/v0.4.5-RC.1/manifest.webmanifest': '49bb8b007c952c0abdb108ed5ad77e79209434aa96ebb2f877c72c21e2b2e8ba',
  'preview/v0.4.5-RC.1/sw.js': 'f3184795cd32bb38759129a0a128a0ca2ac070d81401b77a3c955e738f05fe9e',
};
const productionSqlBlobs = {
  'supabase_schema.sql': '9d211151b01f8dd0e1a597829e77805ca0e60786',
  'supabase_v044_public_record_control_patch.sql': '712b29e3c4ad910187b634427b031224f4b8f70b',
};

const read = file => fs.readFileSync(file, 'utf8');
const sha256 = file => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex');
const gitBlob = file => execFileSync('git', ['hash-object', file], { encoding: 'utf8' }).trim();
const results = [];
const check = (id, name, pass, detail) => results.push({ id, name, status: pass ? 'PASS' : 'FAIL', detail });

function inlineScripts(html) {
  return [...html.matchAll(/<script(?:\s[^>]*)?>([\s\S]*?)<\/script>/gi)].map(match => match[1]);
}
function staticHtml(html) { return html.replace(/<script(?:\s[^>]*)?>[\s\S]*?<\/script>/gi, ''); }
function duplicateStaticIds(html) {
  const ids = [...staticHtml(html).matchAll(/\bid=["']([A-Za-z][A-Za-z0-9_:\-.]*)["']/g)].map(match => match[1]);
  return [...new Set(ids.filter((id, index) => ids.indexOf(id) !== index))];
}
function missingLiteralDomRefs(html) {
  const ids = new Set([...staticHtml(html).matchAll(/\bid=["']([A-Za-z][A-Za-z0-9_:\-.]*)["']/g)].map(match => match[1]));
  const refs = [...html.matchAll(/\$\(['"]([^'"$<>]+)['"]\)/g)].map(match => match[1]);
  return [...new Set(refs.filter(ref => !ids.has(ref)))];
}
function duplicateFunctions(html) {
  const names = [...inlineScripts(html).join('\n').matchAll(/(?:^|\n)function\s+([A-Za-z_$][\w$]*)\s*\(/g)].map(match => match[1]);
  return [...new Set(names.filter((name, index) => names.indexOf(name) !== index))];
}

const root = read(files.root);
const frozenPreview = read(files.frozenPreview);
for (const [label, html] of [['Root', root], ['Frozen RC Preview', frozenPreview]]) {
  let syntaxPass = true;
  let syntaxDetail = 'Inline JavaScript parsed successfully';
  try { for (const script of inlineScripts(html)) new Function(script); }
  catch (error) { syntaxPass = false; syntaxDetail = String(error?.message || error); }
  check(`${label.toLowerCase().replaceAll(' ', '-')}-js-syntax`, `${label} JavaScript syntax`, syntaxPass, syntaxDetail);
  const duplicateIds = duplicateStaticIds(html);
  check(`${label.toLowerCase().replaceAll(' ', '-')}-duplicate-id`, `${label} static duplicate IDs`, duplicateIds.length === 0, duplicateIds.length ? duplicateIds.join(', ') : '0 duplicates');
  const missingRefs = missingLiteralDomRefs(html);
  check(`${label.toLowerCase().replaceAll(' ', '-')}-dom-ref`, `${label} literal DOM references`, missingRefs.length === 0, missingRefs.length ? missingRefs.join(', ') : '0 missing references');
  const duplicateFns = duplicateFunctions(html);
  check(`${label.toLowerCase().replaceAll(' ', '-')}-duplicate-function`, `${label} duplicate function declarations`, duplicateFns.length === 0, duplicateFns.length ? duplicateFns.join(', ') : '0 duplicates');
}

for (const [label, file] of [['Root service worker', files.rootSw], ['Frozen RC service worker', files.frozenPreviewSw]]) {
  let pass = true; let detail = 'JavaScript parsed successfully';
  try { new Function(read(file)); } catch (error) { pass = false; detail = String(error?.message || error); }
  check(label.toLowerCase().replaceAll(' ', '-'), `${label} syntax`, pass, detail);
}
for (const [label, file] of [['Root manifest', files.rootManifest], ['Frozen RC manifest', files.frozenPreviewManifest]]) {
  let pass = true; let detail = 'Valid JSON';
  try { JSON.parse(read(file)); } catch (error) { pass = false; detail = String(error?.message || error); }
  check(label.toLowerCase().replaceAll(' ', '-'), `${label} JSON`, pass, detail);
}

check('stable-version', 'Stable APP_VERSION', root.includes(`const APP_VERSION='${expectedVersion}'`), expectedVersion);
check('stable-title', 'Stable visible version', root.includes('BowlMeet v0.4.5</title>') && !root.includes('0.4.5-RC.1'), 'Root labels normalized to v0.4.5');
check('production-cloud', 'Formal PUBLIC cloud namespace', root.includes("const PUBLIC_HISTORY_CODE='PUBLIC'"), 'PUBLIC');
const productionStorage = [
  "const DB_NAME='bowlingMeetup.local'",
  "const V2KEY='bowlingScoreWorkstation.sessions.v2'",
  "const ACTIVEKEY='bowlingMeetup.activeEvent.v3'",
];
check('production-storage', 'Formal production storage namespace', productionStorage.every(token => root.includes(token)), 'Existing production IndexedDB and localStorage namespaces preserved');
check('stable-cache', 'Stable PWA cache namespace', read(files.rootSw).includes("const CACHE='bowlmeet-v0.4.5-stable-shell'") && read(files.rootSw).includes("const RUNTIME='bowlmeet-v0.4.5-stable-runtime'"), 'Dedicated stable shell and runtime caches');

const logicStart = 'function safeJsonParse';
const stableLogic = inlineScripts(root).join('\n').slice(inlineScripts(root).join('\n').indexOf(logicStart));
const frozenLogic = inlineScripts(frozenPreview).join('\n').slice(inlineScripts(frozenPreview).join('\n').indexOf(logicStart));
check('certified-logic-parity', 'Stable logic parity with frozen RC', stableLogic === frozenLogic, 'Executable application logic unchanged after version and namespace constants');

for (const [file, expected] of Object.entries(frozenHashes)) {
  check(`frozen-${file.split('/').pop()}`, `Frozen RC artifact ${file}`, sha256(file) === expected, expected);
}
for (const [file, expected] of Object.entries(productionSqlBlobs)) {
  check(`production-${file}`, `Production SQL baseline ${file}`, gitBlob(file) === expected, `Git blob ${expected}`);
}

const publicContracts = [
  "row.source==='PUBLIC'",
  "if(row&&row.source!=='PUBLIC')editRoster",
  "alert('這位球員目前只有公開歷史，Player Hub 為唯讀。若要本機管理，請先匯入相關本機紀錄。')",
  "function buildGroupPayload(remotePayload=groupRemote)",
  "function normalizePublicRecordControls(raw=[])",
];
check('public-guard-contracts', 'PUBLIC read-only and tombstone contracts', publicContracts.every(token => root.includes(token)), 'PUBLIC-only guard, merge, and tombstone contracts present');

let diffPass = false; let diffDetail = '';
try { execFileSync('git', ['diff', '--check']); diffPass = true; diffDetail = 'No whitespace errors'; }
catch (error) { diffDetail = String(error?.stdout || error?.message || error); }
check('git-diff-check', 'Git diff integrity', diffPass, diffDetail);

const failed = results.filter(result => result.status === 'FAIL');
const evidence = {
  gate: 'v0.4.5｜Stable Promotion & PUBLIC Release Gate',
  certifiedRcCommit,
  frozenCandidateCommit,
  testedVersion: expectedVersion,
  generatedAt: new Date().toISOString(),
  automatedSummary: { total: results.length, pass: results.length - failed.length, fail: failed.length },
  inheritedCertifiedEvidence: { automated: '22/22 PASS', manualR2: '10/10 PASS', rcDevice: '8/8 PASS', combined: '40/40 PASS' },
  prePromotionPublic: { revision: 23, meetups: 2, sessions: 2, recordControls: 2, mutation: 'NONE' },
  releaseDecision: failed.length ? 'HOLD' : 'PROMOTION_READY',
  artifactHashes: Object.fromEntries(Object.entries(files).map(([name, file]) => [name, { file, sha256: sha256(file) }])),
  results,
};
console.log(JSON.stringify(evidence, null, 2));
process.exitCode = failed.length ? 1 : 0;
