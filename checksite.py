import json,re,subprocess,sys,socket
from urllib.parse import urlparse
SOCIAL=re.compile(r'(facebook|fb\.com|instagram|yelp|twitter|x\.com|linkedin|thumbtack|nextdoor|angi|homeadvisor|houzz|bbb\.org|google\.com|business\.site|sites\.google|linktr\.ee|tiktok|youtube)',re.I)
PARK=re.compile(r'domain (is )?for sale|buy this domain|this domain may be for sale|parked (free|domain)|sedoparking|parkingcrew|bodis|hugedomains|dan\.com|afternic|godaddy\.com/domainsearch|domain has expired|this domain has been registered|future home of|website coming soon|under construction|account suspended|is not available|default web site page|welcome to nginx|apache2 ubuntu default|index of /',re.I)
def check(url):
    import threading; BODY='/tmp/body_%d.html'%threading.get_ident()
    if not url: return 'none'
    host=urlparse(url).hostname or ''
    if SOCIAL.search(host): return 'broken: social/directory page only (%s)'%host
    try: socket.getaddrinfo(host,80)
    except Exception: return 'broken: DNS failure'
    r=subprocess.run(['curl','-sL','-m','20','-A','Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/124 Safari/537.36','-o',BODY,'-w','%{http_code} %{url_effective}',url],capture_output=True,text=True)
    if r.returncode==28: return 'broken: timeout'
    if r.returncode!=0:
        return 'broken: curl error %d'%r.returncode
    code,eff=r.stdout.split(' ',1)
    code=int(code)
    ehost=urlparse(eff).hostname or ''
    if SOCIAL.search(ehost): return 'broken: redirects to social/directory (%s)'%ehost
    try: body=open(BODY,errors='ignore').read()
    except: body=''
    if code in (403,429,503) and re.search(r'cloudflare|captcha|just a moment|attention required',body,re.I): return 'ok (bot-protected %d)'%code
    if code>=400: return 'broken: HTTP %d'%code
    text=re.sub(r'<script.*?</script>|<style.*?</style>','',body,flags=re.S|re.I)
    text=re.sub(r'<[^>]+>',' ',text)
    if PARK.search(body[:20000]) and len(text.split())<400: return 'broken: parked/placeholder'
    if len(text.split())<15 and 'window.location' not in body and '<iframe' not in body.lower() and len(body)<3000: return 'broken: empty page'
    return 'ok (%d)'%code
if __name__=='__main__':
    for u in sys.argv[1:]: print(u,'=>',check(u))
