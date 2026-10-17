(function(){
  'use strict';
  var root=document.documentElement,KEY='dhl-portfolio-theme-v1';
  var VALID=['light','dark','system'];

  /* Theme */
  var pref=root.getAttribute('data-theme-preference');
  if(VALID.indexOf(pref)===-1)pref='system';
  var buttons=Array.prototype.slice.call(document.querySelectorAll('.theme-control button[data-theme-value]'));
  function apply(){
    root.setAttribute('data-theme-preference',pref);
    if(pref==='system')root.removeAttribute('data-theme');else root.setAttribute('data-theme',pref);
    buttons.forEach(function(b){b.setAttribute('aria-pressed',String(b.getAttribute('data-theme-value')===pref));});
  }
  buttons.forEach(function(b){
    b.addEventListener('click',function(){
      pref=b.getAttribute('data-theme-value');
      try{localStorage.setItem(KEY,pref);}catch(e){}
      apply();
    });
  });
  window.addEventListener('storage',function(e){
    if(e.key===KEY){pref=VALID.indexOf(e.newValue)!==-1?e.newValue:'system';apply();}
  });
  apply();

  /* Mobile menu */
  var nav=document.getElementById('site-nav'),toggle=document.querySelector('.menu-toggle');
  function setOpen(open){
    if(!nav||!toggle)return;
    nav.setAttribute('data-open',String(open));
    toggle.setAttribute('aria-expanded',String(open));
  }
  if(nav&&toggle){
    toggle.addEventListener('click',function(){setOpen(nav.getAttribute('data-open')!=='true');});
    document.addEventListener('keydown',function(e){if(e.key==='Escape'&&nav.getAttribute('data-open')==='true'){setOpen(false);toggle.focus();}});
    document.addEventListener('click',function(e){if(!e.target.closest('.header-controls'))setOpen(false);});
    window.addEventListener('resize',function(){if(window.innerWidth>880)setOpen(false);});
  }

  /* Click-to-play video: the player is created only when the viewer asks for it. */
  Array.prototype.forEach.call(document.querySelectorAll('.yt[data-id]'),function(box){
    var link=box.querySelector('a');
    if(!link)return;
    link.addEventListener('click',function(e){
      if(e.metaKey||e.ctrlKey||e.shiftKey||e.altKey||e.button!==0)return;
      e.preventDefault();
      var id=box.getAttribute('data-id'),title=box.getAttribute('data-title')||'Video';
      var f=document.createElement('iframe');
      f.src='https://www.youtube-nocookie.com/embed/'+encodeURIComponent(id)+'?autoplay=1&playsinline=1&rel=0';
      f.title=title;
      f.allow='autoplay; encrypted-media; picture-in-picture; fullscreen';
      f.setAttribute('allowfullscreen','');
      f.setAttribute('referrerpolicy','strict-origin-when-cross-origin');
      box.innerHTML='';
      box.appendChild(f);
    });
  });

  /* Copy buttons */
  Array.prototype.forEach.call(document.querySelectorAll('[data-copy]'),function(btn){
    var status=document.getElementById(btn.getAttribute('aria-describedby')||'')||null;
    var label=btn.textContent;
    function say(t){if(status)status.textContent=t;}
    btn.addEventListener('click',function(){
      var text=btn.getAttribute('data-copy');
      function done(){btn.textContent='Copied';say('Email address copied.');setTimeout(function(){btn.textContent=label;say('');},1800);}
      function fail(){say(text);}
      if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(text).then(done,fail);}else{fail();}
    });
  });

  /* Lightbox: click a figure to view it large; click anywhere or press Escape to close.
     Right-click on the enlarged image still offers "open image in new tab". */
  var lb=document.getElementById('lightbox');
  if(lb){
    var lbImg=lb.querySelector('img'),lbCap=lb.querySelector('figcaption'),lastFocus=null;
    var background=[];
    function openLb(src,alt,cap){
      lastFocus=document.activeElement;lbImg.src=src;lbImg.alt=alt||'';lbCap.textContent=cap||'';
      background=Array.prototype.filter.call(document.body.children,function(el){return el!==lb&&el.tagName!=='SCRIPT';}).map(function(el){var was=el.inert;el.inert=true;return {el:el,was:was};});
      lb.hidden=false;document.body.classList.add('lb-open');lb.querySelector('.lb-close').focus();
    }
    function closeLb(){
      if(lb.hidden)return;
      lb.hidden=true;document.body.classList.remove('lb-open');lbImg.removeAttribute('src');lb.classList.remove('photography-view');
      background.forEach(function(item){item.el.inert=item.was;});background=[];
      if(lastFocus&&lastFocus.focus)lastFocus.focus();
    }
    lb.addEventListener('keydown',function(e){
      if(e.key==='Tab'){e.preventDefault();lb.querySelector('.lb-close').focus();}
    });
    Array.prototype.forEach.call(document.querySelectorAll('a[data-lightbox]'),function(a){
      a.addEventListener('click',function(e){
        if(e.metaKey||e.ctrlKey||e.shiftKey||e.button!==0)return;
        e.preventDefault();
        var img=a.querySelector('img'),fig=a.closest('figure'),cap=fig?fig.querySelector('figcaption'):null;
        lb.classList.toggle('photography-view',!!a.closest('.photography-gallery'));
        openLb(a.getAttribute('href'),img?img.alt:'',cap?cap.textContent:'');
      });
    });
    lb.addEventListener('click',function(){closeLb();});
    document.addEventListener('keydown',function(e){if(e.key==='Escape'&&!lb.hidden)closeLb();});
  }

  /* Respect reduced motion for the looping clip. */
  if(window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches){
    Array.prototype.forEach.call(document.querySelectorAll('video[autoplay]'),function(v){v.removeAttribute('autoplay');v.pause();v.setAttribute('controls','');});
  }

  root.classList.add('js');
})();
