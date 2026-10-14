"""One-use preparation script; the branch preparation job removes this file."""
from pathlib import Path
import re, json
root=Path('.')
assert json.loads((root/'release.json').read_text())['release']=='2026-10-14.5'
release='2026-10-14.6'
bootstrap=(root/'theme-init.js').read_text().replace("  root.classList.add('js');\n",'')
(root/'theme-init.js').write_text(bootstrap)
for p in root.glob('*.html'):
    s=p.read_text().replace('2026-10-14.5',release)
    s=s.replace('<script src="theme-init.js?v='+release+'"></script>','<script id="theme-bootstrap">\n'+bootstrap+'</script>')
    p.write_text(s)
def change(name, old, new):
    p=root/name;s=p.read_text()
    if old not in s:raise ValueError('Expected source not found: '+name+' / '+old[:80])
    p.write_text(s.replace(old,new))
change('index.html','At KAIST’s Exo Lab, with Prof.&nbsp;Kyoungchul Kong, I built foot\u2060–\u2060ground distance and contact-force sensing hardware, integrated it into powered exoskeletons, and ran the experiments behind the publications on this site: how a robot can sense the ground before contact, manage the load at contact, and read the intention of the person wearing it. I received my B.S. (2020) and M.S. (2022) in mechanical engineering from KAIST.','At KAIST’s Exo Lab, I worked with Prof.&nbsp;Kyoungchul Kong on sensor development and experimental evaluation of powered exoskeletons. My contributions included distance- and force-sensing hardware, robot integration, and walking experiments. I received my B.S. (2020) and M.S. (2022) in mechanical engineering from KAIST.')
change('index.html','My interests are gait-phase estimation, contact-aware load modulation, and human-intention recognition, for wearable robots and for legged robots that face the same contact problems.','My research interests include gait-phase estimation, contact-aware load modulation, and human-intention recognition in wearable robots. I am also interested in sensing and control for legged locomotion.')
change('index.html','Three lines of work from KAIST, each with hardware I built and experiments I ran.','Selected projects in sensing, instrumentation, and robot integration.')
change('research.html','This work comes from my M.S. research at KAIST’s Exo Lab (2020–2023). Each project states what I did and what the study reported. Click a figure to enlarge it.','These projects originated in my graduate and post-master’s research at KAIST’s Exo Lab (2020–2023). Click a figure to enlarge it.')
change('research.html','Small time-of-flight (ToF) sensors on the foot measure the distance to the ground throughout the gait cycle. Unlike pressure sensors, they keep reporting during swing, so a robot can see contact coming instead of only registering it.','Time-of-flight (ToF) sensors measure foot\u2060–\u2060ground distance during walking. The distance signal remains available during swing, complementing pressure-based measurements during stance.')
change('research.html','at the outer heel and the fifth metatarsal head','near the lateral heel and the fifth metatarsophalangeal (MTP) joint')
change('research.html','Tested with one healthy participant walking on a flat indoor floor. The detected stance and swing phases matched the timing of pressure-based measurements, and the distance signal stayed informative through swing, where pressure sensors read zero.','Tested with one healthy participant walking on a flat indoor floor. Compared gait-phase estimates with pressure-based measurements and recorded foot\u2060–\u2060ground distance during swing [J1].')
p=root/'research.html';s=p.read_text()
s,n=re.subn(r'      <p class="aside-note">Along the way.*?</p>\n      <div class="media">.*?\n      </div>','',s,flags=re.S);assert n==1
s,n=re.subn(r'        <figure class="fig">\s*<a href="assets/img/grf-results.webp".*?</figure>\n','',s,flags=re.S);assert n==1
s=s.replace('It reanalyses the thesis data; it makes no clinical or stability claims.','It builds on the thesis experiments.')
s=s.replace('<figure class="fig cover">\n  <a href="assets/img/m20-module.webp"','<figure class="fig">\n  <a href="assets/img/m20-module.webp"')
s=s.replace('Walking model (a) and the joint-level response around ground contact in stance (b) and swing (c), from the thesis.','Thesis concept diagram: (a) walking model; (b) joint flexion and extension; (c) stance and swing configurations.')
s=s.replace('Schematic of a walking model and the joint-level assistance concept around ground contact in stance and swing','Thesis diagram showing a walking model, joint flexion and extension, and stance and swing configurations')
s=s.replace('built and instrumented a modified WalkON Suit&nbsp;4','fabricated components and instrumented a modified WalkON Suit&nbsp;4')
s=s.replace('An integrated measurement and analysis setup used across the projects above.','Measurement-system integration and analysis software for wearable-robot evaluation.')
s=s.replace('data-title="CYBATHLON 2020 Powered Exoskeleton Race"','data-title="CYBATHLON 2020 Global Edition - EXO Finals"')
s=s.replace('Play: CYBATHLON 2020 Powered Exoskeleton Race','Play: CYBATHLON 2020 Global Edition - EXO Finals')
s=s.replace('<strong>CYBATHLON 2020</strong> · Powered Exoskeleton Race broadcast','<strong>CYBATHLON 2020 Global Edition - EXO Finals</strong>')
p.write_text(s)
change('publications.html','Titles link to the publisher record. Each entry links back to the project it belongs to.','Published titles link to publisher records. Project links provide additional context for selected publications.')
change('personal.html','Travel photography and noraebang','Photography and music')
change('personal.html','I take photographs when I travel, and I sing and rap at noraebang, the Korean karaoke room.','Outside research, I enjoy travel photography, singing, and rapping.')
change('personal.html','<video autoplay muted loop playsinline','<video controls autoplay muted loop playsinline')
p=root/'styles.css';s=p.read_text().replace('2026-10-14.5',release)
s=s.replace('.facts dd span{display:block','.facts dd>span{display:block')
s=s.replace('.hero .lede{margin-top:1.6rem;max-width:30ch}', '.hero .lede{margin-top:1.6rem;max-width:42ch}')
s=s.replace('.page-head .lede{margin-top:1rem;max-width:34ch}', '.page-head .lede{margin-top:1rem;max-width:48ch}')
s=s.replace('word-break:break-all;user-select:all','word-break:normal;overflow-wrap:anywhere;user-select:all')
s=s.replace('.cols h4{font-size:var(--small)', '.cols h4{font-size:var(--label)')
s=s.replace('.facts dt{font-size:.95rem','.facts dt{font-size:var(--label)')
s=s.replace('.contact-card .label{font-size:var(--small)', '.contact-card .label{font-size:var(--label)')
s=s.replace('  .menu-toggle{display:grid}', '  .js .menu-toggle{display:grid}')
s=s.replace('@media (max-width:1040px){','@media (max-width:1200px){',1)
s=s.replace('.lightbox img{max-width:100%;max-height:calc(100vh - 110px);', '.lightbox img{min-height:0;object-fit:contain;flex:1 1 auto;max-width:100%;max-height:calc(100dvh - 160px);')
s=s.replace('html:not(.js) .header-row{flex-wrap:wrap}','html:not(.js) .header-row{flex-wrap:wrap}\n  html:not(.js) .header-controls{width:100%}')
s=s.replace('@media (prefers-reduced-motion:reduce){','/* Preserve scientific panels and reflow without reducing type. */\n.facts dd .nowrap{display:inline;margin:0;font:inherit;color:inherit}\n.media .fig a{min-width:0}\n@media (max-width:600px){.facts .nowrap{white-space:normal}}\n@media (prefers-reduced-motion:reduce){',1)
p.write_text(s)
p=root/'app.js';s=p.read_text()
s=s.replace("    link.addEventListener('click',function(e){\n      e.preventDefault();", "    link.addEventListener('click',function(e){\n      if(e.metaKey||e.ctrlKey||e.shiftKey||e.altKey||e.button!==0)return;\n      e.preventDefault();")
old="""    function openLb(src,alt,cap){lastFocus=document.activeElement;lbImg.src=src;lbImg.alt=alt||'';lbCap.textContent=cap||'';lb.hidden=false;document.body.classList.add('lb-open');lb.querySelector('.lb-close').focus();}
    function closeLb(){lb.hidden=true;document.body.classList.remove('lb-open');lbImg.removeAttribute('src');if(lastFocus&&lastFocus.focus)lastFocus.focus();}"""
