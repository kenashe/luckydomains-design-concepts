"""Concept B: The Register. Light, editorial, a founder-owned company's journal of record."""
from lib import C, E, V, Ctx, head, write, status_slug, NOTICE, field, is_long

DIR = "concept-b-the-register"
NAME = "The Register"
ROMAN = ["i", "ii", "iii", "iv", "v", "vi", "vii"]
NAV = [("ventures/", "Ventures"), ("services/", "Services"), ("about/", "About"), ("founder/", "Founder"), ("news/", "News"), ("contact/", "Contact")]


def st(v):
    return f'<span class="st st-{status_slug(v["status"])}">{E(v["status"].title())}</span>'


def vhref(ctx, v):
    if v["detail"]:
        return ctx.to(f'ventures/{v["id"]}/')
    if v.get("internal"):
        return ctx.to(f'{v["internal"]}/#domains')
    return ctx.to(f'ventures/#{v["id"]}')


def figure(v, n=1):
    a = v.get("artifact")
    if not a:
        return ""
    rows = "".join(f'<div class="fg-row"><span>{E(t)}</span><code>{E(x)}</code></div>' for t, x in a["lines"])
    return f"""<figure class="fg rv"><div class="fg-plate">{rows}</div><figcaption><b>Fig. {n}.</b> {E(a['title'])}. {E(a['caption'])}</figcaption></figure>"""


def plate(v):
    """Small preview shown beside a register row (pointer or focus)."""
    m = "".join(f"<div><dt>{E(k)}</dt><dd>{E(val)}</dd></div>" for k, val in v["meta"][:4])
    return f'<div class="plate" aria-hidden="true"><p class="plate-k">{E(v["kind"])}</p><p class="plate-t">{E(v["tagline"])}</p><dl>{m}</dl></div>'


def shell(path, title, desc, body, tone="paper"):
    ctx = Ctx(DIR, path)
    nav = "".join(f'<a href="{ctx.to(p)}"{ctx.cur(p)}>{E(l)}</a>' for p, l in NAV)
    toc = "".join(f'<li><a href="{ctx.to(p)}"{ctx.cur(p)}><span>{i:02d}</span>{E(l)}</a></li>' for i, (p, l) in enumerate([("", "Front page")] + NAV, 0))
    return f"""{head(ctx, f"{title} | Lucky Domains, Concept B: The Register", desc, "css/style.css", ("fraunces-normal-300-800.woff2", "instrument-normal-400-600.woff2"))}
<body data-tone="{tone}">
<a class="skip" href="#main">Skip to content</a>
<aside class="review" aria-label="Review notice">{NOTICE} <a href="{ctx.r}">All concepts</a></aside>
<header class="mast">
  <div class="mast-top"><span>A founder-led venture studio</span><span>Concept edition, {E(C['asOf'])}</span></div>
  <a class="mast-logo" href="{ctx.to()}" aria-label="Lucky Domains, concept home"><img src="{ctx.asset('logo-wordmark.png')}" alt="Lucky Domains" width="242" height="60"></a>
  <nav class="mast-nav" aria-label="Sections">{nav}</nav>
</header>
<div class="run" data-run>
  <a class="run-logo" href="{ctx.to()}" aria-label="Lucky Domains, concept home"><img src="{ctx.asset('logo-icon-128.png')}" alt="" width="30" height="30"></a>
  <p class="run-head" aria-hidden="true"><span data-run-title>{E(title)}</span></p>
  <button class="run-btn" type="button" aria-expanded="false" aria-controls="toc">Contents</button>
  <i class="run-bar" aria-hidden="true"></i>
  <nav id="toc" class="toc" aria-label="Contents" hidden><p class="toc-h">Contents</p><ol>{toc}</ol><p class="toc-x"><a href="{C['kenashe']['url']}">The build record, on KenAshe.ai</a></p></nav>
</div>

<main id="main">
{body(ctx)}
</main>
<footer class="colo" data-tone-zone="paper">
  <div class="colo-top">
    <div><img src="{ctx.asset('logo-wordmark.png')}" alt="Lucky Domains" width="194" height="48" loading="lazy"><p>{E(C['company']['description'])}</p></div>
    <div><h2>The company</h2><ul>{"".join(f'<li><a href="{ctx.to(p)}">{E(l)}</a></li>' for p, l in NAV)}</ul></div>
    <div><h2>The record</h2><ul><li><a href="{C['kenashe']['url']}">KenAshe.ai</a></li><li><a href="{C['kenashe']['building']}">Build logs</a></li><li><a href="https://github.com/kenashe">GitHub</a></li></ul><h2>Write</h2><ul><li><a href="mailto:{C['company']['email']}">{C['company']['email']}</a></li></ul></div>
    <div><h2>The mark</h2><div class="marks"><img src="{ctx.asset('logo-icon-128.png')}" alt="Lucky Domains icon, original colors" width="44" height="44" loading="lazy"><img src="{ctx.asset('logo-icon-mono-ink.png')}" alt="Lucky Domains icon, single ink, optional concept treatment" width="44" height="44" loading="lazy"></div><p class="colo-s">Original logo throughout. The single-ink icon is an optional concept treatment.</p></div>
  </div>
  <p class="colo-note">{NOTICE} Concept B: The Register. Set in Fraunces and Instrument Sans. Facts as of {E(C['asOf'])}. <a href="{ctx.r}">Back to all concepts</a></p>
</footer>
<script src="{ctx.c}js/main.js" defer></script>
</body></html>"""


