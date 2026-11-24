# Concepts and design notes

Facts as of November 23, 2026. No production direction has been selected.

## The brief, in one paragraph

Lucky Domains is broadening from a domain, website, and SEO practice into a founder-led digital venture studio, while domain acquisition and brokerage stay an active service. Ken Ashe builds in public on KenAshe.ai. Lucky Domains builds and operates the ventures and runs the commercial services. Standalone brands face their own customers. The site should summarize ventures and send readers to KenAshe.ai for the full build record, without becoming a copy of it and without looking like an agency.

Company description used everywhere:

> Lucky Domains is a founder-led digital venture studio building AI applications, digital identity systems, and internet-native products, while continuing its original domain acquisition and brokerage practice.

## Concept A: Venture Lab

**Thesis.** A premium digital venture studio meets an experimental technology lab. A visitor should think "this company is building unusual internet businesses."

- **Visual system.** Near-black graphite, warm off-white text, one accent (the logo green `#16C784`), a restrained amber used only for "experiment" and "limits". Thin borders, a dot field, generous space.
- **Type.** Bricolage Grotesque for statements, Inter for reading, JetBrains Mono for status, dates, networks, and metadata.
- **Layout.** Asymmetric and editorial: wide venture cards that alternate sides, offset service panels, oversized stage numerals.
- **Headline.** "Domains were the beginning. Not the boundary."
- **Story.** A four-step progression (Domains, Identity, Agents, Ventures) with a sticky rail.
- **Ventures.** "Files" with a metadata table and a real artifact: the first mainnet order payload, the ENS storefront record, the tracker counts, a screenshot of the live site.
- **Domain business.** A full-width "The domain desk is still open" band, the first and largest service, a row in the hero status stack, and the header call to action.
- **KenAshe.ai.** A build-log link on every venture, a founder strip, a "Two sites, two jobs" panel, and a footer column.
- **Logo.** Reversed wordmark in the header (navy recolored to warm white, green untouched, geometry untouched). The footer shows the original, the reversed version, and the icon side by side, labeled.

Motion (all in `concept-a-venture-lab/js/main.js`):

| System | What it does | Pauses or falls back |
|---|---|---|
| Dot field | A canvas grid that brightens toward the cursor. With no pointer it drifts slowly. | Runs only while visible. Static under reduced motion. |
| Operating-status stack | Cycles through four real areas of work every 4.2 seconds. | Pauses on hover and focus, has a Pause button, stops when the tab is hidden. All rows open with no JavaScript or with reduced motion. |
| Progression rail | IntersectionObserver marks the active stage, moves the marker, and draws the line. | Becomes a plain list on small screens. |
| Proximity spotlight | Card glow and border respond as the cursor approaches. | Decorative only. Metadata is always readable. Off for touch. |
| Artifact depth | Evidence panels shift a few pixels with scroll (transform only). | Off below 1080px and under reduced motion. |
| Reveals | Sections fade up once. | Shown immediately under reduced motion. |

## Concept A v2: Venture Lab refinement

Path: `concept-a-venture-lab-v2/`. Template: `tools/concept_a_v2.py`. Own `css/style.css` and `js/main.js`. Screenshots: `screenshots/v2-*.jpg`. Created November 23, 2026.

**Why.** Concept A was the favored direction, and review found six problems worth fixing before it could become a production foundation: visitors had to scroll through the company's history before seeing what it does; the domain practice sat seven phone screens down; status chips mixed different kinds of thing; raw payloads were the first visual a visitor had to interpret; small, widely tracked monospace labels were hard to read; and almost every surface reacted to the pointer. v2 fixes those without becoming a fourth direction. The original is preserved unchanged.

**Preserved.** Near-black graphite, warm off-white text, the logo green as the only primary accent, the reversed logo on dark, the headline "Domains were the beginning. Not the boundary.", the operating-status stack, evidence as imagery, "The domain desk is still open.", the Domains, Identity, Agents, Ventures progression, the domain-acquisition call to action in the navigation, the hero dot field, section-aware motion, and the restrained, founder-led voice.

**Homepage, recomposed.** Hero and operating status. Then a Build, Operate, Acquire strip. Then ZeroHuman as the single featured venture. Then two compact "More from the lab" records. Then a condensed progression. Then the light Domain Desk. Then a short "How it fits together" statement and the footer. The homepage is 24 percent shorter at 1440 pixels (7,487 to 5,697) and 22 percent shorter at 375 pixels (10,878 to 8,537). Depth moved to the Ventures page, the venture files, and KenAshe.ai rather than being cut.

