# v8.27 — DXF'i eski AutoCAD sürümlerinin açabileceği temiz bir dosyaya yazar.
# Kullanım: python3 dxf_compat.py giris.dxf cikis.dxf R2000|R2004|R2007|R2010
#  - bloklar patlatılır (INSERT → çizgiler), katman ve renkler korunur
#  - R2007+ : MTEXT korunur; R2000/R2004 : MTEXT satır satır TEXT olur
#  - HATCH → sınır çizgisi; SOLID korunur; birim cm ($INSUNITS 5); kod sayfası ANSI_1254 (Türkçe)
import sys, ezdxf
from ezdxf import recover
src, aud = recover.readfile(sys.argv[1]); ver = sys.argv[3]
out = ezdxf.new(ver, setup=True); out.units = 5
if ver in ('R2000', 'R2004'): out.header['$DWGCODEPAGE'] = 'ANSI_1254'; out.encoding = 'cp1254'
out.header['$DWGCODEPAGE'] = 'ANSI_1254'
m = out.modelspace(); keep_mtext = ver not in ('R2000', 'R2004')
for l in src.layers:
    n = l.dxf.name
    if n not in out.layers: out.layers.add(n, color=abs(l.dxf.color) if l.dxf.color else 7)
cnt = {}
def put(e, depth=0):
    t = e.dxftype(); lay = e.dxf.get('layer', '0')
    if lay not in out.layers: out.layers.add(lay)
    a = {'layer': lay}
    if e.dxf.hasattr('color'): a['color'] = e.dxf.color
    if e.dxf.hasattr('true_color') and ver != 'R2000': a['true_color'] = e.dxf.true_color
    try:
        if t == 'INSERT':
            if depth < 8:
                for v in e.virtual_entities(): put(v, depth + 1)
            return
        elif t == 'LINE': m.add_line(e.dxf.start, e.dxf.end, dxfattribs=a)
        elif t == 'LWPOLYLINE': m.add_lwpolyline(list(e.get_points('xyb')), format='xyb', close=e.closed, dxfattribs=a)
        elif t == 'POLYLINE': m.add_lwpolyline([(v.dxf.location.x, v.dxf.location.y) for v in e.vertices], close=e.is_closed, dxfattribs=a)
        elif t == 'ARC': m.add_arc(e.dxf.center, e.dxf.radius, e.dxf.start_angle, e.dxf.end_angle, dxfattribs=a)
        elif t == 'CIRCLE': m.add_circle(e.dxf.center, e.dxf.radius, dxfattribs=a)
        elif t == 'SOLID': m.add_solid([e.dxf.vtx0, e.dxf.vtx1, e.dxf.vtx2, e.dxf.vtx3], dxfattribs=a)
        elif t == 'TEXT':
            m.add_text(e.dxf.text, height=e.dxf.height, rotation=e.dxf.get('rotation', 0), dxfattribs=a).set_placement(e.dxf.insert)
        elif t == 'MTEXT':
            if keep_mtext:
                mt = m.add_mtext(e.text, dxfattribs=a)
                for k in ('insert', 'char_height', 'width', 'attachment_point', 'rotation', 'text_direction'):
                    if e.dxf.hasattr(k): mt.dxf.set(k, e.dxf.get(k))
            else:
                h = e.dxf.char_height; p = e.dxf.insert; rot = e.dxf.get('rotation', 0)
                for i, line in enumerate(e.plain_text().split('\n')):
                    if line.strip(): m.add_text(line, height=h, rotation=rot, dxfattribs=a).set_placement((p.x, p.y - i * h * 1.4))
        elif t in ('SPLINE', 'ELLIPSE'): m.add_lwpolyline([(p.x, p.y) for p in e.flattening(0.5)], dxfattribs=a)
        elif t == 'HATCH':
            for path in e.paths:
                if hasattr(path, 'vertices'): m.add_lwpolyline([(v[0], v[1]) for v in path.vertices], close=True, dxfattribs=a)
                elif hasattr(path, 'edges'):
                    for ed in path.edges:
                        if ed.type.name == 'LINE': m.add_line(ed.start, ed.end, dxfattribs=a)
        else:
            cnt['atlandı ' + t] = cnt.get('atlandı ' + t, 0) + 1; return
        cnt[t] = cnt.get(t, 0) + 1
    except Exception as ex:
        cnt['hata ' + t] = cnt.get('hata ' + t, 0) + 1
for e in src.modelspace(): put(e)
out.set_modelspace_vport(height=6500, center=((1734 + 35917) / 2, (730 + 14808) / 2))
a2 = out.audit(); out.saveas(sys.argv[2])
print(ver, sys.argv[2], 'audit hata', len(a2.errors), dict(sorted(cnt.items())))
