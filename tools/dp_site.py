#!/usr/bin/env python3
"""Port the approved design (version 3, Original Interactive, refined) into the Lucky Domains
production candidate.

    python3 tools/dp_site.py /path/to/luckydomains-checkout

The checkout must be on the branch digital-presence-production-candidate of kenashe/luckydomains.
This tool writes complete, hand-editable HTML pages, one stylesheet and one script into that
checkout. It is a porting aid that lives in the design repository only. The production repository
keeps its rules: no build step, no framework, plain files that deploy with a git push. Once the
owner approves the candidate, the HTML in the production repository is the source of truth.

Run this module on its own. It adjusts the shared version 3 content in memory (final owner
decisions), so it must not be imported by tools/build.py.
"""
import json, re, shutil, subprocess, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import p3lib
from p3lib import C, E, S, PG, icon, eyebrow, check, sec_head, section, cards, steps, panel, split, note, cta_band
import p3_r as RF
from p3_r_content import R

HERE = Path(__file__).resolve().parent
SITE = HERE.parent
OUT = Path(sys.argv[1]).resolve()
DOMAIN = "https://luckydomains.io"
ARROW = icon("arrow", "2.4")
LASTMOD = "2026-11-24"          # the date the redesigned pages were written
REVISED = "2026-11-25"          # the date of the final editorial and structured-data pass
BASELINE = "8bfedd71cd361757a3ba97f3680dc7f011dad3bb"   # the candidate as it stood on 2026-11-24; pages that differ from it carry REVISED
PROFILE_OLD = "Profile of Ken Ashe, founder and operator of Lucky Domains, a domain acquisition, brokerage, and SEO practice run with CPA and PMP discipline."
PROFILE_NEW = "Profile of Ken Ashe, CPA, PMP, founder and operator of Lucky Domains, a digital presence studio for the AI era."
KNOWS_OLD = '"knowsAbout": ["Premium domain acquisition", "Domain brokerage", "Domain negotiation", "SEO strategy", "Technical SEO", "Local SEO", "Content strategy"]'
ADDR_AT = '      "email": "info@luckydomains.io",\n      "description"'
ADDR_NEW = ('      "email": "info@luckydomains.io",\n      "address": {\n        "@type": "PostalAddress",\n        "addressLocality": "Berkeley Heights",\n'
            '        "addressRegion": "NJ",\n        "addressCountry": "US"\n      },\n      "description"')
LOCATION = "Berkeley Heights, New Jersey"
ORG_OLD = "Domain acquisition, brokerage, and SEO services company helping businesses secure stronger digital assets and build search visibility over time."
ORG_NEW = "Lucky Domains is a digital presence studio for the AI era, offering website design and development, SEO, AI visibility, digital identity, and domain acquisition and brokerage."
KNOWS_NEW = '"knowsAbout": ["Website design and development", "Technical SEO", "SEO strategy", "Local SEO", "Content strategy", "Entity SEO", "Structured data", "AI visibility", "Brand authority", "Premium domain acquisition", "Domain brokerage", "Domain negotiation"]'


def git_show(rel):
    return subprocess.run(["git", "-C", str(OUT), "show", "origin/main:" + rel], capture_output=True, text=True, check=True).stdout


branch = subprocess.run(["git", "-C", str(OUT), "rev-parse", "--abbrev-ref", "HEAD"], capture_output=True, text=True).stdout.strip()
if branch != "digital-presence-production-candidate":
    sys.exit(f"Refusing: the checkout is on {branch!r}, not digital-presence-production-candidate.")

# ------------------------------------------------------------------ final owner decisions (in memory only)
ARTICLES = []                                   # filled from tools/dp_articles/*.txt (HTML bodies kept as .txt so the review site never serves them as pages)
for f in sorted((HERE / "dp_articles").glob("*.txt")):
    t = f.read_text()
    meta = json.loads(re.search(r"<!--meta\n(.*?)\nmeta-->", t, re.S).group(1))
    meta["_slug"] = f.stem
    meta["_body"] = t.split("meta-->", 1)[1].strip("\n")
    ARTICLES.append(meta)
ARTICLES.sort(key=lambda m: m["order"])
BY_SLUG = {m["_slug"]: m for m in ARTICLES}
DATA = json.loads((HERE / "dp_data.json").read_text())
# The Web3Forms key is a public identifier that already ships in the live page. Read it from there; it is never copied into this repository.
DATA["contact"]["accessKey"] = re.search(r'data-access-key="([^"]+)"', git_show("contact/index.html")).group(1)

eng = PG["services"]["engagements"]
i = next(n for n, e in enumerate(eng) if e["name"] == "Growth SEO")
eng[i] = {"name": "SEO Audits & Optimization", "kind": "Scoped",
          "line": "One-time audits, scoped implementation projects, and ongoing optimization and monitoring by agreement.",
          "check": ["One-time SEO audits and technical SEO reviews", "Scoped implementation, with search and content strategy", "Ongoing optimization and monitoring by agreement"]}
PG["services"]["notList"][2] = "Not a monthly retainer agency"
PG["seo"]["faq"][1][1] = ("Technical fixes can show up within weeks. Content and authority take months. We scope an audit or a project first. "
                          "Ongoing optimization and monitoring continue only where they make sense, and by agreement.")
PG["seo"]["faq"].append(["How is SEO work structured?", "As a one-time audit, a technical review, a scoped implementation project, or a search and content strategy. "
                         "Ongoing optimization and monitoring are available by agreement. There is no standard monthly package."])
