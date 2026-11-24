"""Version 3, Concept B: Original, Editorial. The production components arranged for reading:
an editorial hero, an evolution timeline, case studies and insights given room, a contents rail
with reading progress on every inner page, and a before-and-after identity view."""
from p3lib import (C, E, S, L, PG, icon, eyebrow, check, sec_head, section, cards, steps, panel, split, note, evidence,
                   lab_cards, work_cards, build_concept, LAYER_ICON, cta_band)

CFG = {"k": "B", "name": "Original, Editorial", "dir": "phase-3/editorial"}


def ba_block():
    b = C["beforeAfter"]
    col = lambda k: f'<div class="bv-c" data-state="{k}"><h3>{E(b[k]["label"])}</h3><dl>{"".join("<div><dt>%s</dt><dd>%s</dd></div>" % (E(a), E(v)) for a, v in b[k]["rows"])}</dl></div>'
    return f'<div class="bv" data-bv><div class="ba-bar" role="group" aria-label="Show state"><button type="button" class="bv-b" data-show="before" aria-pressed="true">Before</button><button type="button" class="bv-b" data-show="after" aria-pressed="false">After</button></div><div class="bv-g" aria-live="polite">{col("before")}{col("after")}</div><p class="bv-cap">{E(b["caption"])}</p></div>'


def annotated_case(ctx):
    w = C["work"][0]; marks = {0: "1", 1: "2", 3: "3", 5: "4"}
    done = "".join("<li>%s%s</li>" % (E(x), (' <button class="mk" type="button" aria-describedby="an-%s" data-mk="%s">%s</button>' % (marks[i], marks[i], marks[i])) if i in marks else "") for i, x in enumerate(w["done"]))
    notes = "".join(f'<li id="an-{a["n"]}" data-note="{a["n"]}"><span>{a["n"]}</span>{E(a["note"])}</li>' for a in C["annotations"])
    return f'<div class="case-b"><ul class="check done">{done}</ul><div class="notes" role="group" aria-label="From the public decision log"><p class="notes-h">From the decision log</p><ol>{notes}</ol><a class="link-arrow" href="{w["evidence"][1][1]}">Read DECISIONS.md {icon("arrow", "2.4")}</a></div></div>'


