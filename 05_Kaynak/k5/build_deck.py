import json,re,base64,sys,os
K=sys.argv[1]; old=sys.argv[2]; out=sys.argv[3]
s=open(old).read(); head=s[:s.find('<section')]
order=json.load(open(f'{K}/deck.json'))['order']
def blob(m):
    b=base64.b64encode(open(f'{K}/assets/{m.group(1)}.png','rb').read()).decode()
    return f'data:image/png;base64,{b}'
body=''
for n in order:
    t=open(f'{K}/slides/{n}.html').read()
    body+=re.sub(r'/_blob/([0-9a-f]{32})',blob,t)+'\n'
open(out,'w').write(head+body+'</div></body></html>')
print(out, os.path.getsize(out))
