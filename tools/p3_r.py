"""Version 3, Original Interactive, refined (/phase-3/interactive-refined/).

A separate refinement of concept C. It keeps the navy homepage hero, the presence map, the five
services, and the original production stylesheet, and removes the portfolio, the second map, and
the auto-advancing widgets. Interior pages get a short, light hero. The original concept C in
/phase-3/interactive/ is not touched by this module.
"""
import json
from p3lib import (C, E, S, PG, NOTICE, Ctx, write, icon, eyebrow, check, sec_head, section, cards, steps, panel, split,
                   faq, note, evidence, contact_form, cta_band, p_buy, p_news, LAYER_OF, LAYER_ICON)
from p3_r_content import R

V = "?v=20261124-r1"
CFG = {"k": "C", "name": R["name"], "dir": "phase-3/interactive-refined"}
PAGES = [("", "home"), ("services/", "services"), ("services/website-design/", "websites"), ("services/seo/", "seo"),
         ("services/ai-visibility/", "ai"), ("services/entity-seo/", "entity"), ("services/domains/", "domains"),
         ("how-we-buy-domains/", "buy"), ("tools/digital-presence-check/", "check"), ("about/", "about"), ("founder/", "founder"),
         ("insights/", "insights"), ("insights/domains-identity-for-ai-agents/", "article"), ("news/", "news"), ("contact/", "contact")]
CHECK_PATH = "tools/digital-presence-check/"
STACK = {l["id"]: l for l in C["stack"]}
ARROW = icon("arrow", "2.4")


# ------------------------------------------------------------------ shell
def head(ctx, title, desc):
    return f"""<!DOCTYPE html>
<html lang="en" class="no-js">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex,nofollow,noarchive">
<title>{E(title)} | Lucky Domains (version 3, Original Interactive refined)</title>
<meta name="description" content="{E(desc)}">
<link rel="icon" href="{ctx.asset('favicon.ico')}" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="{ctx.asset('favicon-32.png')}">
<link rel="apple-touch-icon" href="{ctx.asset('apple-touch-icon.png')}">
<link rel="preload" href="{ctx.font('jakarta-normal-400-800.woff2')}" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{ctx.font('inter-normal-400-600.woff2')}" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{ctx.r}phase-3/shared/original.css">
<link rel="stylesheet" href="{ctx.r}phase-3/shared/v3.css">
<link rel="stylesheet" href="{ctx.c}css/style.css{V}">
<script>document.documentElement.className='js'</script>
</head>"""


def header(ctx):
    sub = "".join(f'<li><a href="{ctx.svc(s["id"])}">{icon(s["icon"])}<span>{E(s["name"])}</span></a></li>' for s in C["services"])
    sub += (f'<li class="menu-x"><a href="{ctx.to("services/")}">All services</a><a href="{ctx.to("how-we-buy-domains/")}">How we buy domains</a>'
            f'<a href="{ctx.to(CHECK_PATH)}">Digital Presence Check</a></li>')
    links = ""
    for label, p in R["nav"]:
        if p == "services/":
            cur = ' aria-current="page"' if ctx.path.startswith("services/") or ctx.path == "how-we-buy-domains/" else ""
            links += f'<div class="has-menu"><a href="{ctx.to(p)}"{cur}>{label}</a><button class="menu-btn" type="button" aria-expanded="false" aria-controls="m-svc"><span class="sr">Show service pages</span></button><ul class="menu" id="m-svc">{sub}</ul></div>'
        else:
            links += f'<a href="{ctx.to(p)}"{ctx.cur(p)}>{label}</a>'
    return f"""<aside class="review" aria-label="Review notice"><span>{NOTICE} <span class="rv-x">Version 3: {E(R['name'])}.</span></span> <a href="{ctx.r}phase-3/">Version 3 concepts</a></aside>
<header class="site-header" id="site-header">
  <div class="container header-inner">
    <a class="brand" href="{ctx.to()}" aria-label="Lucky Domains, concept home"><img class="brand-logo" src="{ctx.asset('logo-wordmark.png')}" alt="Lucky Domains" width="170" height="42"></a>
    <nav class="nav" id="nav" aria-label="Primary">{links}<a href="{ctx.to('contact/')}" class="btn btn-accent btn-sm nav-cta">{C['navCta']}</a></nav>
    <button class="nav-toggle" id="nav-toggle" type="button" aria-label="Open menu" aria-controls="nav" aria-expanded="false"><span></span><span></span><span></span></button>
  </div>
</header>"""


