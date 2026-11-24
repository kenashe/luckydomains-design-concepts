"""Neutral review landing page and comparison page."""
from lib import C, E, Ctx, write, NOTICE

STATEMENT = "These are proposed design directions only. They do not modify LuckyDomains.io, KenAshe.ai, production repositories, DNS, forms, or integrations."
CONCEPTS = [
    {"k": "A", "dir": "concept-a-venture-lab", "name": "Venture Lab", "shot": "a",
     "thesis": "A premium digital venture studio meets an experimental technology lab. Dark, precise, and built from real evidence: transaction payloads, ENS records, status labels.",
     "attrs": ["Dark graphite", "Monospace metadata", "Asymmetric, editorial", "Evidence as imagery", "Quietly technical"],
     "motion": "Cursor-responsive dot field, an operating-status stack that cycles and pauses, a section-aware progression rail, proximity spotlight on venture cards, and scroll depth on artifacts.",
     "best": "Signalling that Lucky Domains builds unusual internet businesses, to technical, crypto-native, and investor-minded visitors.",
     "risk": "The furthest from today's site. Brokerage clients who expect a conventional services firm may find it less approachable, and the logo's navy needs a reversed treatment on dark."},
    {"k": "B", "dir": "concept-b-the-register", "name": "The Register", "shot": "b",
     "thesis": "A founder-owned company's journal of record. Warm paper, ink, and one green, with ventures entered like a register and told as editorial features.",
     "attrs": ["Warm paper, light", "Serif editorial type", "Register and features", "Original logo, full color", "Calm and literate"],
     "motion": "Variable-font headlines whose weight follows scroll, a running head with reading progress and section-aware title, a history line that draws as you scroll, cursor-following preview plates, and a page tone that shifts between paper and wash.",
     "best": "Trust and longevity: a holding company with a record. The most comfortable home for domain brokerage clients and for media.",
     "risk": "Reads less like a technology lab. It depends on good writing: thin copy would make it feel empty faster than the other two."},
    {"k": "C", "dir": "concept-c-namespace", "name": "Namespace", "shot": "c",
     "thesis": "Everything the company does has an address. A spatial, interface-like site built on the brand's own navy, green, and mint, with an interactive map of how names, identity, agents, and ventures connect.",
     "attrs": ["Brand navy and mint", "Interactive map", "Modular tiles", "Address-bar navigation", "Closest to current palette"],
     "motion": "A drifting, cursor-aware constellation map with selectable relationships, an address bar that tracks the section in view, cards that rearrange when filtered, a layer stack that opens on scroll, and marching route lines.",
     "best": "Showing how the parts relate, and growing with the portfolio. Each new venture is a new node rather than a new page design.",
     "risk": "The most to build and maintain. The map needs care as nodes are added, and the interface metaphor could feel like a product rather than a company if pushed further."},
]
V2 = {"dir": "concept-a-venture-lab-v2", "orig": "concept-a-venture-lab",
      "summary": "A refinement of Concept A based on review feedback, not a fourth direction. Same dark foundation, logo treatment, headline, operating status, and evidence-led tone, recomposed so a nontechnical visitor or a domain client can follow it.",
      "changes": ["A brighter, underlined \u201cNot the boundary.\u201d and larger, less tracked labels throughout",
                  "A Build, Operate, Acquire strip right after the hero",
                  "ZeroHuman as the single featured venture, with a five-step order diagram and its current limit stated",
                  "\u201cFounded by Ken Ashe. Read the full build record on KenAshe.ai.\u201d next to the featured venture",
                  "Clear type and status labels, and a Ventures page grouped into four kinds of record",
                  "The Domain Desk as a warm light section carrying the original full-color logo",
                  "Calmer motion after the hero, and a homepage about 22 to 24 percent shorter"]}
