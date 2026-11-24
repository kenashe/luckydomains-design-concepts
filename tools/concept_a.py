"""Concept A: Venture Lab. Dark, quietly technical, evidence-led."""
from lib import C, E, V, Ctx, head, write, status_slug, NOTICE, PAGES, field, is_long

DIR = "concept-a-venture-lab"
NAME = "Venture Lab"
HERO_IDS = ["zerohuman", "ai-agent-economy", "domain-brokerage", "autonomous-seo-agent"]


def st(v):
    s = v["status"]
    extra = f'<span class="st st-kind">{E(v["kind"].upper())}</span>' if v["kind"] == "Experiment" else ""
    return f'{extra}<span class="st st-{status_slug(s)}"><i aria-hidden="true"></i>{E(s)}</span>'


def vhref(ctx, v):
    if v["detail"]:
        return ctx.to(f'ventures/{v["id"]}/')
    if v.get("internal"):
        return ctx.to(f'{v["internal"]}/#domains')
    return ctx.to(f'ventures/#{v["id"]}')


def meta(v, n=99):
    return '<dl class="meta">' + "".join(f"<div><dt>{E(k.upper())}</dt><dd>{E(val)}</dd></div>" for k, val in v["meta"][:n]) + "</dl>"


def artifact(v):
    a = v.get("artifact")
    if not a:
        return ""
    lines = "".join(f'<div class="ln"><span class="tag">{E(t)}</span><code>{E(x)}</code></div>' for t, x in a["lines"])
    return f"""<figure class="art" data-depth>
<div class="art-bar"><span aria-hidden="true"></span><span aria-hidden="true"></span><span aria-hidden="true"></span><b>{E(a['title'])}</b></div>
<div class="art-body">{lines}</div>
<figcaption>{E(a['caption'])}</figcaption></figure>"""


def flow(v, tag="h2"):
    if not v["flow"]:
        return ""
    items = "".join(f'<li><span class="fl-n">{i:02d}</span><h3>{E(t)}</h3><p>{E(x)}</p></li>' for i, (t, x) in enumerate(v["flow"], 1))
    return f'<section class="flow reveal"><p class="eyebrow">PROCESS</p><{tag}>{E(v["flowTitle"])}</{tag}><ol class="fl" style="--n:{len(v["flow"])}">{items}</ol></section>'


