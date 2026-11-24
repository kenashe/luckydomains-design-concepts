# Version 3 concepts and design notes

Created November 24, 2026. Ken prefers Concept C for further refinement. Review only; nothing in Version 3 has been implemented on LuckyDomains.io. Phase 1 (`CONCEPTS.md`) and Phase 2 (`PHASE_2_CONCEPTS.md`) notes are unchanged.

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