def footer(ctx):
    sv = "".join(f'<li><a href="{ctx.svc(s["id"])}">{E(s["name"])}</a></li>' for s in C["services"]) + f'<li><a href="{ctx.to("how-we-buy-domains/")}">How we buy domains</a></li>'
    co = "".join(f'<li><a href="{ctx.to(p)}">{t}</a></li>' for t, p in [("About", "about/"), ("Founder", "founder/"), ("Insights", "insights/"), ("News & media", "news/"), ("Digital Presence Check", CHECK_PATH)])
    return f"""<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div class="footer-brand"><a href="{ctx.to()}" class="footer-logo"><img src="{ctx.asset('logo-icon.png')}" alt="" width="42" height="42" loading="lazy"><span>Lucky Domains</span></a><p>{E(C['company']['footer'])}</p></div>
      <div class="footer-col"><h2 class="fh">Services</h2><ul>{sv}</ul></div>
      <div class="footer-col"><h2 class="fh">Company</h2><ul>{co}</ul></div>
      <div class="footer-col"><h2 class="fh">Get in touch</h2><ul><li><a href="mailto:{C['company']['email']}">{C['company']['email']}</a></li><li>{E(R['location'])}</li><li><a href="{ctx.to('contact/')}">{C['navCta']}</a></li><li><a href="{C['founder']['kenashe']}">KenAshe.ai</a></li></ul></div>
    </div>
    <div class="footer-bottom"><span>{E(C['company']['founderLine'])}</span><span>{NOTICE} Version 3, refined.</span></div>
  </div>
</footer>"""


def page(ctx, title, desc, body, cls=""):
    return f"""{head(ctx, title, desc)}
<body class="rf {cls}">
<a class="skip-link" href="#main">Skip to content</a>
{header(ctx)}
<main id="main">
{body}
</main>
{footer(ctx)}
<script src="{ctx.r}phase-3/shared/v3.js" defer></script>
<script src="{ctx.c}js/main.js{V}" defer></script>
</body></html>"""


# ------------------------------------------------------------------ refined components
def mini(lid):
    """Small diagram for a service hero: where this service sits in Domain, Website, Search, Entity, AI."""
    ids = [l["id"] for l in C["stack"]]; at = ids.index(lid); l = STACK[lid]
    lis = "".join(f'<li class="{"on" if i == at else "done" if i < at else ""}"{" aria-current=true" if i == at else ""}>{E(x["name"])}</li>' for i, x in enumerate(C["stack"]))
    return (f'<aside class="mini" aria-label="Where this service sits"><p class="mini-t">Where this fits</p><ol>{lis}</ol>'
            f'<p><strong>{E(l["name"])}, layer {at + 1} of 5.</strong> {E(l["short"])}</p></aside>')


def phero(ctx, key, eb, h1, lead, trail=(), cta=True, cta2=None):
    """Short, light interior hero: compact breadcrumbs, navy heading, one clear call to action."""
    tr = "".join(f'<li><a href="{ctx.to(p)}">{E(t)}</a></li>' for t, p in trail)
    crumbs = f'<nav class="crumbs" aria-label="Breadcrumb"><ol><li><a href="{ctx.to()}">Home</a></li>{tr}<li aria-current="page">{E(eb)}</li></ol></nav>'
    c2 = cta2 or ("All services", "services/")
    btn = f'<div class="btn-row"><a class="btn btn-accent" href="{ctx.to("contact/")}">{C["navCta"]}</a><a class="link-arrow" href="{ctx.to(c2[1])}">{E(c2[0])} {ARROW}</a></div>' if cta else ""
    lid = LAYER_OF.get(key)
    side = mini(lid) if lid else ""
    return (f'<section class="phero"><div class="container phero-g{"" if side else " solo"}"><div class="phero-b">{crumbs}'
            f'<h1>{E(h1)}</h1><p class="lead">{E(lead)}</p>{btn}</div>{side}</div></section>')


def look(key):
    k = R["look"][key]
    lis = "".join(f'<li class="reveal"><h3>{E(n)}</h3><p>{E(t)}</p></li>' for n, t in k["items"])
    return section("look", sec_head("", k["title"], k["lead"]) + f'<ul class="look">{lis}</ul>', True)


def first_party(key):
    f = R["firstParty"][key]
    links = "".join(f'<li><a href="{u}">{E(t)}</a></li>' for t, u in f["links"])
    return section("example", f'<article class="fp reveal"><p class="fp-k">First-party example</p><h2>{E(f["title"])}</h2><p>{E(f["body"])}</p><ul class="fp-l">{links}</ul><p class="fp-n">{E(f["note"])}</p></article>')


def engagement(ctx, name, soft=True):
    e = next(e for e in PG["services"]["engagements"] if e["name"] == name)
    return section("engagement", '<div class="engb reveal"><div>' + f'<p class="fp-k">Named engagement · {E(e["kind"])}</p><h2>{E(name)}</h2><p>{E(e["line"])} The scope is agreed in writing before work starts.</p>'
                   f'<a class="btn btn-accent" href="{ctx.to("contact/")}">Ask about this engagement</a></div>{check(e["check"])}</div>', soft)


def promo(ctx, h="h3"):
    p = R["services"]["promo"]
    return (f'<article class="card svc promo reveal"><div class="icon-badge navy">{icon("chart")}</div><span class="tag">Free self-check</span><{h}>{E(p["title"])}</{h}>'
            f'<p>{E(p["line"])}</p><div class="svc-foot"><a class="link-arrow" href="{ctx.to(CHECK_PATH)}">{E(p["cta"])} {ARROW}</a></div></article>')