def home(ctx):
    h = C["hero"]; f = C["founder"]; fw = C["work"][0]; art = C["article"]; w = PG["websites"]
    idx = "".join(f'<li><a href="{ctx.svc(s["id"])}"><span>{i:02d}</span>{E(s["name"])}</a></li>' for i, s in enumerate(C["services"], 1))
    era = "".join(f'<li class="era" data-era><span class="era-w">{E(l["name"])}</span><div><p class="era-n">Layer {l["n"]}</p><h3>{E(l["line"])}</h3><p>{E(l["detail"])}</p><a class="link-arrow" href="{ctx.svc(l["service"])}">{E(S[l["service"]]["name"])} {icon("arrow", "2.4")}</a></div></li>' for l in C["stack"])
    rows = "".join(f'<article class="row reveal"><span class="row-n">{i:02d}</span><div><span class="tag">{E(s["tag"])}</span><h3><a href="{ctx.svc(s["id"])}">{E(s["name"])}</a></h3><p>{E(s["short"])}</p></div>{check(s["check"])}</article>' for i, s in enumerate(C["services"], 1))
    planned = "".join(f'<li><span class="tag">{E(i["kind"])} · Planned</span><b>{E(i["title"])}</b></li>' for i in C["insights"]["items"])
    uses = "".join(f'<li><b>{E(u["name"])}.</b> {E(u["line"])}</li>' for u in C["aiWork"]["uses"])
    return f"""
<section class="hero hero-b">
  <div class="container hero-inner">
    {eyebrow(h['eyebrow'], True)}
    <h1>{E(h['headline'])}</h1>
    <div class="hb-cols"><p class="lead">{E(h['support'])}</p>
    <div><div class="btn-row"><a href="{ctx.to('contact/')}" class="btn btn-accent btn-lg">{E(h['cta1'])}</a><a href="{ctx.to('services/')}" class="btn btn-on-dark btn-lg">{E(h['cta2'])}</a></div>
    <p class="byline"><img src="{ctx.asset(f['image'])}" alt="" width="44" height="44">{E(h['founder'])}</p></div></div>
    <ol class="hb-idx" aria-label="Services">{idx}</ol>
  </div>
</section>

<section class="section evo" id="evolution"><div class="container">
  <div class="sec-head reveal">{eyebrow('The Lucky Domains story')}<h2>{E(C['company']['storyHeadline'])}</h2><p class="section-lead">{E(C['company']['story'])}</p></div>
  <ol class="eras" data-eras>{era}</ol>
  <p class="pull">{E(C['stackReinforce'])}</p>
</div></section>

{section('services', sec_head('Services', 'Five services, in the order a presence is built.', C['company']['descriptionLong'], False) + f'<div class="rows">{rows}</div>', True)}

{section('identity', split(sec_head('Before and after', 'What a consistent identity looks like.', '', False) + f'<p class="section-lead">{E(PG["entity"]["what"][1])}</p><a class="btn btn-ghost" href="{ctx.svc("entity")}">Entity SEO and digital identity</a>', ba_block()))}

{section('case', sec_head('Case study', fw['title'], fw['summary'], False) + annotated_case(ctx) + f'<p class="v3-more"><a class="btn btn-accent" href="{ctx.to("work/luckydomains-io/")}">Read the full case study</a> <a class="btn btn-ghost" href="{ctx.to("work/")}">All work</a></p>', True)}

{section('websites', split(sec_head(S['websites']['name'], w['h1'], '', False) + f'<p class="section-lead">{E(w["lead"])}</p>' + "".join(f'<p>{E(x)}</p>' for x in w['intro']) + f'<a class="btn btn-accent" href="{ctx.svc("websites")}">Website design and development</a>', panel('What a build includes', w['includes'])))}

{section('search', sec_head('Search and AI visibility', 'SEO is expanding, not disappearing.', PG['seo']['lead'], False) + evidence(ctx) + note(C['notPromised'], 'note', 'What we will not promise.'), True)}

{section('insights', f'<div class="mag">' + f'<article class="mag-lead reveal"><span class="tag">{E(art["kind"])} · {E(art["status"])}</span><h2><a href="{ctx.to(art["slug"])}">{E(art["title"])}</a></h2><p class="section-lead">{E(art["dek"])}</p><a class="link-arrow" href="{ctx.to(art["slug"])}">Read the draft {icon("arrow", "2.4")}</a></article>' + f'<div class="mag-side reveal">{eyebrow("Insights")}<p class="mag-note">{E(C["insights"]["label"])}</p><ul class="mag-l">{planned}</ul><a class="link-arrow" href="{ctx.to("insights/")}">All insights {icon("arrow", "2.4")}</a></div></div>')}

{section('method', split(sec_head(C['aiWork']['title'], C['aiWork']['principle'], '', False) + f'<p class="section-lead">{E(C["aiWork"]["intro"])}</p><p>{E(C["aiWork"]["evidence"])}</p>', f'<ul class="notes-l reveal">{uses}</ul>'), True)}

{section('founder', f'<div class="byl reveal"><img src="{ctx.asset(f["image"])}" alt="Ken Ashe, founder of Lucky Domains" width="200" height="200" loading="lazy"><div>{eyebrow("Founder")}<h2>{E(C["company"]["founderLine"])}</h2><p class="section-lead">{E(f["bio"])}</p><blockquote class="v3-quote"><p>{E(C["company"]["accountability"])}</p></blockquote><div class="btn-row"><a class="btn btn-ghost" href="{ctx.to("founder/")}">About Ken</a><a class="btn btn-ghost" href="{f["kenashe"]}">KenAshe.ai</a></div></div></div>')}
{cta_band(ctx, 'Build your digital presence.', None, C['hero']['cta1'])}"""


def inner(ctx, key, hero, secs):
    if key == "case":
        secs = [(i, lab, annotated_section(ctx) if i == "done" else h) for i, lab, h in secs]
    if key == "article":
        toc = [(f"a{n}", s[0]) for n, s in enumerate(C["article"]["sections"], 1)] + [("sources", "Sources")]
    else:
        toc = [(i, lab) for i, lab, _ in secs]
    rail = '<nav class="rail" aria-label="On this page"><p class="rail-h">On this page</p><ol>' + "".join(f'<li><a href="#{i}" data-toc="{i}">{E(t)}</a></li>' for i, t in toc) + "</ol></nav>"
    return hero + f'<div class="b-wrap"><div class="container b-grid">{rail}<div class="b-flow">' + "".join(s[2] for s in secs) + "</div></div></div>"


def annotated_section(ctx):
    return section("done", sec_head("Work completed", "What changed, with the source for each.", "", False) + annotated_case(ctx))


def build():
    build_concept(dict(CFG, home=home, inner=inner))
