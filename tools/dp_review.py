#!/usr/bin/env python3
"""Write the review page for the staged digital presence production candidate.

    python3 tools/dp_review.py

Writes digital-presence-production-candidate/review/index.html. Reads STAGING.json for the source
commit and tools/dp_results.json (written by hand from the audit, behaviour and performance runs)
for the recorded results. Static page, noindex, review only.
"""
import json, html
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STG = ROOT / "digital-presence-production-candidate"
S = json.loads((STG / "STAGING.json").read_text())
RES = json.loads((ROOT / "tools" / "dp_results.json").read_text())
B = "/luckydomains-design-concepts/digital-presence-production-candidate"
E = html.escape
PR = "https://github.com/kenashe/luckydomains/pull/5"
PR_KA = "https://github.com/kenashe/kenashe/pull/153"
BRANCH = "https://github.com/kenashe/luckydomains/tree/digital-presence-production-candidate"
BLOB = "https://github.com/kenashe/luckydomains/blob/digital-presence-production-candidate/"

PAGES = [("/", "Home"), ("/services/", "Services"), ("/services/website-design/", "Website Design & Development"), ("/services/seo/", "SEO & Search Visibility"),
         ("/services/ai-visibility/", "AI Visibility & Brand Authority"), ("/services/entity-seo/", "Entity SEO & Digital Identity"),
         ("/services/domain-acquisition/", "Domain Acquisition & Brokerage"), ("/how-we-buy-domains/", "How we buy domains"),
         ("/tools/digital-presence-check/", "Digital Presence Check"), ("/about/", "About"), ("/founder/ken-ashe/", "Founder"), ("/insights/", "Insights"),
         ("/news/", "News"), ("/news/website-relaunch/", "June 2026 press release"), ("/contact/", "Contact"), ("/404.html", "404 page")]
