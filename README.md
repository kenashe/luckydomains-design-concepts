# Lucky Domains: proposed redesign concepts

**Current round: [Version 3](#version-3-current-round).** Phase 2 and Phase 1 (Venture Lab, The Register, Namespace, Venture Lab v2, and the production candidate staging copy) are archived below.

Three complete design directions for a possible future LuckyDomains.io, for review and comparison.

**These are proposed design directions only. They do not modify LuckyDomains.io, KenAshe.ai, production repositories, DNS, forms, or integrations.**

Review site: https://kenashe.github.io/luckydomains-design-concepts/

| | Concept | Folder | In one line |
|---|---|---|---|
| A | Venture Lab | `concept-a-venture-lab/` | Dark, quietly technical, evidence as imagery |
| B | The Register | `concept-b-the-register/` | Warm paper, editorial, a company's journal of record |
| C | Namespace | `concept-c-namespace/` | Brand navy and mint, an interactive map, everything has an address |

**Selected direction refinement:** Venture Lab v2, at `concept-a-venture-lab-v2/`, refines Concept A after review. It is not a fourth direction. The original Concept A is preserved unchanged at `concept-a-venture-lab/`.

- Venture Lab v2: https://kenashe.github.io/luckydomains-design-concepts/concept-a-venture-lab-v2/
- Original Concept A: https://kenashe.github.io/luckydomains-design-concepts/concept-a-venture-lab/

Comparison page (including "Venture Lab: original vs v2"): https://kenashe.github.io/luckydomains-design-concepts/comparison/

Design reasoning, motion systems, asset origins, and open content questions are in [CONCEPTS.md](CONCEPTS.md).

## Version 3 (current round)

Three concepts built from the original production site. Each page loads the production
stylesheet unchanged (`phase-3/shared/original.css`), then `phase-3/shared/v3.css`, then the
concept's own layer. All three share one message, five services, and sixteen pages.

- Version 3 review landing: https://kenashe.github.io/luckydomains-design-concepts/phase-3/
- Version 3 comparison (includes the current site): https://kenashe.github.io/luckydomains-design-concepts/phase-3/comparison/
- Concept A, Original Evolved: `phase-3/original-evolved/`
- Concept B, Original Editorial: `phase-3/editorial/`
- Concept C, Original Interactive: `phase-3/interactive/`

Pages in each concept: home, services, five service pages (`services/website-design/`,
`services/seo/`, `services/ai-visibility/`, `services/entity-seo/`, `services/domains/`),
`how-we-buy-domains/`, `work/`, `work/luckydomains-io/`, `about/`, `founder/`, `insights/`,
`insights/domains-identity-for-ai-agents/`, `news/`, `contact/`.

Notes: [PHASE_3_CONCEPTS.md](PHASE_3_CONCEPTS.md). Build: `python3 tools/p3_build.py` (or
`tools/build.py` for everything). Screenshots: `python3 tools/p3_shots.py <base>` writes
`phase-3/screenshots/`. Audit: `python3 tools/p3_audit.py <base> /path/to/axe.min.js`.

## Phase 2 (archived)

Phase 2 corrects the business direction. Lucky Domains is presented as a digital
presence studio for the AI era: websites, SEO, entity and digital identity, AI
visibility, and domain acquisition and brokerage. All three concepts share one
positioning and one content file; they differ in design, structure, and interaction.

- Phase 2 review landing: https://kenashe.github.io/luckydomains-design-concepts/phase-2/
- Phase 2 comparison: https://kenashe.github.io/luckydomains-design-concepts/phase-2/comparison/
- Concept A, Original Evolved: `phase-2/original-evolved/`
- Concept B, Editorial Authority: `phase-2/editorial-authority/`
- Concept C, Intelligent Presence: `phase-2/intelligent-presence/`

Each concept has six pages: home, services, `services/website-design/`,
`services/search-ai-visibility/`, `services/domain-identity/`, and `work/` (a case
study template). About, Insights, Founder, and Contact appear as homepage sections
for now; full pages are deferred until a direction is chosen.

Design notes, motion systems, factual limits, and the recommendation are in
[PHASE_2_CONCEPTS.md](PHASE_2_CONCEPTS.md).

```
phase-2/
├── index.html                  Phase 2 review landing
├── comparison/                 Phase 2 comparison
├── shared/content.json         the one Phase 2 content file (positioning, services, facts, CTAs)
├── shared/p2.js                shared menu and inert-form behavior
├── shared/review-p2.css        additions to the neutral review styling
├── original-evolved/           Concept A: templates in tools/p2_a.py, own css/ and js/
├── editorial-authority/        Concept B: tools/p2_b.py
├── intelligent-presence/       Concept C: tools/p2_c.py
└── screenshots/                {a,b,c}-*.jpg and current-home-*.jpg (live site, read only)
```

Build and check:

```bash
python3 tools/build.py                       # regenerates Phase 1 and Phase 2 pages
python3 tools/verify.py --links              # noindex, notices, logo, forms, dashes, links
python3 -m http.server 8765 --directory ..   # serve the folder that holds this repo
python3 tools/p2_shots.py http://localhost:8765/luckydomains-design-concepts/
python3 tools/p2_audit.py http://localhost:8765/luckydomains-design-concepts /path/to/axe.min.js
```

Phase 2 and Phase 1 are kept as archives. They are not part of the version 3 comparison.

## Production candidate staging

`production-candidate/` is a noindex staging copy of the Venture Lab production
candidate. The real source is the `venture-lab-production-candidate` branch of
`kenashe/luckydomains`. This folder is generated from that branch and is never
edited by hand.

- Staged site: https://kenashe.github.io/luckydomains-design-concepts/production-candidate/
- Review notes: https://kenashe.github.io/luckydomains-design-concepts/production-candidate/review/

```bash
git clone -b venture-lab-production-candidate https://github.com/kenashe/luckydomains.git ../luckydomains
python3 tools/export_staging.py ../luckydomains     # regenerate production-candidate/
python3 tools/staging_review.py                     # rewrite the review page
python3 tools/staging_shots.py http://localhost:8765/luckydomains-design-concepts/production-candidate
python3 tools/verify.py --links
python3 tools/pc_audit.py http://localhost:8765/luckydomains-design-concepts/production-candidate /path/to/axe.min.js
```

Staging pages use absolute paths that start with `/luckydomains-design-concepts/`,
so preview them with the repository served under that name
(`python3 -m http.server 8765 --directory ..` from a folder named
`luckydomains-design-concepts`).

What the export changes, and nothing else: a path prefix, noindex on every page,
staging canonical and social URLs, a notice bar, a disabled contact form (access
key removed, endpoint replaced, submit blocked), and no `CNAME`, `robots.txt`,
`sitemap.xml`, docs, tests, or scripts. `production-candidate/STAGING.json`
records the source commit. The concept folders above are not touched by it.

## What this repository is, and is not

- It is a review site. Nothing here is production.
- Every page carries `<meta name="robots" content="noindex,nofollow,noarchive">` and `robots.txt` disallows all crawling.
- Every concept page shows the notice "Design concept only. Not the live Lucky Domains website."
- Forms are mockups. They have no `action`, no submit button, and no named text fields. Nothing is collected, stored, or sent.
- There is no analytics, no API key, no form credential, no `CNAME`, and no third-party request. Fonts are self-hosted.
- No production selection has been made. Choosing a direction, and building it, are separate future decisions.

## Structure

```
index.html                    review landing page
comparison/                   side-by-side comparison
shared/content.json           the one factual content layer used by all three concepts
shared/assets/                logo files, favicon, founder portrait, one real site screenshot
shared/fonts/                 self-hosted webfonts (SIL Open Font License); Phase 2 added Newsreader, Public Sans, Manrope
phase-2/                      Phase 2 concepts, review landing, comparison, screenshots
shared/review.css             neutral styling for the review pages
concept-a-venture-lab/        10 pages, css/style.css, js/main.js
concept-b-the-register/       10 pages, css/style.css, js/main.js
concept-c-namespace/          10 pages, css/style.css, js/main.js
concept-a-venture-lab-v2/     10 pages, css/style.css, js/main.js (refinement of Concept A)
screenshots/                  generated review screenshots
production-candidate/         generated noindex staging copy of the production candidate, plus review/
tools/                        generator and checks (not needed to view the site)
robots.txt, .nojekyll
```

Each concept, and v2, contains: home, ventures, three venture detail pages (ZeroHuman, AI Agent Economy, Autonomous SEO Agent), services, about, founder, news, and contact.

## How it is built

Plain static HTML, CSS, and vanilla JavaScript. No framework, no bundler, no package manager.

The HTML is generated by a small Python script so that all three concepts read the same facts from `shared/content.json`. The generated files are committed, so GitHub Pages serves them as they are and there is no build step on the host.

```bash
python3 tools/make_assets.py /path/to/luckydomains/assets   # only if logo treatments need regenerating
python3 tools/build.py                                       # regenerate every page
python3 tools/verify.py --links                              # safety, integrity and link checks
```

Each concept owns its templates (`tools/concept_a.py`, `concept_b.py`, `concept_c.py`, and `concept_a_v2.py` for the refinement), its stylesheet, and its script. They share content and nothing visual.

v2 reads extra, additive fields from `shared/content.json` (`portfolioCategory`, `displayType`, `displayStatus`, `featured`, `homepageSummary`, `homepageEvidence`, `evidenceVisual`, `resultNote` on ventures, and top-level `portfolioCategories` and `operatingModel`). The other concepts ignore them; adding them left every Concept A, B, and C page byte-for-byte unchanged.

To change a fact, edit `shared/content.json` and run `tools/build.py`. To change a design, edit that concept's CSS, JS, or template.

## Preview locally

```bash
git clone https://github.com/kenashe/luckydomains-design-concepts.git
cd luckydomains-design-concepts
python3 -m http.server 8000
# open http://localhost:8000
```

All links are relative, so the site works at any path, including the GitHub Pages project path.

## Deployment

GitHub Pages, "Deploy from a branch", branch `main`, folder `/ (root)`. Pushing to `main` redeploys. `.nojekyll` disables Jekyll processing. There is deliberately no `CNAME` file: the review URL stays on `kenashe.github.io`.

## Checks

```bash
python3 tools/verify.py --links        # robots meta, notice, logo, forms, dashes, internal and external links
pip install playwright && python3 -m playwright install chromium
python3 -m http.server 8765 --directory ..     # serve the parent folder so this repo is at /<folder>/
python3 tools/audit.py http://localhost:8765/<folder>/ /path/to/axe.min.js
python3 tools/screenshots.py http://localhost:8765/<folder>/              # v2 images only
python3 tools/screenshots.py http://localhost:8765/<folder>/ --originals  # also re-shoot A, B and C
```

`tools/audit.py` loads all 42 pages at 375, 768, and 1440 pixels and checks for horizontal overflow, console errors, small touch targets, axe-core WCAG 2 A and AA rules, and a reduced-motion pass.

## Screenshots

`screenshots/` holds the review images. Original concepts: `a-*.jpg`, `b-*.jpg`, `c-*.jpg` (home desktop and mobile, ventures, one extra view). Venture Lab v2 uses distinct names so the originals are never overwritten:

| File | View |
|---|---|
| `v2-home-desktop.jpg` | Homepage, 1440 x 900 |
| `v2-home-mobile.jpg` | Homepage, 375 x 760 at 2x |
| `v2-ventures-desktop.jpg` | Ventures page, grouped by type |
| `v2-zerohuman-desktop.jpg` | ZeroHuman file, order diagram in view |
| `v2-domain-desk-desktop.jpg` | The warm Domain Desk section |
| `v2-founder-desktop.jpg` | Founder page |

## Production repositories inspected, not modified

| Source | How it was used |
|---|---|
| `kenashe/luckydomains` (public) | Read-only clone at commit `8b48343`. Documentation read in full. Logo, favicon, and portrait files copied. |
| https://luckydomains.io/ | Read for current copy, services, founder and news content. One screenshot captured. |
| https://kenashe.ai/ and its build pages | Read for venture facts, statuses, and founder background. |
| `kenashe/nbcg-design-concepts` (public) | Read as a structural reference only. No visual design reused. |

No commit, branch, pull request, issue, setting, DNS record, or deployment was created or changed in any of them.
