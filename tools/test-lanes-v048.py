#!/usr/bin/env python3
"""Synthetic localhost native-storage lane UI regression. No real cloud or iPhone."""
import argparse,http.server,threading,json,re,hashlib,sys
from pathlib import Path
from playwright.sync_api import sync_playwright
p=argparse.ArgumentParser();p.add_argument('root',type=Path);p.add_argument('out',type=Path);p.add_argument('--browser',default='chromium');a=p.parse_args();root=a.root.resolve();a.out.mkdir(parents=True,exist_ok=True)
source=(root/'index.html').read_text();original=source
source=re.sub(r"const BUILTIN_SUPABASE_URL='[^']*';","const BUILTIN_SUPABASE_URL='';",source);source=re.sub(r"const BUILTIN_SUPABASE_PUBLISHABLE_KEY='[^']*';","const BUILTIN_SUPABASE_PUBLISHABLE_KEY='';",source);source=source.replace('const BUILTIN_CLOUD=true;','const BUILTIN_CLOUD=false;')
bridge="""window.qa={captureState,applyState,persistDbStateNow,renderLive,liveLanePlan,buildRoomPayload,parseRestorePayload,applyRestorePayload,setLiveRound,clearCompletedMeetupContext,selectLiveMeetup,setSyncConfig,saveLivePrefs,livePrefs,keys:{LIVEKEY},getPlan:()=>liveLanePlan(meetups.find(x=>x.id===currentMeetupId),sessions.find(x=>x.meetupId===currentMeetupId)),stop:()=>{clearTimeout(dbPersistTimer);dbPersistTimer=null},viewer:()=>{const c=getSyncConfig();c.enabled=true;c.meetupId=currentMeetupId;c.role='viewer';localStorage.setItem(SYNCKEY,JSON.stringify(c));renderLive()}};
"""
marker="$('date').value=today();$('meetupDate').value=today();load();";assert marker in source;source=source.replace(marker,bridge+marker).replace('initDataSafety().then(','window.boot=initDataSafety().then(')
class Handler(http.server.SimpleHTTPRequestHandler):
 def __init__(self,*args,**kw):super().__init__(*args,directory=str(root),**kw)
 def do_GET(self):
  if self.path.split('?')[0] in ['/','/index.html']:
   b=source.encode();self.send_response(200);self.send_header('Content-Type','text/html; charset=utf-8');self.end_headers();self.wfile.write(b)
  else:super().do_GET()
 def log_message(self,*args):pass
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),Handler);threading.Thread(target=server.serve_forever,daemon=True).start();url=f'http://127.0.0.1:{server.server_port}'
checks=[];errors=[]
def check(n,ok):
 checks.append(dict(name=n,status='PASS' if ok else 'FAIL'))
 if not ok:print('FAIL',n,flush=True)
def fixture():
 return dict(schema=3,sessions=[dict(id='s1',meetupId='m1',date='2026-10-16',venue='QA',lane='12、13',players=[dict(id='p'+str(i),name=n,scores=[v,None,None,None,None,None],updatedAt=100) for i,(n,v) in enumerate([('阿明',100),('小華',200),('志強',150)])],createdAt=100,updatedAt=100)],meetups=[dict(id='m1',title='測試球聚',date='2026-10-16',lanes='12、13',venue='QA',plannedGames=3,status='ongoing',participantNames=['阿明','小華','志強'],participantIds=[],createdAt=100,updatedAt=100)],roster=[],legacyRecords=[],activeMeetupId='m1',liveState={})
