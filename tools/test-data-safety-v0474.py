#!/usr/bin/env python3
"""Native-storage fault injection on localhost with synthetic data only.
Runtime functions are NOT patched. An IIFE bridge exposes existing calls.
Exit 1 = application safety assertions failed; exit 2 = harness error.
"""
from __future__ import annotations
import argparse, contextlib, hashlib, http.server, json, os, re, shutil, threading, time
from pathlib import Path
from urllib.parse import urlsplit, unquote
from playwright.sync_api import sync_playwright

parser=argparse.ArgumentParser()
parser.add_argument('root',type=Path)
parser.add_argument('out',type=Path)
parser.add_argument('--browser',choices=['chromium','webkit'],default='chromium')
args=parser.parse_args(); ROOT=args.root.resolve(); OUT=args.out.resolve(); OUT.mkdir(parents=True,exist_ok=True)
original=(ROOT/'index.html').read_text(encoding='utf-8')
assert "const DB_VERSION=2;" in original and "async function initDataSafety()" in original
RUN='bowlmeet.fi.'+str(time.time_ns())+'.'
source=original.replace('bowlingMeetup.',RUN)
source=source.replace('bowlingScoreWorkstation.',RUN)
source=re.sub(r'bowlmeet\.preview\.[A-Za-z0-9]+\.',RUN,source)
source=re.sub(r"const BUILTIN_SUPABASE_URL='[^']*';","const BUILTIN_SUPABASE_URL='';",source)
source=re.sub(r"const BUILTIN_SUPABASE_PUBLISHABLE_KEY='[^']*';","const BUILTIN_SUPABASE_PUBLISHABLE_KEY='';",source)
source=source.replace('const BUILTIN_CLOUD=true;','const BUILTIN_CLOUD=false;')
KEYS={k:v for k,v in re.findall(r"const (\w+)='([^']*)';",source) if v.startswith(RUN)}
for k,v in re.findall(r"const (\w+)='([^']*)';",source):
 if k=='DB_NAME': KEYS[k]=v