def register_rows(ctx, vs, h="h3"):
    out = ""
    for i, v in enumerate(vs, 1):
        out += f"""<li class="rg-row" id="r-{v['id']}"><a href="{vhref(ctx, v)}"><span class="rg-n">No. {i:02d}</span><span class="rg-name"><{h}>{E(v['name'])}</{h}><em>{E(v['tagline'])}</em></span><span class="rg-kind">{E(v['kind'])}</span>{st(v)}<span class="rg-since">{E(v['since'])}</span></a>{plate(v)}</li>"""
    return f'<ol class="rg">{out}</ol>'


def home(ctx):
    z, a, s, b = V["zerohuman"], V["ai-agent-economy"], V["autonomous-seo-agent"], V["domain-brokerage"]
    tl = "".join(f'<li><time>{E(t["date"])}</time><h3>{E(t["label"])}</h3><p>{E(t["text"])}</p></li>' for t in C["timeline"])
    bflow = "".join(f'<li><span>{ROMAN[i]}.</span><h3>{E(t)}</h3><p>{E(x)}</p></li>' for i, (t, x) in enumerate(b["flow"]))
    f = C["founder"]
    return f"""
<section class="cover" data-tone-zone="paper" data-run-label="Front page">
  <p class="kick">The company, as it stands in {E(C['asOf'].split(' ')[0])} {E(C['asOf'].split(' ')[-1])}</p>
  <h1 class="kin">First the name. <span>Then <em>everything</em> built on it.</span></h1>
  <div class="cover-cols">
    <div class="cover-lede">
      <p class="drop">{E(C['company']['description'])}</p>
      <p>{E(C['company']['aboutLong'])}</p>
      <p class="acts"><a class="btn" href="{ctx.to('ventures/')}">Read the register of ventures</a><a class="tl" href="{ctx.to('services/')}#domains">Domain acquisition and brokerage</a></p>
    </div>
    <div class="cover-reg">
      <h2 class="lab">In this register</h2>
      {register_rows(ctx, C['ventures'])}
      <p class="fine">Statuses are the labels shown on the public build record, read {E(C['asOf'])}.</p>
    </div>
  </div>
</section>

<section class="hist" data-tone-zone="wash" data-run-label="A short history" aria-labelledby="hist-h">
  <div class="hist-hd"><p class="kick">A short history, with dates</p><h2 id="hist-h">From domains, to identity, to software that <em>acts.</em></h2></div>
  <div class="hist-track" data-track><i class="hist-line" aria-hidden="true"></i><ol class="hist-list">{tl}</ol></div>
  <p class="fine">Only events with a public source are shown. <a href="{ctx.to('about/')}">The longer account</a></p>
</section>

<article class="feat" data-tone-zone="paper" data-run-label="Feature: ZeroHuman" aria-labelledby="feat-h">
  <header class="feat-hd"><p class="kick">Feature · Venture No. 01 · {st(z)}</p><h2 id="feat-h" class="kin"><a href="{vhref(ctx, z)}">A business only AI agents <em>can use.</em></a></h2><p class="stand">{E(z['summary'])}</p></header>
  <div class="feat-cols">
    <div class="feat-body"><p>{E(z['body'][1])}</p><p>{E(z['body'][2])}</p>
      <blockquote class="pull"><p>{E(z['limits'][0])}</p><cite>From the limits section of the build log</cite></blockquote>
      <p class="acts"><a class="btn" href="{vhref(ctx, z)}">Read the feature</a><a class="tl ext" href="{z['buildRecord']}">{C['kenashe']['line']}</a></p>
    </div>
    {figure(z, 1)}
  </div>
</article>

<section class="pair" data-tone-zone="paper" data-run-label="More from the register">
  <article class="rv"><p class="kick">Venture No. 02 · {st(a)} · Experiment</p><p class="stat">One purchase, <em>one toaster.</em></p><h2><a href="{vhref(ctx, a)}">{E(a['name'])}</a></h2><p>{E(a['summary'])}</p><a class="tl" href="{vhref(ctx, a)}">Read the entry</a></article>
  <article class="rv"><p class="kick">Venture No. 03 · {st(s)}</p><p class="stat">8 profiles live, <em>of 63 sites researched.</em></p><h2><a href="{vhref(ctx, s)}">{E(s['name'])}</a></h2><p>{E(s['summary'])}</p><a class="tl" href="{vhref(ctx, s)}">Read the entry</a></article>
</section>

<section class="notice" data-tone-zone="wash" data-run-label="The original practice" aria-labelledby="nt-h">
  <div class="notice-in">
    <p class="kick">Standing notice · {st(b)}</p>
    <h2 id="nt-h" class="kin">The original practice <em>continues.</em></h2>
    <p class="stand">{E(C['services'][0]['body'])}</p>
    <ol class="steps">{bflow}</ol>
    <p class="terms">{E(C['services'][0]['terms'])}</p>
    <p class="acts"><a class="btn" href="{ctx.to('contact/')}?path=domains">Inquire about a domain</a><a class="tl" href="{ctx.to('services/')}#domains">Terms and scope</a></p>
  </div>
</section>

<section class="fnd" data-tone-zone="paper" data-run-label="The founder" aria-labelledby="fnd-h">
  <figure class="port rv"><img src="{ctx.asset(f['image'])}" alt="Ken Ashe, founder of Lucky Domains" width="420" height="420" loading="lazy"><figcaption>Ken Ashe, founder. CPA, PMP.</figcaption></figure>
  <div><p class="kick">The founder</p><h2 id="fnd-h">KenAshe.ai keeps the record. <em>Lucky Domains keeps the company.</em></h2><p>{E(f['lead'])}</p><p>Experiments, build logs, and videos are published under his own name. The ventures those experiments become are held and operated here.</p>
  <p class="acts"><a class="btn" href="{ctx.to('founder/')}">About Ken Ashe</a><a class="tl ext" href="{C['kenashe']['url']}">Visit KenAshe.ai</a></p></div>
</section>"""


