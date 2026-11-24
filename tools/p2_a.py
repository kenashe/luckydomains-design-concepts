"""Phase 2, Concept A: Original, Evolved. The current light Lucky Domains site, redesigned for 2027."""
from p2lib import C, E, S, LAYER, Ctx, head, notice, nav_links, contact_form, write, scripts

DIR = "phase-2/original-evolved"
LABEL = "Concept A, Original Evolved"
P = C["pages"]
FONTS = ("jakarta-normal-400-800.woff2", "inter-normal-400-600.woff2")


def chip(lid):
    return f'<span class="lchip l-{lid}">{E(LAYER[lid]["name"])}</span>'


def shell(path, title, desc, body, cls=""):
    ctx = Ctx(DIR, path)
    svc = "".join(f'<li><a href="{ctx.svc(s["id"])}">{E(s["name"])}</a></li>' for s in C["services"])
    return f"""{head(ctx, f"{title} | Lucky Domains (Phase 2 concept A)", desc, "css/style.css", FONTS)}
<body class="{cls}">
<a class="skip" href="#main">Skip to content</a>
{notice(ctx, LABEL)}
<header class="hd">
  <div class="hd-in">
    <a class="hd-logo" href="{ctx.to()}" aria-label="Lucky Domains, concept home"><img src="{ctx.asset('logo-wordmark.png')}" alt="Lucky Domains" width="169" height="42"></a>
    <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="nav">Menu</button>
    <nav id="nav" class="nav" aria-label="Primary"><ul class="nav-l">{nav_links(ctx)}</ul><a class="btn btn-p nav-cta" href="{ctx.home('#contact')}">{E(C['navCta'])}</a></nav>
  </div>
</header>
<main id="main">
{body(ctx)}
</main>
<footer class="ft">
  <div class="ft-in">
    <div class="ft-brand"><img src="{ctx.asset('logo-wordmark.png')}" alt="Lucky Domains" width="193" height="48" loading="lazy"><p>{E(C['company']['description'])}</p><p class="ft-mail"><a href="mailto:{C['company']['email']}">{C['company']['email']}</a></p></div>
    <div><h2>Services</h2><ul>{svc}</ul></div>
    <div><h2>Company</h2><ul><li><a href="{ctx.to('work/')}">Work</a></li><li><a href="{ctx.home('#story')}">About</a></li><li><a href="{ctx.home('#insights')}">Insights</a></li><li><a href="{ctx.home('#founder')}">Founder</a></li><li><a href="{ctx.home('#contact')}">Contact</a></li><li><a href="{C['founder']['kenashe']}">KenAshe.ai</a></li></ul></div>
  </div>
  <p class="ft-note"><span>{E(C['footer'])}</span><span>{E(C['deferredNote'])}</span></p>
</footer>
{scripts(ctx)}
</body></html>"""


def cta_band(ctx):
    return f"""<section class="band" aria-labelledby="band-h"><div class="band-in"><div><h2 id="band-h">Not sure where to start?</h2><p>Tell Ken what you are working on. {E(C['company']['consult'])}</p></div>
<p class="cta"><a class="btn btn-p" href="{ctx.home('#contact')}">{E(C['navCta'])}</a><a class="btn" href="mailto:{C['company']['email']}">Email {C['company']['email']}</a></p></div></section>"""


def phd(eyebrow, title, lead, crumbs=None, ctx=None):
    bc = ""
    if crumbs:
        bc = '<nav class="crumbs" aria-label="Breadcrumb"><ol>' + "".join(f'<li><a href="{h}">{E(t)}</a></li>' for t, h in crumbs) + f'<li aria-current="page">{E(eyebrow)}</li></ol></nav>'
    return f'<section class="phd"><div class="wrap">{bc}<p class="eyebrow">{E(eyebrow)}</p><h1>{E(title)}</h1><p class="lede">{E(lead)}</p></div></section>'