new="""    var background=[];
    function openLb(src,alt,cap){
      lastFocus=document.activeElement;lbImg.src=src;lbImg.alt=alt||'';lbCap.textContent=cap||'';
      background=Array.prototype.filter.call(document.body.children,function(el){return el!==lb&&el.tagName!=='SCRIPT';}).map(function(el){var was=el.inert;el.inert=true;return {el:el,was:was};});
      lb.hidden=false;document.body.classList.add('lb-open');lb.querySelector('.lb-close').focus();
    }
    function closeLb(){
      if(lb.hidden)return;
      lb.hidden=true;document.body.classList.remove('lb-open');lbImg.removeAttribute('src');
      background.forEach(function(item){item.el.inert=item.was;});background=[];
      if(lastFocus&&lastFocus.focus)lastFocus.focus();
    }
    lb.addEventListener('keydown',function(e){
      if(e.key==='Tab'){e.preventDefault();lb.querySelector('.lb-close').focus();}
    });"""
assert old in s;s=s.replace(old,new);p.write_text(s)
p=root/'release.json';d=json.loads(p.read_text());d['release']=release;p.write_text(json.dumps(d,indent=2)+'\n')
p=root/'.github/scripts/check_frontend.py';s=p.read_text().replace('WIDTHS = [320, 390, 768, 820, 1024, 1440]','WIDTHS = [320, 390, 540, 674, 720, 768, 820, 880, 881, 1024, 1200, 1280, 1440, 1920]')
s=s.replace('            page.wait_for_selector("html.js")\n            for mode', '            page.wait_for_selector("html.js")\n            page.evaluate("document.fonts.ready")\n            for mode')
p.write_text(s)
p=root/'.github/workflows/check-frontend.yml';s=p.read_text()
s=s.replace('run: python3 .github/scripts/check_frontend.py','run: |\n          python3 .github/scripts/check_frontend.py\n          python3 .github/scripts/check_review.py')
s=s.replace("if: github.event_name != 'pull_request'", "if: github.ref == 'refs/heads/main' && github.event_name != 'pull_request'")
p.write_text(s)
print('Prepared website release',release,'on review branch; publication records and image assets unchanged.')
