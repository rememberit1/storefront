import re
def bucket(cat):
    c=cat.lower()
    return 'Roofing' if 'roof' in c else 'Plumbing' if 'plumb' in c else 'HVAC'
ST={'Virginia':'VA','Maryland':'MD','District of Columbia':'DC'}
def short_name(n):
    p=n.strip().split()
    if len(p)==1: return p[0][:1].upper()+p[0][1:]
    return p[0][:1].upper()+p[0][1:]+' '+p[-1][0].upper()+'.'
def trim(t,maxc=300):
    t=re.sub(r'\s+',' ',t).strip()
    if len(t)<=maxc: return t
    s=re.split(r'(?<=[.!?])\s+',t); out=''
    for x in s:
        if len(out)+len(x)+1>maxc: break
        out=(out+' '+x).strip()
    return out or t[:maxc].rsplit(' ',1)[0]+'…'