**Founder introduction.** One line beside the featured venture: "Founded by Ken Ashe. Read the full build record on KenAshe.ai." Ken Ashe links to the Founder page; the build record links to the ZeroHuman log. The homepage portrait strip was removed. The Founder page keeps the portrait, CPA, CGMA, PMP and PMI-ACP credentials, career, speaking, and narrative, and now states the split plainly: KenAshe.ai is the personal creator and build-in-public site, Lucky Domains is the operating company and the home of the ventures.

**Warm Domain Desk.** The brokerage section is now warm paper (`#F3EFE6`) with navy text and the original full-color logo, joined to the dark page by a green hairline and a small "The original practice" tab that straddles the edge. A faint navy dot grid echoes the hero field so it reads as part of the same system. It keeps the ACTIVE label, the four-step process, the success-based fee terms, and both calls to action. The primary section on the Services page uses the same treatment, and the domain path on Contact turns paper-colored when selected. The contrast is intentional: experimental work on dark, the established client practice on light.

**Typography and contrast.** Navigation moved from 12.5 pixel uppercase monospace to 15 pixel Inter. Metadata, eyebrows, chips, captions and footer labels are 12 to 14.5 pixels with tracking cut roughly in half. Monospace is kept for metadata, dates, networks and payloads; explanatory text uses Inter. Secondary text brightened (`#A3A59C` to `#B5B6AE`, 9.6:1) and the dim tier moved to `#9A9D94` (7.1:1). The hero's second line is `#C9C3B8`: 84 percent of the primary line's brightness, 11.2:1 contrast, with a thin green underline under "boundary" that draws once. No visible text in v2 is smaller than 12 pixels at 320 to 1440 pixels wide.

**Portfolio taxonomy.** Every record shows two labels: what it is (type) and the status from its public build record. Additive fields in `shared/content.json` carry this so facts are not duplicated in templates.

| Record | Type | Status | Group |
|---|---|---|---|
| ZeroHuman | Autonomous service | LIVE | Operating ventures |
| AI Agent Economy | Experiment | SHIPPED | Experiments and research |
| Sir Pitches-a-Lot | Competition agent | SHIPPED | Experiments and research |
| Autonomous SEO Agent | Internal operating system | LIVE | Internal systems and studio builds |
| LuckyDomains.io, agent-built | Studio build | LIVE | Internal systems and studio builds |
| Domain Acquisition & Brokerage | Commercial service | ACTIVE | Active services |

ACTIVE is the only status not taken from KenAshe.ai: it marks a service open to clients. The Ventures page shows the four groups by default with jump links; the status filter from the original was removed in favor of grouping. The hero status stack follows the order ZeroHuman, Domain Acquisition & Brokerage, AI Agent Economy, Autonomous SEO Agent.

**Evidence hierarchy.** Understandable process first, selected result second, raw evidence third. ZeroHuman gets a five-step diagram (Discover, Pay, Work, Deliver, Verify) built from the documented order steps, with verified labels such as `zerohuman.eth` and `0.0001 ETH`. The homepage then gives the selected result (the first mainnet Decision, recomputed and matched) beside the current limit (no outside agent purchase as of November 20, 2026), with the raw request and reply in a collapsed panel. Detail pages show the raw evidence open. AI Agent Economy gets a two-wallet transfer diagram (blocks 26385257 to 26385260). The Autonomous SEO Agent gets a 63-segment bar with 8 lit, matching its published counts. The real LuckyDomains.io screenshot stays on its record. No dashboards or product interfaces were invented.

**Motion, reduced.** Kept: the hero dot field (only while the hero is on screen), the status stack (now every 5 seconds, paused on hover, focus, a hidden tab, or the Pause button), a one-time draw of the order flow, a progression line that follows scroll position, and short reveals (12 pixels instead of 22). Removed: the global proximity spotlight on every card (now only inside the featured venture, only while the pointer is inside it), artifact parallax, the sticky progression rail, and the canvas grids on interior page headers (replaced with a static dot pattern). Under reduced motion nothing cycles or animates, the hero holds the same layout, and exactly one status row is open, so the call-to-action buttons stay inside the first screen (they were pushed below it in the original).