def shell(path, title, desc, body, cls=""):
    ctx = Ctx(DIR, path)
    nav = "".join(f'<a href="{ctx.to(p)}"{ctx.cur(p)}>{E(l)}</a>' for p, l in PAGES)
    foot_v = "".join(f'<li><a href="{vhref(ctx, v)}">{E(v["name"])}</a></li>' for v in C["ventures"][:4])
    return f"""{head(ctx, f"{title} | Lucky Domains, Concept A: Venture Lab", desc, "css/style.css", ("bricolage-normal-400-800.woff2", "inter-normal-400-600.woff2"))}
<body class="{cls}">
<a class="skip" href="#main">Skip to content</a>
<aside class="review" aria-label="Review notice"><span>{NOTICE}</span> <a href="{ctx.r}">All concepts</a></aside>
<header class="hd">
  <a class="hd-logo" href="{ctx.to()}" aria-label="Lucky Domains, concept home"><img src="{ctx.asset('logo-wordmark-reversed.png')}" alt="Lucky Domains" width="145" height="36"></a>
  <button class="hd-toggle" type="button" aria-expanded="false" aria-controls="nav"><span>Menu</span></button>
  <nav id="nav" class="hd-nav" aria-label="Primary">{nav}<a class="hd-cta" href="{ctx.to('services/')}#domains">Domain acquisition</a></nav>
</header>
<main id="main">
{body(ctx)}
</main>
<footer class="ft">
  <div class="ft-top">
    <div class="ft-brand">
      <img src="{ctx.asset('logo-wordmark-reversed.png')}" alt="Lucky Domains" width="201" height="50" loading="lazy">
      <p>{E(C['company']['description'])}</p>
    </div>
    <div><h2>Ventures</h2><ul>{foot_v}<li><a href="{ctx.to('ventures/')}">All ventures</a></li></ul></div>
    <div><h2>Company</h2><ul><li><a href="{ctx.to('services/')}">Services</a></li><li><a href="{ctx.to('about/')}">About</a></li><li><a href="{ctx.to('founder/')}">Founder</a></li><li><a href="{ctx.to('news/')}">Updates</a></li><li><a href="{ctx.to('contact/')}">Contact</a></li></ul></div>
    <div><h2>Build record</h2><ul><li><a href="{C['kenashe']['url']}">KenAshe.ai</a></li><li><a href="{C['kenashe']['building']}">All builds</a></li><li><a href="https://github.com/kenashe">GitHub</a></li></ul></div>
  </div>
  <div class="ft-logos" aria-label="Logo treatments in this concept">
    <figure><span class="chip chip-light"><img src="{ctx.asset('logo-wordmark.png')}" alt="Original Lucky Domains logo on a light background" width="129" height="32" loading="lazy"></span><figcaption>ORIGINAL</figcaption></figure>
    <figure><span class="chip"><img src="{ctx.asset('logo-wordmark-reversed.png')}" alt="Reversed Lucky Domains logo on a dark background" width="129" height="32" loading="lazy"></span><figcaption>REVERSED, CONCEPT TREATMENT</figcaption></figure>
    <figure><span class="chip"><img src="{ctx.asset('logo-icon-reversed-128.png')}" alt="Lucky Domains icon" width="32" height="32" loading="lazy"></span><figcaption>ICON</figcaption></figure>
  </div>
  <p class="ft-note">{NOTICE} Concept A: Venture Lab. Facts as of {E(C['asOf'])}. <a href="{ctx.r}">Back to all concepts</a></p>
</footer>
<script src="{ctx.c}js/main.js" defer></script>
</body></html>"""


def vcard(ctx, v, h="h3", flip=False):
    kl = C["kenashe"]["line"]
    links = f'<a class="lk" href="{vhref(ctx, v)}">{"Open the venture file" if v["detail"] else "See the service" if v.get("internal") else "Details"}</a>' if (v["detail"] or v.get("internal")) else ""
    if v["buildRecord"]:
        links += f'<a class="lk ext" href="{v["buildRecord"]}">{kl if v["detail"] else "Build record on KenAshe.ai"}</a>'
    links += "".join(f'<a class="lk ext" href="{u}">{E(l)}</a>' for l, u in v["links"])
    img = v.get("image")
    side = artifact(v) if v.get("artifact") else f'<figure class="art" data-depth><div class="art-bar"><span aria-hidden="true"></span><span aria-hidden="true"></span><span aria-hidden="true"></span><b>luckydomains.io</b></div><img src="{ctx.asset(img["file"])}" alt="{E(img["alt"])}" width="1280" height="800" loading="lazy"><figcaption>{E(img["caption"])}</figcaption></figure>' if img else (
        '<ol class="mini-flow">' + "".join(f'<li><span>{i:02d}</span>{E(t)}</li>' for i, (t, _) in enumerate(v["flow"], 1)) + "</ol>" if v["flow"] else "")
    return f"""<article class="vc reveal{' vc-flip' if flip else ''}{'' if side else ' vc-slim'}" id="{v['id']}" data-spot data-status="{status_slug(v['status'])}">
  <div class="vc-main">
    <p class="vc-top">{st(v)}<span class="vc-since">{E(v['since'].upper())}</span></p>
    <{h}><a href="{vhref(ctx, v)}">{E(v['name'])}</a></{h}>
    <p class="vc-tag">{E(v['tagline'])}</p>
    <p class="vc-sum">{E(v['summary'])}</p>
    {meta(v, 6)}
    <p class="vc-links">{links}</p>
  </div>
  {f'<div class="vc-side">{side}</div>' if side else ''}
</article>"""


