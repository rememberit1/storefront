import json,re,os,sys
sys.path.insert(0,'.')
from helpers20 import bucket, short_name, trim, ST
from build import build
D={x['placeId']:x for x in json.load(open('cands_2026-10-22.json'))}
SPEC=[
("ChIJJyQRnzW5t4kRmyj7C65ICzA","rivers-hvac-maintenance-services","rivershvac1@gmail.com","https://www.velocityboilerworks.com/?wpsl_stores=rivers-hvac-service","medium: Velocity Boiler Works dealer-locator listing for 'Rivers Hvac service' with the same phone 202-553-8506 (Temple Hills MD); owner Anthony Rivers","none (no website on Google listing)","","but I couldn't find a website for you",("Temple Hills","MD")),
("ChIJ75ons8C7t4kRqRnVc41mfTI","joseph-simpson-son-plumbing","simpsonplumbing@verizon.net","https://exa.ai/library/place/sb4wkfm2yj2","medium: one place aggregator with matching phone 301-894-2233 and address; verizon.net mail is still served (AOL/Yahoo). Note: BuildZoom shows MD plumbing license #50288 expired 05-2021","none on Google listing; their old domain simpsonandsonplumbing.com is a parked GoDaddy page","","but I couldn't find a working website for you",None),
("ChIJacbj-FJTtokRmfhCLH-R2Dc","john-r-plumbing","","not found (Facebook page facebook.com/jrpllc is the only site; directories list phone only; LeadSwift shows a masked Gmail, not used)","n/a","broken: Google listing links only to a Facebook page","https://www.facebook.com/jrpllc","but your Google listing only links to a Facebook page",("Chantilly","VA")),
("ChIJz3q7agm7t4kRTrJRaNezIgY","mega-general-contractors","","not found (wanderboat and cost-guide directories list phone only)","n/a","none (no website on Google listing)","","but I couldn't find a website for you",("Alexandria","VA")),
]
leads=[]
for pid,slug,email,src,conf,status,lw,reason,loc in SPEC:
    x=D[pid]
    L={k:x.get(k) for k in ['title','placeId','categoryName','totalScore','reviewsCount','phone','phoneUnformatted','address','city','state','url','openingHours']}
    if not L.get('phoneUnformatted') and L.get('phone'): L['phoneUnformatted']='+1'+re.sub(r'\D','',L['phone'])
    L['bucket']=bucket(L['categoryName'] if 'Electric' not in L['categoryName'] else 'Plumber'); L['stateAbbr']=ST.get(L.get('state') or '')
    if loc: L['city'],L['stateAbbr']=loc
    rv=[r for r in (x.get('reviews') or []) if r.get('stars')==5 and r.get('text') and len(r['text'])>=60]
    rv.sort(key=lambda r: abs(len(r['text'])-220))
    L['reviews']=[{'name':(short_name(r['name']) if r.get('name') else 'Google reviewer'),'stars':5,'text':trim(r['text'])} for r in rv[:4]]
    L.update(email=email or None,email_source=src,email_confidence=conf,site_status=status,listed_website=lw,reason=reason,slug=slug,project='storefront-'+slug,score=round(L['totalScore']*L['reviewsCount'],1))
    leads.append(L)
leads.sort(key=lambda L:(0 if L['email'] else 1,-L['score']))
for L in leads:
    d=f"sites/{L['project']}"; os.makedirs(d,exist_ok=True); open(d+'/index.html','w').write(build(L))
json.dump(leads,open('leads_2026-10-22.json','w'),indent=1)
r=json.load(open('shared/registry.json'))
for L in leads: r[L['slug']]={"site":L['project'],"url":f"https://previews.getbusinesswinnow.com/{L['slug']}/","alt_url":f"https://storefront-previews.businesswinnow.workers.dev/{L['slug']}/","added":"2026-10-22","takedown":"2026-11-05"}
json.dump(r,open('shared/registry.json','w'),indent=2)
for L in leads: print(L['slug'],L['totalScore'],L['reviewsCount'],L['email'],len(L['reviews']),L['categoryName'])