# ------------------------------------------------------------------ home
def home(ctx):
    h = C["hero"]
    card = "".join(f'<li data-step="{i}"><span class="pc-dot" aria-hidden="true"></span><span class="pc-n">{E(l["name"])}</span><span class="pc-l">{E(l["line"])}</span></li>' for i, l in enumerate(C["stack"]))
    slabs = "".join(f'<li class="slab s-{l["id"]}" data-layer="{l["id"]}"><span>{i + 1:02d}</span>{E(l["name"])}</li>' for i, l in enumerate(reversed(C["stack"])))
    steps = "".join(f'<li class="st" data-layer="{l["id"]}"><span class="st-n">{i + 1:02d}</span><div><h3>{E(l["name"])}</h3><p class="st-line">{E(l["line"])}</p><p>{E(l["detail"])}</p><a class="lk" href="{ctx.svc(l["service"])}">{E(S[l["service"]]["name"])}</a></div></li>' for i, l in enumerate(C["stack"]))
    outs = ""
    for o in C["outcomes"]:
        links = " ".join('<a class="lk" href="%s">%s</a>' % (ctx.svc(x), E(S[x]["name"])) for x in o["services"])
        outs += f'<li class="out"><div class="out-chips">{"".join(chip(x) for x in o["layers"])}</div><h3>{E(o["title"])}</h3><p>{E(o["line"])}</p><p class="out-l">{links}</p></li>'
    d = C["diagnostic"]
    radios = "".join(f'<label class="dg-o"><input type="radio" name="stuck" value="{o["id"]}"><span>{E(o["label"])}</span></label>' for o in d["options"])
    answers = "".join(f'<div class="dg-a" data-for="{o["id"]}"><p class="eyebrow">Start here</p><h3>{E(o["start"])}</h3><p>{E(o["why"])}</p><ol>{"".join(f"<li>{E(x)}</li>" for x in o["first"])}</ol><p class="cta"><a class="btn btn-p" href="{ctx.svc(o["service"])}">See {E(o["start"])}</a></p></div>' for o in d["options"])
    w = P["websites"]
    found = "".join(f'<li><h4>{E(f["name"])}</h4><p>{E(f["line"])}</p></li>' for f in w["foundations"])
    sp = P["search"]
    trio = [("seo", "Search", sp["seoIntro"]), ("entity", "Entity", S["entity"]["lead"]), ("ai", "AI visibility", sp["aiIntro"].split(". ")[0] + ".")]
    trio_h = "".join(f'<article class="tri"><p class="eyebrow">{E(t)}</p><h3>{E(S[sid]["name"])}</h3><p>{E(x)}</p><a class="lk" href="{ctx.svc(sid)}">Learn more</a></article>' for sid, t, x in trio)
    fw = C["work"][0]
    others = "".join(f'<li class="wk{" wk-demo" if x.get("concept") else ""}"><p class="wk-cat">{E(x["category"])}{" · Concept content" if x.get("concept") else ""}</p><h3>{E(x["title"])}</h3><p>{E(x["summary"])}</p></li>' for x in C["work"][1:4])
    aw = C["aiWork"]
    uses = "".join(f'<li><h3>{E(u["name"])}</h3><p>{E(u["line"])}</p></li>' for u in aw["uses"])
    lab = "".join(f'<li><p class="lab-k"><span class="tag">{E(x["status"])}</span>{E(x["kind"])}</p><h3><a href="{x["url"]}">{E(x["name"])}</a></h3><p>{E(x["line"])}</p><p class="lab-lim">{E(x["limit"])}</p></li>' for x in C["lab"])
    ins = "".join(f'<li><span class="ins-k">{E(i["kind"])}</span><span class="ins-t">{E(i["title"])}</span>{chip(i["layer"])}</li>' for i in C["insights"]["items"])
    f = C["founder"]
    return f"""
<section class="hero" aria-labelledby="hero-h">
  <div class="wrap hero-in">
    <div class="hero-copy">
      <p class="eyebrow">{E(h['eyebrow'])}</p>
      <h1 id="hero-h">{E(h['headline'])}</h1>
      <p class="lede">{E(h['support'])}</p>
      <p class="cta"><a class="btn btn-p" href="#contact">{E(h['cta1'])}</a><a class="btn" href="{ctx.to('services/')}">{E(h['cta2'])}</a></p>
      <p class="founder-line"><img src="{ctx.asset(f['image'])}" alt="" width="40" height="40">{E(C['company']['founderLine'])}</p>
    </div>
    <figure class="pcard" aria-labelledby="pc-cap">
      <div class="pc-top"><span class="pc-url">yourbusiness.com</span><button class="pc-pause" type="button" aria-pressed="false">Pause</button></div>
      <ol class="pc-list">{card}</ol>
      <figcaption id="pc-cap">Illustration: the five layers of a digital presence, building in order.</figcaption>
    </figure>
  </div>
</section>

<section class="stack" aria-labelledby="stk-h">
  <div class="wrap">
    <div class="sec-hd"><p class="eyebrow">The Digital Presence Stack</p><h2 id="stk-h">Domain, website, search, entity, AI. One system, built in order.</h2><p>{E(C['stackReinforce'])}</p></div>
    <div class="stk">
      <div class="stk-vis" aria-hidden="true"><ol class="slabs">{slabs}</ol></div>
      <ol class="stk-steps">{steps}</ol>
    </div>
  </div>
</section>

<section class="outs-s" aria-labelledby="out-h"><div class="wrap"><div class="sec-hd"><p class="eyebrow">What you get</p><h2 id="out-h">Three outcomes that compound.</h2></div><ul class="outs">{outs}</ul></div></section>

<section class="dg" aria-labelledby="dg-h">
  <div class="wrap dg-in">
    <div><p class="eyebrow">Quick diagnostic</p><h2 id="dg-h">{E(d['title'])}</h2><p>{E(d['intro'])}</p>
    <fieldset class="dg-opts"><legend class="sr">Choose the problem that fits best</legend>{radios}</fieldset></div>
    <div class="dg-out" aria-live="polite"><p class="dg-empty">Choose an option to see a recommended starting point.</p>{answers}</div>
  </div>
</section>

<section class="web" aria-labelledby="web-h">
  <div class="wrap">
    <div class="web-hd"><div><p class="eyebrow">01 · {E(S['websites']['name'])}</p><h2 id="web-h">{E(w['title'])}</h2></div><p class="lede">{E(w['lead'])}</p></div>
    <div class="web-paths">{"".join(f'<article><h3>{E(p["name"])}</h3><p>{E(p["line"])}</p></article>' for p in w['paths'])}</div>
    <ul class="found">{found}</ul>
    <p class="cta"><a class="btn btn-p" href="{ctx.svc('websites')}">Website design and development</a><a class="btn" href="{ctx.to('work/')}">See how LuckyDomains.io was rebuilt</a></p>
  </div>
</section>

<section class="sea" aria-labelledby="sea-h">
  <div class="wrap">
    <div class="sec-hd"><p class="eyebrow">02 to 04 · Search, entity, and AI visibility</p><h2 id="sea-h">{E(sp['title'])}</h2><p>{E(sp['connect'])}</p></div>
    <div class="tris">{trio_h}</div>
    <p class="promise"><strong>What we will not promise.</strong> {E(C['notPromised'])}</p>
  </div>
</section>

<section class="work" aria-labelledby="wk-h">
  <div class="wrap">
    <div class="sec-hd"><p class="eyebrow">Selected work</p><h2 id="wk-h">Real work, with the evidence attached.</h2><p>Every project below links to public evidence. No traffic or ranking figures are claimed.</p></div>
    <article class="wk-feat"><div><p class="wk-cat">{E(fw['category'])} · {E(fw['status'])}</p><h3>{E(fw['title'])}</h3><p>{E(fw['summary'])}</p><p class="cta"><a class="btn btn-p" href="{ctx.to('work/')}">Read the case study</a></p></div>
      <ul class="wk-done">{"".join(f"<li>{E(x)}</li>" for x in fw['done'][:4])}</ul></article>
    <ul class="wks">{others}</ul>
  </div>
</section>

<section class="story" id="story" aria-labelledby="story-h">
  <div class="wrap story-in"><p class="eyebrow">The Lucky Domains story</p><h2 id="story-h">{E(C['company']['storyHeadline'])}</h2><div><p class="lede">{E(C['company']['story'])}</p><p>{E(C['company']['storyCoda'])}</p></div></div>
</section>

<section class="aiw" aria-labelledby="aiw-h">
  <div class="wrap">
    <div class="sec-hd"><p class="eyebrow">{E(aw['title'])}</p><h2 id="aiw-h">{E(aw['principle'])}</h2><p>{E(aw['intro'])}</p></div>
    <ul class="uses">{uses}</ul>
    <p class="aiw-ev">{E(aw['evidence'])}</p>
  </div>
</section>

<section class="lab" aria-labelledby="lab-h"><div class="wrap"><div class="sec-hd"><p class="eyebrow">From the lab</p><h2 id="lab-h">What Ken is testing.</h2><p>{E(C['labIntro'])} <a href="{f['kenashe']}">Full build records on KenAshe.ai</a>.</p></div><ul class="labs">{lab}</ul></div></section>

<section class="ins" id="insights" aria-labelledby="ins-h"><div class="wrap"><div class="sec-hd"><p class="eyebrow">Insights</p><h2 id="ins-h">Plain-English guides to the work.</h2><p class="concept-note">{E(C['insights']['label'])}</p></div><ul class="ins-l">{ins}</ul></div></section>

<section class="fnd" id="founder" aria-labelledby="fnd-h">
  <div class="wrap fnd-in"><img src="{ctx.asset(f['image'])}" alt="Ken Ashe, founder of Lucky Domains" width="280" height="280" loading="lazy">
  <div><p class="eyebrow">Founder</p><h2 id="fnd-h">{E(f['line'])}</h2><p>{E(f['bio'])}</p><p class="acc">{E(C['company']['accountability'])}</p><ul class="creds">{"".join(f"<li>{x}</li>" for x in f['credentials'])}<li>{E(f['membership'])}</li></ul><p><a class="lk" href="{f['kenashe']}">Ken's build-in-public site, KenAshe.ai</a></p></div></div>
</section>

<section class="contact" id="contact" aria-labelledby="ct-h">
  <div class="wrap ct-in"><div><p class="eyebrow">Contact</p><h2 id="ct-h">{E(C['contact']['title'])}</h2><p>{E(C['contact']['intro'])} {E(C['company']['consult'])}</p><p><a class="lk" href="mailto:{C['company']['email']}">{C['company']['email']}</a></p></div>{contact_form()}</div>
</section>"""


