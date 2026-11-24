"""Phase 2, Concept C: Intelligent Presence. A light, interactive explanation of how recognition is built."""
import json
from p2lib import C, E, S, LAYER, Ctx, head, notice, nav_links, contact_form, write, scripts

DIR = "phase-2/intelligent-presence"
LABEL = "Concept C, Intelligent Presence"
P = C["pages"]
M = C["map"]
FONTS = ("manrope-normal-400-800.woff2",)


def tag(lid):
    return f'<span class="ltag l-{lid}">{E(LAYER[lid]["name"])}</span>'


def lst(items, cls="ticks"):
    return f'<ul class="{cls}">' + "".join("<li>%s</li>" % E(x) for x in items) + "</ul>"


def tiles(items, cls="tiles"):
    return f'<ul class="{cls}">' + "".join('<li><h3>%s</h3><p>%s</p></li>' % (E(x["name"]), E(x["line"])) for x in items) + "</ul>"


def shell(path, title, desc, body, cls=""):
    ctx = Ctx(DIR, path)
    svc = "".join(f'<li><a href="{ctx.svc(s["id"])}">{E(s["name"])}</a></li>' for s in C["services"])
    return f"""{head(ctx, f"{title} | Lucky Domains (Phase 2 concept C)", desc, "css/style.css", FONTS)}
<body class="{cls}">
<a class="skip" href="#main">Skip to content</a>
{notice(ctx, LABEL)}
<header class="hd">
  <div class="hd-in">
    <a class="hd-logo" href="{ctx.to()}" aria-label="Lucky Domains, concept home"><img src="{ctx.asset('logo-wordmark.png')}" alt="Lucky Domains" width="161" height="40"></a>
    <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="nav">Menu</button>
    <nav id="nav" class="nav" aria-label="Primary"><ul class="nav-l">{nav_links(ctx)}</ul><a class="btn btn-p nav-cta" href="{ctx.home('#contact')}">{E(C['navCta'])}</a></nav>
  </div>
</header>
<main id="main">
{body(ctx)}
</main>
<footer class="ft">
  <div class="ft-in">
    <div class="ft-brand"><img src="{ctx.asset('logo-wordmark.png')}" alt="Lucky Domains" width="177" height="44" loading="lazy"><p>{E(C['company']['description'])}</p><p><a class="lk" href="mailto:{C['company']['email']}">{C['company']['email']}</a></p></div>
    <div><h2>Services</h2><ul>{svc}</ul></div>
    <div><h2>Company</h2><ul><li><a href="{ctx.to('work/')}">Work</a></li><li><a href="{ctx.home('#story')}">About</a></li><li><a href="{ctx.home('#insights')}">Insights</a></li><li><a href="{ctx.home('#founder')}">Founder</a></li><li><a href="{ctx.home('#contact')}">Contact</a></li><li><a href="{C['founder']['kenashe']}">KenAshe.ai</a></li></ul></div>
  </div>
  <p class="ft-note"><span>{E(C['footer'])}</span><span>{E(C['deferredNote'])}</span></p>
</footer>
{scripts(ctx)}
</body></html>"""


def phd(eyebrow, title, lead, ctx, crumbs, layers=()):
    bc = '<nav class="crumbs" aria-label="Breadcrumb"><ol>' + "".join(f'<li><a href="{h}">{E(t)}</a></li>' for t, h in crumbs) + f'<li aria-current="page">{E(eyebrow)}</li></ol></nav>'
    lt = f'<p class="phd-l">{"".join(tag(l) for l in layers)}</p>' if layers else ""
    return f'<section class="phd"><div class="wrap">{bc}<p class="eyebrow">{E(eyebrow)}</p><h1>{E(title)}</h1><p class="lede">{E(lead)}</p>{lt}</div></section>'


def cta(ctx):
    return f"""<section class="cta-s" aria-labelledby="cta-h"><div class="wrap cta-in"><div><h2 id="cta-h">Find out where your presence is weakest.</h2><p>{E(C['contact']['intro'])} {E(C['company']['consult'])}</p></div>
<p class="cta"><a class="btn btn-p" href="{ctx.home('#contact')}">{E(C['navCta'])}</a><a class="btn" href="mailto:{C['company']['email']}">Email Ken</a></p></div></section>"""


