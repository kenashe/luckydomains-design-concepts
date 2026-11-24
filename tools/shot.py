#!/usr/bin/env python3
"""Quick screenshot helper: python3 tools/shot.py <url-path> <out.png> [width] [height] [full]"""
import sys
from playwright.sync_api import sync_playwright
path, out = sys.argv[1], sys.argv[2]
w = int(sys.argv[3]) if len(sys.argv) > 3 else 1440
h = int(sys.argv[4]) if len(sys.argv) > 4 else 900
full = len(sys.argv) > 5 and sys.argv[5] == "full"
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": w, "height": h}, device_scale_factor=1)
    errs = []
    pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto("http://localhost:8765/site/" + path, wait_until="networkidle")
    if full:
        # trigger reveals
        pg.evaluate("document.querySelectorAll('.reveal,.rv,.rise').forEach(e=>e.classList.add('in'));document.querySelectorAll('img[loading=lazy]').forEach(i=>i.loading='eager')")
        pg.wait_for_timeout(1100)
    else:
        pg.wait_for_timeout(700)
    pg.screenshot(path=out, full_page=full)
    ov = pg.evaluate("document.documentElement.scrollWidth - window.innerWidth")
    print(out, "overflow-x:", ov, "errors:", errs[:5])
    b.close()