assert all(k in KEYS for k in ['V2KEY','V1KEY','MEETUPKEY','ROSTERKEY','DRAFTKEY','PUBLIC_CONTROL_KEY','DB_NAME'])
HOOK=r'''
window.__fi={
 keys:{V2KEY,V1KEY,MEETUPKEY,ROSTERKEY,DRAFTKEY,SETTINGS,LIVEKEY,ACTIVEKEY,PERSONALKEY,PUBLIC_CONTROL_KEY,DB_NAME},
 captureState,applyState,load,initDataSafety,persist,persistMeetups,persistRoster,saveDraft,
 persistDbStateNow,queueDbStatePersist,idbGet,idbGetAll,idbPut,idbPutMany,idbDelete,
 createSnapshot,listSnapshots,getPublicControl,setPublicRecordState,publicRecordState,
 exportFullBackup,renderSafety,
 status:()=>({dbReady,dbMode,timer:dbPersistTimer,score:sessions[0]?.players?.[0]?.scores?.[0]??null,
   sessions:sessions.map(s=>s.id),meetups:meetups.map(m=>m.id),roster:roster.map(r=>r.id),
   publicControl:getPublicControl(),engine:document.getElementById('safetyEngineSub')?.textContent,
   live:document.getElementById('liveSaveState')?.textContent}),
 changeScore:n=>{const t=Date.now();sessions[0].players[0].scores[0]=n;sessions[0].players[0].scoreUpdatedAt[0]=t;sessions[0].players[0].updatedAt=t;sessions[0].updatedAt=t;},
 changeMeetup:()=>{meetups[0].title='FI NEW TITLE';meetups[0].updatedAt=Date.now();},
 changeRoster:()=>{roster[0].name='FI NEW NAME';roster[0].updatedAt=Date.now();},
 stopQueue:()=>{clearTimeout(dbPersistTimer);dbPersistTimer=null;},
 closeDb:()=>{if(appDb)appDb.close();},
 setPublicFixture:s=>{groupRemote={sessions:s.sessions,meetups:s.meetups,recordControls:[]};},
 getBoot:()=>window.__fiBoot
};
'''
marker="$('date').value=today();$('meetupDate').value=today();load();"
assert source.count(marker)==1
source=source.replace(marker,HOOK+'\n'+marker)
assert source.count("initDataSafety().then(")==1
source=source.replace('initDataSafety().then(','window.__fiBoot=initDataSafety().then(')
INIT=r'''
window.__fiFault={};window.__fiEvents=[];window.__fiPageErrors=[];
window.addEventListener('error',e=>__fiPageErrors.push(String(e.message)));
window.addEventListener('unhandledrejection',e=>__fiPageErrors.push('unhandled:'+String(e.reason)));
const nativeSet=Storage.prototype.setItem,nativeGet=Storage.prototype.getItem;
Storage.prototype.setItem=function(k,v){
 if(window.__fiFault.writeKey===String(k)){
  const name=__fiFault.writeName||'QuotaExceededError';__fiEvents.push({kind:'storage-write',key:String(k),name});
  throw new DOMException('Synthetic FI: '+name,name);
 }
 return nativeSet.call(this,k,v);
};
Storage.prototype.getItem=function(k){
 if(window.__fiFault.readKey===String(k)){
  __fiEvents.push({kind:'storage-read',key:String(k)});
  throw new DOMException('Synthetic FI: denied read','SecurityError');
 }
 return nativeGet.call(this,k);
};
const nativePut=IDBObjectStore.prototype.put,nativeDelete=IDBObjectStore.prototype.delete;
for(const [op,fn] of [['put',nativePut],['delete',nativeDelete]]){
 IDBObjectStore.prototype[op]=function(...values){
  const request=fn.apply(this,values),tx=this.transaction;
  const key=op==='put'?values[0]?.key:values[0];
  if(__fiFault.abortKey===key&&__fiFault.abortOp===op){
   __fiFault.abortKey=null;
   tx.addEventListener('abort',()=>__fiEvents.push({kind:'native-abort',key,op}));
   request.addEventListener('success',()=>{__fiEvents.push({kind:'request-success-before-abort',key,op});tx.abort();},{once:true});
  }
  return request;
 };
}
'''

class Handler(http.server.BaseHTTPRequestHandler):
 def do_GET(self):
  path=unquote(urlsplit(self.path).path)
  if path=='/__seed': data=b'<!doctype html><title>FI localhost seed</title>';typ='text/html'
  elif path in ['/app/','/app/index.html']: data=source.encode();typ='text/html; charset=utf-8'
  elif path.startswith('/app/'):
   p=(ROOT/path[5:]).resolve()
   if not p.is_relative_to(ROOT) or not p.is_file(): self.send_error(404);return
   data=p.read_bytes();typ='text/css' if p.suffix=='.css' else 'application/javascript' if p.suffix=='.js' else 'image/svg+xml' if p.suffix=='.svg' else 'image/png' if p.suffix=='.png' else 'application/json'
  else: self.send_error(404);return
  self.send_response(200);self.send_header('Content-Type',typ);self.send_header('Cache-Control','no-store');self.end_headers();self.wfile.write(data)
 def log_message(self,*a): pass
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),Handler)
threading.Thread(target=server.serve_forever,daemon=True).start()
ORIGIN=f'http://127.0.0.1:{server.server_port}'
T0=1700000000000

def state(score=100,stamp=T0):
 return {'schema':3,'appVersion':'0.4.7.4-dev.1','updatedAt':stamp,
  'sessions':[{'id':'fi-session','meetupId':'fi-meetup','date':'2026-09-30','venue':'FI synthetic venue','lane':'1','createdAt':T0,'updatedAt':stamp,
    'players':[{'id':'fi-player','name':'FI synthetic player','scores':[score,None,None,None,None,None],
     'scoreUpdatedAt':[stamp,0,0,0,0,0],'bowlingFrames':[None]*6,'frameUpdatedAt':[0]*6,'updatedAt':stamp}]}],
  'meetups':[{'id':'fi-meetup','sessionId':'fi-session','title':'FI TITLE','date':'2026-09-30','venue':'FI synthetic venue','lanes':'1','plannedGames':6,'status':'done','participantIds':['fi-player'],'participantNames':['FI synthetic player'],'createdAt':T0,'updatedAt':stamp}],
  'roster':[{'id':'fi-player','name':'FI synthetic player','createdAt':T0,'updatedAt':stamp}],
  'legacyRecords':[],'personalData':{},'activeMeetupId':'','draft':None,'settings':{},'liveState':{},'publicControl':{'records':[]}}

