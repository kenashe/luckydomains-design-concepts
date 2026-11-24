"""Phase 2 review landing page and comparison page. Neutral styling (shared/review.css)."""
from p2lib import C, E, write

STATEMENT = "These are proposed design directions only. They do not modify LuckyDomains.io, KenAshe.ai, production repositories, DNS, forms, or integrations."
PAGES = [("", "Home"), ("services/", "Services"), ("services/website-design/", "Website Design"), ("services/search-ai-visibility/", "Search & AI Visibility"),
         ("services/domain-identity/", "Domain & Identity"), ("work/", "Work")]
CONCEPTS = [
    {"k": "A", "dir": "original-evolved", "name": "Original, Evolved",
     "thesis": "The current Lucky Domains site, redesigned for 2027. Same white, green, and navy, same Plus Jakarta Sans headings, same direct founder-led service language, with a stronger hierarchy and diagrams that explain how the pieces fit.",
     "attrs": ["White and warm off-white", "Original full-color logo", "Plus Jakarta Sans and Inter", "Rounded cards and panels", "Closest to today's site"],
     "motion": "A presence card in the hero lights the five layers in order and pauses on hover, focus, or its Pause button. The Digital Presence Stack settles slab by slab as each step scrolls into the reading line. A Where are you stuck? diagnostic reveals a recommended starting point.",
     "best": "Moving to production with the least risk. Existing customers will recognize it, and it keeps the consultation path obvious.",
     "risk": "The safest direction is also the least distinctive. It modernizes the site without giving Lucky Domains a new visual signature."},
    {"k": "B", "dir": "editorial-authority", "name": "Editorial Authority",
     "thesis": "A respected strategy, web, and visibility studio that explains its thinking. Warm paper, ink navy, a serif and sans pairing, numbered chapters, annotated case studies, and insights given real space.",
     "attrs": ["Warm paper and ink", "Newsreader and Public Sans", "Chapters and margin notes", "Annotated evidence", "Built for articles"],
     "motion": "A hairline reading-progress bar and a section-aware contents rail on every inner page. A timeline of five eras of discovery fills as you read. A before-and-after site-structure view, and case-study annotations that highlight on hover, focus, or tap.",
     "best": "Building authority through writing: case studies, guides, and media credibility. Strongest for professional-services trust.",
     "risk": "It only works with good writing. Thin or infrequent articles would make it feel emptier than the others."},
    {"k": "C", "dir": "intelligent-presence", "name": "Intelligent Presence",
     "thesis": "The most interactive direction. A living presence map shows how a domain, a website, content, search, structured data, profiles, reviews, founders, and citations come together into one identity AI systems can recognize.",
     "attrs": ["Cool light ground", "Manrope throughout", "Interactive presence map", "Modular tiles", "Layer color coding"],
     "motion": "The map starts fragmented and settles into a recognized identity, then slowly tours one signal at a time, pausing on interaction. A problem selector lights the signals involved and names the service to start with. On the website page, an internal-link graph shows what each page links to.",
     "best": "Explaining entity, AI visibility, and identity work to visitors who learn by exploring. The clearest picture of how the layers connect.",
     "risk": "The most to build and maintain. The map must stay a teaching aid and not become a dashboard as content grows."},
]
ROWS = [
    ("Similarity to the current site", "Very high. Same palette, logo use, heading font, and plain service language.", "Moderate. Same message and green, but a new editorial voice and serif type.", "Moderate. Same palette and message, with a new interactive structure."),
    ("Immediate service clarity", "Highest. Headline, services menu, and Build your digital presence are visible at once.", "High. A numbered services index sits directly under the cover.", "High. The headline is clear in seconds; the map rewards a second look."),
    ("Website-design credibility", "Strong. A full section with both paths and eight foundations on the homepage.", "Strong. Presented as a feature with a before-and-after structure view.", "Strong. An internal-link graph shows structure working, not just described."),
    ("SEO credibility", "Strong, in familiar terms.", "Strongest. Room to explain the reasoning and show writing.", "Strong. Search shown as one signal among several."),
    ("AI-visibility credibility", "Clear and restrained. Explained with the stack and a no-guarantees note.", "Clear and well argued. The eras timeline explains why AI depends on earlier layers.", "Most vivid. The map shows what AI systems read, without implying a dashboard."),
    ("Domain-service visibility", "In the services menu, the diagnostic, the stack, and the domain page.", "In the services index, the first era, and the domain page.", "In the map, the problem selector, and the domain page."),
    ("Founder visibility", "Founder line in the hero, a concise founder section.", "A byline under the cover and a profile with a pull quote.", "Founder line in the hero and a short founder section."),
    ("Visual warmth", "Warm and approachable.", "Warmest. Paper, serif, and long-form rhythm.", "Cool and clean."),
    ("Interaction level", "Moderate.", "Low to moderate, reading-led.", "High, exploration-led."),
    ("Content requirements", "Moderate. Works with the copy that exists today.", "High. Needs real case studies and articles to stay alive.", "Moderate, plus relationship data for the map."),
    ("Case-study presentation", "Structured cards with clear headings.", "Long-form features with margin annotations tied to the source.", "Tiles tagged by the layers each project touched."),
    ("Accessibility implications", "Fewest custom widgets. Radios, a list, and a pausable card.", "Native controls, with high legibility at long reading lengths.", "Most custom widgets: SVG buttons, tabs, and a graph, each with a text equivalent."),
    ("Performance complexity", "Low.", "Low to moderate. One larger serif font file.", "Moderate. SVG generated in the browser, with no library."),
    ("Long-term maintainability", "Easiest. Most like the existing production code.", "Easy to maintain, demanding to keep current.", "Hardest. New signals or pages need map and graph data."),
    ("Mobile behavior", "Stack becomes a list; diagnostic and card stay usable.", "Rail becomes a chapter strip; reading stays comfortable.", "Map switches to a portrait layout; tabs become a grid."),
    ("Strengths", "Commercial clarity, low risk, fastest to ship.", "Authority, trust, and the best home for writing.", "Explains entities and AI visibility better than words alone."),
    ("Weaknesses", "Least distinctive.", "Least effective without ongoing content.", "Most effort to build and keep accurate."),
]


