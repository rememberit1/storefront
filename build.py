import json,html,re,os
E=html.escape
def slugify(s):
    s=re.sub(r"[’']",'',s.lower()); s=re.sub(r'[^a-z0-9]+','-',s).strip('-')
    return s[:40].strip('-')
DAYS=['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
CSS="""*{box-sizing:border-box}body{margin:0;font:17px/1.6 system-ui,-apple-system,Segoe UI,Roboto,sans-serif;color:#1d2733;background:#f6f8fb}
.wrap{max-width:880px;margin:0 auto;padding:0 18px}
.hero{background:linear-gradient(135deg,%(c1)s,%(c2)s);color:#fff;padding:56px 0 48px}
.hero .cat{text-transform:uppercase;letter-spacing:.08em;font-size:13px;opacity:.85;margin:0}
.hero h1{font-size:clamp(1.9rem,6vw,2.8rem);line-height:1.15;margin:.25em 0 .35em}
.stars{font-size:1.1rem;margin:0 0 22px}.stars b{color:#ffd54a}
.btn{display:inline-block;background:#fff;color:%(c2)s;font-weight:700;text-decoration:none;padding:14px 26px;border-radius:10px;font-size:1.1rem;margin:4px 8px 4px 0}
.btn.alt{background:transparent;color:#fff;border:2px solid #fff}
section{padding:36px 0}h2{font-size:1.45rem;margin:0 0 16px}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:14px}
.card{background:#fff;border-radius:12px;padding:18px 20px;box-shadow:0 1px 3px rgba(0,0,0,.08)}
.card p{margin:0 0 10px}.who{font-weight:600;color:#5a6675;font-size:15px}.who span{color:#e0a800}
.info{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:14px}
table{border-collapse:collapse;width:100%%}td{padding:4px 0;vertical-align:top}td:first-child{font-weight:600;padding-right:14px;white-space:nowrap}
footer{background:#1d2733;color:#b9c3cf;text-align:center;padding:22px 0;font-size:14px}
.callbar{position:fixed;left:0;right:0;bottom:0;background:%(c2)s;text-align:center;padding:10px;display:none}
.callbar a{color:#fff;font-weight:700;text-decoration:none;font-size:1.1rem}
@media(max-width:640px){.callbar{display:block}body{padding-bottom:56px}}"""
PAL={'Plumbing':('#0b6bcb','#08396b'),'Roofing':('#b4441c','#5e1f0a'),'HVAC':('#0f8a7a','#08453d')}
def hours_rows(oh):
    if not oh: return ''
    rows=''.join(f"<tr><td>{E(d['day'])}</td><td>{E(d['hours'])}</td></tr>" for d in oh)
    return f'<div class="card"><h2 style="font-size:1.15rem">Hours</h2><table>{rows}</table></div>'
def build(L):
    c1,c2=PAL[L['bucket']]
    name=E(L['title']); phone=L.get('phone'); tel=re.sub(r'[^0-9+]','',L.get('phoneUnformatted') or phone or '')
    stars=f"<b>★ {L['totalScore']:.1f}</b> on Google · {L['reviewsCount']} reviews"
    btns=(f'<a class="btn" href="tel:{tel}">Call {E(phone)}</a>' if phone else '')
    if L.get('address'):
        maps=L.get('url') or ''
        btns+=f'<a class="btn alt" href="{E(maps)}" rel="nofollow">Directions</a>' if maps else ''
    revs=''.join(f'<div class="card"><p>&ldquo;{E(r["text"])}&rdquo;</p><div class="who"><span>{"★"*int(r["stars"])}</span> {E(r["name"])}</div></div>' for r in L['reviews'])
    contact='<div class="card"><h2 style="font-size:1.15rem">Contact</h2><table>'
    if phone: contact+=f'<tr><td>Phone</td><td><a href="tel:{tel}">{E(phone)}</a></td></tr>'
    if L.get('address'): contact+=f'<tr><td>Address</td><td>{E(L["address"])}</td></tr>'
    if L.get('email'): contact+=f'<tr><td>Email</td><td><a href="mailto:{E(L["email"])}">{E(L["email"])}</a></td></tr>'
    contact+=f'<tr><td>Service</td><td>{E(L["categoryName"])}</td></tr></table></div>'
    loc=E(', '.join(x for x in [L.get('city'),L.get('stateAbbr')] if x))
    desc=f"{L['title']}: {L['categoryName']}{' in '+loc if loc else ''}. Rated {L['totalScore']:.1f} on Google from {L['reviewsCount']} reviews."
    page=f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex, nofollow"><title>{name}{' | '+E(L['categoryName'])}</title><meta name="description" content="{E(desc)}">
<style>{CSS%{'c1':c1,'c2':c2}}</style></head><body>
<header class="hero"><div class="wrap"><p class="cat">{E(L['categoryName'])}{' · '+loc if loc else ''}</p><h1>{name}</h1><p class="stars">{stars}</p>{btns}</div></header>
<main>
<section><div class="wrap"><h2>What customers say on Google</h2><div class="cards">{revs}</div></div></section>
<section style="padding-top:0"><div class="wrap info">{contact}{hours_rows(L.get('openingHours'))}</div></section>
</main>
<footer><div class="wrap">Preview concept, not affiliated with {name}.</div></footer>
{f'<div class="callbar"><a href="tel:{tel}">Call {E(phone)}</a></div>' if phone else ''}
</body></html>"""
    return page
if __name__=='__main__':
    leads=json.load(open('/workspace/storefront/leads.json'))
    for L in leads:
        d=f"/workspace/storefront/sites/{L['project']}"; os.makedirs(d,exist_ok=True)
        open(d+'/index.html','w').write(build(L))
    print('built',len(leads))