# ------------------------------------------------------------------ inner pages
def services(ctx):
    p = P["services"]
    rows = ""
    for s in C["services"]:
        rows += f"""<article class="svc" id="{s['id']}"><div class="svc-hd"><span class="svc-n">{s['n']}</span><h2>{E(s['name'])}</h2></div>
<div class="svc-b"><p class="lede">{E(s['lead'])}</p><p>{E(s['short'])}</p><a class="btn" href="{ctx.svc(s['id'])}">Explore {E(s['name'])}</a></div>
<ul class="svc-i">{"".join(f"<li>{E(x)}</li>" for x in s['includes'])}</ul></article>"""
    eng = "".join(f'<li><h3>{E(e["name"])}</h3><p>{E(e["line"])}</p></li>' for e in p["engagements"])
    return phd(p["eyebrow"], p["title"], p["lead"], [("Home", ctx.to())]) + f"""
<section class="svc-s"><div class="wrap"><ol class="svc-stk" aria-label="The order a presence is built">{"".join(f'<li>{chip(l["id"])}</li>' for l in C["stack"])}</ol>{rows}</div></section>
<section class="eng" aria-labelledby="eng-h"><div class="wrap"><div class="sec-hd"><p class="eyebrow">Ways to work together</p><h2 id="eng-h">Scoped in writing, before work starts.</h2><p>{E(p['pricing'])}</p></div><ul class="engs">{eng}</ul>
<div class="not"><h3>What Lucky Domains is not</h3><ul>{"".join(f"<li>{E(x)}</li>" for x in p['notList'])}</ul></div><p class="promise">{E(C['notPromised'])}</p></div></section>
{cta_band(ctx)}"""


