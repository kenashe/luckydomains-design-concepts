"""Version 3 shared builder. Every page uses the ORIGINAL production markup and class names
(site-header, hero, section, section-soft, sec-head, card, icon-badge, ul.check, steps, split,
panel, cta-band, faq, contact-grid, site-footer) on top of phase-3/shared/original.css, a
verbatim copy of the production stylesheet. Concepts add their own layer on top.
"""
import json, html
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
C = json.loads((ROOT / "phase-3" / "shared" / "content.json").read_text())
E = html.escape
S = {s["id"]: s for s in C["services"]}
L = {l["id"]: l for l in C["stack"]}
PG = C["pages"]
NOTICE = "Design concept only. Not the live Lucky Domains website."
PAGES = [("", "home"), ("services/", "services"), ("services/website-design/", "websites"), ("services/seo/", "seo"),
         ("services/ai-visibility/", "ai"), ("services/entity-seo/", "entity"), ("services/domains/", "domains"),
         ("how-we-buy-domains/", "buy"), ("work/", "work"), ("work/luckydomains-io/", "case"), ("about/", "about"),
         ("founder/", "founder"), ("insights/", "insights"), ("insights/domains-identity-for-ai-agents/", "article"),
         ("news/", "news"), ("contact/", "contact")]
LAYER_OF = {"websites": "website", "seo": "search", "ai": "ai", "entity": "entity", "domains": "domain", "buy": "domain"}

_I = {
 "check": '<path d="M20 6L9 17l-5-5"/>', "target": '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="4.5"/><circle cx="12" cy="12" r="1"/>',
 "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>', "monitor": '<rect x="3" y="4" width="18" height="14" rx="2"/><path d="M3 9h18M8 21h8"/>',
 "search": '<circle cx="11" cy="11" r="7"/><path d="M21 21l-4.3-4.3"/>', "shield": '<path d="M12 2l8 4v6c0 5-3.5 8-8 10-4.5-2-8-5-8-10V6z"/>',
 "trend": '<path d="M3 17l5-5 4 4 8-8"/><path d="M21 8v5h-5"/>', "users": '<circle cx="9" cy="8" r="3.2"/><path d="M3.5 20a5.5 5.5 0 0 1 11 0"/><path d="M16 3.6a3.2 3.2 0 0 1 0 6.2M18 14c2.5.6 4 2.3 4 6"/>',
 "chart": '<path d="M4 4v16h16"/><path d="M7 14l3-3 3 3 5-6"/>', "spark": '<path d="M12 3l1.8 5.2L19 10l-5.2 1.8L12 17l-1.8-5.2L5 10l5.2-1.8z"/><path d="M19 17l.7 2 2 .7-2 .7-.7 2-.7-2-2-.7 2-.7z"/>',
 "mail": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/>', "doc": '<path d="M6 3h8l4 4v14H6z"/><path d="M14 3v4h4M9 12h6M9 16h6"/>',
 "layers": '<path d="M12 3l9 5-9 5-9-5z"/><path d="M3 13l9 5 9-5"/>', "globe": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a14 14 0 0 1 0 18M12 3a14 14 0 0 0 0 18"/>',
 "link": '<path d="M10 14a5 5 0 0 0 7 0l3-3a5 5 0 0 0-7-7l-1 1"/><path d="M14 10a5 5 0 0 0-7 0l-3 3a5 5 0 0 0 7 7l1-1"/>',
}
LAYER_ICON = {"domain": "target", "website": "monitor", "search": "search", "entity": "users", "ai": "spark"}


def icon(name, w="2"):
    return f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{_I[name]}</svg>'


class Ctx:
    def __init__(self, cfg, path):
        self.cfg, self.path = cfg, path
        d = path.count("/")
        self.c = "../" * d or "./"
        self.r = "../" * (d + 2)
    def to(self, p=""):
        return (self.c + p) if p else self.c
    def asset(self, n):
        return f"{self.r}shared/assets/{n}"
    def font(self, n):
        return f"{self.r}shared/fonts/{n}"
    def svc(self, sid):
        return self.to(S[sid]["path"])
    def cur(self, p):
        if p == "services/":
            return ' aria-current="page"' if self.path.startswith("services/") or self.path == "how-we-buy-domains/" else ""
        return ' aria-current="page"' if p and self.path.startswith(p) else ""


# ------------------------------------------------------------------ shell (original header and footer)
def head(ctx, title, desc):
    return f"""<!DOCTYPE html>
<html lang="en" class="no-js">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex,nofollow,noarchive">
<title>{E(title)} | Lucky Domains (version 3 concept {ctx.cfg['k']})</title>
<meta name="description" content="{E(desc)}">
<link rel="icon" href="{ctx.asset('favicon.ico')}" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="{ctx.asset('favicon-32.png')}">
<link rel="apple-touch-icon" href="{ctx.asset('apple-touch-icon.png')}">
<link rel="preload" href="{ctx.font('jakarta-normal-400-800.woff2')}" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{ctx.font('inter-normal-400-600.woff2')}" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{ctx.r}phase-3/shared/original.css">
<link rel="stylesheet" href="{ctx.r}phase-3/shared/v3.css">
<link rel="stylesheet" href="{ctx.c}css/style.css">
<script>document.documentElement.className='js'</script>
</head>"""


