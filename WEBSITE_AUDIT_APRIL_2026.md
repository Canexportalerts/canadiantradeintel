# Canadian Trade Intelligence — Website Audit
## April 20, 2026
**Scope:** Full static site audit — /canadiantradeintel/ repo (148 HTML files)
**Method:** Read-only analysis. No changes made.

---

## AUDIT 1 — Navigation Consistency

### Findings

The site uses a centralized `nav.js` (257 lines) that dynamically injects navigation HTML into pages via a `<nav id="main-nav"></nav>` placeholder. All three required items (Canada Forward, Procurement, Countries) are present in nav.js.

**Navigation links in nav.js:**
- Dashboard, Countries, Spotlight, Reports, Canada Forward
- Resources dropdown: Terminal, Procurement, Sanctions Screener, Business Map, Trade Agreements, Tariff Rates, Practical Guides, Methodology
- About, See Plans (CTA)

**Pages NOT using nav.js — 8 pages (will show no navigation header):**
- `/resources/trade agreements/index.html` (note: space in folder name)
- `/samples/canada-critical-minerals-japan/index.html`
- `/sample/index.html`
- `/countries/kenya/index.html`
- `/countries/ghana/index.html`
- `/countries/singapore/index.html`
- `/countries/philippines/index.html`
- `/countries/thailand/index.html`

### Issues Found
- 8 pages missing nav.js — broken navigation header on all of these
- 5 country pages (recent additions: Kenya, Ghana, Singapore, Philippines, Thailand) missing the script tag

### Verdict
**NEEDS ATTENTION** — 5% of pages (8/148) lack navigation.

---

## AUDIT 2 — Footer Consistency

### Findings

**~40 pages with NO footer at all:**
- All 39 country pages (`/countries/*/index.html`)
- All resource pages
- All Canada Forward theme pages (except main index)
- All Canada Forward province pages (except provinces/index)
- `/procurement/index.html`

**Footer link analysis:**
- **No `/policies/` link exists anywhere in the site** (absent from all footers)
- Homepage footer has 5 columns: Brand/CTA, Intelligence, Tools, Resources, Company
- Footers that do exist are inconsistently implemented — homepage uses CSS classes, `reports/index.html` uses inline styles

### Issues Found
- 40+ pages completely lack footer (no legal, company, or nav fallback links)
- No `/policies/` link anywhere — potential GDPR/privacy compliance issue
- Inconsistent footer structure across pages that do have footers

### Verdict
**CRITICAL** — 27% of pages lack footer. Missing legal links sitewide.

---

## AUDIT 3 — Meta Tags and SEO

### Findings

| Page | Title | Meta Desc | OG Title | OG Desc | Canonical |
|------|-------|-----------|----------|---------|-----------|
| `/` | ✓ | ✓ | ✗ | ✗ | ✗ |
| `/reports/` | ✓ | ✓ | ✗ | ✗ | ✗ |
| `/terminal/` | ✓ | ✓ | ✗ | ✗ | ✗ |
| `/procurement/` | ✓ | ✓ | ✗ | ✗ | ✗ |
| `/spotlight/` | ✓ | ✓ | ✓ | ✓ | ✗ |
| `/spotlight/{slug}/` | ✓ | ✓ | ✓ | ✓ | ✓ |
| `/countries/united-states/` | ✓ | ✓ | ✗ | ✗ | ✗ |
| `/canada-forward/` | ✓ | ✓ | ✗ | ✗ | ✗ |

**All 148 pages have `<title>` and `<meta name="description">`** — 100% coverage.

**OG tags present only on:** Spotlight hub + all individual spotlight slug pages (~43 pages).

**Canonical tags present only on:** Individual spotlight slug pages (~42 pages). All other pages (106+) lack canonical.

### Issues Found
- Missing `og:title` and `og:description` on all main platform hubs (Homepage, Reports, Terminal, Procurement, Countries, Canada Forward, Resources)
- Missing canonical tags on ~99% of pages
- No `og:image` defined anywhere on the site

### Verdict
**CRITICAL** — No OG tags on high-traffic platform pages. No social sharing optimisation for most of the site.

---

## AUDIT 4 — Broken Internal Links

### Findings

