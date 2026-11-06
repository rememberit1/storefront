import json
from concurrent.futures import ThreadPoolExecutor
from checksite import check
c=json.load(open('cands_2026-10-20.json'))
w=[x for x in c if x.get('website')]
with ThreadPoolExecutor(24) as ex: res=list(ex.map(lambda x: check(x['website']), w))
for x,r in zip(w,res): x['site_status']=r
for x in c:
    if not x.get('website'): x['site_status']='none'
json.dump(c,open('cands_2026-10-20.json','w'))
for x in c:
    if not x['site_status'].startswith('ok'): print(x['totalScore'],x['reviewsCount'],'|',x['title'],'|',x.get('website'),'|',x['site_status'],'|',x.get('phone'))