def distinction():
    d = R["services"]["distinction"]
    return (f'<div class="distinct reveal"><h3>{E(d["title"])}</h3><div class="distinct-g"><div><p class="fp-k">{E(d["entity"][0])}</p><p>{E(d["entity"][1])}</p></div>'
            f'<div><p class="fp-k">{E(d["ai"][0])}</p><p>{E(d["ai"][1])}</p></div></div><p class="distinct-n">{E(d["seo"])}</p></div>')


def differs(ctx, key):
    t, x, other = R["differs"][key]
    return f'<p class="v3-note differs"><strong>{E(t)}</strong> {E(x)} See <a href="{ctx.svc(other)}">{E(S[other]["name"])}</a>.</p>'


def map_block(ctx):
    M = R["map"]
    data = {"nodes": [dict(n, href=ctx.svc(n["service"]), svcName=S[n["service"]]["name"]) for n in M["nodes"]], "problems": M["problems"],
            "labels": {o["id"]: o["label"] for o in C["diagnostic"]["options"]}, "icon": ctx.asset("logo-icon-128.png"), "idle": M["idle"], "fragmented": M["fragmented"]}
    blob = json.dumps(data).replace("</", "<\\/")
    fb = "".join(f'<li><b>{E(n["label"])}</b> {E(n["line"])} <span>{E(", ".join(n["details"]))}.</span></li>' for n in M["nodes"])
    return (f'<div class="pmap" data-map><div class="pm-bar"><p class="pm-t" id="pm-t">{E(M["title"])}</p><div class="pm-ctl">'
            '<div class="seg" role="group" aria-label="Map state"><button type="button" class="sg" data-state="fragmented" aria-pressed="false">Fragmented</button>'
            '<button type="button" class="sg" data-state="recognized" aria-pressed="true">Recognized</button></div>'
            '<button type="button" class="pm-pause" aria-pressed="false" aria-label="Pause map animation"><svg viewBox="0 0 24 24" aria-hidden="true"><path class="i-pause" d="M8 5v14M16 5v14"/><path class="i-play" d="M8 5l11 7-11 7z"/></svg></button></div></div>'
            f'<div class="pm-view" aria-labelledby="pm-t"><ul class="pm-fb">{fb}</ul></div>'
            f'<div class="pm-detail" aria-live="polite"><p>{E(M["idle"])}</p></div><p class="pm-cap">{E(M["caption"])}</p>'
            f'<script type="application/json" class="pm-data">{blob}</script></div>')


def diagnostic(ctx):
    d = R["diagnostic"]
    radios = "".join(f'<label class="dg-o"><input type="radio" name="stuck" value="{o["id"]}"><span>{E(o["label"])}</span></label>' for o in C["diagnostic"]["options"])
    ans = "".join(f'<div class="dg-a" data-for="{o["id"]}"><p class="fp-k">A sensible place to start</p><h3>{E(o["start"])}</h3><p>{E(o["why"])}</p>'
                  f'<ol class="dg-steps">{"".join("<li>%s</li>" % E(x) for x in o["first"])}</ol><a class="btn btn-accent" href="{ctx.svc(o["service"])}">See {E(o["start"])}</a></div>' for o in C["diagnostic"]["options"])
    return (f'<section class="section diag" id="start" aria-labelledby="dg-h"><div class="container"><div class="dg-in"><div class="reveal"><h2 id="dg-h">{E(d["title"])}</h2>'
            f'<p class="section-lead">{E(d["intro"])}</p><fieldset class="dg-opts"><legend class="sr">Choose the problem that fits best</legend>{radios}</fieldset></div>'
            f'<div class="dg-out" aria-live="polite"><p class="dg-empty">{E(d["empty"])}</p>{ans}<p class="dg-note">{E(d["note"])}</p></div></div></div></section>')


def progression(ctx):
    p = R["progression"]
    lis = "".join(f'<li class="pg"><span class="pg-n" aria-hidden="true">{l["n"]}</span><h3>{E(l["name"])}</h3><p class="pg-p">{E(l["short"])}</p><p class="pg-x">{E(l["line"])}</p>'
                  f'<a class="link-arrow" href="{ctx.svc(l["service"])}">{E(S[l["service"]]["tag"])} {ARROW}</a></li>' for l in C["stack"])
    return section("layers", sec_head(p["eyebrow"], p["title"], p["lead"]) + f'<ol class="prog" data-prog>{lis}</ol>', True)


