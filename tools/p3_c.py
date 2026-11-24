"""Version 3, Concept C: Original, Interactive. The production design with a living presence map in
the navy hero, layers that light as you scroll, a quick presence check, and example checks that cycle
on every service page. Readable and complete without any of it."""
import json
from p3lib import (C, E, S, L, PG, icon, eyebrow, check, sec_head, section, cards, steps, panel, split, note,
                   svc_cards, lab_cards, work_cards, build_concept, LAYER_OF, LAYER_ICON, cta_band)

CFG = {"k": "C", "name": "Original, Interactive", "dir": "phase-3/interactive", "js_version": "?v=20261124-center"}
CHECK_KEY = {"websites": "websites", "seo": "seo", "ai": "ai", "entity": "entity", "domains": "domains", "buy": "domains"}


def map_block(ctx, mid, sticky=False):
    M = C["map"]
    data = {"nodes": [dict(n, href=ctx.svc(n["service"]), svcName=S[n["service"]]["name"]) for n in M["nodes"]],
            "problems": M["problems"], "icon": ctx.asset("logo-icon-128.png"),
            "diag": {o["id"]: {"start": o["start"], "why": o["why"], "href": ctx.svc(o["service"])} for o in C["diagnostic"]["options"]}}
    blob = json.dumps(data).replace("</", "<\\/")
    fb = "".join(f'<li><b>{E(n["label"])}</b> {E(n["line"])}</li>' for n in M["nodes"])
    seg = '' if sticky else '<div class="seg" role="group" aria-label="Map state"><button type="button" class="sg" data-state="fragmented" aria-pressed="false">Fragmented</button><button type="button" class="sg" data-state="recognized" aria-pressed="true">Recognized</button></div>'
    return f'<div class="pmap{" pmap-s" if sticky else ""}" data-map="{mid}"><div class="pm-bar"><p class="pm-t" id="{mid}-t">Presence map</p>{seg}</div><div class="pm-view" aria-labelledby="{mid}-t"><ul class="pm-fb">{fb}</ul></div><p class="pm-cap">{E(M["caption"])}</p><script type="application/json" class="pm-data">{blob}</script></div>'


def checks_panel(key, title=None):
    k = CHECK_KEY.get(key)
    if not k:
        return ""
    items = C["checks"][k]
    lis = "".join(f'<li data-i="{i}"><span class="ck-n">{i + 1:02d}</span>{E(x)}</li>' for i, x in enumerate(items))
    return f'<div class="xchk reveal" data-xchk><div class="xc-hd"><h3>{E(title or "What we check")}</h3><button type="button" class="xc-pause" aria-pressed="false">Pause</button></div><ol class="xc-l">{lis}</ol><p class="xc-cap">{E(C["checks"]["label"])}</p></div>'


def audit():
    a = C["audit"]
    rows = "".join(f'<li><label class="au-o"><input type="checkbox" data-layer="{l}"><span>{E(t)}</span></label></li>' for l, t in a["items"])
    meters = "".join(f'<li data-m="{l["id"]}"><span>{E(l["name"])}</span><i aria-hidden="true"></i></li>' for l in C["stack"])
    recs = "".join(f'<div class="au-r" data-for="{l["id"]}"><p class="eyebrow eb-dark">Start here</p><h3>{E(S[l["service"]]["name"])}</h3><p>{E(S[l["service"]]["short"])}</p></div>' for l in C["stack"])
    return f'<div class="au"><div class="reveal">{eyebrow("Interactive")}<h2>{E(a["title"])}</h2><p class="section-lead">{E(a["intro"])}</p><fieldset class="au-f"><legend class="sr">Check each statement that is true</legend><ul>{rows}</ul></fieldset></div><div class="au-out" aria-live="polite"><p class="au-k"><b data-count>0</b> of 6 in place</p><ol class="au-m" aria-label="Layers">{meters}</ol>{recs}<div class="au-r au-all" data-for="all"><h3>Everything checks out.</h3><p>A real audit would still find things. Worth a conversation.</p></div><p class="au-note">Self-check only. Nothing is stored or sent.</p></div></div>'


