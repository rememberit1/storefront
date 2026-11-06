# Local-business storefront preview toolkit

## Overview

Build-and-host toolkit for **one-off marketing preview sites** for local service businesses (plumbing, HVAC, roofing, etc.). Each preview is a single HTML page that looks like a simple business website, clearly labeled as a concept preview.

## Purpose

Support outreach that shows a business what a basic site for them could look like. Previews are noindex, temporary, and served from a shared host so you do not burn a Cloudflare Pages project per prospect.

## Features

- `build.py` — generate a styled single-page storefront from structured business data (name, category, reviews, hours, phone, address)
- Color palettes by trade (Plumbing / HVAC / Roofing)
- Sticky mobile call bar, Google-style star rating, review cards, contact block
- Shared Worker host pattern (documented in `README-previews.md`): many slugs under one Worker on a custom preview domain
- `shared/build_worker.py` + `registry.json` — inline registered pages into one Worker deploy
- Assorted `deploy_*.js` / `check*.py` helpers from earlier batch runs

Prospect lead CSVs, scraped places dumps, and outreach drafts are **not** included in this public repo.

## Tech stack

- Python HTML generators
- Cloudflare Worker (shared multi-slug host) and/or legacy per-site Pages deploys
- Static HTML/CSS only on the generated pages

## Run / deploy

```bash
# Generate a page (see build.py for the expected listing dict shape)
python3 build.py

# Shared Worker path (when using shared/)
# 1. Put HTML under sites/<folder>/index.html
# 2. Register the slug in shared/registry.json
# 3. python3 shared/build_worker.py
# 4. Deploy the resulting Worker code through Cloudflare
```

Every preview should keep `<meta name="robots" content="noindex, nofollow">` and a footer stating it is a preview concept, not affiliated with the named business.

## Notes

Do not commit API tokens, customer emails, or call sheets.