# ---------------------------------------------------------------- pages
def home(ctx):
    rows = ""
    for i, vid in enumerate(HERO_IDS, 1):
        v = V[vid]
        d = "".join(f"<div><dt>{E(k.upper())}</dt><dd>{E(val)}</dd></div>" for k, val in v["meta"][1:4])
        rows += f"""<li class="ops-row{' is-on' if i == 1 else ''}">
  <a href="{vhref(ctx, v)}"><span class="ops-i">{i:02d}</span><span class="ops-n">{E(v['name'])}</span>{st(v)}</a>
  <div class="ops-d"><div><p>{E(v['tagline'])}</p><dl>{d}</dl></div></div></li>"""
    steps = [
        ("domains", "Domains", "It started with names.", "Getting a business the exact domain it wants, including one somebody else owns, is still an active Lucky Domains service: valuation, anonymous outreach, negotiation, escrow.", ("Domain acquisition and brokerage", ctx.to("services/") + "#domains"), "ACTIVE SERVICE"),
        ("identity", "Identity", "A name becomes an identity when the records agree.", "Structured data, consistent profiles, and ENS records turn a name into something machines can verify. zerohuman.eth is the storefront, the payment address, and the sender for a live service.", ("Digital identity and presence", ctx.to("services/") + "#identity"), "IDENTITY: zerohuman.eth"),
        ("agents", "Agents", "Then software started holding the name.", "Two agents with their own wallets completed a purchase on Ethereum mainnet. Another agent researches and registers web profiles every day without review.", ("The agent economy experiment", ctx.to("ventures/ai-agent-economy/")), "NETWORK: ETHEREUM MAINNET"),
        ("ventures", "Ventures", "Now the systems are operated, not just demonstrated.", "ZeroHuman runs continuously and is open to any agent. Each venture is summarized here, and the full build record stays on KenAshe.ai.", ("All ventures", ctx.to("ventures/")), "STATUS: LIVE"),
    ]
    marks = "".join(f'<li><a href="#p-{i}" data-mark="{i}"><span>{n:02d}</span>{E(l)}</a></li>' for n, (i, l, *_r) in enumerate(steps, 1))
    arts = "".join(f"""<article class="step" id="p-{i}" data-step="{i}"><p class="step-n">{n:02d} / 04</p><h3>{E(h)}</h3><p>{E(t)}</p><p class="step-ev">{E(ev)}</p><a class="lk" href="{lk[1]}">{E(lk[0])}</a></article>""" for n, (i, l, h, t, lk, ev) in enumerate(steps, 1))
    cards = vcard(ctx, V["zerohuman"]) + vcard(ctx, V["ai-agent-economy"], flip=True) + vcard(ctx, V["autonomous-seo-agent"])
    b = V["domain-brokerage"]
    bflow = "".join(f'<li><span>{i:02d}</span><h3>{E(t)}</h3><p>{E(x)}</p></li>' for i, (t, x) in enumerate(b["flow"], 1))
    f = C["founder"]
    return f"""
<section class="hero">
  <canvas class="grid" aria-hidden="true"></canvas>
  <div class="hero-in">
    <div class="hero-copy">
      <p class="eyebrow">AI APPLICATIONS · DIGITAL IDENTITY · INTERNET-NATIVE VENTURES</p>
      <h1>Domains were the beginning. <span class="dim">Not the boundary.</span></h1>
      <p class="lede">{E(C['company']['heroSupport'])}</p>
      <p class="cta"><a class="btn btn-p" href="{ctx.to('ventures/')}">Explore what we’re building</a><a class="btn" href="{ctx.to('services/')}#domains">Domain acquisition</a></p>
    </div>
    <section class="ops" aria-label="Operating status">
      <div class="ops-hd"><span><i class="pulse" aria-hidden="true"></i>OPERATING STATUS</span><button type="button" class="ops-pause" aria-pressed="false">Pause</button></div>
      <ol class="ops-list">{rows}</ol>
      <p class="ops-ft">Statuses mirror the public build record on KenAshe.ai, {E(C['asOf'])}.</p>
    </section>
  </div>
</section>

<section class="path" aria-labelledby="path-h">
  <div class="path-rail">
    <p class="eyebrow">THE PROGRESSION</p>
    <h2 id="path-h">From a name to something that acts on its own.</h2>
    <ol class="path-marks">{marks}</ol>
    <svg class="path-fig" viewBox="0 0 320 60" role="img" aria-label="Four stages in sequence: domains, identity, agents, ventures">
      <line x1="10" y1="30" x2="310" y2="30" class="pf-base"/><line x1="10" y1="30" x2="310" y2="30" class="pf-fill" pathLength="1"/>
      <circle cx="10" cy="30" r="5"/><circle cx="110" cy="30" r="5"/><circle cx="210" cy="30" r="5"/><circle cx="310" cy="30" r="5"/>
    </svg>
  </div>
  <div class="path-steps">{arts}</div>
</section>

<section class="sec" aria-labelledby="v-h">
  <div class="sec-hd reveal"><p class="eyebrow">VENTURES / 03 OF {len(C['ventures']):02d}</p><h2 id="v-h">Built, run, and written down.</h2><p>Each file below is a summary. The complete record, including what broke, is on KenAshe.ai.</p></div>
  <div class="vcs">{cards}</div>
  <p class="sec-more"><a class="btn" href="{ctx.to('ventures/')}">View all ventures</a></p>
</section>

<section class="band" aria-labelledby="b-h">
  <div class="band-in reveal">
    <p class="eyebrow"><span class="st st-active-service"><i aria-hidden="true"></i>ACTIVE SERVICE</span> THE ORIGINAL PRACTICE</p>
    <h2 id="b-h">The domain desk is still open.</h2>
    <p class="band-lede">{E(C['services'][0]['body'])}</p>
    <ol class="band-flow">{bflow}</ol>
    <p class="band-terms">{E(C['services'][0]['terms'])}</p>
    <p class="cta"><a class="btn btn-p" href="{ctx.to('contact/')}?path=domains">Start a domain inquiry</a><a class="btn" href="{ctx.to('services/')}#domains">How brokerage works</a></p>
  </div>
</section>

<section class="sec fstrip" aria-labelledby="f-h">
  <div class="fstrip-in reveal">
    <img src="{ctx.asset(f['image'])}" alt="Ken Ashe, founder of Lucky Domains" width="320" height="320" loading="lazy">
    <div>
      <p class="eyebrow">FOUNDER-LED</p>
      <h2 id="f-h">Ken Ashe builds in public. Lucky Domains operates what gets built.</h2>
      <p>{E(f['lead'])}</p>
      <p class="cta"><a class="btn" href="{ctx.to('founder/')}">About the founder</a><a class="btn ext" href="{C['kenashe']['url']}">Build logs on KenAshe.ai</a></p>
    </div>
  </div>
</section>"""


