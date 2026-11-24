# Phase 2 concepts and design notes

Created November 24, 2026. Review only. No direction has been selected and nothing has been implemented on LuckyDomains.io. Phase 1 notes stay in `CONCEPTS.md`, unchanged.

## Corrected business positioning

Lucky Domains is a digital presence studio for the AI era. It helps businesses build a digital presence that people, search engines, and AI systems can find, understand, and trust.

Central description, used in all three concepts:

> Lucky Domains helps businesses build a digital presence that people, search engines, and AI systems can find, understand, and trust.

Longer version:

> Lucky Domains designs and builds websites, improves search and AI visibility, strengthens entity and brand signals, and secures the domains that anchor a business’s digital identity.

Five services, in this order:

1. Website Design & Development
2. SEO & Search Visibility
3. AI Visibility & Brand Authority
4. Entity SEO & Digital Identity
5. Domain Acquisition & Brokerage

The story that connects them is the Digital Presence Stack: Domain, Website, Search, Entity, AI. Each layer makes the next one work.

AI appears in two roles only: it changes how the work is done ("AI-powered execution with human accountability"), and it changes where a brand needs to be recognized. AI is not sold as a product, and no concept promises rankings, AI citations, mentions in a particular system, or a Knowledge Panel.

## Why Phase 2 exists

Phase 1 moved too far from the commercial business. Venture Lab and its refinements put ZeroHuman, autonomous agents, and a venture-studio identity at the center. Those projects are good evidence of Ken's experience, but they are not what customers buy. The current light site had stronger commercial clarity: domain acquisition, websites, SEO, and a direct relationship with the founder.

Phase 2 starts from that site, keeps its clarity, and updates the message for a discovery environment shaped by AI.

## How Phase 2 differs from Phase 1

| | Phase 1 | Phase 2 |
|---|---|---|
| Company | Digital venture studio | Digital presence studio |
| Center of the homepage | Ventures and experiments | Websites, search, identity, AI visibility, domains |
| Palette | Mostly dark (Venture Lab) | Primarily light in all three |
| Navigation | Ventures first | Services, Work, About, Insights, Founder, Contact |
| Ken's experiments | Featured ventures | A small "From the lab" section, linked to KenAshe.ai |
| Agent identity | Implied as a business line | One clearly labeled research section on the domain page |
| Baseline | Venture Lab | The current production site |

Phase 1 remains online as an archive at the repository root. The root landing page now carries a short notice pointing to Phase 2.

## Shared content model

`phase-2/shared/content.json` is the single source for all three concepts: company description, hero copy, navigation, the five stack layers, outcomes, the five services, page copy for each service page, the diagnostic, AI copy, lab entries, case studies, founder facts, planned insights, contact copy, and the data for Concept C's map and site graph. Each concept has its own template (`tools/p2_a.py`, `p2_b.py`, `p2_c.py`), stylesheet, and script. `tools/p2lib.py` holds only the page head, the review notice, relative paths, the Services menu, and the inert form. `phase-2/shared/p2.js` handles the menu, Escape, and form behavior shared by all three.

Phase 2 never reads or writes Phase 1 content. Adding Phase 2 left every Phase 1 concept page, stylesheet, script, and screenshot byte-for-byte unchanged.

## Concept A: Original, Evolved

**Thesis.** The current Lucky Domains site, redesigned for 2027. The safest and most production-ready direction.

- **Visual system.** White and warm off-white, the original full-color logo, the existing green (`#16C784`, with `#0A7A4B` for text) and navy (`#0C2340`). Plus Jakarta Sans headings and Inter body text, the same families the live site uses. Rounded cards, soft mint gradients, more whitespace.
- **Message.** The preferred headline exactly: "Build a digital presence people, search engines, and AI recognize." The founder line, "Founded and operated by Ken Ashe, CPA, PMP," sits under the calls to action.
- **Homepage.** Hero, Digital Presence Stack, three outcomes, Where are you stuck?, Website Design & Development, Search, Entity, and AI, Selected work, story, how AI changes the work, From the lab, Insights, Founder, Contact.
- **Motion.**
  1. Hero presence card. The five layers light in order on a card for "yourbusiness.com", hold, and repeat. It pauses on hover, focus, a hidden tab, and a Pause button. Under reduced motion it is static and fully lit.
  2. Digital Presence Stack. Each step's slab settles into place in a sticky stack as the step reaches the middle of the screen. No scroll-jacking. On phones the sticky stack is hidden and the list reads on its own.
  3. Diagnostic. Five radio options reveal a recommended starting point, why, and the first three steps, announced to screen readers. Without JavaScript all five answers are listed.

