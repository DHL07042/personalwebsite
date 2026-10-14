"""Browser checks for the website.

Runs against BASE (default: a local server of the checked-out files). With LIVE=1 it
first waits until the deployed release.json matches the repository's release.json,
so a push to main is validated only after GitHub Pages has published it.

Environment:
  BASE          site root, e.g. http://127.0.0.1:8000/ or https://daeholee.me/
  LIVE          "1" to wait for the deployed release before checking
  WAIT_SECONDS  how long to wait for the deployment (LIVE only, default 420)
  REPORT_DIR    output directory for report.json and screenshots
"""
import json, os, sys, time, urllib.request
from pathlib import Path
from datetime import datetime, timezone

BASE = os.environ.get("BASE", "http://127.0.0.1:8000/")
LIVE = os.environ.get("LIVE") == "1"
WAIT = int(os.environ.get("WAIT_SECONDS", "420"))
OUT = Path(os.environ.get("REPORT_DIR", "browser-report"))
PAGES = ["index.html", "research.html", "publications.html", "personal.html", "contact.html"]
WIDTHS = [320, 390, 768, 820, 1024, 1440]
EXPECTED = json.loads(Path("release.json").read_text())["release"]

if LIVE:
    deadline = time.time() + WAIT
    while True:
        try:
            with urllib.request.urlopen(BASE + "release.json?check=" + str(time.time()), timeout=15) as r:
                if json.load(r).get("release") == EXPECTED:
                    break
        except Exception:
            pass
        if time.time() > deadline:
            sys.exit(f"Deployed release did not reach {EXPECTED} within {WAIT}s; not reporting success.")
        time.sleep(10)

from playwright.sync_api import sync_playwright

report = {"checked_at_utc": datetime.now(timezone.utc).isoformat(), "base": BASE, "release": EXPECTED,
          "matrix": [], "checks": {}, "pageerrors": []}
OUT.mkdir(parents=True, exist_ok=True)

def theme_button(page, mode):
    page.click(f'.theme-control button[data-theme-value="{mode}"]')

