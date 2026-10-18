#!/usr/bin/env python3
"""Synthetic localhost native-storage lane UI regression. No real cloud or iPhone."""
import argparse,http.server,threading,json,re,hashlib,sys
from pathlib import Path
from playwright.sync_api import sync_playwright
p=argparse.ArgumentParser();p.add_argument('root',type=Path);p.add_argument('out',type=Path);p.add_argument('--browser',default='chromium');a=p.parse_args();root=a.root.resolve();a.out.mkdir(parents=True,exist_ok=True)
source=(root/'index.html').read_text();original=source
source=re.sub(r"const BUILTIN_SUPABASE_URL='[^']*';","const BUILTIN_SUPABASE_URL='';",source);source=re.sub(r"const BUILTIN_SUPABASE_PUBLISHABLE_KEY='[^']*';","const BUILTIN_SUPABASE_PUBLISHABLE_KEY='';",source);source=source.replace('const BUILTIN_CLOUD=true;','const BUILTIN_CLOUD=false;')
bridge="""window.qa={applyState,persistDbStateNow,openPlayerHub,openPlayerAnalytics,openPlayerHistory,openPlayerSessionDetail,playerCareerGames,resolveGameDetail,openGameDetail,playerProgress,setPublicRecordState,publish:s=>{groupRemote={schema:2,sessions:s,meetups:[],recordControls:[],updatedAt:100}}};
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
  ctx=browser.new_context(viewport={'width':390,'height':844},service_workers='block');ctx.route('**/*',lambda r:r.continue_() if r.request.url.startswith(url) else r.abort());page=ctx.new_page();page.on('pageerror',lambda e:errors.append(str(e)))
  page.goto(url);page.evaluate('()=>window.boot')
  data=fixture();player=data['sessions'][0]['players'][0];player['scores']=[300,0,120,100,None,None];player['bowlingFrames']=[[dict(rolls=[10,None] if i<9 else [10,10,10]) for i in range(10)],[dict(rolls=[0,0] if i<9 else [0,0,None]) for i in range(10)],[],[dict(rolls=[7,None])]]
  page.evaluate('async s=>{qa.applyState(s);await qa.persistDbStateNow("qa");qa.openPlayerHub("阿明")}',data)
  check('Hub progress sample visible','樣本 4/10' in page.locator('#hubProgress').inner_text())
  check('Insufficient data labelled','待累積 20 局' in page.locator('#hubProgress').inner_text())
  page.evaluate('qa.openPlayerAnalytics("阿明")')
  check('Analytics progress integrated',page.locator('#analyticsProgress').is_visible())
  page.locator('#playerHistoryBody [data-game-detail]').filter(has_text='300').click()
  check('Score opens readonly dialog',page.locator('#gameDetailDialog').is_visible() and page.locator('#gameDetailDialog input').count()==0)
  check('Ten frames rendered',page.locator('#gameDetailContent thead th').count()==11)
  check('Tenth bonus rolls visible',page.locator('#gameDetailContent tbody tr').nth(1).locator('td').last.inner_text()=='10 · 10 · 10')
  check('Perfect cumulative total',page.locator('#gameDetailContent tbody tr').last.locator('td').last.inner_text()=='300')
  for width in [320,390,1440]:
   page.set_viewport_size({'width':width,'height':900});page.screenshot(path=str(a.out/f'progress-{a.browser}-{width}.png'))
   check(f'{width}px no page overflow',page.evaluate('document.documentElement.scrollWidth<=innerWidth'))
  page.keyboard.press('Escape');check('Escape returns focus',page.locator('#playerHistoryBody [data-game-detail]').filter(has_text='300').evaluate('(e)=>e===document.activeElement'))
  page.locator('#playerHistoryBody [data-game-detail]').filter(has_text='120').click();check('Total-only does not fabricate frames','只有總分' in page.locator('#gameDetailContent').inner_text() and page.locator('#gameDetailContent table').count()==0);page.locator('#gameDetailClose').click()
  page.locator('#playerHistoryBody [data-game-detail]').filter(has_text='100').click();check('Incomplete frames labelled','尚未完成' in page.locator('#gameDetailContent').inner_text());page.locator('#gameDetailClose').click()
  page.evaluate('qa.openGameDetail(qa.playerCareerGames("阿明").find(g=>g.score===0))');check('Zero game has full detail',page.locator('#gameDetailContent table').count()==1);page.locator('#gameDetailClose').click()
  page.evaluate('qa.openPlayerHistory()');page.locator('#playerHistoryList [data-game-detail]').first.click();check('Player history chips open detail',page.locator('#gameDetailDialog').is_visible());page.locator('#gameDetailClose').click()
  page.locator('#playerHistoryList [data-player-session]').first.click();page.locator('#playerSessionScores [data-game-detail]').first.click();check('Session detail nested dialog opens',page.locator('#gameDetailDialog').is_visible());page.locator('#gameDetailClose').click();check('Closing nested detail preserves session',page.locator('#playerSessionDialog').is_visible());page.locator('#playerSessionCloseBtn').click()
  remote=dict(id='remote',date='2026-10-18',players=[dict(id='rp',name='公開測試',scores=[88],bowlingFrames=[])],createdAt=200)
  page.evaluate('s=>qa.publish([s])',remote);page.evaluate('qa.openPlayerAnalytics("公開測試")');page.locator('#playerHistoryBody [data-game-detail]').click();check('Public-only score has no fabricated local detail','只有總分' in page.locator('#gameDetailContent').inner_text() and '88' in page.locator('#gameDetailTitle').inner_text());page.locator('#gameDetailClose').click()
  check('Removed public result rejected',page.evaluate('()=>{const g=qa.playerCareerGames("公開測試")[0];qa.setPublicRecordState("remote","removed");return qa.resolveGameDetail(g).reason.includes("不存在")}'))
  data['sessions'][0]['players'][0]['scores'][0]=299
  page.evaluate('s=>{qa.applyState(s);qa.openPlayerAnalytics("阿明");qa.openGameDetail(qa.playerCareerGames("阿明")[0])}',data)
  check('Mismatch is not shown as valid frame data','不一致' in page.locator('#gameDetailContent').inner_text())
  ctx.close();browser.close()
except Exception as e:errors.append('HARNESS: '+repr(e))
finally:
 server.shutdown()
 result=dict(suite='v0.4.8-dev.3 progress and detail native UI',browser=a.browser,source_sha256=hashlib.sha256(original.encode()).hexdigest(),checks=checks,errors=errors)
 result['passed']=sum(x['status']=='PASS' for x in checks);result['failed']=sum(x['status']=='FAIL' for x in checks);result['harness_errors']=len(errors)
 (a.out/f'progress-{a.browser}.json').write_text(json.dumps(result,ensure_ascii=False,indent=2));print(json.dumps(result,ensure_ascii=False));sys.exit(2 if errors else 1 if result['failed'] else 0)