S["seo"]["check"] = ["SEO audits and technical SEO reviews", "Scoped implementation projects", "Search and content strategy", "Ongoing optimization and monitoring by agreement"]
S["seo"]["short"] = "Audits, technical fixes, and search and content strategy that earn visibility and keep it."
R["services"]["distinction"] = {
    "title": "Three related services. Three different jobs.",
    "seo": ["SEO & Search Visibility", "Improves the technical and content foundations that support being found in search."],
    "entity": ["Entity SEO & Digital Identity", "Establishes a clear, consistent, verifiable identity for a person, organization, or brand."],
    "ai": ["AI Visibility & Brand Authority", "Improves the content and supporting evidence that search engines and AI systems use when they understand, describe, cite, or answer questions about that identity."],
    "note": "AI visibility does not replace SEO. Technical health, useful content, and credible authority remain the foundation the other two depend on."}
R["differs"]["ai"][1] = ("SEO improves the technical and content foundations that support being found. Entity SEO establishes a clear, consistent, verifiable identity. "
                         "AI visibility improves the content and evidence that search engines and AI systems use when they describe, cite, or answer questions about that identity.")
R["differs"]["entity"][1] = ("Entity SEO establishes who you are, stated the same way everywhere. AI visibility builds on that identity and improves the content and evidence "
                             "systems use when they answer questions about it. Both depend on sound SEO.")
# Fact check against the public build record: the record documents an agent the founder built and runs; it does not say whose profiles it maintains.
R["firstParty"]["seo"] = {"title": "An internal system: the Autonomous SEO Agent",
    "body": "The Autonomous SEO Agent is an internal system the founder built. Each day it researches listing and profile sites, creates a profile where a listing is legitimate, free, and relevant, "
            "and confirms its own verification emails. Its public build record reports 63 sites researched and eight profiles confirmed live. Most of those profiles carry nofollow links, and no SEO impact has been established.",
    "note": "An internal system, shown to illustrate how automation supports research and monitoring. Not a client product and not a client result.",
    "links": [["Build record on KenAshe.ai", "https://kenashe.ai/building/autonomous-seo-agent/"]]}
R["aiWork"]["example"] = ("An example from our own operations: the Autonomous SEO Agent is an internal system that researches listing and profile sites and creates profiles each day. "
                          "It is not a client product, and no SEO impact has been established.")
R["story"]["about"][2] = R["story"]["about"][2].replace("based in Berkeley Heights, New Jersey, and still run by its founder", "based in Berkeley Heights, New Jersey, and still run by its founder")
C["company"]["footer"] = C["company"].get("footer") or C["company"]["description"]
R["services"]["lead"] = "Each service stands on its own. Start with the one you need."      # no claim about what most clients do


def distinction():
    d = R["services"]["distinction"]
    cols = "".join(f'<div><p class="fp-k">{E(d[k][0])}</p><p>{E(d[k][1])}</p></div>' for k in ("seo", "entity", "ai"))
    return f'<div class="distinct reveal"><h3>{E(d["title"])}</h3><div class="distinct-g distinct-3">{cols}</div><p class="distinct-n">{E(d["note"])}</p></div>'


RF.distinction = distinction

# Final copy refinements from the owner's review on November 25, 2026 (wording only, see tools/dp_copy.py).
import dp_copy
dp_copy.apply(C, R, PG, S, DATA)
COPY_HELPERS = {"note": note, "check": check, "ai_intro": R["aiWork"]["intro"], "ai_limit": R["aiWork"]["limit"]}

# ------------------------------------------------------------------ URLs
MAP = {"": "/", "services/": "/services/", "services/website-design/": "/services/website-design/", "services/seo/": "/services/seo/",
       "services/ai-visibility/": "/services/ai-visibility/", "services/entity-seo/": "/services/entity-seo/", "services/domains/": "/services/domain-acquisition/",
       "how-we-buy-domains/": "/how-we-buy-domains/", "tools/digital-presence-check/": "/tools/digital-presence-check/", "about/": "/about/",
       "founder/": "/founder/ken-ashe/", "insights/": "/insights/", "insights/domains-identity-for-ai-agents/": "/insights/domains-identity-for-ai-agents/",
       "news/": "/news/", "contact/": "/contact/"}
NAV = [("Services", "/services/"), ("About", "/about/"), ("Insights", "/insights/"), ("Founder", "/founder/ken-ashe/"), ("Contact", "/contact/")]


class PCtx:
    """Root-absolute production URLs, in the one canonical form the repository allows."""
    cfg = {"k": "C"}
    c = r = "/"

    def __init__(self, url):
        self.url = url
        self.path = url.strip("/") + "/" if url != "/" else ""

    def to(self, p=""):
        return MAP[p]

    def asset(self, n):
        return "/assets/" + n

    def svc(self, sid):
        return MAP[S[sid]["path"]]

    def cur(self, href):
        if href == "/services/":
            return ' aria-current="page"' if self.url.startswith("/services/") or self.url == "/how-we-buy-domains/" else ""
        return ' aria-current="page"' if self.url.startswith(href) else ""


# ------------------------------------------------------------------ shell
HEAD_COMMON = """<!-- head-common:start -->
<link rel="icon" href="/assets/favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="/assets/favicon-32.png">
<link rel="icon" type="image/png" sizes="16x16" href="/assets/favicon-16.png">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="preload" href="/assets/fonts/jakarta-normal-400-800.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/fonts/inter-normal-400-600.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/css/styles.css">
<script>document.documentElement.className='js'</script>
<!-- head-common:end -->"""


def head(url, title, desc, og_title, ld, robots=""):
    lds = "".join(f'\n<script type="application/ld+json">\n{b.strip()}\n</script>' for b in ld)
    rb = f'<meta name="robots" content="{robots}">\n' if robots else ""
    canon = f'<link rel="canonical" href="{DOMAIN}{url}">\n' if url else ""
    og_url = f'<meta property="og:url" content="{DOMAIN}{url}">\n' if url else ""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
{rb}{canon}<meta name="theme-color" content="#0C2340">

