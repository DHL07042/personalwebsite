"""Verify source bytes and full-frame rendering of owner-provided photography."""
import base64
import hashlib
import json
import os
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE = os.environ.get('BASE', 'http://127.0.0.1:8000/')
OUT = Path(os.environ.get('REPORT_DIR', 'browser-report'))
OUT.mkdir(parents=True, exist_ok=True)
WIDTHS = [320, 390, 674, 820, 1280, 1440, 1920]
manifest = json.loads(Path('photography.json').read_text())
photos = manifest['photos']
report = {'base': BASE, 'checks': {}, 'source_files': [], 'real_photos': [], 'shape_tests': [],
          'source_restoration_complete': False,
          'limits': ['The six source JPEGs are checked against the owner-upload hashes.',
                     'Synthetic shape fixtures test fitting, not photograph content.',
                     'Chromium viewport tests; not physical devices or an Internet latency guarantee.']}
checks = report['checks']
checks['six_explicit_sources'] = (len(photos) == 6 and
    [p['id'] for p in photos] == [f'travel-{i}' for i in range(1,7)])
for p in photos:
    raw = Path(p['path']).read_bytes()
    good = len(raw) == p['bytes'] and hashlib.sha256(raw).hexdigest() == p['sha256']
    report['source_files'].append({'path': p['path'], 'bytes': len(raw), 'pass': good})
checks['source_bytes_match_uploaded_originals'] = all(p['pass'] for p in report['source_files'])
checks['manifest_marks_sources_restored'] = manifest.get('source_restoration_complete') is True
MEASURE = '''e=>{const s=getComputedStyle(e),r=e.getBoundingClientRect();return {
    natural:[e.naturalWidth,e.naturalHeight], rendered:[r.width,r.height],
    fit:s.objectFit,transform:s.transform,radius:s.borderRadius,
    viewportOK:r.left>=-1&&r.right<=innerWidth+1&&r.top>=-1&&r.bottom<=innerHeight+1
}}'''
def ratio_ok(m):
    return (m['natural'][0]>0 and m['rendered'][1]>0 and
            abs(m['rendered'][0]/m['rendered'][1]-m['natural'][0]/m['natural'][1])<0.002)
def fixture(w,h):
    svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}"><rect width="100%" height="100%" fill="#ddd"/><rect x="3" y="3" width="{w-6}" height="{h-6}" fill="none" stroke="#123" stroke-width="6"/></svg>'
    return 'data:image/svg+xml;base64,'+base64.b64encode(svg.encode()).decode()
