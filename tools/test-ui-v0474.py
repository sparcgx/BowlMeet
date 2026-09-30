"""Offline Chromium presentation regression. Native IDB, SW and cloud are NOT tested.
Usage: python tools/test-ui-v0474.py PATH_TO_APP OUTPUT_DIR
Requires playwright; BROWSER_EXECUTABLE may select installed Chromium.
"""
import base64,json,os,re,shutil,sys,statistics
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(sys.argv[1] if len(sys.argv)>1 else '.')
OUT=Path(sys.argv[2] if len(sys.argv)>2 else 'test-results/ui');OUT.mkdir(parents=True,exist_ok=True)
HOOKS="""
window.__audit={applyThemePreferences,applyLayoutPreferences,renderAll,renderHistory,renderRoster,renderStats,renderHistoryMode,validateSheet,renderScoreRows,publicHistoryRecords,publicGames,shareScopeData,renderShareOptions,switchView,saveDraft,loadDraft,
 setFixture:(data)=>{sessions=data.sessions||[];meetups=data.meetups||[];roster=data.roster||[];groupRemote=data.public||{sessions:[],meetups:[]};currentMeetupId=data.current||'';},
 snapshot:()=>JSON.stringify({sessions,meetups,roster}),
 benchmark:(n=7)=>{const r=[];for(let i=0;i<n;i++){const t=performance.now();renderAll();r.push(performance.now()-t)}return r}
};
"""
def source():
 text=(ROOT/'index.html').read_text()
 for match in list(re.finditer(r'<link rel="stylesheet" href="([^"]+)"[^>]*>',text)):
  relative=match[1].split('?')[0].removeprefix('./');text=text.replace(match[0],'<style data-source="'+relative+'">'+(ROOT/relative).read_text()+'</style>')
 text=re.sub(r'<script defer src="([^"]+)"></script>',lambda m:'<script>'+(ROOT/m[1].split('?')[0].removeprefix('./')).read_text()+'</script>',text)
 text=re.sub(r'(src|href)="\./icons/([^"?]+)(?:\?[^"]*)?"',lambda m:m[1]+'="data:image/'+('svg+xml' if m[2].endswith('.svg') else 'png')+';base64,'+base64.b64encode((ROOT/'icons'/m[2]).read_bytes()).decode()+'"',text)
 storage="""<script>const mockStore=new Map();Object.defineProperty(window,'localStorage',{value:{getItem:k=>mockStore.get(k)??null,setItem:(k,v)=>mockStore.set(k,String(v)),removeItem:k=>mockStore.delete(k),clear:()=>mockStore.clear(),key:i=>[...mockStore.keys()][i]??null,get length(){return mockStore.size}}});</script>"""
 text=text.replace('<head>','<head>'+storage)
 marker="$('date').value=today();$('meetupDate').value=today();load();"
 assert marker in text
 return text.replace(marker,HOOKS+'\n'+marker)
def fixture(n=100):
 ss=[];ms=[]
 for i in range(n):
  mid='qa-m-'+str(i);sid='qa-s-'+str(i);date=f'2026-09-{i%28+1:02}'
  ss.append(dict(id=sid,meetupId=mid,date=date,venue='QA',lane='1',players=[dict(id=f'qa-p-{j}',name=f'測試球員{j+1}',scores=[100+(i+j+k)%90 for k in range(6)],updatedAt=1) for j in range(8)],createdAt=i+1,updatedAt=i+1))
  ms.append(dict(id=mid,title='QA '+str(i),sessionId=sid,date=date,venue='QA',lanes='1',plannedGames=6,status='done',participantNames=[f'測試球員{j+1}' for j in range(8)],participantIds=[],createdAt=i+1,updatedAt=i+1))
 return dict(sessions=ss,meetups=ms,roster=[],public={'sessions':[],'meetups':[]})