SEED=r'''async ({keys,local,db,version=2,hold=false})=>{
 if(local){
  const map={V2KEY:'sessions',V1KEY:'legacyRecords',MEETUPKEY:'meetups',ROSTERKEY:'roster',PERSONALKEY:'personalData',PUBLIC_CONTROL_KEY:'publicControl',SETTINGS:'settings',LIVEKEY:'liveState'};
  for(const [k,v] of Object.entries(map))localStorage.setItem(keys[k],JSON.stringify(local[v]));
  if(local.draft)localStorage.setItem(keys.DRAFTKEY,JSON.stringify(local.draft));
 }
 if(db!==null){
  const d=await new Promise((resolve,reject)=>{
   const r=indexedDB.open(keys.DB_NAME,version);
   r.onupgradeneeded=()=>{const d=r.result;d.createObjectStore('state',{keyPath:'key'});const s=d.createObjectStore('snapshots',{keyPath:'id'});s.createIndex('createdAt','createdAt');const l=d.createObjectStore('syncLog',{keyPath:'id'});l.createIndex('createdAt','createdAt');};
   r.onsuccess=()=>resolve(r.result);r.onerror=()=>reject(r.error);
  });
  await new Promise((resolve,reject)=>{const t=d.transaction('state','readwrite');t.oncomplete=resolve;t.onerror=()=>reject(t.error);const s=t.objectStore('state');s.put({key:'appState',value:db});s.put({key:'meta',value:{lastWriteAt:db.updatedAt||0}});s.put({key:'safetyMeta',value:{lastAutoSnapshotAt:Date.now()}});});
  if(hold)window.__heldDb=d;else d.close();
 }
}'''
OBSERVE=r'''async()=>{
 const f=__fi,status=f.status();
 const req=indexedDB.open(f.keys.DB_NAME,2),db=await new Promise((r,j)=>{req.onsuccess=()=>r(req.result);req.onerror=()=>j(req.error);});
 const stored=await new Promise((r,j)=>{const q=db.transaction('state').objectStore('state').get('appState');q.onsuccess=()=>r(q.result?.value??null);q.onerror=()=>j(q.error);});db.close();
 const local={};for(const k of ['V2KEY','MEETUPKEY','ROSTERKEY','DRAFTKEY','PUBLIC_CONTROL_KEY']){try{local[k]=JSON.parse(localStorage.getItem(f.keys[k])||'null')}catch(e){local[k]='ERROR:'+e.name}}
 return {status,db:stored,local,events:__fiEvents,errors:__fiPageErrors};
}'''
results=[];external=[];browser=None
@contextlib.contextmanager
def environment(local=None,db=None,fault=None,hold=False,boot=True):
 ctx=browser.new_context(viewport={'width':390,'height':844},locale='zh-TW',service_workers='block',accept_downloads=True)
 def route(r):
  if r.request.url.startswith(ORIGIN+'/'):r.continue_()
  else:external.append(r.request.url);r.abort()
 ctx.route('**/*',route);ctx.add_init_script(INIT)
 try:
  seed=ctx.new_page();seed.goto(ORIGIN+'/__seed');seed.evaluate(SEED,{'keys':KEYS,'local':local,'db':db,'version':1 if hold else 2,'hold':hold})
  page=ctx.new_page()
  if fault: page.add_init_script('Object.assign(window.__fiFault,'+json.dumps(fault)+');')
  page.goto(ORIGIN+'/app/',wait_until='load')
  if boot:
   page.wait_for_function('!!window.__fi && !!window.__fiBoot',timeout=5000)
   page.evaluate('()=>window.__fiBoot');page.wait_for_timeout(350);page.evaluate('__fi.stopQueue()')
  yield page,seed
 finally:ctx.close()