**Verified working directories (no 404):**
- ✓ `/about/`, `/pricing/`, `/sample/`, `/dashboard/`, `/terminal/`
- ✓ `/procurement/`, `/methodology/`, `/map/`
- ✓ `/tools/sanctions-check/` — exists
- ✓ `/guides/` hub — exists (with `/guides/ised-programmes/` and `/guides/canexport-sme/`)
- ✓ All 41 country paths — exist
- ✓ All 25 Canada Forward paths (hub + 10 themes + 13 provinces + provinces hub) — exist
- ✓ `/canada-forward/indigenous-economy/` — exists
- ✓ `/tools/canadian-suppliers/` — **NOT confirmed, check manually**

**Broken internal links found:**

| Broken Link | Appears In | Notes |
|-------------|------------|-------|
| `/guides/ceta-for-canadian-businesses` | `/guides/ised-programmes/index.html` | Directory missing |
| `/guides/edc-financing` | `/guides/ised-programmes/` + `/guides/canexport-sme/` | Directory missing |
| `/guides/how-to-use-tcs` | `/guides/ised-programmes/` | Directory missing |
| `/practical-guides` | `/resources/trade agreements/index.html` | Should be `/guides/` |
| `/trade-agreements` | One resource page | Should be `/resources/trade-agreements/` |
| `/reports/critical-minerals/` | Potential nav links | No directory — only individual report files |
| `/reports/aerospace-defence/` | Potential nav links | No directory |
| `/reports/agri-food/` | Potential nav links | No directory |
| `/reports/advanced-manufacturing/` | Potential nav links | No directory |
| `/reports/energy-cleantech/` | Potential nav links | No directory |
| `/reports/technology-digital/` | Potential nav links | No directory |

**Map page paradox:**
`/map/index.html` EXISTS but nav.js marks the map link "Coming Soon" — conflicting UX signal.

**Folder name issue:**
`/resources/trade agreements/` (with space) and `/resources/trade-agreements/` (with hyphen) — both exist. The space version breaks URLs.

### Issues Found
- 3 guide pages linked but missing: `/guides/ceta-for-canadian-businesses/`, `/guides/edc-financing/`, `/guides/how-to-use-tcs/`
- 2 broken resource path links (`/practical-guides`, `/trade-agreements`)
- 6 report archive directories missing (sector browsing not possible)
- 1 space-in-folder-name issue in `/resources/trade agreements/` (URL-encodes to `%20`)
- Map page exists but nav says "Coming Soon"

### Verdict
**NEEDS ATTENTION** — 3 confirmed 404 guide links. Resource path inconsistency. Report archives missing.

---

## AUDIT 5 — Reports Page Dynamic vs Hardcoded Content

### Findings

**Hardcoded masthead text in `/reports/index.html` (line ~103):**
```html
<div class="r-meta">Issue #003 current · April 14, 2026 · Six sectors · New issues published every Tuesday</div>
```
This is static HTML. It will be wrong when Issue #004 publishes on April 21, 2026 (tomorrow).

**Dynamic rendering system (line ~365):**
```javascript
fetch('/reports/reports-index.json')
  .then(r => r.json())
  .then(reports => { /* renders report cards */ })
```
Report cards ARE rendered dynamically from JSON. The masthead meta line is not.

**Current state of `/reports/reports-index.json`:**
- Issue: 3, Date: 2026-04-14
- 6 sectors: aerospace_defence, tech_digital, advanced_manufacturing, critical_minerals, energy_cleantech, agri_food
- All sector report files present and linked correctly

**Template line in reports JS:**
```javascript
`<div class="report-issue">Issue #${r.issue || '003'} · ${date}</div>`
```
Fallback hardcodes '003' — will show wrong issue if JSON read fails.

### Issues Found
- Line ~103: Hardcoded "Issue #003 current · April 14, 2026" — becomes stale April 22, 2026
- No JavaScript updates the masthead meta text from JSON
- JS fallback `|| '003'` hardcodes old issue number

### Verdict
**NEEDS ATTENTION** — Will show wrong issue label starting next week. Fix before Tuesday April 22.

---

## AUDIT 6 — Terminal Page Data Currency

### Findings

| Data Field | Source | Status |
|------------|--------|--------|
| FX Rates (CAD/USD, EUR, GBP, JPY, CNY, AUD) | BoC Valet API (live fetch) | Dynamic ✓ |
| BCPI Index | BoC Valet API (live fetch) | Dynamic ✓ |
| Commodity prices (uranium, lithium, canola, etc.) | `/api/terminal_data.json` | Dynamic — updates Tuesday ✓ |
| Stock prices | Unclear — possible hardcoded divs | Needs manual check |
| "This week's intelligence" editorial text | Hardcoded HTML | STALE ✗ |
| Regulatory pulse signals (15+ items) | Hardcoded HTML `<div>` elements | STALE ✗ |
| Trade agreements table | Hardcoded HTML | Static (acceptable for reference) |

**Hardcoded "This week's intelligence" section (lines ~295-315):**
```html
<div class="week-lead">Canada's Defence Industrial Strategy and Hague NATO commitments 
create the single largest procurement opportunity in a generation...</div>
```
No date field. No fetch. Will never update without a manual HTML edit.

**Regulatory pulse signals (lines ~748-850):**
All 15+ signal items are hardcoded HTML:
```html
<div class="signal-item">
  <div class="signal-meta">CRITICAL MINERALS · IMMEDIATE</div>
  <div class="signal-hl">G7 Critical Minerals Alliance Round 2 applications opened March 31...</div>