def page_hd(eyebrow, h1, lede=""):
    return f'<section class="phd"><canvas class="grid grid-sm" aria-hidden="true"></canvas><div class="phd-in"><p class="eyebrow">{eyebrow}</p><h1>{h1}</h1>{f"<p class=lede>{lede}</p>" if lede else ""}</div></section>'


def ventures(ctx):
    vs = C["ventures"]
    filt = [("all", "All"), ("live", "Live"), ("shipped", "Shipped"), ("active-service", "Active service")]
    btns = "".join(f'<button type="button" data-filter="{k}" aria-pressed="{"true" if k == "all" else "false"}">{l}</button>' for k, l in filt)
    cards = "".join(vcard(ctx, v, "h2", flip=i % 2 == 1) for i, v in enumerate(vs))
    return f"""{page_hd("VENTURES", "What Lucky Domains is building and running.", "Six files: live systems, shipped experiments, studio builds, and the original service. Every status mirrors the label on the public build record.")}
<section class="sec">
  <div class="filter" role="group" aria-label="Filter ventures by status">{btns}<span class="filter-n" aria-live="polite"></span></div>
  <div class="vcs">{cards}</div>
  <p class="src-note">Statuses and figures are taken from KenAshe.ai and LuckyDomains.io as read on {E(C['asOf'])}. Presenting these builds under Lucky Domains is the positioning this concept proposes.</p>
</section>"""


