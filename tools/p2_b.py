"""Phase 2, Concept B: Editorial Authority. A content-led studio: warm paper, serif headlines, annotated evidence."""
from p2lib import C, E, S, LAYER, Ctx, head, notice, nav_links, contact_form, write, scripts

DIR = "phase-2/editorial-authority"
LABEL = "Concept B, Editorial Authority"
P = C["pages"]
FONTS = ("newsreader-normal-300-700.woff2", "publicsans-normal-400-700.woff2")
ROMAN = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII"]


def paths_html(w):
    return '<div class="paths">' + "".join("<div><h3>%s</h3><p>%s</p></div>" % (E(p["name"]), E(p["line"])) for p in w["paths"]) + "</div>"


def fn_list(items, cls="fn fn-2"):
    return '<ol class="%s">' % cls + "".join("<li><b>%s</b> %s</li>" % (E(x["name"]), E(x["line"])) for x in items) + "</ol>"


def inc(items):
    return '<ul class="inc">' + "".join("<li>%s</li>" % E(x) for x in items) + "</ul>"


def shell(path, title, desc, body, toc=None, cls=""):
    ctx = Ctx(DIR, path)
    rail = ""
    if toc:
        rail = '<nav class="rail" aria-label="On this page"><p class="rail-h">On this page</p><ol>' + "".join(f'<li><a href="#{i}" data-toc="{i}"><span>{ROMAN[k]}</span>{E(t)}</a></li>' for k, (i, t) in enumerate(toc)) + '</ol><i class="rail-bar" aria-hidden="true"><i></i></i></nav>'
    svc = "".join(f'<li><a href="{ctx.svc(s["id"])}">{E(s["name"])}</a></li>' for s in C["services"])
    return f"""{head(ctx, f"{title} | Lucky Domains (Phase 2 concept B)", desc, "css/style.css", FONTS)}
<body class="{cls}">
<a class="skip" href="#main">Skip to content</a>
{notice(ctx, LABEL)}
<header class="mh">
  <div class="mh-in">
    <a class="mh-logo" href="{ctx.to()}" aria-label="Lucky Domains, concept home"><img src="{ctx.asset('logo-wordmark.png')}" alt="Lucky Domains" width="161" height="40"></a>
    <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="nav">Menu</button>
    <nav id="nav" class="nav" aria-label="Primary"><ul class="nav-l">{nav_links(ctx)}</ul><a class="nav-cta" href="{ctx.home('#contact')}">{E(C['navCta'])}</a></nav>
  </div>
  <i class="progress" aria-hidden="true"></i>
</header>
<main id="main" class="{'has-rail' if toc else ''}">
{rail}
<div class="flow">
{body(ctx)}
</div>
</main>
<footer class="colo">
  <div class="colo-in">
    <div><img src="{ctx.asset('logo-wordmark.png')}" alt="Lucky Domains" width="177" height="44" loading="lazy"><p class="colo-d">{E(C['company']['studio'])}</p><p><a href="mailto:{C['company']['email']}">{C['company']['email']}</a></p></div>
    <div><h2>Services</h2><ul>{svc}</ul></div>
    <div><h2>Studio</h2><ul><li><a href="{ctx.to('work/')}">Work</a></li><li><a href="{ctx.home('#story')}">About</a></li><li><a href="{ctx.home('#insights')}">Insights</a></li><li><a href="{ctx.home('#founder')}">Founder</a></li><li><a href="{ctx.home('#contact')}">Contact</a></li><li><a href="{C['founder']['kenashe']}">KenAshe.ai</a></li></ul></div>
  </div>
  <p class="colo-n"><span>{E(C['footer'])}</span> <span>{E(C['deferredNote'])}</span></p>
</footer>
{scripts(ctx)}
</body></html>"""


def chap(cid, n, kicker, title, inner, cls=""):
    return f'<section class="ch {cls}" id="{cid}" aria-labelledby="{cid}-h"><header class="ch-hd"><p class="kick"><span>{n}</span>{E(kicker)}</p><h2 id="{cid}-h">{E(title)}</h2></header>{inner}</section>'