def map_block(ctx):
    data = {"nodes": [dict(n, href=ctx.svc(n["service"]), svcName=S[n["service"]]["name"]) for n in M["nodes"]],
            "problems": M["problems"], "icon": ctx.asset("logo-icon-128.png"),
            "diag": {o["id"]: {"label": o["label"], "start": o["start"], "why": o["why"], "href": ctx.svc(o["service"])} for o in C["diagnostic"]["options"]}}
    fallback = "".join(f'<li><b>{E(n["label"])}</b> {E(n["line"])}</li>' for n in M["nodes"])
    blob = json.dumps(data).replace("</", "<\\/")
    probs = "".join(f'<button type="button" class="pb" data-problem="{o["id"]}" aria-pressed="false">{E(o["label"])}</button>' for o in C["diagnostic"]["options"])
    return f"""<div class="mp" data-map>
  <div class="mp-bar"><p class="mp-t" id="mp-t">Presence map</p><div class="seg" role="group" aria-label="Map state"><button type="button" class="sg" data-state="fragmented" aria-pressed="false">Fragmented</button><button type="button" class="sg" data-state="recognized" aria-pressed="true">Recognized</button></div></div>
  <div class="mp-view" aria-labelledby="mp-t"><ul class="mp-fallback">{fallback}</ul></div>
  <p class="mp-cap">{E(M['caption'])}</p>
  <script type="application/json" class="mp-data">{blob}</script>
</div>
<div class="probs"><p class="probs-h" id="pb-h">What is holding you back?</p><div class="pbs" role="group" aria-labelledby="pb-h">{probs}</div>
<div class="mp-card" aria-live="polite"><p class="mc-k">Start here</p><h2>Pick a problem, or select any signal on the map.</h2><p>The map highlights the signals involved and the service that fixes them.</p></div></div>"""


