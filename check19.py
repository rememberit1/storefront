import json,sys
sys.path.insert(0,'.')
from checksite import check
from concurrent.futures import ThreadPoolExecutor
c=json.load(open('cands_2026-10-19.json'))
ws=[x for x in c if x.get('website')]
with ThreadPoolExecutor(24) as ex:
    res=list(ex.map(lambda x: check(x['website']), ws))
for x,r in zip(ws,res): x['site_status']=r
for x in c:
    if not x.get('website'): x['site_status']='none'
json.dump(c,open('cands_2026-10-19.json','w'))
import collections
print(collections.Counter(r.split(' (')[0].split(':')[0] for r in res))
for x in c:
    if not x['site_status'].startswith('ok'): print(x['totalScore'],x['reviewsCount'],'|',x['title'],'|',x.get('state'),'|',x.get('website'),'|',x['site_status'])