try:
 with sync_playwright() as pw:
  browser=getattr(pw,a.browser).launch(headless=True)
  ctx=browser.new_context(viewport={'width':390,'height':844},service_workers='block');ctx.route('**/*',lambda r:r.continue_() if r.request.url.startswith(url) else r.abort());page=ctx.new_page();page.on('pageerror',lambda e:errors.append(str(e)));page.on('dialog',lambda d:d.accept())
  page.goto(url);page.evaluate('()=>window.boot')
  page.evaluate('async s=>{qa.applyState(s);await qa.persistDbStateNow("qa");qa.renderLive()}',fixture())
  page.locator('#liveLaneManager summary').click()
  check('Legacy meetup defaults to unassigned',page.locator('#liveScoreList article').count()==3 and page.evaluate('qa.getPlan().players.every(x=>x.lane==="")'))
  for pid,lane in [('p0','12'),('p1','13'),('p2','12')]:page.locator(f'[data-lane-player="{pid}"]').select_option(lane)
  page.locator('[data-lane-move="p2"][data-direction="-1"]').click()
  check('Reorder within lane updates displayed player IDs',page.locator('#liveScoreList article').evaluate_all('(es)=>es.map(e=>e.dataset.pid)')==['p2','p0','p1'])
  page.locator('#liveLaneFilter').select_option('12')
  check('Lane filter shows only assigned players',page.locator('#liveScoreList article').evaluate_all('(es)=>es.map(e=>e.dataset.pid)')==['p2','p0'])
  check('Ranking still includes all players',page.locator('#liveRankBody tr').count()==3 and page.locator('#livePlayers').inner_text()=='3')
  page.evaluate('qa.setLiveRound(2)')
  check('Next round preserves assignment and order',page.locator('#liveScoreList article').evaluate_all('(es)=>es.map(e=>e.dataset.pid)')==['p2','p0'])
  roll=page.locator('[data-pid="p2"] input[data-frame="0"][data-roll="0"]');roll.fill('7');roll.dispatch_event('input')
  page.locator('#liveLaneFilter').select_option('13')
  check('Filter flushes pending score to correct player',page.evaluate('qa.captureState().sessions[0].players.find(x=>x.id==="p2").bowlingFrames[1][0].rolls[0]')==7)
  page.wait_for_timeout(250);before=page.evaluate('JSON.stringify(qa.captureState().sessions)');page.locator('#liveLaneFilter').select_option('12')
  check('Grouping never changes scores or player IDs',before==page.evaluate('JSON.stringify(qa.captureState().sessions)'))
  page.evaluate('qa.stop()');page.reload();page.evaluate('()=>window.boot')
  check('Immediate reload retains plan against stale IDB',page.locator('#liveLaneFilter').input_value()=='12' and page.locator('#liveScoreList article').evaluate_all('(es)=>es.map(e=>e.dataset.pid)')==['p2','p0'])
  page.close();page=ctx.new_page();page.on('pageerror',lambda e:errors.append(str(e)));page.on('dialog',lambda d:d.accept());page.goto(url);page.evaluate('()=>window.boot')
  check('Close and reopen browser tab retains plan',page.locator('#liveLaneFilter').input_value()=='12')
  backup=page.evaluate('qa.captureState()')
  check('Full backup contains local plan',backup['liveState']['m1']['lanePlan']['filter']=='12')
  check('Room sync payload excludes local plan','lanePlan' not in page.evaluate('JSON.stringify(qa.buildRoomPayload("m1"))'))
  page.locator('#liveLaneManager summary').click()
  page.locator('#liveLaneNames').fill('12');page.locator('#liveLaneApply').click()
  check('Removing occupied lane moves players to unassigned',page.evaluate('qa.getPlan().players.find(x=>x.id==="p1").lane')=='')
  page.evaluate('async s=>{await qa.applyRestorePayload(qa.parseRestorePayload(s),"replace");qa.selectLiveMeetup("m1",false)}',backup)
  check('Full replacement restore restores lane order',page.evaluate('qa.getPlan().lanes')==['12','13'] and page.locator('#liveScoreList article').evaluate_all('(es)=>es.map(e=>e.dataset.pid)')==['p2','p0'])
  page.locator('#liveLaneManager').evaluate('(e)=>e.open=true')
  before=page.evaluate('JSON.stringify(qa.getPlan())')
  page.evaluate("window.realSet=Storage.prototype.setItem;Storage.prototype.setItem=function(k,v){if(k===qa.keys.LIVEKEY)throw new DOMException('synthetic quota','QuotaExceededError');return realSet.call(this,k,v)}")
  page.locator('[data-lane-player="p0"]').select_option('13')
  check('Quota failure rejects change and warns',before==page.evaluate('JSON.stringify(qa.getPlan())') and '安排未保存' in page.locator('#liveLaneStatus').inner_text())
  page.evaluate('Storage.prototype.setItem=window.realSet')
  page.evaluate('qa.viewer()')
  check('Viewer cannot edit arrangement',page.locator('#liveLaneApply').is_disabled() and page.locator('[data-lane-player="p0"]').is_disabled())
  page.locator('#liveLaneFilter').select_option('13')
  check('Viewer can filter without modifying data',page.locator('#liveScoreList article').evaluate_all('(es)=>es.map(e=>e.dataset.pid)')==['p1'])
  page.evaluate('qa.setSyncConfig({enabled:false});qa.clearCompletedMeetupContext("m1");qa.selectLiveMeetup("m1",false)')
  check('Reopening completed context preserves arrangement',page.evaluate('qa.getPlan().players.find(x=>x.id==="p2").lane')=='12')
  page.locator('#liveLaneManager').evaluate('(e)=>e.open=true');page.locator('#liveLaneNames').fill('12、12、13');page.locator('#liveLaneApply').click()
  check('Duplicate lane labels normalized',page.evaluate('qa.getPlan().lanes')==['12','13'])
  page.locator('#liveLaneNames').fill('*');page.locator('#liveLaneApply').click()
  check('Reserved filter token rejected',page.evaluate('qa.getPlan().lanes')==['12','13'] and '不能使用' in page.locator('#liveLaneStatus').inner_text())
  page.locator('#liveLaneNames').fill('12、13');page.locator('#liveLaneApply').click()
  for width in [320,390,768,1440]:
   page.set_viewport_size({'width':width,'height':900});page.screenshot(path=str(a.out/f'lanes-{a.browser}-{width}.png'))
   check(f'{width}px no page overflow',page.evaluate('document.documentElement.scrollWidth<=innerWidth'))
  page.evaluate('s=>{qa.applyState(s);qa.renderLive()}',fixture())
  check('Older backup without plans stays usable',page.locator('#liveScoreList article').count()==3)
  page.evaluate('()=>{const p=qa.livePrefs();p.m1.lanePlan={lanes:["12"],players:[null,{id:"ghost",lane:"12"},{id:"p0",lane:"12"},{id:"p0",lane:"12"}],filter:"bad"};localStorage.setItem(qa.keys.LIVEKEY,JSON.stringify(p));qa.renderLive()}')
  check('Malformed plan drops duplicate and unknown IDs',len(page.evaluate('qa.getPlan().players'))==3 and page.locator('#liveLaneFilter').input_value()=='*')
  page.evaluate('()=>{const s=qa.captureState();s.meetups.push({...s.meetups[0],id:"m2"});s.sessions.push({...s.sessions[0],id:"s2",meetupId:"m2"});qa.applyState(s);qa.selectLiveMeetup("m2",false)}')
  check('Different meetups have independent arrangements',page.evaluate('qa.getPlan().players.every(x=>x.lane==="")'))
  ctx.close();browser.close()

except Exception as e:
 errors.append('HARNESS: '+repr(e))
finally:
 server.shutdown()
 result=dict(suite='v0.4.8-dev.1 lane native UI',browser=a.browser,source_sha256=hashlib.sha256(original.encode()).hexdigest(),checks=checks,errors=errors)
 result['passed']=sum(x['status']=='PASS' for x in checks);result['failed']=sum(x['status']=='FAIL' for x in checks);result['harness_errors']=len(errors)
 (a.out/f'lanes-{a.browser}.json').write_text(json.dumps(result,ensure_ascii=False,indent=2));print(json.dumps(result,ensure_ascii=False));sys.exit(2 if errors else 1 if result['failed'] else 0)