def log_case(cid,name,category,fn):
 try:
  ok,detail=fn()
  item={'id':cid,'name':name,'category':category,'status':'PASS' if ok else 'FAIL','detail':detail}
 except Exception as e:item={'id':cid,'name':name,'category':category,'status':'HARNESS_ERROR','detail':str(e)}
 results.append(item);print(json.dumps(item,ensure_ascii=False),flush=True)
 (OUT/'results.partial.json').write_text(json.dumps(results,ensure_ascii=False,indent=2))

def state_result(p):
 o=p.evaluate(OBSERVE)
 return {'memory_score':o['status']['score'],'idb_score':o['db']['sessions'][0]['players'][0]['scores'][0] if o['db'] and o['db'].get('sessions') else None,
 'local_score':o['local']['V2KEY'][0]['players'][0]['scores'][0] if isinstance(o['local']['V2KEY'],list) and o['local']['V2KEY'] else None,
 'memory_session_ids':o['status']['sessions'],'idb_session_ids':[s['id'] for s in (o['db'] or {}).get('sessions',[])],
 'local_session_ids':[s['id'] for s in (o['local']['V2KEY'] or [])] if isinstance(o['local']['V2KEY'],list) else [],
 'dbReady':o['status']['dbReady'],'dbMode':o['status']['dbMode'],'errors':o['errors'],'events':o['events']}

def bootstrap(local,db,expected):
 with environment(local,db) as (p,_):
  d=state_result(p);return d['memory_score']==d['local_score']==d['idb_score']==expected,d

def newer_session():
 old=state();new=state(220,T0+10000);added=json.loads(json.dumps(new['sessions'][0]));added['id']='fi-session-added';new['sessions'].append(added)
 with environment(new,old) as (p,_):
  d=state_result(p);return 'fi-session-added' in d['memory_session_ids'] and 'fi-session-added' in d['local_session_ids'],d

def newer_tombstone():
 old=state();new=state(220,T0+10000);new['publicControl']['records']=[{'id':'fi-session','state':'removed','updatedAt':T0+10000}]
 with environment(new,old) as (p,_):
  p.evaluate('(s)=>__fi.setPublicFixture(s)',new);d=p.evaluate(OBSERVE)
  actual=p.evaluate("__fi.publicRecordState('fi-session')")
  return actual=='removed',{'expected':'removed','actual':actual,'local':d['local']['PUBLIC_CONTROL_KEY'],'idb':d['db']['publicControl'],'no_cloud':True}

def quota(method,key):
 with environment(state(),state()) as (p,_):
  p.evaluate('__fi.stopQueue()')
  p.evaluate('__fi.changeScore(220)' if method=='persist' else '__fi.changeMeetup()' if method=='persistMeetups' else '__fi.changeRoster()')
  p.evaluate('(key)=>{__fiFault.writeKey=__fi.keys[key]}',key)
  outcome=p.evaluate('(method)=>{try{__fi[method]();return "returned"}catch(e){return e.name}}',method)
  p.wait_for_timeout(350);o=p.evaluate(OBSERVE)
  if method=='persist':new_saved=o['db']['sessions'][0]['players'][0]['scores'][0]==220
  elif method=='persistMeetups':new_saved=o['db']['meetups'][0]['title']=='FI NEW TITLE'
  else:new_saved=o['db']['roster'][0]['name']=='FI NEW NAME'
  d={'exception':outcome,'idb_fallback_saved':new_saved,'queued_timer':o['status']['timer'],'injection_events':o['events'],'dbReady':o['status']['dbReady']}
  return outcome=='returned' and new_saved,d

def immediate_reload():
 with environment(state(),state()) as (p,_):
  with p.expect_navigation(wait_until='load'):
   p.evaluate('__fi.changeScore(222);__fi.persist();location.reload()')
  p.wait_for_function('!!window.__fiBoot');p.evaluate('()=>__fiBoot');p.wait_for_timeout(350)
  d=state_result(p);return d['memory_score']==222,d