def venture_detail(v):
    def body(ctx):
        paras = "".join(f"<p>{E(p)}</p>" for p in v["body"])
        facts = "".join(f"<li>{E(x)}</li>" for x in v["facts"])
        limits = "".join(f"<li>{E(x)}</li>" for x in v["limits"])
        links = "".join(f'<a class="lk ext" href="{u}">{E(l)}</a>' for l, u in v["links"])
        rel = "".join(f'<a class="rel" href="{vhref(ctx, V[r])}"><span>RELATED FILE</span>{E(V[r]["name"])}</a>' for r in v["related"])
        nxt = f'<p class="next"><span>NEXT</span>{E(v["next"])}</p>' if v["next"] else ""
        return f"""<section class="phd phd-v"><canvas class="grid grid-sm" aria-hidden="true"></canvas><div class="phd-in">
  <p class="eyebrow"><a href="{ctx.to('ventures/')}">VENTURES</a> / {E(v['name'].upper())}</p>
  <h1>{E(v['name'])}</h1><p class="lede">{E(v['tagline'])}</p><p class="vc-top">{st(v)}<span class="vc-since">{E(v['since'].upper())}</span></p></div></section>
<div class="vd">
  <section class="vd-side" aria-label="Venture metadata">{meta(v)}
    <a class="btn btn-p ext" href="{v['buildRecord']}">{C['kenashe']['line']}</a>
    <p class="vd-links">{links}</p>
  </section>
  <div class="vd-main">
    <section class="reveal"><p class="eyebrow">SUMMARY</p><p class="big">{E(v['summary'])}</p>{paras}</section>
    {flow(v)}
    <section class="reveal"><p class="eyebrow">EVIDENCE</p><h2>What the record shows</h2>{artifact(v)}<ul class="facts">{facts}</ul></section>
    <section class="limits reveal"><p class="eyebrow">LIMITS</p><h2>What this does not prove</h2><ul>{limits}</ul>{nxt}</section>
    <section class="xl reveal"><p>This page is a summary. The full write-up, with transactions and failures, lives on the founder's public build record.</p><a class="btn btn-p ext" href="{v['buildRecord']}">{C['kenashe']['line']}</a>{rel}</section>
  </div>
</div>"""
    return body


def services(ctx):
    out = ""
    for i, s in enumerate(C["services"]):
        inc = "".join(f"<li>{E(x)}</li>" for x in s["includes"])
        nots = ('<div class="sv-not"><h3>What this is not</h3><ul>' + "".join(f"<li>{E(x)}</li>" for x in s["not"]) + "</ul></div>") if s["not"] else ""
        extra = ""
        if i == 0:
            b = V["domain-brokerage"]
            extra = '<ol class="band-flow">' + "".join(f'<li><span>{n:02d}</span><h3>{E(t)}</h3><p>{E(x)}</p></li>' for n, (t, x) in enumerate(b["flow"], 1)) + "</ol>"
        cta = f'<a class="btn btn-p" href="{ctx.to("contact/")}?path=domains">Start a domain inquiry</a>' if i == 0 else f'<a class="btn" href="{ctx.to("contact/")}?path=general">Ask about fit</a>'
        out += f"""<section class="sv sv-{i + 1} reveal" id="{s['id']}" data-spot>
  <div class="sv-hd"><p class="sv-n">{s['n']}</p><p class="vc-top"><span class="st st-{'active-service' if i == 0 else 'shipped'}"><i aria-hidden="true"></i>{E(s['status'])}</span></p></div>
  <div class="sv-main"><h2>{E(s['name'])}</h2><p class="big">{E(s['lead'])}</p><p>{E(s['body'])}</p>{extra}<p class="sv-terms">{E(s['terms'])}</p><p class="cta">{cta}</p></div>
  <div class="sv-side"><h3>In scope</h3><ul class="facts">{inc}</ul>{nots}</div>
</section>"""
    return f"""{page_hd("SERVICES", "The commercial side, kept deliberately narrow.", "Domain acquisition and brokerage is the standing service. Identity and site work are taken on selectively, when they support a launch, an identity, or a venture.")}
<div class="svs">{out}</div>"""