def header(ctx):
    sub = "".join(f'<li><a href="{ctx.svc(s["id"])}">{icon(s["icon"])}<span>{E(s["name"])}</span></a></li>' for s in C["services"])
    sub += f'<li class="menu-x"><a href="{ctx.to("services/")}">All services</a><a href="{ctx.to("how-we-buy-domains/")}">How we buy domains</a></li>'
    links = ""
    for label, p in C["nav"]:
        if p == "services/":
            links += f'<div class="has-menu"><a href="{ctx.to(p)}"{ctx.cur(p)}>{label}</a><button class="menu-btn" type="button" aria-expanded="false" aria-controls="m-svc"><span class="sr">Show service pages</span></button><ul class="menu" id="m-svc">{sub}</ul></div>'
        else:
            links += f'<a href="{ctx.to(p)}"{ctx.cur(p)}>{label}</a>'
    return f"""<aside class="review" aria-label="Review notice"><span>{NOTICE} <span class="rv-x">Version 3, concept {ctx.cfg['k']}: {E(ctx.cfg['name'])}.</span></span> <a href="{ctx.r}phase-3/">Version 3 concepts</a></aside>
<header class="site-header" id="site-header">
  <div class="container header-inner">
    <a class="brand" href="{ctx.to()}" aria-label="Lucky Domains, concept home"><img class="brand-logo" src="{ctx.asset('logo-wordmark.png')}" alt="Lucky Domains" width="170" height="42"></a>
    <nav class="nav" id="nav" aria-label="Primary">{links}<a href="{ctx.to('contact/')}" class="btn btn-accent btn-sm nav-cta">{C['navCta']}</a></nav>
    <button class="nav-toggle" id="nav-toggle" type="button" aria-label="Open menu" aria-controls="nav" aria-expanded="false"><span></span><span></span><span></span></button>
  </div>
</header>"""


def footer(ctx):
    sv = "".join(f'<li><a href="{ctx.svc(s["id"])}">{E(s["name"])}</a></li>' for s in C["services"]) + f'<li><a href="{ctx.to("how-we-buy-domains/")}">How we buy domains</a></li>'
    co = "".join(f'<li><a href="{ctx.to(p)}">{t}</a></li>' for t, p in [("Work", "work/"), ("About", "about/"), ("Founder", "founder/"), ("Insights", "insights/"), ("News & media", "news/"), ("Contact", "contact/")])
    return f"""<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div class="footer-brand"><a href="{ctx.to()}" class="footer-logo"><img src="{ctx.asset('logo-icon.png')}" alt="" width="42" height="42" loading="lazy"><span>Lucky Domains</span></a><p>{E(C['company']['footer'])}</p></div>
      <div class="footer-col"><h2 class="fh">Services</h2><ul>{sv}</ul></div>
      <div class="footer-col"><h2 class="fh">Company</h2><ul>{co}</ul></div>
      <div class="footer-col"><h2 class="fh">Get in touch</h2><ul><li><a href="mailto:{C['company']['email']}">{C['company']['email']}</a></li><li><a href="{ctx.to('contact/')}">{C['navCta']}</a></li><li><a href="{C['founder']['kenashe']}">KenAshe.ai</a></li></ul></div>
    </div>
    <div class="footer-bottom"><span>{E(C['company']['founderLine'])}</span><span>{NOTICE} Version 3, concept {ctx.cfg['k']}.</span></div>
  </div>
</footer>"""


def page(ctx, title, desc, body, cls=""):
    return f"""{head(ctx, title, desc)}
<body class="{cls}">
<a class="skip-link" href="#main">Skip to content</a>
{header(ctx)}
<main id="main">
{body}
</main>
{footer(ctx)}
<script src="{ctx.r}phase-3/shared/v3.js" defer></script>
<script src="{ctx.c}js/main.js" defer></script>
</body></html>"""


def write(rel, text):
    p = ROOT / rel; p.parent.mkdir(parents=True, exist_ok=True); p.write_text(text.strip() + "\n")


# ------------------------------------------------------------------ original components
def eyebrow(t, dark=False):
    return f'<span class="eyebrow{" eb-dark" if dark else ""}">{E(t)}</span>'


def check(items, cls="check"):
    return f'<ul class="{cls}">' + "".join("<li>%s</li>" % E(x) for x in items) + "</ul>"


def sec_head(eb, h, lead="", center=True, hid=""):
    lp = f'<p class="section-lead">{E(lead)}</p>' if lead else ""
    return f'<div class="sec-head{" center" if center else ""} reveal">{eyebrow(eb) if eb else ""}<h2{f" id={hid}" if hid else ""}>{E(h)}</h2>{lp}</div>'


def section(sid, inner, soft=False, cls="", layer=None, label=""):
    lay = f' data-layer="{layer}"' if layer else ""
    lab = f' data-toc="{E(label)}"' if label else ""
    return f'<section class="section{" section-soft" if soft else ""}{(" " + cls) if cls else ""}" id="{sid}"{lay}{lab}><div class="container">{inner}</div></section>'