<meta property="og:type" content="website">
<meta property="og:site_name" content="Lucky Domains">
<meta property="og:title" content="{E(og_title)}">
<meta property="og:description" content="{E(desc)}">
{og_url}<meta property="og:image" content="{DOMAIN}/assets/og-image.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{E(og_title)}">
<meta name="twitter:description" content="{E(desc)}">
<meta name="twitter:image" content="{DOMAIN}/assets/og-image.png">

{HEAD_COMMON}
{lds}
</head>"""


def header(ctx):
    sub = "".join(f'<li><a href="{ctx.svc(s["id"])}">{icon(s["icon"])}<span>{E(s["name"])}</span></a></li>' for s in C["services"])
    sub += ('<li class="menu-x"><a href="/services/">All services</a><a href="/how-we-buy-domains/">How we buy domains</a>'
            '<a href="/tools/digital-presence-check/">Digital Presence Check</a></li>')
    links = ""
    for label, href in NAV:
        if href == "/services/":
            links += (f'<div class="has-menu"><a href="{href}"{ctx.cur(href)}>{label}</a><button class="menu-btn" type="button" aria-expanded="false" aria-controls="m-svc">'
                      f'<span class="sr">Show service pages</span></button><ul class="menu" id="m-svc">{sub}</ul></div>')
        else:
            links += f'<a href="{href}"{ctx.cur(href)}>{label}</a>'
    return f"""<!-- header:start -->
<header class="site-header" id="site-header">
<div class="container header-inner">
<a class="brand" href="/" aria-label="Lucky Domains home"><img class="brand-logo" src="/assets/logo-wordmark.png" alt="Lucky Domains" width="170" height="38"></a>
<nav class="nav" id="nav" aria-label="Primary">{links}<a href="/contact/" class="btn btn-accent btn-sm nav-cta">{C['navCta']}</a></nav>
<button class="nav-toggle" id="nav-toggle" type="button" aria-label="Open menu" aria-controls="nav" aria-expanded="false"><span></span><span></span><span></span></button>
</div>
</header>
<!-- header:end -->"""


def footer():
    sv = "".join(f'<li><a href="{MAP[s["path"]]}">{E(s["name"])}</a></li>' for s in C["services"]) + '<li><a href="/how-we-buy-domains/">How we buy domains</a></li>'
    co = "".join(f'<li><a href="{p}">{t}</a></li>' for t, p in [("About", "/about/"), ("Founder", "/founder/ken-ashe/"), ("Insights", "/insights/"), ("News &amp; media", "/news/"),
                                                                 ("Digital Presence Check", "/tools/digital-presence-check/")])
    return f"""<!-- footer:start -->