def service_cards(ctx, full=False, h="h3"):
    out = ""
    for s in C["services"]:
        ck = check(s["check"]) if full else ""
        out += (f'<article class="card svc reveal"><div class="icon-badge">{icon(s["icon"])}</div><span class="tag">{E(s["tag"])}</span><{h}>{E(s["name"])}</{h}><p>{E(s["short"])}</p>{ck}'
                f'<div class="svc-foot"><a class="link-arrow" href="{ctx.svc(s["id"])}">Explore<span class="sr"> {E(s["name"])}</span> {ARROW}</a></div></article>')
    return f'<div class="grid grid-3 svc5">{out}{promo(ctx, h)}</div>'


# ------------------------------------------------------------------ homepage
def home(ctx):
    h = C["hero"]; f = C["founder"]; a = R["aiWork"]; sv = R["services"]; st = R["story"]
    uses = "".join(f'<li><strong>{E(n)}</strong><span>{E(t)}</span></li>' for n, t in a["uses"])
    return f"""
<section class="hero hero-r">
  <div class="container hero-split">
    <div class="hero-inner">
      {eyebrow(h['eyebrow'], True)}
      <h1>{E(h['headline'])}</h1>
      <p class="lead">{E(R['hero']['lead'])}</p>
      <div class="btn-row"><a href="{ctx.to('contact/')}" class="btn btn-accent btn-lg">{E(h['cta1'])}</a><a href="{ctx.to('services/')}" class="btn btn-on-dark btn-lg">{E(h['cta2'])}</a></div>
      <div class="hero-trust">{icon('check', '2.4')} {E(h['founder'])}</div>
    </div>
    <div class="hero-map">{map_block(ctx)}</div>
  </div>
</section>

{diagnostic(ctx)}

{progression(ctx)}

{section('services', sec_head(sv['eyebrow'], sv['title'], sv['lead']) + service_cards(ctx) + distinction())}

{section('story', f'<div class="story reveal">{eyebrow("The Lucky Domains story")}<h2>{E(st["headline"])}</h2>' + "".join(f'<p class="section-lead">{E(x)}</p>' for x in st["home"]) + f'<a class="link-arrow" href="{ctx.to("about/")}">Read our story {ARROW}</a></div>', True)}

{section('ai-work', '<div class="aiw">' + '<div class="reveal">' + eyebrow(a["eyebrow"]) + f'<h2>{E(a["title"])}</h2><p class="section-lead">{E(a["intro"])}</p><p>{E(a["limit"])}</p></div>' + f'<div class="reveal"><ul class="uses">{uses}</ul><p class="uses-n">{E(a["example"])} <a href="{a["exampleUrl"]}">Build record on KenAshe.ai</a>.</p></div></div>')}

{section('founder', split(sec_head('Founder', C['company']['founderLine'], '', False) + f'<p class="section-lead">{E(f["bio"])}</p><p><strong>{E(C["company"]["accountability"])}</strong></p><a class="btn btn-ghost" href="{ctx.to("founder/")}">About Ken</a>', f'<figure class="founder-card reveal"><img src="{ctx.asset(f["image"])}" alt="Ken Ashe, founder of Lucky Domains" width="460" height="460" loading="lazy"></figure>', True), True)}
{cta_band(ctx, 'Not sure where to start?', None, h['cta1'])}"""


# ------------------------------------------------------------------ interior pages
def pg_services(ctx):
    p = PG["services"]
    eng = "".join(f'<div class="price reveal"><h3>{E(e["name"])}</h3><p class="desc"><strong>{E(e["kind"])}.</strong> {E(e["line"])}</p>{check(e["check"])}</div>' for e in p["engagements"])
    return (phero(ctx, "services", "Services", p["h1"], R["pages"]["services"]["lead"], cta2=("Not sure where to start? Take the check", CHECK_PATH))
            + section("svc", '<h2 class="sr">The five services</h2>' + service_cards(ctx, True, "h3") + distinction())
            + section("engage", sec_head("Engagements", "Scoped in writing, before work starts.", p["pricing"]) + f'<div class="price-grid eng">{eng}</div>' + note(C["notPromised"], "note", "What we will not promise."), True)
            + section("not", '<div class="split"><div class="split-body">' + sec_head("Deliberately specialized", "What Lucky Domains is not", "", False) + '</div><div class="split-media">' + check(p["notList"], "nope") + "</div></div>"))


def svc_hero(ctx, key):
    p = PG[key]
    return phero(ctx, key, p["eyebrow"], p["h1"], R["pages"][key]["lead"], trail=[("Services", "services/")])


