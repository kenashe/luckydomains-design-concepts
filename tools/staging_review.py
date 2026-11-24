#!/usr/bin/env python3
"""Write the staging review dashboard at production-candidate/review/index.html.

    python3 tools/staging_review.py

Static page. Reads production-candidate/STAGING.json for the source commit and page list.
The results below are the measurements recorded on 2026-11-23. Update them when checks are re-run.
"""
import json, html
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
S = json.loads((ROOT / "production-candidate" / "STAGING.json").read_text())
B = "/luckydomains-design-concepts/production-candidate"
E = html.escape
PAGES = [("/", "Home"), ("/ventures/", "Ventures"), ("/ventures/zerohuman/", "ZeroHuman"), ("/ventures/ai-agent-economy/", "AI Agent Economy"),
         ("/ventures/autonomous-seo-agent/", "Autonomous SEO Agent"), ("/services/", "Services"), ("/services/entity-seo/", "Entity SEO"),
         ("/how-we-buy-domains/", "How we buy domains"), ("/about/", "About"), ("/founder/ken-ashe/", "Founder"), ("/news/", "News"),
         ("/news/website-relaunch/", "June 2026 release"), ("/contact/", "Contact"), ("/404.html", "404 page")]
STUBS = ["/services.html", "/about.html", "/contact.html", "/how-we-buy-domains.html", "/news/website-relaunch.html"]
SHOTS = [("pc-home-desktop", "Home, desktop"), ("pc-home-tablet", "Home, tablet"), ("pc-home-mobile", "Home, mobile"), ("pc-ventures", "Ventures"),
         ("pc-zerohuman", "ZeroHuman"), ("pc-services", "Services"), ("pc-domain-desk", "Domain Desk"), ("pc-about", "About"), ("pc-founder", "Founder"), ("pc-contact", "Contact")]
COPY = ["Company description: \u201cLucky Domains is a founder-led digital venture studio that builds and operates AI applications, digital identity systems, and internet-native ventures. Domain acquisition and brokerage remain active.\u201d",
        "\u201cInternet-native ventures\u201d is the only phrase used. The tests reject the variants.",
        "Build: AI applications and internet-native ventures. Operate: autonomous services, internal systems, and digital identities. Acquire: private domain acquisition and brokerage for clients.",
        "Beside ZeroHuman: \u201cBuilt by Ken Ashe. Operated by Lucky Domains. Read the full build record on KenAshe.ai.\u201d",
        "Relationship labels: A Lucky Domains venture, A Lucky Domains experiment, A Lucky Domains internal system.",
        "Ventures page opens with \u201cWhat Lucky Domains builds, runs, tests, and offers.\u201d",
        "All design-review language removed: no concept notice, no \u201cproposed positioning\u201d, no facts-as-of line, no review links.",
        "\u201cNaming across DNS and ENS\u201d removed as a service. ENS appears only as first-party experience.",
        "Founder page no longer leads with the accountant and SEO practice framing. Portrait, credentials, career, speaking and Forbes Business Council membership are kept.",
        "About page: five-step evolution, \u201cFortune favors the prepared.\u201d as operating philosophy, company-only timeline. Speaking appearances moved to the Founder page.",
        "Retired from the old site: engagement tiers, local SEO, authority and links, monthly reporting, the home FAQ and the home fit section."]
QUESTIONS = ["Sir Pitches-a-Lot: the KenAshe.ai build index says June 2026 and its build page says August 2026. No date is shown.",
             "\u201cLongtime Bitcoin and Ethereum participant\u201d: no public source states how long, so the Founder page says only that his public focus areas include AI agents, Bitcoin, digital identity, and domain names.",
             "Autonomous SEO Agent counts (63 researched, 8 live) come from an undated build record.",
             "ZeroHuman: the no-outside-purchase limitation is dated November 20, 2026 and stays until the build record changes.",
             "No announcement of the new positioning has been approved, so none is published. News shows the June release and dated project updates.",
             "One real contact-form submission could not be made from the build environment. It is step 9 of the launch checklist."]
LAUNCH = ["Owner reviews staging.", "Owner approves both draft pull requests.", "Rebase the branch on the current main.", "Re-run the tests and browser checks.",
          "Record the current production commit for rollback.", "Merge the Lucky Domains pull request to main.", "Watch the GitHub Pages deployment finish.",
          "Run python3 scripts/verify_live.py.", "Test the live contact form in a browser, once.", "Verify canonicals, robots, sitemap, Open Graph, structured data and the legacy stubs.",
          "Verify the www redirect.", "Verify MX and TXT records are unchanged.", "Review in Safari on a Mac and on an iPhone.", "Resubmit the sitemap in Search Console.",
          "Merge the KenAshe.ai cross-link pull request, only after the Lucky Domains pages are live.", "Capture final screenshots.", "Roll back at once if anything critical fails."]

