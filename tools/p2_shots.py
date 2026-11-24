#!/usr/bin/env python3
"""Phase 2 screenshots, consistent sizes: desktop 1440x900 viewport, mobile 375x760 at 2x.

    python3 -m http.server 8765 --directory ..     # serve the folder holding this repo
    python3 tools/p2_shots.py http://localhost:8765/luckydomains-design-concepts/

Writes phase-2/screenshots/{a,b,c}-*.jpg plus current-home-*.jpg (the live production
homepage, captured read-only). Nothing outside phase-2/screenshots/ is written.
"""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE = (sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8765/luckydomains-design-concepts/").rstrip("/") + "/phase-2/"
OUT = Path(__file__).resolve().parent.parent / "phase-2" / "screenshots"; OUT.mkdir(parents=True, exist_ok=True)
DIRS = {"a": "original-evolved/", "b": "editorial-authority/", "c": "intelligent-presence/"}
PAGES = [("services", "services/"), ("website", "services/website-design/"), ("search", "services/search-ai-visibility/"), ("domains", "services/domain-identity/"), ("work", "work/")]
SHOW = "document.querySelectorAll('.rise').forEach(e=>e.classList.add('in'));document.querySelectorAll('img[loading=lazy]').forEach(i=>i.loading='eager')"


def snap(pg, name):
    pg.wait_for_timeout(900); pg.screenshot(path=str(OUT / f"{name}.jpg"), type="jpeg", quality=82); print("wrote", name)


with sync_playwright() as p:
    b = p.chromium.launch()
    for k, d in DIRS.items():
        pg = b.new_page(viewport={"width": 1440, "height": 900})
        pg.goto(BASE + d, wait_until="networkidle"); pg.mouse.move(1, 1); pg.wait_for_timeout(2600 if k == "c" else 3400); snap(pg, f"{k}-home-desktop")
        for name, path in PAGES:
            pg.goto(BASE + d + path, wait_until="networkidle"); pg.evaluate(SHOW); pg.mouse.move(1, 1); snap(pg, f"{k}-{name}")
        pg.goto(BASE + d + ("" if k != "b" else "services/website-design/"), wait_until="networkidle"); pg.evaluate(SHOW)
        if k == "a":
            pg.evaluate("document.querySelector('.dg').scrollIntoView({block:'start'}); window.scrollBy(0,-80)")
            pg.check('input[name="stuck"][value="ai"]')
        elif k == "b":
            pg.evaluate("document.getElementById('architecture').scrollIntoView({block:'start'}); window.scrollBy(0,-90)")
            pg.click('.ba-b[data-show="before"]')
        else:
            pg.evaluate("document.querySelector('.hero-map').scrollIntoView({block:'start'}); window.scrollBy(0,-90)")
            pg.wait_for_timeout(2400); pg.click('.pb[data-problem="identity"]')
        pg.mouse.move(1, 1); snap(pg, f"{k}-interaction"); pg.close()
        m = b.new_page(viewport={"width": 375, "height": 760}, device_scale_factor=2, is_mobile=True, has_touch=True)
        m.goto(BASE + d, wait_until="networkidle"); snap(m, f"{k}-home-mobile"); m.close()
    pg = b.new_page(viewport={"width": 1440, "height": 900}); pg.goto("https://luckydomains.io/", wait_until="networkidle"); snap(pg, "current-home-desktop"); pg.close()
    m = b.new_page(viewport={"width": 375, "height": 760}, device_scale_factor=2, is_mobile=True, has_touch=True); m.goto("https://luckydomains.io/", wait_until="networkidle"); snap(m, "current-home-mobile"); m.close()
    b.close()