**Mobile.** At 375 pixels the headline is 40 pixels (from 44), "Not the boundary." fits on one line (two at 320), the hero is tighter, and the first status row starts at about 720 pixels, inside a 760-pixel screen. The Build, Operate, Acquire strip becomes compact rows, the order flow collapses to labeled steps, the "More from the lab" cards drop their diagrams but keep the evidence line, and the footer uses two columns. Status details have a fixed height so cycling never shifts content below.

**About page.** A five-step chain, Name, Presence, Identity, Agents, Ventures, explains why moving from domains into AI applications is an evolution, followed by one sentence: "Each step depends on the one before it." The three-part story, dated record, and structure follow.

**Footer.** One reversed wordmark, the company description, Ventures, Company (with Domain acquisition first), and Build record columns, then the review notice and the facts-as-of date. The logo-treatment gallery moved to the comparison page.

**Copy changes.** "Now the systems are operated, not just demonstrated." became "Some experiments became systems that run." The hero support line now adds "Domain acquisition and brokerage remain an active part of the business." The main hero CTA reads "Domain acquisition & brokerage". "Internet-native ventures" is used in the high-level descriptions. No new factual claims were added. Facts were rechecked against KenAshe.ai on November 23, 2026 and were unchanged.

**Remaining tradeoffs.**
- v2 is a little less mysterious than the original. That is the cost of being understood by domain clients.
- The light Domain Desk only works if it stays the one light moment. A second light section would make the site feel split.
- The taxonomy needs upkeep: when a build changes status on KenAshe.ai, the record here must change too.
- The homepage order flow is ZeroHuman-specific. A future featured venture needs its own verified diagram.
- The stylesheet grew from 27 KB to 40 KB (uncompressed) for the new components. The script shrank from 9.3 KB to 8.4 KB. Total homepage transfer is 278 KB against 270 KB.

**Recommendation.** v2 is recommended over the original as the foundation for any production build. It keeps what made Venture Lab distinctive and fixes the issues that would have hurt the brokerage business and nontechnical visitors. No production selection has been made and nothing has been implemented on LuckyDomains.io.

### Logo treatments in Venture Lab

| Treatment | File | Where v2 uses it |
|---|---|---|
| Original, full color | `shared/assets/logo-wordmark.png` | The light Domain Desk on the homepage and Services page |
| Reversed (concept treatment) | `shared/assets/logo-wordmark-reversed.png` | Header and footer on dark |
| Icon, reversed | `shared/assets/logo-icon-reversed-128.png` | Not used in v2 pages. Shown on the comparison page |
| Favicon | `shared/assets/favicon.ico`, `favicon-32.png` | Browser tab, unchanged from production |

The comparison page shows these side by side, replacing the gallery that sat in the original Concept A footer.

### After v2: the production candidate

Venture Lab v2 was approved as the production direction on November 23, 2026. It was then
ported to the production repository on a branch (`venture-lab-production-candidate` in
`kenashe/luckydomains`) with the final copy: the standardized company description, "Built by
Ken Ashe. Operated by Lucky Domains.", authorized project classifications, no concept
language, and no "Naming across DNS and ENS" service. That branch is hand-written static
HTML and is the source of truth. `production-candidate/` here is its generated, noindex
staging copy. The v2 concept at `concept-a-venture-lab-v2/` is unchanged and remains the
design reference. No v3 was created.

## Concept B: The Register

**Thesis.** A founder-owned company's journal of record. A "register" is both a publication and a list of holdings, which is what a venture studio that started in domain names keeps.

- **Visual system.** Warm paper `#F4EFE5`, ink derived from the logo navy, one text-safe green, a mint wash for standing sections, clay for sample and limit marks. Double rules, hairlines, hard-offset figure plates.
- **Type.** Fraunces (variable, with italics) for display and standfirsts, Instrument Sans for reading and small caps. No monospace except inside evidence figures.
- **Layout.** Masthead with the original full-color logo centered, a section bar, drop caps, margin notes, numbered figures with captions, Roman-numeral chapters.
- **Headline.** "First the name. Then everything built on it."
- **Story.** A dated history line on the home page, then a three-part essay on the about page.
- **Ventures.** Entries in a register (No. 01 to 06) that expand in place, a home-page feature on ZeroHuman, and long-form detail pages with "Limits, stated plainly."
- **Domain business.** A "Standing notice: the original practice continues" section, Chapter I of services, and entry No. 04.
- **KenAshe.ai.** Every entry ends with "Continue reading" on KenAshe.ai. The founder section states "KenAshe.ai keeps the record. Lucky Domains keeps the company."
- **Logo.** Original, untouched, in the masthead and colophon. The compact icon is used in the running head. A single-ink icon is shown in the colophon as an optional concept treatment.

