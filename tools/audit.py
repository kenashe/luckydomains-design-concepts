#!/usr/bin/env python3
"""Browser audit with Playwright: horizontal overflow and console errors at 375, 768 and 1440,
axe-core accessibility rules, small touch targets, and a reduced-motion pass.

    python3 tools/audit.py http://localhost:8765/site/ [/path/to/axe.min.js]
"""
import sys, json
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8765/site/"
AXE = Path(sys.argv[2]).read_text() if len(sys.argv) > 2 else None
ROOT = Path(__file__).resolve().parent.parent
pages = sorted(str(p.parent.relative_to(ROOT)).replace(".", "") for p in ROOT.rglob("index.html") if ".git" not in p.parts)
pages = [(p + "/") if p else "" for p in pages]
problems, axe_total = [], {}
with sync_playwright() as pw:
    b = pw.chromium.launch()
    for w in (375, 768, 1440):
        ctx = b.new_context(viewport={"width": w, "height": 900})
        for path in pages:
            pg = ctx.new_page(); errs = []
            pg.on("console", lambda m, e=errs: e.append(m.text) if m.type == "error" else None)
            pg.on("pageerror", lambda x, e=errs: e.append(str(x)))
            pg.goto(BASE + path, wait_until="networkidle")
            pg.evaluate("document.querySelectorAll('.reveal,.rv,.rise').forEach(e=>e.classList.add('in'))")
            ov = pg.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
            if ov > 0: problems.append(f"{w}px {path or '/'}: horizontal overflow {ov}px")
            if errs: problems.append(f"{w}px {path or '/'}: console {errs[:2]}")
            if w == 375:
                small = pg.evaluate("""[...document.querySelectorAll('a,button')].filter(e=>{const r=e.getBoundingClientRect();const s=getComputedStyle(e);
                    return r.width>0&&r.height>0&&s.visibility!=='hidden'&&r.height<24&&!e.closest('p,li,dd,figcaption,cite')}).map(e=>e.textContent.trim().slice(0,30))""")
                if small: problems.append(f"375px {path or '/'}: targets under 24px tall: {small[:4]}")
            if w == 1440 and AXE:
                pg.wait_for_timeout(900)
                pg.evaluate(AXE)
                res = pg.evaluate("axe.run(document,{runOnly:['wcag2a','wcag2aa','wcag21aa','best-practice']}).then(r=>r.violations.map(v=>({id:v.id,impact:v.impact,n:v.nodes.length,ex:v.nodes[0].html.slice(0,140)})))")
                for v in res:
                    axe_total.setdefault(v["id"], []).append((path or "/", v["n"], v["ex"]))
            pg.close()
        ctx.close()
    # reduced motion: nothing should be animating and all content should be visible
    ctx = b.new_context(viewport={"width": 1440, "height": 900}, reduced_motion="reduce")
    for path in [p for p in pages if p.count("/") == 1 and p.startswith("concept")]:
        pg = ctx.new_page(); pg.goto(BASE + path, wait_until="networkidle"); pg.wait_for_timeout(500)
        r = pg.evaluate("""({anim: document.getAnimations().filter(a=>a.playState==='running').length,
            hidden: [...document.querySelectorAll('main *')].filter(e=>e.offsetParent&&e.textContent.trim()&&getComputedStyle(e).opacity==='0').length})""")
        print("reduced-motion", path, r)
        if r["anim"] or r["hidden"]: problems.append(f"reduced motion {path}: {r}")
        pg.close()
    b.close()
print(f"{len(pages)} pages x 3 widths")
for k, v in axe_total.items(): print("axe", k, len(v), "pages; e.g.", v[0])
print("PROBLEMS" if problems else "CLEAN"); [print("  -", x) for x in problems]