def closing(ctx):
    return f"""<section class="close" aria-labelledby="close-h"><h2 id="close-h">Start with a conversation.</h2><p>{E(C['contact']['intro'])} {E(C['company']['consult'])}</p>
<p class="acts"><a class="btn" href="{ctx.home('#contact')}">{E(C['navCta'])}</a><a class="tl" href="mailto:{C['company']['email']}">{C['company']['email']}</a></p></section>"""


def phd(kick, title, lead, ctx, crumbs):
    bc = '<nav class="crumbs" aria-label="Breadcrumb"><ol>' + "".join(f'<li><a href="{h}">{E(t)}</a></li>' for t, h in crumbs) + f'<li aria-current="page">{E(kick)}</li></ol></nav>'
    return f'<header class="phd">{bc}<p class="kick">{E(kick)}</p><h1>{E(title)}</h1><p class="stand">{E(lead)}</p></header>'


# ------------------------------------------------------------------ home
def home(ctx):
    h = C["hero"]; f = C["founder"]
    eras = "".join(f'<li class="era" data-era><span class="era-n">{e["n"]}</span><div><p class="era-k">{E(LAYER[e["layer"]]["name"])} · {E(e["era"])}</p><h3>{E(LAYER[e["layer"]]["line"])}</h3><p>{E(e["line"])}</p></div></li>' for e in C["eras"])
    toc = "".join(f'<li><a href="{ctx.svc(s["id"])}"><span class="toc-n">{s["n"]}</span><span class="toc-t">{E(s["name"])}</span><span class="toc-s">{E(s["short"])}</span></a></li>' for s in C["services"])
    outs = "".join(f'<li><h3>{E(o["title"])}</h3><p>{E(o["line"])}</p></li>' for o in C["outcomes"])
    w = P["websites"]; sp = P["search"]; fw = C["work"][0]
    ann = C["annotations"]
    done = fw["done"]
    marks = {0: "1", 1: "2", 3: "3", 5: "4"}
    done_h = "".join(f'<li>{E(x)}{f" <button class=mk type=button aria-describedby=an-{marks[i]} data-mk={marks[i]}>{marks[i]}</button>" if i in marks else ""}</li>' for i, x in enumerate(done))
    notes = "".join(f'<li id="an-{a["n"]}" data-note="{a["n"]}"><span>{a["n"]}</span>{E(a["note"])}</li>' for a in ann)
    aw = C["aiWork"]
    uses = "".join(f'<li><b>{E(u["name"])}.</b> {E(u["line"])}</li>' for u in aw["uses"])
    ins = C["insights"]
    art = "".join(f'<article class="art{" art-lead" if i == 0 else ""}"><p class="art-k">{E(it["kind"])} · {E(LAYER[it["layer"]]["name"])}</p><h3>{E(it["title"])}</h3><p class="art-s">Planned</p></article>' for i, it in enumerate(ins["items"]))
    lab = "".join(f'<li><a href="{x["url"]}"><b>{E(x["name"])}</b></a> <span class="st">{E(x["status"])}</span> {E(x["line"])} <em>{E(x["limit"])}</em></li>' for x in C["lab"])
    return f"""
<header class="cover" aria-labelledby="hero-h">
  <p class="kick">{E(h['eyebrow'])}</p>
  <h1 id="hero-h">{E(h['headlineB'])}</h1>
  <div class="cover-cols">
    <p class="stand">{E(C['company']['description'])}</p>
    <div><p>{E(h['support'])}</p><p class="acts"><a class="btn" href="#contact">{E(h['cta1'])}</a><a class="tl" href="{ctx.to('services/')}">{E(h['cta2'])}</a></p><p class="byline"><img src="{ctx.asset(f['image'])}" alt="" width="44" height="44">{E(C['company']['founderLine'])}</p></div>
  </div>
</header>

<section class="index" aria-labelledby="ix-h"><h2 id="ix-h" class="lab-h">The services</h2><ol class="toc">{toc}</ol></section>

<section class="eras" aria-labelledby="er-h"><header class="ch-hd"><p class="kick"><span>I</span>The Digital Presence Stack</p><h2 id="er-h">Domain, website, search, entity, AI. Each era of discovery added a layer. None replaced the last.</h2></header>
  <div class="era-wrap" data-eras><i class="era-line" aria-hidden="true"><i></i></i><ol class="era-l">{eras}</ol></div>
  <p class="pull">{E(C['stackReinforce'])}</p>
  <ul class="outs">{outs}</ul>
</section>

{chap('websites', 'II', S['websites']['name'], w['title'], f'''<div class="feat"><div class="feat-main"><p class="drop">{E(w['intro'][0])}</p><p>{E(w['intro'][1])}</p>
{paths_html(w)}</div>
<div class="feat-side" role="group" aria-label="Built into every site"><h3 class="lab-h">Built into every site</h3>{fn_list(w["foundations"], "fn")}</div></div>
<p class="acts"><a class="btn" href="{ctx.svc('websites')}">Website design and development</a></p>''')}

{chap('visibility', 'III', 'Search, entity, and AI visibility', sp['title'], f'''<p class="stand">{E(sp['lead'])}</p>
<div class="cols3">{"".join(f"<article><p class=lab-h>{t}</p><h3>{E(S[sid]['name'])}</h3><p>{E(x)}</p><a class=tl href={ctx.svc(sid)}>Read more</a></article>" for sid, t, x in [('seo', 'Search', sp['seoIntro']), ('entity', 'Entity', S['entity']['lead']), ('ai', 'AI visibility', S['ai']['lead'])])}</div>
<p class="sidebar"><b>What we will not promise.</b> {E(C['notPromised'])}</p>''')}

{chap('work-feature', 'IV', 'Selected work', fw['title'], f'''<div class="case"><div class="case-main"><p class="stand">{E(fw['summary'])}</p><p>{E(fw['problem'])}</p><h3 class="lab-h">Work completed</h3><ul class="done">{done_h}</ul><p class="case-x">{E(fw['noMetrics'])}</p>
<p class="acts"><a class="btn" href="{ctx.to('work/')}">Read the case study</a></p></div>
<div class="notes" role="group" aria-label="Annotations from the public decision log"><p class="lab-h">From the decision log</p><ol>{notes}</ol><p class="notes-src"><a class="tl" href="{fw['evidence'][1][1]}">Read DECISIONS.md</a></p></div></div>''')}

<section class="story" id="story" aria-labelledby="story-h"><p class="kick"><span>V</span>The Lucky Domains story</p><h2 id="story-h">{E(C['company']['storyHeadline'])}</h2><p class="stand">{E(C['company']['story'])}</p><p>{E(C['company']['storyCoda'])}</p></section>

{chap('method', 'VI', aw['title'], aw['principle'], f'''<div class="method"><p class="stand">{E(aw['intro'])}</p><ul class="notes-l">{uses}</ul></div><p class="sidebar">{E(aw['evidence'])}</p>''')}

<section class="insights" id="insights" aria-labelledby="ins-h"><header class="ch-hd"><p class="kick"><span>VII</span>Insights</p><h2 id="ins-h">Writing that explains the work.</h2><p class="tag-c">{E(ins['label'])}</p></header><div class="arts">{art}</div></section>

<section class="lab" aria-labelledby="lab-h"><h2 id="lab-h" class="lab-h">From the lab</h2><p>{E(C['labIntro'])}</p><ul class="lab-l">{lab}</ul><p><a class="tl" href="{f['kenashe']}">Full build records on KenAshe.ai</a></p></section>

<section class="founder" id="founder" aria-labelledby="fd-h"><figure><img src="{ctx.asset(f['image'])}" alt="Ken Ashe, founder of Lucky Domains" width="260" height="260" loading="lazy"><figcaption>Ken Ashe. {", ".join(f['credentials'])}.</figcaption></figure>
<div><p class="kick"><span>VIII</span>Founder</p><h2 id="fd-h">{E(f['line'])}</h2><p>{E(f['bio'])}</p><blockquote><p>{E(C['company']['accountability'])}</p></blockquote><p>{E(f['discipline'])} {E(f['membership'])}</p><p><a class="tl" href="{f['kenashe']}">KenAshe.ai, Ken's build-in-public site</a></p></div></section>

<section class="contact" id="contact" aria-labelledby="ct-h"><div><p class="kick">Contact</p><h2 id="ct-h">{E(C['contact']['title'])}</h2><p>{E(C['contact']['intro'])} {E(C['company']['consult'])}</p><p><a class="tl" href="mailto:{C['company']['email']}">{C['company']['email']}</a></p></div>{contact_form()}</section>"""