def about(ctx):
    st_html = "".join(f"""<article class="stage reveal"><p class="stage-n">{s['n']}</p><div><h2>{E(s['title'])}</h2><p class="big">{E(s['line'])}</p><p>{E(s['body'])}</p></div></article>""" for s in C["story"])
    tl = "".join(f'<li class="reveal"><time>{E(t["date"].upper())}</time><h3>{E(t["label"])}</h3><p>{E(t["text"])}</p></li>' for t in C["timeline"])
    model = "".join(f"<li><b>{E(a)}</b> {E(b)}</li>" for a, b in C["company"]["model"])
    return f"""{page_hd("ABOUT", "A company that started with literal domains.", E(C['company']['aboutLong']))}
<section class="sec stages">{st_html}</section>
<section class="sec" aria-labelledby="tl-h"><div class="sec-hd reveal"><p class="eyebrow">RECORD</p><h2 id="tl-h">Dated, public, checkable.</h2><p>Only events with a public source are listed. Founding year is not published and is not shown.</p></div><ol class="tl">{tl}</ol></section>
<section class="sec" aria-labelledby="m-h"><div class="sec-hd reveal"><p class="eyebrow">STRUCTURE</p><h2 id="m-h">Who does what.</h2></div><ul class="model reveal">{model}</ul>
<p class="cta"><a class="btn btn-p" href="{ctx.to('ventures/')}">See the ventures</a><a class="btn ext" href="{C['kenashe']['url']}">Visit KenAshe.ai</a></p></section>"""


def founder(ctx):
    f = C["founder"]
    bio = "".join(f"<p>{E(p)}</p>" for p in f["bio"])
    cred = "".join(f"<div><dt>{E(a)}</dt><dd>{E(b)}</dd></div>" for a, b in f["credentials"])
    sp = "".join(f"<div><dt>{E(y)} · {E(ev.upper())}</dt><dd>{E(t)}</dd></div>" for y, ev, t in f["speaking"])
    roles = "".join(f"<li>{E(r)}</li>" for r in f["roles"])
    links = "".join(f'<a class="lk ext" href="{u}">{E(l)}</a>' for l, u in f["links"])
    return f"""<section class="phd fhd"><canvas class="grid grid-sm" aria-hidden="true"></canvas><div class="phd-in fhd-in">
  <div><p class="eyebrow">FOUNDER</p><h1>{E(f['name'])}</h1><p class="lede">{E(f['lead'])}</p><ul class="roles">{roles}</ul>
  <p class="cta"><a class="btn btn-p ext" href="{C['kenashe']['url']}">Visit KenAshe.ai</a><a class="btn" href="{ctx.to('contact/')}?path=media">Media or speaking</a></p></div>
  <img src="{ctx.asset(f['image'])}" alt="Portrait of Ken Ashe" width="420" height="420">
</div></section>
<div class="vd">
  <section class="vd-side" aria-label="Credentials"><p class="eyebrow">OPERATING EVIDENCE</p><dl class="meta meta-stack">{cred}</dl><p class="small">{E(f['membership'])}</p><p class="small">Career: {E(", ".join(f['career']))}.</p></section>
  <div class="vd-main">
    <section class="reveal"><p class="eyebrow">BACKGROUND</p>{bio}<blockquote><p>{E(f['quote'])}</p><cite>{E(f['quoteSource'])}</cite></blockquote></section>
    <section class="reveal"><p class="eyebrow">SPEAKING AND JUDGING</p><dl class="meta meta-stack">{sp}</dl></section>
    <section class="xl reveal"><p class="eyebrow">TWO SITES, TWO JOBS</p><h2>KenAshe.ai is the build record. This site is the company.</h2><p>Experiments, build logs, and videos are published under Ken's own name. Lucky Domains summarizes the ventures and runs the services.</p><a class="btn btn-p ext" href="{C['kenashe']['building']}">Read the build logs on KenAshe.ai</a><p class="vd-links">{links}</p></section>
  </div>
</div>"""