V2_ROWS = [
    ("Hero clarity", "Strong headline. \u201cNot the boundary.\u201d is dim gray and can read as disabled.", "Second line in warm gray at about 85 percent brightness with a thin green underline. Support copy names brokerage."),
    ("Founder visibility", "Ken appears in a portrait strip near the end of the homepage.", "One line beside the featured venture links to the Founder page and the build record. The portrait stays on the Founder page."),
    ("Company-model clarity", "The four-stage story explains the evolution, but not what the company does today.", "A Build, Operate, Acquire strip answers that within the first scroll."),
    ("Text readability", "11 to 12 pixel monospace labels with wide tracking. Some secondary text sits near the contrast floor.", "Labels at 12 to 13.5 pixels, tracking reduced, monospace kept for metadata only, secondary text brightened."),
    ("Domain-business treatment", "A dark full-width band, partway down the page.", "A warm light section with the original logo, the four-step process, the fee terms, and two calls to action. Mirrored on Services."),
    ("Portfolio taxonomy", "Status chips carry the meaning. \u201cExperiment\u201d is shown beside status.", "Every record shows type and status separately. Ventures are grouped: operating ventures, experiments, internal systems, active services."),
    ("Evidence presentation", "Raw payloads and ENS records are the first visual on each card.", "A plain process diagram first, then the selected result, then the raw evidence (collapsed on the homepage, open on detail pages)."),
    ("Motion intensity", "Dot field, cycling stack, sticky rail, proximity glow on every card, and artifact parallax.", "Dot field and cycling stack in the hero, a spotlight inside the featured venture only, a one-time flow draw, and a scroll-linked progression line. No global pointer tracking, no parallax."),
    ("Mobile behavior", "Status panel starts well below the first screen. Long stacked cards.", "Smaller headline, tighter hero, first status row inside the first screen at 375 pixels, compact flow and footer."),
    ("Homepage length", "7,487 px at 1440 wide. 10,878 px at 375 wide.", "5,697 px at 1440 wide (24 percent shorter). 8,537 px at 375 wide (22 percent shorter)."),
    ("Production readiness", "A convincing direction study. The footer is a logo gallery.", "Closer to buildable: a production-style footer, clearer content model, fewer bespoke effects to maintain."),
    ("Risks and tradeoffs", "Most mysterious and most distinctive.", "Slightly less mysterious. The light section is a deliberate break that must stay disciplined, and the taxonomy needs upkeep as builds change status."),
]
ROWS = [
    ("Overall brand impression", "Experimental lab with a serious operator behind it.", "Established, literate, founder-owned company of record.", "Clear, friendly, systems-minded company with a product feel."),
    ("Light versus dark", "Dark throughout.", "Light throughout (warm paper).", "Light page with navy feature surfaces."),
    ("Venture-studio credibility", "Strongest. Evidence and status are the visual language.", "Strong, in a quieter register. Ventures read as documented features.", "Strong on structure. Shows the portfolio as a connected system."),
    ("Fit with the current logo", "Needs the reversed treatment (navy becomes warm white). Original shown in the footer.", "Best fit. Original full-color logo sits in the masthead untouched.", "Natural fit. Palette is taken directly from the logo. Icon in the header, wordmark in the footer."),
    ("Cross-linking to KenAshe.ai", "Per-venture build-log links, plus a founder strip and footer column.", "Strongest narrative link: every entry ends in \"Continue reading\" on KenAshe.ai.", "Most explicit structurally: a two-address diagram and a build-log tile on every record."),
    ("Domain brokerage treatment", "Full-width band on the home page, first service, in the hero status stack and header call to action.", "\"Standing notice\" section, Chapter I of services, entry No. 04 in the register.", "Navy \"root\" module on home and services, a node on the map, first route in contact."),
    ("Motion intensity", "Medium to high, but ambient. Cursor-led.", "Low to medium. Scroll-led and typographic.", "Medium to high. Interaction-led."),
    ("Accessibility implications", "Dark contrast is tuned but leaves less margin. Metadata is small monospace. Cycling stack has a pause control.", "Highest baseline legibility. Fewest moving parts. Native details elements for the register.", "The map is an SVG with focusable nodes and a full list equivalent. Most custom widgets to keep accessible."),
    ("Implementation complexity", "Medium. One canvas effect, the rest is CSS and observers.", "Low to medium. Mostly typography and layout.", "Highest. SVG map, card reordering, view switching."),
    ("Long-term maintainability", "Good. New ventures are new cards with a metadata table.", "Best. New ventures are new entries. Almost no bespoke components.", "Fair. Each new node needs map coordinates and a layout check on mobile."),
    ("Likely content requirements", "Real artifacts for each venture: payloads, screenshots, diagrams.", "Well-edited prose, a standfirst and a figure for each venture.", "Short summaries plus relationship data. Less prose, more structure."),
    ("Strengths", "Distinctive, memorable, and the clearest break from an agency look.", "Timeless, trustworthy, and the easiest to keep honest and current.", "Explains the whole company at a glance and scales with the portfolio."),
    ("Weaknesses", "May read as niche to mainstream domain buyers. Dark-only.", "Least novel interaction. Could be mistaken for a publication.", "More engineering, and the risk of interface for its own sake."),
]