def home(ctx):
    h = C["hero"]; f = C["founder"]; fw = C["work"][0]; art = C["article"]
    steps_h = "".join(f'<li class="ly" data-act="{l["id"]}"><span class="ly-n">{l["n"]}</span><div><h3>{E(l["name"])}</h3><p class="ly-l">{E(l["line"])}</p><p>{E(l["detail"])}</p><a class="link-arrow" href="{ctx.svc(l["service"])}">{E(S[l["service"]]["name"])} {icon("arrow", "2.4")}</a></div></li>' for l in C["stack"])
    probs = "".join(f'<button type="button" class="pb" data-problem="{o["id"]}" aria-pressed="false">{E(o["label"])}</button>' for o in C["diagnostic"]["options"])
    uses_html = '<div class="grid grid-2 uses-c">' + "".join('<div class="card card-sm reveal"><h3>%s</h3><p>%s</p></div>' % (E(u["name"]), E(u["line"])) for u in C["aiWork"]["uses"][:6]) + "</div>"
    tabs = "".join(f'<button type="button" role="tab" id="xt-{s["id"]}" aria-controls="xp-{s["id"]}" aria-selected="{"true" if i == 0 else "false"}" tabindex="{0 if i == 0 else -1}">{icon(s["icon"])}{E(s["tag"])}</button>' for i, s in enumerate(C["services"]))
    pans = "".join(f'<div role="tabpanel" id="xp-{s["id"]}" aria-labelledby="xt-{s["id"]}" class="xp" tabindex="0"><h3>{E(s["name"])}</h3><p>{E(s["short"])}</p>{checks_panel(s["id"], "Examples of what we check")}<a class="btn btn-accent" href="{ctx.svc(s["id"])}">Explore {E(s["name"])}</a></div>' for s in C["services"])
    return f"""
<section class="hero hero-c">
  <div class="container hero-split">
    <div class="hero-inner">
      {eyebrow(h['eyebrow'], True)}
      <h1>{E(h['headline'])}</h1>
      <p class="lead">{E(h['support'])}</p>
      <div class="btn-row"><a href="{ctx.to('contact/')}" class="btn btn-accent btn-lg">{E(h['cta1'])}</a><a href="{ctx.to('services/')}" class="btn btn-on-dark btn-lg">{E(h['cta2'])}</a></div>
      <div class="hero-trust">{icon('check', '2.4')} {E(h['founder'])}</div>
    </div>
    <div class="hero-map">{map_block(ctx, 'm1')}
      <div class="probs"><p class="pb-h" id="pb-h">What is holding you back?</p><div class="pbs" role="group" aria-labelledby="pb-h">{probs}</div>
      <div class="pm-card" aria-live="polite"><p class="pc-k">Start here</p><h2 class="pc-t">Pick a problem, or select any signal on the map.</h2><p>The map lights the signals involved and names the service that fixes them.</p></div></div>
    </div>
  </div>
</section>

<section class="section how" id="how"><div class="container">
  {sec_head('How recognition is built', 'Five layers. Each one lights the next.', C['stackReinforce'])}
  <div class="how-g"><div class="how-map">{map_block(ctx, 'm2', True)}</div><ol class="lys">{steps_h}</ol></div>
</div></section>

{section('services', sec_head('What we do', 'Five services. One digital presence.', C['company']['descriptionLong']) + svc_cards(ctx), True)}

{section('check', audit())}

{section('examples', sec_head('In practice', 'What each service actually checks.', 'Choose a service. The list runs through examples on its own and stops when you interact.') + f'<div class="xt"><div class="xt-tabs" role="tablist" aria-label="Services">{tabs}</div><div class="xt-ps">{pans}</div></div>', True)}

{section('work', sec_head('Selected work', 'Projects mapped to the layers they touched.', fw['noMetrics']) + work_cards(ctx, C['work'][:3]))}

{section('story', f'<div class="story-c reveal">{eyebrow("The Lucky Domains story")}<h2>{E(C["company"]["storyHeadline"])}</h2><p class="section-lead">{E(C["company"]["story"])}</p></div>', True)}

{section('ai-work', split(sec_head(C['aiWork']['title'], C['aiWork']['principle'], '', False) + f'<p class="section-lead">{E(C["aiWork"]["intro"])}</p>', uses_html))}

{section('founder', split(sec_head('Founder', C['company']['founderLine'], '', False) + f'<p class="section-lead">{E(f["bio"])}</p><p><strong>{E(C["company"]["accountability"])}</strong></p><div class="btn-row"><a class="btn btn-ghost" href="{ctx.to("founder/")}">About Ken</a><a class="btn btn-ghost" href="{ctx.to(art["slug"])}">Read the research note</a></div>', f'<figure class="founder-card reveal"><img src="{ctx.asset(f["image"])}" alt="Ken Ashe, founder of Lucky Domains" width="460" height="460" loading="lazy"></figure>', True), True)}
{cta_band(ctx, 'Find out where your presence is weakest.', None, C['hero']['cta1'])}"""


def hero_extra(ctx, key):
    lid = LAYER_OF.get(key)
    if not lid:
        return ""
    chips = "".join(f'<li{" class=on aria-current=true" if l["id"] == lid else ""}><span>{l["n"]}</span>{E(l["name"])}</li>' for l in C["stack"])
    return f'<ol class="hx" aria-label="Where this service sits in the Digital Presence Stack">{chips}</ol>'


def named_engagement(ctx, key):
    name = C["conceptC"]["engagements"].get(key)
    if not name:
        return ""
    e = next(e for e in PG["services"]["engagements"] if e["name"] == name)
    cta = f'<p class="v3-more"><a class="btn btn-accent" href="{ctx.to("contact/")}">Ask about this engagement</a></p>'
    return section("engagement", split(sec_head("Named engagement", name, "", False)
                    + f'<p class="section-lead">{E(e["line"])} The scope is agreed in writing before work starts.</p>' + cta,
                    panel("What is included", e["check"])), True)


def inner(ctx, key, hero, secs):
    out = hero
    for n, (i, lab, html) in enumerate(secs):
        out += html
        if n == 0:
            out += named_engagement(ctx, key)
            if key in CHECK_KEY:
                out += section("checks", '<div class="xwrap">' + checks_panel(key) + "</div>", not C["conceptC"]["engagements"].get(key))
    return out


def build():
    build_concept(dict(CFG, home=home, inner=inner, hero_extra=hero_extra))
