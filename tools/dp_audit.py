#!/usr/bin/env python3
"""Browser audit of the staged digital presence production candidate.

    python3 tools/dp_audit.py http://localhost:8765/luckydomains-design-concepts /path/to/axe.min.js [--json out.json]

Reads the page list from digital-presence-production-candidate/STAGING.json (legacy redirect stubs
are left out, they only redirect). For every page, in Chromium, Firefox and WebKit where they
start, at six widths: HTTP status, horizontal overflow, console errors, broken images, missing alt
text, text under 12px, and touch targets under 24px. In Chromium at 375 and 1440px: axe-core
(WCAG 2.1 A and AA plus best practices). Then layout shift on a fresh load, reduced motion, and
no JavaScript.
"""
import json, sys
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
BASE = sys.argv[1].rstrip("/")
AXE = Path(sys.argv[2]).read_text()
OUT = sys.argv[sys.argv.index("--json") + 1] if "--json" in sys.argv else None
STG = "/digital-presence-production-candidate/"
pages = json.loads((ROOT / "digital-presence-production-candidate" / "STAGING.json").read_text())["pages"]
PAGES = [STG + (p[:-10] if p.endswith("index.html") else p) for p in pages if p.endswith("index.html") or p == "404.html"]
if "--only" in sys.argv:
    PAGES = [p for p in PAGES if sys.argv[sys.argv.index("--only") + 1] in p]
WIDTHS = [320, 375, 390, 768, 1024, 1440]
res = {"base": BASE, "pages": len(PAGES), "widths": WIDTHS, "engines": {}, "problems": [], "axe": {}, "cls": {}, "reduced": {}, "nojs": {}}
P = res["problems"]
CHECK = """(() => {
 const vis = e => { const r = e.getBoundingClientRect(), s = getComputedStyle(e); return r.width > 0 && r.height > 0 && s.visibility !== 'hidden' && s.display !== 'none'; };
 return {
  ov: document.documentElement.scrollWidth - document.documentElement.clientWidth,
  broken: [...document.images].filter(i => i.complete && i.naturalWidth === 0).map(i => i.src),
  noalt: [...document.images].filter(i => !i.hasAttribute('alt')).length,
  tiny: [...document.querySelectorAll('body *')].filter(e => vis(e) && [...e.childNodes].some(n => n.nodeType === 3 && n.textContent.trim()) && parseFloat(getComputedStyle(e).fontSize) < 12).map(e => (e.className || e.tagName) + ':' + getComputedStyle(e).fontSize).slice(0, 4),
  small: [...document.querySelectorAll('a,button,select,input:not([type=hidden]):not([name=botcheck]),textarea,summary')].filter(e => vis(e) && e.getBoundingClientRect().height < 24 && !e.closest('p,li,dd,figcaption,cite,h1,h2,h3,h4,label')).map(e => (e.textContent || e.name || '').trim().slice(0, 28)).slice(0, 4)
 }; })()"""
