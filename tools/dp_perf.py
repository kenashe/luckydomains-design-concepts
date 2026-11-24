#!/usr/bin/env python3
"""Lab performance measurements for the staged production candidate, taken in Chromium.

    python3 tools/dp_perf.py [base] [--json out.json]

These are NOT Lighthouse scores. Lighthouse could not be installed in the build environment.
This script measures the same underlying things directly through the Chrome DevTools Protocol:
first contentful paint, largest contentful paint, cumulative layout shift, total blocking time,
transfer size, and request count. The phone profile uses throttling close to Lighthouse's mobile
preset (150 ms latency, 1.6 Mbps down, 750 Kbps up, CPU slowed 4x) on a 412 by 823 viewport.
Each figure is the median of three cold loads.
"""
import json, statistics, sys
from playwright.sync_api import sync_playwright

BASE = (sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("--") else "https://kenashe.github.io/luckydomains-design-concepts").rstrip("/") + "/digital-presence-production-candidate/"
OUT = sys.argv[sys.argv.index("--json") + 1] if "--json" in sys.argv else None
PAGES = [("Home", ""), ("Services", "services/"), ("SEO service page", "services/seo/"), ("Digital Presence Check", "tools/digital-presence-check/"), ("Insights", "insights/"),
         ("Article", "insights/what-ai-search-reads-on-your-website/"), ("Founder", "founder/ken-ashe/"), ("Contact", "contact/")]
OBS = """() => { window.__m = {lcp: 0, cls: 0, tbt: 0, fcp: 0};
  new PerformanceObserver(l => { for (const e of l.getEntries()) window.__m.lcp = e.startTime }).observe({type: 'largest-contentful-paint', buffered: true});
  new PerformanceObserver(l => { for (const e of l.getEntries()) if (!e.hadRecentInput) window.__m.cls += e.value }).observe({type: 'layout-shift', buffered: true});
  new PerformanceObserver(l => { for (const e of l.getEntries()) window.__m.tbt += Math.max(0, e.duration - 50) }).observe({type: 'longtask', buffered: true});
  new PerformanceObserver(l => { for (const e of l.getEntries()) if (e.name === 'first-contentful-paint') window.__m.fcp = e.startTime }).observe({type: 'paint', buffered: true}); }"""


def run(b, url, phone):
    ctx = b.new_context(viewport={"width": 412, "height": 823} if phone else {"width": 1440, "height": 900}, device_scale_factor=1.75 if phone else 1, is_mobile=phone, has_touch=phone)
    pg = ctx.new_page(); cdp = ctx.new_cdp_session(pg); size = {"bytes": 0, "n": 0, "third": 0}
    cdp.send("Network.enable"); cdp.send("Network.setCacheDisabled", {"cacheDisabled": True})
    if phone:
        cdp.send("Network.emulateNetworkConditions", {"offline": False, "latency": 150, "downloadThroughput": 1.6 * 1024 * 1024 / 8, "uploadThroughput": 750 * 1024 / 8})
        cdp.send("Emulation.setCPUThrottlingRate", {"rate": 4})
    cdp.on("Network.loadingFinished", lambda e: size.__setitem__("bytes", size["bytes"] + e.get("encodedDataLength", 0)) or size.__setitem__("n", size["n"] + 1))
    host = url.split("/")[2]
    pg.on("request", lambda r: size.__setitem__("third", size["third"] + (0 if r.url.split("/")[2:3] == [host] or r.url.startswith("data:") else 1)))
    pg.add_init_script("(" + OBS + ")()")
    pg.goto(url, wait_until="load"); pg.wait_for_timeout(3500)
    m = pg.evaluate("window.__m"); ctx.close()
    return {"fcp": m["fcp"], "lcp": m["lcp"], "cls": m["cls"], "tbt": m["tbt"], "kb": size["bytes"] / 1024, "requests": size["n"], "third": size["third"]}


res = {"base": BASE, "pages": {}}
with sync_playwright() as p:
    b = p.chromium.launch()
    for name, path in PAGES:
        row = {}
        for label, phone in (("phone", True), ("desktop", False)):
            runs = [run(b, BASE + path, phone) for _ in range(3)]
            row[label] = {k: round(statistics.median(r[k] for r in runs), 3 if k == "cls" else 0) for k in runs[0]}
        res["pages"][name] = row
        ph, d = row["phone"], row["desktop"]
        print(f"{name:24} phone: FCP {ph['fcp']/1000:.2f}s LCP {ph['lcp']/1000:.2f}s CLS {ph['cls']:.3f} TBT {ph['tbt']:.0f}ms | desktop: LCP {d['lcp']/1000:.2f}s CLS {d['cls']:.3f} | {d['kb']:.0f} KB, {d['requests']:.0f} requests, {d['third']:.0f} third-party")
    b.close()
if OUT:
    open(OUT, "w").write(json.dumps(res, indent=1))
