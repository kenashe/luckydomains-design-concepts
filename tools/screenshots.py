#!/usr/bin/env python3
"""Generate the review screenshots with Playwright (Chromium).

    python3 -m http.server 8765 --directory ..     # serve the folder that contains this repo as /site
    python3 tools/screenshots.py http://localhost:8765/site/              # v2 images only
    python3 tools/screenshots.py http://localhost:8765/site/ --originals  # also re-shoot A, B, C

Writes JPEGs to screenshots/. Each concept gets: desktop home, mobile home,
ventures page, and one extra view that shows an interaction state.
Venture Lab v2 adds v2-*.jpg files (home desktop and mobile, ventures, ZeroHuman,
the Domain Desk, founder) without overwriting the original Concept A images.
"""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

ARGS = [a for a in sys.argv[1:] if not a.startswith("--")]
BASE = ARGS[0] if ARGS else "http://localhost:8765/site/"
ORIGINALS = "--originals" in sys.argv   # re-shoot the A, B, C images too (off by default so they are preserved)
OUT = Path(__file__).resolve().parent.parent / "screenshots"; OUT.mkdir(exist_ok=True)
CONCEPTS = {"a": "concept-a-venture-lab/", "b": "concept-b-the-register/", "c": "concept-c-namespace/"}
SHOW = "document.querySelectorAll('.reveal,.rv,.rise').forEach(e=>e.classList.add('in'));document.querySelectorAll('img[loading=lazy]').forEach(i=>i.loading='eager')"


def snap(pg, name):
    pg.wait_for_timeout(900)
    pg.screenshot(path=str(OUT / f"{name}.jpg"), type="jpeg", quality=82)
    print("wrote", name)


with sync_playwright() as p:
    b = p.chromium.launch()
    for k, path in (CONCEPTS.items() if ORIGINALS else []):
        d = b.new_page(viewport={"width": 1440, "height": 900})
        d.goto(BASE + path, wait_until="networkidle"); d.mouse.move(980, 420); snap(d, f"{k}-home-desktop")
        d.goto(BASE + path + "ventures/", wait_until="networkidle"); d.evaluate(SHOW); snap(d, f"{k}-ventures-desktop")
        if k == "a":      # venture file with evidence in view
            d.goto(BASE + path + "ventures/zerohuman/", wait_until="networkidle"); d.evaluate(SHOW)
            d.evaluate("document.querySelector('.art').scrollIntoView({block:'center'})")
        elif k == "b":    # kinetic headline and history line mid-scroll
            d.goto(BASE + path, wait_until="networkidle"); d.evaluate(SHOW)
            d.evaluate("window.scrollTo(0, document.querySelector('.hist').offsetTop - 120)"); d.mouse.wheel(0, 260)
        else:             # map with a venture selected
            d.goto(BASE + path, wait_until="networkidle")
            d.evaluate("document.querySelector('.hero-map').scrollIntoView({block:'start'}); window.scrollBy(0,-90)")
            d.locator(".n-v", has_text="ZeroHuman").first.click()
        snap(d, f"{k}-detail-desktop"); d.close()
        m = b.new_page(viewport={"width": 375, "height": 760}, device_scale_factor=2, is_mobile=True, has_touch=True)
        m.goto(BASE + path, wait_until="networkidle"); snap(m, f"{k}-home-mobile"); m.close()
    # Venture Lab v2: distinct filenames, originals untouched
    V2 = BASE + "concept-a-venture-lab-v2/"
    d = b.new_page(viewport={"width": 1440, "height": 900})
    d.goto(V2, wait_until="networkidle"); d.mouse.move(980, 420); snap(d, "v2-home-desktop")
    d.goto(V2 + "ventures/", wait_until="networkidle"); d.evaluate(SHOW); snap(d, "v2-ventures-desktop")
    d.goto(V2 + "ventures/zerohuman/", wait_until="networkidle"); d.evaluate(SHOW)
    d.evaluate("document.querySelector('[data-fx]').scrollIntoView({block:'center'})"); d.wait_for_timeout(2800); snap(d, "v2-zerohuman-desktop")
    d.goto(V2, wait_until="networkidle"); d.evaluate(SHOW)
    d.evaluate("window.scrollTo(0, document.querySelector('.desk').offsetTop - 60)"); snap(d, "v2-domain-desk-desktop")
    d.goto(V2 + "founder/", wait_until="networkidle"); d.evaluate(SHOW); snap(d, "v2-founder-desktop")
    d.close()
    m = b.new_page(viewport={"width": 375, "height": 760}, device_scale_factor=2, is_mobile=True, has_touch=True)
    m.goto(V2, wait_until="networkidle"); snap(m, "v2-home-mobile"); m.close()
    b.close()
