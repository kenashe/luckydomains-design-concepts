"""Concept C: Namespace. A spatial, interface-like reading of the company: everything has an address."""
import json
from lib import C, E, V, Ctx, head, write, status_slug, NOTICE, field, is_long

DIR = "concept-c-namespace"
NAME = "Namespace"
NAV = [("ventures/", "Ventures"), ("services/", "Services"), ("about/", "About"), ("founder/", "Founder"), ("news/", "News"), ("contact/", "Contact")]
SHORT = {"zerohuman": "ZeroHuman", "ai-agent-economy": "Agent Economy", "autonomous-seo-agent": "SEO Agent",
         "domain-brokerage": "Domain Brokerage", "luckydomains-site": "LuckyDomains.io build", "sir-pitches-a-lot": "Sir Pitches-a-Lot"}
P = {p["id"]: p for p in C["pillars"]}
# hand-placed coordinates: [landscape x, y, portrait x, y]
POS = {"core": [380, 285, 175, 300], "domains": [215, 175, 92, 185], "identity": [520, 140, 258, 185], "agents": [535, 425, 258, 420],
       "presence": [225, 405, 92, 420], "domain-brokerage": [95, 95, 80, 78], "zerohuman": [672, 225, 286, 300],
       "ai-agent-economy": [668, 335, 205, 70], "autonomous-seo-agent": [385, 505, 178, 552], "luckydomains-site": [100, 490, 76, 505],
       "sir-pitches-a-lot": [672, 500, 280, 505]}


def st(v):
    s = v["status"]
    return f'<span class="chip st-{status_slug(s)}"><i aria-hidden="true"></i>{E(s.title())}</span>'


def vhref(ctx, v):
    if v["detail"]:
        return ctx.to(f'ventures/{v["id"]}/')
    if v.get("internal"):
        return ctx.to(f'{v["internal"]}/#domains')
    return ctx.to(f'ventures/#{v["id"]}')


def addr(v):
    return f'luckydomains.io/ventures/{v["id"]}' if not v.get("internal") else "luckydomains.io/services#domains"


def map_data(ctx):
    nodes = [{"id": "core", "type": "core", "label": "Lucky Domains", "pos": POS["core"], "title": "Lucky Domains",
              "text": C["company"]["description"], "href": ctx.to("about/"), "cta": "About the company", "chip": "Operating company"}]
    edges = []
    for p in C["pillars"]:
        nodes.append({"id": p["id"], "type": "pillar", "label": p["label"], "pos": POS[p["id"]], "title": p["label"], "text": p["line"], "chip": "Domain of work",
                      "href": ctx.to("ventures/") + "?in=" + p["id"], "cta": f'Ventures in {p["label"].lower()}'})
        edges.append(["core", p["id"], "spine"])
    for v in C["ventures"]:
        nodes.append({"id": v["id"], "type": "venture", "label": SHORT[v["id"]], "pos": POS[v["id"]], "title": v["name"], "text": v["summary"],
                      "status": v["status"], "chip": v["status"].title(), "kind": v["kind"], "href": vhref(ctx, v),
                      "cta": "Open the record" if v["detail"] else ("See the service" if v.get("internal") else "See the entry"),
                      "log": v["buildRecord"], "pillars": v["pillars"]})
        for i, p in enumerate(v["pillars"]):
            edges.append([p, v["id"], "main" if i == 0 else "also"])
    seen = set()
    for v in C["ventures"]:
        for r in v["related"]:
            k = tuple(sorted([v["id"], r]))
            if k not in seen:
                seen.add(k); edges.append([v["id"], r, "rel"])
    return json.dumps({"nodes": nodes, "edges": edges, "icon": ctx.asset("logo-icon-reversed-128.png"), "logLine": C["kenashe"]["line"]}).replace("</", "<\\/")


