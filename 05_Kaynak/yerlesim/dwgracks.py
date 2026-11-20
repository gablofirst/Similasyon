# libredwg'nin düşürdüğü dinamik raf bloklarını (*U98, *U100) ins.json konumlarıyla yeniden yerleştirir → dwgbg.pkl'e ekler
import sys,json,pickle,math,collections
from ezdxf import recover,bbox
from ezdxf.disassemble import recursive_decompose
dxf,insj,pkl=sys.argv[1:4]
fx=lambda x:83.235+(x-87883)/1001.96
fy=lambda y:30.2-(y-200527)/1001.96
d,_=recover.readfile(dxf)
D=pickle.load(open(pkl,'rb'))
I=[e for e in json.load(open(insj)) if e['t']=='I' and e['n'] in('*U98','*U100')]
for n in('*U98','*U100'):
    e=bbox.extents(d.blocks[n],fast=True);print(n,'bb dxf',[round(v) for v in (e.extmin.x,e.extmin.y,e.extmax.x,e.extmax.y)],'bb ins.json',[round(v) for v in next(i['bb'] for i in I if i['n']==n)])
geo={}
for n in('*U98','*U100'):
    segs=collections.defaultdict(list)
    for e in recursive_decompose(d.blocks[n]):
        t=e.dxftype();c=e.dxf.color if e.dxf.color not in(0,256) else (d.layers.get(e.dxf.layer).color if d.layers.has_entry(e.dxf.layer) else 7)
        if t=='LINE':segs[c].append([tuple(e.dxf.start)[:2],tuple(e.dxf.end)[:2]])
        elif t=='LWPOLYLINE':
            p=[(q[0],q[1]) for q in e.get_points()]
            if e.is_closed:p.append(p[0])
            segs[c].append(p)
    geo[n]=segs
k=0
for i in I:
    r=math.radians(i['r'] or 0);cs,sn=math.cos(r),math.sin(r)
    for c,ss in geo[i['n']].items():
        for s in ss:
            D.setdefault(c,[]).append([(fx(i['x']+(u*i['sx'])*cs-(v*i['sy'])*sn),fy(i['y']+(u*i['sx'])*sn+(v*i['sy'])*cs)) for u,v in s]);k+=1
pickle.dump(D,open(pkl,'wb'));print('raf segment',k,'insert',len(I))
