import json, checksite
from concurrent.futures import ThreadPoolExecutor
c=json.load(open('cands_2026-10-20.json'))
bad=[x for x in c if x.get('website') and not x['site_status'].startswith('ok') and 'social' not in x['site_status']]
with ThreadPoolExecutor(4) as ex: res=list(ex.map(lambda x: checksite.check(x['website']), bad))
for x,r in zip(bad,res): x['site_status']=r
json.dump(c,open('cands_2026-10-20.json','w'))
for x in c:
    if not x['site_status'].startswith('ok'): print(x['totalScore'],x['reviewsCount'],'|',x['title'],'|',x.get('website'),'|',x['site_status'])