def map_block(ctx, big=False):
    chips = '<button type="button" class="fchip" data-pillar="all" aria-pressed="true">All</button>' + "".join(
        f'<button type="button" class="fchip" data-pillar="{p["id"]}" aria-pressed="false">{E(p["label"])}</button>' for p in C["pillars"])
    return f"""<div class="map{' map-big' if big else ''}" data-map>
  <div class="map-bar"><span class="map-t"><i aria-hidden="true"></i>namespace map</span><div class="map-f" role="group" aria-label="Highlight a domain of work">{chips}</div></div>
  <div class="map-view"><noscript><p class="map-ns">The interactive map needs JavaScript. The same information is in the list on this page.</p></noscript></div>
  <div class="map-card" aria-live="polite"><p class="map-card-k"><span class="chip">Operating company</span></p><h2>Lucky Domains</h2><p>Select a node to see what it is and how it connects. Every node is also in the list below.</p></div>
  <p class="map-legend"><span><i class="lg lg-live"></i>Live</span><span><i class="lg lg-ship"></i>Shipped</span><span><i class="lg lg-act"></i>Active service</span><span><i class="lg lg-line"></i>Related builds</span></p>
  <script type="application/json" class="map-data">{map_data(ctx)}</script>
</div>"""


def shell(path, title, desc, body, segs):
    ctx = Ctx(DIR, path)
    nav = "".join(f'<a href="{ctx.to(p)}"{ctx.cur(p)}>{E(l)}</a>' for p, l in NAV)
    dirs = "".join(f'<li><a href="{ctx.to(p)}"{ctx.cur(p) if p else (" aria-current=page" if path == "" else "")}><span>/{p}</span>{E(l)}</a></li>' for p, l in [("", "Home")] + NAV)
    seg = "".join(f'<span class="ab-s">/</span><span class="ab-p">{E(s)}</span>' for s in segs)
    return f"""{head(ctx, f"{title} | Lucky Domains, Concept C: Namespace", desc, "css/style.css", ("jakarta-normal-400-800.woff2",))}
<body>
<a class="skip" href="#main">Skip to content</a>
<aside class="review" aria-label="Review notice"><span>{NOTICE}</span> <a href="{ctx.r}">All concepts</a></aside>
<header class="hd">
  <a class="hd-logo" href="{ctx.to()}" aria-label="Lucky Domains, concept home"><img src="{ctx.asset('logo-icon-128.png')}" alt="Lucky Domains" width="40" height="40"></a>
  <div class="ab-wrap">
    <button class="ab" type="button" aria-expanded="false" aria-controls="dir" aria-label="Site directory. Current address: luckydomains.io/{'/'.join(segs)}">
      <span class="ab-lock" aria-hidden="true"></span><span class="ab-h">luckydomains.io</span>{seg}<span class="ab-hash" data-hash aria-hidden="true"></span><span class="ab-c" aria-hidden="true"></span>
    </button>
    <nav id="dir" class="dir" aria-label="Site directory" hidden><ul>{dirs}</ul><p><a href="{C['kenashe']['url']}">kenashe.ai <span>the founder's build record ↗</span></a></p></nav>
  </div>
  <nav class="hd-nav" aria-label="Primary">{nav}</nav>
</header>
<main id="main">
{body(ctx)}
</main>
<footer class="ft">
  <div class="ft-in">
    <div class="ft-brand"><img src="{ctx.asset('logo-wordmark.png')}" alt="Lucky Domains" width="210" height="52" loading="lazy"><p>{E(C['company']['description'])}</p></div>
    <div><h2>/company</h2><ul>{"".join(f'<li><a href="{ctx.to(p)}">{E(l)}</a></li>' for p, l in NAV)}</ul></div>
    <div><h2>/record</h2><ul><li><a href="{C['kenashe']['url']}">KenAshe.ai</a></li><li><a href="{C['kenashe']['building']}">Build logs</a></li><li><a href="https://github.com/kenashe">GitHub</a></li><li><a href="mailto:{C['company']['email']}">{C['company']['email']}</a></li></ul></div>
    <div><h2>/logo</h2><div class="ft-marks"><span><img src="{ctx.asset('logo-icon-128.png')}" alt="Lucky Domains icon, original" width="40" height="40" loading="lazy"></span><span class="dk"><img src="{ctx.asset('logo-icon-reversed-128.png')}" alt="Lucky Domains icon, reversed concept treatment" width="40" height="40" loading="lazy"></span></div><p class="ft-s">Original wordmark and icon. The reversed icon is a concept treatment for navy surfaces.</p></div>
  </div>
  <p class="ft-note">{NOTICE} Concept C: Namespace. Facts as of {E(C['asOf'])}. <a href="{ctx.r}">Back to all concepts</a></p>
</footer>
<script src="{ctx.c}js/main.js" defer></script>
</body></html>"""