def website(ctx):
    w = P["websites"]
    proc = "".join(f'<li><span>{i:02d}</span><h3>{E(x["name"])}</h3><p>{E(x["line"])}</p></li>' for i, x in enumerate(w["process"], 1))
    a = w["architecture"]
    col = lambda k: f'<div class="arch-c"><h3>{E(a[k]["label"])}</h3><ul>{"".join(f"<li>{E(x)}</li>" for x in a[k]["items"])}</ul></div>'
    return phd(w["eyebrow"], w["title"], w["lead"], [("Home", ctx.to()), ("Services", ctx.to("services/"))]) + f"""
<section class="prose-s"><div class="wrap two"><div>{"".join(f"<p>{E(x)}</p>" for x in w['intro'])}</div><div class="web-paths web-paths-1">{"".join(f'<article><h2>{E(p["name"])}</h2><p>{E(p["line"])}</p></article>' for p in w['paths'])}</div></div></section>
<section class="proc-s" aria-labelledby="proc-h"><div class="wrap"><div class="sec-hd"><p class="eyebrow">How a project runs</p><h2 id="proc-h">Six steps, from discovery to improvement.</h2></div><ol class="proc">{proc}</ol></div></section>
<section class="web" aria-labelledby="fd-h"><div class="wrap"><div class="sec-hd"><p class="eyebrow">Built into every site</p><h2 id="fd-h">The foundation search engines and AI systems rely on.</h2></div><ul class="found">{"".join(f'<li><h3>{E(f["name"])}</h3><p>{E(f["line"])}</p></li>' for f in w['foundations'])}</ul></div></section>
<section class="arch-s" aria-labelledby="ar-h"><div class="wrap"><div class="sec-hd"><p class="eyebrow">Information architecture</p><h2 id="ar-h">{E(a['title'])}</h2><p class="concept-note">{E(a['caption'])}</p></div><div class="arch">{col('before')}<span class="arch-arrow" aria-hidden="true">→</span>{col('after')}</div></div></section>
<section class="prose-s"><div class="wrap"><p class="promise">{E(w['not'])}</p><p>{E(w['proof'])} <a class="lk" href="{ctx.to('work/')}">Read the LuckyDomains.io case study</a></p></div></section>
{cta_band(ctx)}"""


