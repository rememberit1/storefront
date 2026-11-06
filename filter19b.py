import json,re,csv,collections,sys
sys.path.insert(0,'.')
t=open('/workspace/agent-tools/f58c63e0-1de9-49e3-ac90-dc239ee27854.txt').read()
i=t.find('{"datasetId"'); d=json.JSONDecoder().raw_decode(t[i:])[0]['items']
json.dump(d,open('raw_places_2026-10-19b.json','w'))
prev={x['placeId'] for x in json.load(open('raw_places_2026-10-19.json'))}
exec(open('filter19.py').read().split("stats=collections.Counter()")[0].split("d=json.JSONDecoder")[0])
log=list(csv.DictReader(open('leads-log.csv')))
def norm(s): return re.sub(r'[^a-z0-9]','',(s or '').lower())
def ph(s): return re.sub(r'\D','',s or '')[-10:]
lognames={norm(r['business']) for r in log}; logph={ph(r['phone']) for r in log if ph(r['phone'])}
src=open('filter19.py').read()
CAT=re.compile(r'plumb|roof|hvac|heating|air condition|furnace|gutter|drain|water heater|septic|sewer',re.I)
CHAIN=eval(re.search(r"CHAIN=(re\.compile\(.*\))\n",src).group(1))
stats=collections.Counter(); seen=set(); out=[]
for x in d:
    pid=x.get('placeId')
    if pid in seen or pid in prev: stats['duplicate']+=1; continue
    seen.add(pid)
    if x.get('permanentlyClosed') or x.get('temporarilyClosed'): stats['closed']+=1; continue
    if (x.get('totalScore') or 0)<4.5: stats['rating<4.5']+=1; continue
    if (x.get('reviewsCount') or 0)<25: stats['reviews<25']+=1; continue
    cats=' '.join([x.get('categoryName') or '']+(x.get('categories') or []))
    if not CAT.search(cats): stats['off-category']+=1; continue
    if norm(x['title']) in lognames or (ph(x.get('phone')) and ph(x.get('phone')) in logph): stats['already in log']+=1; continue
    if CHAIN.search(x['title']): stats['chain/franchise (name)']+=1; continue
    out.append(x)
print(len(d),dict(stats),len(out))
from checksite import check
from concurrent.futures import ThreadPoolExecutor
def chk(u):
    if not u: return 'none'
    return check(re.sub(r'^http://','https://',u))
with ThreadPoolExecutor(8) as ex: res=list(ex.map(lambda x: chk(x.get('website')), out))
for x,r in zip(out,res): x['site_status']=r
json.dump({'stats':dict(stats),'total':len(d)},open('screen_stats_2026-10-19b.json','w'))
json.dump(out,open('cands_2026-10-19b.json','w'))
print(collections.Counter(r.split(' (')[0].split(':')[0] for r in res))
for x in out:
    if not x['site_status'].startswith('ok'): print(x['totalScore'],x['reviewsCount'],'|',x['title'],'|',x.get('state'),'|',x.get('phone'),'|',x.get('website'),'|',x['site_status'])