STUBS = ["/services.html", "/about.html", "/contact.html", "/how-we-buy-domains.html", "/news/website-relaunch.html"]
ARTICLES = [
 dict(slug="what-ai-search-reads-on-your-website", title="What AI Search Reads When It Reads Your Website", kind="Guide · AI visibility",
      sum="Separates search indexing, live retrieval, and model training, lists each company's published crawlers, sets out what Google says its AI features need and do not need, and ends with what an owner controls and does not.",
      src="Google Search Central (AI features, the generative AI optimization guide, generative AI controls, Google-Extended, JavaScript SEO, structured data), Bing Webmaster Guidelines and the AI Performance announcement, OpenAI, Anthropic, and Perplexity crawler documentation.",
      unc="Google updated its generative AI controls page on November 24, 2026. The article now describes the Search Console control from that page, including that content may be used when no control is applied. No AI company other than Google documents whether its crawlers run JavaScript; the article says so and labels the one study it cites as secondary and from 2024. Recheck the crawler pages on launch day."),
 dict(slug="fix-or-rebuild-your-website", title="When to Fix a Website and When to Rebuild It", kind="Guide · Websites",
      sum="A decision framework: what is usually repairable, the signs the foundation is the problem, a comparison table, five deciding questions, how to protect search visibility in a rebuild, and what a rebuild will not fix.",
      src="Google Search Central (site moves, redirects, page experience, mobile-first indexing, helpful content), web.dev Web Vitals, W3C WCAG 2.2, and this repository's decision log for the first-party example.",
      unc="Google has no documentation page on redesigns that keep the same URLs, so the article quotes its site-move guidance. The sentence that the late 2026 redesign kept every address becomes true only when this candidate launches."),
 dict(slug="entity-seo-for-founders", title="Entity SEO for Founders: One Name, Many Profiles", kind="Explainer · Digital identity",
      sum="Why a founder's identity fragments, choosing one authoritative page, consistency, Person and Organization structured data, bylines, sharing a name, what Google says about Knowledge Panels, and why independent recognition cannot be self-written.",
      src="Google Knowledge Panel Help, Google Search Central (ProfilePage, Organization, Article author markup, structured data guidelines, helpful content), Schema.org, and Google's 2012 Knowledge Graph announcement.",
      unc="Google publishes no method for telling apart people with the same name; the article says so. The first-party example describes Ken's Person record (one identifier, 19 profile links, four credentials) and claims no Knowledge Panel."),
 dict(slug="how-a-private-domain-purchase-works", title="How a Private Domain Purchase Actually Works", kind="Explainer · Domains",
      sum="A general guide, separate from the Lucky Domains process page: what taken means, finding the holder, trademark and history checks, valuation, anonymous outreach, negotiation, escrow, the transfer, common mistakes, and when to walk away.",
      src="ICANN (lookup, RDAP, Registration Data Policy, Transfer Policy, domain life cycle, UDRP, registrant responsibilities), WIPO, USPTO, Escrow.com's own documentation, the Internet Archive, and Google's guidance on old domains.",
      unc="ICANN's Board adopted a revised Transfer Policy in June 2026. On November 25, 2026 it was still in ICANN's implementation queue with no effective date. The article states the current 60-day rules, dates that check, and separates generic endings from country-code endings. Recheck on launch day. Not shortened, by the owner's decision. The scope note and the escrow limits added about 190 words, so it is now about 1,800."),
 dict(slug="domains-identity-for-ai-agents", title="Can Domains Become the Identity Layer for AI Agents?", kind="Research · Agent identity",
      sum="The existing research note, expanded and kept exploratory: what a domain already does, what an agent identity would need, the domain-anchored proposals and the blockchain naming proposals, Ken's two experiments and their limits, and what is unresolved.",
      src="The two KenAshe.ai build records, the A2A specification, the MCP Registry documentation, the IETF working group and two Internet-Drafts, ENS documentation, ERC-8004, x402, NIST, and the OpenID Foundation.",
      unc="Almost everything cited is a draft, and several expire in 2027. All six claims about ZeroHuman and the earlier experiment were rechecked against the build records and on-chain on November 24, 2026. The latest dated statement that no outside agent has bought is November 20, 2026."),
]
CHANGED = [
 "Ported into the production repository as plain HTML, one stylesheet and one script. No build step, no framework.",
 "Production URLs: the founder page stays at /founder/ken-ashe/ and the domain service lives at /services/domain-acquisition/. Every existing URL is kept.",
 "Review banners, concept labels and noindex removed from the source. Staging adds its own notice and noindex.",
 "The real contact form replaces the inert one: Web3Forms, the honeypot, validation, success and error states, and the mailto fallback, exactly as on the live site. Inquiry options now match the five services.",
 "Insights is a library of five complete articles. The planned-article cards and the Coming labels are gone.",
 "The services section explains three related services (SEO, Entity SEO, AI Visibility), not two.",
 "Each service page and the process page end with a Related reading list.",
 "The News page lists only the real June 2026 release. The sample announcement is removed.",
 "The sitewide footer no longer links to KenAshe.ai. The repository's rule keeps founder profile links on the founder page; KenAshe.ai is linked where it is the source.",
 "Full metadata on every page: unique title and description, canonical, Open Graph, and structured data.",
]
DECISIONS = [
 "SEO engagements: Growth SEO as a monthly package is removed everywhere. The engagement is named SEO Audits & Optimization: one-time audits, scoped implementation projects, and ongoing optimization and monitoring by agreement.",
 "AI Visibility: the approved explanation is kept. No first-party AI experiment is claimed. Founder commentary appears only on the Founder page, labeled as opinion.",
 "No portfolio: no Work navigation, case studies, logos, testimonials, or results. The test suite fails if any return.",
 "Founder: about 20 years working with HTML, CSS, websites, and WordPress, and more recently AI-assisted development. It is not described as professional software engineering. The four published items are approved: two TechRound pieces, the HackerNoon article, and the ProjectManagement.com article.",
 "Location: Berkeley Heights, New Jersey, on Contact, About, News, the footer, and in the Organization data.",
 "News: historical release untouched. No new announcement written.",
 "Articles: all five are kept, with the byline By Ken Ashe. They stay editorial drafts with no publication date, noindex and outside the sitemap, until Ken approves the text. All five then take the actual launch date.",
 "Digital Presence Check: unchanged from the approved version.",
]
CORRECTION = ("One factual correction to the approved concept. It said the Autonomous SEO Agent maintains Lucky Domains profiles. The public build record does not say whose profiles it maintains, "
              "so the candidate describes it as an internal system the founder built and quotes the record's own figures (63 sites researched, eight profiles confirmed live, no SEO impact established).")
