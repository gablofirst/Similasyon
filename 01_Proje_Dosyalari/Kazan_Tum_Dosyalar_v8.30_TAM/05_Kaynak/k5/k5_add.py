import sys, ezdxf
src, out = sys.argv[1], sys.argv[2]
d = ezdxf.readfile(src); m = d.modelspace()
X=lambda x:8706+(x-48.1)*100; Y=lambda y:11530-(y-6.48)*100
if 'PO_K5_ONERI' not in d.layers: d.layers.add('PO_K5_ONERI', color=6)
w=0.25
segs=[(156.0-w,63.05-w,166.6,63.05+w),   # HP fatura -> bati
      (156.0-w,63.05-w,156.0+w,64.7+w),  # kapi 156'dan guneye
      (140.53,64.7-w,156.0+w,64.7+w)]    # duvar dibi serit -> K1
for x0,y0,x1,y1 in segs:
    m.add_lwpolyline([(X(x0),Y(y0)),(X(x1),Y(y0)),(X(x1),Y(y1)),(X(x0),Y(y1))],close=True,
                     dxfattribs={'layer':'PO_K5_ONERI'})
    h=m.add_hatch(color=6,dxfattribs={'layer':'PO_K5_ONERI'})
    h.paths.add_polyline_path([(X(x0),Y(y0)),(X(x1),Y(y0)),(X(x1),Y(y1)),(X(x0),Y(y1))])
L=(166.6-156.0)+(64.7-63.05)+(156.0-140.53)
t=m.add_mtext(f'K5 (öneri) · HP → kapı 156 → K1 · ≈{L:.0f} m',
              dxfattribs={'layer':'PO_K5_ONERI','char_height':30,'style':'PO_ARIAL'})
t.set_location((X(149.2),Y(63.55)), attachment_point=5)
d.saveas(out); print('K5 uzunluk', round(L,1))
