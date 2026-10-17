"""Display tests only: they do not recover content missing from cropped files."""
import base64
import json
import os
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE = os.environ.get('BASE', 'http://127.0.0.1:8000/')
OUT = Path(os.environ.get('REPORT_DIR', 'browser-report'))
OUT.mkdir(parents=True, exist_ok=True)
report = {'base': BASE, 'checks': {}, 'real_photos': [], 'shape_tests': [],
          'source_restoration_complete': False,
          'limits': ['Existing six travel assets are legacy square crops. Uncropped sources are still required.',
                     'Landscape/portrait/panorama fixtures test display behavior only; they are not restored photographs.',
                     'Chromium viewport tests, not physical-device certification.']}
checks = report['checks']
MEASURE = '''e=>{const s=getComputedStyle(e),r=e.getBoundingClientRect();return {
    natural:[e.naturalWidth,e.naturalHeight], rendered:[r.width,r.height],
    fit:s.objectFit,transform:s.transform,radius:s.borderRadius,
    viewportOK:r.left>=-1&&r.right<=innerWidth+1&&r.top>=-1&&r.bottom<=innerHeight+1
}}'''
def ratio_ok(m):
    return (m['natural'][0]>0 and m['rendered'][1]>0 and
            abs(m['rendered'][0]/m['rendered'][1]-m['natural'][0]/m['natural'][1])<0.015)
def fixture(w,h):
    # A visibly bordered engineering test rectangle, not replacement photo content.
    svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}"><rect width="100%" height="100%" fill="#ddd"/><rect x="3" y="3" width="{w-6}" height="{h-6}" fill="none" stroke="#123" stroke-width="6"/></svg>'
    return 'data:image/svg+xml;base64,'+base64.b64encode(svg.encode()).decode()
with sync_playwright() as p:
    b=p.chromium.launch()
    ctx=b.new_context(viewport={'width':1280,'height':960})
    page=ctx.new_page()
    for width in [390,674,820,1280,1920]:
        page.set_viewport_size({'width':width,'height':960})
        for mode in ['light','dark']:
            page.goto(BASE+'personal.html',wait_until='domcontentloaded')
            page.wait_for_selector('html.js')
            page.evaluate('document.fonts.ready')
            page.locator(f'.theme-control button[data-theme-value="{mode}"]').click()
            links=page.locator('.photography-gallery a[data-lightbox]')
            checks[f'{width}_{mode}_six_photos']=links.count()==6
            for i in range(6):
                a=links.nth(i);im=a.locator('img');a.scroll_into_view_if_needed()
                im.evaluate('(e)=>e.decode()');a.hover();page.wait_for_timeout(50)
                m=im.evaluate(MEASURE)
                thumb=ratio_ok(m) and m['fit']=='contain' and m['transform']=='none' and m['radius']=='0px'
                target=a.get_attribute('href');a.click()
                full=page.locator('#lightbox img');full.evaluate('(e)=>e.decode()')
                fm=full.evaluate(MEASURE)
                enlarged=ratio_ok(fm) and fm['fit']=='contain' and fm['viewportOK'] and fm['radius']=='0px' and full.get_attribute('src')==target
                page.keyboard.press('Escape')
                focus=a.evaluate('(e)=>document.activeElement===e')
                report['real_photos'].append({'width':width,'theme':mode,'photo':i+1,'preview':m,'full':fm,'pass':thumb and enlarged and focus})
            for shape,(w,h) in {'landscape':(1600,900),'portrait':(900,1600),'panorama':(2400,600)}.items():
                a=links.first
                a.evaluate('''(e,v)=>{e.href=v.src;const i=e.querySelector('img');i.src=v.src;i.width=v.w;i.height=v.h;}''', {'src':fixture(w,h),'w':w,'h':h})
                a.scroll_into_view_if_needed();im=a.locator('img');im.evaluate('(e)=>e.decode()');a.hover()
                tm=im.evaluate(MEASURE);a.click();full=page.locator('#lightbox img');full.evaluate('(e)=>e.decode()');fm=full.evaluate(MEASURE)
                report['shape_tests'].append({'width':width,'theme':mode,'shape':shape,'preview':tm,'full':fm,'pass':ratio_ok(tm) and ratio_ok(fm) and fm['viewportOK']})
                page.keyboard.press('Escape')
            checks[f'{width}_{mode}_page_reflow']=page.evaluate('document.documentElement.scrollWidth<=innerWidth+1')
    checks['sixty_existing_photo_display_cases']=len(report['real_photos'])==60 and all(x['pass'] for x in report['real_photos'])
    checks['thirty_varied_aspect_ratio_cases']=len(report['shape_tests'])==30 and all(x['pass'] for x in report['shape_tests'])
    # Verify that closing a photograph does not leak its styling into research figures.
    page.goto(BASE+'research.html',wait_until='domcontentloaded');page.wait_for_selector('html.js')
    page.locator('a[data-lightbox]').first.click()
    checks['research_figure_view_not_reclassified']=page.locator('#lightbox').evaluate("e=>!e.classList.contains('photography-view')")
    page.keyboard.press('Escape')
    b.close()
report['pass']=all(checks.values())
(OUT/'photo-framing.json').write_text(json.dumps(report,indent=2))
print(json.dumps({'checks':checks,'pass':report['pass'],'source_restoration_complete':False,'limits':report['limits']},indent=2))
if not report['pass']:
    raise SystemExit('Photo display regression failed; full source recovery is a separate pending task.')