def li(items, tag="ul"): return f"<{tag}>" + "".join(f"<li>{E(x)}</li>" for x in items) + f"</{tag}>"

page = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex,nofollow,noarchive">
<title>Production candidate review | Lucky Domains staging</title>
<meta name="description" content="Staging review for the Lucky Domains Venture Lab production candidate. Not the live site.">
<link rel="icon" href="/luckydomains-design-concepts/shared/assets/favicon.ico" sizes="any">
<link rel="stylesheet" href="/luckydomains-design-concepts/shared/review.css">
<style>.pg-l{{columns:2;column-gap:40px;padding-left:20px}}.pg-l li{{margin-bottom:6px;break-inside:avoid}}.kv{{width:100%}}.kv th{{width:32%}}.cmp{{display:grid;grid-template-columns:1fr 1fr;gap:20px}}.sec{{max-width:1240px;margin:0 auto;padding:8px clamp(18px,4vw,48px) clamp(28px,4vw,48px)}}.sec h2{{font-size:clamp(24px,2.6vw,32px);margin:0 0 16px}}.sec ul,.sec ol{{max-width:62em;padding-left:22px}}.sec li{{margin-bottom:6px}}@media(max-width:800px){{.pg-l{{columns:1}}.cmp{{grid-template-columns:1fr}}}}</style>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="top">
  <a href="{B}/" aria-label="Lucky Domains staging home"><img src="/luckydomains-design-concepts/shared/assets/logo-wordmark.png" alt="Lucky Domains" width="194" height="48"></a>
  <nav aria-label="Review"><a href="{B}/">Staged site</a><a href="{B}/review/" aria-current="page">Review notes</a><a href="/luckydomains-design-concepts/">Design concepts</a></nav>
</header>
<main id="main">
<section class="intro">
  <p class="k">Staging review, November 23, 2026</p>
  <h1>Production candidate</h1>
  <p class="lead">The approved Venture Lab v2 design, ported to the production repository on a branch and exported here for review. This is a staging copy. It is not indexed and its contact form is disabled.</p>
  <p class="state">The live sites are unchanged. Nothing has been merged or deployed to LuckyDomains.io or KenAshe.ai. No DNS, GitHub Pages setting, form, or integration was touched.</p>
  <p class="go"><a class="btn" href="{B}/">Open the staged site</a></p>
</section>

<section class="sec"><h2>Approved positioning</h2>
<ul><li><b>Lucky Domains</b> is a founder-led digital venture studio and operating company. It builds AI applications, operates autonomous services and internal systems, develops digital identity systems, explores internet-native ventures, and continues its original domain acquisition and brokerage practice.</li>
<li><b>Ken Ashe</b> builds and documents in public. KenAshe.ai holds the full build records.</li>
<li><b>Standalone brands</b> face their own users or customers.</li>
<li><b>Domain brokerage</b> remains an active Lucky Domains service.</li></ul>
<table class="kv"><tbody>
<tr><th scope="row">ZeroHuman</th><td>Autonomous service, LIVE. A Lucky Domains venture. Built by Ken Ashe, operated by Lucky Domains.</td></tr>
<tr><th scope="row">AI Agent Economy</th><td>Experiment, SHIPPED. A Lucky Domains experiment.</td></tr>
<tr><th scope="row">Autonomous SEO Agent</th><td>Internal operating system, LIVE. A Lucky Domains internal system.</td></tr>
<tr><th scope="row">Domain Acquisition and Brokerage</th><td>Commercial service, ACTIVE.</td></tr>
<tr><th scope="row">Sir Pitches-a-Lot</th><td>Competition agent, SHIPPED, in the experiments group. No date shown.</td></tr>
<tr><th scope="row">LuckyDomains.io</th><td>Studio build, LIVE.</td></tr></tbody></table></section>

<section class="sec"><h2>Every staged page</h2>
<ol class="pg-l">{"".join(f'<li><a href="{B}{p}">{E(n)}</a> <span style="color:#566170">{E(p)}</span></li>' for p, n in PAGES)}</ol>
<p>Legacy redirect stubs, unchanged from production: {", ".join(f'<a href="{B}{p}">{E(p)}</a>' for p in STUBS)}. Each one sends you to its directory URL.</p></section>

<section class="sec"><h2>Current production and the candidate</h2>
<div class="cmp"><figure><img src="screenshots/live-home-desktop.jpg" alt="The current live LuckyDomains.io home page" width="1440" height="900" loading="lazy"><figcaption>Live today (read only capture, November 23, 2026)</figcaption></figure>
<figure><a href="{B}/"><img src="screenshots/pc-home-desktop.jpg" alt="The production candidate home page on staging" width="1440" height="900" loading="lazy"></a><figcaption>Production candidate</figcaption></figure></div></section>

<section class="gal"><h2>Screenshots</h2><div class="gal-g">{"".join(f'<figure><img src="screenshots/{f}.jpg" alt="{E(c)}, production candidate" width="1440" height="900" loading="lazy" style="max-height:520px;width:auto"><figcaption>{E(c)}</figcaption></figure>' for f, c in SHOTS)}</div></section>

