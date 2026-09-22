import fs from 'node:fs';
import crypto from 'node:crypto';
import { execFileSync } from 'node:child_process';

const sourceEvidenceCommit = 'e0237facdd3b9ad5d76003615d58af063dbf86de';
const expectedVersion = '0.4.5-RC.1';
const files = {
  root: 'index.html',
  preview: 'preview/v0.4.5-RC.1/index.html',
  rootManifest: 'manifest.webmanifest',
  previewManifest: 'preview/v0.4.5-RC.1/manifest.webmanifest',
  rootSw: 'sw.js',
  previewSw: 'preview/v0.4.5-RC.1/sw.js',
};

const read = file => fs.readFileSync(file, 'utf8');
const sha256 = file => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex');
const results = [];
const check = (id, name, pass, detail) => results.push({ id, name, status: pass ? 'PASS' : 'FAIL', detail });

function inlineScripts(html) {
  return [...html.matchAll(/<script(?:\s[^>]*)?>([\s\S]*?)<\/script>/gi)].map(match => match[1]);
}

function staticHtml(html) {
  return html.replace(/<script(?:\s[^>]*)?>[\s\S]*?<\/script>/gi, '');
}

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
const preview = read(files.preview);
const devPreview = read('preview/v0.4.5-dev.4/index.html');

for (const [label, html] of [['Root', root], ['Preview', preview]]) {
  let syntaxPass = true;
  let syntaxDetail = 'Inline JavaScript parsed successfully';
  try {
    for (const script of inlineScripts(html)) new Function(script);
  } catch (error) {
    syntaxPass = false;
    syntaxDetail = String(error?.message || error);
  }
  check(`${label.toLowerCase()}-js-syntax`, `${label} JavaScript syntax`, syntaxPass, syntaxDetail);

  const duplicateIds = duplicateStaticIds(html);
  check(`${label.toLowerCase()}-duplicate-id`, `${label} static duplicate IDs`, duplicateIds.length === 0, duplicateIds.length ? duplicateIds.join(', ') : '0 duplicates');

  const missingRefs = missingLiteralDomRefs(html);
  check(`${label.toLowerCase()}-dom-ref`, `${label} literal DOM references`, missingRefs.length === 0, missingRefs.length ? missingRefs.join(', ') : '0 missing references');

  const duplicateFns = duplicateFunctions(html);
  check(`${label.toLowerCase()}-duplicate-function`, `${label} duplicate function declarations`, duplicateFns.length === 0, duplicateFns.length ? duplicateFns.join(', ') : '0 duplicates');
}

for (const [label, file] of [['Root service worker', files.rootSw], ['Preview service worker', files.previewSw]]) {
  let pass = true;
  let detail = 'JavaScript parsed successfully';
  try { new Function(read(file)); } catch (error) { pass = false; detail = String(error?.message || error); }
  check(label.toLowerCase().replaceAll(' ', '-'), `${label} syntax`, pass, detail);
}

for (const [label, file] of [['Root manifest', files.rootManifest], ['Preview manifest', files.previewManifest]]) {
  let pass = true;
  let detail = 'Valid JSON';
  try { JSON.parse(read(file)); } catch (error) { pass = false; detail = String(error?.message || error); }
  check(label.toLowerCase().replaceAll(' ', '-'), `${label} JSON`, pass, detail);
}

check('root-version', 'Root APP_VERSION', root.includes(`const APP_VERSION='${expectedVersion}'`), expectedVersion);
check('preview-version', 'Preview APP_VERSION', preview.includes(`const APP_VERSION='${expectedVersion}'`), expectedVersion);

const contextContracts = [
  "function validMeetupContextId(id='')",
  'function validateCurrentMeetupContext()',
  "function syncMeetupDerivedSelectors(id='')",
  "if(id&&id!=='all'){setCurrentMeetup(id);syncMeetupDerivedSelectors(id)}",
  'validateCurrentMeetupContext();renderKpis()',
];
check('root-context-contract', 'Root Meetup context safety contract', contextContracts.every(token => root.includes(token)), 'Canonical validation, selector sync, all-history guard, and render validation present');
check('preview-context-contract', 'Preview Meetup context safety contract', contextContracts.every(token => preview.includes(token)), 'Canonical validation, selector sync, all-history guard, and render validation present');

