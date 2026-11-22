# ADEYA DWG (DXF'e çevrilmiş) → plan koordinatında çizgi segmentleri (dwgbg.pkl)
import sys,pickle,collections,math
from ezdxf import recover
from ezdxf.disassemble import recursive_decompose
fx=lambda x:83.235+(x-87883)/1001.96
fy=lambda y:30.2-(y-200527)/1001.96
d,_=recover.readfile(sys.argv[1]);m=d.modelspace()
out=collections.defaultdict(list)
def col(e):
    try:
        c=e.dxf.color
        if c in (0,256):
            L=d.layers.get(e.dxf.layer);c=L.color if L else 7
        return c
    except Exception:return 7
for e in recursive_decompose(m):
    t=e.dxftype();c=col(e);pts=None
    try:
        if t=='LINE':pts=[e.dxf.start,e.dxf.end]
        elif t in('LWPOLYLINE','POLYLINE'):
            pts=list(e.points()) if t=='POLYLINE' else [(p[0],p[1]) for p in e.get_points()]
            if e.is_closed and pts:pts=pts+[pts[0]]
        elif t in('CIRCLE','ARC'):
            r=e.dxf.radius;cx,cy=e.dxf.center[0],e.dxf.center[1]
            a0,a1=(0,360) if t=='CIRCLE' else (e.dxf.start_angle,e.dxf.end_angle)
            if a1<a0:a1+=360
            n=max(6,int((a1-a0)/15));pts=[(cx+r*math.cos(math.radians(a0+(a1-a0)*k/n)),cy+r*math.sin(math.radians(a0+(a1-a0)*k/n))) for k in range(n+1)]
        elif t=='SOLID' or t=='3DFACE':
            v=[e.dxf.vtx0,e.dxf.vtx1,e.dxf.vtx3,e.dxf.vtx2];pts=v+[v[0]]
    except Exception:pts=None
    if pts and len(pts)>1:out[c].append([(fx(p[0]),fy(p[1])) for p in pts])
pickle.dump(dict(out),open(sys.argv[2],'wb'))
allp=[q for v in out.values() for s in v for q in s]
xs=[p[0] for p in allp];ys=[p[1] for p in allp]
print({k:len(v) for k,v in sorted(out.items(),key=lambda kv:-len(kv[1]))[:12]})
print('X',round(min(xs),1),round(max(xs),1),'Y',round(min(ys),1),round(max(ys),1),'seg',sum(len(v) for v in out.values()))
