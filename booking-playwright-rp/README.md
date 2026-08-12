# Booking.com Playwright + ReportPortal demo

Automates the 9 test cases from TMS folder 90 ("Search & Filters", see
[`../test-cases/search-and-filters.md`](../test-cases/search-and-filters.md)) against the live
[booking.com](https://www.booking.com) website, and reports the results to ReportPortal via
[`@reportportal/agent-js-playwright`](https://github.com/reportportal/agent-js-playwright).

**The goal of this project is to showcase ReportPortal's reporting capabilities** — Test Case ID
linking, rich attributes and descriptions, custom statuses, and failure attachments (screenshots,
video, trace) — not to be a precise, flake-free regression suite. A few tests intentionally fail.

## Setup

```bash
npm install
npx playwright install chromium
```

Create and fill in the `.env` based on `.env.example`:

```env
RP_API_KEY=...
RP_ENDPOINT=https://tms.beta.reportportal.io/api/v1
RP_PROJECT=
RP_LAUNCH="Release regression - Search & Filters (booking.com)"
```

## Run

```bash
npm test          # headless, reports to ReportPortal + local HTML report
npm run test:headed   # watch the browser while it runs
```

## What each test demonstrates

The 9 tests are grouped into 3 nested `test.describe` suites inside
[`tests/search-and-filters.spec.ts`](tests/search-and-filters.spec.ts), so ReportPortal shows a
3-level suite tree ("Search & Filters" → group → test).

### Destination Search — building and submitting a search

| Test | TMS ID | Expected result | ReportPortal status |
|------|--------|------------------|----------------------|
| Search hotels by destination city | TMS-BOOK-001 | Pass | PASSED |
| Search with valid check-in/check-out dates | TMS-BOOK-005 | Pass | PASSED |
| Search with empty destination field | TMS-BOOK-008 | Real site doesn't block the same way the TMS case expects | **FAILED (intentional)** |
| Search with check-out date before check-in date | TMS-BOOK-007 | Calendar UI prevents the invalid selection instead of showing an inline error | **FAILED (intentional)** |

### Results Filtering — narrowing an already-loaded results page

| Test | TMS ID | Expected result | ReportPortal status |
|------|--------|------------------|----------------------|
| Filter search results by star rating | TMS-BOOK-002 | Pass | PASSED |
| Filter search results by nightly price range | TMS-BOOK-003 | Booking.com's own filter buckets/currency don't match the exact bound | **FAILED (intentional)** |
| Show only properties with free cancellation | TMS-BOOK-006 | Pass | PASSED |

### Results Interaction — acting on an already-loaded results page

| Test | TMS ID | Expected result | ReportPortal status |
|------|--------|------------------|----------------------|
| Sort hotel results by lowest price | TMS-BOOK-004 | Pass | PASSED |
| Open hotel details from search results | TMS-BOOK-009 | Pass | PASSED |

Each test sets:

- `ReportingApi.setTestCaseId(...)` — the original `TMS-BOOK-xxx` demo ID, so ReportPortal groups
  reruns of the same test case together regardless of code changes.
- `ReportingApi.addAttributes([...])` — structured (`priority`, `area`, `type`, `browser`) and
  tag-style (`search`, `smoke`, `filters`, ...) attributes copied from the TMS test case.
- `ReportingApi.setDescription(...)` — preconditions, steps and expected result from the TMS test
  case, rendered as ReportPortal markdown.

## Notes

- `pages/BookingHomePage.ts` and `pages/SearchResultsPage.ts` centralize the booking.com locators.
  Because this automates a live third-party site, the UI can change over time (layout, A/B tests,
  cookie/sign-in prompts) — if a selector breaks, it only needs to be fixed in one place.
- Everything runs through Playwright's own Chromium browser.
