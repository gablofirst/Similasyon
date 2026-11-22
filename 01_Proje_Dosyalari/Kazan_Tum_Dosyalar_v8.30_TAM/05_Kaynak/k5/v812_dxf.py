# v8.12 çizim (21.11.2026, Sedat onayı): K5 bandı ana çizimde · K4 + masalar 0,3 m güneye · kafes derinliği 5,2 → 4,9 m
# · K1 kapı 139'dan K4'e uzar · HP akışı K5 üzerinden · tel çit X 150,8 → 167,6 · yangın kapısı 160,1 önünde K5 geçit bölümü
# Kullanım: python3 v812_dxf.py v8.11.dxf v8.12.dxf
import sys, ezdxf
from ezdxf import bbox
from ezdxf.math import Matrix44
d = ezdxf.readfile(sys.argv[1]); m = d.modelspace()
X = lambda x: 8706+(x-48.1)*100; Y = lambda y: 11530-(y-6.48)*100
px = lambda v: 48.1+(v-8706)/100; py = lambda v: 6.48+(11530-v)/100
SH = 0.3; DY = -SH*100           # güneye 0,3 m = DXF Y −30
def bb(e):
    b = bbox.extents([e]); x0, x1 = sorted([px(b.extmin.x), px(b.extmax.x)]); y0, y1 = sorted([py(b.extmin.y), py(b.extmax.y)]); return x0, x1, y0, y1
def mtxt(e): return e.plain_text() if e.dxftype() == 'MTEXT' else ''
log = []
for e in list(m):
    L = e.dxf.layer; t = e.dxftype()
    if L == 'PO_KONVEYOR':
        if t == 'LWPOLYLINE':
            x0, x1, y0, y1 = bb(e)
            if abs(y0-65.0) < .01 and abs(y1-65.7) < .01: e.translate(0, DY, 0); log.append(f'K4/masa {x0:.1f}-{x1:.1f} → Y 65,3–66,0')
            elif abs(x0-139.73) < .02:   # K1: alt ucu 63,9 → 65,3 (K4 üst kenarı)
                pts = [(p[0], Y(65.3) if abs(p[1]-Y(63.9)) < 1 else p[1]) for p in e.get_points('xy')]; e.set_points(pts, format='xy'); log.append('K1 → Y 65,3')
        elif t == 'MTEXT' and any(k in mtxt(e) for k in ('K4-', 'masası')): e.translate(0, DY, 0)
    elif L == 'PO_KARGO':
        if t == 'LWPOLYLINE':
            pts = [(p[0], Y(65.8+SH) if abs(p[1]-Y(65.8)) < 1 else p[1]) for p in e.get_points('xy')]; e.set_points(pts, format='xy')
        elif t == 'MTEXT':
            s = e.text
            for a, b in (('206 m²', '188 m²'), ('122 m²', '109 m²'), ('19 m²', '18 m²')): s = s.replace(a, b)
            e.text = s
    elif L == 'PO_AKIS_ETICARET':
        x0, x1, y0, y1 = bb(e)
        if t == 'LWPOLYLINE' and y1 > 65:
            pts = [(p[0], p[1]+DY if abs(p[1]-Y(65.35)) < 2 else p[1]) for p in e.get_points('xy')]; e.set_points(pts, format='xy')
        elif t in ('SOLID', 'CIRCLE', 'MTEXT') and y0 > 64.6 and y1 < 66.1: e.translate(0, DY, 0)
    elif L == 'PO_AKIS_HAZIR_PAKET' and t in ('LWPOLYLINE', 'SOLID'):
        x0, x1, y0, y1 = bb(e)
        if y1 > 66: m.delete_entity(e); log.append('eski HP elle taşıma oku silindi')
    elif L == 'PO_UYARI' and 'tel çit' in mtxt(e):
        e.text = 'v8.12: tel çit X 150,8 → X 167,6–167,9 taşındı (uygulanacak)'
    elif L == 'PO_YAZI' and 'YERLEŞİM v8.11' in mtxt(e):
        e.text = e.text.replace('YERLEŞİM v8.11', 'YERLEŞİM v8.12 (K5)')
    elif L == 'PO_SACAK' and t == 'MTEXT':
        e.text = e.text.replace('v8.11:', 'v8.12: K4 + kafes 0,3 m güneye ·')
# tel çit: TEL ÇİT bloğunda X ≈150,8 enine çit +17,05 m doğuya (X 167,6–167,9, kafes 167,5 dışında, kolon 167,82 hizası)
ins = [e for e in m if e.dxftype() == 'INSERT' and e.dxf.name == 'TEL ÇİT'][0]
be = list(d.blocks['TEL ÇİT']); ve = list(ins.virtual_entities()); n = 0
for b, v in zip(be, ve):
    x0, x1, y0, y1 = bb(v)
    if x0 > 150.4 and x1 < 150.95 and y0 > 64.3: b.transform(Matrix44.translate(1705, 0, 0)); n += 1
