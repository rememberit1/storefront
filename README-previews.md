# Shared preview host: `storefront-previews` (Cloudflare Worker)

The account hit the 21-project Pages limit (error 8000027), so new previews no longer get their own Pages project.
They are all served by one **Cloudflare Worker** (not Pages, so it uses no Pages slot), on Ben's branded custom domain:

    https://previews.getbusinesswinnow.com/<slug>/      <- use this in emails
    https://storefront-previews.businesswinnow.workers.dev/<slug>/   (backup URL, same content)

The custom domain is a Workers Custom Domain on zone getbusinesswinnow.com. Cloudflare manages its proxied AAAA record for `previews`. Never edit the apex, MX, SPF, DKIM (zoho._domainkey), DMARC or zoho-verification records, and never turn on Email Routing (Zoho handles mail).

- Old `storefront-*.pages.dev` projects stay as they are (links already emailed). Never touch `silverspring-plumbing-pros` or `vista-previews`.
- Every response has `X-Robots-Tag: noindex, nofollow`; `/robots.txt` is `Disallow: /`; each page has `<meta name="robots" content="noindex, nofollow">`.
- Unknown or removed slugs return 404 "This preview is no longer available."; `/<slug>` redirects to `/<slug>/`.

## Files (`/workspace/storefront/shared/`)
- `registry.json`: the list of live previews: `slug -> {site, added, takedown}`. `site` is the folder under `/workspace/storefront/sites/<site>/index.html`.
- `build_worker.py`: inlines every registry page into one Worker and writes `deploy_code.js`.
- `deploy_code.js`: the code to run with the Cloudflare MCP `execute` tool. Pass it as `"code": "$file:/workspace/storefront/shared/deploy_code.js"`. It PUTs the whole Worker each time, so the deploy always matches `registry.json` exactly.

## Add a preview
1. Build the page into `sites/storefront-<slug>/index.html`. Keep the footer "Preview concept, not affiliated with <Business>." and the robots meta tag.
2. Add `"<slug>": {"site": "storefront-<slug>", "url": "https://previews.getbusinesswinnow.com/<slug>/", "added": "YYYY-MM-DD", "takedown": "<added + 14 days>"}` to `registry.json`. Slugs must be lowercase a-z, 0-9 and `-`.
3. `python3 shared/build_worker.py`, then run `deploy_code.js` through Cloudflare `execute`.
4. Check it: `curl -sI https://previews.getbusinesswinnow.com/<slug>/` should return 200 with x-robots-tag, and the body should contain the footer.
5. Put the URL in the draft and in `leads-log.csv` (`preview_url` = the previews.getbusinesswinnow.com URL; `pages_project` = `storefront-previews (shared Worker)`; `takedown_due`).

## Remove one preview (14-day takedown of a single path)
1. Each run, find registry entries whose `takedown` date has passed and whose lead has not claimed the site (check `leads-log.csv` email_status and replies).
2. Delete that slug from `registry.json`. Keep the `sites/` folder for the record.
3. Rebuild and redeploy (step 3 above). Only that path disappears; the other slugs are unaffected.
4. Confirm `curl -s -o /dev/null -w '%{http_code}' .../<slug>/` returns 404, then set the lead's status in `leads-log.csv` to `preview taken down YYYY-MM-DD`.
5. If someone claims a preview, leave it in the registry (or move it to its own project/domain) and clear its takedown date.

## Limits
- One Worker script can be up to 3 MB compressed on the free plan. Each preview is about 6-10 KB, so a few hundred fit. Prune expired slugs anyway.
- Free plan: 100k requests a day across the account.