<footer class="site-footer">
<div class="container">
<div class="footer-grid">
<div class="footer-brand"><a href="/" class="footer-logo"><img src="/assets/logo-icon.png" alt="" width="42" height="42" loading="lazy" decoding="async"><span>Lucky Domains</span></a><p>{E(C['company']['description'])}</p></div>
<div class="footer-col"><h2 class="fh">Services</h2><ul>{sv}</ul></div>
<div class="footer-col"><h2 class="fh">Company</h2><ul>{co}</ul></div>
<div class="footer-col"><h2 class="fh">Get in touch</h2><ul><li><a href="mailto:info@luckydomains.io">info@luckydomains.io</a></li><li>{LOCATION}</li><li><a href="/contact/">{C['navCta']}</a></li></ul></div>
</div>
<div class="footer-bottom"><span>&copy; <span id="year">2026</span> Lucky Domains. All rights reserved.</span><span>{E(C['company']['founderLine'])}</span></div>
</div>
</footer>
<!-- footer:end -->"""


BLOCK = "html head body header footer main nav section article aside div ul ol li p h1 h2 h3 h4 form fieldset legend table thead tbody tr th td figure figcaption blockquote dl dt dd select option details summary".split()
RAW = re.compile(r"(<script\b.*?</script>|<textarea\b.*?</textarea>|<svg\b.*?</svg>|<!--.*?-->)", re.S)


def pretty(body):
    """Put block-level tags on their own lines so the committed HTML is readable and hand-editable."""
    parts = RAW.split(body)
    out = []
    for n, part in enumerate(parts):
        if n % 2:
            out.append("\n" + part + "\n" if part.startswith("<!--") else part)
            continue
        part = re.sub(r"\s*\n\s*", " ", part)
        part = re.sub(r"<(%s)\b" % "|".join(BLOCK), r"\n<\1", part)
        part = re.sub(r"</(%s)>" % "|".join(BLOCK), r"</\1>\n", part)
        out.append(part)
    text = "".join(out)
    lines = [l.strip() for l in text.split("\n")]
    return "\n".join(l for l in lines if l)


def page(ctx, title, desc, og_title, body, ld, cls="", robots="", canonical=True):
    main = pretty(f'<main id="main">{body}</main>')
    return (head(ctx.url if canonical else "", title, desc, og_title, ld, robots)
            + f'\n<body class="rf {cls}">\n<a class="skip-link" href="#main">Skip to content</a>\n{pretty_keep(header(ctx))}\n{main}\n{pretty_keep(footer())}\n'
              '<script src="/js/main.js" defer></script>\n</body>\n</html>\n')


def pretty_keep(block):
    """Pretty-print a header or footer block but keep its marker comments on their own lines."""
    first, rest = block.split("\n", 1)
    inner, last = rest.rsplit("\n", 1)
    return first + "\n" + pretty(inner) + "\n" + last


def write(rel, text):
    p = OUT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text)


# ------------------------------------------------------------------ structured data
def crumbs_ld(items):
    els = ",\n".join(f'        {{"@type":"ListItem","position":{n},"name":{json.dumps(name)},"item":"{DOMAIN}{u}"}}' for n, (name, u) in enumerate(items, 1))
    return f'    {{\n      "@type": "BreadcrumbList",\n      "@id": "{DOMAIN}{items[-1][1]}#breadcrumb",\n      "itemListElement": [\n{els}\n      ]\n    }}'


def page_ld(url, name, kind, items, extra=""):
    web = (f'    {{\n      "@type": "{kind}",\n      "@id": "{DOMAIN}{url}#webpage",\n      "url": "{DOMAIN}{url}",\n      "name": {json.dumps(name)},\n'
           f'      "isPartOf": {{ "@id": "{DOMAIN}/#website" }},\n      "publisher": {{ "@id": "{DOMAIN}/#organization" }},\n'
           f'      "breadcrumb": {{ "@id": "{DOMAIN}{url}#breadcrumb" }},\n      "inLanguage": "en-US"{extra}\n    }}')
    return '{\n  "@context": "https://schema.org",\n  "@graph": [\n' + crumbs_ld(items) + ",\n" + web + "\n  ]\n}"


def service_ld(url, name, stype, desc, levels=None):
    cat = ""
    if levels:
        offers = ",\n".join(f'          {{"@type":"Offer","itemOffered":{{"@type":"Service","name":{json.dumps(x)}}}}}' for x in levels)
        cat = f',\n      "hasOfferCatalog": {{\n        "@type": "OfferCatalog",\n        "name": {json.dumps(name + " engagements")},\n        "itemListElement": [\n{offers}\n        ]\n      }}'
    svc = (f'    {{\n      "@type": "Service",\n      "@id": "{DOMAIN}{url}#service",\n      "name": {json.dumps(name)},\n      "serviceType": {json.dumps(stype)},\n'
           f'      "url": "{DOMAIN}{url}",\n      "description": {json.dumps(desc)},\n      "provider": {{ "@id": "{DOMAIN}/#organization" }},\n      "areaServed": "US"{cat}\n    }}')
    base = page_ld(url, name, "WebPage", [("Home", "/"), ("Services", "/services/"), (name, url)], f',\n      "about": {{ "@id": "{DOMAIN}{url}#service" }}')
    return base[:-len("\n  ]\n}")] + ",\n" + svc + "\n  ]\n}"


def org_current(text, full=True):
    """Bring the one shared Organization record up to date, identically on every page that carries it.

    The live site mirrors the full Organization node on the home page, the founder page and the June 2026 press
    release, the same way it mirrors the Person node. Only that node changes: its description, its knowsAbout list,
    and a city-level address. Its @id, name, logo, founder, sameAs and contact point are untouched.
    """
    assert text.count(ORG_OLD) == 1, "expected one Organization description"
    text = text.replace(ORG_OLD, ORG_NEW)
    if full:
        assert text.count(KNOWS_OLD) == 1 and text.count(ADDR_AT) == 1, "expected the full Organization node"
        text = text.replace(KNOWS_OLD, KNOWS_NEW).replace(ADDR_AT, ADDR_NEW)
    return text


def old_ld(rel, full=False):
    """Structured data blocks as they are on the live page, with the shared Organization record brought up to date."""
    blocks = re.findall(r'<script type="application/ld\+json">\n?(.*?)\n?</script>', git_show(rel), re.S)
    return [org_current(b, full) if ORG_OLD in b else b for b in blocks]


# ------------------------------------------------------------------ page parts that differ from the approved concept
def reading(slugs, soft=False):
    lis = "".join(f'<li><a href="/insights/{s}/">{E(BY_SLUG[s]["title"])}</a><span>{E(BY_SLUG[s]["category"])} · {E(BY_SLUG[s]["topic"])}</span></li>' for s in slugs)
    return (f'<section class="section section--tight reading{" section-soft" if soft else ""}" aria-labelledby="rd-h"><div class="container"><div class="reading-in reveal">'
            f'<h2 id="rd-h">Related reading</h2><ul>{lis}</ul><a class="link-arrow" href="/insights/">All insights {ARROW}</a></div></div></section>')


def contact_form():
    opts = "".join(f'<option value="{E(v)}">{E(v)}</option>' for v in DATA["contact"]["needs"])
    sel = lambda name, vals, first="": "".join(([f'<option value="">{first}</option>'] if first else []) + [f'<option value="{E(v)}">{E(v)}</option>' for v in vals])
    return f"""<div class="form-card reveal">
