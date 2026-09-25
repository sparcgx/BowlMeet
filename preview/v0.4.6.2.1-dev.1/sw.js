const PREVIEW_CACHE_ROOT='bowlmeet-preview-v04621d1-';
const CACHE=PREVIEW_CACHE_ROOT+'gridfix-shell';
const RUNTIME=PREVIEW_CACHE_ROOT+'gridfix-runtime';
const APP_SHELL=['./','./index.html','./manifest.webmanifest','./assets/liquid-glass-dev4.css?v=04621d1','../../icons/icon-192.png','../../icons/icon-512.png','../../icons/icon-maskable-512.png'];

self.addEventListener('install',event=>{event.waitUntil(caches.open(CACHE).then(cache=>cache.addAll(APP_SHELL)))});

self.addEventListener('activate',event=>{event.waitUntil(
  caches.keys()
    .then(keys=>Promise.all(keys.filter(k=>k.startsWith(PREVIEW_CACHE_ROOT)&&k!==CACHE&&k!==RUNTIME).map(k=>caches.delete(k))))
    .then(()=>self.clients.claim())
)});

async function matchPreviewCache(request){
  const runtime=await caches.open(RUNTIME);
  const runtimeHit=await runtime.match(request);
  if(runtimeHit)return runtimeHit;
  const shell=await caches.open(CACHE);
  return shell.match(request);
}

self.addEventListener('fetch',event=>{
  const req=event.request;
  if(req.method!=='GET')return;
  const url=new URL(req.url);

  if(req.mode==='navigate'){
    event.respondWith(
      fetch(req)
        .then(res=>{const copy=res.clone();caches.open(RUNTIME).then(c=>c.put(req,copy));return res})
        .catch(async()=>await matchPreviewCache(req)||await matchPreviewCache('./index.html'))
    );
    return;
  }

  event.respondWith((async()=>{
    const cached=await matchPreviewCache(req);
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