SEO = [
 "No existing URL changes, so no redirects are needed at launch.",
 "The five legacy .html redirect stubs are byte for byte unchanged and stay crawlable.",
 "The /services/ page keeps the #websites, #seo, #domains and #selling anchors, because KenAshe.ai posts link to them through the services.html stub.",
 "Every page has a self-referencing canonical on https://luckydomains.io with a trailing slash, matching its internal links and its sitemap entry.",
 "The sitemap lists every indexable page. An article joins it when it is published.",
 "robots.txt is unchanged and blocks no duplicate URL forms.",
 "Structured data: Organization, WebSite, ProfilePage and the shared Person on the home page; Service, WebPage and BreadcrumbList on each service page; Article and BreadcrumbList on each article. The shared Person node is byte-identical to the live copy.",
 "Staging URLs appear nowhere in the source. The test suite checks for them.",
]
EDITS = [
 ("When to Fix a Website and When to Rebuild It", [
   "The opening no longer says most disappointing websites do not need replacing. It says a disappointing site does not automatically need replacing.",
   "The five questions are introduced as practical guidance, not a validated scoring system, and the outcomes are worded as rules of thumb.",
   "\"An address that does not change cannot be lost\" is gone. Keeping an address lowers migration risk and does not remove it, with Google's own sentence on ranking fluctuations after any significant change.",
   "Softened: \"the riskiest moment\", \"always larger than expected\", \"rarely works\", \"cheap and certain\", and a claim about what most organizations aim for."]),
 ("How a Private Domain Purchase Actually Works", [
   "Escrow now reduces the central transaction risk. The text says what it does not cover: trademarks, the name's history, the price, and deals outside the service's process.",
   "A scope note near the top separates ICANN's rules for generic endings (.com, .net, .org) from country-code endings (.uk, .de, .io), quoting ICANN.",
   "The transfer-policy warning is dated: on November 25, 2026 the revised policy was still queued with no effective date.",
   "Factual correction: Escrow.com is now described in the words of its own page (\"licensed as an escrow service\", \"regularly audited by each state's regulatory agency\"). The earlier quoted phrase could not be confirmed there.",
   "Factual correction: the lookup tool sentence no longer gives a date for RDAP replacing WHOIS.",
   "Removed an unsupported claim about how often owners reply. Softened \"the normal case\", \"most\", \"never send money\", and \"every time\". Length kept."]),
 ("What AI Search Reads When It Reads Your Website", [
   "All crawler documentation was reread on November 25, 2026 and the article says so.",
   "OpenAI's sentence now carries its own qualifier: sites opted out of OAI-SearchBot \"can still appear as navigational links\".",
   "Google's Search generative AI control is described from its documentation: what it excludes, that content may be used when no control is applied, and that it does not affect model training or other parts of Search.",
   "Softened: \"most confusion\", \"most AI companies\", \"none of this is exotic\", and the claim that anyone citing selection rules is guessing."]),
 ("Can Domains Become the Identity Layer for AI Agents?", [
   "Proof of control is now separated from identity. Controlling a domain or a key shows who holds it. It does not show who the operator is in the real world, or that the operator is competent or trustworthy.",
   "The same distinction is applied to certificates and to ZeroHuman: the name shows where results come from, not who runs the service or whether to trust it.",
   "ZeroHuman's documented limits are all kept (no outside buyer as of November 20, 2026, Ken's own test buyer, no escrow, draft specifications), and that one is added."]),
 ("Entity SEO for Founders: One Name, Many Profiles", [
   "Removed an unsupported sentence about what founders ask for most.",
   "Softened absolutes about who is responsible, what most founders use, how systems weigh properties, and what can be done about a shared name."]),
]
STRUCTURED = [
 "Founder page: the ProfilePage description now reads \"Profile of Ken Ashe, CPA, PMP, founder and operator of Lucky Domains, a digital presence studio for the AI era.\" Its dateModified is November 25, 2026.",
 "One Organization record. The full Organization node appears on the home page, the founder page and the June 2026 press release. All three now carry the same description, topics and city-level address. Before this pass the founder page and the release still listed the old topics.",
 "The press release itself is untouched: headline, text, dates and NewsArticle data are exactly as published. Only the shared company record inside its structured data was brought up to date, the way the shared founder record already is.",
 "Articles refer to the shared founder record with the same URL it has everywhere else (kenashe.ai), and name the publisher. Before, the same record was given a second URL.",
 "The shared Ken Ashe Person record is unchanged and still byte-identical to the live copy on all three pages.",
 "SEO service data lists audits, technical reviews, scoped projects, strategy, and ongoing work by agreement.",
 "Sitemap dates: the five pages changed in this pass carry November 25, 2026. The others keep November 24, 2026.",
 "KenAshe.ai: every current description on the pull request branch was checked. Its only structured reference to Lucky Domains uses the same Organization identifier and no description, so nothing conflicts. Dated posts and the site-launch release were left alone.",
 "New tests fail the build if the Organization description, topics or address ever differ between pages, if a second company identity appears, or if the founder record is given a second URL.",
]
DIGEST = ("In the Digest prompt on KenAshe.ai, one clause changed. From: \"a domain acquisition, brokerage, website-build, and white-hat SEO practice.\" "
          "To: \"a digital presence studio for the AI era that offers website design and development, SEO, AI visibility, digital identity, and domain acquisition and brokerage.\" "
          "The subjects that trigger a mention, the example sentence, the five existing links, the link guardrail, the schedule and the models are unchanged. "
          "It is a separate commit in the KenAshe.ai pull request, so it can be dropped on its own. It could not be shadow-tested from the build environment; the pipeline's own tests give the same result before and after (73 pass, three files cannot load there).")