def vcard(ctx, v, h="h3"):
    pills = "".join(f'<span class="tag">{E(P[p]["label"])}</span>' for p in v["pillars"])
    rel = "".join(f'<a class="tag tag-l" href="{vhref(ctx, V[r])}">linked: {E(SHORT[r])}</a>' for r in v["related"])
    log = f'<a class="lk ext" href="{v["buildRecord"]}">{C["kenashe"]["line"] if v["detail"] else "Build record on KenAshe.ai"}</a>' if v["buildRecord"] else ""
    more = "".join(f'<a class="lk ext" href="{u}">{E(l)}</a>' for l, u in v["links"])
    open_ = f'<a class="lk" href="{vhref(ctx, v)}">{"Open the record" if v["detail"] else "See the service"}</a>' if (v["detail"] or v.get("internal")) else ""
    return f"""<article class="vc" id="{v['id']}" data-pillars="{' '.join(v['pillars'])}">
  <p class="vc-a">{E(addr(v))}</p>
  <p class="vc-top">{st(v)}<span class="vc-k">{E(v['kind'])} · {E(v['since'])}</span></p>
  <{h}><a href="{vhref(ctx, v)}">{E(v['name'])}</a></{h}>
  <p class="vc-t">{E(v['tagline'])}</p>
  <p class="vc-s">{E(v['summary'])}</p>
  <p class="vc-tags">{pills}{rel}</p>
  <p class="vc-l">{open_}{log}{more}</p>
</article>"""


def route(flow, cls=""):
    items = "".join(f'<li><span class="rt-n">{i}</span><h3>{E(t)}</h3><p>{E(x)}</p></li>' for i, (t, x) in enumerate(flow, 1))
    return f'<ol class="route {cls}" style="--n:{len(flow)}">{items}</ol>'


def layers(ctx):
    data = [("domains", "01", "Name", C["story"][0]["line"], ("Domain acquisition and brokerage", ctx.to("services/") + "#domains")),
            ("presence", "02", "Presence", C["story"][1]["line"], ("Selected engagements", ctx.to("services/") + "#engagements")),
            ("identity", "03", "Identity", "Records, structured data, and ENS names make it unambiguous who or what is behind the name.", ("Digital identity and presence", ctx.to("services/") + "#identity")),
            ("agents", "04", "Agents", C["story"][2]["line"], ("See the ventures", ctx.to("ventures/")))]
    plates = "".join(f'<div class="pl pl-{i}" data-pl="{d[0]}"><span>{d[1]}</span>{d[2]}</div>' for i, d in enumerate(data))
    rows = "".join(f'<li data-ly="{d[0]}"><span class="ly-n">{d[1]}</span><div><h3>{d[2]}</h3><p>{E(d[3])}</p><a class="lk" href="{d[4][1]}">{E(d[4][0])}</a></div></li>' for d in data)
    return f"""<div class="ly" data-layers><div class="ly-fig" aria-hidden="true"><div class="ly-stack">{plates}</div></div><ol class="ly-list">{rows}</ol></div>"""


