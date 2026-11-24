#!/usr/bin/env python3
"""Version 3 screenshots. Desktop 1440x900 viewport, mobile 375x760 at 2x.

    python3 tools/p3_shots.py http://localhost:8765/luckydomains-design-concepts/

Writes phase-3/screenshots/{a,b,c}-*.jpg and copies the read-only production references.
"""
import argparse, shutil
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("base", nargs="?", default="http://localhost:8765/luckydomains-design-concepts/")
parser.add_argument("--only", choices=("a", "b", "c"), help="refresh only one concept's screenshots")
args = parser.parse_args()
BASE = args.base.rstrip("/") + "/phase-3/"
OUT = ROOT / "phase-3" / "screenshots"; OUT.mkdir(parents=True, exist_ok=True)
DIRS = {"a": "original-evolved/", "b": "editorial/", "c": "interactive/"}
PAGES = [("services", "services/"), ("ai", "services/ai-visibility/"), ("websites", "services/website-design/"), ("work", "work/luckydomains-io/")]
SHOW = "document.querySelectorAll('.reveal').forEach(e=>e.classList.add('in'));document.querySelectorAll('img[loading=lazy]').forEach(i=>i.loading='eager')"


def snap(pg, name):
    pg.wait_for_timeout(900); pg.screenshot(path=str(OUT / f"{name}.jpg"), type="jpeg", quality=82); print("wrote", name)


with sync_playwright() as p:
    b = p.chromium.launch()
    for k, d in DIRS.items():
        if args.only and k != args.only:
            continue
        pg = b.new_page(viewport={"width": 1440, "height": 900})
        pg.goto(BASE + d, wait_until="networkidle"); pg.mouse.move(1000, 400); pg.wait_for_timeout(2600); snap(pg, f"{k}-home-desktop")
        for name, path in PAGES:
            pg.goto(BASE + d + path, wait_until="networkidle"); pg.evaluate(SHOW); pg.mouse.move(1, 1); snap(pg, f"{k}-{name}")
        pg.goto(BASE + d, wait_until="networkidle"); pg.evaluate(SHOW)
        if k == "a":
            pg.check('input[name="stuck"][value="ai"]'); pg.evaluate("window.scrollTo(0, document.getElementById('stuck').getBoundingClientRect().top + window.scrollY - 140)")
        elif k == "b":
            pg.evaluate("document.getElementById('case').scrollIntoView({block:'start'}); window.scrollBy(0,-60)"); pg.focus('.mk[data-mk="2"]')
        else:
            pg.wait_for_timeout(2400); pg.click('.pb[data-problem="identity"]')
        pg.mouse.move(1, 1) if k != "b" else None; snap(pg, f"{k}-interaction"); pg.close()
        m = b.new_page(viewport={"width": 375, "height": 760}, device_scale_factor=2, is_mobile=True, has_touch=True)
        m.goto(BASE + d, wait_until="networkidle"); snap(m, f"{k}-home-mobile")
        m.goto(BASE + d + "services/ai-visibility/", wait_until="networkidle"); snap(m, f"{k}-service-mobile"); m.close()
    b.close()
if not args.only:
    for f in ("current-home-desktop.jpg", "current-home-mobile.jpg"):
        shutil.copyfile(ROOT / "phase-2" / "screenshots" / f, OUT / f); print("copied", f)
