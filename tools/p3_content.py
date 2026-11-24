"""Writes phase-3/shared/content.json, the one content source for the three version 3 concepts.

Copy is reused from the original production site (kenashe/luckydomains at efed1de) and from the
already-checked Phase 2 content file, then extended for the fuller page set. Run: python3 tools/p3_content.py
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
P2 = json.loads((ROOT / "phase-2" / "shared" / "content.json").read_text())
P1F = json.loads((ROOT / "shared" / "content.json").read_text())["founder"]
KA = "https://kenashe.ai/"
GOOGLE = "https://developers.google.com/search/docs/appearance/ai-features"
GOOGLE2 = "https://developers.google.com/search/docs/fundamentals/ai-optimization-guide"
BING = "https://blogs.bing.com/webmaster/2026/10/introducing-topics-portfolio-beta-in-ai-performance/"

SV = {s["id"]: s for s in P2["services"]}
PAGES2 = P2["pages"]

C = {
  "_readme": "Version 3 shared content. One copy and fact source for all three version 3 concepts. Built by tools/p3_content.py from the original production site (kenashe/luckydomains, main at efed1de), the Phase 2 content file, and public sources read November 24, 2026. Items marked concept are layout or planning copy, not published facts.",
  "asOf": "November 24, 2026",
  "preferredConcept": "C",
  "conceptC": {"location": "Berkeley Heights, New Jersey",
               "workLead": "We use our own projects to show how we work. We do not name clients or disclose identifying details. Any illustrative example is labeled, and we do not claim traffic, ranking, or lead figures.",
               "engagements": {"websites": "Website Build", "ai": "Entity and AI Visibility Audit", "entity": "Entity and AI Visibility Audit"}},
  "company": dict(P2["company"], description="Lucky Domains helps businesses build a digital presence that people, search engines, and AI systems can find, understand, and trust.",
                  descriptionLong="Lucky Domains helps businesses build a digital presence that people, search engines, and AI systems can find, understand, and trust. We design and build websites, improve search and AI visibility, strengthen entity and brand signals, and secure the domains that anchor your identity.",
                  footer="A digital presence studio for the AI era. Websites, search, digital identity, AI visibility, and domains.",
                  story="Lucky Domains began with the most fundamental piece of digital identity: the domain. From there, the work expanded naturally into the website built on that name, the search visibility that brings people to it, and the entity and authority signals that help search engines and AI systems understand the brand. Today, Lucky Domains works across that entire digital presence.",
                  originalModel="The original site described the work as Domain, Site, Rankings. Version 3 keeps that order and adds the two layers that now decide how a business is understood: Entity and AI."),
  "hero": {"eyebrow": "Websites · Search · Digital identity · AI visibility",
           "headline": "Build a digital presence people, search engines, and AI recognize.",
           "headlineHl": "people, search engines, and AI",
           "support": P2["hero"]["support"], "cta1": "Build your digital presence", "cta2": "Explore our services",
           "founder": "Founded and operated by Ken Ashe, CPA, PMP."},
  "audiences": [
      {"id": "people", "name": "People", "line": "Visitors who decide in seconds whether you look credible."},
      {"id": "search", "name": "Search engines", "line": "Crawl, index, and rank the pages that answer best."},
      {"id": "ai", "name": "AI systems", "line": "Read the same evidence to summarize, cite, and recommend."}],
  "stack": [
      {"id": "domain", "n": "01", "name": "Domain", "short": "Own the name.", "line": "Own the name and anchor the identity.", "detail": P2["stack"][0]["detail"], "service": "domains"},
      {"id": "website", "n": "02", "name": "Website", "short": "Build the destination.", "line": "Build the destination the business controls.", "detail": P2["stack"][1]["detail"], "service": "websites"},
      {"id": "search", "n": "03", "name": "Search", "short": "Become discoverable.", "line": "Make the site technically sound, relevant, and discoverable.", "detail": P2["stack"][2]["detail"], "service": "seo"},
      {"id": "entity", "n": "04", "name": "Entity", "short": "Establish who you are.", "line": "Help platforms understand who you are and how your website, profiles, founders, reviews, and references relate.", "detail": P2["stack"][3]["detail"], "service": "entity"},
      {"id": "ai", "n": "05", "name": "AI", "short": "Become understandable and citable.", "line": "Make the brand easier for AI-powered discovery to understand, verify, cite, and surface.", "detail": P2["stack"][4]["detail"], "service": "ai"}],
  "stackReinforce": P2["stackReinforce"],
  "services": [
      {"id": "websites", "icon": "monitor", "name": "Website Design & Development", "tag": "Websites", "path": "services/website-design/",
       "h": "The owned foundation everything else depends on", "short": "New websites and redesigns built to be found, understood, and trusted.",
       "check": ["New builds and redesigns", "Information architecture and content structure", "Search-ready technical foundation", "Accessibility, performance, and structured data"]},
      {"id": "seo", "icon": "search", "name": "SEO & Search Visibility", "tag": "SEO", "path": "services/seo/",
       "h": "Be the result people actually click", "short": "Technical, on-page, content, and local SEO that earns visibility and keeps it.",
       "check": ["Technical SEO audits and fixes", "On-page optimization and internal linking", "Local SEO and Google Business Profile", "Search Console monitoring and honest reporting"]},
      {"id": "ai", "icon": "spark", "name": "AI Visibility & Brand Authority", "tag": "AI visibility", "path": "services/ai-visibility/",
       "h": "Improve the evidence AI systems use", "short": "Improve the evidence that search engines and AI systems use to understand your brand.",
       "check": ["AI visibility baseline", "Important-query testing", "Citation and source analysis", "Monitoring over time"]},
      {"id": "entity", "icon": "users", "name": "Entity SEO & Digital Identity", "tag": "Entity SEO", "path": "services/entity-seo/",
       "h": "Make it clear who you are", "short": "One clear, consistent identity for a person or a company, in plain words and in structured data.",
       "check": ["Canonical entity-home audit", "Person and Organization structured data", "Profile and reference consistency", "Knowledge Panel readiness"]},
      {"id": "domains", "icon": "target", "name": "Domain Acquisition & Brokerage", "tag": "Domains", "path": "services/domains/",
       "h": "Get the name that's already taken", "short": "Valuation, anonymous outreach, negotiation, and escrow-backed transfer. Or a quiet sale of a name you own.",
       "check": ["Fair-market valuation and strategy", "Anonymous outreach and negotiation", "Secure, escrow-backed transfer", "Expiring and backorder domain hunting"]}],
  "nav": [["Services", "services/"], ["Work", "work/"], ["About", "about/"], ["Insights", "insights/"], ["Founder", "founder/"], ["Contact", "contact/"]],
  "navCta": "Start a project",
  "notPromised": P2["notPromised"],
  "noSecret": "There is no secret AI markup. Google says there is no special schema and no new machine-readable file needed for its AI features. Structured data helps systems read facts you can already show.",
  "diagnostic": P2["diagnostic"],
  "aiWork": dict(P2["aiWork"], uses=[{"name": "Technical crawls", "line": "Indexing, speed, and crawlability checks across every page."},
                                     {"name": "Structured-data validation", "line": "Person, Organization, and service data checked against the visible facts."},
                                     {"name": "Duplicate and canonical checks", "line": "Finding duplicate URL forms and links that point at them."},
                                     {"name": "Content research", "line": "The questions customers actually ask, and who answers them now."},
                                     {"name": "Profile discovery", "line": "Every profile and listing that describes a brand, and where they disagree."},
                                     {"name": "Citation monitoring", "line": "Which sources AI systems cite for the questions that matter."},
                                     {"name": "QA", "line": "Links, metadata, accessibility, and performance checked on every change."},
                                     {"name": "Reporting preparation", "line": "Changes tracked over time and summarized in plain English."}]),
  "lab": P2["lab"], "labIntro": P2["labIntro"], "work": P2["work"], "annotations": P2["annotations"],
  "map": P2["map"], "siteGraph": P2["siteGraph"],
  "founder": dict(P2["founder"], credentialsFull=P1F["credentials"], speaking=P1F["speaking"], career=P1F["career"],
                  links=[["KenAshe.ai", KA, "Build logs, essays, and videos"], ["LinkedIn", "https://www.linkedin.com/in/kenashe", "linkedin.com/in/kenashe"], ["X", "https://x.com/kenashe", "@kenashe"], ["GitHub", "https://github.com/kenashe", "github.com/kenashe"]],
                  forbes="https://councils.forbes.com/profile/Ken-Ashe-Founder-Lucky-Domains/f9cc3b77-a7e7-4319-8314-a706bcaf85e8",
                  quote="A CPA would call that a control. A project manager would call it a repeatable process.",
                  bioLong=["Ken started his career in accounting and financial reporting before moving into project, product, and program leadership. Over roughly two decades, that career ran through S&P Global, EY, Noom, and Prudential Financial, where he served as Director of Project and Product Management.",
                           "He built Lucky Domains alongside that work and still runs it himself. The person on your first call is the person who values the domain, scopes the site, runs the audit, and writes the report.",
                           "He also builds and documents AI systems in public at KenAshe.ai. That work keeps his judgment current, and some of it, like the internal agent that maintains profiles, runs inside Lucky Domains today."],
                  split=[["KenAshe.ai", "Ken's personal build-in-public site: experiments, build logs, videos, and what failed."], ["LuckyDomains.io", "The company: websites, search, digital identity, AI visibility, and domains, for clients."]]),
  "contact": dict(P2["contact"], paths=["Start a website project", "SEO and search visibility", "AI visibility and brand authority", "Entity SEO and digital identity", "Domain acquisition or brokerage", "Media, speaking, or something else"]),
  "evidenceGoogle": {"label": "Google Search Central", "url": GOOGLE, "url2": GOOGLE2,
                     "line": "Google says the same SEO fundamentals apply to AI Overviews and AI Mode: crawlable pages, useful first-party content, internal links, good page experience, and structured data that matches the visible text. It also says there is no special schema and no new AI text file required."},
  "evidenceBing": {"label": "Bing Webmaster Tools", "url": BING,
                   "line": "Bing Webmaster Tools now includes an AI Performance report that shows which pages are cited in AI-generated answers in Copilot and Bing, and the grounding queries behind those citations. AI visibility is becoming measurable, at least in part."},
  "insights": {"label": "Planned articles. Concept content, not yet published.", "items": P2["insights"]["items"]},
}

# ---------------------------------------------------------------- page copy
W = PAGES2["websites"]; S2 = PAGES2["search"]; D2 = PAGES2["domains"]
C["pages"] = {
 "services": {"title": "Services", "eyebrow": "Services", "h1": "Five services. One digital presence.", "lead": "Each service stands on its own. Together they follow the order a presence is built: the name, the destination, the visibility, the identity, and the recognition that depends on all of it.",
   "engagements": [
     {"name": "Domain Hunt", "kind": "Success fee", "line": "A single target domain, found and secured.", "check": ["Valuation, anonymous outreach, negotiation, and escrow transfer", "Success-based fee, agreed in writing before outreach", "No purchase, no success fee"]},
     {"name": "Website Build", "kind": "Scoped", "line": "A new site or a rebuild on your own domain.", "check": ["Written scope before work starts", "Search-ready structure and technical foundation", "A handoff you can edit without us"]},
     {"name": "Growth SEO", "kind": "Monthly", "line": "Ongoing SEO to compound visibility.", "check": ["Technical, on-page, content, and local SEO as scoped", "Reporting every month", "No ranking guarantees"]},
     {"name": "Entity and AI Visibility Audit", "kind": "Scoped", "line": "A baseline and plan for a person or company.", "check": ["Entity and structured-data review", "Important-query testing across AI systems", "A prioritized implementation roadmap"]},
     {"name": "Full Launch", "kind": "Scoped", "line": "Name, site, search, and identity together.", "check": ["For a new business or a rebrand", "One accountable operator across all of it", "Pricing set after the consultation"]}],
   "pricing": "Every engagement is scoped in writing before work starts. Pricing is set on the consultation, from that scope, not from a menu.",
   "notList": PAGES2["services"]["notList"]},
 "websites": {"title": "Website Design & Development", "eyebrow": "Website Design & Development", "h1": "A website built to be found, understood, and trusted.", "lead": "You do not just need a website that looks good. You need the owned foundation that search visibility, brand authority, and AI recognition depend on. Lucky Domains designs and builds it on your own domain.",
   "intro": W["intro"], "paths": W["paths"], "process": W["process"], "foundations": W["foundations"], "architecture": W["architecture"],
   "includes": ["Site structure and page templates", "Core pages built around real search demand", "Technical foundation: canonicals, structured data, speed", "Accessibility and analytics foundations", "Launched on a real host and your own domain", "A handoff you can edit without us"],
   "aiNote": "AI-assisted development and testing: research, page drafts, and repetitive markup move faster, and every change is checked by automated tests for links, metadata, accessibility, and performance before it ships. Ken reviews the result.",
   "not": W["not"], "proof": W["proof"],
   "faq": [["Do you redesign existing sites or only build new ones?", "Both. Ken starts by reviewing the site you have and writes down what is holding it back. Sometimes the right answer is to fix it. Sometimes it is to rebuild."],
           ["Which platform do you build on?", "Whatever you can maintain. LuckyDomains.io is plain static HTML on GitHub Pages because that suits a small site. Larger sites may need a content management system. The recommendation comes with the scope."],
           ["Will the new site keep my search rankings?", "A redesign is planned so existing URLs keep working: redirects or canonicals for anything that moves, and a check of what Google has indexed before launch. No one can guarantee rankings, but a careful migration protects what you have."],
           ["Do you write the content?", "Ken plans the page structure around real search demand and drafts or edits core page copy with you. You stay the source of facts about your business."]]},
 "seo": {"title": "SEO & Search Visibility", "eyebrow": "SEO & Search Visibility", "h1": "SEO is expanding, not disappearing.", "lead": "Search still decides which businesses get found, and AI-powered search is built on top of it. Lucky Domains builds visibility the durable way: fix the foundation, sharpen every page, and create content customers are actually searching for.",
   "areas": S2["seoAreas"][:4] + [{"name": "Local SEO", "line": "Google Business Profile, consistent local listings, and reviews, for businesses that serve a place."},
                                   {"name": "Authority building", "line": "Earned, editorial references and digital PR. No rented links."},
                                   {"name": "Search intent", "line": "Matching each page to what the searcher is actually trying to do."},
                                   {"name": "Search Console and monitoring", "line": "Indexing, coverage, and queries watched over time, and reported in plain English."}],
   "process": [{"name": "Audit", "line": "Crawl the site, read Search Console, and find what blocks indexing and ranking."}, {"name": "Fix the foundation", "line": "Speed, indexing, canonicals, structured data, and mobile health."},
               {"name": "Target the pages", "line": "Match each page to a real query and the intent behind it."}, {"name": "Build content", "line": "Pages and articles that answer the questions buyers ask."}, {"name": "Monitor", "line": "Track what changed, report it honestly, and adjust."}],
   "reporting": "Reporting is plain English and tied to the work done: what changed, what moved, and what did not. There are no ranking guarantees, and no one who offers them should be trusted.",
   "faq": [["Is SEO still worth it with AI search?", "Yes. Google says its AI features are built on its core search systems and that the same SEO fundamentals apply. Pages that are crawlable, useful, and well structured are the ones AI features can draw on."],
           ["How long does SEO take?", "Technical fixes can show up within weeks. Content and authority take months. The work is cumulative, which is why it is scoped as ongoing."],
           ["Do you build links?", "No rented or bought links. Authority comes from earned, editorial references and content worth citing."]]},
 "ai": {"title": "AI Visibility & Brand Authority", "eyebrow": "AI Visibility & Brand Authority", "h1": "Improve the evidence that search engines and AI systems use to understand your brand.", "lead": "AI assistants and AI-powered search form a view of your business from what they can read and verify. Lucky Domains helps make that evidence clear, consistent, and easy to find, and measures what changes.",
   "goals": ["Easier to understand", "Easier to verify", "Associated with the correct people, services, and locations", "Supported by useful first-party content", "Consistently represented across trusted profiles and references", "Measured with emerging AI-citation data where it exists"],
   "deliverables": S2["aiSteps"][:2] + [{"name": "Important-query testing", "line": "The questions that matter to your business, asked across major AI systems, with the answers and sources recorded."},
                                         {"name": "Content clarity and coverage", "line": "Your own pages reviewed for the facts a system needs to explain you."}] + S2["aiSteps"][2:3] +
                   [{"name": "Authority-content plan", "line": "The first-party content and credible references that would strengthen the evidence."}, {"name": "Profile and reference alignment", "line": "Names, descriptions, founders, and locations brought into agreement."},
                    {"name": "Structured-data validation", "line": "Markup that matches the visible facts on the page, and nothing more."}, {"name": "Monitoring over time", "line": "The baseline re-run on a schedule, with changes reported."}],
   "measure": "Where data exists, it is used. Bing Webmaster Tools reports cited pages and grounding queries for Copilot and Bing AI answers. For other systems, the same important questions are re-asked on a schedule and the answers compared with the baseline.",
   "faq": [["Can you get my business recommended by ChatGPT?", "No one can promise that. What can be done is to make the evidence about your business clear, consistent, and easy to verify, so systems that look for it find it."],
           ["Is this different from SEO?", "It builds on SEO. Crawlable pages, good content, and accurate structured data are the foundation. AI visibility adds entity consistency, third-party corroboration, and testing how AI systems actually describe you."],
           ["Do I need an llms.txt file or special AI markup?", "Google says its search features do not use them and that no special markup is needed. Other services may. Lucky Domains will tell you which, if any, are worth maintaining for your situation."]]},
 "entity": {"title": "Entity SEO & Digital Identity", "eyebrow": "Entity SEO & Digital Identity", "h1": "Help search engines and AI systems understand exactly who you are.", "lead": "Search engines increasingly organize the web around entities, not just keywords. Lucky Domains helps people and companies create a clear, consistent identity across their website, structured data, profiles, and credible third-party sources.",
   "what": ["Traditional SEO helps pages rank. Entity SEO helps search engines understand the person or organization behind those pages: the canonical website, official profiles, founders, companies, authors, credentials, products, and credible references that all belong to the same real-world entity.", "When those signals conflict or stay disconnected, systems struggle to tell one person or company from another. When they are consistent and machine-readable, they have a clearer picture to work with."],
   "people": D2["people"] + ["Founder and executive visibility"], "business": D2["business"] + ["Official social profiles"],
   "agents": ["Human-readable names", "Domain or ENS-based identity", "Wallets and service endpoints", "Machine-readable service information", "Discovery", "Provenance", "Permissions", "Reputation"],
   "levels": [{"name": "Entity foundation", "line": "The audit and fixes most people and companies need first.", "check": ["Canonical entity-home audit", "Person or Organization structured-data review", "Stable entity @id architecture", "sameAs profile mapping", "Logo, image, name, and description consistency", "Brand-search and entity-search baseline"]},
              {"name": "Entity authority", "line": "For larger or more complicated public footprints. Everything in the foundation, plus:", "check": ["Cross-domain entity graph audit", "Founder, company, author, and product relationship review", "External profile and citation consistency audit", "Third-party corroboration assessment", "AI and LLM entity-discovery review", "Knowledge Graph and brand-SERP monitoring recommendations"]}],
   "panel": "Google creates Knowledge Panels automatically. No one can submit a form to force one. This work improves the evidence Google uses to recognize an entity and tell it apart from everyone with a similar name.",
   "faq": [["Will this get me a Knowledge Panel?", "It cannot guarantee one. It improves the evidence Google works from. If Google already shows a panel, Ken can help you review it and submit corrections."],
           ["What is an entity home?", "The one page that says, authoritatively, who you are: usually your homepage or founder page, with structured data that the rest of the web can point to."]]},
 "domains": {"title": "Domain Strategy, Acquisition & Brokerage", "eyebrow": "Domain Acquisition & Brokerage", "h1": "Own the name your identity is built on.", "lead": "The right domain builds instant trust and anchors everything else: your site, your email, your profiles, and every reference to you. Lucky Domains helps you secure it, even when it is taken, and represents sellers who want a discreet, well-negotiated exit.",
   "anchor": D2["anchors"], "steps": D2["acquisition"], "selling": D2["selling"], "terms": D2["terms"], "not": ["Not a public auction or a bidding war in your name", "Not a guaranteed close. Some owners will not sell", "Not a quoted success rate. None is published", "Not a retainer. No purchase, no success fee"],
   "includes": SV["domains"]["includes"],
   "faq": [["How much does it cost to buy a domain that is not for sale?", "It depends on the name, its history, and the owner. Ken sets a fair-market range from comparable sales before anyone is contacted, and you approve or decline every price."],
           ["Will the owner know who I am?", "No. Outreach is anonymous so the price stays grounded in value, not in how well funded the buyer looks."],
           ["What if the owner will not sell?", "Some will not. Ken tells you plainly and stops, rather than pushing toward a number that only makes sense to the seller."]]},
 "buy": {"title": "How We Buy Domains", "eyebrow": "Domain acquisition", "h1": "How we buy a domain that is not listed for sale", "lead": "Most good .coms are registered and not for sale. That does not mean they cannot be bought. It means the buyer needs a number, a method, and patience. Here is exactly what Ken does when a client wants a name someone else owns.",
   "steps": [{"name": "Set the range", "line": "Before anyone is contacted, Ken builds a fair-market range for the name from comparable sales, traffic and keyword data, and what the domain is strategically worth to your business. You see that range and the reasoning behind it."},
             {"name": "Reach the owner anonymously", "line": "Ken identifies the registrant and opens the conversation without revealing who the buyer is. A price should reflect what the asset is worth, not how well funded the buyer looks."},
             {"name": "Negotiate against the range", "line": "Sellers open high. Ken negotiates against the range you agreed, not against the opening ask, and tells you plainly if the owner's price moves outside what the name is worth to you."},
             {"name": "Close through escrow", "line": "Every transfer runs through a third-party escrow service. Funds are released only when the domain is verifiably in your control."}],
   "fee": ["The brokerage fee for a domain hunt is success-based and agreed in writing before Ken contacts anyone. If there is no purchase, there is no success fee. The purchase price itself is yours to approve or decline at every step.", "Some names are not obtainable at a sensible price. When that is the case, Ken says so and stops, rather than pushing you toward a number that only makes sense to the seller."]},
 "work": {"title": "Work", "eyebrow": "Work", "h1": "Real projects, with the evidence attached.", "lead": "Case studies use only public evidence. Where a client's details cannot be shared, the layout is shown with placeholders and labeled. No traffic, ranking, or lead figures are claimed."},
 "about": {"title": "About", "eyebrow": "About Lucky Domains", "h1": "Domains were the beginning. Not the boundary.", "lead": "Lucky Domains is a digital presence studio for the AI era: websites, search, digital identity, AI visibility, and the domains that anchor them.",
   "philosophy": "Fortune favors the prepared. The wins that look lucky from the outside are the result of preparation, relationships, and doing the unglamorous work well.",
   "values": [["Integrity first", "We give you the honest answer, even when it is that you do not need this."], ["Patience and persistence", "Great domains and durable visibility take time. We play the long game and do not fake quick wins."], ["Real accountability", "A written scope, a plan you can challenge, work you can follow, and reporting honest enough to question."], ["Evidence over claims", "No guaranteed rankings, citations, or Knowledge Panels. We improve the evidence and show you what changed."]],
   "believe": ["Specialists beat generalists. We do not try to be a do-everything agency", "Discretion gets better deals", "White-hat is the only hat worth wearing", "Reporting should be honest enough to question"],
   "rhythm": [{"name": "Scope", "line": "A written scope before work starts."}, {"name": "Plan", "line": "A valuation or roadmap you can challenge."}, {"name": "Execute", "line": "Work you can follow, checked by tests."}, {"name": "Report", "line": "Plain-English reporting tied to what was done."}]},
 "founder": {"title": "Ken Ashe, Founder", "eyebrow": "Founder", "h1": "Ken Ashe", "lead": "Founder and operator of Lucky Domains. CPA and PMP, with roughly two decades in finance, product, and program leadership, and a builder of AI systems documented in public."},
 "insights": {"title": "Insights", "eyebrow": "Insights", "h1": "Plain-English thinking on websites, search, identity, and AI.", "lead": "Guides and research notes on how businesses get found and understood. Ken's deeper build logs live on KenAshe.ai."},
 "news": {"title": "News & Media", "eyebrow": "Newsroom", "h1": "News and media", "lead": "Announcements from Lucky Domains, founder background, and media resources. For media inquiries, email info@luckydomains.io.",
   "release": {"date": "June 24, 2026", "title": "Lucky Domains Launches Redesigned Website for Premium Domain Acquisition and SEO", "line": "LuckyDomains.io positions the company as a focused partner for businesses that need a better domain name and durable search visibility.", "url": "https://luckydomains.io/news/website-relaunch/", "note": "Published release, linked as it stands on the live site."},
   "sample": {"title": "Lucky Domains repositions as a digital presence studio for the AI era", "line": "Placeholder showing where an approved announcement of the new positioning would go. No such announcement has been made.", "note": "Sample concept copy. Not published."}},
 "contact": {"title": "Contact", "eyebrow": "Contact", "h1": "Start with a conversation.", "lead": "Tell Ken what you are working on: a website, search, identity, AI visibility, or a domain. Replies come within one business day. The first consultation is free, with no obligation."},
}

C["beforeAfter"] = {"caption": "Illustration with a made-up business. Not a client.",
  "before": {"label": "Before: four places, four different stories", "rows": [["Website", "Harbor Lane Dental, family dentistry since 2009"], ["Google Business Profile", "Harbor Lane Dental Care LLC"], ["Directory listing", "Harbourlane Dental, old address"], ["Founder profile", "No link to the practice"]]},
  "after": {"label": "After: one identity, described the same way", "rows": [["Website", "Harbor Lane Dental, family dentistry in one place since 2009"], ["Google Business Profile", "Harbor Lane Dental, same name, hours, and address"], ["Directory listing", "Harbor Lane Dental, corrected address, links to the site"], ["Founder profile", "Dr. Founder, owner of Harbor Lane Dental"]]}}
C["checks"] = {"label": "Examples of what we check. Illustrative, not a client report.",
  "websites": ["Every important page reachable from the homepage in two clicks", "One canonical URL per page", "Images sized and compressed", "Forms usable with a keyboard alone", "Structured data matches the visible text"],
  "seo": ["Key pages indexed in Search Console", "Each page targets one clear search intent", "Internal links point to canonical URLs", "Google Business Profile matches the website", "Nothing important blocked by robots.txt"],
  "ai": ["How major AI assistants describe the business today", "Which sources they cite for the category", "Whether the founder and company are connected", "Whether profiles disagree on name or location", "Whether pages say who, what, where, and for whom"],
  "entity": ["One entity home with a stable identifier", "sameAs links to official profiles only", "The same name, logo, and description everywhere", "Founder, company, and author relationships stated", "Independent sources corroborate the facts"],
  "domains": ["Who owns the name, and for how long", "Comparable sales for similar names", "Possible trademark conflicts", "Traffic and history signals", "Escrow terms agreed before any money moves"]}
C["audit"] = {"title": "Quick presence check", "intro": "Six yes-or-no questions. A rough self-check, not an audit.",
  "items": [["domain", "You own the exact domain customers type to find you."], ["website", "Your site loads quickly and works well on a phone."], ["search", "You show up when people search your name and your main service."],
            ["entity", "Your name, description, and founders match across your site and profiles."], ["entity", "Your site has Organization or Person structured data."], ["ai", "You have checked how AI assistants describe your business."]]}

C["article"] = {
  "slug": "insights/domains-identity-for-ai-agents/", "title": "Can domains become the identity layer for AI agents?", "kind": "Research note", "status": "Draft for review. Not published.",
  "dek": "People use domains as durable identities. Businesses use them as the canonical home of their brand. AI agents may need something similar: a readable name, a way to be found, and a way to check who stands behind them.",
  "sections": [
    ["Domains already do this for people and companies", ["A domain is the one identifier most people and businesses fully control. Email, profiles, structured data, and citations all point back to it. When a search engine or an AI system needs to decide which company a mention belongs to, the domain is often the anchor that settles it."]],
    ["What an agent would need", ["An agent that offers a service, or pays for one, needs some of the same things: a human-readable name, a known place to be looked up, a description of what it does that other software can read, a payment destination tied to that name, evidence that a result came from it, and a record that travels with it."]],
    ["What Ken has tested in public", ["ZeroHuman is a small service that sells two jobs to other AI agents. Its ENS name, zerohuman.eth, is the storefront, the payment address, and the sender of every result. A text record on the name publishes the menu, and the service is listed in the ERC-8004 agent registry as agent #56626, linked back from the name with an ENSIP-25 record.", "An earlier experiment had two AI agents with their own wallets complete one purchase on Ethereum mainnet, with an ENS text record as the storefront. Both are documented on KenAshe.ai."]],
    ["What it does not prove", ["As of November 20, 2026, no outside agent had bought from ZeroHuman. Both experiments were operated by Ken. There is no settled standard for agent identity, and these tests are evidence that the pieces can work, not that the market has chosen them."]],
    ["Where this leaves Lucky Domains", ["This is research, not a product. Lucky Domains does not sell agent identity. The question matters to the core work anyway: if software is going to look businesses up, the same identity signals that help search engines and AI systems today will matter even more."]]],
  "sources": [["ZeroHuman build record", "https://kenashe.ai/building/zerohuman/"], ["AI Agent Economy build record", "https://kenashe.ai/building/ai-agent-economy/"], ["zerohuman.eth on ENS", "https://app.ens.domains/zerohuman.eth"]]}

out = ROOT / "phase-3" / "shared" / "content.json"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(C, indent=2, ensure_ascii=False) + "\n")
print("wrote", out.relative_to(ROOT))


def build():
    pass  # the content file is written when this module is imported