def page(path, title, body):
    r = "../" * (path.count("/") + 1)
    cur = lambda p: ' aria-current="page"' if p == path else ""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex,nofollow,noarchive">
<title>{E(title)} | Lucky Domains Phase 2 design concepts</title>
<meta name="description" content="Phase 2 redesign concepts for Lucky Domains. Review only, not the live site.">
<link rel="icon" href="{r}shared/assets/favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="{r}shared/assets/favicon-32.png">
<link rel="stylesheet" href="{r}shared/review.css">
<link rel="stylesheet" href="{r}phase-2/shared/review-p2.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="top">
  <a href="{r}phase-2/" aria-label="Lucky Domains, Phase 2 concepts"><img src="{r}shared/assets/logo-wordmark.png" alt="Lucky Domains" width="194" height="48"></a>
  <nav aria-label="Review"><a href="{r}phase-2/"{cur("")}>Phase 2 concepts</a><a href="{r}phase-2/comparison/"{cur("comparison/")}>Comparison</a><a href="{r}">Phase 1 archive</a></nav>
</header>
<main id="main">{body(r)}</main>
<footer class="bot"><p>{STATEMENT}</p><p>Design concept only. Not the live Lucky Domains website. Review site for Ken Ashe. Not indexed. Facts as of {E(C['asOf'])}. <a href="https://github.com/kenashe/luckydomains-design-concepts">Repository</a>.</p></footer>
</body></html>"""


def landing(r):
    cards = ""
    for c in CONCEPTS:
        base = f"{r}phase-2/{c['dir']}/"
        k = c["k"].lower()
        cards += f"""<article class="card">
  <a class="shot" href="{base}" tabindex="-1" aria-hidden="true"><img src="{r}phase-2/screenshots/{k}-home-desktop.jpg" alt="" width="1440" height="900" loading="lazy"><img class="shot-m" src="{r}phase-2/screenshots/{k}-home-mobile.jpg" alt="" width="375" height="760" loading="lazy"></a>
  <div class="card-b">
    <p class="k">Concept {c['k']}</p><h2>{E(c['name'])}</h2>
    <p class="thesis">{E(c['thesis'])}</p>
    <ul class="attrs">{"".join(f"<li>{E(a)}</li>" for a in c['attrs'])}</ul>
    <dl><div><dt>Motion and interaction</dt><dd>{E(c['motion'])}</dd></div><div><dt>Best suited for</dt><dd>{E(c['best'])}</dd></div><div><dt>Tradeoff</dt><dd>{E(c['risk'])}</dd></div></dl>
    <p class="go"><a class="btn" href="{base}">Explore concept {c['k']}<span class="sr">: {E(c['name'])}</span></a>
    <span class="more">{"".join(f'<a href="{base}{p}">{E(t)}</a>' for p, t in PAGES[1:])}</span></p>
  </div>