# ------------------------------------------------------------------ inner
def services(ctx):
    p = P["services"]
    body = ""
    for k, s in enumerate(C["services"]):
        body += chap(s["id"], ROMAN[k], s["name"], s["lead"], f'<div class="svc"><p class="stand">{E(s["short"])}</p><ul class="inc">{"".join(f"<li>{E(x)}</li>" for x in s["includes"])}</ul></div><p class="acts"><a class="btn" href="{ctx.svc(s["id"])}">Read about {E(s["name"])}</a></p>')
    eng = "".join(f'<li><h3>{E(e["name"])}</h3><p>{E(e["line"])}</p></li>' for e in p["engagements"])
    body += chap("engagements", "VI", "Ways to work together", "Scoped in writing, before work starts.", f'<p class="stand">{E(p["pricing"])}</p><ul class="outs">{eng}</ul><p class="sidebar"><b>What Lucky Domains is not.</b> {E("; ".join(p["notList"]))}. {E(C["notPromised"])}</p>')
    return phd(p["eyebrow"], p["title"], p["lead"], ctx, [("Home", ctx.to())]) + body + closing(ctx)


def website(ctx):
    w = P["websites"]; a = w["architecture"]
    proc = "".join(f'<li><span>{i:02d}</span><h3>{E(x["name"])}</h3><p>{E(x["line"])}</p></li>' for i, x in enumerate(w["process"], 1))
    before = "".join(f'<li data-k="{E(x)}">{E(x)}</li>' for x in a["before"]["items"])
    after = "".join(f'<li data-k="{E(x)}">{E(x)}</li>' for x in a["after"]["items"])
    body = (chap("approach", "I", "The approach", "Structure before style.", f'<p class="drop">{E(w["intro"][0])}</p><p>{E(w["intro"][1])}</p>{paths_html(w)}')
            + chap("architecture", "II", "Information architecture", a["title"], f'''<div class="ba" data-ba><div class="ba-bar"><button type="button" class="ba-b" aria-pressed="false" data-show="before">Before</button><button type="button" class="ba-b" aria-pressed="true" data-show="after">After</button></div>
<div class="ba-v"><div class="ba-c" data-state="before"><p class="lab-h">{E(a["before"]["label"])}</p><ul>{before}</ul></div><div class="ba-c" data-state="after"><p class="lab-h">{E(a["after"]["label"])}</p><ul>{after}</ul></div></div>
<p class="cap">{E(a["caption"])} Pages are grouped around the services people search for, with proof and the founder one click away.</p></div>''')
            + chap("process", "III", "How a project runs", "Six steps, from discovery to improvement.", f'<ol class="proc">{proc}</ol>')
            + chap("foundations", "IV", "The foundation", "What search engines and AI systems rely on.", f'{fn_list(w["foundations"])}<p class="sidebar">{E(w["not"])}</p><p>{E(w["proof"])} <a class="tl" href="{ctx.to("work/")}">Read the case study</a></p>'))
    toc = [("approach", "The approach"), ("architecture", "Information architecture"), ("process", "How a project runs"), ("foundations", "The foundation")]
    return phd(w["eyebrow"], w["title"], w["lead"], ctx, [("Home", ctx.to()), ("Services", ctx.to("services/"))]) + body + closing(ctx), toc