def news(ctx):
    items = ""
    for n in C["news"]:
        link = f'<a class="lk ext" href="{n["url"]}">Read at the source: {E(n["source"])}</a>' if n["url"] else '<span class="small">No link. This item does not exist outside this concept.</span>'
        items += f"""<article class="nw reveal{' nw-sample' if n['concept'] else ''}"><div class="nw-meta"><time>{E(n['date'].upper())}</time><span class="nw-type">{E(n['type'])}</span></div><div><h2>{E(n['title'])}</h2><p>{E(n['text'])}</p>{link}</div></article>"""
    return f"""{page_hd("UPDATES", "Company news and project updates.", "Published company news is preserved as written. Project updates are dated summaries of public build records. Sample copy is marked.")}
<section class="sec nws">{items}</section>"""


def contact(ctx):
    paths = C["contact"]["paths"]
    tabs = "".join(f'<button type="button" role="tab" id="t-{p["id"]}" aria-controls="pn-{p["id"]}" aria-selected="{"true" if i == 0 else "false"}" tabindex="{0 if i == 0 else -1}"><span>{i + 1:02d}</span>{E(p["label"])}</button>' for i, p in enumerate(paths))
    panels = ""
    for i, p in enumerate(paths):
        flds = "".join(field(x, is_long(x)) for x in p["fields"])
        panels += f"""<div role="tabpanel" id="pn-{p['id']}" aria-labelledby="t-{p['id']}" {'hidden' if i else ''}>
  <p class="big">{E(p['blurb'])}</p>
  <form class="cf" novalidate>{field("Name")}{field("Email", type_="email")}{flds}
  <button class="btn btn-p" type="button">Send inquiry</button><p class="cf-note" role="status">{E(C['contact']['notice'])}</p></form></div>"""
    return f"""{page_hd("CONTACT", "Four ways in.", "Pick the path that fits. In production, each would route to the right inbox.")}
<section class="sec ct">
  <div class="ct-tabs" role="tablist" aria-label="Inquiry type">{tabs}</div>
  <div class="ct-panels">{panels}</div>
  <div class="ct-side"><p class="eyebrow">DIRECT</p><p><a class="lk" href="mailto:{C['company']['email']}">{C['company']['email']}</a></p><p class="small">This is the company's published address. The form on this page is a design mockup and sends nothing.</p></div>
</section>"""


def build():
    write(f"{DIR}/index.html", shell("", "Home", C["company"]["description"], home, "home"))
    write(f"{DIR}/ventures/index.html", shell("ventures/", "Ventures", "Ventures built and operated by Lucky Domains.", ventures))
    for v in C["ventures"]:
        if v["detail"]:
            write(f"{DIR}/ventures/{v['id']}/index.html", shell(f"ventures/{v['id']}/", v["name"], v["summary"], venture_detail(v)))
    write(f"{DIR}/services/index.html", shell("services/", "Services", "Domain acquisition and brokerage, digital identity, and selected engagements.", services))
    write(f"{DIR}/about/index.html", shell("about/", "About", C["company"]["aboutLong"], about))
    write(f"{DIR}/founder/index.html", shell("founder/", "Founder", C["founder"]["lead"], founder))
    write(f"{DIR}/news/index.html", shell("news/", "Updates", "Company news and project updates.", news))
    write(f"{DIR}/contact/index.html", shell("contact/", "Contact", "Contact Lucky Domains.", contact))