Motion (all in `concept-b-the-register/js/main.js`):

| System | What it does | Pauses or falls back |
|---|---|---|
| Kinetic headlines | Font weight and tracking follow each heading's travel up the viewport (variable font axis). | Fixed weight under reduced motion. |
| Running head | A slim bar with the section title in view and a reading-progress line. | Title swaps without animation under reduced motion. Always visible on mobile, where it holds the Contents menu. |
| History line | The timeline rule draws with scroll and each event settles as the line reaches it. | Fully drawn under reduced motion. Vertical on mobile. |
| Preview plates | A small card follows the cursor over register rows. On keyboard focus it sits beside the row. | Not shown on touch or under reduced motion. It repeats information available on the linked page. |
| Page tone | Background shifts between paper and wash as sections pass. | Instant under reduced motion. |
| Figure wipes | Evidence figures reveal left to right once. | Shown immediately under reduced motion. |

## Concept C: Namespace

**Thesis.** Everything the company does has an address. The site reads as a namespace: a root, branches, and nodes that relate to each other.

- **Visual system.** The logo's own navy, green, and mint on a cool light ground. Rounded modular tiles, navy feature surfaces, dashed "route" lines.
- **Type.** Plus Jakarta Sans (the current brand heading face) for everything, IBM Plex Mono for addresses and paths.
- **Layout.** A map-first home page, tile grids, sticky record cards, a branch diagram on services.
- **Headline.** "Every venture starts with a name."
- **Navigation.** An address bar that shows the current path, tracks the section in view, and opens a site directory. Standard links sit beside it on desktop.
- **Story.** Four layers (Name, Presence, Identity, Agents) as a stack that opens.
- **Ventures.** Nodes on a map and cards in a grid, the same data both ways, filterable by domain of work. Detail pages are records with summary, flow, evidence, limits, and connections tiles.
- **Domain business.** The navy "root" module on home and services, a node on the map, and the first route on the contact page.
- **KenAshe.ai.** A "Two addresses, two jobs" diagram, a green build-log tile on every record, and a link in the map card.
- **Logo.** Compact icon in the header, original wordmark in the footer, reversed icon at the center of the map and in the footer as a labeled concept treatment.

Motion (all in `concept-c-namespace/js/main.js`):

| System | What it does | Pauses or falls back |
|---|---|---|
| Constellation map | SVG nodes drift slightly and lean toward the cursor. Selecting a node or a filter lights its relationships and updates a detail card. | Runs only while visible and while the tab is active. Static under reduced motion. Nodes are focusable buttons. The grid below carries the same information. A portrait layout is used on narrow screens. |
| Address bar | The fragment updates to the section in view. | Works as a plain menu without it. |
| Card rearrangement | Filtering moves matching cards to the front with a FLIP animation. | Reorders instantly under reduced motion. Non-matching cards dim but stay readable and usable. |
| Layer stack | Four plates separate when the section enters view and respond to hover, focus, and tap on the list. | Open and static under reduced motion. |
| Route lines and tiles | Dashed lines march along process routes. Tiles rise in once. | Off under reduced motion. |

No WebGL, no animation library, and no scroll-jacking in any concept.

## What is shared

`shared/content.json` holds the company description, pillars, story, dated timeline, six ventures, three services, founder facts, news items, and contact routes. All three concepts render from it, so a fact cannot differ between them.

## Source assets and their origins

| File in `shared/assets/` | Origin | Changed? |
|---|---|---|
| `logo-wordmark.png`, `logo-icon.png` | `kenashe/luckydomains`, `assets/` | No. Byte-for-byte copies. |
| `logo-*-reversed.png`, `logo-*-mono-light.png`, `logo-*-mono-ink.png`, `logo-icon-128.png`, `logo-icon-reversed-128.png` | Derived here by `tools/make_assets.py` | Color only. Each pixel is unmixed between the two brand colors and recolored. Geometry is untouched. Concept treatments, not replacements. |
| `favicon.ico`, `favicon-32.png`, `apple-touch-icon.png` | `kenashe/luckydomains`, `assets/` | No. |
| `ken-ashe-2026-square.jpg` | `kenashe/luckydomains`, `assets/` | No. Concept A and B display it in grayscale with CSS. |
| `artifact-luckydomains-io.jpg` | Screenshot of https://luckydomains.io/ taken November 23, 2026 | Captured for this review. |
| `shared/fonts/*.woff2` | Google Fonts (Bricolage Grotesque, Inter, JetBrains Mono, Fraunces, Instrument Sans, Plus Jakarta Sans, IBM Plex Mono), Latin subsets | SIL Open Font License. Self-hosted so the review site makes no third-party requests. |

