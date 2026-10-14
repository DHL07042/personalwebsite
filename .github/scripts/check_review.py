"""Focused regressions for website review. No analytics, uploads or account access."""
import json, os, re
from pathlib import Path
from urllib.parse import urlsplit, unquote
from html.parser import HTMLParser
from playwright.sync_api import sync_playwright

BASE=os.environ.get('BASE','http://127.0.0.1:8000/')
OUT=Path(os.environ.get('REPORT_DIR','browser-report'))
OUT.mkdir(parents=True,exist_ok=True)
PAGES=['index.html','research.html','publications.html','personal.html','contact.html']
class Document(HTMLParser):
    def __init__(self):super().__init__();self.ids=set();self.links=[];self.sources=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id' in a:self.ids.add(a['id'])
        if tag=='a' and 'href' in a:self.links.append(a['href'])
        if 'src' in a:self.sources.append(a['src'])
        if tag=='source' and 'src' in a:self.sources.append(a['src'])
parsed={}
for fn in PAGES:
    d=Document();d.feed(Path(fn).read_text());parsed[fn]=d
broken=[]
for fn,d in parsed.items():
    for url in d.links+d.sources:
        u=urlsplit(url)
        if u.scheme or u.netloc:continue
        target=unquote(u.path) or fn
        if not Path(target).is_file():broken.append([fn,url,'missing file'])
        elif u.fragment and target in parsed and u.fragment not in parsed[target].ids:broken.append([fn,url,'missing anchor'])
bootstrap=Path('theme-init.js').read_text().strip()
checks={'local_links_and_sources':not broken,'bootstrap_source_consistency':True}
for fn in PAGES:
    s=Path(fn).read_text();m=re.search(r'<script id="theme-bootstrap">\s*(.*?)\s*</script>',s,re.S)
    checks['bootstrap_source_consistency'] &= bool(m and m.group(1).strip()==bootstrap and not re.search(r'<script[^>]+src="theme-init',s))
checks['bootstrap_does_not_hide_navigation']='classList' not in bootstrap
research=Path('research.html').read_text()
# The two PSAO crops stay off the page (uncropped sources are in assets/src). grf-results.webp was
# restored in release 2026-10-14.7 with the owner's condition mapping (Case I/II/III = pre-tuning off/weak/strong).
checks['held_figures_not_rendered']=all(n not in research for n in ['gait-distance.webp','gait-phases.webp'])
checks['held_assets_preserved']=all(Path('assets/img',n).is_file() for n in ['gait-distance.webp','gait-phases.webp','grf-results.webp'])
# Display asset provenance and source-based scope checks.
import hashlib
media=json.loads(Path('media-processing.json').read_text())
checks['media_manifest_integrity']=all(hashlib.sha256(Path(x['source']).read_bytes()).hexdigest()==x['source_sha256'] and hashlib.sha256(Path(x['output']).read_bytes()).hexdigest()==x['output_sha256'] and x['decoded_pixel_equality'] for x in media['assets'])
checks['t1_byline_matches_supplied_sources']='<strong>D. Lee</strong>, K. Kong, and H. Choi' in Path('publications.html').read_text().split('id="T1"')[1]
checks['t1_scope_is_not_fully_crossed']='for one participant, plus examples from two additional participants' in research
checks['grf_owner_mapping_retained']='off (Case I), weak (Case II) and strong (Case III)' in research
checks['t1_provenance_retained']=research.count('[T1]')>=6
report={'base':BASE,'checks':checks,'broken_links':broken,'text_zoom':[],'limits':['Chromium viewport tests; not physical devices.','No guarantee of Internet tail latency or full video playback.']}
with sync_playwright() as p:
    browser=p.chromium.launch()
    # A blocked enhancement script must never leave mobile navigation hidden.
    c=browser.new_context(viewport={'width':390,'height':844})
    c.route('**/app.js*',lambda route:route.abort())
    page=c.new_page();page.goto(BASE+'contact.html',wait_until='domcontentloaded')
    checks['blocked_app_main_visible']=page.locator('#main').is_visible()
    checks['blocked_app_nav_readable']=all(page.locator('#site-nav a').nth(i).is_visible() for i in range(5))
    checks['blocked_app_no_dead_menu']=not page.locator('.menu-toggle').is_visible()
    page.locator('#site-nav a[href="research.html"]').click();page.wait_for_url('**/research.html')
    checks['blocked_app_link_navigation']=page.url.endswith('/research.html')
    c.close()
    c=browser.new_context(viewport={'width':1440,'height':1000},color_scheme='light')
    page=c.new_page();page.goto(BASE+'research.html',wait_until='domcontentloaded');page.evaluate('document.fonts.ready')
    checks['research_images_contain']=page.locator('a[href="assets/img/m20-module.webp"] img').evaluate('(e)=>getComputedStyle(e).objectFit')=='contain'
    a=page.locator('a[data-lightbox]').first;a.click()
    checks['dialog_visible']=page.locator('#lightbox').is_visible()
    checks['dialog_background_inert']=page.locator('#main').evaluate('(e)=>e.inert')
    page.keyboard.press('Tab');checks['dialog_tab_contained']=page.locator('.lb-close').evaluate('(e)=>e===document.activeElement')
    page.keyboard.press('Shift+Tab');checks['dialog_reverse_tab_contained']=page.locator('.lb-close').evaluate('(e)=>e===document.activeElement')
    page.keyboard.press('Escape');checks['dialog_close_restores_focus']=a.evaluate('(e)=>e===document.activeElement') and not page.locator('#main').evaluate('(e)=>e.inert')
    page.goto(BASE+'personal.html',wait_until='domcontentloaded')
    checks['loop_has_pause_control']=page.locator('video').first.evaluate('(e)=>e.controls')
    for width in [674,820,1280]:
        page.set_viewport_size({'width':width,'height':1000})
        for fn in ['index.html','research.html','contact.html']:
            page.goto(BASE+fn,wait_until='domcontentloaded');page.evaluate('document.fonts.ready')
            page.add_style_tag(content='html{font-size:200%!important}')
            row={'width':width,'page':fn,'overflow':page.evaluate('document.documentElement.scrollWidth>innerWidth+1'),'offenders':page.evaluate("Array.from(document.querySelectorAll('body *')).filter(e=>e.getBoundingClientRect().right>innerWidth+1).slice(0,8).map(e=>({tag:e.tagName,cls:e.className,right:e.getBoundingClientRect().right}))")}
            report['text_zoom'].append(row)
    checks['text_zoom_no_horizontal_overflow']=all(not r['overflow'] for r in report['text_zoom'])
    for name,width,fn in [('review-desktop',1440,'index.html'),('review-laptop',1280,'index.html'),('review-fold',674,'index.html'),('review-tablet',820,'research.html'),('review-phone',390,'research.html'),('review-research',1440,'research.html')]:
        page.set_viewport_size({'width':width,'height':1000});page.goto(BASE+fn,wait_until='domcontentloaded');page.evaluate('document.fonts.ready')
        page.locator('.theme-control button[data-theme-value="light"]').click()
        page.locator('img').evaluate_all("images=>images.forEach(img=>img.loading='eager')")
        page.evaluate("Promise.race([Promise.all(Array.from(document.images).map(img=>img.decode().catch(()=>{}))),new Promise(r=>setTimeout(r,3000))])")
        page.screenshot(path=str(OUT/(name+'.png')),full_page=True)
    browser.close()
report['pass']=all(checks.values())
(OUT/'review.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
if not report['pass']:raise SystemExit('Focused review checks failed.')