def home(ctx):
    cards = "".join(vcard(ctx, v) for v in C["ventures"])
    b = V["domain-brokerage"]; f = C["founder"]
    return f"""
<section class="hero" data-addr="">
  <div class="hero-copy">
    <p class="eyebrow"><span class="chip st-active-service"><i aria-hidden="true"></i>Domain brokerage: active</span><span class="chip st-live"><i aria-hidden="true"></i>Ventures: live</span></p>
    <h1>Every venture starts with <span>a name.</span></h1>
    <p class="lede">{E(C['company']['description'])}</p>
    <p class="cta"><a class="btn btn-p" href="#map">Explore the map</a><a class="btn" href="{ctx.to('services/')}#domains">Domain acquisition and brokerage</a></p>
  </div>
  <div class="hero-map" id="map">{map_block(ctx)}</div>
</section>

<section class="sec" data-addr="ventures" aria-labelledby="idx-h">
  <div class="sec-hd"><p class="path">/ventures</p><h2 id="idx-h">The same map, as a list.</h2><p>Six records. Filter by domain of work and the cards rearrange. Each one links to the founder's full build log where one exists.</p></div>
  <div class="tools"><div class="map-f" role="group" aria-label="Filter ventures by domain of work" data-gridfilter><button type="button" class="fchip" data-pillar="all" aria-pressed="true">All</button>{"".join(f'<button type="button" class="fchip" data-pillar="{p["id"]}" aria-pressed="false">{E(p["label"])}</button>' for p in C["pillars"])}</div></div>
  <div class="grid" data-grid>{cards}</div>
</section>

<section class="sec" data-addr="layers" aria-labelledby="ly-h">
  <div class="sec-hd"><p class="path">/about#layers</p><h2 id="ly-h">Four layers, built in order.</h2><p>Each layer made the next one possible. The first is still a service you can hire.</p></div>
  {layers(ctx)}
</section>

<section class="desk" data-addr="domains" aria-labelledby="dk-h">
  <div class="desk-in">
    <p class="path">/services#domains {st(b)}</p>
    <h2 id="dk-h">Domain acquisition and brokerage, still at the root.</h2>
    <p class="lede">{E(C['services'][0]['body'])}</p>
    {route(b['flow'], 'route-dk')}
    <p class="terms">{E(C['services'][0]['terms'])}</p>
    <p class="cta"><a class="btn btn-p" href="{ctx.to('contact/')}?path=domains">Start a domain inquiry</a><a class="btn btn-d" href="{ctx.to('services/')}#domains">Scope and terms</a></p>
  </div>
</section>

<section class="sec link2" data-addr="founder" aria-labelledby="l2-h">
  <div class="sec-hd"><p class="path">/founder</p><h2 id="l2-h">Two addresses, two jobs.</h2></div>
  <div class="l2">
    <a class="l2-n l2-k" href="{C['kenashe']['url']}"><span class="path">kenashe.ai ↗</span><b>Ken Ashe builds in public.</b><span>Experiments, build logs, videos, and what failed.</span></a>
    <div class="l2-mid" aria-hidden="true"><i></i><img src="{ctx.asset(f['image'])}" alt="" width="120" height="120" loading="lazy"><i></i></div>
    <a class="l2-n l2-l" href="{ctx.to('ventures/')}"><span class="path">luckydomains.io</span><b>Lucky Domains operates the ventures.</b><span>Summaries here, full records there. Brokerage stays an active service.</span></a>
  </div>
  <p class="cta c"><a class="btn" href="{ctx.to('founder/')}">About Ken Ashe</a></p>
</section>"""


def phd(path, h1, lede=""):
    return f'<header class="phd"><p class="path">{E(path)}</p><h1>{h1}</h1>{f"<p class=lede>{lede}</p>" if lede else ""}</header>'


def ventures(ctx):
    cards = "".join(vcard(ctx, v, "h2") for v in C["ventures"])
    chips = '<button type="button" class="fchip" data-pillar="all" aria-pressed="true">All</button>' + "".join(f'<button type="button" class="fchip" data-pillar="{p["id"]}" aria-pressed="false">{E(p["label"])}</button>' for p in C["pillars"])
    return f"""{phd("/ventures", "Ventures, records, and one standing service.", "Six entries in the Lucky Domains namespace. Statuses mirror the labels on the public build record.")}
<section class="sec sec-t" data-addr="">
  <div class="tools"><div class="seg" role="group" aria-label="View"><button type="button" data-view="grid" aria-pressed="true">Grid</button><button type="button" data-view="map" aria-pressed="false">Map</button></div>
  <div class="map-f" role="group" aria-label="Filter ventures by domain of work" data-gridfilter>{chips}</div></div>
  <div class="grid" data-grid>{cards}</div>
  <div class="mapview" data-mapview hidden>{map_block(ctx, True)}</div>
  <p class="fine">Figures and statuses come from KenAshe.ai and LuckyDomains.io, read {E(C['asOf'])}. Grouping these builds under Lucky Domains is the positioning this concept proposes.</p>
</section>"""


