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

## Verification snapshot (local, November 23, 2026)

- 32 pages. All carry the noindex meta tag. All 30 concept pages carry the review notice, the original logo, and domain acquisition.
- No em dashes or en dashes in any HTML, CSS, JS, JSON, or Markdown file.
- All internal links resolve. All external links returned 200.
- 375, 768, and 1440 pixels: no horizontal overflow and no console errors on any page.
- axe-core 4.10 (WCAG 2 A, AA, and best-practice rules) at 1440 pixels: no violations on any page.
- Reduced motion: no running animations and no hidden content on any concept home page.
- Home page weight, uncached: A 269 KB, B 324 KB, C 141 KB. Layout shift at or near zero.

## Known rendering differences and limits

- Tested in Chromium only (Playwright, headless). Safari and Firefox were not run.
- Concept A's card border glow uses CSS masks and `color-mix()`. Older browsers show a plain border.
- Concept B's kinetic headlines need variable-font support. Without it the heading keeps one weight.
- Concept B's selected-route styling uses `:has()`. Without it the radio button alone shows the selection.
- Concept C's layer stack uses 3D transforms. On very small screens it is scaled down.
- `backdrop-filter` on sticky headers falls back to a solid translucent color.
- Lighthouse could not be installed in the build sandbox. Scores should be taken from the deployed URL.
