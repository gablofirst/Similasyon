import ezdxf,collections,json,sys
from ezdxf import bbox
d=ezdxf.readfile('raf.dxf');m=d.modelspace()
cache={}
def bb(name):
    if name not in cache:
        try:
            e=bbox.extents(d.blocks[name],fast=True)
            cache[name]=(e.extmin.x,e.extmin.y,e.extmax.x,e.extmax.y) if e.has_data else None
        except Exception: cache[name]=None
    return cache[name]
out=[]
for e in m:
    t=e.dxftype()
    if t=='INSERT':
        b=bb(e.dxf.name)
        out.append(dict(t='I',n=e.dxf.name,L=e.dxf.layer,x=e.dxf.insert.x,y=e.dxf.insert.y,r=e.dxf.rotation,sx=e.dxf.xscale,sy=e.dxf.yscale,bb=b))
    elif t=='LWPOLYLINE':
        out.append(dict(t='P',L=e.dxf.layer,pts=[(p[0],p[1]) for p in e.get_points()]))
    elif t=='LINE':
        out.append(dict(t='P',L=e.dxf.layer,pts=[tuple(e.dxf.start)[:2],tuple(e.dxf.end)[:2]]))
    elif t in('TEXT','MTEXT'):
        out.append(dict(t='T',x=e.dxf.insert.x,y=e.dxf.insert.y,s=e.dxf.text if t=='TEXT' else e.plain_text()))
json.dump(out,open('ins.json','w'))
for k,v in cache.items():print(k,[round(a) for a in v] if v else None)
