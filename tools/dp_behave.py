#!/usr/bin/env python3
"""Interaction tests for the digital presence production candidate.

    python3 tools/dp_behave.py [staging-base] [candidate-base] [--engines chromium,firefox]

staging-base   the exported staging copy, default http://localhost:8765/luckydomains-design-concepts/digital-presence-production-candidate/
candidate-base the production-candidate checkout served at a site root, default http://localhost:8770/
               (python3 -m http.server 8770 --directory /path/to/luckydomains-checkout)

Staging checks cover what a reviewer sees. Candidate checks cover what only exists in the real
source: the contact form's own validation and its Web3Forms request (intercepted, never sent),
the ?need= prefill, the legacy redirect stubs, and that a page view makes no third-party request.
Runs in Chromium and Firefox, and in WebKit when it can start.
"""
import sys
from playwright.sync_api import sync_playwright

ENGINES = sys.argv[sys.argv.index("--engines") + 1].split(",") if "--engines" in sys.argv else ["chromium", "firefox", "webkit"]
sys.argv = [x for i, x in enumerate(sys.argv) if x != "--engines" and (i == 0 or sys.argv[i - 1] != "--engines")]
B = (sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8765/luckydomains-design-concepts/digital-presence-production-candidate/").rstrip("/") + "/"
P = (sys.argv[2] if len(sys.argv) > 2 else "http://localhost:8770/").rstrip("/") + "/"
ART = "insights/what-ai-search-reads-on-your-website/"
R = []
HOT = "document.querySelectorAll('[data-map] .nd.hot').length"
SVG = "document.querySelector('.pm-view svg').getAttribute('class')"
PULSE = "document.getAnimations().some(a=>a.effect&&a.effect.target&&a.effect.target.classList&&a.effect.target.classList.contains('pulse'))"


def ok(n, c):
    R.append(("PASS" if c else "FAIL", n))


with sync_playwright() as p:
    engines = {}
    for eng in ENGINES:
        try:
            b = getattr(p, eng).launch()
        except Exception:
            engines[eng] = "could not start"; continue
        engines[eng] = "ran"
        ctx = b.new_context(viewport={"width": 1440, "height": 900}); pg = ctx.new_page(); errs = []
        pg.on("pageerror", lambda e: errs.append(str(e))); pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
        # ---- homepage: presence map
        pg.goto(B, wait_until="networkidle")
        ok(f"{eng}: map starts fragmented", pg.evaluate(SVG).startswith("frag"))
        pg.mouse.move(5, 5); pg.wait_for_timeout(1500)
        ok(f"{eng}: map settles to recognized", pg.evaluate(SVG).startswith("rec"))
        ok(f"{eng}: six signals, one map", pg.locator("[data-map] .nd").count() == 6 and pg.locator("[data-map]").count() == 1)
        pg.wait_for_timeout(3600)
        ok(f"{eng}: a pulse runs when idle", pg.evaluate(PULSE) or pg.evaluate("new Promise(r=>setTimeout(()=>r(%s),1500))" % PULSE))
        pg.click(".pm-pause")
        ok(f"{eng}: pause button state", pg.get_attribute(".pm-pause", "aria-pressed") == "true" and pg.get_attribute(".pm-pause", "aria-label") == "Play map animation")
        pg.mouse.move(5, 5); pg.wait_for_timeout(4500); ok(f"{eng}: no pulse while paused", not pg.evaluate(PULSE))
        pg.click(".pm-pause")
        pg.click(".sg[data-state=fragmented]"); pg.wait_for_timeout(300)
        ok(f"{eng}: fragmented toggle", pg.evaluate(SVG).startswith("frag") and "Fragmented" in pg.inner_text(".pm-detail"))
        pg.click(".sg[data-state=recognized]"); pg.wait_for_timeout(1300)
        pg.locator("[data-map] .nd").nth(3).click()
        ok(f"{eng}: select signal by click", pg.evaluate(HOT) == 1 and "Profiles" in pg.inner_text(".pm-detail") and pg.locator(".pd-chips li").count() == 3
           and pg.get_attribute(".pd-link", "href").endswith("/services/entity-seo/"))
        pg.locator("[data-map] .nd").nth(3).click(); ok(f"{eng}: click again clears", pg.evaluate(HOT) == 0)
        pg.locator("[data-map] .nd").nth(0).focus(); pg.keyboard.press("Enter")
        ok(f"{eng}: select by keyboard", "Domain" in pg.inner_text(".pm-detail") and pg.locator("[data-map] .nd").nth(0).get_attribute("aria-pressed") == "true"
           and pg.get_attribute(".pd-link", "href").endswith("/services/domain-acquisition/"))
        pg.keyboard.press("Escape"); ok(f"{eng}: Escape clears selection", pg.evaluate(HOT) == 0)
        # ---- homepage: diagnostic, progression, structure
        ok(f"{eng}: diagnostic sits directly under the hero", pg.evaluate("document.querySelector('.hero').nextElementSibling.classList.contains('diag')"))
        pg.check("input[name=stuck][value=ai]")
        ok(f"{eng}: diagnostic shows a starting point", pg.is_visible(".dg-a[data-for=ai]") and "AI Visibility" in pg.inner_text(".dg-a.on")
           and pg.get_attribute(".dg-a.on a", "href").endswith("/services/ai-visibility/") and not pg.is_visible(".dg-empty"))
        ok(f"{eng}: diagnostic lights related signals", pg.evaluate(HOT) == 3)
        pg.focus("input[name=stuck][value=ai]"); pg.keyboard.press("ArrowUp")
        ok(f"{eng}: diagnostic by keyboard", pg.evaluate("document.querySelector('.dg-a.on').dataset.for") == "identity")
        pg.evaluate("document.querySelector('[data-prog]').scrollIntoView({block:'center'})"); pg.wait_for_timeout(500)
        ok(f"{eng}: progression activates on scroll", pg.evaluate("document.querySelector('[data-prog]').classList.contains('on')") and pg.locator("[data-prog] li a").count() == 5)
        ok(f"{eng}: homepage section order", pg.evaluate("[...document.querySelectorAll('main > section')].map(s=>s.id||s.className.split(' ')[0]).join(',')")
           == "hero,start,layers,services,story,ai-work,founder,section")
        ok(f"{eng}: no sticky sections on the homepage", pg.evaluate("[...document.querySelectorAll('main *')].filter(e=>getComputedStyle(e).position==='sticky').length") == 0)
        ok(f"{eng}: navigation order, no Work", pg.evaluate("[...document.querySelectorAll('#nav > a, #nav > .has-menu > a')].map(a=>a.textContent.trim()).join('|')")
           == "Services|About|Insights|Founder|Contact|Start a project")
        pg.goto(B, wait_until="networkidle"); pg.keyboard.press("Tab")
        ok(f"{eng}: skip link first", pg.evaluate("document.activeElement.textContent.trim()").startswith("Skip"))
        seq = []
        for _ in range(14):
            pg.keyboard.press("Tab"); seq.append(pg.evaluate("(()=>{const e=document.activeElement,s=getComputedStyle(e);return s.outlineStyle!=='none'||e.classList.contains('nd')})()"))
        ok(f"{eng}: focus visible on tab stops", all(seq))
        pg.click(".menu-btn"); ok(f"{eng}: services menu opens", pg.is_visible("#m-svc a") and pg.locator("#m-svc a").count() == 8)
        pg.keyboard.press("Escape"); ok(f"{eng}: Escape closes menu", not pg.is_visible("#m-svc a"))
        # ---- Digital Presence Check
        reqs = []
        pg.goto(B + "tools/digital-presence-check/", wait_until="networkidle"); pg.on("request", lambda r: reqs.append(r.url))
        ok(f"{eng}: check has ten questions, three options each", pg.locator(".dq").count() == 10 and pg.locator(".dq input").count() == 30)
        for n, v in ((1, "yes"), (2, "yes"), (3, "no"), (4, "yes"), (5, "unsure")):
            pg.check(f"input[name=dpc-{n}][value={v}]")
        st = pg.evaluate("[...document.querySelectorAll('.dpc-areas li')].map(l=>l.dataset.state+':'+l.querySelector('[data-status]').textContent)")
        ok(f"{eng}: check statuses", st == ["yes:Nothing flagged", "no:Worth a closer look", "unsure:Worth checking", "none:Not answered yet", "none:Not answered yet"])
        ok(f"{eng}: check summary and starting point", "5 of 10 answered" in pg.inner_text("[data-sum]") and "Website Design" in pg.inner_text("[data-next-t]"))
        pg.focus("input[name=dpc-6][value=yes]"); pg.keyboard.press("Space"); pg.keyboard.press("ArrowRight")
        ok(f"{eng}: check works by keyboard", pg.is_checked("input[name=dpc-6][value=no]"))
        for n in range(1, 11):
            pg.check(f"input[name=dpc-{n}][value=yes]")
        ok(f"{eng}: all yes is not called a pass", "does not mean there are no problems" in pg.inner_text("[data-sum]") and not pg.is_visible("[data-next]"))
        ok(f"{eng}: check stores and sends nothing", pg.evaluate("localStorage.length+sessionStorage.length") == 0 and pg.evaluate("document.cookie") == "" and not reqs and not ctx.cookies())
        pg.click("[data-reset]"); ok(f"{eng}: clear answers", pg.locator(".dq input:checked").count() == 0)
        ok(f"{eng}: not-an-audit statement visible", pg.locator("text=This is a preliminary self-check, not a technical audit.").first.is_visible())
        # ---- Insights and an article
        pg.goto(B + "insights/", wait_until="networkidle")
        ok(f"{eng}: library lists five articles", pg.locator(".ins-card").count() == 5 and pg.locator(".ins-card a").count() == 5)
        pg.locator(".ins-card a").first.click(); pg.wait_for_load_state("networkidle")
        ok(f"{eng}: library card opens the article", pg.url.endswith(ART) and pg.locator("h1").count() == 1)
        ok(f"{eng}: article has byline, draft label, reading time, sources", "Ken Ashe" in pg.inner_text(".art-by") and "Editorial draft" in pg.inner_text(".art-by")
           and "min read" in pg.inner_text(".art-by") and pg.locator("#sources li").count() >= 8)
        n_toc = pg.locator(".art-toc a").count(); n_h2 = pg.locator(".art-body h2").count()
        ok(f"{eng}: contents list matches the headings", n_toc == n_h2 and n_toc >= 6)
        pg.locator(".art-toc a").nth(2).click(); pg.wait_for_timeout(700)
        target = pg.locator(".art-toc a").nth(2).get_attribute("href")[1:]
        ok(f"{eng}: contents link scrolls to its section", pg.evaluate(f"Math.abs(document.getElementById('{target}').getBoundingClientRect().top) < 140"))
        ok(f"{eng}: contents list marks the section being read", pg.evaluate("(document.querySelector('.art-toc a[aria-current]')||{getAttribute:()=>''}).getAttribute('href')") == "#" + target)
        ok(f"{eng}: article links to services and related articles", pg.locator(".art-svc").count() >= 3 and pg.locator(".art-related .ins-card").count() == 2)
        ok(f"{eng}: article table scrolls inside its own box", pg.evaluate("document.documentElement.scrollWidth-document.documentElement.clientWidth") == 0)
        # ---- contact form on staging is disabled
        pg.goto(B + "contact/", wait_until="networkidle"); posts = []; pg.on("request", lambda r: posts.append(r.url) if r.method == "POST" else None)
        pg.fill("#name", "Review"); pg.click("#contact-form button[type=submit]"); pg.wait_for_timeout(400)
        ok(f"{eng}: staging contact form sends nothing", not posts and "disabled" in pg.inner_text("#form-status") and pg.get_attribute("#contact-form", "data-access-key") == "")
        ok(f"{eng}: inquiry options match the services", pg.locator("#need option").count() == 8 and pg.locator("#need option", has_text="AI visibility").count() == 1)
        pg.goto(B + "services/seo/", wait_until="networkidle"); pg.click(".faq-q"); pg.wait_for_timeout(400)
        ok(f"{eng}: FAQ opens", pg.get_attribute(".faq-q", "aria-expanded") == "true")
        ok(f"{eng}: service page is static and light", pg.locator("[data-xchk]").count() == 0 and pg.locator("#look li").count() == 8
           and pg.evaluate("getComputedStyle(document.querySelector('h1')).color") == "rgb(12, 35, 64)")
        ok(f"{eng}: every staging page is noindex with a notice", pg.evaluate("document.querySelector('meta[name=robots]').content") == "noindex,nofollow,noarchive"
           and pg.locator(".stg-note").is_visible())
        ok(f"{eng}: no console errors on staging", not errs)
        # ---- candidate source: real contact form, prefill, stubs, third parties
        c = b.new_context(viewport={"width": 1280, "height": 900}); q = c.new_page(); sent = []; third = []

        def handle(route):
            sent.append(route.request.post_data or ""); route.fulfill(status=200, content_type="application/json", body='{"success": true}')
        q.route("https://api.web3forms.com/**", handle)
        q.on("request", lambda r: third.append(r.url) if not r.url.startswith(P) and "web3forms" not in r.url and not r.url.startswith("data:") else None)
        q.goto(P + "contact/?need=seo", wait_until="networkidle")
        ok(f"{eng}: candidate ?need= prefill", q.input_value("#need") == "SEO and search visibility")
        q.click("#contact-form button[type=submit]"); q.wait_for_timeout(300)
        ok(f"{eng}: candidate form validates before sending", "Please fill in" in q.inner_text("#form-status") and not sent)
        q.fill("#name", "Test"); q.fill("#email", "test@example.com"); q.fill("#target", "example.com"); q.select_option("#timeline", "1 to 3 months"); q.fill("#message", "Automated check. Intercepted, never sent.")
        q.click("#contact-form button[type=submit]"); q.wait_for_timeout(900)
        ok(f"{eng}: candidate form posts to Web3Forms with the key, subject and honeypot (intercepted)", len(sent) == 1 and "access_key" in sent[0] and "luckydomains.io: SEO and search visibility / example.com" in sent[0] and "Thanks!" in q.inner_text("#form-status"))
        ok(f"{eng}: candidate form keeps the honeypot and mailto fallback", q.locator("input[name=botcheck]").count() == 1 and q.locator('#contact-form a[href="mailto:info@luckydomains.io"]').count() == 1)
        for stub, dest in (("services.html", "services/"), ("about.html", "about/"), ("contact.html", "contact/"), ("how-we-buy-domains.html", "how-we-buy-domains/"), ("news/website-relaunch.html", "news/website-relaunch/")):
            q.goto(P + stub, wait_until="networkidle"); q.wait_for_timeout(300)
            ok(f"{eng}: legacy stub {stub} redirects", q.url == P + dest)
        q.goto(P + "services.html#seo", wait_until="networkidle"); q.wait_for_timeout(400)
        ok(f"{eng}: legacy anchor services.html#seo lands on the SEO card", q.url == P + "services/#seo" and q.locator("#seo").count() == 1)
        for path in ("", "services/website-design/", ART, "tools/digital-presence-check/", "founder/ken-ashe/", "news/website-relaunch/"):
            q.goto(P + path, wait_until="networkidle")
        ok(f"{eng}: candidate pages make no third-party request", not third)
        ok(f"{eng}: candidate pages are indexable, drafts excepted", q.goto(P).ok and q.locator("meta[name=robots]").count() == 0
           and (q.goto(P + ART).ok and q.get_attribute("meta[name=robots]", "content") == "noindex"))
        c.close()
        # ---- phone
        m = b.new_context(viewport={"width": 375, "height": 760}, has_touch=True, is_mobile=(eng != "firefox")).new_page()
        m.goto(B, wait_until="networkidle"); m.wait_for_timeout(1500)
        m.locator("[data-map] .nd").nth(1).tap(); ok(f"{eng}: tap selects a signal on a phone", "Website" in m.inner_text(".pm-detail"))
        m.click("#nav-toggle"); ok(f"{eng}: mobile menu opens", m.get_attribute("#nav-toggle", "aria-expanded") == "true" and m.locator("#nav a:visible").count() >= 6)
        m.keyboard.press("Escape"); ok(f"{eng}: Escape closes mobile menu", m.get_attribute("#nav-toggle", "aria-expanded") == "false")
        m.evaluate("document.querySelector('.dg-o input[value=domain]').scrollIntoView({block:'center'})"); m.locator(".dg-o:has(input[value=domain])").tap()
        ok(f"{eng}: recommendation appears without scrolling back", m.evaluate("document.querySelector('.dg-a.on').getBoundingClientRect().top < innerHeight"))
        m.goto(B + ART, wait_until="networkidle")
        ok(f"{eng}: article on a phone has no sideways scroll and a contents box", m.evaluate("document.documentElement.scrollWidth-document.documentElement.clientWidth") == 0 and m.locator(".art-toc").is_visible())
        b.close()
    b = p.chromium.launch()
    q = b.new_context(reduced_motion="reduce", viewport={"width": 1440, "height": 900}).new_page(); q.goto(B, wait_until="networkidle"); q.wait_for_timeout(3500)
    ok("reduced motion: nothing animating", q.evaluate("document.getAnimations().filter(a=>a.playState==='running').length") == 0)
    ok("reduced motion: map recognized, pause hidden", q.evaluate(SVG).startswith("rec") and not q.is_visible(".pm-pause"))
    q.locator("[data-map] .nd").nth(2).click(); ok("reduced motion: selection still works", "Search" in q.inner_text(".pm-detail"))
    n = b.new_context(java_script_enabled=False, viewport={"width": 375, "height": 760}).new_page(); n.goto(B)
    ok("no JavaScript: map shows six signals as text", n.locator(".pm-fb li:visible").count() == 6)
    ok("no JavaScript: all five recommendations listed", n.locator(".dg-a:visible").count() == 5)
    ok("no JavaScript: content visible", n.evaluate("[...document.querySelectorAll('.reveal')].every(e=>getComputedStyle(e).opacity==='1')"))
    n.goto(B + "tools/digital-presence-check/"); ok("no JavaScript: check lists areas with service links", n.locator(".dpc-areas .da-b a:visible").count() == 5 and n.is_visible(".dpc-nojs"))
    n.goto(B + ART); ok("no JavaScript: article and contents list readable", n.locator(".art-toc a:visible").count() >= 6 and n.locator(".art-body h2:visible").count() >= 6)
    n.goto(B + "services/seo/"); ok("no JavaScript: FAQ answers visible", n.evaluate("[...document.querySelectorAll('.faq-a')].every(e=>e.offsetHeight>20)"))
    n.goto(B + "contact/"); ok("no JavaScript: contact page offers the email address", n.locator('a[href="mailto:info@luckydomains.io"]:visible').count() >= 2)
    b.close()
print(engines)
F = [r for r in R if r[0] == "FAIL"]
print(len(R), "checks,", len(F), "failed")
for f in F:
    print("  ", f)
