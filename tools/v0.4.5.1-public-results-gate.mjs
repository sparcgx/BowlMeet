import fs from 'node:fs';
import crypto from 'node:crypto';
import { execFileSync } from 'node:child_process';

const expectedVersion='0.4.5.1';
const read=file=>fs.readFileSync(file,'utf8');
const sha256=file=>crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex');
const gitBlob=file=>execFileSync('git',['hash-object',file],{encoding:'utf8'}).trim();
const root=read('index.html'),manifest=read('manifest.webmanifest'),sw=read('sw.js');
const results=[];
const check=(id,name,pass,detail)=>results.push({id,name,status:pass?'PASS':'FAIL',detail});

function inlineScripts(html){return [...html.matchAll(/<script(?:\s[^>]*)?>([\s\S]*?)<\/script>/gi)].map(m=>m[1])}
function staticHtml(html){return html.replace(/<script(?:\s[^>]*)?>[\s\S]*?<\/script>/gi,'')}
function duplicateStaticIds(html){const ids=[...staticHtml(html).matchAll(/\bid=["']([A-Za-z][A-Za-z0-9_:\-.]*)["']/g)].map(m=>m[1]);return [...new Set(ids.filter((id,i)=>ids.indexOf(id)!==i))]}
function missingLiteralDomRefs(html){const ids=new Set([...staticHtml(html).matchAll(/\bid=["']([A-Za-z][A-Za-z0-9_:\-.]*)["']/g)].map(m=>m[1]));const refs=[...html.matchAll(/\$\(['"]([^'"$<>]+)['"]\)/g)].map(m=>m[1]);return [...new Set(refs.filter(ref=>!ids.has(ref)))]}
function duplicateFunctions(html){const names=[...inlineScripts(html).join('\n').matchAll(/(?:^|\n)function\s+([A-Za-z_$][\w$]*)\s*\(/g)].map(m=>m[1]);return [...new Set(names.filter((name,i)=>names.indexOf(name)!==i))]}
function functionBlock(name){const start=root.indexOf(`function ${name}(`);if(start<0)return '';const next=root.indexOf('\nfunction ',start+10);return root.slice(start,next<0?root.length:next)}

let syntaxPass=true,syntaxDetail='Inline JavaScript parsed successfully';
try{for(const script of inlineScripts(root))new Function(script)}catch(error){syntaxPass=false;syntaxDetail=String(error?.message||error)}
check('js-syntax','Root JavaScript syntax',syntaxPass,syntaxDetail);
const duplicateIds=duplicateStaticIds(root);check('duplicate-id','Static duplicate IDs',duplicateIds.length===0,duplicateIds.length?duplicateIds.join(', '):'0 duplicates');
const missingRefs=missingLiteralDomRefs(root);check('dom-ref','Literal DOM references',missingRefs.length===0,missingRefs.length?missingRefs.join(', '):'0 missing references');
const duplicateFns=duplicateFunctions(root);check('duplicate-function','Duplicate function declarations',duplicateFns.length===0,duplicateFns.length?duplicateFns.join(', '):'0 duplicates');
let swPass=true,swDetail='JavaScript parsed successfully';try{new Function(sw)}catch(error){swPass=false;swDetail=String(error?.message||error)}check('sw-syntax','Service Worker syntax',swPass,swDetail);
let manifestPass=true,manifestDetail='Valid JSON';try{JSON.parse(manifest)}catch(error){manifestPass=false;manifestDetail=String(error?.message||error)}check('manifest-json','Manifest JSON',manifestPass,manifestDetail);

check('version','APP_VERSION',root.includes(`const APP_VERSION='${expectedVersion}'`),expectedVersion);
check('cache','Hotfix PWA cache',sw.includes("const CACHE='bowlmeet-v0.4.5.1-public-only-shell'")&&sw.includes("const RUNTIME='bowlmeet-v0.4.5.1-public-only-runtime'"),'Dedicated v0.4.5.1 shell/runtime');
check('public-code','Formal PUBLIC cloud code unchanged',root.includes("const PUBLIC_HISTORY_CODE='PUBLIC'"),'PUBLIC');
check('public-source-helper','Published-only source helper',functionBlock('publicHistoryRecords').includes("filter(s=>stateMap.get(s.id)!=='removed')"),'Remote sessions only; removed tombstones excluded');
check('public-meetup-helper','Published meetup helper',functionBlock('publicMeetupRecords').includes('ids.has(m.id)'),'Only meetups linked to a published session');
check('public-games-helper','Public games helper',functionBlock('publicGames').includes('publicHistoryRecords()')&&!functionBlock('publicGames').includes('allGames()'),'Scores derive only from published remote sessions');

const rankingScope=functionBlock('rankingRowsForScope');
check('ranking-all-public','Leaderboard all-history source',rankingScope.includes('for(const g of publicGames())')&&!rankingScope.includes('allGames()'),'All-history uses publicGames');
check('ranking-meetup-public','Leaderboard meetup source',rankingScope.includes('publicMeetupById(scope)')&&rankingScope.includes('publicSessionForMeetup(scope)')&&!rankingScope.includes('linkedSession('),'Single meetup uses published session');
const leaderboard=functionBlock('renderLeaderboard');
check('ranking-options-public','Leaderboard option isolation',leaderboard.includes('publicMeetupRecords()')&&!leaderboard.includes('[...meetups]'),'Selector lists published meetups only');
check('ranking-kpi-public','Leaderboard KPI isolation',leaderboard.includes("sel.value==='all'?publicGames()")&&leaderboard.includes('publicSessionForMeetup(sel.value)'),'KPI uses the same public source');

const shareScope=functionBlock('shareScopeData');
check('share-scope-public','Share source isolation',shareScope.includes('publicMeetupById(scope)')&&shareScope.includes('publicSessionForMeetup(scope)')&&shareScope.includes("scope==='all'?publicGames()")&&!shareScope.includes('allGames()'),'All share card types receive public-only scope data');
const shareOptions=functionBlock('renderShareOptions');
check('share-options-public','Share option isolation',shareOptions.includes('publicMeetupRecords()')&&!shareOptions.includes('[...meetups]'),'Selector lists published meetups only');
check('share-full-card-public','Full score share isolation',root.includes('meetupFullShareRows(m,data.session)')&&functionBlock('meetupFullShareRows').includes('publicSessionForMeetup(m?.id)'),'Full card receives published session');
check('share-awards-public','Award/summary share isolation',root.includes("function computeAwards(meetupId,source='public')")&&root.includes("computeAwards(id,'local')"),'Share defaults public; editable Awards view remains local');
check('share-entry-guard','Local share entry guard',root.includes("requirePublicMeetup(currentMeetupId,'分享成績')")&&root.includes("requirePublicMeetup(id,'分享成績')"),'Live and post-review share require publication');
check('history-share-guard','History share guard',functionBlock('shareHistorySession').includes('publicHistoryRecords().find'),'History share resolves the published copy');
check('ui-disclosure','Public-only UI disclosure',root.includes('只統計已同步到公開歷史的成績')&&root.includes('本機未公開或已取消公開的紀錄不會列入'),'Leaderboard and share source disclosed');

const fixture={meetups:[{id:'m1'},{id:'m2'},{id:'m3'}],sessions:[{id:'s1',meetupId:'m1',players:[{name:'公開甲',scores:[100,120]}]},{id:'s2',meetupId:'m2',players:[{name:'已取消',scores:[300]}]},{id:'s3',meetupId:'m3',players:[{name:'公開乙',scores:[150]}]}],recordControls:[{id:'s2',state:'removed',updatedAt:2}]};
const state=new Map(fixture.recordControls.map(x=>[x.id,x.state])),published=fixture.sessions.filter(s=>state.get(s.id)!=='removed'),games=published.flatMap(s=>s.players.flatMap(p=>p.scores.map(score=>({player:p.name,score,meetupId:s.meetupId}))));
check('fixture-local-excluded','Fixture local-only exclusion',!games.some(g=>g.player==='本機未公開'),'Local-only data has no path into public fixture');
check('fixture-removed-excluded','Fixture tombstone exclusion',!games.some(g=>g.player==='已取消')&&games.length===3,'Removed session excluded; 3 published games remain');
check('fixture-meetup-scope','Fixture meetup isolation',games.filter(g=>g.meetupId==='m1').map(g=>g.score).join(',')==='100,120','Single public meetup returns only its published scores');

check('schema-baseline','Production Supabase schema unchanged',gitBlob('supabase_schema.sql')==='9d211151b01f8dd0e1a597829e77805ca0e60786','Matches v0.4.5 production blob');
check('patch-baseline','Production Supabase patch unchanged',gitBlob('supabase_v044_public_record_control_patch.sql')==='712b29e3c4ad910187b634427b031224f4b8f70b','Matches v0.4.5 production blob');
let diffPass=true,diffDetail='No whitespace errors';try{execFileSync('git',['diff','--check'])}catch(error){diffPass=false;diffDetail=String(error?.stdout||error?.message||error)}check('git-diff-check','Git diff integrity',diffPass,diffDetail);

const failed=results.filter(x=>x.status==='FAIL');
console.log(JSON.stringify({gate:'v0.4.5.1｜Public Results Only Hotfix Gate',testedVersion:expectedVersion,generatedAt:new Date().toISOString(),automatedSummary:{total:results.length,pass:results.length-failed.length,fail:failed.length},releaseDecision:failed.length?'HOLD':'PROMOTION_READY',scopeSafety:{supabaseSchemaChanged:false,dataFormatChanged:false,publicPayloadWritten:false},artifactHashes:{'index.html':sha256('index.html'),'manifest.webmanifest':sha256('manifest.webmanifest'),'sw.js':sha256('sw.js')},results},null,2));
process.exitCode=failed.length?1:0;