def pg_websites(ctx):
    w = PG["websites"]
    paths = (f'<div class="grid grid-2"><article class="card reveal"><div class="icon-badge">{icon("search")}</div><span class="tag">Review</span><h3>{E(w["paths"][0]["name"])}</h3><p>{E(w["paths"][0]["line"])}</p></article>'
             f'<article class="card reveal"><div class="icon-badge">{icon("monitor")}</div><span class="tag">Named engagement · Scoped</span><h3>Website Build</h3><p>{E(w["paths"][1]["line"])}</p></article></div>')
    return (svc_hero(ctx, "websites")
            + section("approach", split(sec_head("The approach", "Structure before style.", "", False) + "".join(f'<p class="section-lead">{E(x)}</p>' for x in w["intro"]), panel("What a build includes", w["includes"])))
            + look("websites")
            + section("paths", sec_head("Two ways to start", "Review the site you have, or build the one you need.", "Both are scoped in writing before work starts.") + paths)
            + section("process", sec_head("How a project runs", "Six steps, from discovery to improvement.") + steps(w["process"], "steps steps-6") + note(w["aiNote"], "note", "AI-assisted, human-reviewed."), True)
            + first_party("websites")
            + section("faq", sec_head("Questions", "Website projects, answered.") + faq(w["faq"]) + f'<p class="center v3-more">{E(w["not"])}</p>', True))


def pg_seo(ctx):
    s = PG["seo"]
    return (svc_hero(ctx, "seo")
            + section("covers", split(sec_head("What SEO covers", "The fundamentals still decide who gets found.", "", False)
                                      + '<p class="section-lead">Technical health, pages matched to real search intent, useful content, and earned authority. AI-powered search draws on the same foundation, so this work now does two jobs.</p>'
                                      + note(s["reporting"], "note", "Honest reporting."), panel("What the work includes", [x["name"] for x in s["areas"]])))
            + look("seo")
            + section("expanding", sec_head("Why SEO is expanding", "AI search is built on search.", "What the search engines themselves say.") + evidence(ctx))
            + section("process", sec_head("How we work", "Five steps, repeated.") + steps(s["process"], "steps steps-5"), True)
            + first_party("seo")
            + section("faq", sec_head("Questions", "SEO, answered.") + faq(s["faq"]), True))


def pg_ai(ctx):
    a = PG["ai"]
    keep = ("Baseline", "Consistency audit", "Content clarity and coverage", "Source analysis", "Authority-content plan", "Monitoring over time")
    dl = [x for x in a["deliverables"] if x["name"] in keep]
    return (svc_hero(ctx, "ai")
            + section("goal", split(sec_head("The goal", "Make your business easy to understand and easy to verify.", "", False) + '<p class="section-lead">Lucky Domains helps make a company:</p>' + check(a["goals"]),
                                    panel("What AI systems rely on", ["Crawlable pages with useful first-party content", "Structured data that matches the visible facts", "Consistent names, descriptions, and founders across profiles", "Credible third-party references", "Clear relationships between people, services, and places"])))
            + look("ai")
            + section("deliver", sec_head("What the work involves", "From a written baseline to monitoring.", a["measure"]) + steps(dl, "steps steps-6") + differs(ctx, "ai"))
            + engagement(ctx, "Entity and AI Visibility Audit")
            + section("evidence", sec_head("What the sources say", "No secret markup. Measurable, in part.") + evidence(ctx) + note(C["notPromised"], "warn", "What we will not promise.") + note(C["noSecret"], "note"))
            + section("faq", sec_head("Questions", "AI visibility, answered.") + faq(a["faq"]), True))


def pg_entity(ctx):
    e = PG["entity"]
    aud = (f'<div class="grid grid-3 idg"><article class="card reveal"><div class="icon-badge">{icon("users")}</div><h3>For people</h3>{check(e["people"][:5])}</article>'
           f'<article class="card reveal"><div class="icon-badge">{icon("globe")}</div><h3>For businesses</h3>{check(e["business"][:5])}</article>'
           f'<article class="card reveal card-emerging"><div class="icon-badge navy">{icon("spark")}</div><span class="tag">Emerging research</span><h3>For AI agents</h3><p>Agents may need the same things people and companies do: a readable name, a way to be found, and a way to check who stands behind them. This is research, not a service.</p>'
           f'<div class="svc-foot"><a class="link-arrow" href="{ctx.to(C["article"]["slug"])}">Read the research note {ARROW}</a></div></article></div>')
    lv = "".join(f'<div class="price reveal"><span class="tag">Level {i}</span><h3>{E(x["name"])}</h3><p class="desc">{E(x["line"])}</p>{check(x["check"])}</div>' for i, x in enumerate(e["levels"], 1))
    return (svc_hero(ctx, "entity")
            + section("what", split(sec_head("What entity SEO is", "Your website can rank and still be misunderstood.", "", False) + "".join(f'<p class="section-lead">{E(x)}</p>' for x in e["what"]),
                                    panel("The evidence we work on", ["A clear canonical website", "Accurate structured data", "Consistent external profiles", "Unambiguous person and company relationships", "Credible third-party references", "Consistent public facts"])))
            + look("entity")
            + section("identity", sec_head("Digital identity", "Identity for people and businesses.", "The same discipline applies to a founder and to a company. Agent identity is an emerging research area.") + aud + differs(ctx, "entity"))
            + section("levels", sec_head("What the service includes", "Two levels, built on facts you already have.", "All structured data we write describes real facts already supported by you and your site.") + f'<div class="price-grid lv">{lv}</div>'
                      + f'<p class="v3-note differs"><strong>Named engagement.</strong> Either level can be scoped as an <a href="{ctx.svc("ai")}#engagement">Entity and AI Visibility Audit</a>: a baseline and plan for a person or company, agreed in writing before work starts.</p>'
                      + note(e["panel"], "warn", "Knowledge Panels."), True)
            + first_party("entity")
            + section("faq", sec_head("Questions", "Entity SEO, answered.") + faq(e["faq"]), True))