def search(ctx):
    sp = P["search"]
    areas = "".join(f'<li><h3>{E(x["name"])}</h3><p>{E(x["line"])}</p></li>' for x in sp["seoAreas"])
    steps = "".join(f'<li><span>{i:02d}</span><h3>{E(x["name"])}</h3><p>{E(x["line"])}</p></li>' for i, x in enumerate(sp["aiSteps"], 1))
    aud = "".join(f'<li><h3>{E(x["name"])}</h3><p>{E(x["line"])}</p></li>' for x in C["aiShift"]["audiences"])
    return phd(sp["eyebrow"], sp["title"], sp["lead"], [("Home", ctx.to()), ("Services", ctx.to("services/"))]) + f"""
<section class="web" id="seo" aria-labelledby="seo-h"><div class="wrap"><div class="sec-hd"><p class="eyebrow">02 · {E(S['seo']['name'])}</p><h2 id="seo-h">{E(S['seo']['lead'])}</h2><p>{E(sp['seoIntro'])}</p></div><ul class="found found-3">{areas}</ul></div></section>
<section class="aud-s" aria-labelledby="aud-h"><div class="wrap"><div class="sec-hd"><p class="eyebrow">The shift</p><h2 id="aud-h">{E(C['aiShift']['title'])}</h2><p>{E(C['aiShift']['intro'])}</p></div><ul class="aud">{aud}</ul></div></section>
<section class="proc-s" id="ai-visibility" aria-labelledby="ai-h"><div class="wrap"><div class="sec-hd"><p class="eyebrow">03 · {E(S['ai']['name'])}</p><h2 id="ai-h">{E(S['ai']['short'])}</h2><p>{E(sp['aiIntro'])}</p></div><ol class="proc">{steps}</ol>
<div class="promise-2"><p><strong>What we will not promise.</strong> {E(C['notPromised'])}</p><p>{E(C['noSecret'])}</p></div></div></section>
<section class="story" aria-labelledby="cn-h"><div class="wrap story-in"><p class="eyebrow">How they connect</p><h2 id="cn-h">One system, not three services.</h2><div><p class="lede">{E(sp['connect'])}</p><p><a class="lk" href="{ctx.svc('entity')}">Entity SEO and digital identity</a></p></div></div></section>
{cta_band(ctx)}"""