def search(ctx):
    sp = P["search"]
    areas = "".join(f'<li><b>{E(x["name"])}</b> {E(x["line"])}</li>' for x in sp["seoAreas"])
    steps = "".join(f'<li><span>{i:02d}</span><h3>{E(x["name"])}</h3><p>{E(x["line"])}</p></li>' for i, x in enumerate(sp["aiSteps"], 1))
    aud = "".join(f'<li><b>{E(x["name"])}</b> {E(x["line"])}</li>' for x in C["aiShift"]["audiences"])
    body = (chap("seo", "I", S["seo"]["name"], S["seo"]["lead"], f'<p class="drop">{E(sp["seoIntro"])}</p><ol class="fn fn-2">{areas}</ol>')
            + chap("shift", "II", "The shift", C["aiShift"]["title"], f'<p class="stand">{E(C["aiShift"]["intro"])}</p><ul class="notes-l">{aud}</ul>')
            + chap("ai-visibility", "III", S["ai"]["name"], S["ai"]["short"], f'<p>{E(sp["aiIntro"])}</p><ol class="proc">{steps}</ol><p class="sidebar"><b>What we will not promise.</b> {E(C["notPromised"])} {E(C["noSecret"])}</p>')
            + chap("connect", "IV", "How they connect", "One system, not three services.", f'<p class="pull">{E(sp["connect"])}</p><p><a class="tl" href="{ctx.svc("entity")}">Entity SEO and digital identity</a></p>'))
    toc = [("seo", "SEO and search visibility"), ("shift", "The shift"), ("ai-visibility", "AI visibility"), ("connect", "How they connect")]
    return phd(sp["eyebrow"], sp["title"], sp["lead"], ctx, [("Home", ctx.to()), ("Services", ctx.to("services/"))]) + body + closing(ctx), toc