def venture_detail(v):
    def body(ctx):
        m = "".join(f"<div><dt>{E(k)}</dt><dd>{E(val)}</dd></div>" for k, val in v["meta"])
        paras = "".join(f"<p>{E(p)}</p>" for p in v["body"])
        facts = "".join(f"<li>{E(x)}</li>" for x in v["facts"])
        limits = "".join(f"<li>{E(x)}</li>" for x in v["limits"])
        a = v["artifact"]
        lines = "".join(f'<div class="ev-r"><span>{E(t)}</span><code>{E(x)}</code></div>' for t, x in a["lines"])
        links = "".join(f'<a class="lk ext" href="{u}">{E(l)}</a>' for l, u in v["links"])
        conn = "".join(f'<a class="node" href="{ctx.to("ventures/")}?in={p}"><i class="nd nd-p"></i><span><b>{E(P[p]["label"])}</b>{E(P[p]["line"])}</span></a>' for p in v["pillars"])
        conn += "".join(f'<a class="node" href="{vhref(ctx, V[r])}"><i class="nd nd-v"></i><span><b>{E(V[r]["name"])}</b>{E(V[r]["tagline"])}</span></a>' for r in v["related"])
        nxt = f'<p class="nxt"><span class="path">next</span>{E(v["next"])}</p>' if v["next"] else ""
        return f"""{phd(f"/ventures/{v['id']}", E(v['name']), E(v['tagline']))}
<div class="rec">
  <section class="rec-side" aria-label="Record"><div class="tile"><p class="vc-top">{st(v)}<span class="vc-k">{E(v['kind'])}</span></p><dl class="kv">{m}</dl><p class="rec-l">{links}</p></div>
    <a class="tile tile-g" href="{v['buildRecord']}"><span class="path">kenashe.ai ↗</span><b>{C['kenashe']['line']}</b></a></section>
  <div class="rec-main">
    <section class="tile" data-addr="summary"><p class="path">#summary</p><p class="big">{E(v['summary'])}</p>{paras}</section>
    <section class="tile" data-addr="flow"><p class="path">#flow</p><h2>{E(v['flowTitle'])}</h2>{route(v['flow'])}</section>
    <section class="tile tile-n" data-addr="evidence"><p class="path">#evidence</p><h2>{E(a['title'])}</h2><div class="ev">{lines}</div><p class="ev-c">{E(a['caption'])}</p><ul class="ck">{facts}</ul></section>
    <section class="tile tile-w" data-addr="limits"><p class="path">#limits</p><h2>What this does not prove</h2><ul class="ck ck-w">{limits}</ul>{nxt}</section>
    <section class="tile" data-addr="connections"><p class="path">#connections</p><h2>Connected to</h2><div class="nodes">{conn}</div></section>
  </div>
</div>"""
    return body