def cards(items, cols=3, cls="card"):
    out = ""
    for it in items:
        ic = f'<div class="icon-badge">{icon(it["icon"])}</div>' if it.get("icon") else ""
        tag = f'<span class="tag">{E(it["tag"])}</span>' if it.get("tag") else ""
        ck = check(it["check"]) if it.get("check") else ""
        lk = f'<div class="svc-foot"><a class="link-arrow" href="{it["href"]}">{E(it.get("cta", "Learn more"))} {icon("arrow", "2.4")}</a></div>' if it.get("href") else ""
        out += f'<article class="{cls} svc reveal">{ic}{tag}<h3>{E(it["h"])}</h3><p>{E(it["p"])}</p>{ck}{lk}</article>'
    return f'<div class="grid grid-{cols}">{out}</div>'


def steps(items, cls="steps"):
    return f'<div class="{cls}">' + "".join(f'<div class="step reveal"><div class="n" aria-hidden="true"></div><h3>{E(x["name"])}</h3><p>{E(x["line"])}</p></div>' for x in items) + "</div>"


def panel(h, items, foot=""):
    return f'<div class="panel reveal"><h3>{E(h)}</h3>{check(items)}{foot}</div>'


def split(body, media, alt=False):
    return f'<div class="split{" alt" if alt else ""}"><div class="split-body">{body}</div><div class="split-media">{media}</div></div>'


def faq(items):
    return '<div class="faq">' + "".join(f'<div class="faq-item"><button class="faq-q" type="button" aria-expanded="false">{E(q)}</button><div class="faq-a"><div class="faq-a-inner"><p>{E(a)}</p></div></div></div>' for q, a in items) + "</div>"


def cta_band(ctx, h="Not sure where to start?", p=None, btn=None):
    p = p or ("Tell Ken what you are working on. " + C["company"]["consult"])
    return f'<section class="section section--tight" aria-label="Contact"><div class="container"><div class="cta-band reveal"><h2>{E(h)}</h2><p>{E(p)}</p><div class="btn-row" style="justify-content:center"><a class="btn btn-lg" href="{ctx.to("contact/")}">{E(btn or C["navCta"])}</a><a class="btn btn-ghost btn-lg cta-ghost" href="mailto:{C["company"]["email"]}">Email Ken</a></div></div></div></section>'


def note(text, kind="note", strong=""):
    s = f"<strong>{E(strong)}</strong> " if strong else ""
    return f'<p class="v3-note v3-{kind}">{s}{E(text)}</p>'


def evidence(ctx):
    g, b = C["evidenceGoogle"], C["evidenceBing"]
    return f'<div class="grid grid-2 evid">' + "".join(f'<article class="card reveal"><div class="icon-badge navy">{icon("doc")}</div><span class="tag">Source: {E(x["label"])}</span><p>{E(x["line"])}</p><div class="svc-foot"><a class="link-arrow" href="{x["url"]}">Read the source {icon("arrow", "2.4")}</a></div></article>' for x in (g, b)) + "</div>"


def page_hero(ctx, key, extra="", cta=True):
    p = PG[key]
    btn = f'<div class="btn-row"><a class="btn btn-accent btn-lg" href="{ctx.to("contact/")}">{C["navCta"]}</a><a class="btn btn-on-dark btn-lg" href="{ctx.to("services/")}">All services</a></div>' if cta else ""
    crumbs = '<nav class="crumbs" aria-label="Breadcrumb"><ol><li><a href="%s">Home</a></li>%s<li aria-current="page">%s</li></ol></nav>' % (ctx.to(), ('<li><a href="%s">Services</a></li>' % ctx.to("services/")) if ctx.path.startswith("services/") and ctx.path != "services/" else ("<li><a href=\"%s\">Work</a></li>" % ctx.to("work/") if ctx.path.startswith("work/") and ctx.path != "work/" else ("<li><a href=\"%s\">Insights</a></li>" % ctx.to("insights/") if ctx.path.startswith("insights/") and ctx.path != "insights/" else "")), E(p["eyebrow"]))
    return f'<section class="hero hero--page"><div class="container hero-inner">{crumbs}{eyebrow(p["eyebrow"], True)}<h1>{E(p["h1"])}</h1><p class="lead">{E(p["lead"])}</p>{btn}{extra}</div></section>'


def svc_cards(ctx, ids=None):
    return cards([dict(icon=S[i]["icon"], tag=S[i]["tag"], h=S[i]["h"], p=S[i]["short"], check=S[i]["check"], href=ctx.svc(i), cta="Explore " + S[i]["name"]) for i in (ids or [s["id"] for s in C["services"]])], 3)


