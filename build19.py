import json,os
from build import build
leads=json.load(open('/workspace/storefront/leads_2026-10-19.json'))
for L in leads:
    d=f"/workspace/storefront/sites/{L['project']}"; os.makedirs(d,exist_ok=True)
    open(d+'/index.html','w').write(build(L))
print('built',len(leads))