def idb_abort(method,store,key):
 with environment(state(),state()) as (p,_):
  p.evaluate('__fi.stopQueue()')
  if method=='idbDelete':p.evaluate("()=>__fi.idbPut('state',{key:'fi-delete',value:'retain-on-abort'})")
  p.evaluate('({key,op})=>Object.assign(__fiFault,{abortKey:key,abortOp:op})',{'key':key,'op':'delete' if method=='idbDelete' else 'put'})
  call="__fi.idbDelete('state','fi-delete')" if method=='idbDelete' else "__fi.idbPut('state',{key:'fi-one',value:1})" if method=='idbPut' else "__fi.persistDbStateNow('fi-abort', {...__fi.captureState(), sessions:[]})"
  d=p.evaluate("async()=>{const promise="+call+";const outcome=await Promise.race([promise.then(()=> 'resolved',e=>'rejected:'+e.name),new Promise(r=>setTimeout(()=>r('PENDING_AFTER_750MS'),750))]);return {outcome,events:__fiEvents};}")
  d['transaction_rolled_back']=p.evaluate("async()=>"+("(await __fi.idbGet('state','fi-delete'))?.value==='retain-on-abort'" if method=='idbDelete' else "!(await __fi.idbGet('state','fi-one'))" if method=='idbPut' else "(await __fi.idbGet('state','appState')).value.sessions.length===1"))
  return d['outcome'].startswith('rejected:') and d['transaction_rolled_back'],d

def closed_connection():
 with environment(state(),state()) as (p,_):
  p.evaluate('__fi.stopQueue();__fi.closeDb();__fi.changeScore(220);__fi.persist()');p.wait_for_timeout(350)
  before=state_result(p)
  p.reload();p.wait_for_function('!!window.__fiBoot');p.evaluate('()=>__fiBoot');p.wait_for_timeout(350)
  after=state_result(p)
  return after['memory_score']==220,{'before_reload':before,'after_reload':after}

def malformed_state():
 with environment(state(220,T0+10000),{'unexpected':'not-an-app-state'}) as (p,_):
  d=state_result(p);return d['memory_score']==220 or d['local_score']==220,d

def missing_idb():
 with environment(state(220),None,fault=None,boot=False) as (p,_):
  p.wait_for_function('!!window.__fiBoot');p.evaluate('()=>__fiBoot');p.wait_for_timeout(350);d=state_result(p)
  return d['memory_score']==220 and d['idb_score']==220,d

def disabled_idb():
 with environment(state(220),state(),boot=False) as (p,_):
  p.wait_for_function('!!window.__fiBoot');p.evaluate('()=>__fiBoot');p.wait_for_timeout(350)
  p.evaluate("localStorage.setItem(__fi.keys.V2KEY,JSON.stringify([{...__fi.captureState().sessions[0],players:[{...__fi.captureState().sessions[0].players[0],scores:[220,null,null,null,null,null]}]}]))")
  p.add_init_script("indexedDB.open=function(){throw new DOMException('Synthetic FI: IDB disabled','SecurityError')};")
  p.reload();p.wait_for_function('!!window.__fiBoot');p.evaluate('()=>__fiBoot');p.wait_for_timeout(250)
  d=p.evaluate('__fi.status()');return d['score']==220 and not d['dbReady'],d

def partial_mirror():
 with environment(state(),state()) as (p,_):
  new=state(220,T0+10000);new['meetups'][0]['title']='FI NEW TITLE';new['roster'][0]['name']='FI NEW NAME'
  p.evaluate('__fiFault.writeKey=__fi.keys.MEETUPKEY')
  p.evaluate('(s)=>__fi.applyState(s,{render:false})',new)
  p.wait_for_timeout(200);o=p.evaluate(OBSERVE)
  d={'memory_score':o['status']['score'],'local_score':o['local']['V2KEY'][0]['players'][0]['scores'][0],
   'local_meetup_title':o['local']['MEETUPKEY'][0]['title'],'idb_score':o['db']['sessions'][0]['players'][0]['scores'][0],
   'engine':o['status']['engine'],'dbReady':o['status']['dbReady'],'events':o['events']}
  return (d['local_score']==220 and d['local_meetup_title']=='FI NEW TITLE') or d['idb_score']==220,d