def diagnostic(ctx, sid="dg"):
    d = C["diagnostic"]
    radios = "".join(f'<label class="dg-o"><input type="radio" name="stuck" value="{o["id"]}"><span>{E(o["label"])}</span></label>' for o in d["options"])
    ans = "".join(f'<div class="dg-a" data-for="{o["id"]}"><span class="eyebrow eb-dark">Start here</span><h3>{E(o["start"])}</h3><p>{E(o["why"])}</p><ol class="dg-steps">{"".join("<li>%s</li>" % E(x) for x in o["first"])}</ol><a class="btn btn-accent" href="{ctx.svc(o["service"])}">See {E(o["start"])}</a></div>' for o in d["options"])
    return f'<div class="dg-in"><div class="reveal">{eyebrow("Quick diagnostic")}<h2 id="{sid}-h">{E(d["title"])}</h2><p class="section-lead">{E(d["intro"])}</p><fieldset class="dg-opts"><legend class="sr">Choose the problem that fits best</legend>{radios}</fieldset></div><div class="dg-out" aria-live="polite"><p class="dg-empty">Choose an option to see a recommended starting point.</p>{ans}</div></div>'


def contact_form():
    opts = "".join("<option>%s</option>" % E(x) for x in C["contact"]["paths"])
    f = lambda i, l, ctl: f'<div class="field"><label for="{i}">{l}</label>{ctl}</div>'
    return (f'<form class="form-card" novalidate data-inert>{f("f-name", "Name", "<input id=f-name type=text autocomplete=off>")}'
            f'{f("f-email", "Email", "<input id=f-email type=email autocomplete=off>")}{f("f-what", "What is this about?", "<select id=f-what>" + opts + "</select>")}'
            f'{f("f-msg", "Tell Ken what you are working on", "<textarea id=f-msg></textarea>")}'
            f'<button type="button" class="btn btn-accent btn-lg">Send to Ken</button><p class="form-note cf-note" role="status">{E(C["contact"]["notice"])}</p></form>')


def lab_cards():
    return '<div class="grid grid-3 lab">' + "".join(f'<article class="card reveal"><span class="tag">{E(x["status"])} · {E(x["kind"])}</span><h3><a href="{x["url"]}">{E(x["name"])}</a></h3><p>{E(x["line"])}</p><p class="lim">{E(x["limit"])}</p></article>' for x in C["lab"]) + "</div>"


def work_cards(ctx, items=None):
    out = ""
    for x in (items or C["work"]):
        demo = x.get("concept")
        href = ctx.to("work/luckydomains-io/") if x.get("featured") else (x["evidence"][0][1] if x["evidence"] else "")
        lk = f'<div class="svc-foot"><a class="link-arrow" href="{href}">{"Read the case study" if x.get("featured") else E(x["evidence"][0][0]) if x["evidence"] else ""} {icon("arrow", "2.4")}</a></div>' if href else ""
        out += f'<article class="card svc wk{" wk-demo" if demo else ""} reveal" data-layers="{" ".join(x["layers"])}"><span class="tag">{E(x["category"])}{" · Concept content" if demo else ""}</span><h3>{E(x["title"])}</h3><p>{E(x["summary"])}</p><p class="wk-m">{E(x["client"])}{" · " + E(x["status"]) if x["status"] and not demo else ""}</p>{lk}</article>'
    return f'<div class="grid grid-3 wks">{out}</div>'


# ------------------------------------------------------------------ inner page sections: lists of (id, label, html)
def p_services(ctx):
    p = PG["services"]
    eng = "".join(f'<div class="price reveal"><h3>{E(e["name"])}</h3><p class="desc"><strong>{E(e["kind"])}.</strong> {E(e["line"])}</p>{check(e["check"])}</div>' for e in p["engagements"])
    return [("svc", "The services", section("svc", sec_head("What we do", "Domain, website, search, entity, AI.", C["stackReinforce"]) + svc_cards(ctx))),
            ("engage", "Ways to work together", section("engage", sec_head("Engagements", "Scoped in writing, before work starts.", p["pricing"]) + f'<div class="price-grid eng">{eng}</div>' + note(C["notPromised"], "note", "What we will not promise."), True)),
            ("not", "What we are not", section("not", '<div class="split"><div class="split-body">' + sec_head("Deliberately specialized", "What Lucky Domains is not", "", False) + '</div><div class="split-media">' + check(p["notList"], "nope") + '</div></div>'))]


def p_websites(ctx):
    w = PG["websites"]; a = w["architecture"]
    col = lambda k: f'<div class="arch-c" data-state="{k}"><h3>{E(a[k]["label"])}</h3><ul>{"".join("<li>%s</li>" % E(x) for x in a[k]["items"])}</ul></div>'
    paths = cards([dict(icon="search" if i == 0 else "monitor", h=x["name"], p=x["line"]) for i, x in enumerate(w["paths"])], 2)
    found = cards([dict(h=x["name"], p=x["line"]) for x in w["foundations"]], 4, "card card-sm")
    return [("approach", "The approach", section("approach", split(sec_head("The approach", "Structure before style.", "", False) + "".join(f'<p class="section-lead">{E(x)}</p>' for x in w["intro"]), panel("What a build includes", w["includes"])), layer="website")),
            ("paths", "Two ways to start", section("paths", sec_head("Two ways to start", "Consult on the site you have, or build the one you need.") + paths, True)),
            ("process", "How a project runs", section("process", sec_head("How a project runs", "Six steps, from discovery to improvement.") + steps(w["process"], "steps steps-6"))),
            ("foundation", "Built into every site", section("foundation", sec_head("Built into every site", "The foundation search engines and AI systems rely on.") + found + note(w["aiNote"], "note", "AI-assisted, human-reviewed."), True)),
            ("architecture", "Information architecture", section("architecture", sec_head("Information architecture", a["title"], a["caption"]) + f'<div class="arch" data-ba><div class="ba-bar" role="group" aria-label="Show page map"><button type="button" class="ba-b" data-show="before" aria-pressed="false">Before</button><button type="button" class="ba-b" data-show="after" aria-pressed="true">After</button></div><div class="arch-g">{col("before")}{col("after")}</div></div>')),
            ("faq", "Questions", section("faq", sec_head("Questions", "Website projects, answered.") + faq(w["faq"]) + f'<p class="center v3-more">{E(w["not"])} {E(w["proof"])} <a href="{ctx.to("work/luckydomains-io/")}">Read the case study</a>.</p>', True))]