def page(path, title, body):
    r = "../" * path.count("/") or "./"
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex,nofollow,noarchive">
<title>{E(title)} | Lucky Domains proposed redesign concepts</title>
<meta name="description" content="Three proposed redesign concepts for Lucky Domains. Review only, not the live site.">
<link rel="icon" href="{r}shared/assets/favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="{r}shared/assets/favicon-32.png">
<link rel="stylesheet" href="{r}shared/review.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="top">
  <a href="{r}" aria-label="Lucky Domains, proposed redesign concepts"><img src="{r}shared/assets/logo-wordmark.png" alt="Lucky Domains" width="194" height="48"></a>
  <nav aria-label="Review"><a href="{r}"{' aria-current="page"' if path == '' else ''}>Concepts</a><a href="{r}comparison/"{' aria-current="page"' if path else ''}>Comparison</a></nav>
</header>
<main id="main">{body(r)}</main>
<footer class="bot"><p>{STATEMENT}</p><p>Review site for Ken Ashe. Not indexed. Facts as of {E(C['asOf'])}. Source and notes: <a href="https://github.com/kenashe/luckydomains-design-concepts">repository</a>.</p></footer>
</body></html>"""


def landing(r):
    cards = ""
    for c in CONCEPTS:
        attrs = "".join(f"<li>{E(a)}</li>" for a in c["attrs"])
        cards += f"""<article class="card">
  <a class="shot" href="{r}{c['dir']}/" tabindex="-1" aria-hidden="true"><img src="{r}screenshots/{c['shot']}-home-desktop.jpg" alt="" width="1440" height="900" loading="lazy"><img class="shot-m" src="{r}screenshots/{c['shot']}-home-mobile.jpg" alt="" width="375" height="760" loading="lazy"></a>
  <div class="card-b">
    <p class="k">Concept {c['k']}</p>
    <h2>{E(c['name'])}</h2>
    <p class="thesis">{E(c['thesis'])}</p>
    <ul class="attrs">{attrs}</ul>
    <dl>
      <div><dt>Motion and interaction</dt><dd>{E(c['motion'])}</dd></div>
      <div><dt>Best suited for</dt><dd>{E(c['best'])}</dd></div>
      <div><dt>Tradeoff</dt><dd>{E(c['risk'])}</dd></div>
    </dl>
    <p class="go"><a class="btn" href="{r}{c['dir']}/">Explore concept {c['k']}<span class="sr">: {E(c['name'])}</span></a>
    <span class="more"><a href="{r}{c['dir']}/ventures/">Ventures</a><a href="{r}{c['dir']}/services/">Services</a><a href="{r}{c['dir']}/about/">About</a><a href="{r}{c['dir']}/founder/">Founder</a><a href="{r}{c['dir']}/news/">News</a><a href="{r}{c['dir']}/contact/">Contact</a></span></p>
  </div>
</article>"""
    return f"""
<section class="refine p2-banner" aria-labelledby="p2-h">
  <p class="k">Current round</p>
  <h2 id="p2-h">Phase 2: three light concepts for a digital presence studio</h2>
  <p class="lead">Phase 2 corrects the business direction: websites, search, digital identity, AI visibility, and domains. Everything below on this page is Phase 1, kept as an archive and not a finalist.</p>
  <p class="go"><a class="btn" href="{r}phase-2/">Open the Phase 2 concepts</a><a class="btn btn-l" href="{r}phase-2/comparison/">Phase 2 comparison</a></p>