<section class="sec"><h2>Production copy changes</h2>{li(COPY)}</section>

<section class="sec"><h2>URLs</h2>
<p><b>Preserved (10 pages, 5 stubs):</b> /, /services/, /services/entity-seo/, /how-we-buy-domains/, /about/, /founder/ken-ashe/, /news/, /news/website-relaunch/, /contact/, /404.html, and the five legacy .html stubs. Anchors #domains, #selling, #websites, #seo and #pricing on Services still exist, and the old ?need= values on Contact still work.</p>
<p><b>New (4):</b> /ventures/, /ventures/zerohuman/, /ventures/ai-agent-economy/, /ventures/autonomous-seo-agent/.</p>
<p><b>Retired:</b> none. The navigation label Updates points at /news/. There is no /updates/ page.</p></section>

<section class="sec"><h2>SEO migration summary</h2>
<ul><li>Every page has a unique title, description, self-referencing trailing-slash canonical, Open Graph and Twitter tags.</li>
<li>The sitemap lists all 13 indexable pages on the apex host. robots.txt is unchanged.</li>
<li>Legacy stubs are byte-for-byte unchanged: noindex, follow, canonical, instant refresh, query string and hash preserved.</li>
<li>Production pages carry no robots meta. Only the 404 page and the stubs are noindex. (Everything on this staging copy is noindex by design.)</li>
<li>The Organization description and topics were updated. Domain brokerage stays in them. The shared Person node is byte-identical to production today.</li>
<li>No software product, customer, rating, or metric was added to structured data.</li>
<li>Fonts are self-hosted, so pages make no third-party request.</li></ul></section>

<section class="sec"><h2>Test results on the production branch</h2>
<table class="kv"><tbody>
<tr><th scope="row">Repository test suite</th><td>python3 tests/test_site.py: all 2,535 checks pass.</td></tr>
<tr><th scope="row">Accessibility</th><td>axe-core 4.10, WCAG 2 and 2.1 A and AA plus best-practice rules, 14 pages at 375 and 1440 px: no violations.</td></tr>
<tr><th scope="row">Responsive</th><td>14 pages at 320, 375, 390, 768, 1024 and 1440 px: no horizontal overflow, no text under 12 px, no undersized touch targets.</td></tr>
<tr><th scope="row">Browsers</th><td>Chromium and Firefox ran every page and width with no console errors and no broken images. WebKit could not start in the build environment, so Safari is not tested.</td></tr>
<tr><th scope="row">Keyboard</th><td>Skip link, visible focus, menu opens and closes with Escape, status rows open on focus, Pause works, disclosures and FAQ open with Enter.</td></tr>
<tr><th scope="row">Reduced motion</th><td>No running animation and no hidden content on any page.</td></tr>
<tr><th scope="row">No JavaScript</th><td>Navigation, headings, all status rows, all FAQ answers and the contact email fallback are visible.</td></tr>
<tr><th scope="row">Layout shift</th><td>0.0002 at most.</td></tr>
<tr><th scope="row">Contact form</th><td>Success, API-failure and network-failure states verified in a browser with the endpoint mocked. The access key is unchanged. One real submission could not be made: the build environment cannot reach the form service. It is step 9 of the launch checklist.</td></tr>
<tr><th scope="row">Lighthouse</th><td>Not available. The Lighthouse package could not be installed in the build environment (the package registry is blocked) and the PageSpeed API returned quota errors. No scores are reported.</td></tr>
<tr><th scope="row">Page weight</th><td>230 to 355 KB on twelve pages on a first uncached load, uncompressed and measured locally. The release page is 874 KB, most of it its existing hero image. The three self-hosted font files are 156 KB of every first load and are cached after the first page. The current pages are about 105 to 150 KB plus Google Fonts (754 KB for the release).</td></tr>
</tbody></table></section>

<section class="sec"><h2>How staging differs from the production branch</h2>
{li(S["transformations"])}
<p>Source: {E(S["source_repository"])}, branch {E(S["source_branch"])}, commit <code>{E(S["source_commit"][:10])}</code>. Generated by tools/export_staging.py. The production branch is the source of truth.</p></section>

<section class="sec"><h2>Unresolved questions</h2>{li(QUESTIONS)}</section>

<section class="sec"><h2>Production launch checklist (prepared, not executed)</h2>{li(LAUNCH, "ol")}</section>
</main>
<footer class="bot"><p>The live sites are unchanged. This staging copy is noindex, collects nothing, and sends nothing.</p><p>Staging review for Ken Ashe. <a href="https://github.com/kenashe/luckydomains-design-concepts">Repository</a>.</p></footer>
</body></html>
"""
out = ROOT / "production-candidate" / "review" / "index.html"
out.write_text(page)
print("wrote", out.relative_to(ROOT))