def p_seo(ctx):
    s = PG["seo"]
    return [("areas", "What SEO covers", section("areas", sec_head("SEO & Search Visibility", "The fundamentals still decide who gets found.", "And they now feed AI-powered search too.") + cards([dict(icon=["trend", "doc", "link", "layers", "target", "shield", "search", "chart"][i], h=x["name"], p=x["line"]) for i, x in enumerate(s["areas"])], 4, "card card-sm"), layer="search")),
            ("expanding", "Why SEO is expanding", section("expanding", sec_head("Why SEO is expanding", "AI search is built on search.", "What the search engines themselves say.") + evidence(ctx), True)),
            ("process", "How we work", section("process", sec_head("How we work", "Five steps, repeated.") + steps(s["process"], "steps steps-5") + note(s["reporting"], "note", "Honest reporting."))),
            ("faq", "Questions", section("faq", sec_head("Questions", "SEO, answered.") + faq(s["faq"]), True))]


def p_ai(ctx):
    a = PG["ai"]
    goals = check(a["goals"])
    aud = cards([dict(icon=["users", "search", "spark"][i], h=x["name"], p=x["line"]) for i, x in enumerate(C["audiences"])], 3)
    return [("goal", "The goal", section("goal", split(sec_head("The goal", "Make your business easy to understand and easy to verify.", "", False) + '<p class="section-lead">Lucky Domains helps make a company:</p>' + goals, panel("What AI systems rely on", ["Crawlable pages with useful first-party content", "Structured data that matches the visible facts", "Consistent names, descriptions, and founders across profiles", "Credible third-party references", "Clear relationships between people, services, and places"])), layer="ai")),
            ("audiences", "Three audiences", section("audiences", sec_head("Where recognition happens", "People, search engines, and AI systems read the same evidence.") + aud, True)),
            ("deliver", "What the work includes", section("deliver", sec_head("What the work includes", "Nine deliverables, from baseline to monitoring.") + cards([dict(h=f"{i:02d}. {x['name']}", p=x["line"]) for i, x in enumerate(a["deliverables"], 1)], 3, "card card-sm"))),
            ("evidence", "What the sources say", section("evidence", sec_head("What the sources say", "No secret markup. Measurable, in part.", a["measure"]) + evidence(ctx) + note(C["notPromised"], "warn", "What we will not promise.") + note(C["noSecret"], "note"), True)),
            ("faq", "Questions", section("faq", sec_head("Questions", "AI visibility, answered.") + faq(a["faq"])))]


def p_entity(ctx):
    e = PG["entity"]
    aud = (f'<div class="grid grid-3 idg"><article class="card reveal"><div class="icon-badge">{icon("users")}</div><h3>For people</h3>{check(e["people"])}</article>'
           f'<article class="card reveal"><div class="icon-badge">{icon("globe")}</div><h3>For businesses</h3>{check(e["business"])}</article>'
           f'<article class="card reveal card-emerging"><div class="icon-badge navy">{icon("spark")}</div><span class="tag">Emerging research</span><h3>For AI agents</h3>{check(e["agents"])}<div class="svc-foot"><a class="link-arrow" href="{ctx.to(C["article"]["slug"])}">Read the research note {icon("arrow", "2.4")}</a></div></article></div>')
    lv = "".join(f'<div class="price reveal"><span class="tag">Level {i}</span><h3>{E(x["name"])}</h3><p class="desc">{E(x["line"])}</p>{check(x["check"])}</div>' for i, x in enumerate(e["levels"], 1))
    return [("what", "What entity SEO is", section("what", split(sec_head("What entity SEO is", "Your website can rank and still be misunderstood.", "", False) + "".join(f'<p class="section-lead">{E(x)}</p>' for x in e["what"]), panel("The evidence we work on", ["A clear canonical website", "Accurate structured data", "Consistent external profiles", "Unambiguous person and company relationships", "Credible third-party references", "Consistent public facts"])), layer="entity")),
            ("identity", "Identity for three audiences", section("identity", sec_head("Digital identity", "Identity for people, businesses, and, soon, agents.", "Agent identity is an emerging research area, not a mature service.") + aud, True)),
            ("levels", "Two levels", section("levels", sec_head("What the service includes", "Two levels, built on facts you already have.", "All structured data we write describes real facts already supported by you and your site.") + f'<div class="price-grid lv">{lv}</div>' + note(e["panel"], "warn", "Knowledge Panels."))),
            ("faq", "Questions", section("faq", sec_head("Questions", "Entity SEO, answered.") + faq(e["faq"]), True))]