# ------------------------------------------------------------------ home
def home(ctx):
    h = C["hero"]; f = C["founder"]
    tabs = "".join(f'<button type="button" role="tab" id="tb-{l["id"]}" aria-controls="tp-{l["id"]}" aria-selected="{"true" if i == 0 else "false"}" tabindex="{0 if i == 0 else -1}"><span>{i + 1:02d}</span>{E(l["name"])}</button>' for i, l in enumerate(C["stack"]))
    panels = ""
    for i, l in enumerate(C["stack"]):
        nodes = [n["label"] for n in M["nodes"] if n["layer"] == l["id"]]
        panels += f'<div class="tp" role="tabpanel" id="tp-{l["id"]}" aria-labelledby="tb-{l["id"]}" tabindex="0"><p class="eyebrow">Layer {i + 1:02d}</p><h3>{E(l["line"])}</h3><p>{E(l["detail"])}</p><p class="tp-n"><b>Signals:</b> {E(", ".join(nodes))}</p><a class="lk" href="{ctx.svc(l["service"])}">{E(S[l["service"]]["name"])}</a></div>'
    outs = "".join(f'<li><p class="o-tags">{"".join(tag(x) for x in o["layers"])}</p><h3>{E(o["title"])}</h3><p>{E(o["line"])}</p></li>' for o in C["outcomes"])
    w = P["websites"]; sp = P["search"]
    sig = "".join(f'<article class="sig"><p class="o-tags">{tag(t)}</p><h3>{E(S[sid]["name"])}</h3><p>{E(S[sid]["short"])}</p>{lst(S[sid]["includes"][:5], "ticks ticks-s")}<a class="lk" href="{ctx.svc(sid)}">How it works</a></article>' for sid, t in [("seo", "search"), ("entity", "entity"), ("ai", "ai")])
    fw = C["work"][0]
    wk = "".join(f'<li class="wt{" wt-demo" if x.get("concept") else ""}"><p class="o-tags">{"".join(tag(l) for l in x["layers"])}</p><h3>{E(x["title"])}</h3><p>{E(x["summary"])}</p><p class="wt-m">{E(x["client"])}{" · " + E(x["status"]) if x["status"] else ""}</p></li>' for x in C["work"][1:4])
    aw = C["aiWork"]
    uses = "".join(f'<li><b>{E(u["name"])}</b><span>{E(u["line"])}</span></li>' for u in aw["uses"])
    lab = "".join(f'<li><span class="pill">{E(x["status"])}</span><a href="{x["url"]}"><b>{E(x["name"])}</b></a><span>{E(x["line"])}</span><em>{E(x["limit"])}</em></li>' for x in C["lab"])
    ins = "".join(f'<li>{tag(i["layer"])}<b>{E(i["title"])}</b><span>{E(i["kind"])}</span></li>' for i in C["insights"]["items"])
    return f"""
<section class="hero" aria-labelledby="hero-h">
  <div class="wrap hero-in">
    <div class="hero-copy">
      <p class="eyebrow">{E(h['eyebrow'])}</p>
      <h1 id="hero-h">{E(h['headlineC'])}</h1>
      <p class="lede">{E(h['support'])}</p>
      <p class="cta"><a class="btn btn-p" href="#contact">{E(h['cta1'])}</a><a class="btn" href="{ctx.to('services/')}">{E(h['cta2'])}</a></p>
      <p class="fl"><img src="{ctx.asset(f['image'])}" alt="" width="40" height="40">{E(C['company']['founderLine'])}</p>
    </div>
    <div class="hero-map">{map_block(ctx)}</div>
  </div>
</section>

<section class="layers" aria-labelledby="ly-h"><div class="wrap">
  <div class="sec-hd"><p class="eyebrow">The Digital Presence Stack</p><h2 id="ly-h">Five layers. Each one makes the next one work.</h2><p>{E(C['stackReinforce'])}</p></div>
  <div class="tx"><div class="tabs" role="tablist" aria-label="Layers of a digital presence">{tabs}</div><div class="tps">{panels}</div></div>
</div></section>

<section class="outs-s" aria-labelledby="out-h"><div class="wrap"><div class="sec-hd"><p class="eyebrow">Outcomes</p><h2 id="out-h">What a connected presence gives you.</h2></div><ul class="outs">{outs}</ul></div></section>

<section class="mod" aria-labelledby="web-h"><div class="wrap">
  <div class="mod-hd"><p class="o-tags">{tag('website')}</p><h2 id="web-h">{E(w['title'])}</h2><p class="lede">{E(w['lead'])}</p></div>
  <div class="mod-g"><div class="mod-paths">{tiles(w['paths'], 'tiles tiles-1')}</div><div>{tiles(w['foundations'][:6], 'tiles tiles-2')}</div></div>
  <p class="cta"><a class="btn btn-p" href="{ctx.svc('websites')}">Website design and development</a></p>
</div></section>

<section class="sigs-s" aria-labelledby="sg-h"><div class="wrap">
  <div class="sec-hd"><p class="eyebrow">Search, entity, and AI visibility</p><h2 id="sg-h">{E(sp['title'])}</h2><p>{E(sp['connect'])}</p></div>
  <div class="sigs">{sig}</div>
  <p class="note">{E(C['notPromised'])}</p>
</div></section>

<section class="wk-s" aria-labelledby="wk-h"><div class="wrap">
  <div class="sec-hd"><p class="eyebrow">Selected work</p><h2 id="wk-h">Projects mapped to the layers they touched.</h2><p>Every project links to public evidence. No traffic or ranking figures are claimed.</p></div>
  <article class="wf"><div><p class="o-tags">{"".join(tag(l) for l in fw['layers'])}</p><h3>{E(fw['title'])}</h3><p>{E(fw['summary'])}</p><p class="cta"><a class="btn btn-p" href="{ctx.to('work/')}">Open the case study</a></p></div>{lst(fw['done'][:4])}</article>
  <ul class="wts">{wk}</ul>
</div></section>

<section class="story" id="story" aria-labelledby="st-h"><div class="wrap st-in"><p class="eyebrow">The Lucky Domains story</p><h2 id="st-h">{E(C['company']['storyHeadline'])}</h2><div><p class="lede">{E(C['company']['story'])}</p><p>{E(C['company']['storyCoda'])}</p></div></div></section>

<section class="aiw" aria-labelledby="aw-h"><div class="wrap aw-in">
  <div><p class="eyebrow">{E(aw['title'])}</p><h2 id="aw-h">{E(aw['principle'])}</h2><p>{E(aw['intro'])}</p><p class="note">{E(aw['evidence'])}</p></div>
  <ul class="uses">{uses}</ul>
</div></section>

<section class="mini" aria-label="From the lab and insights"><div class="wrap mini-in">
  <div class="lab"><p class="eyebrow">From the lab</p><h2>What Ken is testing</h2><p>{E(C['labIntro'])}</p><ul class="lab-l">{lab}</ul><a class="lk" href="{f['kenashe']}">Build records on KenAshe.ai</a></div>
  <div class="ins" id="insights"><p class="eyebrow">Insights</p><h2>Guides to the work</h2><p class="cn">{E(C['insights']['label'])}</p><ul class="ins-l">{ins}</ul></div>
</div></section>

<section class="fnd" id="founder" aria-labelledby="fd-h"><div class="wrap fd-in"><img src="{ctx.asset(f['image'])}" alt="Ken Ashe, founder of Lucky Domains" width="200" height="200" loading="lazy">
<div><p class="eyebrow">Founder</p><h2 id="fd-h">{E(f['line'])}</h2><p>{E(f['bio'])}</p><p class="acc">{E(C['company']['accountability'])}</p><p class="o-tags">{"".join(f"<span class=pill>{x}</span>" for x in f['credentials'])}</p></div></div></section>

<section class="ct" id="contact" aria-labelledby="ct-h"><div class="wrap ct-in"><div><p class="eyebrow">Contact</p><h2 id="ct-h">{E(C['contact']['title'])}</h2><p>{E(C['contact']['intro'])} {E(C['company']['consult'])}</p><p><a class="lk" href="mailto:{C['company']['email']}">{C['company']['email']}</a></p></div>{contact_form()}</div></section>"""


