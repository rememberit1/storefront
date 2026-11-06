import json,re
from helpers20 import bucket, short_name, trim, ST
t=open('/workspace/agent-tools/8e82d590-b0c6-46b8-8736-9b598faed6f9.txt').read()
D={x['placeId']:x for x in json.JSONDecoder().raw_decode(t)[0]['items']}
SPEC=[ # placeId, slug, email, source, confidence, site_status, listed_website, reason
("ChIJB0TWW8PIpmMRq-toCEFkDzk","bk-plumbing","Bkplumbing52@gmail.com","https://nextdoor.com/pages/bk-plumbing-llc-laurel-md/","high: business's own Nextdoor page (BK Plumbing LLC, Laurel MD, same phone 240-784-1347). Alt: emmanuelblack66@gmail.com on chamberofcommerce.com + Brandywine Nextdoor page (not used)","none on Google listing; their old domain bkplumbingmd.com shows 'Site not found'","","but I couldn't find a working website for you"),
("ChIJnwslSYNdtokR4QguHYWT_T8","air-and-heating-repair","smaradiaga173@gmail.com","https://citylocalpro.com/cl12310-hvac-system-maintenance-tips-manassas-va","medium-high: business-written CityLocalPro page (same phone 240-815-4666, Manassas)","none (no website on Google listing)","","but I couldn't find a website for you"),
("ChIJver-K2ynt4kRxabJj62fLZk","jw-plumbing-services","jwplumbingsevice1@gmail.com","https://sites.google.com/view/jwplumbingservesdmv/home","high: business's own Google Sites page linked from their Google listing (same phone 202-489-2070, 173 St Patrick Dr, Waldorf). Note spelling 'sevice' is as published","broken: Google listing links only to a basic Google Sites page","https://sites.google.com/view/jwplumbingservesdmv/home","but your Google listing only links to a basic Google Sites page"),
("ChIJFzHqgFRdtokRj-MT2xXbWYI","red-blue-services-plumbing","Craig@RedandBlueServices.com","https://contractorfinder.bradfordwhite.com/contractors/red-and-blue-services-34642-manassas-va ; https://local.yahoo.com/info-169481169-red-blue-services-manassas/","medium-high: contractor-submitted Bradford White profile (same name, Manassas address, business description); domain MX (Google) active. Profile phone 703-270-1253 differs from Google 703-479-0722","none on Google listing; their domain redandblueservices.com shows a Wix 'domain not connected' error","","but I couldn't find a working website for you"),
("ChIJ-yCrIFuzt4kRsM_EDLcVZHY","sbg-home-exteriors","info@sbghome.com","https://sbghome.com/ (search-index copy of their own site) ; https://local-roofing.net/Virginia/SBG-Home-Exteriors-70083985328/","medium-high: on business's own site (same phone 703-899-2365); domain MX (Microsoft 365) active","broken: sbghome.com is an 'under construction' placeholder","https://sbghome.com/","but the website on your Google listing is just an 'under construction' page"),
("ChIJkZTp9pC9t4kRe8VPyIYsxOI","akinfe-air","brianakinfe19@gmail.com","https://firmtechservices.com/314-Air-Conditioning-Service-Silver-Spring-MD ; https://localbeings.com/akinfe-air","medium-high: Akinfe Air service pages (same phone 202-445-1445) built for the business by Firm Tech Services. Alt: brianakinfe@ymail.com on Nextdoor (not used)","none (no website on Google listing)","","but I couldn't find a website for you"),
("ChIJr_AR0Z_Qt4kRr5pQr-0flT4","dmv-exteriors","info@dmvexteriors.com","https://dmvexteriors.com/contact-us/ (search-index copy of their own site) ; https://nextdoor.com/pages/dmv-exteriors-sandy-spring-md/","medium-high: on business's own contact page (same phone 844-368-7663); domain MX (Google) active","broken: dmvexteriors.com shows 'Suspended Site' (HTTP 503)","https://dmvexteriors.com/","but the website on your Google listing has been suspended"),
("ChIJ5W8vCQr9304RO7dCGpLywGA","bayfront-heating-and-ac","Bayfronthvac@gmail.com","https://bayfronthvac.net/ (search-index copy of their own site)","medium: on business's own site (same phone 443-977-1428), but that site now returns HTTP 500; Edgewater/Annapolis area, edge of the DC region","none on Google listing; bayfronthvac.net returns a server error and hvacbaltimoremaryland.com shows 'Site not found'","","but I couldn't find a working website for you"),
("ChIJdQXZ_g8Jt4kRMcjwrZ6SvWo","on-q-services","","not found (BBB offers a contact form only; directories list phone only)","n/a","broken: onqservicesllc.com shows 'Site not found' (HTTP 404)","http://www.onqservicesllc.com/","but the website on your Google listing isn't loading"),
("ChIJR94TEyg4tokRcGzEayNUJao","beltway-sewer-plumbing-services","","not found (NoVA Contractor Hub, iBegin, WhereOrg list phone only)","n/a","none (no website on Google listing)","","but I couldn't find a website for you"),
]
leads=[]
for pid,slug,email,src,conf,status,lw,reason in SPEC:
    x=D[pid]
    L={k:x.get(k) for k in ['title','placeId','categoryName','totalScore','reviewsCount','phone','phoneUnformatted','address','city','state','url','openingHours']}
    if not L.get('phoneUnformatted') and L.get('phone'): L['phoneUnformatted']='+1'+re.sub(r'\D','',L['phone'])
    L['bucket']=bucket(L['categoryName']); L['stateAbbr']=ST.get(L.get('state') or '')
    rv=[r for r in (x.get('reviews') or []) if r.get('stars')==5 and r.get('text') and len(r['text'])>=60]
    rv.sort(key=lambda r: abs(len(r['text'])-220))
    L['reviews']=[{'name':(short_name(r['name']) if r.get('name') else 'Google reviewer'),'stars':5,'text':trim(r['text'])} for r in rv[:4]]
    L['email']=email or None; L['email_source']=src; L['email_confidence']=conf
    L['site_status']=status; L['listed_website']=lw; L['reason']=reason
    L['slug']=slug; L['project']='storefront-'+slug
    L['score']=round(L['totalScore']*L['reviewsCount'],1)
    leads.append(L)
leads.sort(key=lambda L:(0 if L['email'] else 1,-L['score']))
json.dump(leads,open('leads_2026-10-20.json','w'),indent=1)
for L in leads: print(L['slug'],L['totalScore'],L['reviewsCount'],L['email'],len(L['reviews']),L.get('city'),L.get('stateAbbr'))