def domains(ctx):
    dp = P["domains"]; ag = dp["agents"]
    acq = "".join(f'<li><span>{i:02d}</span><h3>{E(x["name"])}</h3><p>{E(x["line"])}</p></li>' for i, x in enumerate(dp["acquisition"], 1))
    topics = "".join(f'<li><b>{E(t["name"])}.</b> {E(t["line"])}</li>' for t in ag["topics"])
    ev = "".join(f'<li><a href="{x["url"]}"><b>{E(x["name"])}</b></a> <span class="st">{E(x["status"])}</span> {E(x["line"])} <em>{E(x["limit"])}</em></li>' for x in C["lab"][:2])
    body = (chap("anchor", "I", "Identity anchors", "A domain is where identity starts.", f'<p class="pull">{E(dp["anchors"])}</p>')
            + chap("domains", "II", S["domains"]["name"], S["domains"]["lead"], f'<p class="stand">{E(S["domains"]["short"])}</p><ol class="proc proc-4">{acq}</ol><h3 class="lab-h" id="selling">Selling a domain</h3><p>{E(dp["selling"])}</p><p class="sidebar"><b>Fee.</b> {E(dp["terms"])} {E(" ".join(x + "." for x in dp["notList"]))}</p><p class="acts"><a class="btn" href="{ctx.home("#contact")}">Tell Ken the domain you want</a></p>')
            + chap("entity", "III", S["entity"]["name"], S["entity"]["lead"], f'<p>{E(S["entity"]["short"])}</p><div class="two"><div><h3>For people</h3>{inc(dp["people"])}</div><div><h3>For businesses</h3>{inc(dp["business"])}</div></div>')
            + chap("agents", "IV", ag["label"], ag["question"], f'<p class="stand">{E(ag["intro"])}</p><ul class="notes-l">{topics}</ul><p class="sidebar caution">{E(ag["caution"])}</p><h3 class="lab-h">Supporting experiments</h3><ul class="lab-l">{ev}</ul>', "ch-research"))
    toc = [("anchor", "Identity anchors"), ("domains", "Domain acquisition"), ("entity", "Entity SEO"), ("agents", "Agent identity")]
    return phd(dp["eyebrow"], dp["title"], dp["lead"], ctx, [("Home", ctx.to()), ("Services", ctx.to("services/"))]) + body + closing(ctx), toc