</section>
<section class="intro">
  <p class="k">Phase 1 archive · Review, {E(C['asOf'])}</p>
  <h1>Proposed redesign concepts</h1>
  <p class="lead">Three complete directions for a future LuckyDomains.io, built on one shared set of facts so the differences are design, not content. These are review concepts, not the live site.</p>
  <p class="state">{STATEMENT}</p>
  <p class="pos">Positioning used in all three: <q>{E(C['company']['description'])}</q></p>
</section>
<section class="cards" aria-label="Concepts">{cards}</section>
<section class="refine" aria-labelledby="rf-h">
  <p class="k">Selected direction refinement</p>
  <h2 id="rf-h">Venture Lab v2</h2>
  <article class="card">
    <a class="shot" href="{r}{V2['dir']}/" tabindex="-1" aria-hidden="true"><img src="{r}screenshots/v2-home-desktop.jpg" alt="" width="1440" height="900" loading="lazy"><img class="shot-m" src="{r}screenshots/v2-home-mobile.jpg" alt="" width="375" height="760" loading="lazy"></a>
    <div class="card-b">
      <p class="thesis">{E(V2['summary'])}</p>
      <h3>What changed</h3>
      <ul class="chg">{"".join(f"<li>{E(x)}</li>" for x in V2['changes'])}</ul>
      <p class="state state-s">Neither the original Concept A nor v2 is production. No direction has been implemented.</p>
      <p class="go"><a class="btn" href="{r}{V2['dir']}/">Explore Venture Lab v2</a><a class="btn btn-l" href="{r}{V2['orig']}/">Original Concept A</a>
      <span class="more"><a href="{r}comparison/#v2">Original vs v2</a><a href="{r}{V2['dir']}/ventures/">Ventures</a><a href="{r}{V2['dir']}/services/">Services</a><a href="{r}{V2['dir']}/founder/">Founder</a></span></p>
    </div>
  </article>
</section>
<section class="refine" aria-labelledby="pc-h">
  <p class="k">Staging</p>
  <h2 id="pc-h">Production candidate</h2>
  <p class="lead">Venture Lab v2, ported to the production repository on a branch and exported here as a noindex staging copy with the contact form disabled. The live site is unchanged.</p>
  <p class="go"><a class="btn" href="{r}production-candidate/">Open the staged site</a><a class="btn btn-l" href="{r}production-candidate/review/">Review notes</a></p>
</section>
<section class="next">
  <h2>How to review</h2>
  <ol><li>Open each concept at desktop width, then on a phone.</li><li>Follow one venture from the home page to its detail page and out to KenAshe.ai.</li><li>Find domain brokerage from the home page in each one.</li><li>Read the <a href="{r}comparison/">side-by-side comparison</a>.</li></ol>
  <p>Every form is a mockup and sends nothing. No analytics are loaded. Fonts are self-hosted, so the pages make no third-party requests.</p>
</section>"""


def comparison(r):
    head = "".join(f'<th scope="col"><span>Concept {c["k"]}</span>{E(c["name"])}</th>' for c in CONCEPTS)
    rows = "".join(f'<tr><th scope="row">{E(a)}</th><td data-c="A: Venture Lab">{E(b)}</td><td data-c="B: The Register">{E(c)}</td><td data-c="C: Namespace">{E(d)}</td></tr>' for a, b, c, d in ROWS)
    shots = ""
    for c in CONCEPTS:
        shots += f"""<figure><a href="{r}{c['dir']}/ventures/"><img src="{r}screenshots/{c['shot']}-ventures-desktop.jpg" alt="Concept {c['k']}, {E(c['name'])}: ventures page" width="1440" height="900" loading="lazy"></a><figcaption>Concept {c['k']}: {E(c['name'])}, ventures page</figcaption></figure>"""
        shots += f"""<figure><a href="{r}{c['dir']}/"><img src="{r}screenshots/{c['shot']}-detail-desktop.jpg" alt="Concept {c['k']}, {E(c['name'])}: additional view" width="1440" height="900" loading="lazy"></a><figcaption>Concept {c['k']}: {E(c['name'])}, a second view</figcaption></figure>"""
    return f"""
<section class="intro">
  <p class="k">Side by side</p>
  <h1>Comparison</h1>
  <p class="lead">The same thirteen questions asked of each direction. The notes are observations to argue with, not a decision.</p>
  <p class="state">{STATEMENT}</p>
