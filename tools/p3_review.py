"""Version 3 review landing page and comparison page (neutral styling from shared/review.css)."""
from p3lib import C, E, PAGES, write

STATEMENT = "These are proposed design directions only. They do not modify LuckyDomains.io, KenAshe.ai, production repositories, DNS, forms, or integrations."
NAMES = {"home": "Home", "services": "Services", "websites": "Website Design", "seo": "SEO", "ai": "AI Visibility", "entity": "Entity SEO", "domains": "Domains",
         "buy": "How we buy domains", "work": "Work", "case": "Case study", "about": "About", "founder": "Founder", "insights": "Insights", "article": "Research note", "news": "News & media", "contact": "Contact"}
CONCEPTS = [
    {"k": "A", "dir": "original-evolved", "name": "Original, Evolved",
     "thesis": "The production site, kept recognizable and modernized. Same navy hero, white and soft-grey bands, icon cards, green checks, numbered steps, green call-to-action band, and navy footer, with larger type, more room, and the three signature interactions.",
     "attrs": ["Closest to the current site", "Original stylesheet underneath", "Navy hero, white sections", "Layer bar that follows you", "Most conventional to ship"],
     "motion": "A recognition map in the hero sends pulses from the brand to people, search engines, and AI systems, and leans toward the cursor. The Digital Presence Stack lights layer by layer as it scrolls past. A sticky layer bar highlights Domain, Website, Search, Entity, and AI as you read each homepage section. Plus the Where are you stuck? diagnostic.",
     "best": "Shipping with the least risk. It feels like the company you already built, redesigned for 2027.",
     "risk": "The least new. It improves the current site rather than giving it a new signature."},
    {"k": "B", "dir": "editorial", "name": "Original, Editorial",
     "thesis": "The same original components, set for reading. A large left-aligned headline, the Lucky Domains story told as five layers in giant type, services as numbered editorial rows, an annotated case study, and insights given real space.",
     "attrs": ["Same palette and fonts", "Left-aligned, larger type", "Contents rail on inner pages", "Annotated case study", "Best home for writing"],
     "motion": "Reading progress on every page, and a section-aware contents rail on every inner page. The five layer words come into full weight as they cross the middle of the screen. A before-and-after identity example alternates on its own and stops once you choose. Case-study notes highlight on hover, focus, or tap.",
     "best": "A business that will publish case studies and guides, and wants the site to read as expertise.",
     "risk": "Needs writing to stay strong. Long service pages ask more of the reader than A."},
    {"k": "C", "dir": "interactive", "name": "Original, Interactive",
     "thesis": "The original design with the most interaction. A living presence map in the navy hero shows how a domain, a website, content, search, structured data, profiles, reviews, founders, and citations come together into one identity, and the rest of the site lets visitors explore it.",
     "attrs": ["Same palette and fonts", "Presence map in the hero", "Layers light the map as you scroll", "Quick presence self-check", "Example checks on every service page"],
     "motion": "The hero map settles from fragmented to recognized, then tours one signal at a time; pick a problem and it lights the signals involved. A second map lights each layer as you read it. Example-check lists step through on their own and pause on interaction. A six-question self-check updates as you tick boxes.",
     "best": "Showing, not telling, how entity work and AI visibility connect. The most memorable demonstration of the service.",
     "risk": "The most to build and maintain, and the busiest homepage. The map has to stay an explanation, not a dashboard."},
]
ROWS = [
    ("Similarity to the current site", "It is the current site.", "Very high. Same stylesheet, components, palette, and fonts.", "High. Same stylesheet and components, rearranged for reading.", "High. Same stylesheet and components, plus interactive panels."),
    ("Business message", "Domain, site, rankings.", "Digital presence studio for the AI era.", "Same.", "Same."),
    ("Pages", "Nine pages, a 404 page, and five redirect stubs.", "Sixteen.", "Sixteen.", "Sixteen."),
    ("Immediate service clarity", "High for three services.", "Highest. Five cards right after the stack.", "High. A five-service index sits in the hero.", "High. The headline is clear; the map rewards a second look."),
    ("Website-design credibility", "A middle piece between domain and SEO.", "A full homepage section and a deep page.", "Featured as an essay with a process and a page map.", "Page map, foundations, and example checks."),
    ("SEO credibility", "Strong.", "Strong, with Google's own guidance cited.", "Strongest. Room to explain the reasoning.", "Strong, shown as one signal among several."),
    ("AI-visibility credibility", "Mentioned under Entity SEO.", "Its own page, sources cited, no guarantees.", "Same, argued at more length.", "Same, plus the map shows what AI systems read."),
    ("Domain-service visibility", "First of three services.", "Menu, stack, diagnostic, its own section and page, plus How we buy domains.", "Menu, services index, its own page, plus How we buy domains.", "Menu, map, self-check, its own page, plus How we buy domains."),
    ("Founder visibility", "Founder line in the hero and a founder page.", "Founder line in the hero, a homepage section, and a full page.", "A byline in the hero and a profile section.", "Founder line in the hero, a homepage section, and a full page."),
    ("Motion", "Reveal on scroll only.", "Moderate, concentrated on the homepage.", "Low to moderate, reading-led.", "Highest, exploration-led."),
    ("Content requirements", "Existing copy.", "Moderate.", "Highest. Needs real case studies and articles.", "Moderate, plus map and check data."),
    ("Case-study presentation", "None.", "Cards and a structured case page.", "Annotated with the source of each change.", "Cards tagged by layer and a structured case page."),
    ("Accessibility implications", "Reveal-on-scroll content and FAQ answers stay hidden without JavaScript.", "Fewest custom widgets.", "Native controls and a reading rail.", "Most custom widgets, each with a text equivalent."),
    ("Implementation complexity", "Live today.", "Lowest. Mostly the existing stylesheet plus one layer.", "Low.", "Highest. Browser-generated SVG and several widgets."),
    ("Long-term maintainability", "Known.", "Easiest.", "Easy to maintain, demanding to keep current.", "Hardest. Map and check data must stay accurate."),
    ("Mobile behavior", "Good.", "Layer bar scrolls; map and stack stack vertically.", "Rail becomes a chapter strip; type stays large.", "Map switches to a portrait layout; tabs become a grid."),
    ("Strengths", "Commercial clarity and a direct founder relationship.", "Keeps all of that and adds the new story and depth.", "Authority and trust through writing.", "Explains entity and AI work better than words alone."),
    ("Weaknesses", "Message stops at rankings; three pages of services.", "Least new.", "Least effective without ongoing content.", "Busiest, and the most to maintain."),
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
<title>{E(title)} | Lucky Domains version 3 design concepts</title>
<meta name="description" content="Version 3 redesign concepts for Lucky Domains, built from the original site. Review only, not the live site.">
<link rel="icon" href="{r}shared/assets/favicon.ico" sizes="any">
<link rel="stylesheet" href="{r}shared/review.css">
<link rel="stylesheet" href="{r}phase-2/shared/review-p2.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="top">
  <a href="{r}phase-3/" aria-label="Lucky Domains, version 3 concepts"><img src="{r}shared/assets/logo-wordmark.png" alt="Lucky Domains" width="194" height="48"></a>
  <nav aria-label="Review"><a href="{r}phase-3/"{cur("")}>Version 3</a><a href="{r}phase-3/comparison/"{cur("comparison/")}>Comparison</a><a href="{r}phase-2/">Phase 2 archive</a><a href="{r}">Phase 1 archive</a></nav>
</header>
<main id="main">{body(r)}</main>
<footer class="bot"><p>{STATEMENT}</p><p>Design concept only. Not the live Lucky Domains website. Review site for Ken Ashe. Not indexed. Facts as of {E(C['asOf'])}. <a href="https://github.com/kenashe/luckydomains-design-concepts">Repository</a>.</p></footer>
</body></html>"""


def landing(r):
    cards = ""
    for c in CONCEPTS:
        base = f"{r}phase-3/{c['dir']}/"; k = c["k"].lower()
        more = "".join(f'<a href="{base}{p}">{NAMES[key]}</a>' for p, key in PAGES[1:])
        cards += f"""<article class="card">
  <a class="shot" href="{base}" tabindex="-1" aria-hidden="true"><img src="{r}phase-3/screenshots/{k}-home-desktop.jpg" alt="" width="1440" height="900" loading="lazy"><img class="shot-m" src="{r}phase-3/screenshots/{k}-home-mobile.jpg" alt="" width="375" height="760" loading="lazy"></a>
  <div class="card-b"><p class="k">Concept {c['k']}</p><h2>{E(c['name'])}</h2><p class="thesis">{E(c['thesis'])}</p>
    <ul class="attrs">{"".join(f"<li>{E(a)}</li>" for a in c['attrs'])}</ul>
    <dl><div><dt>Motion and interaction</dt><dd>{E(c['motion'])}</dd></div><div><dt>Best suited for</dt><dd>{E(c['best'])}</dd></div><div><dt>Tradeoff</dt><dd>{E(c['risk'])}</dd></div></dl>
    <p class="go"><a class="btn" href="{base}">Explore concept {c['k']}<span class="sr">: {E(c['name'])}</span></a></p>
    <p class="more more-16"><span class="sr">All sixteen pages:</span>{more}</p></div>
</article>"""
    stack = "".join(f"<li><b>{E(l['name'])}</b> {E(l['line'])}</li>" for l in C["stack"])
    svcs = "".join(f"<li>{E(s['name'])}</li>" for s in C["services"])
    pages = ", ".join(NAMES[k] for _, k in PAGES)
    return f"""
<section class="intro"><p class="k">Version 3 · {E(C['asOf'])}</p><h1>Version 3: built from the original site</h1>
<p class="lead">Three new directions that start from the live Lucky Domains design, not from a new one. Each loads the production stylesheet itself and adds a layer on top. All three tell the same story, offer the same services, and have the same sixteen pages, so the comparison is about design and interaction.</p>
<p class="state">{STATEMENT}</p></section>
<section class="p2-why" aria-labelledby="why-h"><h2 id="why-h">What changed from Phase 2</h2>
<p>Phase 2 drifted away from the original look and built only six pages per concept. Version 3 keeps the original design (navy hero, white and soft-grey sections, icon cards, green checks, numbered steps, the green call-to-action band, and the navy footer), builds a fuller site, and adds motion that explains the business instead of showcasing experiments.</p>
<div class="p2-cols">
<div><h3>Shared positioning</h3><p class="pos"><q>{E(C['company']['description'])}</q></p><p>{E(C['company']['originalModel'])}</p></div>
<div><h3>The Digital Presence Stack</h3><ol class="p2-stack">{stack}</ol></div>
<div><h3>Five services, sixteen pages</h3><ul class="p2-svcs">{svcs}</ul><p>Pages in every concept: {E(pages)}.</p></div></div></section>
<section class="cards" aria-label="Concepts">{cards}</section>
<section class="p2-ref" aria-labelledby="ref-h"><h2 id="ref-h">The current site, for reference</h2><p>The live LuckyDomains.io homepage, captured read-only.</p>
<div class="p2-ref-g"><figure><img src="{r}phase-3/screenshots/current-home-desktop.jpg" alt="The current live LuckyDomains.io homepage at desktop width" width="1440" height="900" loading="lazy"><figcaption>Desktop</figcaption></figure><figure><img src="{r}phase-3/screenshots/current-home-mobile.jpg" alt="The current live LuckyDomains.io homepage at mobile width" width="375" height="760" loading="lazy"><figcaption>Mobile</figcaption></figure></div></section>
<section class="next"><h2>How to review</h2><ol><li>Open the current site and concept A side by side. A should feel like the same company.</li><li>Follow one service from the homepage to its page and on to Contact in each concept.</li><li>Try each concept's interactions: the recognition map, stack, and diagnostic (A), the reading rail and before-and-after (B), and the presence map and self-check (C).</li><li>Read the <a href="{r}phase-3/comparison/">comparison</a>.</li></ol>
<p>Earlier rounds stay available as archives: <a href="{r}phase-2/">Phase 2</a> and <a href="{r}">Phase 1</a> (including Venture Lab). They are not finalists here.</p></section>"""


def comparison(r):
    head = '<th scope="col"><span>Reference</span>Current site</th>' + "".join(f'<th scope="col"><span>Concept {c["k"]}</span>{E(c["name"])}</th>' for c in CONCEPTS)
    rows = "".join(f'<tr><th scope="row">{E(x[0])}</th><td data-c="Current site">{E(x[1])}</td><td data-c="A">{E(x[2])}</td><td data-c="B">{E(x[3])}</td><td data-c="C">{E(x[4])}</td></tr>' for x in ROWS)
    shots = [("home-desktop", "Home, desktop"), ("home-mobile", "Home, mobile"), ("services", "Services"), ("ai", "AI Visibility"), ("websites", "Website Design"), ("work", "Case study"), ("service-mobile", "Service page, mobile"), ("interaction", "Interaction")]
    gal = '<h3>Current production site</h3><div class="p2-gal"><figure><img src="%sphase-3/screenshots/current-home-desktop.jpg" alt="Current LuckyDomains.io homepage, desktop" width="1440" height="900" loading="lazy"><figcaption>Home, desktop</figcaption></figure><figure><img src="%sphase-3/screenshots/current-home-mobile.jpg" alt="Current LuckyDomains.io homepage, mobile" width="375" height="760" loading="lazy"><figcaption>Home, mobile</figcaption></figure></div>' % (r, r)
    for c in CONCEPTS:
        k = c["k"].lower()
        figs = "".join(f'<figure><a href="{r}phase-3/screenshots/{k}-{f}.jpg"><img src="{r}phase-3/screenshots/{k}-{f}.jpg" alt="Concept {c["k"]}, {E(c["name"])}: {E(t)}" width="{375 if "mobile" in f else 1440}" height="{760 if "mobile" in f else 900}" loading="lazy"></a><figcaption>{E(t)}</figcaption></figure>' for f, t in shots)
        gal += f'<h3>Concept {c["k"]}: {E(c["name"])}</h3><div class="p2-gal">{figs}</div>'
    return f"""
<section class="intro"><p class="k">Version 3 · Side by side</p><h1>Comparison</h1>
<p class="lead">The current site against the three version 3 concepts. All three concepts share one message, five services, and sixteen pages; the notes are about design. They are observations to argue with, not a decision.</p><p class="state">{STATEMENT}</p></section>
<section class="tbl" aria-label="Comparison table"><table class="t4"><thead><tr><th scope="col"><span class="sr">Criterion</span></th>{head}</tr></thead><tbody>{rows}</tbody></table></section>
<section class="gal p2-gals" aria-labelledby="g-h"><h2 id="g-h">Screenshots</h2>{gal}</section>
<section class="next"><h2>Shared by all three</h2><ul><li>The production stylesheet, loaded unchanged, under each concept's own layer.</li><li>One message: {E(C['company']['description'])}</li><li>Domain, Website, Search, Entity, AI, presented as one system.</li><li>Five services, each with its own page, plus How we buy domains.</li><li>No guarantees of rankings, AI citations, or Knowledge Panels, with Google's and Bing's own documentation cited.</li><li>ZeroHuman and other experiments only in a small From the lab section and a labeled research note.</li><li>Noindex, forms that send nothing, keyboard access, and complete content without JavaScript or motion.</li></ul>
<p><a class="btn" href="{r}phase-3/">Back to version 3</a></p></section>"""


def build():
    write("phase-3/index.html", page("", "Version 3 concepts", landing))
    write("phase-3/comparison/index.html", page("comparison/", "Comparison", comparison))
