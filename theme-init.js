(function(){
  'use strict';
  var root=document.documentElement,pref='system';
  try{var s=localStorage.getItem('dhl-portfolio-theme-v1');if(s==='light'||s==='dark'||s==='system')pref=s;}catch(e){}
  root.setAttribute('data-theme-preference',pref);
  if(pref==='system')root.removeAttribute('data-theme');else root.setAttribute('data-theme',pref);
})();
