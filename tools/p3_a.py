"""Version 3, Concept A: Original, Evolved. The production site's structure and components, modernized,
with the three signature interactions: a recognition map in the hero, a scroll-driven Digital Presence
Stack with a section-aware layer bar, and the Where are you stuck? diagnostic."""
from p3lib import (C, E, S, L, PG, icon, eyebrow, check, sec_head, section, cards, steps, panel, split, note, evidence,
                   svc_cards, diagnostic, lab_cards, work_cards, build_concept, LAYER_OF, LAYER_ICON, cta_band)

CFG = {"k": "A", "name": "Original, Evolved", "dir": "phase-3/original-evolved"}


def layer_bar(ctx, home=False, current=None):
    items = ""
    for l in C["stack"]:
        href = f"#{l['id']}" if home else ctx.svc(l["service"])
        cur = ' aria-current="true"' if current == l["id"] else ""
        items += f'<li><a href="{href}" data-l="{l["id"]}"{cur}><span class="lb-n">{l["n"]}</span>{E(l["name"])}</a></li>'
    return f'<nav class="lbar" aria-label="The Digital Presence Stack"><div class="container lbar-in"><span class="lbar-t">Digital Presence Stack</span><ol>{items}</ol></div></nav>'


def recog_map(ctx):
    au = {x["id"]: x for x in C["audiences"]}
    nodes = [("people", 96, 92, "users"), ("search", 430, 150, "search"), ("ai", 150, 360, "spark")]
    paths = {"people": "M260 220 C 200 180, 150 140, 96 92", "search": "M260 220 C 330 200, 380 170, 430 150", "ai": "M260 220 C 230 290, 190 330, 150 360"}
    g = "".join(f'<path class="rm-l" d="{paths[n]}"/><path class="rm-p rm-p-{n}" d="{paths[n]}"/>' for n, _, _, _ in nodes)
    nd = "".join(f'<div class="rm-n" data-n="{n}" style="left:{x / 5.2:.2f}%;top:{y / 4.4:.2f}%"><span class="rm-ic">{icon(ic)}</span><b>{E(au[n]["name"])}</b></div>' for n, x, y, ic in nodes)
    lst = "".join("<li>%s: %s</li>" % (E(x["name"]), E(x["line"])) for x in C["audiences"])
    return f"""<figure class="rmap" aria-labelledby="rm-cap">
  <div class="rm-box" aria-hidden="true"><svg viewBox="0 0 520 440">{g}<circle class="rm-halo" cx="260" cy="220" r="62"/></svg>
  <div class="rm-core"><img src="{ctx.asset('logo-icon-128.png')}" alt="" width="56" height="56"><span>Your business</span></div>{nd}</div>
  <figcaption id="rm-cap"><span>Illustration: one brand, recognized by people, search engines, and AI systems.</span><button type="button" class="rm-pause" aria-pressed="false">Pause</button></figcaption>
  <ul class="sr">{lst}</ul>
</figure>"""