checks=[];metrics={};errors=[]
def check(name,ok,detail=None):checks.append(dict(name=name,status='PASS' if ok else 'FAIL',**({'detail':detail} if detail is not None else {})))
with sync_playwright() as pw:
 exe=os.environ.get('BROWSER_EXECUTABLE') or shutil.which('chromium')
 browser=pw.chromium.launch(**({'executable_path':exe} if exe else {}),headless=True,args=['--no-sandbox'])
 for width,height in [(320,740),(390,844),(430,932),(768,1000),(1440,1000)]:
  ctx=browser.new_context(viewport={'width':width,'height':height},is_mobile=width<=680,has_touch=width<=680,service_workers='block',locale='zh-TW')
  ctx.route('**/*',lambda r:r.abort())
  page=ctx.new_page();page.on('pageerror',lambda e:errors.append(str(e)));page.set_content(source(),wait_until='load');page.wait_for_timeout(250)
  check(f'{width}: initialization',page.evaluate('typeof __audit')=='object')
  for theme in ['default','liquid-glass','clear-blue','soft-violet','dark-night','high-contrast']:
   page.evaluate('(theme)=>__audit.applyThemePreferences({theme,motionEnabled:true,transparencyEnabled:true})',theme);page.wait_for_timeout(250)
   props=page.evaluate('''()=>{const mob=innerWidth<=680,el=document.querySelector(mob?'.dock-item.active':'.tabs .tab.active'),c=getComputedStyle(el),header=document.querySelector('.topbar').getBoundingClientRect(),img=document.querySelector('.brand-icon');return {overflow:document.documentElement.scrollWidth>innerWidth,headerHeight:header.height,iconOK:img.complete&&img.naturalWidth===192,animation:c.animationName,duration:c.animationDuration,radius:c.borderRadius,itemBackdrop:c.backdropFilter,dockPosition:getComputedStyle(document.querySelector('.mobile-glass-dock')).position,targets:[...document.querySelectorAll(mob?'.mobile-glass-dock .dock-item':'.tabs .tab')].map(x=>x.getBoundingClientRect().height)}}''')
   tag=f'{width}/{theme}'
   check(tag+': no horizontal overflow',not props['overflow'])
   check(tag+': verified 192px icon loaded',props['iconOK'])
   check(tag+': targets >=44px',all(h>=43.9 for h in props['targets']))
   check(tag+': approved motion timing',props['animation']=='none' if theme=='high-contrast' else props['duration']=='1s',props['animation'])
   check(tag+': no per-item backdrop filters',props['itemBackdrop']=='none')
   if width<=680:check(tag+': fixed mobile dock',props['dockPosition']=='fixed')
   if width in [390,1440] and theme in ['default','liquid-glass','dark-night']:page.screenshot(path=str(OUT/f'ui-{width}-{theme}.png'))
  active='.dock-item.active' if width<=680 else '.tabs .tab.active'
  page.evaluate("__audit.applyThemePreferences({theme:'default',motionEnabled:false,transparencyEnabled:true})");page.wait_for_timeout(250)
  check(f'{width}: Theme Motion Off stops animation',page.locator(active).evaluate('(e)=>getComputedStyle(e).animationName')=='none')
  page.evaluate("__audit.applyThemePreferences({theme:'dark-night',motionEnabled:true,transparencyEnabled:false})");page.wait_for_timeout(250)
  check(f'{width}: transparency off removes gradient',page.locator(active).evaluate('(e)=>getComputedStyle(e).backgroundImage')=='none')
  check(f'{width}: transparency off is opaque',page.locator(active).evaluate('(e)=>getComputedStyle(e).backgroundColor').startswith('rgb('))
  page.evaluate("__audit.applyThemePreferences({theme:'default',motionEnabled:true,transparencyEnabled:true})");page.emulate_media(reduced_motion='reduce');page.wait_for_timeout(100)
  check(f'{width}: OS reduced motion stops animation',page.locator(active).evaluate('(e)=>getComputedStyle(e).animationName')=='none');page.emulate_media(reduced_motion='no-preference')
  page.evaluate("window.dispatchEvent(new Event('pagehide'))")
  check(f'{width}: pagehide pauses motion',page.locator(active).evaluate('(e)=>getComputedStyle(e).animationPlayState')=='paused')
  page.evaluate("window.dispatchEvent(new Event('pageshow'))")
  check(f'{width}: pageshow resumes motion',page.locator(active).evaluate('(e)=>getComputedStyle(e).animationPlayState')=='running')
  page.emulate_media(forced_colors='active');page.wait_for_timeout(200)
  check(f'{width}: forced-colors stops motion',page.locator(active).evaluate('(e)=>getComputedStyle(e).animationName')=='none');page.emulate_media(forced_colors='none')
  # Exercise actual navigation event handlers, not just CSS selectors.
  if width<=680:
   page.locator('[data-dock-view="scoreView"]').first.click();check(f'{width}: dock score navigation',page.locator('#scoreView').evaluate('(e)=>e.classList.contains("active")'))
   page.locator('[data-dock-view="historyView"]').first.click();check(f'{width}: dock history navigation',page.locator('#historyView').evaluate('(e)=>e.classList.contains("active")'))
   page.locator('#mobileDockMoreBtn').click();check(f'{width}: More sheet opens',page.locator('#mobileMoreSheet').evaluate('(e)=>e.classList.contains("open")'))
   page.locator('.mobile-more-item[data-dock-view="syncView"]').click();check(f'{width}: More to settings',page.locator('#syncView').evaluate('(e)=>e.classList.contains("active")'))
  else:
   page.locator('.tabs [data-view="scoreView"]').click();check(f'{width}: desktop score navigation',page.locator('#scoreView').evaluate('(e)=>e.classList.contains("active")'))
  page.evaluate("__audit.switchView('scoreView');__audit.renderScoreRows([{id:'input-qa',name:'QA',scores:[100,null,null,null,null,null]}])")
  for bad in ['301','-1','12.5']:
   page.locator('.score-in').nth(1).fill(bad)
   r=page.evaluate('__audit.validateSheet()');check(f'{width}: rejects invalid score {bad}',not r['ok'])
  page.locator('.score-in').nth(1).fill('0');check(f'{width}: valid zero accepted',page.evaluate('__audit.validateSheet().ok'))
  if width==1440:
   fx=fixture(100);page.evaluate('(d)=>__audit.setFixture(d)',fx);page.evaluate("__audit.switchView('meetupView')")
   before=page.evaluate('__audit.snapshot()');metrics['renderAll100x8_ms']=page.evaluate('__audit.benchmark(7)');metrics['nodes_before_history']=page.locator('*').count()
   check('Synthetic refresh does not alter score/meetup/roster data',before==page.evaluate('__audit.snapshot()'))
   page.evaluate("__audit.switchView('historyView')");check('History renders all 100 sessions on entry',page.locator('#sessionList .session').count()==100)
   fx['public']={'sessions':[fx['sessions'][0]],'meetups':[fx['meetups'][0]],'recordControls':[]};page.evaluate('(d)=>__audit.setFixture(d)',fx)
   check('Public-only source excludes 99 unpublished sessions',page.evaluate('__audit.publicHistoryRecords().length')==1)
   page.evaluate("__audit.renderShareOptions('all')");check('Share uses public-only 48 scores',page.evaluate('__audit.shareScopeData().vals.length')==48)
   fx['public']['recordControls']=[{'id':'qa-s-0','state':'removed','updatedAt':99999}];page.evaluate('(d)=>__audit.setFixture(d)',fx)
   check('Tombstone removes cancelled public results',page.evaluate('__audit.publicHistoryRecords().length')==0)
  ctx.close()
 browser.close()
check('No unhandled page errors in exercised routes',not errors,errors)
result={'environment':'Chromium Linux; offline inlined source/assets; mock localStorage; no real cloud or native PWA/IndexedDB','checks':checks,'passed':sum(c['status']=='PASS' for c in checks),'failed':sum(c['status']=='FAIL' for c in checks),'metrics':metrics}
(OUT/'ui-results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2));print(json.dumps(result,ensure_ascii=False,indent=2));sys.exit(bool(result['failed']))
