"""Focused editorial regressions; run by check_review.py on the checked-out site."""
import hashlib
import json
import os
from html.parser import HTMLParser
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE = os.environ.get('BASE', 'http://127.0.0.1:8000/')
OUT = Path(os.environ.get('REPORT_DIR', 'browser-report'))
OUT.mkdir(parents=True, exist_ok=True)
EXPECTED = (
    'I’m drawn to the precision and physical feedback of circuit driving—feeling the chassis load up through the seat and steering wheel in high-g corners. '
    'Through progressive on-track training (including the BMW M Intensive, Mercedes-AMG Performance, and HMG N Track Performance programs) '
    'in limit handling, weight transfer, and low-grip car control, I’m steadily working my way from lead-follow sessions toward solo open-track driving.'
)
AXES = [
    ('Physical human–robot interaction', 'coupled dynamics, compliance, and physical interfaces.'),
    ('Perception-guided assistive control', 'intent inference amid reactive responses, and pre-contact sensing.'),
    ('Biomechanical evaluation', 'interaction loads, locomotor performance, and human adaptation.'),
]
report = {'base': BASE, 'checks': {}, 'limits': ['Chromium viewport tests, not physical-device certification.', 'No driving video playback or network-tail-latency test.']}
checks = report['checks']
checks['public_cv_bytes_unchanged'] = hashlib.sha256(Path('Daeho-Lee-CV.pdf').read_bytes()).hexdigest() == '33b5d254c655c0aa46193741ea5246a98ad469cdfea45976dcc7ba966fe8eb0b'
with sync_playwright() as p:
    browser = p.chromium.launch()
    ctx = browser.new_context(viewport={'width': 1280, 'height': 1000})
    page = ctx.new_page()
    page.goto(BASE + 'personal.html', wait_until='domcontentloaded')
    page.wait_for_selector('html.js')
    driving = page.locator('#performance-driving')
    checks['driving_heading_preserved'] = driving.locator('h2').inner_text() == 'Performance driving'
    checks['programs_stay_in_one_paragraph'] = driving.locator('.part.prose p').count() == 1 and driving.locator('.part.prose p').inner_text() == EXPECTED
    checks['no_separate_program_row_or_columns'] = driving.locator('.summary, .cols, h3, h4, ul, ol').count() == 0
    checks['driving_eyebrow_has_no_date'] = driving.locator('.eyebrow').inner_text() == 'Off duty'
    checks['no_training_log_or_ranking'] = all(x not in driving.inner_text() for x in ['How I practice', 'Courses completed', 'September', 'August', '2026', '1:52', '13%', 'coasting', 'braking later'])
    for fn in ['index.html', 'research.html']:
        page.goto(BASE + fn, wait_until='domcontentloaded')
        block = page.locator('.research-interests')
        checks[fn + '_three_axes'] = block.locator('.ri-row').count() == 3
        checks[fn + '_axis_text'] = [(block.locator('.ri-row').nth(i).locator('dt').inner_text(), block.locator('.ri-row').nth(i).locator('dd').inner_text()) for i in range(3)] == AXES
        checks[fn + '_future_scope'] = block.locator('.ri-scope').inner_text() == 'Wearable and legged robots'
    page.goto(BASE + 'index.html', wait_until='domcontentloaded')
    checks['background_does_not_claim_legged_robot_experience'] = page.locator('.hero .lede').inner_text() == 'My research background is in sensing and experimental evaluation of wearable robots.'
    for label, width, fn, selector, mode in [
        ('driving-desktop', 1280, 'personal.html', '#performance-driving', 'light'),
        ('driving-phone', 390, 'personal.html', '#performance-driving', 'dark'),
        ('interests-desktop', 1280, 'index.html', '.research-interests', 'light'),
        ('interests-fold', 674, 'index.html', '.research-interests', 'light'),
        ('interests-phone', 390, 'research.html', '.research-interests', 'dark'),
    ]:
        page.set_viewport_size({'width': width, 'height': 1000})
        page.goto(BASE + fn, wait_until='domcontentloaded')
        page.wait_for_selector('html.js')
        page.evaluate('document.fonts.ready')
        page.locator(f'.theme-control button[data-theme-value="{mode}"]').click()
        checks[label + '_no_overflow'] = page.evaluate('document.documentElement.scrollWidth <= innerWidth + 1')
        page.locator(selector).screenshot(path=str(OUT / (label + '.png')))
    browser.close()
report['pass'] = all(checks.values())
(OUT / 'copy-ri.json').write_text(json.dumps(report, indent=2))
print(json.dumps(report, indent=2))
if not report['pass']:
    raise SystemExit('Copy/RI regression check failed.')