def real_quota():
 with environment(state(),state()) as (p,_):
  d=p.evaluate(r'''()=>{__fi.stopQueue();let bytes=0,count=0;const chunk='X'.repeat(32768);let name='';try{while(count<512){localStorage.setItem('fi-native-quota-'+count,chunk);bytes+=chunk.length;count++}}catch(e){name=e.name}__fi.changeScore(233);const snap=__fi.captureState();snap.sessions[0].notes='Y'.repeat(65536);__fi.applyState(snap,{render:false});let outcome='returned';try{__fi.persist()}catch(e){outcome=e.name}return {nativeQuota:name,fillCharacters:bytes,fillKeys:count,persistOutcome:outcome}}''')
  p.wait_for_timeout(350);o=p.evaluate(OBSERVE);d['idb_score']=o['db']['sessions'][0]['players'][0]['scores'][0]
  return d['nativeQuota']=='QuotaExceededError' and d['idb_score']==233,d

def both_fail():
 with environment(state(),state()) as (p,_):
  p.evaluate('__fi.closeDb();__fiFault.writeKey=__fi.keys.V2KEY;__fi.changeScore(220)')
  d=p.evaluate("()=>{let exception='';try{__fi.persist()}catch(e){exception=e.name}return {exception,...__fi.status()}}")
  p.wait_for_timeout(200)
  warning=('未儲存' in (d['engine'] or '') or '失敗' in (d['engine'] or '') or '暫存' in (d['engine'] or ''))
  return warning,{'exception':d['exception'],'dbReady':d['dbReady'],'engine':d['engine'],'memory_score':d['score'],'unsaved_warning':warning}

def delayed_boot():
 with environment(state(),state(),hold=True,boot=False) as (p,seed):
  p.wait_for_function('!!window.__fi')
  p.evaluate('__fi.changeScore(240);__fi.persist()');p.wait_for_timeout(200)
  before=p.evaluate('__fi.status()')
  seed.evaluate('__heldDb.close()')
  p.wait_for_function('!!window.__fiBoot');p.evaluate('()=>__fiBoot');p.wait_for_timeout(350)
  after=state_result(p)
  return after['memory_score']==240,{'during_blocked_open':before,'after_unblocking':after}

def snapshot_roundtrip():
 with environment(state(),state()) as (p,_):
  d=p.evaluate("async()=>{const snap=await __fi.createSnapshot('FI baseline snapshot');__fi.changeScore(250);await __fi.persistDbStateNow('FI change');__fi.applyState(snap.state,{render:false});await __fi.persistDbStateNow('FI restore');return {after:__fi.status().score,snapshotScore:snap.state.sessions[0].players[0].scores[0]}}")
  return d['after']==100 and d['snapshotScore']==100,d

def zero_score():return bootstrap(state(0,T0+10),state(0,T0+10),0)

def newer_draft():
 old=state();new=state(220,T0+10000)
 old['draft']={'date':'2026-09-30','players':[{'id':'fi-draft','name':'FI draft','scores':[100,None,None,None,None,None]}]}
 new['draft']={'date':'2026-09-30','players':[{'id':'fi-draft','name':'FI draft','scores':[220,None,None,None,None,None]}]}
 with environment(new,old) as (p,_):
  o=p.evaluate(OBSERVE);d={'draft_score':o['local']['DRAFTKEY']['players'][0]['scores'][0],'visible_input':p.locator('.score-in').first.input_value()}
  return d['draft_score']==220,d

def corrupt_ls():
 with environment(state(),state(225,T0+10)) as (p,_):
  p.evaluate("localStorage.setItem(__fi.keys.V2KEY,'{bad json')")
  p.reload();p.wait_for_function('!!window.__fiBoot');p.evaluate('()=>__fiBoot');p.wait_for_timeout(350)
  d=state_result(p);return d['memory_score']==225 and d['local_score']==225,d