SAFARI_MAC = [
 "Home: fonts look right, the navy hero fills the width, and the map settles from scattered to connected.",
 "Click a signal, click it again, switch Fragmented and Recognized, press Pause.",
 "Press Tab from the top: a green outline shows on each stop, and Escape closes the Services menu.",
 "Choose each \"What is holding you back?\" option: an answer appears beside it and the page does not jump.",
 "Scroll to the five layers: the line draws once and nothing sticks.",
 "Open a service page, then the Digital Presence Check: answer a few and use Clear answers.",
 "Open an article: the contents list stays beside the text and the table scrolls in its own box.",
 "Narrow the window to phone width: nothing scrolls sideways.",
]
SAFARI_PHONE = [
 "Home fits without sideways scrolling, in portrait and landscape.",
 "Open the menu, open Services inside it, close it.",
 "Tap a signal on the map and tap Pause. Nothing is cut off.",
 "Tap a \"What is holding you back?\" option: the answer appears just below.",
 "Digital Presence Check: the three answer buttons are easy to tap and the result updates.",
 "One article: comfortable to read, contents box above the text, wide table scrolls by itself.",
 "Contact: fields do not zoom the page. Send shows a notice and sends nothing here.",
 "Turn on Reduce Motion and reload the home page: the map appears connected and nothing moves.",
]
EDITORIAL = [
 "Approve the final text of each of the five articles.",
 "Approve the byline, By Ken Ashe.",
 "Choose the launch day. All five articles take that date.",
 "Complete the Safari check on the MacBook and the iPhone.",
]
BLOCKERS = [
 "Ken's approval of the final article text and the byline.",
 "Ken's choice of launch day.",
 "The Safari check on a MacBook and an iPhone. WebKit could not run in the build environment.",
 "After launch only: one real contact form submission from a browser, the www redirect, the legacy stubs, and the 404 page on the live domain.",
]
DEPLOY = [
 "Ken approves the articles, the byline and the launch day, and completes the Safari check.",
 "Bring the branch up to date with main and re-export staging if anything changed.",
 "On launch day, reopen the time-sensitive sources (ICANN transfer policy status, Google's AI controls, the crawler pages) and correct the articles if anything moved.",
 "Run the final publication command (below). It dates all five articles with the launch day and runs the launch tests.",
 "Commit and push. CI must be green on the pull request.",
 "Record the commit that is live (the rollback point). When the candidate was prepared it was efed1de.",
 "Ken marks the pull request ready and merges it with a merge commit, the same day. GitHub Pages redeploys within minutes.",
 "Run python3 scripts/verify_live.py, then check the live site in Safari and Chrome: navigation, the map, the check, one article, the legacy stubs, the 404 page.",
 "Send one real contact form message from a browser and confirm it arrives.",
 "Resubmit the sitemap in Search Console.",
 "Only then merge the KenAshe.ai pull request.",
]
SHOTS = [("home-desktop", "Home, desktop", 1440, 900), ("presence-map", "Presence map", 592, 600), ("diagnostic", "Problem diagnostic", 1440, 520), ("five-layers", "Five layers", 1440, 620),
         ("services", "Services overview", 1440, 900), ("website-design", "Website Design", 1440, 900), ("seo", "SEO", 1440, 900), ("ai-visibility", "AI Visibility", 1440, 900),
         ("entity-seo", "Entity SEO", 1440, 900), ("domain-acquisition", "Domain Acquisition", 1440, 900), ("digital-presence-check", "Digital Presence Check", 1440, 900),
         ("insights", "Insights library", 1440, 900), ("article", "Article, desktop", 1440, 900), ("about", "About", 1440, 900), ("founder", "Founder", 1440, 900), ("contact", "Contact", 1440, 900),
         ("home-mobile", "Home, mobile", 375, 760), ("article-mobile", "Article, mobile", 375, 760), ("service-mobile", "Service page, mobile", 375, 760), ("check-mobile", "Check, mobile", 375, 760)]