with sync_playwright() as p:
    b=p.chromium.launch()
    ctx=b.new_context(viewport={'width':1280,'height':960})
    page=ctx.new_page()
    served=[]
    for entry in photos:
        r=ctx.request.get(BASE+entry['path'])
        served.append(r.status==200 and hashlib.sha256(r.body()).hexdigest()==entry['sha256'])
    checks['served_original_bytes_match'] = all(served)
    for width in WIDTHS:
        page.set_viewport_size({'width':width,'height':960})
        for mode in ['light','dark']:
            page.goto(BASE+'personal.html',wait_until='domcontentloaded')
            page.wait_for_selector('html.js');page.evaluate('document.fonts.ready')
            page.locator(f'.theme-control button[data-theme-value="{mode}"]').click()
            links=page.locator('.photography-gallery a[data-lightbox]')
            checks[f'{width}_{mode}_six_photos']=links.count()==6
            for i,entry in enumerate(photos):
                a=links.nth(i);im=a.locator('img');a.scroll_into_view_if_needed()
                im.evaluate('(e)=>e.decode()');a.hover();page.wait_for_timeout(50)
                m=im.evaluate(MEASURE)
                source_ok=(a.get_attribute('href')==entry['path'] and im.get_attribute('src')==entry['path'] and
                    m['natural']==[entry['width'],entry['height']] and
                    im.get_attribute('width')==str(entry['width']) and im.get_attribute('height')==str(entry['height']))
                thumb=ratio_ok(m) and m['fit']=='contain' and m['transform']=='none' and m['radius']=='0px'
                target=a.get_attribute('href');a.click()
                full=page.locator('#lightbox img');full.evaluate('(e)=>e.decode()')
                fm=full.evaluate(MEASURE)
                enlarged=(ratio_ok(fm) and fm['natural']==m['natural'] and fm['fit']=='contain' and
                    fm['viewportOK'] and fm['radius']=='0px' and full.get_attribute('src')==target)
                page.keyboard.press('Escape');focus=a.evaluate('(e)=>document.activeElement===e')
                report['real_photos'].append({'width':width,'theme':mode,'photo':i+1,'preview':m,'full':fm,
                    'pass':source_ok and thumb and enlarged and focus})
            for shape,(w,h) in {'landscape':(1600,900),'portrait':(900,1600),'panorama':(2400,600)}.items():
                a=links.first
                a.evaluate('''(e,v)=>{e.href=v.src;const i=e.querySelector('img');i.src=v.src;i.width=v.w;i.height=v.h;}''',{'src':fixture(w,h),'w':w,'h':h})
                a.scroll_into_view_if_needed();im=a.locator('img');im.evaluate('(e)=>e.decode()');a.hover()
                tm=im.evaluate(MEASURE);a.click();full=page.locator('#lightbox img');full.evaluate('(e)=>e.decode()');fm=full.evaluate(MEASURE)
                report['shape_tests'].append({'width':width,'theme':mode,'shape':shape,'preview':tm,'full':fm,
                    'pass':ratio_ok(tm) and ratio_ok(fm) and fm['viewportOK']})
                page.keyboard.press('Escape')
            checks[f'{width}_{mode}_page_reflow']=page.evaluate('document.documentElement.scrollWidth<=innerWidth+1')
    checks['eighty_four_original_photo_display_cases']=len(report['real_photos'])==84 and all(x['pass'] for x in report['real_photos'])
    checks['forty_two_varied_aspect_ratio_cases']=len(report['shape_tests'])==42 and all(x['pass'] for x in report['shape_tests'])
    page.goto(BASE+'research.html',wait_until='domcontentloaded');page.wait_for_selector('html.js')
    page.locator('a[data-lightbox]').first.click()
    checks['research_figure_view_not_reclassified']=page.locator('#lightbox').evaluate("e=>!e.classList.contains('photography-view')")
    page.keyboard.press('Escape')
    for name,width,mode in [('desktop',1280,'light'),('phone',390,'light'),('fold',674,'light'),('tablet',820,'light'),('dark',1280,'dark')]:
        page.set_viewport_size({'width':width,'height':960})
        page.goto(BASE+'personal.html',wait_until='domcontentloaded');page.wait_for_selector('html.js');page.evaluate('document.fonts.ready')
        page.locator(f'.theme-control button[data-theme-value="{mode}"]').click()
        for im in page.locator('.photography-gallery img').all():im.scroll_into_view_if_needed();im.evaluate('(e)=>e.decode()')
        page.locator('#off-duty').screenshot(path=str(OUT/f'photo-gallery-{name}.png'))
        page.locator('.photography-gallery a').nth(3 if name=='desktop' else 0).click()
        page.locator('#lightbox img').evaluate('(e)=>e.decode()')
        page.screenshot(path=str(OUT/f'photo-lightbox-{name}.png'))
        page.keyboard.press('Escape')
    b.close()
report['source_restoration_complete']=checks['six_explicit_sources'] and checks['source_bytes_match_uploaded_originals'] and checks['served_original_bytes_match']
report['pass']=all(checks.values())
(OUT/'photo-framing.json').write_text(json.dumps(report,indent=2))
print(json.dumps({'checks':checks,'pass':report['pass'],'source_restoration_complete':report['source_restoration_complete'],'limits':report['limits']},indent=2))
if not report['pass']:raise SystemExit('Photo source fidelity or rendering check failed.')