def services(ctx):
    s0, s1, s2 = C["services"]
    b = V["domain-brokerage"]

    def inc(s):
        return "".join(f"<li>{E(x)}</li>" for x in s["includes"])
    nots = "".join(f"<li>{E(x)}</li>" for x in s0["not"])
    return f"""{phd("/services", "One standing service. Two selective ones.", "Domain acquisition and brokerage sits at the root. Identity and site work branch from it, and are taken on when they support a launch, an identity, or a venture.")}
<section class="desk desk-p" id="domains" data-addr="domains">
  <div class="desk-in">
    <p class="path">/services#domains <span class="chip st-active-service"><i aria-hidden="true"></i>Active</span></p>
    <h2>{E(s0['name'])}</h2><p class="big">{E(s0['lead'])}</p><p class="lede">{E(s0['body'])}</p>
    {route(b['flow'], 'route-dk')}
    <div class="desk-cols"><div><h3>In scope</h3><ul class="ck ck-d">{inc(s0)}</ul></div><div><h3>What this is not</h3><ul class="ck ck-d ck-x">{nots}</ul><p class="terms">{E(s0['terms'])}</p></div></div>
    <p class="cta"><a class="btn btn-p" href="{ctx.to('contact/')}?path=domains">Start a domain inquiry</a></p>
  </div>
</section>
<section class="sec branch">
  <i class="branch-l" aria-hidden="true"></i>
  <div class="branch-g">
    <article class="tile" id="identity" data-addr="identity"><p class="path">/services#identity <span class="chip">Selective</span></p><h2>{E(s1['name'])}</h2><p class="big">{E(s1['lead'])}</p><p>{E(s1['body'])}</p><ul class="ck">{inc(s1)}</ul><p class="terms">{E(s1['terms'])}</p><p class="cta"><a class="btn" href="{ctx.to('contact/')}?path=general">Ask about fit</a></p></article>
    <article class="tile" id="engagements" data-addr="engagements"><p class="path">/services#engagements <span class="chip">By fit</span></p><h2>{E(s2['name'])}</h2><p class="big">{E(s2['lead'])}</p><p>{E(s2['body'])}</p><ul class="ck">{inc(s2)}</ul><p class="terms">{E(s2['terms'])}</p><p class="cta"><a class="btn" href="{ctx.to('contact/')}?path=general">Ask about fit</a></p></article>
  </div>
</section>"""


def about(ctx):
    tl = "".join(f'<li data-p="{t["pillar"]}"><time>{E(t["date"])}</time><div><h3>{E(t["label"])}</h3><p>{E(t["text"])}</p></div><span class="tag">{E(P[t["pillar"]]["label"])}</span></li>' for t in C["timeline"])
    model = "".join(f'<div class="tile"><b>{E(a)}</b><p>{E(b)}</p></div>' for a, b in C["company"]["model"])
    return f"""{phd("/about", "A company that started with literal domains.", E(C['company']['aboutLong']))}
<section class="sec sec-t" data-addr="layers"><div class="sec-hd"><p class="path">#layers</p><h2>Four layers, built in order.</h2></div>{layers(ctx)}</section>
<section class="sec" data-addr="record"><div class="sec-hd"><p class="path">#record</p><h2>The dated record.</h2><p>Only events with a public source. A founding year is not published, so none is shown.</p></div><ol class="tl">{tl}</ol></section>
<section class="sec" data-addr="structure"><div class="sec-hd"><p class="path">#structure</p><h2>Who does what.</h2></div><div class="model">{model}</div>
<p class="cta"><a class="btn btn-p" href="{ctx.to('ventures/')}">Open the ventures</a><a class="btn ext" href="{C['kenashe']['url']}">Visit KenAshe.ai</a></p></section>"""


def founder(ctx):
    f = C["founder"]
    bio = "".join(f"<p>{E(p)}</p>" for p in f["bio"])
    cred = "".join(f"<div><dt>{E(a)}</dt><dd>{E(b)}</dd></div>" for a, b in f["credentials"])
    sp = "".join(f"<div><dt>{E(y)} · {E(ev)}</dt><dd>{E(t)}</dd></div>" for y, ev, t in f["speaking"])
    roles = "".join(f'<span class="tag">{E(r)}</span>' for r in f["roles"])
    links = "".join(f'<a class="lk ext" href="{u}">{E(l)}</a>' for l, u in f["links"][1:])
    return f"""{phd("/founder", E(f['name']), E(f['lead']))}
<div class="rec rec-f">
  <section class="rec-side" aria-label="Portrait and links"><div class="tile tile-ph"><img src="{ctx.asset(f['image'])}" alt="Portrait of Ken Ashe" width="420" height="420"><p class="vc-tags">{roles}</p></div>
    <a class="tile tile-g" href="{C['kenashe']['url']}"><span class="path">kenashe.ai ↗</span><b>Visit KenAshe.ai, the build record</b></a><p class="rec-l">{links}</p></section>
  <div class="rec-main">
    <section class="tile" data-addr="background"><p class="path">#background</p>{bio}<blockquote><p>{E(f['quote'])}</p><cite>{E(f['quoteSource'])}</cite></blockquote></section>
    <section class="tile" data-addr="credentials"><p class="path">#credentials</p><h2>Operating evidence</h2><dl class="kv kv-w">{cred}</dl><p class="fine">{E(f['membership'])} Career: {E(", ".join(f['career']))}.</p></section>
    <section class="tile" data-addr="speaking"><p class="path">#speaking</p><h2>Speaking and judging</h2><dl class="kv kv-w">{sp}</dl></section>
  </div>
</div>"""