## Concept B: Editorial Authority

**Thesis.** A respected digital strategy, web, and visibility studio that explains its thinking. Content-led, warm, and permanent-feeling, with services kept prominent.

- **Visual system.** Warm paper (`#F7F3EA`), ink navy, one text-safe green, a clay accent for cautions and concept labels. Newsreader for headlines and standfirsts, Public Sans for reading. Double rules, hairlines, drop caps, numbered chapters, margin notes.
- **Message.** "Be the business people, search engines, and AI can explain." A numbered services index sits directly under the cover so services are never more than one scroll away.
- **Homepage.** Cover, services index, five eras of discovery, the website feature, search, entity, and AI, an annotated case study, the story, method (how AI changes the work), Insights given full space, From the lab, Founder, Contact.
- **Motion.**
  1. Reading progress and a contents rail. A hairline in the masthead fills as you read. Inner pages have a sticky "On this page" rail that marks the chapter in view; on phones it becomes a horizontal chapter strip.
  2. Eras of discovery. A vertical rule fills with scroll position and each era (the address, the destination, the result, the record, the answer) is marked as the rule reaches it.
  3. Before and after. On the website page, a two-state view switches between a page map organized around the company and one organized around what people need, and the pages settle into place. Case-study markers highlight their margin note on hover, focus, or tap.

## Concept C: Intelligent Presence

**Thesis.** The most interactive direction, still light and commercially clear. It shows how recognition is built rather than describing it.

- **Visual system.** Cool light ground (`#F5F8FB`), navy type, green signals, a color per layer (domain navy, website blue, search green, entity violet, AI rust). Manrope throughout. Modular tiles, pill tags, a navy call-to-action band.
- **Message.** "Make your business easy to find, understand, and trust." Readable in seconds; the map is beside it, not in front of it.
- **Homepage.** Hero with the presence map and a problem selector, a layer explorer, outcomes, website design, search, entity, and AI, work tagged by layer, story, AI and the work, lab and insights, founder, contact.
- **Motion.**
  1. Presence map. Ten signals (domain, website, content, search, structured data, profiles, reviews, founders, citations, AI systems) start scattered with broken links, then settle around one clear identity. A slow tour then highlights one signal at a time. The tour pauses on hover and focus, stops when the tab is hidden, and ends for good once the visitor chooses anything. A toggle switches between the fragmented and recognized states. Each signal is a keyboard-operable button that explains itself and links to the service. A portrait layout is used below 520 pixels, with no overlapping labels at any tested width.
  2. Problem selector. Five problems light the signals involved and name the service to start with.
  3. Internal-link graph. On the website page, selecting a page highlights the pages it links with. A text list of every link is provided for screen readers and readers without JavaScript.
  - The layer explorer is a standard tablist with arrow-key, Home, and End support.

No WebGL and no animation library. The SVG is generated in the browser from JSON in the page.

## Case studies and evidence

Only public evidence is used.

| Case | Source | Notes |
|---|---|---|
| LuckyDomains.io, off Wix onto a site the company owns | `kenashe/luckydomains` DECISIONS D1, D4, D8, D11; kenashe.ai building index | 93 internal links rewritten is the one figure, and it is a work figure, not an outcome. No traffic, ranking, or lead figures are claimed |
| One identity across two sites | Structured data on luckydomains.io and kenashe.ai | One Person identifier, 19 profile references, four credentials. No Knowledge Panel is claimed |
| Rebuilding an image pipeline | kenashe.ai build record | Ken's own site: 2,083 PNGs to WebP, image source tree 95 percent smaller |
| Internal agent for profile building | kenashe.ai Autonomous SEO Agent build record | 63 sites researched, 8 profiles live, no SEO impact established |
| A confidential domain acquisition | None | Labeled "Layout demonstration. Concept content." No client, price, or outcome |

