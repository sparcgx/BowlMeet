/* v0.4.7.4-dev.1 | Versioned shell; never cache cloud APIs or other previews. */
const PRODUCTION_CACHE_ROOT='bowlmeet-preview-v0474d1-';
const CACHE='bowlmeet-preview-v0474d1-shell';
const RUNTIME='bowlmeet-preview-v0474d1-runtime';
const APP_SHELL=['./','./index.html','./manifest.webmanifest?v=0474d1','./assets/liquid-glass-dev4.css?v=0474d1','./assets/theme-center-v0470.css?v=0474d1','./assets/theme-center-v0470-mobile.css?v=0474d1','./assets/theme-center-v0470-accessibility.css?v=0474d1','./assets/liquid-motion-v0470.css?v=0474d1','./assets/score-card-v0471.css?v=0474d1','./assets/score-card-mobile-v0471.css?v=0474d1','./assets/score-card-accessibility-v0471.css?v=0474d1','./assets/rc-mobile-repair-v0471.css?v=0474d1','./assets/ui-hardening-v0474.css?v=0474d1','./assets/ui-lifecycle-v0474.js?v=0474d1','./icons/icon-192.png?v=0474d1','./icons/icon-512.svg?v=0474d1','./icons/icon-maskable-512.svg?v=0474d1'];
const SCOPE=new URL(self.registration.scope);
const INDEX_URL=new URL('./index.html',SCOPE).href;
const ASSET_URLS=new Set(APP_SHELL.slice(2).map(p=>new URL(p,SCOPE).href));
const RUNTIME_LIMIT=40;
self.addEventListener('install',event=>{
  event.waitUntil(caches.open(CACHE).then(cache=>cache.addAll(APP_SHELL)));
});
// Preserve explicit update / optional backup confirmation; never auto-skip waiting.
self.addEventListener('message',event=>{if(event.data?.type==='SKIP_WAITING')self.skipWaiting();});
self.addEventListener('activate',event=>{event.waitUntil(
  caches.keys().then(keys=>Promise.all(keys.filter(k=>k.startsWith(PRODUCTION_CACHE_ROOT)&&k!==CACHE&&k!==RUNTIME).map(k=>caches.delete(k))))
    .then(()=>self.clients.claim())
);});
async function cached(request){
  try{
    const runtime=await caches.open(RUNTIME),hit=await runtime.match(request);
    if(hit)return hit;
    return (await caches.open(CACHE)).match(request);
  }catch{return undefined;}
}
async function remember(request,response){
  if(!response?.ok||response.type==='opaque')return;
  try{
    const runtime=await caches.open(RUNTIME);
    await runtime.put(request,response.clone());
    const keys=await runtime.keys();
    await Promise.all(keys.slice(0,Math.max(0,keys.length-RUNTIME_LIMIT)).map(key=>runtime.delete(key)));
  }catch{/* Cache quota/write errors must not hide a valid network response. */}
}
function offline(){return new Response('離線且尚無此版本快取，請連線後再開啟 BowlMeet。',{status:503,headers:{'Content-Type':'text/plain; charset=utf-8'}});}
self.addEventListener('fetch',event=>{
  const req=event.request,url=new URL(req.url);
  if(req.method!=='GET'||url.origin!==SCOPE.origin||!url.pathname.startsWith(SCOPE.pathname))return;
  if(req.headers.has('authorization')||req.headers.has('apikey'))return;
  const appNavigation=req.mode==='navigate'&&(url.pathname===SCOPE.pathname||url.href.split('?')[0]===INDEX_URL);
  // Versioned assets are immutable within this shell. Other paths (including
  // /preview/, API calls, downloads and test pages) bypass this worker entirely.
  if(!appNavigation&&!ASSET_URLS.has(url.href))return;
  event.respondWith((async()=>{
    if(appNavigation){
      try{
        const res=await fetch(req);
        if(res.ok){await remember(INDEX_URL,res);return res;}
        return await cached(INDEX_URL)||res;
      }catch{return await cached(INDEX_URL)||offline();}
    }
    const hit=await cached(req);if(hit)return hit;
    try{const res=await fetch(req);await remember(req,res);return res;}
    catch{return offline();}
  })());
});
