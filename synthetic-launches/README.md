# Synthetic launches — Stream A / Stream B

Postman collections and a Python uploader that seed ReportPortal with realistic
automation results for the Booking Flow Demo TMS cases (folders 93+95 and 92+94).

Folder Search & Filters is already covered by the live Playwright suite in
[`../booking-playwright-rp`](../e2e-playwright-tests/) and is not included here.

## What gets uploaded

| Stream | Collection | TMS folders | Cases | Launch name |
|--------|------------|-------------|-------|-------------|
| A | `stream-a-cancellations-mobile.postman_collection.json` | Cancellations, Mobile | 12 | Nightly regression - Cancellations & Mobile |
| B | `stream-b-booking-nfr.postman_collection.json` | Booking Flow, Non-functional | 15 | Nightly regression - Booking Flow & NFR |

Each STEP item has `testCaseId` (`TMS-BOOK-xxx` / `TMS-MOB-xxx`), attributes from the
TMS case, nested steps for `Type: STEPS` cases, and mixed PASSED/FAILED outcomes
(~30% fail) with Product Bug / Automation Bug / System Issue / To Investigate.

Stream A logs look like WebdriverIO / Appium. Stream B logs look like Playwright.

`catalog.py` is the source of truth. Collections are generated from it — do not edit the JSON by hand.

## Setup

```bash
python3 -m pip install -r requirements.txt
cp .env.example .env
```

Fill `RP_URL`, `RP_PROJECT`, and `RP_API_KEY` in `.env`. The uploader also falls back
to [`../../Demo launch/.env`](../../Demo%20launch/.env) if that file exists.

## Run

Regenerate collections after editing `catalog.py`:

```bash
python3 rp_stream_upload.py --generate
```

Upload one stream:

```bash
python3 rp_stream_upload.py stream-a-cancellations-mobile.postman_collection.json
python3 rp_stream_upload.py stream-b-booking-nfr.postman_collection.json
```

Generate both collections and upload them:

```bash
python3 rp_stream_upload.py --all
python3 rp_stream_upload.py --all --reset
```

`--reset` deletes existing launches with the same name before upload.