def domains(ctx):
    dp = P["domains"]; ag = dp["agents"]
    acq = "".join(f'<li><span>{i:02d}</span><h3>{E(x["name"])}</h3><p>{E(x["line"])}</p></li>' for i, x in enumerate(dp["acquisition"], 1))
    topics = "".join(f'<li><h3>{E(t["name"])}</h3><p>{E(t["line"])}</p></li>' for t in ag["topics"])
    ev = "".join(f'<li><p class="lab-k"><span class="tag">{E(x["status"])}</span>{E(x["kind"])}</p><h4><a href="{x["url"]}">{E(x["name"])}</a></h4><p>{E(x["line"])}</p><p class="lab-lim">{E(x["limit"])}</p></li>' for x in C["lab"][:2])
    return phd(dp["eyebrow"], dp["title"], dp["lead"], [("Home", ctx.to()), ("Services", ctx.to("services/"))]) + f"""
<section class="prose-s"><div class="wrap"><p class="lede narrow">{E(dp['anchors'])}</p></div></section>
<section class="proc-s" id="domains" aria-labelledby="dm-h"><div class="wrap"><div class="sec-hd"><p class="eyebrow">05 · {E(S['domains']['name'])}</p><h2 id="dm-h">{E(S['domains']['lead'])}</h2><p>{E(S['domains']['short'])}</p></div><ol class="proc proc-4">{acq}</ol>
<div class="two two-gap"><div class="sell"><h3 id="selling">Selling a domain</h3><p>{E(dp['selling'])}</p></div><div><p class="promise"><strong>Fee.</strong> {E(dp['terms'])}</p><ul class="not-l">{"".join(f"<li>{E(x)}</li>" for x in dp['notList'])}</ul></div></div>
<p class="cta"><a class="btn btn-p" href="{ctx.home('#contact')}">Tell Ken the domain you want</a></p></div></section>
<section class="web" id="entity" aria-labelledby="en-h"><div class="wrap"><div class="sec-hd"><p class="eyebrow">04 · {E(S['entity']['name'])}</p><h2 id="en-h">{E(S['entity']['lead'])}</h2><p>{E(S['entity']['short'])} {E(C['notPromised'].split('.')[0])}.</p></div>
<div class="idg"><article><h3>Identity for people</h3><ul>{"".join(f"<li>{E(x)}</li>" for x in dp['people'])}</ul></article><article><h3>Identity for businesses</h3><ul>{"".join(f"<li>{E(x)}</li>" for x in dp['business'])}</ul></article></div></div></section>
<section class="agents" id="agents" aria-labelledby="ag-h"><div class="wrap"><div class="sec-hd"><p class="eyebrow"><span class="tag tag-amber">{E(ag['label'])}</span></p><h2 id="ag-h">{E(ag['question'])}</h2><p>{E(ag['intro'])}</p></div>
<ul class="topics">{topics}</ul><p class="caution">{E(ag['caution'])}</p><h3 class="sub">Supporting experiments</h3><ul class="labs labs-2">{ev}</ul></div></section>
{cta_band(ctx)}"""