def work(ctx):
    w = C["work"][0]
    ann = C["annotations"]; marks = {0: "1", 1: "2", 3: "3", 5: "4"}
    done_h = "".join(f'<li>{E(x)}{f" <button class=mk type=button aria-describedby=an-{marks[i]} data-mk={marks[i]}>{marks[i]}</button>" if i in marks else ""}</li>' for i, x in enumerate(w["done"]))
    notes = "".join(f'<li id="an-{a["n"]}" data-note="{a["n"]}"><span>{a["n"]}</span>{E(a["note"])}</li>' for a in ann)
    ev = "".join(f'<li><a class="tl" href="{u}">{E(t)}</a></li>' for t, u in w["evidence"])
    more = ""
    for x in C["work"][1:]:
        demo = x.get("concept")
        more += f'<article class="more{" more-demo" if demo else ""}"><p class="art-k">{E(x["category"])} · {E(x["client"])}{" · " + E(x["status"]) if x["status"] else ""}</p><h3>{E(x["title"])}</h3><p>{E(x["summary"])}</p>{"<p class=tag-c>" + E(x["note"]) + "</p>" if x.get("note") else ""}{"<p class=tag-c>Layout demonstration. Concept content.</p>" if demo else ""}<p>{"".join(f"<a class=tl href={u}>{E(t)}</a> " for t, u in x["evidence"])}</p></article>'
    body = (f'<header class="phd"><nav class="crumbs" aria-label="Breadcrumb"><ol><li><a href="{ctx.to()}">Home</a></li><li><a href="{ctx.to("work/")}">Work</a></li><li aria-current="page">Case study</li></ol></nav><p class="kick">Case study · {E(w["category"])}</p><h1>{E(w["title"])}</h1><p class="stand">{E(w["summary"])}</p>'
            f'<dl class="meta"><div><dt>Client</dt><dd>{E(w["client"])}</dd></div><div><dt>Year</dt><dd>{w["year"]}</dd></div><div><dt>Status</dt><dd>{E(w["status"])}</dd></div><div><dt>Layers</dt><dd>{", ".join(LAYER[l]["name"] for l in w["layers"])}</dd></div></dl></header>'
            + chap("problem", "I", "Problem", "A site the business did not own.", f'<p class="drop">{E(w["problem"])}</p>')
            + chap("approach", "II", "Approach", "Plain files, the company's own domain.", f'<p>{E(w["approach"])}</p><p>{E(w["built"])}</p>')
            + chap("done", "III", "Work completed", "What changed, with the source for each.", f'<div class="case"><div class="case-main"><ul class="done">{done_h}</ul></div><div class="notes" role="group" aria-label="Annotations from the public decision log"><p class="lab-h">From the decision log</p><ol>{notes}</ol></div></div>')
            + chap("evidence", "IV", "Evidence available", "Everything here can be checked.", f'<ul class="ev">{ev}</ul><p class="sidebar">{E(w["noMetrics"])}</p>')
            + chap("status", "V", "Current status", w["status"] + ".", '<p>The site is live and maintained from the public repository. A redesign is being explored in these concepts.</p>')
            + chap("lessons", "VI", "Lessons", "What we would do the same way again.", f'<ol class="fn">{"".join(f"<li>{E(x)}</li>" for x in w["lessons"])}</ol>')
            + f'<section class="mores" aria-labelledby="mw-h"><h2 id="mw-h" class="lab-h">More work</h2><div class="more-g">{more}</div></section>')
    toc = [("problem", "Problem"), ("approach", "Approach"), ("done", "Work completed"), ("evidence", "Evidence available"), ("status", "Current status"), ("lessons", "Lessons")]
    return body + closing(ctx), toc


def build():
    write(f"{DIR}/index.html", shell("", "A digital presence studio", C["company"]["description"], home, cls="home"))
    write(f"{DIR}/services/index.html", shell("services/", "Services", P["services"]["lead"], services, toc=[(s["id"], s["name"]) for s in C["services"]] + [("engagements", "Ways to work together")]))
    for path, title, fn, desc in [("services/website-design/", "Website Design & Development", website, P["websites"]["lead"]),
                                  ("services/search-ai-visibility/", "Search & AI Visibility", search, P["search"]["lead"]),
                                  ("services/domain-identity/", "Domain Strategy & Digital Identity", domains, P["domains"]["lead"]),
                                  ("work/", "Case study: LuckyDomains.io", work, C["work"][0]["summary"])]:
        holder = {}
        def body(ctx, fn=fn, holder=holder):
            html, toc = fn(ctx); holder["toc"] = toc; return html
        probe = Ctx(DIR, path); _, toc = fn(probe)
        write(f"{DIR}/{path}index.html", shell(path, title, desc, body, toc=toc))
