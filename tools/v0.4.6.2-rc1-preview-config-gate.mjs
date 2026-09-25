import fs from 'node:fs';

const read = p => fs.readFileSync(p,'utf8');
const preview = read('preview/v0.4.6.2-RC.1/index.html');
const previewSw = read('preview/v0.4.6.2-RC.1/sw.js');
const schema = read('supabase_schema.sql');
const root = read('index.html');
const rootSw = read('sw.js');

const code = preview.match(/const PUBLIC_HISTORY_CODE='([^']+)'/)?.[1] || '';
const pin = preview.match(/const PUBLIC_HISTORY_PIN='([^']+)'/)?.[1] || '';
const checks = [];
const check = (name, ok) => checks.push({name,ok:Boolean(ok)});

check('preview code V46RC2', code === 'V46RC2');
check('preview code matches six-char Supabase rule', /^[A-Z2-9]{6}$/.test(code));
check('schema contains six-char group-code validation', schema.includes("^[A-Z2-9]{6}$"));
check('preview PIN is six digits', /^[0-9]{6}$/.test(pin));
check('preview DB isolated', preview.includes("const DB_NAME='bowlmeet.preview.v0462rc1.local'"));
check('preview layout key isolated', preview.includes("const LAYOUT_PREFS_KEY='bowlmeet.preview.v0462rc1.layoutPreferences.v1'"));
check('preview cache Fix1 rotated', previewSw.includes("PREVIEW_CACHE_PREFIX=PREVIEW_CACHE_ROOT+'rc1fix1-'"));
check('preview cache cleanup scoped', previewSw.includes('k.startsWith(PREVIEW_CACHE_ROOT)'));
check('preview has no global caches.match', !/\bcaches\.match\(/.test(previewSw));
check('production PUBLIC unchanged', root.includes("const PUBLIC_HISTORY_CODE='PUBLIC'"));
check('production DB unchanged', root.includes("const DB_NAME='bowlingMeetup.local'"));
check('production cache remains RC namespace', rootSw.includes("bowlmeet-v0.4.6.2-rc1-shell"));

const pass=checks.filter(x=>x.ok).length, fail=checks.length-pass;
for(const x of checks) console.log(`${x.ok?'PASS':'FAIL'} ${x.name}`);
console.log(`\nRC.1 Preview Cloud Configuration Gate: ${pass} PASS / ${fail} FAIL`);
if(fail) process.exit(1);