const previewIsolation = [
  "const PUBLIC_HISTORY_CODE='V45D41'",
  "const DB_NAME='bowlmeet.preview.v045rc1.local'",
  "const V2KEY='bowlmeet.preview.v045rc1.sessions.v2'",
  "const ACTIVEKEY='bowlmeet.preview.v045rc1.activeEvent.v3'",
];
check('preview-storage-isolation', 'Preview storage/cloud isolation', previewIsolation.every(token => preview.includes(token)), 'Cloud V45D41, isolated IndexedDB and localStorage keys');
check('preview-cache-isolation', 'Preview cache isolation', read(files.previewSw).includes("const PREVIEW_CACHE_PREFIX='bowlmeet-preview-v045rc1-'"), 'Dedicated RC Preview cache prefix');

const normalizeRcPreview = value => value
  .replaceAll('0.4.5-RC.1', '0.4.5-dev.4-R2')
  .replaceAll('v045rc1', 'v045d4')
  .replace(/[ \t]+$/gm, '');
check('rc-preview-functional-parity', 'RC Preview functional parity with accepted R2', normalizeRcPreview(preview) === normalizeRcPreview(devPreview), 'Only version, isolated namespace tokens, and whitespace normalization differ from accepted R2 Preview');

const logicStart = 'function safeJsonParse';
const rcScript = inlineScripts(root).join('\n');
const acceptedScript = inlineScripts(devPreview).join('\n');
const rcLogic = rcScript.slice(rcScript.indexOf(logicStart));
const acceptedLogic = acceptedScript.slice(acceptedScript.indexOf(logicStart));
check('rc-root-logic-parity', 'RC root logic parity with accepted R2', rcLogic === acceptedLogic, 'Executable application logic unchanged after storage/version constants');

let schemaUnchanged = false;
let schemaDetail = '';
try {
  execFileSync('git', ['diff', '--quiet', '12fbb04..HEAD', '--', 'supabase_schema.sql', 'supabase_pin_change_patch.sql', 'supabase_v044_public_record_control_patch.sql']);
  schemaUnchanged = true;
  schemaDetail = 'No changes from pre-DEV4-06 baseline';
} catch {
  schemaDetail = 'Schema or patch files changed';
}
check('supabase-schema', 'Supabase schema and patches unchanged', schemaUnchanged, schemaDetail);

let diffCheckPass = false;
let diffCheckDetail = '';
try {
  execFileSync('git', ['diff', '--check', '12fbb04..HEAD']);
  diffCheckPass = true;
  diffCheckDetail = 'No whitespace errors';
} catch (error) {
  diffCheckDetail = String(error?.stdout || error?.message || error);
}
check('git-diff-check', 'Git diff integrity', diffCheckPass, diffCheckDetail);

const failed = results.filter(result => result.status === 'FAIL');
const evidence = {
  gate: 'v0.4.5-RC.1｜Release Candidate Integration & Freeze Gate',
  sourceEvidenceCommit,
  testedVersion: expectedVersion,
  generatedAt: new Date().toISOString(),
  automatedSummary: { total: results.length, pass: results.length - failed.length, fail: failed.length },
  inheritedManualAcceptance: { status: 'PASS', confirmedBy: 'User', confirmedDate: '2026-09-22', matrix: 'DEV4-06-R2 10-item device regression' },
  rcDeviceAcceptance: { status: 'PENDING', scope: 'RC version, PWA cache, isolated storage, startup and cross-module smoke test' },
  releaseDecision: failed.length ? 'HOLD' : 'DEVICE_ACCEPTANCE_PENDING',
  artifactHashes: Object.fromEntries(Object.entries(files).map(([name, file]) => [name, { file, sha256: sha256(file) }])),
  results,
};

console.log(JSON.stringify(evidence, null, 2));
process.exitCode = failed.length ? 1 : 0;
