# v8.10 DXF'teki as-built katmanlarını (PO_ dışı) plan koordinatına çevirir → asb_plan.pkl
import sys, pickle, collections, math
from ezdxf import recover
from ezdxf.disassemble import recursive_decompose
d,_=recover.readfile(sys.argv[1]); m=d.modelspace()
px=lambda x:48.1+(x-8706)/100; py=lambda y:6.48+(11530-y)/100
out=collections.defaultdict(list)
ents=[e for e in m if not e.dxf.layer.startswith('PO_')]
for e in recursive_decompose(ents):
    t=e.dxftype(); L=e.dxf.layer; pts=None
    try:
        if t=='LINE': pts=[e.dxf.start,e.dxf.end]
        elif t=='LWPOLYLINE':
            pts=[(p[0],p[1]) for p in e.get_points()]
            if e.closed and pts: pts=pts+[pts[0]]
        elif t=='POLYLINE':
            pts=[(v.dxf.location.x,v.dxf.location.y) for v in e.vertices]
            if e.is_closed and pts: pts=pts+[pts[0]]
        elif t in('CIRCLE','ARC'):
            r=e.dxf.radius;cx,cy=e.dxf.center[0],e.dxf.center[1]
            a0,a1=(0,360) if t=='CIRCLE' else (e.dxf.start_angle,e.dxf.end_angle)
            if a1<a0:a1+=360
            n=max(6,int((a1-a0)/15));pts=[(cx+r*math.cos(math.radians(a0+(a1-a0)*k/n)),cy+r*math.sin(math.radians(a0+(a1-a0)*k/n))) for k in range(n+1)]
        elif t in('SOLID','3DFACE'):
            v=[e.dxf.vtx0,e.dxf.vtx1,e.dxf.vtx3,e.dxf.vtx2];pts=v+[v[0]]
        elif t=='HATCH':
            for p in e.paths:
                if hasattr(p,'vertices'): out[L].append([(px(v[0]),py(v[1])) for v in p.vertices])
    except Exception: pts=None
    if pts and len(pts)>1: out[L].append([(px(p[0]),py(p[1])) for p in pts])
pickle.dump(dict(out),open(sys.argv[2],'wb'))
print({k:len(v) for k,v in out.items() if k in('DUVAR','KOLON','PARAPET DUVAR','İÇ CEPHE SANDWICH PANEL','SEKSİYONEL KAPI','KAPI YANGIN')})