with sync_playwright() as pw:
    for eng in ("chromium", "firefox", "webkit"):
        try:
            b = getattr(pw, eng).launch()
        except Exception as e:
            res["engines"][eng] = "could not start: " + str(e).splitlines()[0][:120]; continue
        res["engines"][eng] = "ran"
        for w in WIDTHS:
            ctx = b.new_context(viewport={"width": w, "height": 800})
            for path in PAGES:
                pg = ctx.new_page(); errs = []
                pg.on("console", lambda m, e=errs: e.append(m.text) if m.type == "error" else None)
                pg.on("pageerror", lambda x, e=errs: e.append(str(x)))
                r = pg.goto(BASE + path, wait_until="networkidle")
                if r.status != 200: P.append(f"{eng} {w} {path}: HTTP {r.status}")
                pg.evaluate("document.querySelectorAll('.reveal').forEach(e=>e.classList.add('in'));document.querySelectorAll('[data-prog]').forEach(e=>e.classList.add('on'));document.querySelectorAll('img[loading=lazy]').forEach(i=>i.loading='eager')")
                pg.wait_for_timeout(250)
                c = pg.evaluate(CHECK)
                if c["ov"] > 0: P.append(f"{eng} {w} {path}: horizontal overflow {c['ov']}px")
                if errs: P.append(f"{eng} {w} {path}: console {errs[:2]}")
                if c["broken"]: P.append(f"{eng} {w} {path}: broken images {c['broken'][:2]}")
                if c["noalt"]: P.append(f"{eng} {w} {path}: {c['noalt']} images without alt")
                if c["tiny"]: P.append(f"{eng} {w} {path}: text under 12px {c['tiny']}")
                if c["small"] and w <= 390: P.append(f"{eng} {w} {path}: touch targets under 24px {c['small']}")
                if eng == "chromium" and w in (375, 1440):
                    pg.wait_for_timeout(700); pg.evaluate(AXE)
                    v = pg.evaluate("axe.run(document,{runOnly:['wcag2a','wcag2aa','wcag21a','wcag21aa','best-practice']}).then(r=>r.violations.map(v=>({id:v.id,n:v.nodes.length,ex:v.nodes[0].html.slice(0,120)})))")
                    for x in v: res["axe"].setdefault(x["id"], []).append([w, path, x["n"], x["ex"]])
                pg.close()
            ctx.close()
        b.close()
    b = pw.chromium.launch()
    # layout shift, measured on a fresh load at two widths
    for w, mob in ((1440, False), (375, True)):
        ctx = b.new_context(viewport={"width": w, "height": 900 if not mob else 760}, is_mobile=mob)
        for path in PAGES:
            pg = ctx.new_page(); pg.goto(BASE + path, wait_until="load")
            v = pg.evaluate("""() => new Promise(res => { let cls = 0; new PerformanceObserver(l => { for (const e of l.getEntries()) if (!e.hadRecentInput) cls += e.value }).observe({type:'layout-shift',buffered:true}); setTimeout(() => res(+cls.toFixed(4)), 2200) })""")
            res["cls"][f"{w} {path}"] = v
            if v > 0.1: P.append(f"layout shift {v} at {w} on {path}")
            pg.close()
        ctx.close()
    # reduced motion
    ctx = b.new_context(viewport={"width": 1440, "height": 900}, reduced_motion="reduce")
    for path in PAGES:
        pg = ctx.new_page(); pg.goto(BASE + path, wait_until="networkidle"); pg.wait_for_timeout(400)
        r = pg.evaluate("""({anim: document.getAnimations().filter(a=>a.playState==='running').length, hidden: [...document.querySelectorAll('main *')].filter(e=>e.offsetParent&&e.textContent.trim()&&getComputedStyle(e).opacity==='0').length})""")
        res["reduced"][path] = r
        if r["anim"] or r["hidden"]: P.append(f"reduced motion {path}: {r}")
        pg.close()
    ctx.close()
    # no JavaScript
    ctx = b.new_context(viewport={"width": 375, "height": 760}, java_script_enabled=False)
    for path in PAGES:
        pg = ctx.new_page(); pg.goto(BASE + path, wait_until="load")
        r = {"h1": pg.locator("h1").first.is_visible(), "nav": pg.locator("#nav a:visible").count(),
             "hidden": pg.locator("main *").evaluate_all("els => els.filter(e => e.offsetParent && e.textContent.trim() && getComputedStyle(e).opacity === '0').length")}
        res["nojs"][path] = r
        if not r["h1"] or r["nav"] < 6 or r["hidden"]: P.append(f"no JavaScript {path}: {r}")
        pg.close()
    ctx.close(); b.close()
for k, v in res["engines"].items(): print("engine", k, v)
for k, v in res["axe"].items(): print("axe", k, len(v), "hits, e.g.", v[0])
print("max layout shift", max(res["cls"].values()))
print("PROBLEMS" if P else "CLEAN"); [print("  -", x) for x in P[:40]]
if OUT: Path(OUT).write_text(json.dumps(res, indent=1))
