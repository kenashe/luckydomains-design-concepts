#!/usr/bin/env python3
"""Screenshots of the staged digital presence production candidate.

    python3 tools/dp_shots.py [base]

Writes digital-presence-production-candidate/review/screenshots/*.jpg from the staging export.
The base defaults to the local preview (http://localhost:8765/luckydomains-design-concepts).
"""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
BASE = (sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8765/luckydomains-design-concepts").rstrip("/") + "/digital-presence-production-candidate/"
OUT = ROOT / "digital-presence-production-candidate" / "review" / "screenshots"
OUT.mkdir(parents=True, exist_ok=True)
SHOW = ("document.querySelectorAll('.reveal').forEach(e=>e.classList.add('in'));document.querySelectorAll('[data-prog]').forEach(e=>e.classList.add('on'));"
        "document.querySelectorAll('img[loading=lazy]').forEach(i=>i.loading='eager')")
ARTICLE = "insights/what-ai-search-reads-on-your-website/"
PAGES = [("services", "services/"), ("website-design", "services/website-design/"), ("seo", "services/seo/"), ("ai-visibility", "services/ai-visibility/"), ("entity-seo", "services/entity-seo/"),
         ("domain-acquisition", "services/domain-acquisition/"), ("how-we-buy-domains", "how-we-buy-domains/"), ("insights", "insights/"), ("article", ARTICLE), ("about", "about/"),
         ("founder", "founder/ken-ashe/"), ("contact", "contact/"), ("news", "news/")]


def snap(pg, name, **kw):
    pg.screenshot(path=str(OUT / f"{name}.jpg"), type="jpeg", quality=80, **kw)
    print("wrote", name)


with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1440, "height": 900})
    pg.goto(BASE, wait_until="networkidle"); pg.mouse.move(700, 880); pg.wait_for_timeout(1800); snap(pg, "home-desktop")
    pg.evaluate(SHOW); pg.wait_for_timeout(1800); snap(pg, "home-desktop-full", full_page=True)
    pg.locator("[data-map] .nd").nth(3).click(); pg.mouse.move(700, 880); pg.wait_for_timeout(700)
    pg.locator(".hero-map").screenshot(path=str(OUT / "presence-map.jpg"), type="jpeg", quality=84); print("wrote presence-map")
    pg.keyboard.press("Escape"); pg.check('input[name="stuck"][value="identity"]'); pg.wait_for_timeout(600)
    pg.locator("#start").screenshot(path=str(OUT / "diagnostic.jpg"), type="jpeg", quality=84); print("wrote diagnostic")
    pg.locator("#layers").screenshot(path=str(OUT / "five-layers.jpg"), type="jpeg", quality=84); print("wrote five-layers")
    for name, path in PAGES:
        pg.goto(BASE + path, wait_until="networkidle"); pg.evaluate(SHOW); pg.mouse.move(1, 1); pg.wait_for_timeout(300); snap(pg, name)
    pg.goto(BASE + ARTICLE, wait_until="networkidle"); pg.evaluate(SHOW); pg.wait_for_timeout(300); snap(pg, "article-full", full_page=True)
    pg.goto(BASE + "tools/digital-presence-check/", wait_until="networkidle"); pg.evaluate(SHOW)
    for n, v in ((1, "yes"), (2, "yes"), (3, "no"), (4, "yes"), (5, "unsure"), (6, "yes")):
        pg.check(f'input[name="dpc-{n}"][value="{v}"]')
    pg.evaluate("window.scrollTo(0, 0)"); pg.mouse.move(1, 1); snap(pg, "digital-presence-check"); pg.close()
    m = b.new_page(viewport={"width": 375, "height": 760}, device_scale_factor=2, is_mobile=True, has_touch=True)
    for name, path in [("home-mobile", ""), ("service-mobile", "services/ai-visibility/"), ("article-mobile", ARTICLE), ("insights-mobile", "insights/"), ("check-mobile", "tools/digital-presence-check/"), ("contact-mobile", "contact/")]:
        m.goto(BASE + path, wait_until="networkidle"); m.wait_for_timeout(1600 if not path else 300); snap(m, name)
    m.close()
    m1 = b.new_page(viewport={"width": 375, "height": 760}, is_mobile=True, has_touch=True)
    m1.goto(BASE, wait_until="networkidle"); m1.evaluate(SHOW); m1.wait_for_timeout(1800); snap(m1, "home-mobile-full", full_page=True)
    m1.goto(BASE + ARTICLE, wait_until="networkidle"); m1.evaluate(SHOW); m1.wait_for_timeout(300); snap(m1, "article-mobile-full", full_page=True)
    b.close()
