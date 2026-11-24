#!/usr/bin/env python3
"""Screenshots of the staged production candidate, plus the current live home page for comparison.

    python3 -m http.server 8765 --directory ..      # so this repo is served at /luckydomains-design-concepts/
    python3 tools/staging_shots.py http://localhost:8765/luckydomains-design-concepts/production-candidate

Writes JPEGs to production-candidate/review/screenshots/. Desktop 1440x900, tablet 768x1024, mobile 375x760 at 2x.
"""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE = sys.argv[1].rstrip("/")
OUT = Path(__file__).resolve().parent.parent / "production-candidate" / "review" / "screenshots"; OUT.mkdir(parents=True, exist_ok=True)
SHOW = "document.querySelectorAll('.reveal').forEach(e=>e.classList.add('in'));document.querySelectorAll('img[loading=lazy]').forEach(i=>i.loading='eager')"
DESK = [("home-desktop", "/", None), ("ventures", "/ventures/", None), ("zerohuman", "/ventures/zerohuman/", "[data-fx]"), ("services", "/services/", None),
        ("domain-desk", "/", "#domain-desk"), ("about", "/about/", None), ("founder", "/founder/ken-ashe/", None), ("contact", "/contact/", None)]
with sync_playwright() as p:
    b = p.chromium.launch()
    d = b.new_page(viewport={"width": 1440, "height": 900})
    for name, path, sel in DESK:
        d.goto(BASE + path, wait_until="networkidle"); d.evaluate(SHOW)
        if sel == "[data-fx]": d.evaluate("document.querySelector('[data-fx]').scrollIntoView({block:'center'})"); d.wait_for_timeout(2800)
        elif sel: d.evaluate(f"window.scrollTo(0, document.querySelector('{sel}').offsetTop - 70)")
        else: d.mouse.move(980, 420)
        d.wait_for_timeout(900); d.screenshot(path=str(OUT / f"pc-{name}.jpg"), type="jpeg", quality=82); print("wrote", name)
    d.goto("https://luckydomains.io/", wait_until="networkidle"); d.wait_for_timeout(900)
    d.screenshot(path=str(OUT / "live-home-desktop.jpg"), type="jpeg", quality=82); print("wrote live-home-desktop (current production, read only)")
    d.close()
    t = b.new_page(viewport={"width": 768, "height": 1024}); t.goto(BASE + "/", wait_until="networkidle"); t.wait_for_timeout(900)
    t.screenshot(path=str(OUT / "pc-home-tablet.jpg"), type="jpeg", quality=82); t.close(); print("wrote home-tablet")
    m = b.new_page(viewport={"width": 375, "height": 760}, device_scale_factor=2, is_mobile=True, has_touch=True)
    m.goto(BASE + "/", wait_until="networkidle"); m.wait_for_timeout(900)
    m.screenshot(path=str(OUT / "pc-home-mobile.jpg"), type="jpeg", quality=82); m.close(); print("wrote home-mobile")
    b.close()