def news(ctx):
    items = ""
    for n in C["news"]:
        link = f'<a class="lk ext" href="{n["url"]}">Source: {E(n["source"])}</a>' if n["url"] else '<span class="fine">No link. This item exists only in this concept.</span>'
        items += f"""<article class="tile nw{' nw-s' if n['concept'] else ''}"><p class="vc-top"><span class="chip{' chip-w' if n['concept'] else ''}">{E(n['type'].title() if not n['concept'] else n['type'])}</span><time class="vc-k">{E(n['date'])}</time></p><h2>{E(n['title'])}</h2><p>{E(n['text'])}</p>{link}</article>"""
    return f"""{phd("/news", "Company news and project updates.", "Published news is preserved as written. Project updates are dated summaries of public build records. Sample copy is marked.")}
<section class="sec sec-t"><div class="feed">{items}</div></section>"""


def contact(ctx):
    paths = C["contact"]["paths"]
    btns = "".join(f'<button type="button" class="rtc" data-route="{p["id"]}" aria-pressed="{"true" if i == 0 else "false"}"><span class="path">/contact#{p["id"]}</span><b>{E(p["label"])}</b><span>{E(p["blurb"])}</span></button>' for i, p in enumerate(paths))
    groups = "".join(f'<div class="cf-g" data-for="{p["id"]}"{" hidden" if i else ""}>{"".join(field(x, is_long(x)) for x in p["fields"])}</div>' for i, p in enumerate(paths))
    return f"""{phd("/contact", "Four routes in.", "Choose a route and the form asks only what that inquiry needs.")}
<section class="sec sec-t ct">
  <div class="rtcs" role="group" aria-label="Inquiry route">{btns}</div>
  <form class="tile cf" novalidate><p class="path" data-cf-path>/contact#domains</p><h2 data-cf-title>{E(paths[0]['label'])}</h2>{field("Name")}{field("Email", type_="email")}{groups}
    <button class="btn btn-p" type="button">Send inquiry</button><p class="cf-note" role="status">{E(C['contact']['notice'])}</p>
    <p class="fine">Or write to <a href="mailto:{C['company']['email']}">{C['company']['email']}</a>, the company's published address.</p></form>
</section>"""


def build():
    write(f"{DIR}/index.html", shell("", "Home", C["company"]["description"], home, []))
    write(f"{DIR}/ventures/index.html", shell("ventures/", "Ventures", "Ventures in the Lucky Domains namespace.", ventures, ["ventures"]))
    for v in C["ventures"]:
        if v["detail"]:
            write(f"{DIR}/ventures/{v['id']}/index.html", shell(f"ventures/{v['id']}/", v["name"], v["summary"], venture_detail(v), ["ventures", v["id"]]))
    write(f"{DIR}/services/index.html", shell("services/", "Services", "Domain acquisition and brokerage, digital identity, and selected engagements.", services, ["services"]))
    write(f"{DIR}/about/index.html", shell("about/", "About", C["company"]["aboutLong"], about, ["about"]))
    write(f"{DIR}/founder/index.html", shell("founder/", "Founder", C["founder"]["lead"], founder, ["founder"]))
    write(f"{DIR}/news/index.html", shell("news/", "News", "Company news and project updates.", news, ["news"]))
    write(f"{DIR}/contact/index.html", shell("contact/", "Contact", "Contact Lucky Domains.", contact, ["contact"]))
