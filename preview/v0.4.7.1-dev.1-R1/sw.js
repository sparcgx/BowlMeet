const PREVIEW_CACHE_ROOT='bowlmeet-preview-v0471d1r1-';
const CACHE='bowlmeet-preview-v0471d1r1-shell';
const RUNTIME='bowlmeet-preview-v0471d1r1-runtime';
const APP_SHELL=['./','./index.html','./manifest.webmanifest','../../assets/liquid-glass-dev4.css?v=0471d1r1','../../assets/theme-center-v0470.css?v=0471d1r1','../../assets/theme-center-v0470-mobile.css?v=0471d1r1','../../assets/theme-center-v0470-accessibility.css?v=0471d1r1','../../assets/liquid-motion-v0470.css?v=0471d1r1','../../icons/icon-192.png','../../icons/icon-512.png','../../icons/icon-maskable-512.png'];

self.addEventListener('install',event=>{event.waitUntil(caches.open(CACHE).then(cache=>cache.addAll(APP_SHELL)))});

self.addEventListener('message',event=>{if(event.data?.type==='SKIP_WAITING')self.skipWaiting()});

self.addEventListener('activate',event=>{event.waitUntil(
  caches.keys()
    .then(keys=>Promise.all(keys.filter(k=>k.startsWith(PREVIEW_CACHE_ROOT)&&k!==CACHE&&k!==RUNTIME).map(k=>caches.delete(k))))
    .then(()=>self.clients.claim())
)});

async function matchProductionCache(request){
  const runtime=await caches.open(RUNTIME);
  const runtimeHit=await runtime.match(request);
  if(runtimeHit)return runtimeHit;
  const shell=await caches.open(CACHE);
  return shell.match(request);
}

self.addEventListener('fetch',event=>{
  const req=event.request;
  if(req.method!=='GET')return;

  if(req.mode==='navigate'){
    event.respondWith(
      fetch(req)
        .then(res=>{const copy=res.clone();caches.open(RUNTIME).then(c=>c.put(req,copy));return res})
        .catch(async()=>await matchProductionCache(req)||await matchProductionCache('./index.html'))
    );
    return;
  }

  event.respondWith((async()=>{
    const cached=await matchProductionCache(req);
    const fresh=fetch(req)
      .then(res=>{
        if(res&&res.ok){
          const copy=res.clone();
          caches.open(RUNTIME).then(c=>c.put(req,copy));
        }
        return res;
      })
      .catch(()=>cached);
    return cached||fresh;
  })());
});