def pg_domains(ctx):
    d = PG["domains"]
    return (svc_hero(ctx, "domains")
            + section("anchor", split(sec_head("The anchor", "Every other signal points back to the name.", "", False) + f'<p class="section-lead">{E(d["anchor"])}</p>', panel("What's included", d["includes"])))
            + look("domains")
            + section("buy", sec_head("Buying a domain", "Four steps, in the order they happen.") + steps(d["steps"]) + f'<p class="center v3-more"><a class="btn btn-ghost" href="{ctx.to("how-we-buy-domains/")}">How we buy domains, in detail</a></p>')
            + section("sell", split(sec_head("Selling a domain", "A confidential, managed exit.", "", False) + f'<p class="section-lead">{E(d["selling"])}</p>' + note(d["terms"], "note", "Fee."), '<div class="reveal">' + check(d["not"], "nope") + "</div>", True), True)
            + section("faq", sec_head("Questions", "Domains, answered.") + faq(d["faq"])))


def pg_buy(ctx):
    b = PG["buy"]
    return phero(ctx, "buy", "How we buy domains", b["h1"], R["pages"]["buy"]["lead"], trail=[("Services", "services/")], cta2=("Domain Acquisition & Brokerage", "services/domains/")) + "".join(s[2] for s in p_buy(ctx))


def pg_check(ctx):
    k = R["check"]; p = R["pages"]["check"]; n = 0; groups = ""
    for g in k["groups"]:
        qs = ""
        for q, why in g["questions"]:
            n += 1
            opts = "".join(f'<label class="dq-o"><input type="radio" name="dpc-{n}" value="{v}"><span>{E(t)}</span></label>' for v, t in k["options"])
            qs += f'<fieldset class="dq" data-area="{g["id"]}"><legend><span class="dq-n" aria-hidden="true">{n}</span>{E(q)}</legend><p class="dq-why">{E(why)}</p><div class="dq-os">{opts}</div></fieldset>'
        groups += f'<section class="dq-g" aria-labelledby="dg-{g["id"]}"><h2 id="dg-{g["id"]}">{E(g["name"])}</h2>{qs}</section>'
    areas = "".join(f'<li data-area="{g["id"]}"><div class="da-h"><span class="da-n">{E(g["name"])}</span><span class="da-s" data-status>{E(k["status"]["none"])}</span></div>'
                    f'<div class="da-b"><p>{E(g["advice"])}</p><a class="link-arrow" href="{ctx.svc(g["service"])}">{E(S[g["service"]]["name"])} {ARROW}</a></div></li>' for g in k["groups"])
    cfg = json.dumps({"status": k["status"], "allYes": k["allYes"], "total": n}).replace("</", "<\\/")
    return (phero(ctx, "check", p["eyebrow"], p["h1"], p["lead"], cta=False)
            + f'<section class="section dpc-s"><div class="container"><p class="dpc-top"><strong>{E(k["statement"])}</strong> {E(k["privacy"])}</p>'
              f'<div class="dpc" data-dpc><div class="dpc-q">{groups}</div>'
              f'<aside class="dpc-out" aria-labelledby="dpc-h"><h2 id="dpc-h">Areas to look at</h2><p class="dpc-sum" role="status" data-sum>Answer the questions to see possible areas to investigate.</p>'
              f'<p class="dpc-nojs">{E(k["nojs"])}</p><ul class="dpc-areas">{areas}</ul>'
              f'<div class="dpc-next" data-next hidden><p class="fp-k">A sensible place to start</p><p class="dpc-next-t" data-next-t></p><a class="btn btn-accent" href="{ctx.to("contact/")}">Talk to Ken about it</a></div>'
              f'<p class="dpc-note"><strong>{E(k["statement"])}</strong> It points to possible areas to investigate. It cannot confirm that anything is working. {E(k["privacy"])}</p>'
              f'<button type="button" class="btn btn-ghost btn-sm dpc-reset" data-reset>Clear answers</button></aside></div>'
              f'<script type="application/json" class="dpc-data">{cfg}</script></div></section>'
            + section("next", sec_head("After the check", "What a real review adds.", "A self-check relies on what you already know. A review looks at the site, the data, and the sources directly.")
                      + cards([dict(icon="search", h="Evidence, not recall", p="Crawls, Search Console, structured-data tests, and the answers AI systems give today."),
                               dict(icon="doc", h="A written baseline", p="What was found, in plain English, before anything is changed."),
                               dict(icon="target", h="A scoped plan", p="What to fix first, what it would take, and what it will not promise.")], 3), True))