log.append(f'tel çit parçası taşındı: {n}')
# K5 bandı (PO_KONVEYOR, mor): HP fatura → batı Y 63,05 → kapı 156 → duvar dibi şerit Y 64,85 → K1 doğu kenarı
w = 0.25; YS = 64.85
segs = [(156.0-w, 63.05-w, 166.6, 63.05+w), (156.0-w, 63.05-w, 156.0+w, YS+w), (140.53, YS-w, 156.0+w, YS+w)]
GATE = (159.5, 160.7)
def rect(x0, y0, x1, y1): return [(X(x0), Y(y0)), (X(x1), Y(y0)), (X(x1), Y(y1)), (X(x0), Y(y1))]
for x0, y0, x1, y1 in segs:
    m.add_lwpolyline(rect(x0, y0, x1, y1), close=True, dxfattribs={'layer': 'PO_KONVEYOR', 'color': 6})
    parts = [(x0, x1)] if y0 > 63.5 or x1 < GATE[0] else [(x0, GATE[0]), (GATE[1], x1)]
    for a, b in parts:
        h = m.add_hatch(color=6, dxfattribs={'layer': 'PO_KONVEYOR'}); h.paths.add_polyline_path(rect(a, y0, b, y1))
m.add_lwpolyline(rect(GATE[0], 63.05-w-0.05, GATE[1], 63.05+w+0.05), close=True, dxfattribs={'layer': 'PO_UYARI', 'color': 1, 'lineweight': 50})
L5 = (166.6-156.0)+(YS-63.05)+(156.0-140.53)
t = m.add_mtext(f'K5 · HP → kapı 156 → K1 · ≈{L5:.0f} m', dxfattribs={'layer': 'PO_KONVEYOR', 'char_height': 30, 'style': 'PO_ARIAL', 'color': 6})
t.set_location((X(149.2), Y(63.75)), attachment_point=5)
t = m.add_mtext('K5 geçit bölümü (menteşeli) · yangın kapısı 160,1 önü', dxfattribs={'layer': 'PO_UYARI', 'char_height': 18, 'style': 'PO_ARIAL', 'color': 1})
t.set_location((X(160.1), Y(62.45)), attachment_point=8)
# HP akışı: H6 → K5 → K1 (turuncu ok)
fl = [(166.3, 63.05), (156.0, 63.05), (156.0, YS), (141.4, YS)]
m.add_lwpolyline([(X(a), Y(b)) for a, b in fl], dxfattribs={'layer': 'PO_AKIS_HAZIR_PAKET', 'color': 30, 'const_width': 8})
m.add_solid([(X(141.4), Y(YS-0.3)), (X(141.4), Y(YS+0.3)), (X(140.6), Y(YS)), (X(140.6), Y(YS))], dxfattribs={'layer': 'PO_AKIS_HAZIR_PAKET', 'color': 30})

# Kaçış geçitleri (saçak): yangın kapısı 125,4 ve 160,1 önünden yanaşma şeridine 1,2 m boş koridor; masalar bölünür.
# Ölçüm (k5_kacis / kac_sacak): saçaktaki kapıların hiçbiri sayılmazsa en uzun 45,8 m (>45); yalnız 125,4 + 160,1 açıkken 44,3 m.
if 'PO_KACIS' not in d.layers: d.layers.add('PO_KACIS', color=3)
GEC = {125.4: (124.8, 126.0), 160.1: (159.5, 160.7)}
for e in list(m.query('LWPOLYLINE[layer=="PO_KONVEYOR"]')):
    x0, x1, y0, y1 = bb(e)
    for xc, (a, b) in GEC.items():
        if abs(y0-65.3) < .01 and x0 < a and x1 > b:     # masa geçitte bölünür
            m.add_lwpolyline(rect(x0, 65.3, a, 66.0), close=True, dxfattribs={'layer': 'PO_KONVEYOR'})
            m.add_lwpolyline(rect(b, 65.3, x1, 66.0), close=True, dxfattribs={'layer': 'PO_KONVEYOR'})
            m.delete_entity(e); log.append(f'masa {x0:.1f}-{x1:.1f} geçit {a}-{b} ile bölündü')
for xc, (a, b) in GEC.items():
    m.add_lwpolyline(rect(a, 64.4, b, 71.0), close=True, dxfattribs={'layer': 'PO_KACIS', 'color': 3, 'lineweight': 50})
    h = m.add_hatch(color=3, dxfattribs={'layer': 'PO_KACIS'}); h.set_pattern_fill('ANSI31', scale=8); h.paths.add_polyline_path(rect(a, 64.4, b, 71.0))
    t = m.add_mtext(f'KAÇIŞ GEÇİDİ 1,2 m · kapı {xc:.1f}'.replace('.', ','), dxfattribs={'layer': 'PO_KACIS', 'char_height': 22, 'style': 'PO_ARIAL', 'color': 3, 'rotation': 90})
    t.set_location((X(b+0.35), Y(68.0)), attachment_point=5)
for e in m.query('MTEXT[layer=="PO_KONVEYOR"]'):
    for k, xn in (('Batı masası', 122.9), ('Doğu masası', 157.75)):
        if k in e.plain_text(): e.dxf.insert = (X(xn), e.dxf.insert.y, 0)
t = m.add_mtext('Yangın kapısı 143,1: dışı K5 + K4 → çıkış sayılmaz (İSG teyidi)', dxfattribs={'layer': 'PO_UYARI', 'char_height': 16, 'style': 'PO_ARIAL', 'color': 1})
t.set_location((X(143.1), Y(62.3)), attachment_point=8)
d.saveas(sys.argv[2]); print('\n'.join(log)); print('K5 uzunluk', round(L5, 1))
