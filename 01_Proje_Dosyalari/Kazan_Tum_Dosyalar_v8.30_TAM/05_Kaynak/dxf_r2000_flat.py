# v8.10 — ezdxf DXF'i LibreDWG'nin okuyabileceği düz R2000 DXF'e çevirir (bloklar çizgiye açılır, MTEXT → TEXT, HATCH → sınır).
# Kullanım: python3 dxf_r2000_flat.py giris.dxf flat_r2000.dxf ; sonra: dxf2dwg -y --as r2000 -o cikis.dwg flat_r2000.dxf
import sys, ezdxf
src = ezdxf.readfile(sys.argv[1]); out = ezdxf.new('R2000', setup=True); out.units = 5; m = out.modelspace()
for l in src.layers:
    if l.dxf.name not in out.layers: out.layers.add(l.dxf.name, color=l.dxf.color if l.dxf.color > 0 else 7)
def put(e, depth=0):
    t = e.dxftype(); lay = e.dxf.get('layer', '0')
    if lay not in out.layers: out.layers.add(lay)
    a = {'layer': lay}
    if e.dxf.hasattr('color'): a['color'] = e.dxf.color
    try:
        if t == 'INSERT':
            if depth < 7:
                for v in e.virtual_entities(): put(v, depth+1)
        elif t == 'LINE': m.add_line(e.dxf.start, e.dxf.end, dxfattribs=a)
        elif t == 'LWPOLYLINE': m.add_lwpolyline(list(e.get_points('xyb')), format='xyb', close=e.closed, dxfattribs=a)
        elif t == 'POLYLINE': m.add_lwpolyline([(v.dxf.location.x, v.dxf.location.y) for v in e.vertices], close=e.is_closed, dxfattribs=a)
        elif t == 'ARC': m.add_arc(e.dxf.center, e.dxf.radius, e.dxf.start_angle, e.dxf.end_angle, dxfattribs=a)
        elif t == 'CIRCLE': m.add_circle(e.dxf.center, e.dxf.radius, dxfattribs=a)
        elif t == 'SOLID': m.add_solid([e.dxf.vtx0, e.dxf.vtx1, e.dxf.vtx2, e.dxf.vtx3], dxfattribs=a)
        elif t == 'TEXT': m.add_text(e.dxf.text, height=e.dxf.height, rotation=e.dxf.get('rotation', 0), dxfattribs=a).set_placement(e.dxf.insert)
        elif t == 'MTEXT':
            h = e.dxf.char_height; p = e.dxf.insert; rot = e.dxf.get('rotation', 0)
            for i, line in enumerate(e.plain_text().split('\n')):
                if line.strip(): m.add_text(line, height=h, rotation=rot, dxfattribs=a).set_placement((p.x, p.y-i*h*1.4))
        elif t == 'HATCH':
            for path in e.paths:
                if hasattr(path, 'vertices'): m.add_lwpolyline([(v[0], v[1]) for v in path.vertices], close=True, dxfattribs=a)
    except Exception: pass
for e in src.modelspace(): put(e)
out.saveas(sys.argv[2])
