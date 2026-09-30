import fs from 'node:fs';
import vm from 'node:vm';
import assert from 'node:assert/strict';
import path from 'node:path';
const root=path.resolve(process.argv[2]||'.');
const checks=[];
async function test(name,fn){try{await fn();checks.push({name,status:'PASS'});}catch(e){checks.push({name,status:'FAIL',detail:e.message});}}
const html=fs.readFileSync(path.join(root,'index.html'),'utf8');
const script=html.match(/<script>\s*([\s\S]*?)<\/script>/)[1];
await test('Application JavaScript parses',()=>new vm.Script(script));
await test('DB_VERSION stays 2',()=>assert.match(script,/const DB_VERSION=2;/));
await test('Production PUBLIC code preserved',()=>assert.match(script,/const PUBLIC_HISTORY_CODE='PUBLIC';/));
await test('Theme and layout local-only keys preserved',()=>{assert.match(script,/const LAYOUT_PREFS_KEY='bowlingMeetup.layoutPreferences.v1';/);assert.match(script,/const THEME_PREFS_KEY='bowlingMeetup.themePreferences.v1';/);});
const coreNames=['normalizeBowlingRoll','normalizeBowlingFrame','bowlingGameStarted','bowlingFrameComplete','bowlingFrameValid','bowlingNextRolls','bowlingGameCalc'];
const core=coreNames.map(n=>script.split('\n').find(line=>line.startsWith('function '+n+'('))).join('\n');
const calc=new Function(core+';return bowlingGameCalc;')();
const frame=r=>({rolls:r});
await test('Perfect 300',()=>assert.equal(calc([...Array(9)].map(()=>frame([10,null])).concat(frame([10,10,10]))).final,300));
await test('All spares 150',()=>assert.equal(calc([...Array(9)].map(()=>frame([5,5])).concat(frame([5,5,5]))).final,150));
await test('Open frames 90',()=>assert.equal(calc([...Array(9)].map(()=>frame([9,0])).concat(frame([9,0,null]))).final,90));
await test('Gutter game 0',()=>assert.equal(calc([...Array(9)].map(()=>frame([0,0])).concat(frame([0,0,null]))).final,0));
await test('Invalid tenth pins rejected',()=>assert.equal(calc([...Array(9)].map(()=>frame([0,0])).concat(frame([10,8,8]))).complete,false));
await test('Incomplete game has no final total',()=>assert.equal(calc([frame([10,null])]).final,null));
let seed=474;const rand=n=>{seed=(seed*1664525+1013904223)>>>0;return seed%n;};
function independent(rolls){let score=0,k=0;for(let f=0;f<10;f++){if(rolls[k]===10){score+=10+rolls[k+1]+rolls[k+2];k++;}else if(rolls[k]+rolls[k+1]===10){score+=10+rolls[k+2];k+=2;}else{score+=rolls[k]+rolls[k+1];k+=2;}}return score;}
await test('2000 deterministic valid games match independent scorer',()=>{
 for(let g=0;g<2000;g++){
  const frames=[],flat=[];
  for(let f=0;f<9;f++){const a=rand(11),b=a===10?null:rand(11-a);frames.push(frame([a,b]));flat.push(a);if(b!==null)flat.push(b);}
  const a=rand(11),b=a===10?rand(11):rand(11-a),c=(a===10)?rand((b===10?10:10-b)+1):(a+b===10?rand(11):null);
  frames.push(frame([a,b,c]));flat.push(a,b);if(c!==null)flat.push(c);
  const r=calc(frames);assert.equal(r.complete,true);assert.equal(r.final,independent(flat));
 }
});
function worker(){
 const events={},db=new Map(),origin='https://example.test/BowlMeet/',calls=[];let throwPut=false,network=async req=>{calls.push(req.url||req);return new Response('network');},skips=0;
 const key=req=>new URL(typeof req==='string'?req:req.url,origin).href;
 const cache=name=>{if(!db.has(name))db.set(name,new Map());const m=db.get(name);return {match:async req=>m.get(key(req))?.clone(),put:async(req,res)=>{if(throwPut)throw Error('quota');m.set(key(req),res.clone());},keys:async()=>[...m.keys()].map(x=>new Request(x)),delete:async req=>m.delete(key(req)),addAll:async paths=>{for(const p of paths)m.set(key(p),new Response('precache:'+p));}};};
 const ctx={URL,Set,Response,Headers,Promise,console,fetch:req=>network(req),caches:{open:async n=>cache(n),keys:async()=>[...db.keys()],delete:async n=>db.delete(n)},self:{registration:{scope:origin},addEventListener:(n,f)=>events[n]=f,clients:{claim:async()=>{}},skipWaiting:()=>skips++}};
 vm.createContext(ctx);vm.runInContext(fs.readFileSync(path.join(root,'sw.js'),'utf8'),ctx);
 const req=(url,mode='cors',method='GET',headers={})=>({url:new URL(url,origin).href,mode,method,headers:new Headers(headers)});
 async function send(r){let result=null,handled=false;events.fetch({request:r,respondWith:p=>{handled=true;result=p;},waitUntil:()=>{}});return {handled,response:await result};}
 return {ctx,db,cache,req,send,calls,setNetwork:fn=>network=fn,setQuota:()=>throwPut=true,skips:()=>skips,events,run:code=>vm.runInContext(code,ctx)};
}
await test('Worker JS parses',()=>new vm.Script(fs.readFileSync(path.join(root,'sw.js'),'utf8')));
await test('Manual update: install does not auto skip waiting',async()=>{const w=worker();let p;w.events.install({waitUntil:x=>p=x});await p;assert.equal(w.skips(),0);w.events.message({data:{type:'SKIP_WAITING'}});assert.equal(w.skips(),1);});
await test('POST RPC bypasses cache',async()=>{const w=worker();assert.equal((await w.send(w.req('rpc','cors','POST'))).handled,false);});
await test('Cross-origin cloud GET bypasses cache',async()=>{const w=worker();assert.equal((await w.send(w.req('https://cloud.test/auth/v1/settings'))).handled,false);});
await test('Requests bearing apikey bypass cache',async()=>{const w=worker();assert.equal((await w.send(w.req('index.html','navigate','GET',{apikey:'fixture'}))).handled,false);});
await test('Other project paths bypass cache',async()=>{const w=worker();assert.equal((await w.send(w.req('https://example.test/another/','navigate'))).handled,false);});
await test('Preview navigation bypasses production SW',async()=>{const w=worker();assert.equal((await w.send(w.req('preview/test/index.html','navigate'))).handled,false);});
await test('503 navigation uses last known good shell',async()=>{const w=worker();await w.cache(w.run('CACHE')).put('index.html',new Response('good'));w.setNetwork(async()=>new Response('bad',{status:503}));const r=await w.send(w.req('index.html','navigate'));assert.equal(await r.response.text(),'good');});
await test('Offline cold start returns explicit 503',async()=>{const w=worker();w.setNetwork(async()=>{throw Error('offline');});const r=await w.send(w.req('index.html','navigate'));assert.equal(r.response?.status,503);});
await test('Quota failure does not lose network response',async()=>{const w=worker();w.setQuota();const r=await w.send(w.req('index.html','navigate'));assert.equal(await r.response.text(),'network');});
await test('Versioned stylesheet and manifest are precached exactly',()=>{const w=worker(),shell=Array.from(w.run('APP_SHELL'));for(const match of html.matchAll(/<link rel="(?:stylesheet|manifest)" href="([^"]+)"/g))assert(shell.includes(match[1]),match[1]);});
await test('Activation leaves preview caches intact',async()=>{const w=worker();await w.cache('bowlmeet-preview-fixture').put('index.html',new Response('preview'));await w.cache('bowlmeet-vold-shell').put('index.html',new Response('old'));let p;w.events.activate({waitUntil:x=>p=x});await p;assert(w.db.has('bowlmeet-preview-fixture'));assert(!w.db.has('bowlmeet-vold-shell'));});
await test('Navigation query strings do not create unbounded cached URLs',async()=>{const w=worker();for(let i=0;i<50;i++)await w.send(w.req('index.html?room=fixture'+i,'navigate'));assert((await w.cache(w.run('RUNTIME')).keys()).length<=1);});
await test('Manual score guard exists before normalization',()=>assert.match(script,/function validateSheet\(\)\{[\s\S]*?input\.validity\.badInput/));
const result={suite:'Source / scoring differential / simulated Service Worker',scope:'No real cloud calls; Cache API simulated in Node',checks,passed:checks.filter(c=>c.status==='PASS').length,failed:checks.filter(c=>c.status==='FAIL').length};
console.log(JSON.stringify(result,null,2));if(result.failed)process.exitCode=1;