# ------------------------------------------------------------------ inner
def services(ctx):
    p = P["services"]
    cards = "".join(f'<li class="sc" id="{s["id"]}"><p class="o-tags">{"".join(tag(l["id"]) for l in C["stack"] if l["service"] == s["id"])}</p><span class="sc-n">{s["n"]}</span><h2>{E(s["name"])}</h2><p class="sc-l">{E(s["lead"])}</p>{lst(s["includes"], "ticks ticks-s")}<a class="btn" href="{ctx.svc(s["id"])}">Explore {E(s["name"])}</a></li>' for s in C["services"])
    eng = "".join(f'<li><h3>{E(e["name"])}</h3><p>{E(e["line"])}</p></li>' for e in p["engagements"])
    return phd(p["eyebrow"], p["title"], p["lead"], ctx, [("Home", ctx.to())]) + f"""
<section class="sv-s"><div class="wrap"><ul class="scs">{cards}</ul></div></section>
<section class="outs-s" aria-labelledby="en-h"><div class="wrap"><div class="sec-hd"><p class="eyebrow">Ways to work together</p><h2 id="en-h">Scoped in writing, before work starts.</h2><p>{E(p['pricing'])}</p></div><ul class="outs">{eng}</ul>
<p class="note">{E(" · ".join(p['notList']))}. {E(C['notPromised'])}</p></div></section>{cta(ctx)}"""


def website(ctx):
    w = P["websites"]; g = C["siteGraph"]
    tiers = {}
    for pid, label, t in g["pages"]:
        tiers.setdefault(t, []).append((pid, label))
    graph = "".join(f'<div class="gr-t">{"".join(f"<button type=button class=gn data-page={pid} aria-pressed=false>{E(label)}</button>" for pid, label in row)}</div>' for t, row in sorted(tiers.items()))
    names = {pid: label for pid, label, _ in g["pages"]}
    adj = {}
    for a, b in g["links"]:
        adj.setdefault(a, []).append(b); adj.setdefault(b, []).append(a)
    linklist = "".join(f'<li><b>{E(names[pid])}</b> links with {E(", ".join(names[x] for x in adj[pid]))}.</li>' for pid, _, _ in g["pages"])
    gdata = json.dumps({"links": g["links"]})
    proc = "".join(f'<li><span>{i:02d}</span><h3>{E(x["name"])}</h3><p>{E(x["line"])}</p></li>' for i, x in enumerate(w["process"], 1))
    return phd(w["eyebrow"], w["title"], w["lead"], ctx, [("Home", ctx.to()), ("Services", ctx.to("services/"))], ["website"]) + f"""
<section class="mod" aria-labelledby="ap-h"><div class="wrap"><div class="sec-hd"><p class="eyebrow">The approach</p><h2 id="ap-h">Structure before style.</h2></div></div><div class="wrap two"><div>{"".join(f"<p>{E(x)}</p>" for x in w['intro'])}</div>{tiles(w['paths'], 'tiles tiles-1')}</div></section>
<section class="graph-s" aria-labelledby="gr-h"><div class="wrap">
  <div class="sec-hd"><p class="eyebrow">Internal linking</p><h2 id="gr-h">{E(P['websites']['architecture']['title'])}</h2><p>Select a page to see what it links to. Every service page connects to proof and to contact, and nothing important is more than two clicks from home.</p></div>
  <div class="gr" data-graph><svg class="gr-svg" aria-hidden="true"></svg>{graph}<script type="application/json" class="gr-data">{gdata}</script></div>
  <p class="cap">{E(g['caption'])}</p>
  <details class="gr-list"><summary>Read the links as a list</summary><ul>{linklist}</ul></details>
</div></section>
<section class="outs-s" aria-labelledby="pr-h"><div class="wrap"><div class="sec-hd"><p class="eyebrow">How a project runs</p><h2 id="pr-h">Six steps, from discovery to improvement.</h2></div><ol class="proc">{proc}</ol></div></section>
<section class="mod" aria-labelledby="fd-h"><div class="wrap"><div class="sec-hd"><p class="eyebrow">Built into every site</p><h2 id="fd-h">The foundation search engines and AI systems rely on.</h2></div>{tiles(w['foundations'], 'tiles tiles-4')}
<p class="note">{E(w['not'])}</p><p>{E(w['proof'])} <a class="lk" href="{ctx.to('work/')}">Read the case study</a></p></div></section>{cta(ctx)}"""


