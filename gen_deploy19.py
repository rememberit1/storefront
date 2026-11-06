import json,re
tpl=open('deploy_matrix.js').read()
i=tpl.index('const SITES = ')+len('const SITES = ')
j=tpl.index(';\n',i)
head,tail=tpl[:i],tpl[j:]
leads=json.load(open('leads_2026-10-19.json'))
projs=[L['project'] for L in leads]
batches=[projs[k:k+4] for k in range(0,len(projs),4)]
for n,b in enumerate(batches,1):
    sites={p:open(f'sites/{p}/index.html').read() for p in b}
    code=head+json.dumps(sites)+tail
    open(f'deploy_2026-10-19_{n}.js','w').write(code.strip())
    print(n,b,len(code))