def home(ctx):
    h = C["hero"]; f = C["founder"]
    head = E(h["headline"]).replace(E(h["headlineHl"]), f'<span class="hl">{E(h["headlineHl"])}</span>')
    rm = recog_map(ctx)
    stk = "".join(f'<li class="sk" data-sk="{l["id"]}"><span class="sk-n">{l["n"]}</span><div class="icon-badge">{icon(LAYER_ICON[l["id"]])}</div><h3>{E(l["name"])}</h3><p>{E(l["short"])}</p></li>' for l in C["stack"])
    w = PG["websites"]; s = PG["seo"]; e = PG["entity"]; a = PG["ai"]; d = PG["domains"]; fw = C["work"][0]; art = C["article"]
    uses = "".join(f'<div class="value reveal"><div class="ic">{icon(["search", "doc", "link", "chart", "users", "spark", "shield", "trend"][i])}</div><div><h3>{E(u["name"])}</h3><p>{E(u["line"])}</p></div></div>' for i, u in enumerate(C["aiWork"]["uses"]))
    lay = lambda lid: f'<span class="ltag">{icon(LAYER_ICON[lid])}Layer {L[lid]["n"]} · {E(L[lid]["name"])}</span>'
    ins = cards([dict(icon="spark", tag=art["kind"] + " · Draft", h=art["title"], p=art["dek"], href=ctx.to(art["slug"]), cta="Read the draft")] + [dict(icon=LAYER_ICON[i["layer"]], tag=i["kind"] + " · Planned", h=i["title"], p="Not yet published.") for i in C["insights"]["items"][:2]], 3)
    return f"""
<section class="hero hero-a">
  <div class="container hero-split">
    <div class="hero-inner">
      {eyebrow(h['eyebrow'], True)}
      <h1>{head}</h1>
      <p class="lead">{E(h['support'])}</p>
      <div class="btn-row"><a href="{ctx.to('contact/')}" class="btn btn-accent btn-lg">{E(h['cta1'])}</a><a href="{ctx.to('services/')}" class="btn btn-on-dark btn-lg">{E(h['cta2'])}</a></div>
      <div class="hero-trust">{icon('check', '2.4')} {E(h['founder'])}</div>
    </div>
    {rm}
  </div>
</section>
{layer_bar(ctx, True)}

{section('stack', sec_head('The Digital Presence Stack', 'Domain, website, search, entity, AI.', C['stackReinforce']) + f'<ol class="sks" data-stack>{stk}</ol><p class="center v3-more">{E(C["company"]["originalModel"])}</p>', True)}

{section('services', sec_head('What we do', 'Five services. One digital presence.', C['company']['descriptionLong']) + svc_cards(ctx))}

{section('stuck', diagnostic(ctx), True)}

{section('domain', split(lay('domain') + sec_head('', S['domains']['h'], '', False) + f'<p class="section-lead">{E(d["lead"])}</p>' + steps(d['steps'], 'steps steps-2') + f'<div class="btn-row"><a class="btn btn-accent" href="{ctx.svc("domains")}">Domain acquisition and brokerage</a><a class="btn btn-ghost" href="{ctx.to("how-we-buy-domains/")}">How we buy domains</a></div>', panel("What's included", d['includes'][:7], f'<p class="pnote">{E(d["terms"])}</p>')), layer='domain')}

{section('website', split(lay('website') + sec_head('', w['h1'], '', False) + f'<p class="section-lead">{E(w["lead"])}</p>' + check(S['websites']['check']) + f'<div class="btn-row"><a class="btn btn-accent" href="{ctx.svc("websites")}">Website design and development</a><a class="btn btn-ghost" href="{ctx.to("work/luckydomains-io/")}">See a case study</a></div>', panel('What a build includes', w['includes']), True), True, layer='website')}

{section('search', split(lay('search') + sec_head('', s['h1'], '', False) + f'<p class="section-lead">{E(s["lead"])}</p>' + check(S['seo']['check']) + f'<a class="btn btn-accent" href="{ctx.svc("seo")}">SEO and search visibility</a>', f'<div class="card reveal evid1"><div class="icon-badge navy">{icon("doc")}</div><span class="tag">Source: {E(C["evidenceGoogle"]["label"])}</span><p>{E(C["evidenceGoogle"]["line"])}</p><a class="link-arrow" href="{C["evidenceGoogle"]["url"]}">Read the source {icon("arrow", "2.4")}</a></div>'), layer='search')}

{section('entity', split(lay('entity') + sec_head('', e['h1'], '', False) + f'<p class="section-lead">{E(e["what"][0])}</p>' + f'<a class="btn btn-accent" href="{ctx.svc("entity")}">Entity SEO and digital identity</a>', f'<div class="grid grid-2 idg2"><div class="card card-sm reveal"><h3>For people</h3>{check(e["people"][:4])}</div><div class="card card-sm reveal"><h3>For businesses</h3>{check(e["business"][:4])}</div></div>', True), True, layer='entity')}

{section('ai', split(lay('ai') + sec_head('', 'Improve the evidence AI systems use to understand you.', '', False) + f'<p class="section-lead">{E(a["lead"])}</p>' + check(a['goals'][:4]) + f'<a class="btn btn-accent" href="{ctx.svc("ai")}">AI visibility and brand authority</a>', panel('What we will not promise', [C['notPromised'], C['noSecret']])), layer='ai')}

{section('work', sec_head('Selected work', 'Real work, with the evidence attached.', fw['noMetrics']) + work_cards(ctx, C['work'][:3]), True)}

{section('story', f'<div class="story-a reveal">{eyebrow("The Lucky Domains story")}<h2>{E(C["company"]["storyHeadline"])}</h2><p class="section-lead">{E(C["company"]["story"])}</p><a class="link-arrow" href="{ctx.to("about/")}">About Lucky Domains {icon("arrow", "2.4")}</a></div>')}

{section('ai-work', split(sec_head(C['aiWork']['title'], C['aiWork']['principle'], '', False) + f'<p class="section-lead">{E(C["aiWork"]["intro"])}</p><p>{E(C["aiWork"]["evidence"])}</p>', f'<div class="grid uses-a">{uses}</div>'), True)}

{section('founder', split(sec_head('Founder', C['company']['founderLine'], '', False) + f'<p class="section-lead">{E(f["bio"])}</p><p><strong>{E(C["company"]["accountability"])}</strong></p><div class="btn-row"><a class="btn btn-ghost" href="{ctx.to("founder/")}">About Ken</a><a class="btn btn-ghost" href="{f["kenashe"]}">KenAshe.ai</a></div>', f'<figure class="founder-card reveal"><img src="{ctx.asset(f["image"])}" alt="Ken Ashe, founder of Lucky Domains" width="460" height="460" loading="lazy"></figure>', True))}

{section('insights', sec_head('Insights', 'Plain-English thinking on search, identity, and AI.', C['insights']['label']) + ins, True)}
{cta_band(ctx, 'Build your digital presence.', None, C['hero']['cta1'])}"""


def hero_extra(ctx, key):
    lid = LAYER_OF.get(key)
    return f'<p class="ltag ltag-dark">{icon(LAYER_ICON[lid])}Layer {L[lid]["n"]} of 05 · {E(L[lid]["name"])}</p>' if lid else ""


def inner(ctx, key, hero, secs):
    return hero + layer_bar(ctx, False, LAYER_OF.get(key)) + "".join(s[2] for s in secs)


def build():
    build_concept(dict(CFG, home=home, inner=inner, hero_extra=hero_extra))