with sync_playwright() as p:
    browser = p.chromium.launch()
    ctx = browser.new_context(viewport={"width": 1440, "height": 1000}, color_scheme="dark")
    page = ctx.new_page()
    page.on("pageerror", lambda e: report["pageerrors"].append(str(e)))

    # First visit: no stored preference, so the page follows the system (no data-theme attribute).
    page.goto(BASE, wait_until="domcontentloaded")
    page.wait_for_selector("html.js")
    report["checks"]["first_visit_follows_system"] = page.get_attribute("html", "data-theme") is None
    report["checks"]["first_visit_dark_scheme"] = page.evaluate("getComputedStyle(document.documentElement).colorScheme") == "dark"

    # Layout matrix: no horizontal overflow, 200 status, explicit theme applied.
    for width in WIDTHS:
        page.set_viewport_size({"width": width, "height": 1000})
        for fn in PAGES:
            response = page.goto(BASE + fn, wait_until="domcontentloaded")
            page.wait_for_selector("html.js")
            for mode in ["light", "dark"]:
                theme_button(page, mode)
                row = page.evaluate("""() => ({
                    overflow: document.documentElement.scrollWidth > innerWidth + 1,
                    theme: document.documentElement.getAttribute('data-theme'),
                    scheme: getComputedStyle(document.documentElement).colorScheme,
                    bodyFont: getComputedStyle(document.body).fontSize
                })""")
                row.update(page=fn, width=width, mode=mode, status=response.status if response else None)
                report["matrix"].append(row)

    # Preference persistence.
    page.goto(BASE, wait_until="domcontentloaded"); page.wait_for_selector("html.js")
    theme_button(page, "dark")
    page.reload(wait_until="domcontentloaded"); page.wait_for_selector("html.js")
    report["checks"]["theme_reload"] = page.get_attribute("html", "data-theme") == "dark"
    page.goto(BASE + "research.html", wait_until="domcontentloaded"); page.wait_for_selector("html.js")
    report["checks"]["theme_across_pages"] = page.get_attribute("html", "data-theme") == "dark"

    # System mode: attribute removed, computed scheme follows the OS.
    theme_button(page, "system")
    page.emulate_media(color_scheme="light"); page.wait_for_timeout(100)
    report["checks"]["system_light"] = page.get_attribute("html", "data-theme") is None and \
        page.evaluate("getComputedStyle(document.documentElement).colorScheme") == "light"
    page.emulate_media(color_scheme="dark"); page.wait_for_timeout(100)
    report["checks"]["system_dark"] = page.get_attribute("html", "data-theme") is None and \
        page.evaluate("getComputedStyle(document.documentElement).colorScheme") == "dark"

    # Mobile menu.
    page.set_viewport_size({"width": 390, "height": 844})
    page.goto(BASE, wait_until="domcontentloaded"); page.wait_for_selector("html.js")
    page.locator(".menu-toggle").click()
    report["checks"]["mobile_menu_open"] = page.get_attribute("#site-nav", "data-open") == "true"
    page.keyboard.press("Escape")
    report["checks"]["mobile_menu_escape"] = page.get_attribute("#site-nav", "data-open") == "false"
    page.locator(".menu-toggle").click()
    page.locator('#site-nav a[href="contact.html"]').click()
    page.wait_for_url("**/contact.html")
    report["checks"]["mobile_link_navigation"] = page.url.endswith("/contact.html")

    # Videos: click-to-play boxes with a plain link fallback.
    page.goto(BASE + "personal.html", wait_until="domcontentloaded")
    report["checks"]["personal_video_boxes"] = page.locator(".yt").count() == 3 and \
        page.locator('.yt a[href*="youtube.com/watch"]').count() == 3
    page.locator(".yt a").first.click(); page.wait_for_timeout(300)
    report["checks"]["video_player_on_click"] = page.locator(".yt iframe").count() == 1
    page.goto(BASE + "research.html", wait_until="domcontentloaded")
    report["checks"]["research_video_box"] = page.locator(".yt").count() == 1

    # Contact: address shown as text, copy button present.
    page.goto(BASE + "contact.html", wait_until="domcontentloaded"); page.wait_for_selector("html.js")
    report["checks"]["contact_copy_button"] = page.locator("[data-copy]").count() == 1

    # Screenshots.
    for name, width, fn, mode in [("desktop-light", 1440, "index.html", "light"), ("desktop-dark", 1440, "research.html", "dark"),
                                  ("phone-light", 390, "index.html", "light"), ("phone-dark", 390, "personal.html", "dark")]:
        page.set_viewport_size({"width": width, "height": 1000})
        page.goto(BASE + fn, wait_until="domcontentloaded"); page.wait_for_selector("html.js")
        theme_button(page, mode); page.wait_for_timeout(400)
        page.screenshot(path=str(OUT / f"{name}.png"), full_page=True)

    # Without JavaScript: navigation readable, no overflow.
    nc = browser.new_context(java_script_enabled=False, viewport={"width": 390, "height": 844})
    np_ = nc.new_page(); np_.goto(BASE, wait_until="domcontentloaded")
    report["checks"]["no_js_nav_readable"] = all(np_.locator("#site-nav a").nth(i).is_visible() for i in range(5))
    report["checks"]["no_js_no_overflow"] = np_.evaluate("document.documentElement.scrollWidth <= innerWidth + 1")
    browser.close()

matrix_ok = all((not r["overflow"]) and r["status"] == 200 and r["theme"] == r["mode"] and r["scheme"] == r["mode"] for r in report["matrix"])
report["pass"] = all(report["checks"].values()) and matrix_ok and not report["pageerrors"]
report["failed_checks"] = [k for k, v in report["checks"].items() if not v]
report["failed_matrix_rows"] = [r for r in report["matrix"] if r["overflow"] or r["status"] != 200 or r["theme"] != r["mode"] or r["scheme"] != r["mode"]]
(OUT / "report.json").write_text(json.dumps(report, indent=2))
print(json.dumps({k: report[k] for k in ["base", "release", "checks", "pageerrors", "failed_matrix_rows", "pass"]}, indent=2))
if not report["pass"]:
    sys.exit("Frontend verification failed; see report.json.")
