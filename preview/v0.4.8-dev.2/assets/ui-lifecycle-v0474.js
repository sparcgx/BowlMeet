/* Pause decorative UI only. Never changes storage, polling, or data lifecycle. */
(()=>{
 'use strict';
 const root=document.documentElement;
 const pause=()=>{root.dataset.uiPaused=document.hidden?'true':'false';};
 document.addEventListener('visibilitychange',pause,{passive:true});
 window.addEventListener('pagehide',()=>{root.dataset.uiPaused='true';},{passive:true});
 window.addEventListener('pageshow',pause,{passive:true});
 pause();
})();