</article>"""
    stack = "".join(f"<li><b>{E(l['name'])}</b> {E(l['line'])}</li>" for l in C["stack"])
    svcs = "".join(f"<li>{E(s['name'])}</li>" for s in C["services"])
    return f"""
<section class="intro">
  <p class="k">Phase 2 · {E(C['asOf'])}</p>
  <h1>Phase 2 redesign concepts</h1>
  <p class="lead">Three new, light directions for LuckyDomains.io. They correct the business direction of Phase 1 and share one positioning, one set of services, and one content file, so the comparison is about design.</p>
  <p class="state">{STATEMENT}</p>
</section>
<section class="p2-why" aria-labelledby="why-h">
  <h2 id="why-h">Why Phase 2</h2>
  <p>Phase 1 moved too far from the commercial business. It put AI experiments and a venture-studio identity at the center, when the work customers actually buy is websites, search, identity, and domains. Phase 2 starts again from the current light site and its commercial clarity, then brings the message up to date for a discovery environment shaped by AI.</p>
  <div class="p2-cols">
    <div><h3>Shared positioning</h3><p class="pos"><q>{E(C['company']['description'])}</q></p><p>{E(C['company']['long'])}</p></div>
    <div><h3>The Digital Presence Stack</h3><ol class="p2-stack">{stack}</ol></div>
    <div><h3>Five core services</h3><ul class="p2-svcs">{svcs}</ul><p>AI is explained as a change in how the work is done (AI-powered execution with human accountability) and in where brands need to be recognized. Ken's agent experiments appear only as a small supporting section.</p></div>
  </div>
</section>
<section class="cards" aria-label="Concepts">{cards}</section>
<section class="p2-ref" aria-labelledby="ref-h">
  <h2 id="ref-h">The current site, for reference</h2>
  <p>The live LuckyDomains.io homepage, captured read-only on {E(C['asOf'])}. Phase 2 starts from this site's commercial clarity.</p>
  <div class="p2-ref-g"><figure><img src="{r}phase-2/screenshots/current-home-desktop.jpg" alt="The current live LuckyDomains.io homepage at desktop width" width="1440" height="900" loading="lazy"><figcaption>Desktop</figcaption></figure><figure><img src="{r}phase-2/screenshots/current-home-mobile.jpg" alt="The current live LuckyDomains.io homepage at mobile width" width="375" height="760" loading="lazy"><figcaption>Mobile</figcaption></figure></div>
</section>
<section class="next">
  <h2>How to review</h2>
  <ol><li>Open each concept at desktop width, then on a phone.</li><li>Ask whether a business owner would understand what Lucky Domains does within five seconds.</li><li>Find website design, SEO, and domain acquisition from the homepage in each one.</li><li>Try each concept's interaction: the diagnostic (A), the reading rail and before-and-after view (B), and the presence map (C).</li><li>Read the <a href="{r}phase-2/comparison/">comparison</a>.</li></ol>
  <p>Phase 1 (Venture Lab, The Register, Namespace, Venture Lab v2, and the production candidate) stays available as an <a href="{r}">archive</a>. It is not part of this comparison.</p>
