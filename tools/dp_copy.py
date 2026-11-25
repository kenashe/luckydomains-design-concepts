"""Final copy refinements for the production candidate (owner review, November 25, 2026).

Imported by tools/dp_site.py. Nothing here changes design, structure, URLs or behaviour. It only
changes words:

  1. Founder page: new introduction, no repeated biography, no unconfirmed quotation.
  2. Website Design & Development: design is a first-class service, not a support act for SEO.
  3. The Autonomous SEO Agent example stays on the SEO page only.
  4. Positive, confident language. Limits and disclosures are kept, said once, without criticism of others.
  5. Reader-friendly wording on the homepage, the diagnostic and the service introductions.
  6. Domains: confidentiality wherever possible, not anonymity in all circumstances. Buyer-side and
     seller-side fees stated separately, using the terms already on the live site.
  7. Contact: "Typically within one business day."

apply(C, R, PG, S, DATA) edits the in-memory copy before pages are rendered.
swap(key, body) edits strings that are written directly in the page templates.
"""
import html
import re

E = html.escape


def apply(C, R, PG, S, DATA):
    # ---- service summaries (homepage and Services page) ----------------------------------------
    S["websites"]["short"] = "Thoughtful design supported by strong technical and search foundations."
    S["websites"]["check"] = ["Modern design for new websites and redesigns", "Typography, layout, and responsive pages",
                              "Clear navigation and calls to action", "Search, accessibility, and performance built in"]
    S["ai"]["check"] = ["A baseline of what AI says about your business", "A review of the sources those answers rely on",
                        "A plan to strengthen your online credibility", "Monitoring over time"]
    S["entity"]["check"] = ["A review of your primary online identity", "Structured data for people and organizations",
                            "Consistent profiles and references", "Help distinguishing your brand from similar names"]
    S["seo"]["short"] = "Audits, technical fixes, and search and content strategy to build lasting search visibility."
    S["domains"]["short"] = "Valuation, confidential outreach, negotiation, and escrow-backed transfer. Or a quiet sale of a name you own."
    S["domains"]["check"][1] = "Confidential outreach and negotiation"

    # ---- homepage: presence map, diagnostic, five layers, how we work ---------------------------
    nodes = {n["id"]: n for n in R["map"]["nodes"]}
    nodes["website"]["details"] = ["Clear design", "Useful content", "Speed and accessibility"]
    nodes["search"]["line"] = "Pages that search engines can read, understand, and show for relevant searches."
    nodes["search"]["details"] = ["Pages search engines can find", "What customers search for", "Local listings and reviews"]
    nodes["authority"]["details"] = ["Mentions and citations", "Independent references", "Your own expertise"]
    nodes["ai"]["line"] = "AI assistants and AI-powered search, which may draw on signals like these when they describe a brand."
    nodes["ai"]["details"] = ["How AI describes you today", "The sources it cites", "Questions it cannot yet answer"]
    R["map"]["idle"] = "Six signals that can help search and AI systems discover and understand a brand. Select any signal to see what it includes."
    R["progression"]["lead"] = ("Each layer makes the next one easier. A clear name supports the website, a well-built website supports search, "
                                "and search and AI systems may draw on all of it.")
    R["services"]["distinction"]["note"] = "AI visibility builds on SEO. Technical health, useful content, and credible authority remain the foundation the other two depend on."

    opt = {o["id"]: o for o in C["diagnostic"]["options"]}
    opt["domain"]["first"][2] = "Confidential outreach, negotiation, and escrow"
    opt["website"]["first"][0] = "A written review of design, clarity, speed, and search visibility"
    opt["search"]["why"] = ("When a business is hard to find, the cause is often technical, or the pages do not match what people search for. "
                            "We find which, fix the foundation, then build pages around what your customers look for.")
    opt["search"]["first"] = ["A technical review, including Google Search Console data", "Pages matched to what people actually search for", "Local listings and links between your pages"]
    opt["identity"]["why"] = ("When your name, description, founders, and profiles disagree, search and AI systems have a harder time telling who you are. "
                              "We establish one primary home for your identity and bring the rest into line.")
    opt["identity"]["first"] = ["Review your primary online identity", "Map your profiles and the sources that mention you", "Add structured data that states who you are"]
    opt["ai"]["first"] = ["Test what AI says about your business, and record it", "See which sources those answers rely on", "A plan to strengthen your online credibility"]

    a = R["aiWork"]
    a["intro"] = "AI improves how we research, design, build, test, and optimize. It adds speed and depth to audits, monitoring, and implementation."
    a["limit"] = "Ken leads every engagement, reviews every recommendation before it reaches you, and stays accountable for the result."
    a["uses"] = [["Research", "The questions customers ask, and who answers them now."],
                 ["Design and development", "Layouts, page drafts, and repetitive markup move faster. Every change is tested before it ships."],
                 ["Technical audits", "Speed, search visibility, and page health checked across every page."],
                 ["Content planning", "Page plans built from what customers search for."],
                 ["Structured data checks", "The data that describes your business checked against what the page says."],
                 ["Profile review", "The profiles and listings that describe a brand, and where they disagree."],
                 ["Monitoring", "Search visibility and cited sources tracked over time."],
                 ["Testing", "Links, metadata, accessibility, and performance checked on every change."]]

    # ---- Website Design & Development ----------------------------------------------------------
    R["pages"]["websites"]["lead"] = ("Lucky Domains designs and builds websites that look great, reflect your brand, and make it easy for customers "
                                      "to understand what you offer, on strong technical and search foundations.")
    w = PG["websites"]
    w["intro"] = ["A website should look great, reflect your brand, and make it easy for customers to understand what you offer. Lucky Domains combines thoughtful "
                  "visual design, intuitive navigation, responsive development, and strong technical foundations so your website performs as well as it looks.",
                  "Design and structure are planned together. Typography, layout, and a consistent visual identity carry your brand. Clear page structure, "
                  "fast templates, and accessible markup make the site easy to use and easy for search engines to read."]
    w["includes"] = ["Modern visual design that reflects your brand", "Typography, layout, and a consistent visual identity", "Responsive pages, designed for phones first",
                     "Intuitive navigation and clear calls to action", "Interactive elements and purposeful animation", "Search and technical foundations built in",
                     "Accessibility and performance", "Launched on your own domain, with a handoff you can edit"]
    w["paths"][0]["line"] = ("Ken reviews the existing site and writes down what is holding it back: design, clarity, structure, speed, and search visibility. "
                             "You get a plain-English recommendation to fix or to rebuild, and what either would take.")
    w["paths"][1]["line"] = ("Visual design, page templates, the core pages, and the technical foundation, launched on your own domain. "
                             "Pages are designed around your brand and built around what your customers look for.")
    step = {p["name"]: p for p in w["process"]}
    step["Structure"]["line"] = "A page plan built from the services you sell and what your customers search for."
    step["Design"]["line"] = "Visual design, typography, and layout that reflect your brand, make the business clear in seconds, and work on every screen size."
    assert w["faq"][2][0] == "Will the new site keep my search rankings?"
    w["faq"][2][1] = ("A redesign is planned so existing URLs keep working: redirects or canonicals for anything that moves, and a check of what Google has indexed "
                      "before launch. No one can guarantee rankings, and a careful migration helps protect what you have.")
    w["not"] = "We focus on business and marketing websites. Ongoing e-commerce platform maintenance and open-ended feature work are outside our scope."
    R["look"]["websites"] = {"title": "What we look at", "lead": "The same things matter whether we review the site you have or design a new one.", "items": [
        ["Visual design", "Whether the site looks current and reflects your brand consistently."],
        ["Typography and layout", "Readable type, a clear hierarchy, and room to breathe on every screen."],
        ["User experience and navigation", "Whether visitors can find what they need, with important pages a click or two from the home page."],
        ["Calls to action and forms", "A clear next step on every page, and forms that are easy to complete."],
        ["Interaction and motion", "Interactive elements and animation that help explain, and that respect reduced-motion settings."],
        ["Responsive design", "Templates that work on every screen size, starting with phones."],
        ["Accessibility and performance", "Keyboard support, readable contrast, fast templates, and nothing loaded that the page does not need."],
        ["Search and technical foundations", "One address per page, internal links and the sitemap in agreement, and structured data that matches the visible text."],
        ["Maintainability", "A site you can edit yourself, documented in plain English."]]}
    DATA["meta"]["websites"]["desc"] = ("Website design and development: modern, responsive websites that reflect your brand and are easy to use, "
                                        "built on strong technical and search foundations.")

    # ---- SEO, AI visibility, Entity SEO --------------------------------------------------------
    R["pages"]["seo"]["lead"] = ("Search is still how many customers find a business, and AI-powered search builds on it. "
                                 "We fix the foundation, sharpen every page, and build content people are searching for.")
    PG["seo"]["reporting"] = ("Reporting is plain English and tied to the work done: what changed, what moved, and what did not. "
                              "We set realistic expectations and do not guarantee rankings.")
    faq = {q: n for n, (q, _) in enumerate(PG["seo"]["faq"])}
    PG["seo"]["faq"][faq["Do you build links?"]][1] = ("We follow sustainable, ethical search practices. Authority comes from earned, editorial references "
                                                       "and content worth citing, not from bought or rented links.")
    PG["seo"]["faq"][faq["How is SEO work structured?"]][1] = ("Engagements are flexible and scoped around your needs: a one-time audit, a technical review, a scoped "
                                                               "implementation project, or a search and content strategy, with ongoing optimization and monitoring by agreement.")
    DATA["meta"]["seo"]["desc"] = "SEO audits, technical reviews, scoped implementation projects, and search and content strategy, with transparent reporting and realistic expectations."

    R["pages"]["ai"]["lead"] = ("AI assistants and AI-powered search may form a view of your business from what they can read and verify. "
                                "We make that evidence clear, consistent, and easy to find, and measure what changes.")
    C["notPromised"] = ("We set realistic expectations and measure progress transparently. No one can guarantee rankings, AI citations, mentions in a particular "
                        "AI system, or a Knowledge Panel, and we do not. We improve the evidence those systems work from and show you what changed.")
    DATA["meta"]["ai"]["desc"] = ("Improve the content and evidence that search engines and AI systems use to understand, describe, and cite your business. "
                                  "Built on search fundamentals, with realistic expectations.")
    items = {n: x for x in R["look"]["entity"]["items"] for n in [x[0]]}
    items["Canonical entity home"][0] = "Your primary online identity (entity home)"
    items["Entity disambiguation"][0] = "Telling you apart (entity disambiguation)"
    items["Entity disambiguation"][1] = "What distinguishes your brand from people and companies with similar names."
    assert PG["entity"]["levels"][0]["check"][0] == "Canonical entity-home audit"
    PG["entity"]["levels"][0]["check"][0] = "Review of your primary online identity (entity home)"

    # ---- engagements ---------------------------------------------------------------------------
    PG["services"]["pricing"] = "Every engagement is scoped in writing before work starts, and pricing follows from that scope."
    PG["services"]["notList"] = ["Five connected services, each with its own scope", "Flexible engagements, scoped around your needs",
                                 "Realistic expectations, measured transparently", "Sustainable, ethical search practices"]
    eng = {e["name"]: e for e in PG["services"]["engagements"]}
    eng["Domain Hunt"]["check"][0] = "Valuation, confidential outreach, negotiation, and escrow transfer"
    eng["Website Build"]["check"] = ["Design, page templates, and core pages", "Search and technical foundations built in", "A handoff you can edit yourself"]
    eng["Entity and AI Visibility Audit"]["check"] = ["A review of your online identity and structured data", "Testing what AI systems say about your business", "A prioritized plan"]

    # ---- domains -------------------------------------------------------------------------------
    d = PG["domains"]
    d["steps"][1]["line"] = "The conversation opens without revealing who the buyer is, wherever possible, so the price stays grounded in value."
    d["includes"][d["includes"].index("Anonymous owner outreach")] = "Confidential owner outreach"
    d["terms"] = "For sellers, brokerage is success-based and agreed in writing before any buyer is contacted."
    d["not"] = ["A fair-market range before any outreach", "Qualified buyers approached confidentially",
                "Negotiation and transfer through third-party escrow", "A success-based fee, agreed in writing first"]
    q = {x[0]: x for x in d["faq"]}
    q["Will the owner know who I am?"][1] = ("Your identity is kept confidential during initial outreach and negotiation wherever possible, so the price stays grounded in value. "
                                             "Anonymity cannot be promised in every circumstance, for example where an escrow or transfer step requires the parties to be named.")
    R["look"]["domains"]["lead"] = "Every acquisition follows the same order, and no one is contacted before the range is set."
    out = {x[0]: x for x in R["look"]["domains"]["items"]}
    out["Outreach"][1] = "Confidential contact wherever possible, so the price reflects the name and not the buyer."
    DATA["meta"]["domains"]["desc"] = ("Secure the right domain, even when someone else owns it: valuation, confidential outreach, negotiation, and escrow-backed transfer. "
                                       "Discreet sales for domain owners.")
    b = PG["buy"]
    b["steps"][1]["name"] = "Reach the owner confidentially"
    b["steps"][1]["line"] = ("Ken identifies the registrant and opens the conversation without revealing who the buyer is, wherever possible. "
                             "A price should reflect what the asset is worth, not how well funded the buyer looks.")
    b["steps"][2]["line"] = ("An owner's first price is a starting point, not a valuation. Ken negotiates against the range you agreed, "
                             "and tells you plainly if the owner's price moves outside what the name is worth to you.")
    b["fee"][0] = ("On the buyer's side, the brokerage fee for a domain hunt is success-based and agreed in writing before Ken contacts anyone. If there is no purchase, "
                   "there is no success fee. The purchase price itself is yours to approve or decline at every step. Brokerage for sellers is agreed separately, "
                   "in writing, before any buyer is contacted.")
    R["pages"]["buy"]["lead"] = ("Many good .com names are registered and not listed for sale. That does not always mean they cannot be bought. "
                                 "Here is what Ken does when a client wants a name someone else owns.")
    DATA["meta"]["buy"]["desc"] = "Many good .com names are registered and not listed for sale. Here is what Lucky Domains does when a client wants a name someone else owns."

    # ---- About ---------------------------------------------------------------------------------
    PG["about"]["believe"] = ["Focus beats breadth: five connected services, done well", "Discretion matters, especially in a negotiation",
                              "Sustainable, ethical search practices", "Realistic expectations and transparent reporting"]
    v = {x[0]: x for x in PG["about"]["values"]}
    v["Patience and persistence"][1] = "Great domains and durable visibility take time. We play the long game."
    v["Real accountability"][1] = "A written scope, a plan you can challenge, work you can follow, and transparent reporting."
    v["Evidence over claims"][1] = "We set realistic expectations, improve the evidence, and show you what changed."

    # ---- Contact -------------------------------------------------------------------------------
    PG["contact"]["lead"] = ("Tell Ken what you are working on: a website, search, identity, AI visibility, or a domain. "
                             "Replies typically come within one business day. The first consultation is free, with no obligation.")
    DATA["meta"]["contact"]["desc"] = ("Tell Ken what you are working on: a website, search visibility, digital identity, AI visibility, or a domain. "
                                       "Free, no-obligation consultation. Replies typically come within one business day.")

    # ---- Founder -------------------------------------------------------------------------------
    f = DATA["founder"]
    f["lead"] = "Founder and operator of Lucky Domains."
    f["bio"] = ["Ken began his career in accounting and financial reporting before moving into project, product, and program leadership at companies including "
                "S&P Global, EY, Prudential Financial, and Noom.",
                "He has worked with HTML, CSS, websites, and WordPress for approximately 20 years. More recently, he has embraced AI-assisted development to build websites and applications.",
                "He founded Lucky Domains to bring together his experience in business, technology, digital identity, and online discovery. "
                "He still runs it himself, so the person on your first call is the person who does the work."]
    f["experience"] = [["Finance and reporting", "Accounting and financial reporting are where the habit of documented reasoning and reporting that can be checked comes from."],
                       ["Product and program leadership", "Roughly two decades of corporate experience, including serving as Director of Project and Product Management at Prudential Financial, shape how projects are planned and delivered."],
                       ["Websites and AI", "Hands-on website work, and AI applications built and documented in public on KenAshe.ai, including what did not work."]]


