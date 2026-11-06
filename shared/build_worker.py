#!/usr/bin/env python3
"""Build the deploy code for the shared 'storefront-previews' Worker from registry.json.
Output: deploy_code.js (an async arrow fn for the Cloudflare MCP 'execute' tool)."""
import json, os
here = os.path.dirname(os.path.abspath(__file__))
reg = json.load(open(os.path.join(here, "registry.json")))
pages = {}
for slug, e in reg.items():
    pages[slug] = open(os.path.join(here, "..", "sites", e["site"], "index.html"), encoding="utf-8").read()
worker = """const PAGES = %s;
const H = {'x-robots-tag': 'noindex, nofollow'};
export default { async fetch(request) {
  if (request.method !== 'GET' && request.method !== 'HEAD') return new Response('Method not allowed', { status: 405, headers: H });
  const url = new URL(request.url); const p = url.pathname;
  if (p === '/robots.txt') return new Response('User-agent: *\\nDisallow: /\\n', { headers: { ...H, 'content-type': 'text/plain' } });
  const m = p.match(/^\\/([a-z0-9-]+)\\/?(index\\.html)?$/);
  if (m && PAGES[m[1]]) {
    if (!p.endsWith('/') && !m[2]) return Response.redirect(url.origin + '/' + m[1] + '/', 301);
    return new Response(PAGES[m[1]], { headers: { ...H, 'content-type': 'text/html; charset=utf-8', 'cache-control': 'public, max-age=300' } });
  }
  return new Response('<!doctype html><meta name="robots" content="noindex, nofollow"><title>Not found</title><p>This preview is no longer available.</p>', { status: 404, headers: { ...H, 'content-type': 'text/html; charset=utf-8' } });
} };""" % json.dumps(pages)
code = """async () => {
  const name = 'storefront-previews';
  const worker = %s;
  const meta = { main_module: 'worker.js', compatibility_date: '2026-10-01' };
  const b = 'SFP' + Date.now();
  const body = [`--${b}`, 'Content-Disposition: form-data; name="metadata"', 'Content-Type: application/json', '', JSON.stringify(meta),
    `--${b}`, 'Content-Disposition: form-data; name="worker.js"; filename="worker.js"', 'Content-Type: application/javascript+module', '', worker, `--${b}--`, ''].join('\\r\\n');
  const r = await cloudflare.request({ method: 'PUT', path: `/accounts/${accountId}/workers/scripts/${name}`, body, contentType: `multipart/form-data; boundary=${b}`, rawBody: true });
  const s = await cloudflare.request({ method: 'POST', path: `/accounts/${accountId}/workers/scripts/${name}/subdomain`, body: { enabled: true, previews_enabled: false } });
  const sub = await cloudflare.request({ method: 'GET', path: `/accounts/${accountId}/workers/subdomain` });
  return { upload: r.success, errors: r.errors, subdomainEnabled: s.success, subErrors: s.errors, accountSubdomain: sub.result?.subdomain, slugs: %s };
}""" % (json.dumps(worker), json.dumps(list(pages)))
open(os.path.join(here, "deploy_code.js"), "w").write(code)
print("ok", list(pages), len(code))