def phd(kick, h1, stand=""):
    return f'<header class="phd" data-run-label="{E(kick)}"><p class="kick">{kick}</p><h1 class="kin">{h1}</h1>{f"<p class=stand>{stand}</p>" if stand else ""}</header>'


def ventures(ctx):
    rows = ""
    for i, v in enumerate(C["ventures"], 1):
        links = ""
        if v["detail"]:
            links += f'<a class="btn" href="{vhref(ctx, v)}">Read the full entry</a>'
        if v.get("internal"):
            links += f'<a class="btn" href="{vhref(ctx, v)}">Terms and scope</a>'
        if v["buildRecord"]:
            links += f'<a class="tl ext" href="{v["buildRecord"]}">{C["kenashe"]["line"] if v["detail"] else "Build record on KenAshe.ai"}</a>'
        links += "".join(f'<a class="tl ext" href="{u}">{E(l)}</a>' for l, u in v["links"])
        m = "".join(f"<div><dt>{E(k)}</dt><dd>{E(val)}</dd></div>" for k, val in v["meta"])
        steps = ('<ol class="steps steps-s">' + "".join(f'<li><span>{ROMAN[k]}.</span><h3>{E(t)}</h3></li>' for k, (t, _) in enumerate(v["flow"])) + "</ol>") if (v["flow"] and not v.get("artifact")) else ""
        img = v.get("image")
        pic = f'<figure class="fg fg-img rv"><img src="{ctx.asset(img["file"])}" alt="{E(img["alt"])}" width="1280" height="800" loading="lazy"><figcaption><b>Fig. {i}.</b> {E(img["caption"])}</figcaption></figure>' if img else ""
        rows += f"""<details class="en" id="{v['id']}"{' open' if i == 1 else ''}>
  <summary><span class="rg-n">No. {i:02d}</span><span class="rg-name"><h2>{E(v['name'])}</h2><em>{E(v['tagline'])}</em></span><span class="rg-kind">{E(v['kind'])}</span>{st(v)}<span class="rg-since">{E(v['since'])}</span><i class="en-x" aria-hidden="true"></i></summary>
  <div class="en-body"><div><p class="stand">{E(v['summary'])}</p><p class="acts">{links}</p></div><div><dl class="glance">{m}</dl></div>{figure(v, i)}{pic}{steps}</div>
</details>"""
    return f"""{phd("The register of ventures", "Six entries, <em>each with a source.</em>", "What Lucky Domains builds, runs, and has shipped. Every status is the label shown on the public build record. Open an entry for the summary, or follow it to the complete log.")}
<section class="ens" data-tone-zone="paper"><div class="ens-hd" aria-hidden="true"><span>No.</span><span>Venture</span><span>Kind</span><span>Status</span><span>Since</span><span></span></div>{rows}
<p class="fine">Figures and statuses come from KenAshe.ai and LuckyDomains.io, read {E(C['asOf'])}. Listing these builds under Lucky Domains is the positioning this concept proposes.</p></section>"""


