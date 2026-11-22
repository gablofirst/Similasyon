# v8.12 çakışma: PO katmanları (güney bant + saçak) × KOLON / DUVAR / TEL ÇİT / kapı ve kendi aralarında
import sys, ezdxf, itertools
from ezdxf import bbox
d = ezdxf.readfile(sys.argv[1]); m = d.modelspace()
px = lambda v: 48.1+(v-8706)/100; py = lambda v: 6.48+(11530-v)/100
def boxes(ents, sub=True):
    out = []
    for e in ents:
        for s in (e.virtual_entities() if (e.dxftype() == 'INSERT' and sub) else [e]):
            if s.dxftype() in ('TEXT', 'MTEXT', 'ATTRIB'): continue
            try: b = bbox.extents([s])
            except Exception: continue
            if not b.has_data: continue
            x0, x1 = sorted([px(b.extmin.x), px(b.extmax.x)]); y0, y1 = sorted([py(b.extmin.y), py(b.extmax.y)])
            if x1-x0 > 60 or y1-y0 > 60: continue
            out.append((e.dxf.layer, s.dxftype(), x0, y0, x1, y1))
    return out
AS = boxes([e for e in m if e.dxf.layer in ('KOLON', 'DUVAR', 'TEL ÇİT', 'PARAPET DUVAR', 'SEKSİYONEL KAPI', 'KAPI YANGIN')])
PO = [b for b in boxes([e for e in m if e.dxf.layer in ('PO_KONVEYOR', 'PO_KARGO', 'PO_SACAK', 'PO_SEVK', 'PO_HAZIR_PAKET', 'PO_ETICARET_HUCRE', 'PO_PAKETLEME')]) if b[5] > 60]
ov = lambda a, b: a[2] < b[4]-0.005 and a[4] > b[2]+0.005 and a[3] < b[5]-0.005 and a[5] > b[3]+0.005
for p in PO:
    for a in AS:
        if ov(p, a): print(f'{p[0]:14s} {p[2]:.2f}-{p[4]:.2f}/{p[3]:.2f}-{p[5]:.2f}  ×  {a[0]:16s} {a[1]:10s} {a[2]:.2f}-{a[4]:.2f}/{a[3]:.2f}-{a[5]:.2f}')
conv = [p for p in PO if p[0] == 'PO_KONVEYOR' and p[1] == 'LWPOLYLINE']; kg = [p for p in PO if p[0] == 'PO_KARGO' and p[1] == 'LWPOLYLINE']
for a, b in itertools.product(conv, kg):
    if ov(a, b): print('konveyör × kafes', a[2:], b[2:])
k5 = [p for p in conv if p[5] < 65.2 and p[3] > 64.5]; k4 = [p for p in conv if abs(p[3]-65.3) < .01]
print('K5 şerit', [(round(p[3], 2), round(p[5], 2)) for p in k5], '· K4', sorted({(round(p[3], 2), round(p[5], 2)) for p in k4}))
print('K5–duvar', round(min(p[3] for p in k5)-64.4, 2), 'm · K5–K4', round(min(p[3] for p in k4)-max(p[5] for p in k5), 2), 'm')