def p_domains(ctx):
    d = PG["domains"]
    return [("anchor", "The anchor", section("anchor", split(sec_head("The anchor", "Every other signal points back to the name.", "", False) + f'<p class="section-lead">{E(d["anchor"])}</p>', panel("What's included", d["includes"])), layer="domain")),
            ("buy", "Buying a domain", section("buy", sec_head("Buying a domain", "Four steps, in the order they happen.") + steps(d["steps"]) + f'<p class="center v3-more"><a class="btn btn-ghost" href="{ctx.to("how-we-buy-domains/")}">How we buy domains, in detail</a></p>', True)),
            ("sell", "Selling a domain", section("sell", split(sec_head("Selling a domain", "A confidential, managed exit.", "", False) + f'<p class="section-lead">{E(d["selling"])}</p>' + note(d["terms"], "note", "Fee."), '<div class="reveal">' + check(d["not"], "nope") + "</div>", True))),
            ("faq", "Questions", section("faq", sec_head("Questions", "Domains, answered.") + faq(d["faq"]), True))]


def p_buy(ctx):
    b = PG["buy"]
    return [("process", "The process", section("process", sec_head("The process", "Four steps, in the order they happen.") + steps(b["steps"]), layer="domain")),
            ("fee", "How the fee works", section("fee", split(sec_head("How the fee works", "Success-based, agreed before outreach.", "", False) + "".join(f'<p class="section-lead">{E(x)}</p>' for x in b["fee"]) + f'<div class="btn-row"><a class="btn btn-accent" href="{ctx.to("contact/")}">Tell Ken the name you want</a><a class="btn btn-ghost" href="{ctx.svc("domains")}">Back to domains</a></div>', '<div class="reveal"><h3>What this is not</h3>' + check(PG["domains"]["not"], "nope") + "</div>"), True))]


def p_work(ctx):
    fw = C["work"][0]
    feat = f'<article class="split wk-feat reveal"><div class="split-body"><span class="tag">{E(fw["category"])} · {E(fw["status"])}</span><h2>{E(fw["title"])}</h2><p class="section-lead">{E(fw["summary"])}</p><a class="btn btn-accent" href="{ctx.to("work/luckydomains-io/")}">Read the case study</a></div><div class="split-media">{panel("Work completed", fw["done"][:4])}</div></article>'
    return [("featured", "Featured case study", section("featured", feat)),
            ("more", "More work", section("more", sec_head("More work", "Websites, entity work, and AI-assisted operations.", fw["noMetrics"]) + work_cards(ctx, C["work"][1:]), True)),
            ("lab", "From the lab", section("lab", sec_head("From the lab", "What Ken is testing.", C["labIntro"]) + lab_cards()))]


def p_case(ctx):
    w = C["work"][0]
    meta = "".join(f'<div class="stat"><div class="num">{E(v)}</div><div class="lbl">{E(k)}</div></div>' for k, v in [("Client", "Our own site"), ("Year", w["year"]), ("Status", "Live"), ("Internal links fixed", "93")])
    ev = "".join(f'<li><a href="{u}">{E(t)}</a></li>' for t, u in w["evidence"])
    return [("glance", "At a glance", section("glance", f'<div class="stats cs-stats reveal">{meta}</div>' + note(w["noMetrics"], "note"), layer="website")),
            ("problem", "Problem", section("problem", split(sec_head("Problem", "A site the business did not own.", "", False) + f'<p class="section-lead">{E(w["problem"])}</p>', panel("Approach", [w["approach"], w["built"]])), True)),
            ("done", "Work completed", section("done", sec_head("Work completed", "What changed.") + f'<div class="cs-done reveal">{check(w["done"])}</div>')),
            ("evidence", "Evidence available", section("evidence", split(sec_head("Evidence available", "Everything here can be checked.", "", False) + f'<ul class="ev">{ev}</ul>', '<div class="reveal"><h3>Lessons</h3>' + check(w["lessons"]) + "</div>"), True))]


def p_about(ctx):
    a = PG["about"]
    vals = "".join(f'<div class="value reveal"><div class="ic">{icon(["shield", "trend", "chart", "doc"][i])}</div><div><h3>{E(t)}</h3><p>{E(x)}</p></div></div>' for i, (t, x) in enumerate(a["values"]))
    layers = "".join(f'<li data-layer="{l["id"]}"><span class="ly-n">{l["n"]}</span><b>{E(l["name"])}</b><span>{E(l["short"])}</span></li>' for l in C["stack"])
    return [("story", "Our story", section("story", split(sec_head("Our story", "It started with the name.", "", False) + f'<p class="section-lead">{E(C["company"]["story"])}</p><p>{E(C["company"]["originalModel"])}</p>', f'<ol class="ab-stack reveal" aria-label="The five layers">{layers}</ol>'), layer="domain")),
            ("believe", "What we believe", section("believe", split(sec_head("What we believe", "Fortune favors the prepared.", "", False) + f'<p class="section-lead">{E(a["philosophy"])}</p>' + check(a["believe"]), f'<div class="grid" style="gap:22px">{vals}</div>'), True)),
            ("rhythm", "How we work", section("rhythm", sec_head("How we work", "Discipline you can see in the deliverables.") + steps(a["rhythm"]) + note(C["aiWork"]["intro"], "note", C["aiWork"]["principle"]))),
            ("founder", "The founder", section("founder", split(sec_head("The founder", C["company"]["founderLine"], "", False) + f'<p class="section-lead">{E(C["founder"]["bio"])}</p><a class="btn btn-ghost" href="{ctx.to("founder/")}">About Ken</a>', f'<figure class="founder-card reveal"><img src="{ctx.asset("ken-ashe-2026-square.jpg")}" alt="Ken Ashe, founder of Lucky Domains" width="460" height="460" loading="lazy"></figure>', True), True))]