# Strings written directly in the page templates. (old, new) pairs are plain text unless marked raw.
def _t(old, new, n=1):
    return (E(old), E(new), n)


SWAPS = {
    "services": [_t("Scoped in writing, before work starts.", "Flexible engagements, scoped around your needs."),
                 ("<strong>What we will not promise.</strong>", "<strong>Realistic expectations.</strong>", 1),
                 _t("Deliberately specialized", "How we work"),
                 ("What Lucky Domains is not</h2>", "Focused on what we do well.</h2><p class=\"section-lead\">We focus on websites, search, digital identity, AI visibility, and domains. "
                  "Paid advertising and social media management are outside what we offer.</p>", 1),
                 ('<ul class="nope">', '<ul class="check">', 1)],
    "websites": [_t("Structure before style.", "Great design. Strong foundations.")],
    "seo": [("<strong>Honest reporting.</strong>", "<strong>Transparent reporting.</strong>", 1),
            _t("The fundamentals still decide who gets found.", "Search fundamentals still matter."),
            _t("AI-powered search draws on the same foundation, so this work now does two jobs.", "AI-powered search draws on much of the same foundation, so this work supports both.")],
    "ai": [_t("What AI systems rely on", "What AI systems may draw on"),
           ("<strong>What we will not promise.</strong>", "<strong>Realistic expectations.</strong>", 1),
           _t("No secret markup. Measurable, in part.", "Built on search fundamentals. Measurable, in part."),
           _t("Authority-content plan", "Credibility plan"),
           _t("The first-party content and credible references that would strengthen the evidence.",
              "A plan to strengthen your online credibility: the content on your own site and the credible references that would support it.")],
    "entity": [_t("Read the research note", "Read the research article")],
    "domains": [_t("Every other signal points back to the name.", "The name your other signals point back to."),
                ("<strong>Fee.</strong>", "<strong>Seller-side fee.</strong>", 1),
                ('<ul class="nope">', '<ul class="check">', 1)],
    "buy": [_t("What this is not", "What to expect")],
}
BUYER_FEE = "For buyers, the brokerage fee is success-based and agreed in writing before outreach. If there is no purchase, there is no success fee."
EXPECT = ["Private, direct negotiation, not a public auction", "A fair-market range you see before anyone is contacted",
          "Some owners will not sell, and Ken will say so plainly", "No success rate is quoted, because every name is different",
          "A success-based fee: no purchase, no success fee"]