def pg_about(ctx):
    a = PG["about"]; st = R["story"]
    vals = "".join(f'<div class="value reveal"><div class="ic">{icon(["shield", "trend", "chart", "doc"][i])}</div><div><h3>{E(t)}</h3><p>{E(x)}</p></div></div>' for i, (t, x) in enumerate(a["values"]))
    layers = "".join(f'<li><span class="ly-n">{l["n"]}</span><b>{E(l["name"])}</b><span>{E(l["short"])}</span></li>' for l in C["stack"])
    return (phero(ctx, "about", "About", st["headline"], a["lead"], cta=False)
            + section("story", split(sec_head("Our story", "It started with the name.", "", False) + "".join(f'<p>{E(x)}</p>' for x in st["about"]), f'<ol class="ab-stack reveal" aria-label="The five layers">{layers}</ol>'))
            + section("believe", split(sec_head("What we believe", "Fortune favors the prepared.", "", False) + f'<p class="section-lead">{E(a["philosophy"])}</p>' + check(a["believe"]), f'<div class="grid" style="gap:22px">{vals}</div>'), True)
            + section("rhythm", sec_head("How we work", "Discipline you can see in the deliverables.") + steps(a["rhythm"]) + note(R["aiWork"]["intro"], "note", R["aiWork"]["title"]))
            + section("founder", split(sec_head("The founder", C["company"]["founderLine"], "", False) + f'<p class="section-lead">{E(C["company"]["accountability"])}</p><a class="btn btn-ghost" href="{ctx.to("founder/")}">About Ken</a>',
                                       f'<figure class="founder-card reveal"><img src="{ctx.asset(C["founder"]["image"])}" alt="Ken Ashe, founder of Lucky Domains" width="460" height="460" loading="lazy"></figure>', True), True))


def pg_founder(ctx):
    f = C["founder"]; rf = R["founder"]; art = C["article"]
    cred = "".join(f'<div class="stat"><div class="num">{E(a)}</div><div class="lbl">{E(b)}</div></div>' for a, b in f["credentialsFull"])
    exp = cards([dict(icon=["chart", "monitor", "spark"][i], h=t, p=x) for i, (t, x) in enumerate(rf["experience"])], 3)
    sp = "".join(f'<div class="value reveal"><div class="ic">{icon("users")}</div><div><h3>{E(y)} · {E(ev)}</h3><p>{E(t)}</p></div></div>' for y, ev, t in f["speaking"])
    links = "".join(f'<div class="info"><div class="ic">{icon("link")}</div><div><h3>{E(t)}</h3><p><a href="{u}">{E(d)}</a></p></div></div>' for t, u, d in f["links"])
    two = "".join(f'<article class="card reveal"><span class="tag">{E(a)}</span><p>{E(b)}</p></article>' for a, b in f["split"])
    return (phero(ctx, "founder", "Founder", "Ken Ashe", PG["founder"]["lead"], cta=False)
            + section("bio", split(sec_head("Background", "Builder, operator, accountant.", "", False) + "".join(f'<p>{E(x)}</p>' for x in f["bioLong"]) + f'<blockquote class="v3-quote"><p>{E(f["quote"])}</p><cite>Ken Ashe</cite></blockquote>',
                                   f'<figure class="founder-card reveal"><img src="{ctx.asset(f["image"])}" alt="Portrait of Ken Ashe" width="460" height="460"></figure>'))
            + section("experience", sec_head("Experience", "Finance discipline, applied to digital work.", f["discipline"]) + exp, True)
            + section("creds", sec_head("Credentials", "Operating evidence, not the headline.") + f'<div class="stats creds reveal">{cred}</div><p class="center v3-more">Member of <a href="{f["forbes"]}">Forbes Business Council</a>.</p>')
            + section("speaking", split(sec_head("Speaking and judging", "On stage and on panels.", "", False) + f'<div class="grid" style="gap:22px">{sp}</div>', f'<div class="contact-side reveal">{links}</div>'), True)
            + section("sites", sec_head("Two sites, two jobs", "Where to find what.") + f'<div class="grid grid-2">{two}</div>'
                      + f'<p class="center v3-more">{E(rf["research"])} <a href="{ctx.to(art["slug"])}">Read the research note</a> or visit <a href="{f["kenashe"]}">KenAshe.ai</a>.</p>'))


