#!/usr/bin/env python3
"""Synthetic localhost native-storage lane UI regression. No real cloud or iPhone."""
import argparse,http.server,threading,json,re,hashlib,sys
from pathlib import Path
from playwright.sync_api import sync_playwright
p=argparse.ArgumentParser();p.add_argument('root',type=Path);p.add_argument('out',type=Path);p.add_argument('--browser',default='chromium');a=p.parse_args();root=a.root.resolve();a.out.mkdir(parents=True,exist_ok=True)
source=(root/'index.html').read_text();original=source
source=re.sub(r"const BUILTIN_SUPABASE_URL='[^']*';","const BUILTIN_SUPABASE_URL='';",source);source=re.sub(r"const BUILTIN_SUPABASE_PUBLISHABLE_KEY='[^']*';","const BUILTIN_SUPABASE_PUBLISHABLE_KEY='';",source);source=source.replace('const BUILTIN_CLOUD=true;','const BUILTIN_CLOUD=false;')
bridge="""window.qa={computeSeriesResult,getSeriesRules,publicSeriesResult,renderLeaderboard,drawShareCard,switchView,renderShareOptions,setPublicRecordState,publish:s=>{groupRemote={schema:2,sessions:s.sessions,meetups:s.meetups,recordControls:[],updatedAt:100}},captureState,applyState,persistDbStateNow,renderLive,liveLanePlan,buildRoomPayload,parseRestorePayload,applyRestorePayload,setLiveRound,clearCompletedMeetupContext,selectLiveMeetup,setSyncConfig,saveLivePrefs,livePrefs,keys:{LIVEKEY},getPlan:()=>liveLanePlan(meetups.find(x=>x.id===currentMeetupId),sessions.find(x=>x.meetupId===currentMeetupId)),stop:()=>{clearTimeout(dbPersistTimer);dbPersistTimer=null},viewer:()=>{const c=getSyncConfig();c.enabled=true;c.meetupId=currentMeetupId;c.role='viewer';localStorage.setItem(SYNCKEY,JSON.stringify(c));renderLive()}};
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
  check('Series defaults disabled',page.evaluate('qa.getSeriesRules("m1")') is None)
  page.locator('#seriesSettings summary').click();page.locator('#seriesMode').select_option('total');page.locator('#seriesRounds').select_option('1');page.locator('#seriesSaveBtn').click()
  check('Individual total ranks correct player',page.locator('#liveSeriesResults tbody tr').first.inner_text().find('小華')>=0)
  check('Completed round final result', '最終結果' in page.locator('#liveSeriesResults').inner_text())
  page.locator('#seriesRounds').select_option('3');page.locator('#seriesSaveBtn').click()
  check('Missing rounds show provisional and deficit', '暫定排名' in page.locator('#liveSeriesResults').inner_text() and '缺 2 局' in page.locator('#liveSeriesResults').inner_text())
  page.locator('#seriesMode').select_option('team')
  for pid,team in [('p0','A 隊'),('p1','B 隊'),('p2','A 隊')]:page.locator(f'[data-series-player="{pid}"]').fill(team)
  page.locator('#seriesSaveBtn').click()
  check('Unequal teams warn', '各隊人數不同' in page.locator('#liveSeriesResults').inner_text())
  check('Team aggregate sum',page.evaluate('qa.computeSeriesResult(qa.captureState().sessions[0],qa.getSeriesRules("m1")).rows[0].total')==250)
  backup=page.evaluate('qa.captureState()');page.evaluate('qa.stop()');page.reload();page.evaluate('()=>window.boot')
  check('Immediate reload preserves team rules',page.evaluate('qa.getSeriesRules("m1").mode')=='team')
  page.locator('#seriesSettings').evaluate('(e)=>e.open=true');page.locator('#seriesMode').select_option('off');page.locator('#seriesSaveBtn').click()
  check('Disabling series preserves score records',page.evaluate('qa.captureState().sessions[0].players[0].scores[0]')==100 and page.evaluate('qa.getSeriesRules("m1")') is None)
  page.evaluate('async s=>{await qa.applyRestorePayload(qa.parseRestorePayload(s),"replace");qa.selectLiveMeetup("m1",false)}',backup)
  check('Replacement backup restores rules and membership',page.evaluate('qa.getSeriesRules("m1").teams[0].ids')==['p0','p2'])
  check('Cloud payload excludes series settings','seriesRules' not in page.evaluate('JSON.stringify(qa.buildRoomPayload("m1"))'))
  page.locator('#seriesSettings').evaluate('(e)=>e.open=true');page.locator('#seriesMode').select_option('avg');page.locator('#seriesRounds').select_option('1');page.locator('#seriesSaveBtn').click()
  public=fixture();public['sessions'][0]['players']=public['sessions'][0]['players'][:2];public['sessions'][0]['players'][0]['scores']=[10,None,None,None,None,None];public['sessions'][0]['players'][1]['scores']=[20,None,None,None,None,None]
  page.evaluate('s=>qa.publish(s)',public)
  check('Public series uses remote scores only',page.evaluate('qa.publicSeriesResult("m1").rows.map(x=>x.total)')==[20,10])
  page.evaluate('qa.renderLeaderboard("m1")')
  check('Public leaderboard excludes private-only player','志強' not in page.locator('#publicSeriesResults').inner_text())
  page.evaluate("qa.switchView('shareView');qa.renderShareOptions('m1');document.getElementById('shareCardType').value='series';window.texts=[];window.realFill=CanvasRenderingContext2D.prototype.fillText;CanvasRenderingContext2D.prototype.fillText=function(t,...args){texts.push(String(t));return realFill.call(this,t,...args)};qa.drawShareCard()")
  check('Series card only draws published scores',page.evaluate('texts.includes("20")&&!texts.includes("200")&&!texts.includes("志強")'))
  page.locator('#shareCanvas').screenshot(path=str(a.out/f'series-card-{a.browser}.png'))
  page.evaluate("qa.setPublicRecordState('s1','removed');window.texts=[];qa.drawShareCard()")
  check('Unpublish removes series output',page.evaluate('!qa.publicSeriesResult("m1").configured&&!texts.includes("小華")'))
  page.evaluate("qa.switchView('meetupView');qa.viewer()")
  check('Viewer cannot alter series',page.locator('#seriesSaveBtn').is_disabled())
  page.evaluate('qa.setSyncConfig({enabled:false});qa.renderLive()');page.locator('#seriesSettings').evaluate('(e)=>e.open=true')
  before=page.evaluate('JSON.stringify(qa.getSeriesRules("m1"))')
  page.evaluate("()=>{window.realSet=Storage.prototype.setItem;Storage.prototype.setItem=function(k,v){if(k===qa.keys.LIVEKEY)throw new DOMException('synthetic quota','QuotaExceededError');return realSet.call(this,k,v)}}")
  page.locator('#seriesMode').select_option('total');page.locator('#seriesSaveBtn').click()
  check('Quota failure rejects settings and warns',before==page.evaluate('JSON.stringify(qa.getSeriesRules("m1"))') and '未保存' in page.locator('#seriesStatus').inner_text())
  page.evaluate('()=>{Storage.prototype.setItem=window.realSet}');page.evaluate('qa.clearCompletedMeetupContext("m1");qa.selectLiveMeetup("m1",false)')
  check('Completed meetup retains series rules',page.evaluate('qa.getSeriesRules("m1").mode')=='avg')
  for width in [320,390,1440]:
   page.set_viewport_size({'width':width,'height':900});page.locator('.series-panel').scroll_into_view_if_needed();page.screenshot(path=str(a.out/f'series-{a.browser}-{width}.png'))
   check(f'{width}px series no page overflow',page.evaluate('document.documentElement.scrollWidth<=innerWidth'))
  page.close();page=ctx.new_page();page.goto(url);page.evaluate('()=>window.boot')
  check('Reopen tab retains rules',page.evaluate('qa.getSeriesRules("m1").mode')=='avg')
  ctx.close();browser.close()

except Exception as e:
 errors.append('HARNESS: '+repr(e))
finally:
 server.shutdown()
 result=dict(suite='v0.4.8-dev.2 series native UI',browser=a.browser,source_sha256=hashlib.sha256(original.encode()).hexdigest(),checks=checks,errors=errors)
 result['passed']=sum(x['status']=='PASS' for x in checks);result['failed']=sum(x['status']=='FAIL' for x in checks);result['harness_errors']=len(errors)
 (a.out/f'series-{a.browser}.json').write_text(json.dumps(result,ensure_ascii=False,indent=2));print(json.dumps(result,ensure_ascii=False));sys.exit(2 if errors else 1 if result['failed'] else 0)