def venture_detail(v):
    idx = [x["id"] for x in C["ventures"]].index(v["id"]) + 1

    def body(ctx):
        m = "".join(f"<div><dt>{E(k)}</dt><dd>{E(val)}</dd></div>" for k, val in v["meta"])
        paras = f'<p class="drop">{E(v["body"][0])}</p>' + "".join(f"<p>{E(p)}</p>" for p in v["body"][1:])
        steps = "".join(f'<li><span>{ROMAN[k]}.</span><h3>{E(t)}</h3><p>{E(x)}</p></li>' for k, (t, x) in enumerate(v["flow"]))
        facts = "".join(f"<li>{E(x)}</li>" for x in v["facts"])
        limits = "".join(f"<li>{E(x)}</li>" for x in v["limits"])
        links = "".join(f'<li><a class="tl ext" href="{u}">{E(l)}</a></li>' for l, u in v["links"])
        rel = "".join(f'<a class="next-en" href="{vhref(ctx, V[r])}"><span>Related entry</span>{E(V[r]["name"])}</a>' for r in v["related"])
        nxt = f'<blockquote class="pull"><p>{E(v["next"])}</p></blockquote>' if v["next"] else ""
        return f"""<article class="art" data-tone-zone="paper">
<header class="phd" data-run-label="{E(v['name'])}"><p class="kick"><a href="{ctx.to('ventures/')}">The register</a> · Venture No. {idx:02d} · {E(v['kind'])} · {st(v)}</p><h1 class="kin">{E(v['name'])}: <em>{E(v['tagline'][0].lower() + v['tagline'][1:])}</em></h1><p class="stand">{E(v['summary'])}</p></header>
<div class="art-grid">
  <section class="margin" aria-label="At a glance"><h2 class="lab">At a glance</h2><dl class="glance">{m}</dl><ul class="margin-l">{links}</ul><a class="btn" href="{v['buildRecord']}">The complete build log<span class="sr"> on KenAshe.ai</span></a></section>
  <div class="prose">
    {paras}
    <h2>{E(v['flowTitle'])}</h2><ol class="steps steps-v">{steps}</ol>
    {figure(v, 1)}
    <h2>What the record shows</h2><ul class="list">{facts}</ul>
    <section class="lim" data-tone-zone="wash"><h2>Limits, stated plainly</h2><ul class="list">{limits}</ul></section>
    {nxt}
    <div class="cont"><p class="kick">Continue reading</p><p>This entry is a summary. The full account, with transactions and what went wrong, is published by the founder.</p><a class="btn" href="{v['buildRecord']}">{C['kenashe']['line']}</a>{rel}</div>
  </div>
</div></article>"""
    return body


