#!/usr/bin/env python3
"""Version 3 screenshots. Desktop 1440x900 viewport, mobile 375x760 at 2x.

    python3 tools/p3_shots.py http://localhost:8765/luckydomains-design-concepts/

Writes phase-3/screenshots/{a,b,c}-*.jpg, the refined set r-*.jpg, and copies the read-only production
references. Use --only a, b, c, or r to refresh one set.
"""
import argparse, shutil
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("base", nargs="?", default="http://localhost:8765/luckydomains-design-concepts/")
parser.add_argument("--only", choices=("a", "b", "c", "r"), help="refresh only one set of screenshots")
args = parser.parse_args()
BASE = args.base.rstrip("/") + "/phase-3/"
OUT = ROOT / "phase-3" / "screenshots"; OUT.mkdir(parents=True, exist_ok=True)
DIRS = {"a": "original-evolved/", "b": "editorial/", "c": "interactive/"}
PAGES = [("services", "services/"), ("ai", "services/ai-visibility/"), ("websites", "services/website-design/"), ("work", "work/luckydomains-io/")]
SHOW = "document.querySelectorAll('.reveal').forEach(e=>e.classList.add('in'));document.querySelectorAll('img[loading=lazy]').forEach(i=>i.loading='eager')"


def snap(pg, name):
    pg.wait_for_timeout(900); pg.screenshot(path=str(OUT / f"{name}.jpg"), type="jpeg", quality=82); print("wrote", name)


def refined(b):
    """Original Interactive, refined: the screenshots the owner asked for."""
    R = BASE + "interactive-refined/"
    pg = b.new_page(viewport={"width": 1440, "height": 900})
    pg.goto(R, wait_until="networkidle"); pg.mouse.move(700, 880); pg.wait_for_timeout(1800); snap(pg, "r-home-desktop")
    pg.evaluate(SHOW + ";document.querySelector('[data-prog]').classList.add('on')"); pg.wait_for_timeout(1800)
    pg.screenshot(path=str(OUT / "r-home-desktop-full.jpg"), type="jpeg", quality=72, full_page=True); print("wrote r-home-desktop-full")
    pg.locator("[data-map] .nd").nth(3).click(); pg.mouse.move(700, 880); pg.wait_for_timeout(700)
    pg.locator(".hero-map").screenshot(path=str(OUT / "r-map.jpg"), type="jpeg", quality=84); print("wrote r-map")
    pg.keyboard.press("Escape"); pg.check('input[name="stuck"][value="identity"]'); pg.wait_for_timeout(600)
    pg.locator("#start").screenshot(path=str(OUT / "r-diagnostic.jpg"), type="jpeg", quality=84); print("wrote r-diagnostic")
    pg.locator("#layers").screenshot(path=str(OUT / "r-progression.jpg"), type="jpeg", quality=84); print("wrote r-progression")
    for name, path in [("services", "services/"), ("websites", "services/website-design/"), ("seo", "services/seo/"), ("ai", "services/ai-visibility/"), ("entity", "services/entity-seo/"),
                       ("domains", "services/domains/"), ("about", "about/"), ("founder", "founder/")]:
        pg.goto(R + path, wait_until="networkidle"); pg.evaluate(SHOW); pg.mouse.move(1, 1); snap(pg, f"r-{name}")
    pg.goto(R + "tools/digital-presence-check/", wait_until="networkidle"); pg.evaluate(SHOW)
    for n, v in ((1, "yes"), (2, "yes"), (3, "no"), (4, "yes"), (5, "unsure"), (6, "yes")):
        pg.check(f'input[name="dpc-{n}"][value="{v}"]')
    pg.evaluate("window.scrollTo(0, 0)"); pg.mouse.move(1, 1); snap(pg, "r-check"); pg.close()
    m = b.new_page(viewport={"width": 375, "height": 760}, device_scale_factor=2, is_mobile=True, has_touch=True)
    m.goto(R, wait_until="networkidle"); m.wait_for_timeout(1600); snap(m, "r-home-mobile")
    m.goto(R + "services/ai-visibility/", wait_until="networkidle"); snap(m, "r-service-mobile")
    m.goto(R + "tools/digital-presence-check/", wait_until="networkidle"); m.check('input[name="dpc-1"][value="no"]'); m.evaluate("window.scrollTo(0, 0)"); snap(m, "r-check-mobile"); m.close()
    m1 = b.new_page(viewport={"width": 375, "height": 760}, is_mobile=True, has_touch=True)
    m1.goto(R, wait_until="networkidle"); m1.evaluate(SHOW + ";document.querySelector('[data-prog]').classList.add('on')"); m1.wait_for_timeout(1800)
    m1.screenshot(path=str(OUT / "r-home-mobile-full.jpg"), type="jpeg", quality=72, full_page=True); print("wrote r-home-mobile-full"); m1.close()


with sync_playwright() as p:
    b = p.chromium.launch()
    if args.only in (None, "r"):
        refined(b)
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