def swap(key, body, helpers):
    """Apply the template-level wording changes for one page. Every change must match, or the build stops."""
    for old, new, n in SWAPS.get(key, []):
        assert body.count(old) == n, f"copy refinement for {key!r} did not match {n} time(s): {old[:70]!r} ({body.count(old)})"
        body = body.replace(old, new)
    note, check = helpers["note"], helpers["check"]
    if key == "home":       # the Autonomous SEO Agent example now lives on the SEO page only
        body, n = re.subn(r'<p class="uses-n">.*?</p>', "", body, flags=re.S)
        assert n == 1 and "Autonomous SEO Agent" not in body
    if key == "ai":         # one statement of limits is enough; the sources above it already cover special markup
        body, n = re.subn(r'<p class="v3-note[^"]*">(?:(?!</p>).)*There is no secret AI markup\.(?:(?!</p>).)*</p>', "", body, flags=re.S)
        assert n == 1, "could not find the special-markup note on the AI page"
    if key == "domains":    # buyer-side fee, in the live site's own words, under the buying steps
        at = '<p class="center v3-more"><a class="btn btn-ghost" href="/how-we-buy-domains/">'
        assert body.count(at) == 1
        body = body.replace(at, note(BUYER_FEE, "note", "Buyer-side fee.") + at)
    if key == "buy":        # realistic expectations, stated once and without the run of "Not ..." lines
        body, n = re.subn(r'<ul class="nope">.*?</ul>', lambda m: check(EXPECT), body, count=1, flags=re.S)
        assert n == 1
    if key == "about":      # the About page states how AI is used and who is accountable in one note
        a, b = helpers["ai_intro"], helpers["ai_limit"]
        assert body.count(E(a)) == 1
        body = body.replace(E(a), E(a + " " + b))
    return body