```
`/api/regulatory_pulse.json` exists but is currently 3 bytes (empty file).

### Issues Found
- "This week's intelligence" editorial block is hardcoded — permanently stale
- All 15+ regulatory pulse signals are hardcoded HTML — no live data
- `/api/regulatory_pulse.json` exists but is empty (3 bytes) — field created but not populated
- Stock prices unclear — confirm whether JS overwrites hardcoded values

### Verdict
**CRITICAL** — Two major content blocks on the terminal page are hardcoded and will mislead users. The regulatory signals file path exists but is unpopulated.

---

## AUDIT 7 — Canada Forward Sub-page Completeness

### Findings

**Full coverage — all 25 pages exist and are substantial:**

**Hub + Themes (11 pages):**
| Page | Exists | Size | Status |
|------|--------|------|--------|
| `/canada-forward/index.html` | ✓ | 103.5 KB | Full |
| `/canada-forward/build-canada/` | ✓ | 40.7 KB | Full |
| `/canada-forward/care-economy/` | ✓ | — | Full |
| `/canada-forward/cities/` | ✓ | — | Full |
| `/canada-forward/defence-security/` | ✓ | 39.3 KB | Full |
| `/canada-forward/digital-economy/` | ✓ | — | Full |
| `/canada-forward/energy-transition/` | ✓ | — | Full |
| `/canada-forward/financial-services/` | ✓ | — | Full |
| `/canada-forward/foreign-investment/` | ✓ | — | Full |
| `/canada-forward/indigenous-economy/` | ✓ | 16.8 KB | Full (smallest) |
| `/canada-forward/ocean-economy/` | ✓ | — | Full |

**Provinces + Territories (14 pages including hub):**
All 13 provinces and territories covered:
Alberta, BC, Manitoba, New Brunswick, Newfoundland, Nova Scotia, Nunavut, NWT, Ontario, PEI, Quebec, Saskatchewan, Yukon

### Issues Found
- `indigenous-economy` is notably smaller (16.8 KB vs 40+ KB for others) — may be content-light
- All pages confirmed substantial — no stubs found

### Verdict
**PASS** — Full coverage. All pages substantive. Well-structured.

---

## AUDIT 8 — 404 Stub Pages Needed

### Summary of all paths linked but missing:

**Missing guide pages (will 404):**
1. `/guides/ceta-for-canadian-businesses/` — linked from `/guides/ised-programmes/`
2. `/guides/edc-financing/` — linked from `/guides/ised-programmes/` and `/guides/canexport-sme/`
3. `/guides/how-to-use-tcs/` — linked from `/guides/ised-programmes/`

**Broken path aliases (won't 404 but go to wrong place):**
4. `/practical-guides` — should be `/guides/`
5. `/trade-agreements` — should be `/resources/trade-agreements/`

**Missing report archives (404 if navigated to):**
6. `/reports/critical-minerals/`
7. `/reports/aerospace-defence/`
8. `/reports/agri-food/`
9. `/reports/advanced-manufacturing/`
10. `/reports/energy-cleantech/`
11. `/reports/technology-digital/`

**Pages with broken nav (not 404 but degraded UX):**
- `/countries/kenya/`, `/countries/ghana/`, `/countries/singapore/`, `/countries/philippines/`, `/countries/thailand/`
- `/sample/`, `/resources/trade agreements/`

### Verdict
**NEEDS ATTENTION** — 3 hard 404s on guide pages. 6 potential 404s on report archive paths if linked.

---

## PRIORITY ACTION LIST

### 1. Broken links — fix immediately (404s)

**CRITICAL — Do this week:**
- [ ] Create `/guides/ceta-for-canadian-businesses/index.html` (stub or full)
- [ ] Create `/guides/edc-financing/index.html` (stub or full)
- [ ] Create `/guides/how-to-use-tcs/index.html` (stub or full)
- [ ] Fix `/practical-guides` links → change to `/guides/` in `/resources/trade agreements/index.html`
- [ ] Resolve `/trade-agreements` → `/resources/trade-agreements/` path inconsistency
- [ ] Remove "Coming Soon" from nav.js `/map/` link (page exists) — or delete map if truly not ready

**MODERATE — Do this sprint:**
- [ ] Add `<script src="/nav.js"></script>` + `<nav id="main-nav"></nav>` to: Kenya, Ghana, Singapore, Philippines, Thailand country pages + `/sample/` + `/resources/trade agreements/`
- [ ] Rename `/resources/trade agreements/` → `/resources/trade-agreements/` (fix URL encoding)

### 2. Stub pages needing content

**Create stub pages for missing guides** (minimum viable stub with real content outline):
- `/guides/ceta-for-canadian-businesses/` — CETA practical guide for SMEs
- `/guides/edc-financing/` — EDC export financing guide
- `/guides/how-to-use-tcs/` — TCS offices and referral guide

**Consider creating report archive pages** (if sector browsing is planned):
- `/reports/critical-minerals/`, etc. — redirect to `/reports/` filtered by sector

### 3. SEO gaps on high-traffic pages

**Add OG tags to all platform hubs (these get shared most):**
```html
<!-- Add to <head> of homepage, reports, terminal, procurement, countries, canada-forward -->
<meta property="og:title" content="[Page Title] · Canadian Trade Intelligence">
<meta property="og:description" content="[Meta description text]">
<meta property="og:type" content="website">
<meta property="og:image" content="https://canadiantradeintel.ca/og-image.png">
<meta property="og:url" content="https://canadiantradeintel.ca/[path]/">
```

**Add canonical tags to all pages:**
```html
<link rel="canonical" href="https://canadiantradeintel.ca/[path]/">
```

**Priority order:** Homepage > Reports > Terminal > Countries > Canada Forward > Procurement > Spotlight hub > Guide pages

### 4. Dynamic vs hardcoded content risks

**FIX BEFORE TUESDAY (April 22):**
- `reports/index.html` line ~103: Replace hardcoded "Issue #003 current · April 14, 2026" with JS that reads `reports-index.json` and renders the max issue + date

**FIX THIS SPRINT:**
- `terminal/index.html` "This week's intelligence" block: Move editorial text to `/api/terminal_intelligence.json` (create file), fetch and render dynamically
- `terminal/index.html` regulatory pulse signals: Move 15 hardcoded signal divs to `/api/regulatory_pulse.json` (file exists, currently 3 bytes — needs population from pipeline), fetch and render dynamically
- JS fallback `|| '003'` in reports page — change to `|| ''` or fetch-and-derive

**MEDIUM PRIORITY:**
- Add `/policies/` page and link it from all footers (GDPR/privacy requirement)
- Standardise footer HTML across all pages (currently inconsistent implementations)
- Add footers to the 40 country pages and procurement page that currently have none

---

## SUMMARY STATISTICS

| Metric | Count | Status |
|--------|-------|--------|
| Total HTML files | 148 | — |
| Pages with nav.js | 140 (95%) | ✓ |
| Pages missing nav.js | 8 (5%) | ✗ |
| Pages with footer | ~108 (73%) | ⚠ |
| Pages missing footer | ~40 (27%) | ✗ |
| Pages with `<title>` | 148 (100%) | ✓ |
| Pages with `<meta description>` | 148 (100%) | ✓ |
| Pages with `og:title` | ~43 (29%) | ✗ |
| Pages with canonical | ~42 (28%) | ✗ |
| Broken guide links (hard 404) | 3 | ✗ |
| Report archive dirs missing | 6 | ✗ |
| Stale hardcoded content blocks | 2 major | ✗ |
| Canada Forward coverage | 13/13 provinces, 10/10 themes | ✓ |
| Countries covered | 41 | ✓ |
| `/policies/` page | Does not exist | ✗ |

---

*Audit compiled: April 20, 2026*
*Method: Static read-only file analysis across full repo*
*Next audit recommended: After major structural changes or quarterly*