def pg_insights(ctx):
    a = C["article"]; p = PG["insights"]
    feat = (f'<article class="split wk-feat reveal"><div class="split-body"><span class="tag">{E(a["kind"])} · Emerging topic</span><h2>{E(a["title"])}</h2><p class="section-lead">{E(a["dek"])}</p>'
            f'<a class="btn btn-accent" href="{ctx.to(a["slug"])}">Read the research note</a></div><div class="split-media">{panel("In this note", [s[0] for s in a["sections"]])}</div></article>')
    planned = cards([dict(icon=LAYER_ICON[i["layer"]], tag=i["kind"] + " · Planned", h=i["title"], p="Not yet published.") for i in C["insights"]["items"][:4]], 2)
    return (phero(ctx, "insights", "Insights", p["h1"], p["lead"], cta=False)
            + section("featured", feat)
            + section("planned", sec_head("Planned articles", "What is coming.", C["insights"]["label"]) + planned, True)
            + section("tools", f'<div class="grid grid-2 ins-t">{promo(ctx, "h2")}<article class="card reveal"><div class="icon-badge navy">{icon("doc")}</div><span class="tag">Build logs</span><h2>KenAshe.ai</h2>'
                               f'<p>Ken publishes build logs, essays, and videos about the systems he builds, including what failed.</p><div class="svc-foot"><a class="link-arrow" href="{C["founder"]["kenashe"]}">Visit KenAshe.ai {ARROW}</a></div></article></div>'))


def pg_article(ctx):
    a = C["article"]; ra = R["article"]; c = ra["carry"]
    hero = (f'<section class="phero"><div class="container phero-g solo"><div class="phero-b"><nav class="crumbs" aria-label="Breadcrumb"><ol><li><a href="{ctx.to()}">Home</a></li><li><a href="{ctx.to("insights/")}">Insights</a></li><li aria-current="page">{E(a["kind"])}</li></ol></nav>'
            f'<h1>{E(a["title"])}</h1><p class="lead">By Ken Ashe. {E(ra["status"])}</p></div></div></section>')
    secs = list(a["sections"]); body = ""
    for i, (h, ps) in enumerate(secs, 1):
        body += f'<section class="art-s" id="a{i}"><h2>{E(h)}</h2>{"".join("<p>%s</p>" % E(x) for x in ps)}</section>'
        if i == 2:
            dl = "".join(f'<div><dt>{E(t)}</dt><dd>{E(d)}</dd></div>' for t, d in c["items"])
            body += f'<section class="art-s" id="carry"><h2>{E(c["title"])}</h2><p>{E(c["intro"])}</p><dl class="carry">{dl}</dl></section>'
    src = "".join(f'<li><a href="{u}">{E(t)}</a></li>' for t, u in a["sources"])
    return hero + (f'<section class="section article" id="article"><div class="container art-wrap"><p class="art-dek">{E(a["dek"])}</p>{body}'
                   f'<section class="art-s" id="sources"><h2>Sources and build records</h2><ul class="ev">{src}</ul></section></div></section>')


def pg_news(ctx):
    n = PG["news"]
    return phero(ctx, "news", "News & media", n["h1"], n["lead"], cta=False) + "".join(s[2] for s in p_news(ctx))


def pg_contact(ctx):
    c = PG["contact"]
    side = (f'<div class="contact-side"><div class="info"><div class="ic">{icon("mail")}</div><div><h3>Email</h3><p><a href="mailto:{C["company"]["email"]}">{C["company"]["email"]}</a></p></div></div>'
            f'<div class="info"><div class="ic">{icon("globe")}</div><div><h3>Based in</h3><p>{E(R["location"])}</p></div></div>'
            f'<div class="info"><div class="ic">{icon("chart")}</div><div><h3>Response time</h3><p>Within one business day.</p></div></div>'
            f'<div class="info"><div class="ic">{icon("shield")}</div><div><h3>First consultation</h3><p>Free, with no obligation.</p></div></div>'
            f'<div class="info"><div class="ic">{icon("target")}</div><div><h3>Not sure what you need?</h3><p><a href="{ctx.to(CHECK_PATH)}">Take the Digital Presence Check</a></p></div></div></div>')
    return phero(ctx, "contact", "Contact", c["h1"], c["lead"], cta=False) + section("form", f'<h2 class="sr">Contact form and details</h2><div class="contact-grid">{contact_form()}{side}</div>')


BUILD = {"services": pg_services, "websites": pg_websites, "seo": pg_seo, "ai": pg_ai, "entity": pg_entity, "domains": pg_domains, "buy": pg_buy, "check": pg_check,
         "about": pg_about, "founder": pg_founder, "insights": pg_insights, "article": pg_article, "news": pg_news, "contact": pg_contact}


def title_desc(key):
    if key == "home":
        return "Websites, search, digital identity, AI visibility, and domains", C["company"]["description"]
    if key == "article":
        return C["article"]["title"], C["article"]["dek"]
    if key == "check":
        return R["pages"]["check"]["title"], R["pages"]["check"]["lead"]
    return PG[key]["title"], R["pages"].get(key, {}).get("lead") or PG[key]["lead"]


def build():
    for path, key in PAGES:
        ctx = Ctx(CFG, path)
        if key == "home":
            body = home(ctx)
        else:
            body = BUILD[key](ctx)
            if key not in ("contact",):
                body += cta_band(ctx)
        t, d = title_desc(key)
        write(f"{CFG['dir']}/{path}index.html", page(ctx, t, d, body, "home" if key == "home" else f"pg-{key}"))
