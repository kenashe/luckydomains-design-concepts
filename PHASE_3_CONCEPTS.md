# Version 3 concepts and design notes

Created November 24, 2026. Ken selected Concept C, and a refined version now lives at `/phase-3/interactive-refined/` (see [Refinement](#refinement-original-interactive-refined) below). Review only; nothing in Version 3 has been implemented on LuckyDomains.io. Phase 1 (`CONCEPTS.md`) and Phase 2 (`PHASE_2_CONCEPTS.md`) notes are unchanged.

## Why version 3

Ken did not like the Phase 2 designs. He liked the original site's design, wanted more pages rather than fewer, and wanted more automation. Version 3 therefore:

- starts from the original production design, not a new one;
- builds the fuller site architecture (sixteen pages per concept, not six);
- adds motion that explains the business: the Digital Presence Stack, a recognition map, and a diagnostic.

The business message is the corrected one from Phase 2, held constant across all three concepts.

## Built from the original, literally

`phase-3/shared/original.css` is a byte-for-byte copy of `css/styles.css` from `kenashe/luckydomains` at `efed1de` (SHA-256 prefix `e826a42f937531e4`). Every version 3 page loads it first, then `phase-3/shared/v3.css`, then the concept's own `css/style.css`.

All pages use the original markup and class names: `site-header`, `hero` and `hero--page` (the navy hero with the dot texture and green glow), `section` and `section-soft`, `sec-head`, `eyebrow`, `card` with `icon-badge`, `ul.check` and `ul.nope`, `steps` with numbered navy circles, `split` with the navy `panel`, `price` cards, `faq`, `contact-grid` and `form-card`, `cta-band`, and the navy `site-footer`. The icons are the original site's line icons plus five drawn in the same style.

`v3.css` only adds what the original lacked: self-hosted fonts (the same Plus Jakarta Sans and Inter), the review notice, the Services menu, breadcrumbs, the diagnostic, the before-and-after page map, the article layout, and a few accessibility fixes listed below.

## Shared message and content

- **Description:** "Lucky Domains helps businesses build a digital presence that people, search engines, and AI systems can find, understand, and trust."
- **Hero (all three):** eyebrow "Websites · Search · Digital identity · AI visibility", headline "Build a digital presence people, search engines, and AI recognize.", calls to action "Build your digital presence" and "Explore our services", founder line "Founded and operated by Ken Ashe, CPA, PMP."
- **Framework:** Domain, Website, Search, Entity, AI. The About page notes that the original site said Domain, Site, Rankings, and that version 3 keeps that order and adds Entity and AI.
- **Services:** Website Design & Development, SEO & Search Visibility, AI Visibility & Brand Authority, Entity SEO & Digital Identity, Domain Acquisition & Brokerage.
- **Navigation:** Services (menu with all five, All services, How we buy domains), Work, About, Insights, Founder, Contact, and "Start a project".

`phase-3/shared/content.json` is the single source, written by `tools/p3_content.py` from the original site's copy, the already-checked Phase 2 content, and the sources below.

## Pages (sixteen in each concept)

Home · Services · Website Design & Development · SEO & Search Visibility · AI Visibility & Brand Authority · Entity SEO & Digital Identity · Domain Strategy, Acquisition & Brokerage · How We Buy Domains · Work · Case study (LuckyDomains.io) · About · Founder · Insights · Research note ("Can domains become the identity layer for AI agents?") · News & Media · Contact

Inner pages share one set of section renderers (`tools/p3lib.py`) built from the original components. Each concept composes its own homepage and wraps the inner pages its own way.

## Concept A: Original, Evolved

The production site, kept recognizable and modernized: larger type, more space, a split navy hero, and the original components throughout.

**Motion**
1. **Recognition map** (hero). Pulses travel from "Your business" to People, Search engines, and AI systems, and the nodes lean slightly toward the cursor. Pause button; pauses on a hidden tab; static under reduced motion.
2. **Digital Presence Stack.** Five layer cards light in order, with a connecting line, as the section scrolls past.
3. **Section-aware layer bar.** A sticky bar under the header lists the five layers. On the homepage it highlights each layer as you read its section (Domain, Website, Search, Entity, AI). On inner pages it marks the page's layer and links to each service.

Plus the Where are you stuck? diagnostic.

## Concept B: Original, Editorial

The same original components, set for reading: a large left-aligned headline, a five-service index in the hero, the Lucky Domains story told as five layers in giant type, services as numbered editorial rows, an annotated case study, and a magazine-style insights block.

**Motion**
1. **Reading progress and a contents rail.** A thin progress line on every page. Every inner page has a sticky "On this page" rail that marks the section in view; on small screens it becomes a horizontal chapter strip.
2. **Scroll-linked layer words.** Domain, Website, Search, Entity, AI come into full weight as each crosses the middle of the screen.
3. **Before and after.** An identity example (a made-up dental practice, labeled) alternates between inconsistent and consistent, pausing on hover, focus, and a hidden tab, and stopping once the visitor chooses. Case-study markers highlight their note from the public decision log.

## Concept C: Original, Interactive

The original design with the most interaction, still readable and service-led.

**Motion**
1. **Presence map** (hero). Ten signals start scattered and settle around one identity, then a slow tour lights one at a time. Problems ("What is holding you back?") and signals are selectable and name the service to start with. Pauses on hover, focus, and a hidden tab; stops once the visitor chooses anything.
2. **Layers light the map.** In "How recognition is built", a sticky map lights each layer's signals as its text reaches the middle of the screen.
3. **Example checks.** Each service page, and the homepage's service tabs, step through five examples of what Lucky Domains checks, labeled as illustrative. Pause button; pauses on hover, focus, and a hidden tab.

Plus a six-question presence self-check that updates as boxes are ticked and names a starting service. It stores and sends nothing.

The map engine is the one tested in Phase 2, restyled for the navy hero. It uses no library and no WebGL.

## Sources and factual limits

| Claim | Source |
|---|---|
| Same SEO fundamentals apply to Google's AI features; no special schema or AI text files needed | [Google Search Central: AI features and your website](https://developers.google.com/search/docs/appearance/ai-features) and the [AI optimization guide](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide) |
| Bing Webmaster Tools reports cited pages and grounding queries for Copilot and Bing AI answers | [Bing Webmaster blog, October 2026](https://blogs.bing.com/webmaster/2026/10/introducing-topics-portfolio-beta-in-ai-performance/) |
| Domain process, fee terms, Entity SEO levels, values, How we buy domains | Original production pages at `efed1de` |
| LuckyDomains.io case study | `kenashe/luckydomains` DECISIONS D1, D4, D8, D11 |
| Founder background, credentials, speaking | Original founder page and kenashe.ai |
| ZeroHuman and AI Agent Economy | kenashe.ai build records |

- No traffic, ranking, lead, or AI-citation figures are claimed. The one number in the case study, 93 internal links rewritten, is a work figure from the decision log.
- Engagements follow the original site (Domain Hunt, Growth SEO, Full Launch, Entity SEO Audit), with Website Build and the Entity SEO Audit broadened to include AI visibility. Pricing is not listed, as on the live site.
- "Website Build" as a named engagement and "AI Visibility" deliverables come from the approved direction, not from the live site.
- The before-and-after uses a made-up business and is labeled. The example checks are labeled illustrative.
- The research note is labeled "Draft for review. Not published." and says Lucky Domains does not sell agent identity.
- The News page links the real June 24, 2026 release and labels a placeholder for a future announcement as sample copy.
- Insights titles other than the research note are labeled as planned.
- Concept C uses the confirmed company location: Berkeley Heights, New Jersey. No street address is shown.

## Accessibility fixes over the original

- The original `.reveal` sections and FAQ answers stay hidden without JavaScript. Version 3 shows them.
- The original green link color (`#0FA968`) and the green buttons fall below WCAG AA contrast on white. Version 3 uses `#0A7A4B` for links and button fills.
- The footer uses `h2` labels instead of `h4` to keep the heading order valid.
- Added: a Services menu button with `aria-expanded`, closed with Escape; breadcrumbs; visible focus on every control; labeled form fields with no `name` attributes, so forms cannot send.

## Open questions

- Should Local SEO and Google Business Profile keep their own page eventually?
- Should the research note be published on Lucky Domains or KenAshe.ai, or stay a draft? Until Ken decides, it remains review-only.

Confirmed: Website Build and Entity and AI Visibility Audit are named, scoped engagements. Case studies do not identify clients. The LuckyDomains.io case study covers the company's own site.

## Preferred concept

Ken chose Concept C, Original, Interactive, as the preferred design direction for review. The hero presence map now centers the visible logo artwork within the circle at both map sizes. The review does not authorize a production rollout.

## Refinement: Original, Interactive, refined

Added November 24, 2026, at `/phase-3/interactive-refined/`. This is one refined version for owner approval, not another exploration. Concept C in `/phase-3/interactive/` and every other concept are unchanged. Nothing has been implemented on LuckyDomains.io.

**Guiding principle:** keep Original Interactive's presence map, service architecture, and visual identity, and add restraint, simplicity, and clarity.

### Why it changed

Ken's feedback on concept C: no public portfolio, a shorter and calmer homepage, one map instead of two, the diagnostic out of the hero, the presence check on its own page, static service detail, and lighter interior pages.

### Homepage, in order

1. Navy hero with the presence map
2. What is holding you back? (the diagnostic, on a light section)
3. Domain, Website, Search, Entity, AI (one connected line)
4. Five services, in commercial order, with a note on how Entity SEO and AI visibility differ
5. The company story: "Domains were the beginning. Not the boundary."
6. AI-powered execution. Human accountability.
7. Founder
8. Contact call to action
9. Footer

The homepage is 6,635 pixels tall on a 1440 pixel desktop (concept C: 10,623) and 11,359 on a 375 pixel phone (concept C: 18,204). About 38 percent shorter on both.

### Removed

- Work in the navigation and the footer
- The Work page and the LuckyDomains.io case-study page
- Selected work on the homepage
- Every "Read the case study" link and work-related call to action
- The second, sticky presence map in How recognition is built
- The auto-advancing "What each service actually checks" tabs on the homepage and the auto-advancing panel on each service page
- The six-question presence check on the homepage
- The problem buttons and recommendation panel inside the hero
- The before-and-after page map on the website page (it listed a Work page)

Nothing replaces the portfolio. No client examples, anonymized engagements, testimonials, or results were written.

### Retained interactions

1. **Presence map** (hero, the signature interaction). Six high-level signals: Domain, Website, Search, Profiles, Authority, AI systems. The signals start scattered and settle around the brand once. After that, one soft pulse at a time travels from a signal to the centre. Selecting a signal by mouse, touch, or keyboard shows what it includes (for example Profiles: official profiles, founders, structured data) and the related service. Fragmented and Recognized states remain. Signals lean a few pixels toward a mouse pointer.
2. **What is holding you back?** Five options. Choosing one shows a concise explanation, the relevant service, three first steps, and a link, in the same section, so no one has to scroll back to the hero. It also lights the related signals on the map. A line states that it is a starting point, not a diagnosis.
3. **Five-layer progression** (supporting motion). A connected line draws once when the section scrolls into view. No sticky section and no scroll-jacking.

Motion rules: the pulse pauses on hover, on focus, when the map is off screen, on a hidden tab, while a signal is selected, and with the Pause button. Under reduced motion nothing moves, the map shows the recognized state, and everything is still selectable. Without JavaScript the six signals, the five recommendations, the layers, and the check questions are plain text.

### Digital Presence Check

`/phase-3/interactive-refined/tools/digital-presence-check/`. Ten questions in five areas (Domain, Website, Search, Identity, AI visibility), each with Yes, No, and Not sure. The result names areas to look at and links to the related service. It never gives a score, and when every answer is Yes it says that does not mean there are no problems. The page states: "This is a preliminary self-check, not a technical audit." It runs entirely in the browser. It has no form element, no account, no storage, no cookies, and no network requests. Linked from the Services menu, the homepage services grid, the Services page, Insights, Contact, and the footer.

The domain question was rewritten: a business does not need an exact-match domain, it needs a suitable one that it controls.

### Service pages

Each of the five service pages now has a static section, "What we look at" (or "What the work involves" for domains), built from the old example checks and the service copy:

- Website Design & Development: information architecture, navigation, responsive design, accessibility, page performance, canonical URLs, structured data, forms, maintainability
- SEO & Search Visibility: crawlability, indexing, internal linking, search intent, technical errors, content structure, local search signals, Search Console data
- AI Visibility & Brand Authority: brand-related queries, AI-generated descriptions, source and citation patterns, first-party content quality, important unanswered questions, external authority signals
- Entity SEO & Digital Identity: Organization and Person structured data, identity consistency, official profiles, founder relationships, canonical entity home, entity disambiguation
- Domain Acquisition & Brokerage: ownership research, valuation, acquisition strategy, outreach, negotiation, transfer and escrow

Interior pages use a short, light hero: compact breadcrumbs, a navy heading, a shorter introduction, one call to action, and on service pages a small diagram of where the service sits in the five layers. On a 1440 pixel desktop the first content section now starts 440 to 570 pixels down the page (concept C: 720 to 900).

### First-party examples

Three service pages carry one example each, labeled "First-party example" and stated to be our own work, not client work:

| Page | Example | Source |
|---|---|---|
| Website Design & Development | How LuckyDomains.io was rebuilt, and the image pipeline on KenAshe.ai | `kenashe/luckydomains` DECISIONS.md; KenAshe.ai build record |
| SEO & Search Visibility | The Autonomous SEO Agent, an internal system (63 sites researched, 8 profiles confirmed live, no SEO impact established) | KenAshe.ai build record |
| Entity SEO & Digital Identity | The founder's own Person data across KenAshe.ai and LuckyDomains.io | Structured data on luckydomains.io |

AI Visibility and Domains have no example. No documented first-party AI-answer experiment was available to cite, and domain transactions are confidential.

### Pages (fifteen)

Home · Services · Website Design & Development · SEO & Search Visibility · AI Visibility & Brand Authority · Entity SEO & Digital Identity · Domain Acquisition & Brokerage · How we buy domains · Digital Presence Check · About · Founder · Insights · Research note ("Can domains become the identity layer for AI agents?") · News & media · Contact

Navigation: Services (menu with the five services, All services, How we buy domains, Digital Presence Check), About, Insights, Founder, Contact, and "Start a project".

### Files

- `tools/p3_r.py`: templates. `tools/p3_r_content.py`: the copy that differs from the shared content, written to `phase-3/interactive-refined/content.json`.
- `phase-3/interactive-refined/css/style.css` and `js/main.js`: the refinement's own layer. It still loads `phase-3/shared/original.css` (the production stylesheet, unchanged) and `v3.css` first.
- Screenshots: `phase-3/screenshots/r-*.jpg` (`python3 tools/p3_shots.py <base> --only r`).
- Audit: `python3 tools/p3_audit.py <base> /path/to/axe.min.js --only interactive-refined`.

### Test results (November 24, 2026)

- axe-core (WCAG 2.1 A and AA, plus best practices): no violations on any of the 15 pages at 375 and 1440 pixels.
- Chromium and Firefox at 320, 375, 390, 768, 1024, and 1440 pixels: no horizontal overflow, no console errors, no broken images, no text under 12 pixels, no touch target under 24 pixels.
- Layout shift: 0 on every page at desktop and phone widths.
- 98 behavior checks pass in Chromium and Firefox: keyboard order and visible focus, menus and Escape, the map by click, touch, and keyboard, the Pause button, the diagnostic, the progression, the Digital Presence Check (including that it stores and sends nothing), the inert contact form, reduced motion, and no JavaScript.
- WebKit could not start in the build environment (missing system libraries), so Safari is not verified.
- Lighthouse was not run (it cannot be installed in the build environment).
- First-load transfer: 267 KB for the homepage and 242 to 334 KB for interior pages, with no third-party requests. Concept C's homepage is 275 KB. The refinement's own CSS and JavaScript total 30 KB uncompressed.

### A fix carried over from the original design

With five navigation links instead of six, the closed mobile menu was short enough to show a sliver above the header. The refinement hides the closed menu fully, which also keeps its links out of the keyboard order until it is opened.

### Open questions for Ken

1. **Growth SEO** is still listed as a monthly engagement on the Services page, as on the live site. Is ongoing monthly SEO still offered?
2. **AI Visibility example.** Is there a documented first-party experiment on AI-generated answers that should be cited on that page? None was used.
3. **Founder page.** The brief mentions finance, data, and product leadership and published work. The page uses only facts already on record (S&P Global, EY, Noom, Prudential Financial; Forbes Business Council membership). Data leadership and specific published pieces need a source before they are added.
4. **Research note.** It keeps its question title, "Can domains become the identity layer for AI agents?", and is labeled an emerging topic, not a service. Should the title change to "Domains as Identity for AI Agents"?
5. **News sample.** The News page still shows a labeled placeholder for a future repositioning announcement. Keep or remove?
6. **URLs at launch.** The live site uses `/founder/ken-ashe/` and `/news/website-relaunch/`. The refinement uses `/founder/`. Any production migration needs its own plan that keeps existing URLs working.

### Design judgment

The refinement is the stronger site. The homepage now has one idea per section and two interactions that earn their place. The map explains the business faster with six signals than it did with ten, and the diagnostic is more useful on its own than it was inside the hero. The interior pages read like a professional services site, not a product demo. The trade-off is that the site shows less evidence of delivered work, so credibility rests on the depth of the service pages, the founder, and the first-party examples. That is the right trade for a founder-led studio that does not publish client work.
