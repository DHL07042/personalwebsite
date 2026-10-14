/* Progressive enhancement: links and video players work without this file. */
(function(){'use strict';
 const root=document.documentElement,sel=document.getElementById('theme-select');
 const mq=window.matchMedia('(prefers-color-scheme: dark)'), key='dhl-portfolio-theme-v1';
 let pref=['light','dark','system'].includes(root.dataset.themePreference)?root.dataset.themePreference:'light';
 function apply(){root.dataset.themePreference=pref;root.dataset.theme=pref==='system'?(mq.matches?'dark':'light'):pref;if(sel)sel.value=pref;}
 if(sel)sel.addEventListener('change',()=>{pref=sel.value;try{localStorage.setItem(key,pref);}catch(e){}apply();});
 const onSystem=()=>{if(pref==='system')apply();};if(mq.addEventListener)mq.addEventListener('change',onSystem);else mq.addListener(onSystem);
 window.addEventListener('storage',e=>{if(e.key===key){pref=['light','dark','system'].includes(e.newValue)?e.newValue:'light';apply();}});
 const nav=document.getElementById('site-nav'),button=document.querySelector('.menu-toggle');
 function close(focus){if(nav)nav.dataset.open='false';if(button){button.setAttribute('aria-expanded','false');if(focus)button.focus();}}
 if(button&&nav){button.addEventListener('click',()=>{const open=nav.dataset.open!=='true';nav.dataset.open=String(open);button.setAttribute('aria-expanded',String(open));});nav.querySelectorAll('a').forEach(a=>a.addEventListener('click',()=>close(false)));document.addEventListener('keydown',e=>{if(e.key==='Escape'&&nav.dataset.open==='true')close(true);});document.addEventListener('click',e=>{if(!e.target.closest('.header-controls'))close(false);});}
 const copy=document.querySelector('[data-copy]'),status=document.getElementById('copy-status');
 if(copy)copy.addEventListener('click',async()=>{try{if(!navigator.clipboard)throw Error('Unavailable');await navigator.clipboard.writeText(copy.dataset.copy);status.textContent='Email address copied.';}catch(e){status.textContent=copy.dataset.copy;}});
 apply();root.classList.add('js');
})();
