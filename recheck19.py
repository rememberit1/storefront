import json,sys
sys.path.insert(0,'.')
from checksite import check
from concurrent.futures import ThreadPoolExecutor
c=json.load(open('cands_2026-10-19.json'))
ws=[x for x in c if x.get('website') and not x['site_status'].startswith('ok') and x.get('state') not in ('New Jersey','New York')]
print('rechecking',len(ws),flush=True)
with ThreadPoolExecutor(int(sys.argv[1]) if len(sys.argv)>1 else 4) as ex:
    res=list(ex.map(lambda x: check(x['website']), ws))
for x,r in zip(ws,res): x['site_status2']=r; 
for x,r in zip(ws,res):
    if r.startswith('ok'): x['site_status']=r
json.dump(c,open('cands_2026-10-19.json','w'))
import collections
print(collections.Counter(r.split(' (')[0].split(':')[0] for r in res))
for x in ws:
    if not x['site_status'].startswith('ok'): print(x['totalScore'],x['reviewsCount'],'|',x['title'],'|',x.get('website'),'|',x['site_status2'])