def work(ctx):
    w = C["work"][0]
    ev = "".join(f'<li><a class="lk" href="{u}">{E(t)}</a></li>' for t, u in w["evidence"])
    others = ""
    for x in C["work"][1:]:
        evs = "".join(f'<a class="lk" href="{u}">{E(t)}</a>' for t, u in x["evidence"])
        demo = x.get("concept")
        body = (f'<dl class="cs-mini">{"".join(f"<div><dt>{k}</dt><dd>{v}</dd></div>" for k, v in [("Problem", "[What the client needed, in their words]"), ("Approach", "[Valuation, outreach, negotiation, escrow]"), ("Work completed", "[Steps taken]"), ("Evidence available", "[Only what the client permits]"), ("Current status", "[Closed or in progress]"), ("Lessons", "[What we would repeat]")])}</dl>') if demo else ""
        others += f'<article class="wk{" wk-demo" if demo else ""}"><p class="wk-cat">{E(x["category"])} · {E(x["client"])}{" · " + E(x["status"]) if x["status"] else ""}</p><h3>{E(x["title"])}</h3><p>{E(x["summary"])}</p>{"<p class=concept-note>" + E(x["note"]) + "</p>" if x.get("note") else ""}{body}<p class="wk-ev">{evs}</p></article>'
    return phd("Work", "Real projects, with the evidence attached.", "Case studies use only public evidence. Where a client's details cannot be shared, the layout is shown with placeholders and labeled.", [("Home", ctx.to())]) + f"""
<article class="cs" aria-labelledby="cs-h"><div class="wrap">
  <header class="cs-hd"><p class="wk-cat">{E(w['category'])} · {E(w['client'])}</p><h2 id="cs-h">{E(w['title'])}</h2><p class="lede">{E(w['summary'])}</p>
  <dl class="cs-meta"><div><dt>Year</dt><dd>{w['year']}</dd></div><div><dt>Status</dt><dd>{E(w['status'])}</dd></div><div><dt>Layers</dt><dd>{"".join(chip(l) for l in w['layers'])}</dd></div></dl></header>
  <div class="cs-grid">
    <section><h3>Problem</h3><p>{E(w['problem'])}</p></section>
    <section><h3>Approach</h3><p>{E(w['approach'])}</p><p>{E(w['built'])}</p></section>
    <section class="cs-wide"><h3>Work completed</h3><ul class="wk-done">{"".join(f"<li>{E(x)}</li>" for x in w['done'])}</ul></section>
    <section><h3>Evidence available</h3><ul class="ev">{ev}</ul><p class="concept-note">{E(w['noMetrics'])}</p></section>
    <section><h3>Current status</h3><p>{E(w['status'])}. A redesign is being explored in these concepts.</p></section>
    <section class="cs-wide"><h3>Lessons</h3><ul class="lessons">{"".join(f"<li>{E(x)}</li>" for x in w['lessons'])}</ul></section>
  </div>
</div></article>
<section class="work" aria-labelledby="mw-h"><div class="wrap"><div class="sec-hd"><h2 id="mw-h">More work</h2></div><div class="wk-grid">{others}</div></div></section>
{cta_band(ctx)}"""


def build():
    write(f"{DIR}/index.html", shell("", "Websites, SEO, and AI visibility", C["company"]["description"], home, "home"))
    write(f"{DIR}/services/index.html", shell("services/", "Services", P["services"]["lead"], services))
    write(f"{DIR}/services/website-design/index.html", shell("services/website-design/", "Website Design & Development", P["websites"]["lead"], website))
    write(f"{DIR}/services/search-ai-visibility/index.html", shell("services/search-ai-visibility/", "Search & AI Visibility", P["search"]["lead"], search))
    write(f"{DIR}/services/domain-identity/index.html", shell("services/domain-identity/", "Domain Strategy & Digital Identity", P["domains"]["lead"], domains))
    write(f"{DIR}/work/index.html", shell("work/", "Work", "Case studies with public evidence.", work))