def services(ctx):
    out = ""
    b = V["domain-brokerage"]
    for i, s in enumerate(C["services"]):
        inc = "".join(f"<li>{E(x)}</li>" for x in s["includes"])
        nots = ('<h3 class="lab">What this is not</h3><ul class="list list-x">' + "".join(f"<li>{E(x)}</li>" for x in s["not"]) + "</ul>") if s["not"] else ""
        steps = ('<ol class="steps">' + "".join(f'<li><span>{ROMAN[k]}.</span><h3>{E(t)}</h3><p>{E(x)}</p></li>' for k, (t, x) in enumerate(b["flow"])) + "</ol>") if i == 0 else ""
        cta = f'<a class="btn" href="{ctx.to("contact/")}?path=domains">Inquire about a domain</a>' if i == 0 else f'<a class="tl" href="{ctx.to("contact/")}?path=general">Ask whether it fits</a>'
        out += f"""<section class="ch ch-{i + 1}" id="{s['id']}" data-tone-zone="{'wash' if i == 0 else 'paper'}" data-run-label="{E(s['name'])}">
  <div class="ch-n"><span>Chapter</span>{ROMAN[i].upper()}</div>
  <div class="ch-main"><p class="kick">{E(s['status'].title())}</p><h2 class="kin">{E(s['name'])}</h2><p class="stand">{E(s['lead'])}</p><p>{E(s['body'])}</p>{steps}<p class="terms">{E(s['terms'])}</p><p class="acts">{cta}</p></div>
  <div class="ch-side"><h3 class="lab">In scope</h3><ul class="list">{inc}</ul>{nots}</div>
</section>"""
    return f"""{phd("Services", "The commercial practice, <em>in three chapters.</em>", "Domain acquisition and brokerage is the standing service and comes first. The other two are taken on selectively, where they support a launch, an identity, or a venture.")}{out}"""


def about(ctx):
    parts = "".join(f"""<section class="part rv" data-run-label="Part {s['n']}: {E(s['title'])}"><p class="part-n">{s['n']}</p><div><h2>{E(s['title'])}</h2><p class="stand">{E(s['line'])}</p><p>{E(s['body'])}</p></div></section>""" for s in C["story"])
    tl = "".join(f'<li><time>{E(t["date"])}</time><h3>{E(t["label"])}</h3><p>{E(t["text"])}</p></li>' for t in C["timeline"])
    model = "".join(f"<li><b>{E(a)}</b> {E(b)}</li>" for a, b in C["company"]["model"])
    return f"""{phd("About the company", "It began with <em>literal</em> domains.")}
<div class="essay" data-tone-zone="paper"><p class="drop">{E(C['company']['aboutLong'])}</p></div>
<div class="parts" data-tone-zone="paper">{parts}</div>
<section class="hist" data-tone-zone="wash" data-run-label="The record" aria-labelledby="hist-h"><div class="hist-hd"><p class="kick">The record</p><h2 id="hist-h">Dated, public, <em>checkable.</em></h2></div><div class="hist-track" data-track><i class="hist-line" aria-hidden="true"></i><ol class="hist-list">{tl}</ol></div><p class="fine">A founding year is not published, so none is shown.</p></section>
<section class="arr" data-tone-zone="paper" data-run-label="The arrangement"><p class="kick">The arrangement</p><h2>Who does <em>what.</em></h2><ul class="arr-l">{model}</ul><p class="acts"><a class="btn" href="{ctx.to('ventures/')}">Read the register</a><a class="tl ext" href="{C['kenashe']['url']}">Visit KenAshe.ai</a></p></section>"""