edits = "".join(f'<div class="ed-a"><h3>{E(t)}</h3>' + '<ul class="chg">' + "".join(f"<li>{E(x)}</li>" for x in items) + "</ul></div>" for t, items in EDITS)
ul = lambda items, cls="chg": f'<ul class="{cls}">' + "".join(f"<li>{E(x)}</li>" for x in items) + "</ul>"
ol = lambda items: '<ol class="chg">' + "".join(f"<li>{E(x)}</li>" for x in items) + "</ol>"
links = "".join(f'<li><a href="{B}{p}">{E(n)}</a></li>' for p, n in PAGES)
arts = "".join(f'<li><a href="{B}/insights/{a["slug"]}/">{E(a["title"])}</a></li>' for a in ARTICLES)
stubs = "".join(f'<li><a href="{B}{p}">{E(p)}</a></li>' for p in STUBS)
art_rows = "".join(f'<tr><th scope="row"><a href="{B}/insights/{a["slug"]}/">{E(a["title"])}</a><br><span class="rv-s">{E(a["kind"])} · {RES["words"][a["slug"]]:,} words</span></th>'
                   f'<td data-c="What it covers">{E(a["sum"])}</td><td data-c="Principal sources">{E(a["src"])}</td><td data-c="Uncertainties">{E(a["unc"])}</td></tr>' for a in ARTICLES)
