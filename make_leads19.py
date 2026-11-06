import json,re
from build import slugify
det={x['placeId']:x for x in json.load(open('details_2026-10-19.json'))}
cb={x['placeId']:x for x in json.load(open('cands_2026-10-19b.json'))}
ca={x['placeId']:x for x in json.load(open('cands_2026-10-19.json'))}
SPEC=[ # placeId, slug, email, email_source, confidence, site_status, listed_website, reason
("ChIJ7yNPn7ZVtokR2HsqGX5Q04M","ca-plumbing-drain","info@caplumbingdrain.com","https://www.caplumbingdrain.com/contact-us/ (search-index copy of their own site) ; https://www.sewerlinerepairlist.com/contractors/va/ca-plumbing-drain-llc","medium-high: on business's own site (same phone 703-420-0087) + directory with same address; site now errors but domain MX (Outlook) is active","none on Google listing; their own domain caplumbingdrain.com returns a WordPress error (HTTP 500)","","but I couldn't find a working website for you"),
("ChIJt-wOkJxLtokRoup8WG6zlt8","all-things-plumbing-gas","Shawn@AllThingsPlumbingAndGas.com","https://nextdoor.com/pages/all-things-plumbing-gas-falls-church-va-1/ ; https://exa.ai/library/place/mcj89rksv5m","high: business's own Nextdoor page (same phone 703-581-4812, address 7524 Lisle Ave, owner Shawn); domain MX active. Alt: shawnj703@gmail.com on owner's Nextdoor profile","none on Google listing; their own domain allthingsplumbingandgas.com shows a WordPress error page","","but I couldn't find a working website for you"),
("ChIJb04_u91ctokROU1URuRy5rk","universal-heat-and-air","support@varepair.com","https://www.varepair.com/ and https://www.varepair.com/contact-us/ (search-index copies of their own site)","medium-high: on business's own site (VA Repair = Universal Heat & Air, same phone 703-580-8988); site currently down but domain MX (Google) active","broken: varepair.com returns HTTP 500 (PHP error)","https://www.varepair.com/","but the website on your Google listing isn't loading"),
("ChIJ2UZdRMpKtokRJFIDlNSJQYc","air-control","fkent.aircontrol@gmail.com","https://nextdoor.com/pages/air-control-llc-arlington-va/","high: business's own Nextdoor page (owner Fred, same phone 703-969-6320, lic. 2705124129); also on search-index copy of aircontrol-llc.com","broken: aircontrol-nova.com shows 'Account Suspended'; newer aircontrol-llc.com shows 'Site not found' (404)","http://www.aircontrol-nova.com/","but the website on your Google listing has been suspended"),
("ChIJ-cl33mX5tokRAdUXzh3FXKA","all-total-service-plumbing","alltotalplumbingservice@gmail.com","https://nextdoor.com/pages/a-total-service-plumbing-fort-belvoir-va/","medium-high: business's Nextdoor page (owner Scot Morgal, same phone 703-656-0559); DexKnows lists alltotalplumbing@aol.com (not used)","none (no website on Google listing)","","but I couldn't find a website for you"),
("ChIJi15BaYVVtokRSPNkugTMnpE","c-m-king","cmkingllc@comcast.net","https://exa.ai/library/place/mj4nvlyd10d","medium: one place aggregator with matching phone 703-296-7891 and address; their old domain cmkingllc.com no longer exists","none (no website on Google listing; old domain cmkingllc.com expired/NXDOMAIN)","","but I couldn't find a website for you"),
("ChIJeTc0LucTI4IRJ5UUOx8M93U","42-degrees-heating-and-cooling","info@42degreeshvac.com","https://www.freelistingusa.com/listings/42-degrees-heating-and-cooling ; https://www.fyple.com/company/42-degrees-heating-and-cooling-o27z46p/","medium-high: self-submitted listing (business-written description, logo, same phone/address); domain MX (Google) active. whatsyourhours lists degreesheatingandcooling@outlook.com (not used)","broken: 42degreeshvac.com shows 'Error. Page cannot be displayed' (confirmed via Apify fetch and box)","http://www.42degreeshvac.com/","but the website on your Google listing isn't loading"),
("ChIJEYvH_S_Bt4kRWQ1Xukclo4Y","rooter-master-services","","not found (checked Birdeye, gigopro, localitybiz, centralindex; none list an email)","n/a","none (no website on Google listing)","","but I couldn't find a website for you"),
("ChIJq-sRrBhPtokRX8_2UcFKy58","hvac-experts","","not found (directories show phone only; did not use LeadIQ's guessed name@domain pattern)","n/a","broken: callhvacexperts.com is a blank 'coming soon' (SeedProd) page","http://www.callhvacexperts.com/","but the website on your Google listing is just a blank placeholder page"),
("ChIJV0JElKE8pwcRQhSx_wiGdOI","pipefathers-plumbing","","not found usable (info@pipefathersplumbing.com is on search-index copy of their site, but the domain has no MX record, so it would bounce)","n/a","broken: pipefathersplumbing.com shows 'Error. Page cannot be displayed' (confirmed via Apify fetch and box)","http://pipefathersplumbing.com/","but the website on your Google listing isn't loading"),
("ChIJ8Z_vHHKa5SMREDx3Exz-dA8","all-american-hvac-sovereign-service","","not found (directories show phone/address only; allamericanhvacmd@gmail.com belongs to a different Urbana/Frederick company)","n/a","broken: aahvacservices.com redirects to a hosting 'account suspended' page","http://aahvacservices.com/","but the website on your Google listing has been suspended"),
("ChIJHQOe0g7sUiQR6zzY3RCBB34","affordable-hvac-services","","not found (Nextdoor business page and directories show phone only)","n/a","none (no website on Google listing)","","but I couldn't find a website for you"),
("ChIJo_aVUHrdt4kRExjpaEEqMrc","ca-plumbing","","not found (rejected candaplumbing18@gmail.com: belongs to an unrelated C and A Plumbing in Smiths Grove, KY)","n/a","none (no website on Google listing)","","but I couldn't find a website for you"),
("ChIJndTbL8y-t4kRa10P2jDKkhk","siwel-plumbing-heating-ac-service","","not found (BBB hides email; info@siwelinc.com belongs to a different Siwel company)","n/a","broken: siwelplumbinginc.com has an invalid TLS certificate and returns HTTP 500","https://siwelplumbinginc.com/","but the website on your Google listing isn't loading"),
]
def bucket(cat):
    c=cat.lower()
    return 'Roofing' if 'roof' in c else 'Plumbing' if 'plumb' in c else 'HVAC'