</section>"""


def comparison(r):
    head = "".join(f'<th scope="col"><span>Concept {c["k"]}</span>{E(c["name"])}</th>' for c in CONCEPTS)
    rows = "".join(f'<tr><th scope="row">{E(a)}</th><td data-c="A: Original, Evolved">{E(b)}</td><td data-c="B: Editorial Authority">{E(c)}</td><td data-c="C: Intelligent Presence">{E(d)}</td></tr>' for a, b, c, d in ROWS)
    shots = [("home-desktop", "Home, desktop"), ("home-mobile", "Home, mobile"), ("services", "Services"), ("website", "Website Design"), ("search", "Search & AI Visibility"), ("domains", "Domain & Identity"), ("work", "Work"), ("interaction", "Interaction")]
    gal = ""
    for c in CONCEPTS:
        k = c["k"].lower()
        figs = "".join(f'<figure><a href="{r}phase-2/screenshots/{k}-{f}.jpg"><img src="{r}phase-2/screenshots/{k}-{f}.jpg" alt="Concept {c["k"]}, {E(c["name"])}: {E(t)}" width="{375 if f == "home-mobile" else 1440}" height="{760 if f == "home-mobile" else 900}" loading="lazy"></a><figcaption>{E(t)}</figcaption></figure>' for f, t in shots)
        gal += f'<h3>Concept {c["k"]}: {E(c["name"])}</h3><div class="p2-gal">{figs}</div>'
    return f"""
<section class="intro">
  <p class="k">Phase 2 · Side by side</p>
  <h1>Comparison</h1>
  <p class="lead">Seventeen questions asked of each direction. All three share the same positioning, services, and facts, so these notes are about design. They are observations to argue with, not a decision.</p>
  <p class="state">{STATEMENT}</p>
</section>
<section class="tbl" aria-label="Comparison table"><table><thead><tr><th scope="col"><span class="sr">Criterion</span></th>{head}</tr></thead><tbody>{rows}</tbody></table></section>
<section class="p2-ref" aria-labelledby="ref-h"><h2 id="ref-h">Reference: the current homepage</h2>
<div class="p2-ref-g"><figure><img src="{r}phase-2/screenshots/current-home-desktop.jpg" alt="The current live LuckyDomains.io homepage at desktop width" width="1440" height="900" loading="lazy"><figcaption>Live LuckyDomains.io, desktop, captured {E(C['asOf'])}</figcaption></figure><figure><img src="{r}phase-2/screenshots/current-home-mobile.jpg" alt="The current live LuckyDomains.io homepage at mobile width" width="375" height="760" loading="lazy"><figcaption>Mobile</figcaption></figure></div></section>
<section class="gal p2-gals" aria-labelledby="g-h"><h2 id="g-h">Screenshots</h2>{gal}</section>
<section class="next"><h2>Shared by all three</h2>
<ul><li>One positioning: {E(C['company']['description'])}</li><li>The Domain, Website, Search, Entity, AI progression, told differently in each.</li><li>Five services, with website design and SEO given full weight and domain acquisition always one click away.</li><li>No guarantees of rankings, AI citations, or Knowledge Panels.</li><li>Agent identity presented as emerging research on the domain page, not as an offer.</li><li>Only public evidence in case studies, and a labeled layout demonstration where a client's details cannot be shown.</li><li>Noindex, forms that send nothing, keyboard access, and a complete experience without JavaScript or motion.</li></ul>
<p><a class="btn" href="{r}phase-2/">Back to the Phase 2 concepts</a></p></section>"""


def build():
    write("phase-2/index.html", page("", "Phase 2 concepts", landing))
    write("phase-2/comparison/index.html", page("comparison/", "Comparison", comparison))