url_rows = "".join(f'<tr><th scope="row">{E(a)}</th><td data-c="Status">{E(b)}</td></tr>' for a, b in [
    ("/, /services/, /services/entity-seo/, /how-we-buy-domains/, /about/, /founder/ken-ashe/, /contact/, /news/, /news/website-relaunch/", "Preserved. Same URL, same file path."),
    ("/services.html, /about.html, /contact.html, /how-we-buy-domains.html, /news/website-relaunch.html", "Preserved, unchanged. Legacy redirect stubs."),
    ("/services/website-design/, /services/seo/, /services/ai-visibility/, /services/domain-acquisition/", "New service pages."),
    ("/tools/digital-presence-check/", "New. There is no /tools/ index page until there is a second tool."),
    ("/insights/ and five article URLs under it", "New."),
    ("/work/, /portfolio/", "Never created.")])
perf = RES.get("perf")
if perf:
    prow = "".join(f'<tr><th scope="row">{E(n)}</th><td data-c="Phone: first paint">{v["phone"]["fcp"]/1000:.1f} s</td><td data-c="Phone: main content">{v["phone"]["lcp"]/1000:.1f} s</td>'
                   f'<td data-c="Layout shift">{v["phone"]["cls"]:.2f}</td><td data-c="Blocking time">{v["phone"]["tbt"]:.0f} ms</td><td data-c="Transfer">{v["desktop"]["kb"]:.0f} KB</td>'
                   f'<td data-c="Requests">{v["desktop"]["requests"]:.0f}</td></tr>' for n, v in perf["pages"].items())
    perf_html = (f'<table class="t2"><thead><tr><th scope="col">Page</th><th scope="col">First paint</th><th scope="col">Main content</th><th scope="col">Layout shift</th><th scope="col">Blocking time</th>'
                 f'<th scope="col">Transfer</th><th scope="col">Requests</th></tr></thead><tbody>{prow}</tbody></table>'
                 f'<p class="state-s">{E(RES["perfNote"])}</p>')
else:
    perf_html = '<p class="state-s">Measured on the published staging copy. Figures are added after the first deployment.</p>'
gal = "".join(f'<figure><a href="screenshots/{f}.jpg"><img src="screenshots/{f}.jpg" alt="Staged production candidate: {E(t)}" width="{w}" height="{h}" loading="lazy"></a><figcaption>{E(t)}</figcaption></figure>' for f, t, w, h in SHOTS)

page = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex,nofollow,noarchive">
<title>Staging review | Lucky Domains production candidate</title>
<meta name="description" content="Review notes for the staged Lucky Domains production candidate. Review only, not the live site.">
<link rel="icon" href="/luckydomains-design-concepts/shared/assets/favicon.ico" sizes="any">
<link rel="stylesheet" href="/luckydomains-design-concepts/shared/review.css">
<link rel="stylesheet" href="/luckydomains-design-concepts/phase-2/shared/review-p2.css">
<link rel="stylesheet" href="/luckydomains-design-concepts/phase-3/shared/review-p3.css">
<style>.rv-s{{font-weight:400;font-size:13.5px;color:var(--soft)}}.rv-cols{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:4px 32px}}.rv-cols ul{{margin:0 0 14px;padding-left:20px}}.rv-cols li{{font-size:15.5px;margin-bottom:4px}}
.t4{{table-layout:fixed}}.rv-two{{grid-template-columns:repeat(2,minmax(0,1fr))}}.rv-two ol{{margin:0 0 14px;padding-left:22px}}.rv-cmd{{background:#0f1720;color:#e6edf3;padding:14px 16px;border-radius:8px;overflow-x:auto;font-size:14px}}.rv-cmd code{{background:none;color:inherit;padding:0}}.ed-a{{margin:0 0 18px}}.ed-a h3{{margin-bottom:6px}}@media (max-width:1000px){{.rv-two{{grid-template-columns:1fr}}}}
.t4 thead th{{width:27%}}.t4 thead th:first-child{{width:19%}}.refine code{{font-size:.92em;background:#eef0f2;padding:1px 5px;border-radius:4px}}@media (max-width:1000px){{.rv-cols{{grid-template-columns:1fr}}}}</style>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="top">
  <a href="{B}/review/" aria-label="Lucky Domains, staging review"><img src="/luckydomains-design-concepts/shared/assets/logo-wordmark.png" alt="Lucky Domains" width="194" height="48"></a>
  <nav aria-label="Review"><a href="{B}/">Staged site</a><a href="{B}/review/" aria-current="page">Review notes</a><a href="/luckydomains-design-concepts/phase-3/interactive-refined/">Approved design</a><a href="/luckydomains-design-concepts/phase-3/">Version 3</a></nav>
</header>
<main id="main">
<section class="intro"><p class="k">Production candidate · Final pre-launch review · November 25, 2026</p><h1>The new Lucky Domains site, staged for approval</h1>
<p class="lead">This is the actual production candidate, exported from the branch <a href="{BRANCH}">digital-presence-production-candidate</a> at commit <code>{S['source_commit'][:10]}</code>. It is not another design concept. Nothing here is live on LuckyDomains.io, and nothing will be until Ken approves it.</p>
<p class="go-row"><a class="btn" href="{B}/">Open the staged site</a><a class="btn btn-l" href="{B}/insights/">Read the five articles</a><a class="btn btn-l" href="{B}/tools/digital-presence-check/">Digital Presence Check</a></p>
<p class="go-row"><a class="btn btn-l" href="{PR}">Lucky Domains draft pull request</a><a class="btn btn-l" href="{PR_KA}">KenAshe.ai draft pull request</a></p>
<p class="state">The live LuckyDomains.io and KenAshe.ai sites were not changed. Both pull requests are drafts and unmerged. Staging pages are noindex, the contact form is disabled here, and nothing is collected.</p></section>

<section class="refine" aria-labelledby="wt-h"><h2 id="wt-h">Waiting on Ken</h2>{ol(EDITORIAL)}
<p class="state-s">Nothing else is outstanding. The design, structure, positioning and implementation are approved, and no further design work is planned.</p></section>

<section class="refine" aria-labelledby="pg-h"><h2 id="pg-h">Every staged page</h2>
<div class="rv-cols"><div><h3>Pages</h3><ul>{links}</ul></div><div><h3>Insights articles</h3><ul>{arts}</ul><h3>Legacy redirect stubs</h3><ul>{stubs}</ul></div>
<div><h3>How to review</h3><ul><li>Start on the home page and use the site as a visitor would.</li><li>Read each article in full. They are the largest new piece of writing.</li><li>Try the site on your own phone, and in Safari.</li><li>The form shows a notice here and sends nothing.</li></ul></div></div></section>

<section class="refine" aria-labelledby="ch-h"><h2 id="ch-h">What changed from the approved design</h2>
<p class="lead">The design is the approved one. These are the differences between the refined concept and this candidate.</p>{ul(CHANGED)}
<p class="state-s">{E(CORRECTION)}</p></section>

<section class="refine" aria-labelledby="dc-h"><h2 id="dc-h">Final content decisions, as applied</h2>{ul(DECISIONS)}</section>

<section class="refine" aria-labelledby="ed-h"><h2 id="ed-h">Final editorial pass, November 25</h2>
<p class="lead">No article was rewritten. These are the corrections, by article. Every quotation in all five was checked against its source on November 25, 2026.</p>
{edits}</section>

<section class="refine" aria-labelledby="sd-h"><h2 id="sd-h">Structured data and consistency corrections</h2>{ul(STRUCTURED)}
<h3>Digest prompt, exact change</h3><p>{E(DIGEST)}</p></section>

<section class="tbl v2c" aria-labelledby="ar-h"><h2 id="ar-h">Article inventory</h2>
<p class="lead">Five complete articles. Every source was reopened on November 25, 2026, and every quotation was checked against it. Nothing in them is an invented client, statistic, quotation, or result.</p>
<table class="t4"><thead><tr><th scope="col">Article</th><th scope="col">What it covers</th><th scope="col">Principal sources</th><th scope="col">Uncertainties to know about</th></tr></thead><tbody>{art_rows}</tbody></table>
<p class="state-s">How to add, edit and publish an article: <a href="{BLOB}docs/INSIGHTS.md">docs/INSIGHTS.md</a> in the production repository.</p></section>

<section class="tbl v2c" aria-labelledby="ur-h"><h2 id="ur-h">URLs</h2>
<table class="t2"><thead><tr><th scope="col">URL</th><th scope="col">Status</th></tr></thead><tbody>{url_rows}</tbody></table>
<p class="state-s">The complete map is <a href="{BLOB}docs/URL_MAP.md">docs/URL_MAP.md</a>.</p>
<h3>SEO migration approach</h3>{ul(SEO)}</section>

<section class="refine" aria-labelledby="ts-h"><h2 id="ts-h">Test results</h2>{ul(RES["tests"])}
<h3>Load measurements</h3>{perf_html}
<h3>Limits</h3>{ul(RES["limits"])}</section>

<section class="refine" aria-labelledby="sf-h"><h2 id="sf-h">Safari check for Ken</h2>
<p class="lead">About ten minutes, on this staging copy. Note the page, the device and what you saw if anything looks wrong.</p>
<div class="rv-cols rv-two"><div><h3>MacBook, Safari</h3>{ol(SAFARI_MAC)}</div><div><h3>iPhone, Safari</h3>{ol(SAFARI_PHONE)}</div></div>
<h3>Launch blockers</h3>{ul(BLOCKERS)}</section>

<section class="refine" aria-labelledby="dp-h"><h2 id="dp-h">Production deployment and rollback</h2>
<p class="lead">Prepared, not executed. The full procedures are in <a href="{BLOB}docs/RUNBOOK.md">docs/RUNBOOK.md</a>, sections 9 and 10.</p>{ol(DEPLOY)}
<h3>Final publication command</h3><p>Run on launch day, on the branch, before the merge:</p>
<pre class="rv-cmd"><code>python3 scripts/articles.py publish --all --date "$(TZ=America/New_York date +%F)" \\
  &amp;&amp; python3 tests/test_site.py --launch</code></pre>
<p class="state-s">It removes the draft marking from all five articles, writes the launch date into each byline and its structured data, adds the articles to the sitemap, and then runs the launch tests. If the merge slips to another day, run it again with <code>--redate</code> after the date.</p>
<h3>Rollback</h3><p>GitHub Pages serves whatever main contains, so a rollback is one commit: revert the merge commit with <code>git revert -m 1</code>, run the tests, and push. Do not force push, delete CNAME, or touch DNS. The old pages are live again within minutes. That is why the KenAshe.ai links are merged last.</p></section>

<section class="refine" aria-labelledby="st-h"><h2 id="st-h">What staging changes, and nothing else</h2>{ul(S["transformations"])}
<p class="state-s">Exported by <code>tools/dp_export.py</code> from {S['files']} source files. The export refuses to run from main or with uncommitted changes, and checks each protection before it finishes. Staging cannot show the real contact form delivering mail, the www redirect, or the 404 page being served for a missing path.</p></section>

<section class="gal p2-gals" aria-labelledby="g-h"><h2 id="g-h">Screenshots</h2><div class="p2-gal rf-gal">{gal}</div>
<p class="rf-full">Full-length captures: <a href="screenshots/home-desktop-full.jpg">home, desktop</a>, <a href="screenshots/home-mobile-full.jpg">home, mobile</a>, <a href="screenshots/article-full.jpg">article, desktop</a>, <a href="screenshots/article-mobile-full.jpg">article, mobile</a>.</p></section>
</main>
<footer class="bot"><p>The live LuckyDomains.io and KenAshe.ai sites were not changed.</p><p>Staging review for Ken Ashe. Not the live Lucky Domains website. Not indexed. <a href="https://github.com/kenashe/luckydomains-design-concepts">Review repository</a>.</p></footer>
</body></html>
"""
out = STG / "review" / "index.html"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(page)
print("wrote", out.relative_to(ROOT))