def search(ctx):
    sp = P["search"]
    steps = "".join(f'<li><span>{i:02d}</span><h3>{E(x["name"])}</h3><p>{E(x["line"])}</p></li>' for i, x in enumerate(sp["aiSteps"], 1))
    aud = "".join(f'<li><h3>{E(x["name"])}</h3><p>{E(x["line"])}</p></li>' for x in C["aiShift"]["audiences"])
    return phd(sp["eyebrow"], sp["title"], sp["lead"], ctx, [("Home", ctx.to()), ("Services", ctx.to("services/"))], ["search", "entity", "ai"]) + f"""
<section class="mod" id="seo" aria-labelledby="seo-h"><div class="wrap"><div class="sec-hd"><p class="o-tags">{tag('search')}</p><h2 id="seo-h">{E(S['seo']['lead'])}</h2><p>{E(sp['seoIntro'])}</p></div>{tiles(sp['seoAreas'], 'tiles tiles-3')}</div></section>
<section class="outs-s" aria-labelledby="au-h"><div class="wrap"><div class="sec-hd"><p class="eyebrow">The shift</p><h2 id="au-h">{E(C['aiShift']['title'])}</h2><p>{E(C['aiShift']['intro'])}</p></div><ul class="aud">{aud}</ul></div></section>
<section class="mod" id="ai-visibility" aria-labelledby="ai-h"><div class="wrap"><div class="sec-hd"><p class="o-tags">{tag('ai')}</p><h2 id="ai-h">{E(S['ai']['short'])}</h2><p>{E(sp['aiIntro'])}</p></div><ol class="proc">{steps}</ol>
<div class="note-2"><p><b>What we will not promise.</b> {E(C['notPromised'])}</p><p>{E(C['noSecret'])}</p></div></div></section>
<section class="story" aria-labelledby="cn-h"><div class="wrap st-in"><p class="eyebrow">How they connect</p><h2 id="cn-h">One system, not three services.</h2><div><p class="lede">{E(sp['connect'])}</p><a class="lk" href="{ctx.svc('entity')}">Entity SEO and digital identity</a></div></div></section>{cta(ctx)}"""


def domains(ctx):
    dp = P["domains"]; ag = dp["agents"]
    acq = "".join(f'<li><span>{i:02d}</span><h3>{E(x["name"])}</h3><p>{E(x["line"])}</p></li>' for i, x in enumerate(dp["acquisition"], 1))
    lab = "".join(f'<li><span class="pill">{E(x["status"])}</span><a href="{x["url"]}"><b>{E(x["name"])}</b></a><span>{E(x["line"])}</span><em>{E(x["limit"])}</em></li>' for x in C["lab"][:2])
    return phd(dp["eyebrow"], dp["title"], dp["lead"], ctx, [("Home", ctx.to()), ("Services", ctx.to("services/"))], ["domain", "entity"]) + f"""
<section class="mod"><div class="wrap anchor">
  <div class="an-c"><span class="an-d">yourname.com</span></div>
  <div><p class="lede">{E(dp['anchors'])}</p></div>
</div></section>
<section class="outs-s" id="domains" aria-labelledby="dm-h"><div class="wrap"><div class="sec-hd"><p class="o-tags">{tag('domain')}</p><h2 id="dm-h">{E(S['domains']['lead'])}</h2><p>{E(S['domains']['short'])}</p></div><ol class="proc proc-4">{acq}</ol>
<div class="two two-gap"><div class="tile-x" id="selling"><h3>Selling a domain</h3><p>{E(dp['selling'])}</p></div><div class="tile-x"><h3>Fee</h3><p>{E(dp['terms'])}</p>{lst(dp['notList'], 'ticks ticks-x')}</div></div>
<p class="cta"><a class="btn btn-p" href="{ctx.home('#contact')}">Tell Ken the domain you want</a></p></div></section>
<section class="mod" id="entity" aria-labelledby="en-h"><div class="wrap"><div class="sec-hd"><p class="o-tags">{tag('entity')}</p><h2 id="en-h">{E(S['entity']['lead'])}</h2><p>{E(S['entity']['short'])}</p></div>
<div class="two"><div class="tile-x"><h3>For people</h3>{lst(dp['people'])}</div><div class="tile-x"><h3>For businesses</h3>{lst(dp['business'])}</div></div></div></section>
<section class="rsch" id="agents" aria-labelledby="ag-h"><div class="wrap"><div class="sec-hd"><p class="eyebrow"><span class="pill pill-a">{E(ag['label'])}</span></p><h2 id="ag-h">{E(ag['question'])}</h2><p>{E(ag['intro'])}</p></div>
{tiles(ag['topics'], 'tiles tiles-4')}<p class="note note-a">{E(ag['caution'])}</p><h3 class="sub">Supporting experiments</h3><ul class="lab-l lab-2">{lab}</ul></div></section>{cta(ctx)}"""


