const PREVIEW_CACHE_ROOT='bowlmeet-preview-v0462d1r1-';
const PREVIEW_CACHE_PREFIX=PREVIEW_CACHE_ROOT+'fix1-';
const CACHE=PREVIEW_CACHE_PREFIX+'shell';
const RUNTIME=PREVIEW_CACHE_PREFIX+'runtime';
const APP_SHELL=['./','./index.html','./manifest.webmanifest','./assets/liquid-glass-dev4.css','../../icons/icon-192.png','../../icons/icon-512.png','../../icons/icon-maskable-512.png'];

self.addEventListener('install',e=>e.waitUntil(caches.open(CACHE).then(c=>c.addAll(APP_SHELL))));

self.addEventListener('activate',e=>e.waitUntil(
  caches.keys()
    .then(keys=>Promise.all(keys.filter(k=>k.startsWith(PREVIEW_CACHE_ROOT)&&k!==CACHE&&k!==RUNTIME).map(k=>caches.delete(k))))
    .then(()=>self.clients.claim())
));

self.addEventListener('message',e=>{if(e.data&&e.data.type==='SKIP_WAITING')self.skipWaiting()});

async function matchPreviewCache(request){
  const runtime=await caches.open(RUNTIME);
  const runtimeHit=await runtime.match(request);
  if(runtimeHit)return runtimeHit;
  const shell=await caches.open(CACHE);
  return shell.match(request);
}

self.addEventListener('fetch',e=>{
  const r=e.request;
  if(r.method!=='GET')return;
  const u=new URL(r.url);

  if(r.mode==='navigate'){
    e.respondWith(
      fetch(r)
        .then(res=>{const x=res.clone();caches.open(RUNTIME).then(c=>c.put(r,x));return res})
        .catch(async()=>await matchPreviewCache(r)||await matchPreviewCache('./index.html'))
    );
    return;
  }

  if(u.origin===self.location.origin){
    e.respondWith((async()=>{
      const cached=await matchPreviewCache(r);
      const fresh=fetch(r)
        .then(res=>{const x=res.clone();caches.open(RUNTIME).then(c=>c.put(r,x));return res})
        .catch(()=>cached);
      return cached||fresh;
    })());
  }
});
