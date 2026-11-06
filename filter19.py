import json,re,csv,collections
t=open('/workspace/agent-tools/c3bfbe6f-4c0f-4137-a9af-96084ae33668.txt').read()
d=json.JSONDecoder().raw_decode(t)[0]['items']
json.dump(d,open('raw_places_2026-10-19.json','w'))
log=list(csv.DictReader(open('leads-log.csv')))
def norm(s): return re.sub(r'[^a-z0-9]','',(s or '').lower())
def ph(s): return re.sub(r'\D','',s or '')[-10:]
lognames={norm(r['business']) for r in log}; logph={ph(r['phone']) for r in log if ph(r['phone'])}
CAT=re.compile(r'plumb|roof|hvac|heating|air condition|furnace|gutter|drain|water heater|septic|sewer',re.I)
CHAIN=re.compile(r'roto-?rooter|mr\.? rooter|benjamin franklin|one hour|\bars\b|rescue rooter|aire serv|michael ?& ?son|len the plumber|horizon services|service experts|mister sparky|mr\.? handyman|window nation|long roofing|power home|leaffilter|leaf filter|ace hardware|baker brothers|john c\.? flood|ductz|rooter-?man|zoom drain|bluefrog|sears|home depot|lowe\'?s|lennox|carrier|trane|frank gay|anytime plumbing|mr\.? plumber|roof ?maxx|erie home|american residential|bath ?fitter|re-bath|goettl|dr\.? energy|ace plumbing|aaa |abc home',re.I)
stats=collections.Counter(); seen=set(); out=[]
for x in d:
    pid=x.get('placeId')
    if pid in seen: stats['duplicate']+=1; continue
    seen.add(pid)
    if x.get('permanentlyClosed') or x.get('temporarilyClosed'): stats['closed']+=1; continue
    if (x.get('totalScore') or 0)<4.5: stats['rating<4.5']+=1; continue
    if (x.get('reviewsCount') or 0)<25: stats['reviews<25']+=1; continue
    cats=' '.join([x.get('categoryName') or '']+(x.get('categories') or []))
    if not CAT.search(cats): stats['off-category']+=1; continue
    if norm(x['title']) in lognames or (ph(x.get('phone')) and ph(x.get('phone')) in logph): stats['already in log']+=1; continue
    if CHAIN.search(x['title']): stats['chain/franchise (name)']+=1; continue
    out.append(x)
print(len(d),len(seen),dict(stats),len(out))
json.dump({'stats':dict(stats),'unique':len(seen),'total':len(d)},open('screen_stats_2026-10-19.json','w'))
json.dump(out,open('cands_2026-10-19.json','w'))
nw=[x for x in out if not x.get('website')]
print('no website',len(nw))
for x in nw: print(x['totalScore'],x['reviewsCount'],'|',x['title'],'|',x['categoryName'],'|',x.get('phone'),'|',x.get('address'))