def work(ctx):
    w = C["work"][0]
    ev = "".join(f'<li><a class="lk" href="{u}">{E(t)}</a></li>' for t, u in w["evidence"])
    blocks = [("Problem", f"<p>{E(w['problem'])}</p>"), ("Approach", f"<p>{E(w['approach'])}</p><p>{E(w['built'])}</p>"),
              ("Work completed", lst(w["done"])), ("Evidence available", f'<ul class="ev">{ev}</ul><p class="note">{E(w["noMetrics"])}</p>'),
              ("Current status", f"<p>{E(w['status'])}. A redesign is being explored in these concepts.</p>"), ("Lessons", lst(w["lessons"], "ticks ticks-l"))]
    grid = "".join(f'<section class="cb{" cb-w" if t in ("Work completed", "Lessons") else ""}"><h3>{t}</h3>{b}</section>' for t, b in blocks)
    more = ""
    for x in C["work"][1:]:
        demo = x.get("concept")
        more += f'<li class="wt{" wt-demo" if demo else ""}"><p class="o-tags">{"".join(tag(l) for l in x["layers"])}</p><h3>{E(x["title"])}</h3><p>{E(x["summary"])}</p><p class="wt-m">{E(x["client"])}{" · " + E(x["status"]) if x["status"] else ""}</p>{"".join(f"<a class=lk href={u}>{E(t)}</a>" for t, u in x["evidence"])}</li>'
    return phd("Work", w["title"], w["summary"], ctx, [("Home", ctx.to())], w["layers"]) + f"""
<section class="mod" aria-labelledby="cs-h"><div class="wrap"><div class="sec-hd"><p class="eyebrow">Case study</p><h2 id="cs-h">How the project ran</h2></div><dl class="cs-meta"><div><dt>Category</dt><dd>{E(w['category'])}</dd></div><div><dt>Client</dt><dd>{E(w['client'])}</dd></div><div><dt>Year</dt><dd>{w['year']}</dd></div><div><dt>Status</dt><dd>{E(w['status'])}</dd></div></dl><div class="cbs">{grid}</div></div></section>
<section class="outs-s" aria-labelledby="mw-h"><div class="wrap"><div class="sec-hd"><h2 id="mw-h">More work</h2></div><ul class="wts wts-2">{more}</ul></div></section>{cta(ctx)}"""


def build():
    write(f"{DIR}/index.html", shell("", "Make your business easy to find, understand, and trust", C["company"]["description"], home, "home"))
    write(f"{DIR}/services/index.html", shell("services/", "Services", P["services"]["lead"], services))
    write(f"{DIR}/services/website-design/index.html", shell("services/website-design/", "Website Design & Development", P["websites"]["lead"], website))
    write(f"{DIR}/services/search-ai-visibility/index.html", shell("services/search-ai-visibility/", "Search & AI Visibility", P["search"]["lead"], search))
    write(f"{DIR}/services/domain-identity/index.html", shell("services/domain-identity/", "Domain Strategy & Digital Identity", P["domains"]["lead"], domains))
    write(f"{DIR}/work/index.html", shell("work/", "Work", C["work"][0]["summary"], work))