The production logo files were not edited. Venture "artifacts" (order payloads, the ENS record, tracker counts) are typeset from text published on KenAshe.ai, not invented and not images of dashboards.

## Where each fact comes from

| Content | Source |
|---|---|
| Services, brokerage process, fee terms, "what this is not" | luckydomains.io services, how-we-buy-domains, and entity SEO pages; `PRODUCT.md` |
| Founder background, credentials, career, quote | luckydomains.io founder page; kenashe.ai about page |
| Speaking and judging, Forbes Business Council membership | kenashe.ai about page |
| ZeroHuman, AI Agent Economy, Autonomous SEO Agent, Sir Pitches-a-Lot | The matching build pages on kenashe.ai |
| "LuckyDomains.io, agent-built" | kenashe.ai building index; `kenashe/luckydomains` documentation |
| June 24, 2026 release | luckydomains.io newsroom |
| Venture statuses (LIVE, SHIPPED) | The labels shown on kenashe.ai on November 23, 2026 |

## Content notes and open questions for Ken

1. **Attribution is the proposal.** KenAshe.ai currently presents these builds as Ken's own. Showing them as Lucky Domains ventures is the positioning this exercise explores, and the ventures pages say so in a footnote.
2. **AI Agent Economy status.** KenAshe.ai labels it SHIPPED. The concepts show "Experiment" as its kind and SHIPPED as its status, not a separate EXPERIMENT status.
3. **ZeroHuman maturity.** Every concept states that, as of November 20, 2026, no outside agent has bought from it and both paid orders came from the founder's test buyer. Update this the day that changes.
4. **Autonomous SEO Agent counts.** "63 researched, 8 confirmed live" is the figure on the build page and is undated there.
5. **Sir Pitches-a-Lot date.** The building index says June 2026 (Agent Battle Night, NY Tech Week) and the build page says August 2026. The concepts show "2026" only.
6. **Digital Identity & Presence.** Entity and structured-data work is an existing service. "Naming across DNS and ENS" is marked "proposed scope" because it is not offered on the live site today.
7. **Founding year and location.** No founding year is published, so none is shown. The live site uses two different New Jersey towns, so the concepts say "New Jersey" only.
8. **News.** One real company release, three project updates sourced to build pages, and one item marked "SAMPLE CONCEPT COPY · NOT PUBLISHED".
9. **Contact.** Four routes: domains, venture or product partnerships, media or speaking, general. No AI consulting route was created.
10. **Email.** `info@luckydomains.io` appears as a plain `mailto:` link because it is the published address. No form posts anywhere.

## Verification snapshot (local, November 23, 2026, updated for v2)

- 42 pages. All carry the noindex meta tag. All 40 concept pages carry the review notice, a Lucky Domains logo treatment, and domain acquisition. Every concept home page, including v2, shows the original full-color logo.
- No em dashes or en dashes in any HTML, CSS, JS, JSON, or Markdown file.
- All internal links resolve. All external links returned 200.
- 375, 768, and 1440 pixels: no horizontal overflow and no console errors on any page. v2 was also checked at 320 and 390 pixels, in Chromium and Firefox.
- axe-core 4.10 (WCAG 2 A, AA, and best-practice rules) at 1440 pixels: no violations on any page.
- Reduced motion: no running animations and no hidden content on any concept home page.
- Home page weight, uncached: A 269 KB, B 324 KB, C 141 KB. Layout shift at or near zero.

## Known rendering differences and limits

- Tested in Chromium (all pages) and Firefox (v2 pages), with Playwright, headless. WebKit could not run in the build sandbox, so Safari rendering is untested.
- Concept A's card border glow uses CSS masks and `color-mix()`. Older browsers show a plain border.
- Concept B's kinetic headlines need variable-font support. Without it the heading keeps one weight.
- Concept B's selected-route styling uses `:has()`. Without it the radio button alone shows the selection.
- Concept C's layer stack uses 3D transforms. On very small screens it is scaled down.
- `backdrop-filter` on sticky headers falls back to a solid translucent color.
- Lighthouse could not be installed in the build sandbox. Scores should be taken from the deployed URL.