Lab entries (ZeroHuman, AI Agent Economy, the Autonomous SEO Agent) each carry their stated limitation, including that no outside agent had bought from ZeroHuman as of November 20, 2026.

## Source assets

| Asset | Origin |
|---|---|
| `shared/assets/logo-wordmark.png`, favicons, `ken-ashe-2026-square.jpg` | `kenashe/luckydomains`, unchanged copies made in Phase 1 |
| `shared/fonts/newsreader-normal-300-700.woff2`, `publicsans-normal-400-700.woff2`, `manrope-normal-400-800.woff2` | Google Fonts Latin subsets, SIL Open Font License, added for Phase 2 and self-hosted |
| `jakarta-normal-400-800.woff2`, `inter-normal-400-600.woff2` | Phase 1 files, reused |
| `phase-2/screenshots/current-home-*.jpg` | Read-only captures of the live luckydomains.io homepage |

All three concepts use the original full-color logo. No logo was redrawn or recolored for Phase 2.

## Factual limits

- Services and copy follow what the live site already offers, reorganized. "AI Visibility & Brand Authority" groups work the site already describes under Entity SEO (AI systems understanding a brand) with baselines and monitoring. Its list of activities is what the prompt for this round approved.
- "Analytics foundations" is offered as client website work. LuckyDomains.io itself uses no analytics.
- "Replies come within one business day" and "The first consultation is free" come from the live site.
- Location is omitted: the live site names two different New Jersey towns.
- Insights are planned titles only, each labeled as not yet published.
- Agent identity is described as an open question with no settled standard, and the page says Lucky Domains does not sell an agent-identity product.

## Accessibility

- Semantic landmarks, one h1 per page, heading order checked by axe, skip links, visible focus rings, breadcrumbs on inner pages.
- Services menu: a real link to the overview plus a disclosure button (`aria-expanded`), closed with Escape. Without JavaScript it opens on hover and focus, and every service is also in the footer.
- Interactive pieces use native controls (radios, buttons, `details`, tablist) with text equivalents. No essential information is hover-only.
- Reduced motion: nothing cycles or animates; every state is shown or reachable.
- Without JavaScript: navigation, all diagnostic answers, all layer panels, every map signal, both architecture views, and the link list are visible.
- No visible text under 12 pixels, touch targets of at least 24 pixels, no horizontal overflow from 320 to 1440 pixels.

## Performance

| Concept | Home, first load | Inner pages | Script |
|---|---|---|---|
| A | 271 KB | 207 to 208 KB | 3.7 KB plus 2.1 KB shared |
| B | 343 KB | 285 to 286 KB | 4.0 KB plus 2.1 KB shared |
| C | 239 KB | 164 to 166 KB | 13.9 KB plus 2.1 KB shared |

Measured locally, uncompressed, first uncached load, including the 47 KB founder portrait on home pages. Fonts dominate: Concept B's Newsreader file is 132 KB. No page makes a third-party request. Layout shift stayed at or below 0.0005 on every page.

Homepage length at 1440 pixels: A 11,771, B 11,381, C 9,452 pixels. All three carry the full requested homepage, and A is the longest. A production build should consider trimming the lab and insights sections from the homepage.

## Open questions

1. Is "AI Visibility & Brand Authority" a separately priced service, or part of SEO and entity work? The concepts present it as its own service.
2. Is "Ongoing" monthly work still offered? The live site offers Growth SEO monthly; the concepts keep a general ongoing engagement.
3. Should Local SEO and Google Business Profile stay prominent? They are listed under SEO.
4. Which case studies can use client names? None are named here.
5. Sir Pitches-a-Lot still has conflicting public dates, so it is not used.
6. Location: which New Jersey town, if any, should appear?

## Recommendation

Concept A, Original Evolved, is the strongest starting point. It says what Lucky Domains does fastest, it is closest to the site customers already know, it gives website design and SEO the most weight, and it is the cheapest to build and maintain on the existing static stack.

Two pieces from the others are worth borrowing if A is chosen: B's annotated case-study layout for the Work section, and C's presence map, simplified, for the AI Visibility and Entity pages where it explains something words do not.

No production selection or implementation has happened.