with sync_playwright() as pw:
 engine=getattr(pw,args.browser)
 exe=os.environ.get('BROWSER_EXECUTABLE') or (shutil.which('chromium') if args.browser=='chromium' else None)
 browser=engine.launch(headless=True,**({'executable_path':exe,'args':['--no-sandbox']} if exe else {}))
 version=browser.version
 log_case('FI-01','Equal localStorage and IndexedDB bootstrap','control',lambda:bootstrap(state(),state(),100))
 log_case('FI-02','Newer IndexedDB wins against older local mirror','control',lambda:bootstrap(state(),state(220,T0+10000),220))
 log_case('FI-03','Newer local score must survive older IndexedDB','freshness',lambda:bootstrap(state(220,T0+10000),state(),220))
 log_case('FI-04','New local session must survive older IndexedDB','freshness',newer_session)
 log_case('FI-05','Local removed tombstone must not become published','freshness',newer_tombstone)
 log_case('FI-06','Newer local draft must survive older IndexedDB','freshness',newer_draft)
 log_case('FI-07','Immediate reload before 120ms persistence must retain edit','freshness',immediate_reload)
 log_case('FI-08','Sessions quota exception must not skip IDB fallback','quota',lambda:quota('persist','V2KEY'))
 log_case('FI-09','Meetups quota exception must not skip IDB fallback','quota',lambda:quota('persistMeetups','MEETUPKEY'))
 log_case('FI-10','Roster quota exception must not skip IDB fallback','quota',lambda:quota('persistRoster','ROSTERKEY'))
 log_case('FI-11','Partial localStorage mirror must not leave mixed generations','quota',partial_mirror)
 log_case('FI-12','Native localStorage quota must preserve IDB write path','native-quota',real_quota)
 log_case('FI-13','idbPut promise rejects on native abort after request success','transaction',lambda:idb_abort('idbPut','state','fi-one'))
 log_case('FI-14','idbPutMany promise rejects on native abort and data rolls back','transaction',lambda:idb_abort('idbPutMany','state','meta'))
 log_case('FI-15','idbDelete promise rejects on native abort and record remains','transaction',lambda:idb_abort('idbDelete','state','fi-delete'))
 log_case('FI-16','Closed IndexedDB connection fallback survives restart','freshness',closed_connection)
 log_case('FI-17','Malformed saved IDB object must not erase valid local records','corruption',malformed_state)
 log_case('FI-18','IDB missing: valid local data imports on first boot','control',missing_idb)
 log_case('FI-19','IDB unavailable: valid local data usable in fallback','control',disabled_idb)
 log_case('FI-20','Both write paths unavailable must show an unsaved warning','feedback',both_fail)
 log_case('FI-21','Edit while IDB open is blocked must survive release','startup-race',delayed_boot)
 log_case('FI-22','Normal snapshot restore retains score','control',snapshot_roundtrip)
 log_case('FI-23','Valid zero score survives storage bootstrap','control',zero_score)
 log_case('FI-24','Corrupt local JSON recovers from valid IndexedDB','control',corrupt_ls)
 browser.close()
server.shutdown()
result={'version':'v0.4.7.4-dev.2','purpose':'Data Safety Fault Injection — test-only; NOT a repair',
 'source_index_sha256':hashlib.sha256(original.encode()).hexdigest(),'browser':args.browser,'browser_version':version,
 'environment':'localhost HTTP, fresh isolated browser context per scenario, native localStorage + native IndexedDB; Service Worker blocked; no production data or cloud',
 'source_storage_prefix':RUN,'external_requests_blocked':external,'counts':{k:sum(r['status']==k for r in results) for k in ['PASS','FAIL','HARNESS_ERROR']},
 'gate':'HARNESS_ERROR' if any(r['status']=='HARNESS_ERROR' for r in results) else 'FAIL' if any(r['status']=='FAIL' for r in results) else 'PASS','cases':results,
 'limitations':['Not iOS Safari or installed PWA','No live Supabase/RLS','No physical disk-power-loss test','Synthetic targeted API failures are not actual OS disk exhaustion; FI-12 uses native localStorage quota','Test bridge exposes existing calls, does not replace storage functions']}
(OUT/'results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'gate':result['gate'],'counts':result['counts'],'browser_version':version},ensure_ascii=False))
raise SystemExit(2 if result['counts']['HARNESS_ERROR'] else 1 if result['counts']['FAIL'] else 0)