def p_founder(ctx):
    f = C["founder"]
    cred = "".join(f'<div class="stat"><div class="num">{E(a)}</div><div class="lbl">{E(b)}</div></div>' for a, b in f["credentialsFull"])
    sp = "".join(f'<div class="value reveal"><div class="ic">{icon("users")}</div><div><h3>{E(y)} · {E(ev)}</h3><p>{E(t)}</p></div></div>' for y, ev, t in f["speaking"])
    links = "".join(f'<div class="info"><div class="ic">{icon("link")}</div><div><h3>{E(t)}</h3><p><a href="{u}">{E(d)}</a></p></div></div>' for t, u, d in f["links"])
    split2 = "".join(f'<article class="card reveal"><span class="tag">{E(a)}</span><p>{E(b)}</p></article>' for a, b in f["split"])
    return [("bio", "Background", section("bio", split(sec_head("Background", "Builder, operator, accountant.", "", False) + "".join(f'<p class="section-lead">{E(x)}</p>' for x in f["bioLong"]) + f'<blockquote class="v3-quote"><p>{E(f["quote"])}</p><cite>Ken Ashe</cite></blockquote>', f'<figure class="founder-card reveal"><img src="{ctx.asset(f["image"])}" alt="Portrait of Ken Ashe" width="460" height="460"></figure>'), layer="entity")),
            ("creds", "Credentials", section("creds", sec_head("Credentials", "Operating evidence, not the headline.", f["discipline"]) + f'<div class="stats creds reveal">{cred}</div><p class="center v3-more">Career: {E(", ".join(f["career"]))}. Member of <a href="{f["forbes"]}">Forbes Business Council</a>.</p>', True)),
            ("speaking", "Speaking and judging", section("speaking", split(sec_head("Speaking and judging", "On stage and on panels.", "", False) + f'<div class="grid" style="gap:22px">{sp}</div>', f'<div class="contact-side reveal">{links}</div>'))),
            ("sites", "Two sites, two jobs", section("sites", sec_head("Two sites, two jobs", "Where to find what.") + f'<div class="grid grid-2">{split2}</div>', True)),
            ("lab", "From the lab", section("lab", sec_head("From the lab", "What Ken is testing.", C["labIntro"]) + lab_cards()))]


def p_insights(ctx):
    a = C["article"]
    feat = f'<article class="split wk-feat reveal"><div class="split-body"><span class="tag">{E(a["kind"])} · {E(a["status"])}</span><h2>{E(a["title"])}</h2><p class="section-lead">{E(a["dek"])}</p><a class="btn btn-accent" href="{ctx.to(a["slug"])}">Read the draft</a></div><div class="split-media">{panel("In this note", [s[0] for s in a["sections"]])}</div></article>'
    items = C["insights"]["items"][:4]
    planned = cards([dict(icon=LAYER_ICON[i["layer"]], tag=i["kind"] + " · Planned", h=i["title"], p="Not yet published.") for i in items], 2)
    return [("featured", "Featured", section("featured", feat)),
            ("planned", "Planned articles", section("planned", sec_head("Planned articles", "What is coming.", C["insights"]["label"]) + planned + f'<p class="center v3-more">Ken publishes build logs and essays at <a href="{C["founder"]["kenashe"]}">KenAshe.ai</a>.</p>', True))]


def p_article(ctx):
    a = C["article"]
    body = "".join(f'<section class="art-s" id="a{i}" data-toc="{E(h)}"><h2>{E(h)}</h2>{"".join("<p>%s</p>" % E(x) for x in ps)}</section>' for i, (h, ps) in enumerate(a["sections"], 1))
    src = "".join(f'<li><a href="{u}">{E(t)}</a></li>' for t, u in a["sources"])
    return [("article", "Article", f'<section class="section article" id="article"><div class="container art-wrap"><p class="v3-note v3-warn"><strong>{E(a["status"])}</strong> Concept content for review.</p><p class="art-dek">{E(a["dek"])}</p>{body}<section class="art-s" id="sources" data-toc="Sources"><h2>Sources</h2><ul class="ev">{src}</ul></section></div></section>')]


