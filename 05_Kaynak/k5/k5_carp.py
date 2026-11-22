import sys, ezdxf
from ezdxf import bbox
d=ezdxf.readfile(sys.argv[1]); m=d.modelspace()
px=lambda X:48.1+(X-8706)/100; py=lambda Y:6.48+(11530-Y)/100
segs={'HP→batı':(155.75,62.8,166.6,63.3),'kapı 156':(155.75,62.8,156.25,64.95),'şerit':(140.53,64.45,156.25,64.95)}
lay=['KOLON','DUVAR','PARAPET DUVAR','TEL ÇİT','PO_HUCRE_RAF','PO_HP_RAF','PO_PAKETLEME','PO_KONVEYOR','PO_KARGO','PO_HAZIR_PAKET','PO_ETICARET_HUCRE','PO_SACAK','PO_BARIYER','CEPHE SANDWICH PANEL','SEKSİYONEL KAPI','PO_HUCRE_DONGU']
for e in m:
    if e.dxf.layer not in lay or e.dxftype() in ('TEXT','MTEXT'): continue
    for sub in (e.virtual_entities() if e.dxftype() in ('INSERT',) else [e]):
        try: b=bbox.extents([sub])
        except Exception: continue
        if not b.has_data: continue
        x0,x1=sorted([px(b.extmin.x),px(b.extmax.x)]); y0,y1=sorted([py(b.extmin.y),py(b.extmax.y)])
        if (x1-x0)>60 or (y1-y0)>60: continue  # bina geneli kontur
        for n,(a0,b0,a1,b1) in segs.items():
            if x0<a1 and x1>a0 and y0<b1 and y1>b0:
                print(f'{n:9s} × {e.dxf.layer:22s} {sub.dxftype():10s} X {x0:.2f}–{x1:.2f} Y {y0:.2f}–{y1:.2f}')