</section>
<section class="tbl" aria-label="Comparison table"><table><thead><tr><th scope="col"><span class="sr">Criterion</span></th>{head}</tr></thead><tbody>{rows}</tbody></table></section>
<section class="gal" aria-label="Screenshots"><h2>Ventures page and a second view, each concept</h2><div class="gal-g">{shots}</div></section>
<section class="tbl v2c" id="v2" aria-labelledby="v2-h"><p class="k">Selected direction refinement</p><h2 id="v2-h">Venture Lab: original vs v2</h2>
<p class="lead">v2 refines Concept A after review. It is not a fourth direction, and the table above still compares the three original concepts as they were.</p>
<table><thead><tr><th scope="col"><span class="sr">Criterion</span></th><th scope="col"><span>Concept A</span>Original</th><th scope="col"><span>Concept A</span>v2 refinement</th></tr></thead>
<tbody>{"".join(f'<tr><th scope="row">{E(a)}</th><td data-c="Original">{E(b)}</td><td data-c="v2">{E(c)}</td></tr>' for a, b, c in V2_ROWS)}</tbody></table>
<div class="gal-g gal-2"><figure><a href="{r}concept-a-venture-lab/"><img src="{r}screenshots/a-home-desktop.jpg" alt="Original Concept A homepage" width="1440" height="900" loading="lazy"></a><figcaption>Original Concept A</figcaption></figure><figure><a href="{r}concept-a-venture-lab-v2/"><img src="{r}screenshots/v2-home-desktop.jpg" alt="Venture Lab v2 homepage" width="1440" height="900" loading="lazy"></a><figcaption>Venture Lab v2</figcaption></figure>
<figure><a href="{r}concept-a-venture-lab-v2/#featured"><img src="{r}screenshots/v2-zerohuman-desktop.jpg" alt="Venture Lab v2 ZeroHuman page with the order diagram" width="1440" height="900" loading="lazy"></a><figcaption>v2: ZeroHuman file with the order diagram</figcaption></figure><figure><a href="{r}concept-a-venture-lab-v2/#domain-desk"><img src="{r}screenshots/v2-domain-desk-desktop.jpg" alt="Venture Lab v2 warm Domain Desk section" width="1440" height="900" loading="lazy"></a><figcaption>v2: the warm Domain Desk</figcaption></figure></div>
<h3>Logo treatments used in Venture Lab</h3>
<p>Moved here from the original concept's footer. Only color changes. Geometry is untouched.</p>
<div class="logos"><figure><span class="chip chip-l"><img src="{r}shared/assets/logo-wordmark.png" alt="Original Lucky Domains logo" width="161" height="40" loading="lazy"></span><figcaption>Original, full color. Used on the light Domain Desk.</figcaption></figure>
<figure><span class="chip chip-d"><img src="{r}shared/assets/logo-wordmark-reversed.png" alt="Reversed Lucky Domains logo" width="161" height="40" loading="lazy"></span><figcaption>Reversed, concept treatment. Header and footer on dark.</figcaption></figure>
<figure><span class="chip chip-d"><img src="{r}shared/assets/logo-icon-reversed-128.png" alt="Lucky Domains icon, reversed" width="40" height="40" loading="lazy"></span><figcaption>Icon, for compact use.</figcaption></figure>
<figure><span class="chip chip-l"><img src="{r}shared/assets/favicon-32.png" alt="Lucky Domains favicon" width="32" height="32" loading="lazy"></span><figcaption>Favicon, unchanged from production.</figcaption></figure></div>
</section>
<section class="next"><h2>Shared by all three</h2>
<ul><li>The same content file, so facts cannot drift between concepts.</li><li>The original Lucky Domains logo, with any recolored treatment labeled as a concept treatment.</li><li>Domain acquisition and brokerage visible from the home page, the services page, and contact.</li><li>Venture summaries that link out to the full build record on KenAshe.ai.</li><li>Keyboard access, visible focus, skip links, and a complete experience with motion reduced.</li><li>The notice: {NOTICE}</li></ul>
<p><a class="btn" href="{r}">Back to the concepts</a></p></section>"""


def build():
    write("index.html", page("", "Proposed redesign concepts", landing))
    write("comparison/index.html", page("comparison/", "Comparison", comparison))