ST={'Virginia':'VA','Maryland':'MD','District of Columbia':'DC'}
def short_name(n):
    p=n.strip().split()
    if len(p)==1: return p[0][:1].upper()+p[0][1:]
    return p[0][:1].upper()+p[0][1:]+' '+p[-1][0].upper()+'.'
def trim(t,maxc=300):
    t=re.sub(r'\s+',' ',t).strip()
    if len(t)<=maxc: return t
    s=re.split(r'(?<=[.!?])\s+',t); out=''
    for x in s:
        if len(out)+len(x)+1>maxc: break
        out=(out+' '+x).strip()
    return out or t[:maxc].rsplit(' ',1)[0]+'…'
ROOTER_REVIEWS=[{"name":"Thomas N.","stars":5,"text":"Sam and Mario came quickly for an emergency and were professional speedy in fixing it. Highly recommend!"},
{"name":"Kenneth","stars":5,"text":"I had a water bubble appear in my ceiling. Called Rooter Masters and they had guys out to inspect issue, drain the bubble, and do a make shift patch on the ceiling within one hour. Both technicians were friendly and professional. I would use their services again."},
{"name":"Carl T.","stars":5,"text":"I had a draining problem in my kitchen sink. Called Rooter Master the next morning. Sam showed up was nice and very respectful. Gave me a estimate and started the work. Sam got my draining issue fixed and cleaned up after the work was done. I highly recommend this company for ur plumbing needs."}]
leads=[]
for pid,slug,email,src,conf,status,lw,reason in SPEC:
    x=det.get(pid) or cb.get(pid)
    base=ca.get(pid) or cb.get(pid) or {}
    L={k:x.get(k) for k in ['title','placeId','categoryName','totalScore','reviewsCount','phone','phoneUnformatted','address','city','state','url','openingHours']}
    if not L.get('phoneUnformatted') and L.get('phone'): L['phoneUnformatted']='+1'+re.sub(r'\D','',L['phone'])
    L['bucket']=bucket(L['categoryName']); L['stateAbbr']=ST.get(L.get('state') or '')
    if 'reviews' in x and x['reviews']:
        rv=[r for r in x['reviews'] if r.get('stars')==5 and r.get('text') and 60<=len(r['text']) and not re.search(r'llc|account|enterprises',r.get('name') or '',re.I) and 'cyst' not in r['text'] and r.get('name') not in ('Aimen Y','zgslvn')]
        rv.sort(key=lambda r: abs(len(r['text'])-220))
        L['reviews']=[{'name':short_name(r['name']),'stars':5,'text':trim(r['text'])} for r in rv[:4]]
    else:
        L['reviews']=ROOTER_REVIEWS
        L['reviews_source']='Google reviews as mirrored on https://reviews.birdeye.com/rooter-master-services-167479795820333 (Apify credit ran out before the Google scrape)'
    L['email']=email or None; L['email_source']=src; L['email_confidence']=conf
    L['site_status']=status; L['listed_website']=lw; L['reason']=reason
    L['project']='storefront-'+slug
    L['score']=round(L['totalScore']*L['reviewsCount'],1)
    leads.append(L)
leads.sort(key=lambda L:(0 if L['email'] else 1,-L['score']))
json.dump(leads,open('leads_2026-10-19.json','w'),indent=1)
for L in leads: print(L['project'],L['totalScore'],L['reviewsCount'],L['email'],len(L['reviews']),L.get('city'),L.get('stateAbbr'),[r['name'] for r in L['reviews']])