def p_news(ctx):
    n = PG["news"]; r = n["release"]; s = n["sample"]; f = C["founder"]
    sp = "".join(f'<li><strong>{E(y)} · {E(ev)}.</strong> {E(t)}</li>' for y, ev, t in f["speaking"])
    return [("news", "Company news", section("news", sec_head("Company news", "Announcements.", "", False) + f'<div class="grid grid-2"><article class="card reveal"><span class="tag">{E(r["date"])} · Press release</span><h3><a href="{r["url"]}">{E(r["title"])}</a></h3><p>{E(r["line"])}</p><p class="wk-m">{E(r["note"])}</p></article><article class="card wk-demo reveal"><span class="tag">{E(s["note"])}</span><h3>{E(s["title"])}</h3><p>{E(s["line"])}</p></article></div>')),
            ("media", "Media resources", section("media", split(sec_head("Media resources", "For company information and founder background.", "", False) + f'<div class="contact-side"><div class="info"><div class="ic">{icon("users")}</div><div><h3>Founder</h3><p><a href="{ctx.to("founder/")}">Ken Ashe</a></p></div></div><div class="info"><div class="ic">{icon("mail")}</div><div><h3>Media inquiries</h3><p><a href="mailto:{C["company"]["email"]}">{C["company"]["email"]}</a></p></div></div><div class="info"><div class="ic">{icon("doc")}</div><div><h3>Press kit and coverage</h3><p><a href="{f["kenashe"]}newsroom/">Newsroom on KenAshe.ai</a></p></div></div></div>', f'<div class="panel reveal"><h3>Speaking and judging</h3><ul class="sp">{sp}</ul></div>'), True))]


def p_contact(ctx):
    side = (f'<div class="contact-side"><div class="info"><div class="ic">{icon("mail")}</div><div><h3>Email</h3><p><a href="mailto:{C["company"]["email"]}">{C["company"]["email"]}</a></p></div></div>'
            f'<div class="info"><div class="ic">{icon("chart")}</div><div><h3>Response time</h3><p>Within one business day.</p></div></div>'
            f'<div class="info"><div class="ic">{icon("shield")}</div><div><h3>First consultation</h3><p>Free, with no obligation.</p></div></div>'
            f'<div class="info"><div class="ic">{icon("target")}</div><div><h3>Buying a domain?</h3><p><a href="{ctx.to("how-we-buy-domains/")}">How we buy domains</a></p></div></div></div>')
    return [("form", "Contact form", section("form", f'<h2 class="sr">Contact form and details</h2><div class="contact-grid">{contact_form()}{side}</div>'))]


INNER = {"services": p_services, "websites": p_websites, "seo": p_seo, "ai": p_ai, "entity": p_entity, "domains": p_domains, "buy": p_buy,
         "work": p_work, "case": p_case, "about": p_about, "founder": p_founder, "insights": p_insights, "article": p_article, "news": p_news, "contact": p_contact}
HERO_KEY = {"case": None, "article": None}


def hero_for(ctx, key, extra=""):
    if key == "case":
        w = C["work"][0]
        return f'<section class="hero hero--page"><div class="container hero-inner"><nav class="crumbs" aria-label="Breadcrumb"><ol><li><a href="{ctx.to()}">Home</a></li><li><a href="{ctx.to("work/")}">Work</a></li><li aria-current="page">Case study</li></ol></nav>{eyebrow("Case study · " + w["category"], True)}<h1>{E(w["title"])}</h1><p class="lead">{E(w["summary"])}</p>{extra}</div></section>'
    if key == "article":
        a = C["article"]
        return f'<section class="hero hero--page"><div class="container hero-inner"><nav class="crumbs" aria-label="Breadcrumb"><ol><li><a href="{ctx.to()}">Home</a></li><li><a href="{ctx.to("insights/")}">Insights</a></li><li aria-current="page">{E(a["kind"])}</li></ol></nav>{eyebrow(a["kind"] + " · Draft", True)}<h1>{E(a["title"])}</h1><p class="lead">By Ken Ashe. {E(a["status"])}</p>{extra}</div></section>'
    return page_hero(ctx, key, extra, cta=key not in ("contact", "news", "insights", "founder"))


def title_desc(key):
    if key == "case":
        return C["work"][0]["title"], C["work"][0]["summary"]
    if key == "article":
        return C["article"]["title"], C["article"]["dek"]
    return PG[key]["title"], PG[key]["lead"]


def build_concept(cfg):
    """cfg: k, name, dir, home(ctx)->html, inner(ctx, key, sections)->html (optional), hero_extra(ctx,key)->html (optional)."""
    for path, key in PAGES:
        ctx = Ctx(cfg, path)
        if key == "home":
            body = cfg["home"](ctx); t, d = "Websites, search, digital identity, AI visibility, and domains", C["company"]["description"]
        else:
            secs = INNER[key](ctx)
            extra = cfg.get("hero_extra", lambda c, k: "")(ctx, key)
            hero = hero_for(ctx, key, extra)
            body = cfg["inner"](ctx, key, hero, secs) if cfg.get("inner") else hero + "".join(s[2] for s in secs)
            if key not in ("contact",):
                body += cta_band(ctx)
            t, d = title_desc(key)
        write(f"{cfg['dir']}/{path}index.html", page(ctx, t, d, body, "home" if key == "home" else f"pg-{key}"))