<form id="contact-form" data-access-key="{DATA['contact']['accessKey']}" novalidate>
<input type="hidden" name="subject" value="New inquiry from luckydomains.io">
<input type="hidden" name="from_name" value="Lucky Domains website">
<!-- honeypot -->
<input type="checkbox" name="botcheck" tabindex="-1" style="display:none" aria-hidden="true">
<div class="field"><label for="name">Name</label><input id="name" name="name" type="text" autocomplete="name" required placeholder="Jane Doe"></div>
<div class="field"><label for="email">Email</label><input id="email" name="email" type="email" autocomplete="email" required placeholder="jane@company.com"></div>
<div class="field"><label for="need">I need help with</label><select id="need" name="need" required><option value="">Choose one</option>{opts}</select></div>
<div class="field"><label for="target">Your website, the domain name, or the business this is about</label><input id="target" name="target" type="text" required placeholder="https://yoursite.com or example.com"></div>
<div class="field"><label for="listed">Buying a domain? Is it listed for sale? (optional)</label><select id="listed" name="listed">{sel("listed", ["Not applicable", "Not sure", "Yes", "No"])}</select></div>
<div class="field"><label for="timeline">Timeline</label><select id="timeline" name="timeline" required>{sel("timeline", ["As soon as possible", "1 to 3 months", "3 to 6 months", "Exploring, no date yet"], "Choose one")}</select></div>
<div class="field"><label for="budget">Budget band (optional)</label><select id="budget" name="budget">{sel("budget", ["Not sure", "Under 5k", "5k to 25k", "25k to 100k", "100k+"])}</select></div>
<div class="field"><label for="message">Anything else Ken should know</label><textarea id="message" name="message" required placeholder="What you are trying to achieve, what you have tried, and what a good outcome looks like"></textarea></div>
<button type="submit" class="btn btn-accent btn-lg" style="width:100%">Send message</button>
<div id="form-status" class="form-status" role="status" aria-live="polite"></div>
<p class="form-note">Prefer email? Reach Ken directly at <a href="mailto:info@luckydomains.io">info@luckydomains.io</a>. Not sure what you need? <a href="/tools/digital-presence-check/">Take the Digital Presence Check</a>.</p>
</form>
</div>"""


def pg_contact(ctx):
    c = PG["contact"]
    info = lambda ic, h, body: f'<div class="info"><div class="ic">{icon(ic)}</div><div><h3>{h}</h3><p>{body}</p></div></div>'
    side = ('<div class="contact-side">' + info("mail", "Email", '<a href="mailto:info@luckydomains.io">info@luckydomains.io</a>') + info("globe", "Based in", LOCATION)
            + info("chart", "Response time", "Typically within one business day.")
            + info("shield", "First consultation", "Free, with no obligation. A short first call, about 20 minutes.")
            + info("target", "Buying a domain?", '<a href="/how-we-buy-domains/">How we buy domains</a>') + "</div>")
    return RF.phero(ctx, "contact", "Contact", c["h1"], c["lead"], cta=False) + section("form", f'<h2 class="sr">Contact form and details</h2><div class="contact-grid">{contact_form()}{side}</div>')


def pg_founder(ctx):
    f = C["founder"]; d = DATA["founder"]
    cred = "".join(f'<div class="stat"><div class="num">{E(a)}</div><div class="lbl">{E(b)}</div></div>' for a, b in f["credentialsFull"])
    exp = cards([dict(icon=ic, h=t, p=x) for ic, (t, x) in zip(["chart", "monitor", "spark"], d["experience"])], 3)
    sp = "".join(f'<div class="value reveal"><div class="ic">{icon("users")}</div><div><h3>{E(y)} · {E(ev)}</h3><p>{E(t)}</p></div></div>' for y, ev, t in f["speaking"])
    links = "".join(f'<div class="info"><div class="ic">{icon("link")}</div><div><h3>{E(t)}</h3><p><a href="{u}" rel="noopener">{E(x)}</a></p></div></div>' for t, u, x in f["links"])
    two = "".join(f'<article class="card reveal"><span class="tag">{E(a)}</span><p>{E(b)}</p></article>' for a, b in d["twoSites"])
    pubs = "".join(f'<li class="reveal"><p class="fp-k">{E(p["kind"])} · {E(p["outlet"])}{(" · " + E(p["date"])) if p.get("date") else ""}</p><h3><a href="{p["url"]}" rel="noopener">{E(p["title"])}</a></h3>'
                   f'{("<p>" + E(p["line"]) + "</p>") if p.get("line") else ""}</li>' for p in d["published"])
    pub_sec = section("published", sec_head("Published work and media", d["publishedTitle"], d["publishedLead"]) + f'<ul class="pubs">{pubs}</ul>'
                      + f'<p class="center v3-more">The full list is in the <a href="https://kenashe.ai/newsroom/" rel="noopener">newsroom on KenAshe.ai</a>.</p>') if d["published"] else ""
    return (RF.phero(ctx, "founder", "Founder", "Ken Ashe", d["lead"], cta=False)
            + section("bio", split(sec_head("Background", "Business, technology, and digital identity.", "", False) + "".join(f'<p>{E(x)}</p>' for x in d["bio"]),
                                   f'<figure class="founder-card reveal"><img src="/assets/ken-ashe-2026-square.jpg" alt="Ken Ashe, founder and operator of Lucky Domains" width="640" height="640" decoding="async"></figure>'))
            + section("experience", sec_head("Experience", "Finance discipline, applied to digital work.", f["discipline"]) + exp, True)
            + section("creds", sec_head("Credentials", "Professional credentials.") + f'<div class="stats creds reveal">{cred}</div><p class="center v3-more">Ken Ashe is a member of <a href="{f["forbes"]}" rel="noopener">Forbes Business Council</a>.</p>')
            + pub_sec.replace('class="section"', 'class="section section-soft"', 1)
            + section("speaking", split(sec_head("Speaking and judging", "On stage and on panels.", "", False) + f'<div class="grid" style="gap:22px">{sp}</div>',
                                        f'<div class="contact-side reveal"><h3 class="sr">Connect</h3>{links}</div>'))
            + section("sites", sec_head("Two sites, two jobs", "Where to find what.") + f'<div class="grid grid-2">{two}</div>'
                      + f'<p class="center v3-more">{E(d["research"])} <a href="/insights/domains-identity-for-ai-agents/">Read the research article</a> or visit <a href="https://kenashe.ai/" rel="noopener">KenAshe.ai</a>.</p>', True))


def pg_insights(ctx):
    d = DATA["insights"]
    return (RF.phero(ctx, "insights", "Insights", d["h1"], d["lead"], cta=False)
            + '<section class="section" id="library" aria-labelledby="lib-h"><div class="container"><h2 class="sr" id="lib-h">Articles</h2><div class="grid grid-2 ins-grid">\n<!-- articles:start -->\n<!-- articles:end -->\n</div></div></section>'
            + section("tools", f'<div class="grid grid-2 ins-t">{RF.promo(ctx, "h2").replace("<h2>Not sure where to start?</h2>", "<h2>Check your digital presence</h2>", 1)}<article class="card reveal"><div class="icon-badge navy">{icon("doc")}</div><span class="tag">Build records</span><h2>KenAshe.ai</h2>'
                               f'<p>{E(d["kenashe"])}</p><div class="svc-foot"><a class="link-arrow" href="https://kenashe.ai/" rel="noopener">Visit KenAshe.ai {ARROW}</a></div></article></div>', True))


def pg_news(ctx):
    n = PG["news"]; r = n["release"]
    info = lambda ic, h, body: f'<div class="info"><div class="ic">{icon(ic)}</div><div><h3>{h}</h3><p>{body}</p></div></div>'
    rel = (f'<article class="card news-card reveal"><span class="tag">{E(r["date"])} · Press release</span><h3><a href="/news/website-relaunch/">{E(r["title"])}</a></h3><p>{E(r["line"])}</p>'
           f'<div class="svc-foot"><a class="link-arrow" href="/news/website-relaunch/">Read the release {ARROW}</a></div></article>')
    media = ('<div class="contact-side">' + info("users", "Founder", '<a href="/founder/ken-ashe/">Ken Ashe</a>') + info("doc", "About Lucky Domains", '<a href="/about/">About the company</a>')
             + info("mail", "Media inquiries", '<a href="mailto:info@luckydomains.io">info@luckydomains.io</a>') + info("globe", "Location", LOCATION) + "</div>")
    return (RF.phero(ctx, "news", "News & media", n["h1"], n["lead"], cta=False)
            + section("news", split(sec_head("Company news", "Announcements.", "Press releases appear here as they were published.", False) + rel,
                                    '<div class="reveal">' + sec_head("Media resources", "For company information.", "", False).replace("<h2", '<h2 class="h-sm"') + media + "</div>")))


def pg_404(ctx):
    return ('<section class="hero hero-404"><div class="container hero-inner">' + eyebrow("404", True) + "<h1>This page wandered off.</h1>"
            '<p class="lead">The page you are looking for does not exist or has moved. These will get you back on track.</p>'
            '<div class="btn-row"><a href="/" class="btn btn-accent btn-lg">Back to home</a><a href="/services/" class="btn btn-on-dark btn-lg">Services</a>'
            '<a href="/insights/" class="btn btn-on-dark btn-lg">Insights</a><a href="/contact/" class="btn btn-on-dark btn-lg">Contact</a></div></div></section>')


# ------------------------------------------------------------------ the pages
M = DATA["meta"]
SVC_READING = {"websites": ["fix-or-rebuild-your-website", "what-ai-search-reads-on-your-website"], "seo": ["what-ai-search-reads-on-your-website", "fix-or-rebuild-your-website"],
               "ai": ["what-ai-search-reads-on-your-website", "entity-seo-for-founders"], "entity": ["entity-seo-for-founders", "domains-identity-for-ai-agents"],
               "domains": ["how-a-private-domain-purchase-works", "domains-identity-for-ai-agents"], "buy": ["how-a-private-domain-purchase-works"]}
SVC_URL = {"websites": "/services/website-design/", "seo": "/services/seo/", "ai": "/services/ai-visibility/", "entity": "/services/entity-seo/", "domains": "/services/domain-acquisition/"}
SVC_FN = {"websites": RF.pg_websites, "seo": RF.pg_seo, "ai": RF.pg_ai, "entity": RF.pg_entity, "domains": RF.pg_domains}


def build_pages():
    def emit(rel, url, key, body, ld, cls="", og=None, band=True, robots="", canonical=True):
        ctx = PCtx(url)
        body = dp_copy.swap(key, body, COPY_HELPERS)
        if band:
            body += cta_band(ctx)
        m = M[key]
        write(rel, page(ctx, m["title"], m["desc"], og or m.get("og") or m["title"].split(" | ")[0], body, ld, cls, robots, canonical))

    ctx = PCtx("/")
    home_ld = old_ld("index.html", full=True)
    assert "Berkeley Heights" in home_ld[0] and "AI visibility" in home_ld[0] and ORG_NEW in home_ld[0]
    emit("index.html", "/", "home", RF.home(ctx), home_ld, "home", band=False)

    ctx = PCtx("/services/")
    body = RF.pg_services(ctx)
    # anchors the earlier site used, still linked from KenAshe.ai posts through the legacy services.html stub
    for name, anchor in (("Website Design &amp; Development", "websites"), ("SEO &amp; Search Visibility", "seo"), ("Domain Acquisition &amp; Brokerage", "domains")):
        at = body.rindex('<article class="card svc reveal"', 0, body.index(f"<h3>{name}</h3>"))
        body = body[:at] + f'<article id="{anchor}" class="card svc reveal"' + body[at + len('<article class="card svc reveal"'):]
    body = body.replace("<h3>Domain Acquisition &amp; Brokerage</h3>", '<h3><span id="selling"></span>Domain Acquisition &amp; Brokerage</h3>', 1)
    emit("services/index.html", "/services/", "services", body, [page_ld("/services/", "Services", "CollectionPage", [("Home", "/"), ("Services", "/services/")])], "pg-services")
    for key, fn in SVC_FN.items():
        url = SVC_URL[key]; ctx = PCtx(url); s = S[key]
        levels = {"entity": ["Entity foundation", "Entity authority", "Entity and AI Visibility Audit"], "ai": ["Entity and AI Visibility Audit"], "websites": ["Website review", "Website Build"],
                  "seo": ["SEO audits", "Technical SEO reviews", "Scoped SEO implementation projects", "Search and content strategy", "Ongoing optimization and monitoring by agreement"], "domains": ["Domain acquisition", "Domain brokerage for sellers"]}[key]
        emit(f"{url.strip('/')}/index.html", url, key, fn(ctx) + reading([x for x in SVC_READING[key] if x in BY_SLUG]), [service_ld(url, s["name"], M[key]["type"], M[key]["desc"], levels)], f"pg-{key}")

    ctx = PCtx("/how-we-buy-domains/")
    emit("how-we-buy-domains/index.html", "/how-we-buy-domains/", "buy", RF.pg_buy(ctx) + reading([x for x in SVC_READING["buy"] if x in BY_SLUG]),
         [page_ld("/how-we-buy-domains/", "How we buy domains", "WebPage", [("Home", "/"), ("Services", "/services/"), ("Domain Acquisition & Brokerage", "/services/domain-acquisition/"), ("How we buy domains", "/how-we-buy-domains/")])], "pg-buy")
    ctx = PCtx("/tools/digital-presence-check/")
    emit("tools/digital-presence-check/index.html", "/tools/digital-presence-check/", "check", RF.pg_check(ctx),
         [page_ld("/tools/digital-presence-check/", "Digital Presence Check", "WebPage", [("Home", "/"), ("Digital Presence Check", "/tools/digital-presence-check/")],
                  ',\n      "description": "A free, browser-based self-check. Ten questions about a domain, website, search visibility, identity, and AI visibility. Nothing is stored or sent."')], "pg-check")
    ctx = PCtx("/about/")
    emit("about/index.html", "/about/", "about", RF.pg_about(ctx), old_ld("about/index.html"), "pg-about")
    ctx = PCtx("/founder/ken-ashe/")
    founder_ld = old_ld("founder/ken-ashe/index.html", full=True)
    assert founder_ld[0].count(PROFILE_OLD) == 1 and founder_ld[0].count('"dateModified": "2026-09-14T17:00:00-04:00"') == 1
    founder_ld[0] = founder_ld[0].replace(PROFILE_OLD, PROFILE_NEW).replace('"dateModified": "2026-09-14T17:00:00-04:00"', f'"dateModified": "{REVISED}T08:00:00-05:00"')
    emit("founder/ken-ashe/index.html", "/founder/ken-ashe/", "founder", pg_founder(ctx), founder_ld, "pg-founder")
    ctx = PCtx("/insights/")
    emit("insights/index.html", "/insights/", "insights", pg_insights(ctx), [page_ld("/insights/", "Insights", "CollectionPage", [("Home", "/"), ("Insights", "/insights/")])], "pg-insights")
    ctx = PCtx("/news/")
    emit("news/index.html", "/news/", "news", pg_news(ctx), old_ld("news/index.html"), "pg-news")
    ctx = PCtx("/contact/")
    emit("contact/index.html", "/contact/", "contact", pg_contact(ctx), old_ld("contact/index.html"), "pg-contact", band=False)
    ctx = PCtx("/404.html")
    emit("404.html", "/404.html", "404", pg_404(ctx), [], "pg-404", band=False, robots="noindex", canonical=False)

    # The June 2026 press release is history. Its headline, text, dates and NewsArticle data stay exactly as
    # published. The shared header, footer, font and script lines follow the rest of the site, and the shared
    # Organization record in its structured data is kept current, as the shared Person record already is.
    old = git_show("news/website-relaunch/index.html")
    ctx = PCtx("/news/website-relaunch/")
    new = re.sub(r'<header class="site-header" id="site-header">.*?</header>', lambda m: pretty_keep(header(ctx)), old, count=1, flags=re.S)
    new = re.sub(r'<footer class="site-footer">.*?</footer>', lambda m: pretty_keep(footer()), new, count=1, flags=re.S)
    new, n = re.subn(r'<link rel="icon" href="/assets/favicon\.ico".*?<link rel="stylesheet" href="/css/styles\.css">', lambda m: HEAD_COMMON, new, count=1, flags=re.S)
    assert n == 1, "could not find the shared head lines in the press release"
    new = new.replace('<a class="skip-link" href="#main">', '<a class="skip-link" href="#main">', 1).replace("<body>", '<body class="rf pg-release">', 1)
    main_old = re.search(r"<main id=\"main\">.*?</main>", old, re.S).group(0)
    assert main_old in new, "the press release body changed"
    new = org_current(new, full=True)
    art = lambda t: re.search(r'\{\s*"@type": "NewsArticle".*?\n    \}', t, re.S).group(0)
    assert art(old) == art(new), "the NewsArticle record changed"
    write("news/website-relaunch/index.html", new)


def build_articles():
    for m in ARTICLES:
        meta = {k: v for k, v in m.items() if not k.startswith("_")}
        meta["related"] = [s for s in meta.get("related", []) if s in BY_SLUG]      # tolerate articles that are not written yet
        write(f"insights/{m['_slug']}/index.html", '<script type="application/json" id="article-meta">\n' + json.dumps(meta, indent=2, ensure_ascii=False)
              + "\n</script>\n<!-- article:start -->\n" + m["_body"] + "\n<!-- article:end -->\n")
    keep = {m["_slug"] for m in ARTICLES}
    for d in (OUT / "insights").iterdir():
        if d.is_dir() and d.name not in keep:
            shutil.rmtree(d)
    r = subprocess.run([sys.executable, str(OUT / "scripts" / "articles.py"), "sync"], capture_output=True, text=True)
    print(r.stdout.strip().splitlines()[0] if r.stdout.strip() else "", r.stderr.strip())
    if r.returncode:
        sys.exit("articles.py sync failed")


def build_assets():
    # one stylesheet: the live file, unchanged, then the approved additions
    live = git_show("css/styles.css").rstrip() + "\n"
    v3 = (SITE / "phase-3/shared/v3.css").read_text()
    v3 = re.sub(r"^/\*.*?\*/\s*", "", v3, count=1, flags=re.S)
    v3 = v3.replace("../../shared/fonts/", "../assets/fonts/")
    v3 = re.sub(r"^\.review[^\n]*\n", "", v3, flags=re.M)
    v3 = re.sub(r"\.review\{font-size:12px\}\.review \.rv-x\{display:none\}", "", v3)
    rf = (SITE / "phase-3/interactive-refined/css/style.css").read_text()
    rf = re.sub(r"^/\*.*?\*/\s*", "", rf, count=1, flags=re.S)
    extra = (HERE / "dp_extra.css").read_text()
    css = (live + "\n/* ==========================================================================\n   Digital presence studio (November 2026). See DECISIONS.md D12.\n"
           "   Everything above this line is the stylesheet as it was before the redesign.\n   The sections below add to it and, where noted, correct it.\n"
           "   ========================================================================== */\n\n/* ---- Shared additions: self-hosted fonts, Services menu, contrast and no-JavaScript fixes ---- */\n"
           + v3.strip() + "\n\n/* ---- Homepage, presence map, diagnostic, light page heroes, service pages, Digital Presence Check ---- */\n" + rf.strip()
           + "\n\n" + extra.strip() + "\n")
    assert ".review" not in css and "shared/fonts" not in css
    write("css/styles.css", css)

    # one script: shared behaviour, the approved interactions, then the contact form exactly as it is on the live site
    v3js = (SITE / "phase-3/shared/v3.js").read_text()
    a = v3js.index("  $$('[data-ba]')"); b = v3js.index("})();", a)
    v3js = v3js[:a] + v3js[b:]
    v3js = re.sub(r"^/\*.*?\*/\s*", "", v3js, count=1, flags=re.S)
    rfjs = (SITE / "phase-3/interactive-refined/js/main.js").read_text()
    rfjs = re.sub(r"^/\*.*?\*/\s*", "", rfjs, count=1, flags=re.S)
    old = git_show("js/main.js")
    form = old[old.index("  // Footer year"):old.rindex("})();")]
    old_map = 'var map = { buying: "Buying a domain", selling: "Selling a domain", website: "Website consult or build", seo: "SEO" };'
    assert old_map in form
    form = form.replace(old_map, "var map = " + json.dumps(DATA["contact"]["needMap"]) + ";")
    form = form.replace("// Prefill the \"I need help with\" select from ?need=buying|selling|website|seo (links on Services and the process page).",
                        "// Prefill the \"I need help with\" select from ?need=website|seo|ai|entity|buying|selling.")
    js = ((HERE / "dp_main_head.js").read_text().rstrip() + "\n" + v3js.strip() + "\n\n" + (HERE / "dp_main_mid.js").read_text().rstrip() + "\n" + rfjs.strip()
          + "\n\n" + (HERE / "dp_main_tail.js").read_text().replace("/*FORM*/", form.rstrip()).rstrip() + "\n")
    assert "data-inert" not in js and "api.web3forms.com/submit" in js
    write("js/main.js", js)

    (OUT / "assets/fonts").mkdir(parents=True, exist_ok=True)
    for f in ("jakarta-normal-400-800.woff2", "inter-normal-400-600.woff2"):
        shutil.copyfile(SITE / "shared/fonts" / f, OUT / "assets/fonts" / f)
    (OUT / "assets/fonts/LICENSE.txt").write_text(
        "Plus Jakarta Sans (jakarta-normal-400-800.woff2) and Inter (inter-normal-400-600.woff2) are variable fonts,\nLatin subset, licensed under the SIL Open Font License 1.1.\n"
        "Plus Jakarta Sans: https://github.com/tokotype/PlusJakartaSans\nInter: https://github.com/rsms/inter\nLicense text: https://openfontlicense.org/\n")
    shutil.copyfile(SITE / "shared/assets/logo-icon-128.png", OUT / "assets/logo-icon-128.png")

    man = json.loads(git_show("site.webmanifest"))
    man["description"] = "Websites, SEO, AI visibility, digital identity, and domains for growing businesses."
    write("site.webmanifest", json.dumps(man, indent=2) + "\n")


def build_sitemap():
    def lastmod(url):
        rel = (url.strip("/") + "/index.html").lstrip("/") if url != "/" else "index.html"
        was = subprocess.run(["git", "-C", str(OUT), "show", f"{BASELINE}:{rel}"], capture_output=True, text=True).stdout
        return LASTMOD if was == (OUT / rel).read_text() else REVISED
    pages = [("/", "1.0", "monthly"), ("/services/", "0.9", "monthly"), ("/services/website-design/", "0.8", "monthly"), ("/services/seo/", "0.8", "monthly"),
             ("/services/ai-visibility/", "0.8", "monthly"), ("/services/entity-seo/", "0.8", "monthly"), ("/services/domain-acquisition/", "0.8", "monthly"),
             ("/how-we-buy-domains/", "0.7", "yearly"), ("/tools/digital-presence-check/", "0.7", "yearly"), ("/about/", "0.6", "yearly"),
             ("/founder/ken-ashe/", "0.7", "yearly"), ("/contact/", "0.7", "yearly"), ("/insights/", "0.7", "monthly"), ("/news/", "0.5", "monthly"),
             ("/news/website-relaunch/", "0.5", "yearly")]
    rows = "\n".join(f"  <url><loc>{DOMAIN}{u}</loc><lastmod>{lastmod(u)}</lastmod><changefreq>{cf}</changefreq><priority>{pr}</priority></url>" for u, pr, cf in pages)
    write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + rows
          + "\n  <!-- Published Insights articles. This block is maintained by scripts/articles.py. Drafts are left out. -->\n  <!-- insights:start -->\n  <!-- insights:end -->\n</urlset>\n")
    print("lastmod:", {u: lastmod(u) for u, _, _ in pages if lastmod(u) == REVISED})


build_assets()
build_pages()
build_articles()
build_sitemap()                 # after the articles, so /insights/ is compared with its final cards
r = subprocess.run([sys.executable, str(OUT / "scripts" / "articles.py"), "sync"], capture_output=True, text=True)   # refill the sitemap's article block
if r.returncode:
    sys.exit("articles.py sync failed: " + r.stderr)
print("production candidate written to", OUT)
