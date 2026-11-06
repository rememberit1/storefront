import json,sys,re
sys.path.insert(0,'.')
import checksite
from checksite import check
from concurrent.futures import ThreadPoolExecutor
c=json.load(open('cands_2026-10-19.json'))
def chk(u):
    u2=re.sub(r'^http://','https://',u)
    r=check(u2)
    return r
ws=[x for x in c if x.get('website') and not x['site_status'].startswith('ok') and x.get('state') not in ('New Jersey','New York')]
print('rechecking',len(ws),flush=True)
with ThreadPoolExecutor(8) as ex:
    res=list(ex.map(lambda x: chk(x['website']), ws))
for x,r in zip(ws,res):
    x['site_status3']=r
    if r.startswith('ok'): x['site_status']=r+' via https'
json.dump(c,open('cands_2026-10-19.json','w'))
import collections
print(collections.Counter(r.split(' (')[0].split(':')[0] for r in res))
for x in ws:
    if not x['site_status'].startswith('ok'): print(x['totalScore'],x['reviewsCount'],'|',x['title'],'|',x.get('website'),'|',x['site_status3'])