def founder(ctx):
    f = C["founder"]
    bio = f'<p class="drop">{E(f["bio"][0])}</p>' + "".join(f"<p>{E(p)}</p>" for p in f["bio"][1:])
    cred = "".join(f"<div><dt>{E(a)}</dt><dd>{E(b)}</dd></div>" for a, b in f["credentials"])
    sp = "".join(f"<div><dt>{E(y)}, {E(ev)}</dt><dd>{E(t)}</dd></div>" for y, ev, t in f["speaking"])
    links = "".join(f'<li><a class="tl ext" href="{u}">{E(l)}</a></li>' for l, u in f["links"])
    return f"""{phd("The founder", "Ken Ashe, <em>builder and operator.</em>", E(f['lead']))}
<div class="art-grid art-grid-f" data-tone-zone="paper">
  <section class="margin" aria-label="Portrait and credentials"><figure class="port"><img src="{ctx.asset(f['image'])}" alt="Portrait of Ken Ashe" width="420" height="420"><figcaption>Ken Ashe. Founder, Lucky Domains.</figcaption></figure>
    <h2 class="lab">Credentials, as operating evidence</h2><dl class="glance">{cred}</dl><p class="fine">{E(f['membership'])}</p></section>
  <div class="prose">{bio}
    <blockquote class="pull"><p>{E(f['quote'])}</p><cite>{E(f['quoteSource'])}</cite></blockquote>
    <h2>Speaking and judging</h2><dl class="glance glance-w">{sp}</dl>
    <div class="cont"><p class="kick">Two sites, two jobs</p><p>KenAshe.ai is the personal build record: experiments, logs, videos, and what failed. This site is the company that holds and operates the results.</p><a class="btn" href="{C['kenashe']['url']}">Visit KenAshe.ai</a><ul class="margin-l row">{links}</ul></div>
  </div>
</div>"""


def news(ctx):
    items = ""
    for n in C["news"]:
        link = f'<a class="tl ext" href="{n["url"]}">Read at the source: {E(n["source"])}</a>' if n["url"] else '<span class="fine">No link. This item exists only in this concept.</span>'
        stamp = '<span class="stamp" aria-hidden="true">Sample</span>' if n["concept"] else ""
        items += f"""<article class="nt rv{' nt-sample' if n['concept'] else ''}">{stamp}<p class="nt-d"><time>{E(n['date'])}</time><span>{E(n['type'].title() if not n['concept'] else n['type'])}</span></p><div><h2>{E(n['title'])}</h2><p>{E(n['text'])}</p>{link}</div></article>"""
    return f"""{phd("News", "Notices, <em>in the order they happened.</em>", "Published company news is kept as written. Project updates are dated summaries of public build records. Sample copy is marked as such.")}
<section class="nts" data-tone-zone="paper">{items}</section>"""


def contact(ctx):
    paths = C["contact"]["paths"]
    radios = "".join(f'<label class="rt"><input type="radio" name="regarding" value="{p["id"]}"{" checked" if i == 0 else ""}><span><b>{E(p["label"])}</b><em>{E(p["blurb"])}</em></span></label>' for i, p in enumerate(paths))
    groups = "".join(f'<div class="cf-g" data-for="{p["id"]}"{" hidden" if i else ""}>{"".join(field(x, is_long(x)) for x in p["fields"])}</div>' for i, p in enumerate(paths))
    return f"""{phd("Correspondence", "Write to <em>the company.</em>", "Four kinds of letter are expected. Choose one, and the form asks only what that inquiry needs.")}
<section class="corr" data-tone-zone="paper">
  <form class="cf" novalidate>
    <fieldset><legend class="lab">Regarding</legend>{radios}</fieldset>
    <div class="cf-fields"><h2 class="lab">Your details</h2>{field("Name")}{field("Email", type_="email")}{groups}
      <button class="btn" type="button">Send the letter</button><p class="cf-note" role="status">{E(C['contact']['notice'])}</p></div>
  </form>
  <div class="corr-side"><h2 class="lab">By email</h2><p><a class="tl" href="mailto:{C['company']['email']}">{C['company']['email']}</a></p><p class="fine">The published company address. The form here is a design mockup and sends nothing.</p></div>
</section>"""


def build():
    write(f"{DIR}/index.html", shell("", "Front page", C["company"]["description"], home))
    write(f"{DIR}/ventures/index.html", shell("ventures/", "Ventures", "The register of ventures.", ventures))
    for v in C["ventures"]:
        if v["detail"]:
            write(f"{DIR}/ventures/{v['id']}/index.html", shell(f"ventures/{v['id']}/", v["name"], v["summary"], venture_detail(v)))
    write(f"{DIR}/services/index.html", shell("services/", "Services", "Domain acquisition and brokerage, digital identity, and selected engagements.", services))
    write(f"{DIR}/about/index.html", shell("about/", "About", C["company"]["aboutLong"], about))
    write(f"{DIR}/founder/index.html", shell("founder/", "Founder", C["founder"]["lead"], founder))
    write(f"{DIR}/news/index.html", shell("news/", "News", "Company news and project updates.", news))
    write(f"{DIR}/contact/index.html", shell("contact/", "Contact", "Contact Lucky Domains.", contact))
