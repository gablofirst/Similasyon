# v6.6 — kare hücre göz geometrisi (render, DXF, WMS ve 3D ortak kullanır)
# Plan koordinatı: X doğu, Y güney (m). Hücre: dış çevre rafı (tek yüz, içe bakar) + ada (4 yüz, dışa bakar), 1,5 m tek yön döngü koridoru.
# Göz no: toplama döngüsü sırası (giriş = 01). Yüz: D = dış çevre rafı, A = ada rafı.
import math
RD, AI, GW = 0.88, 1.5, 1.78

def path(h):
    x0, y0, x1, y1 = h['x0'], h['y0'], h['x1'], h['y1']; c = RD+AI/2; ym = (y0+y1)/2
    if h['acik'] == 'E':
        return [(x1-c, ym), (x1-c, y0+c), (x0+c, y0+c), (x0+c, y1-c), (x1-c, y1-c), (x1-c, ym)]
    return [(x0+c, ym), (x0+c, y0+c), (x1-c, y0+c), (x1-c, y1-c), (x0+c, y1-c), (x0+c, ym)]

def _proj(P, q):
    best = None; acc = 0
    for (ax, ay), (bx, by) in zip(P, P[1:]):
        L = math.hypot(bx-ax, by-ay); u = max(0, min(1, ((q[0]-ax)*(bx-ax)+(q[1]-ay)*(by-ay))/(L*L)))
        px, py = ax+u*(bx-ax), ay+u*(by-ay); d = math.hypot(q[0]-px, q[1]-py)
        if best is None or d < best[0]-1e-6: best = (d, acc+u*L, (px, py))
        acc += L
    return best[1], best[2]

def _bays(a, b, n=None):
    L = b-a; n = int(L//GW) if n is None else n; off = a+(L-n*GW)/2
    return [off+(i+0.5)*GW for i in range(n)]

def gozler(h):
    x0, y0, x1, y1 = h['x0'], h['y0'], h['x1'], h['y1']; ym = (y0+y1)/2
    ax0, ay0, ax1, ay1 = h['ada']; G = []
    def add(yuz, kenar, cx, cy, fx, fy, rot):   # c: göz merkezi (raf bandı ortası), f: yüz noktası (koridor kenarı)
        G.append(dict(hucre=h['ad'], yuz=yuz, kenar=kenar, x=round(cx, 3), y=round(cy, 3), fx=round(fx, 3), fy=round(fy, 3), rot=rot))
    # dış çevre
    for x in _bays(x0+RD, x1-RD): add('D', 'K', x, y0+RD/2, x, y0+RD, 0)
    for x in _bays(x0+RD, x1-RD): add('D', 'G', x, y1-RD/2, x, y1-RD, 0)
    sideX = x0 if h['acik'] == 'E' else x1; openX = x1 if h['acik'] == 'E' else x0
    sgn = 1 if sideX == x0 else -1
    for y in _bays(y0+RD, y1-RD): add('D', 'B' if sideX == x0 else 'Do', sideX+sgn*RD/2, y, sideX+sgn*RD, y, 90)
    osg = -sgn
    for a, b in ((y0+RD, ym-2.0), (ym+2.0, y1-RD)):
        for y in _bays(a, b): add('D', 'Do' if openX == x1 else 'B', openX+osg*RD/2, y, openX+osg*RD, y, 90)
    # ada (dışa bakar)
    for x in _bays(ax0, ax1): add('A', 'K', x, ay0+RD/2, x, ay0, 0); add('A', 'G', x, ay1-RD/2, x, ay1, 0)
    for y in _bays(ay0, ay1): add('A', 'B', ax0+RD/2, y, ax0, y, 90); add('A', 'Do', ax1-RD/2, y, ax1, y, 90)
    P = path(h)
    for g in G: g['s'], _ = _proj(P, (g['fx'], g['fy']))
    G.sort(key=lambda g: (round(g['s'], 2), g['yuz']))
    for i, g in enumerate(G, 1): g['no'] = i
    return G

def raf_bantlari(h):
    """çizim için raf dikdörtgenleri (x0,y0,x1,y1)"""
    x0, y0, x1, y1 = h['x0'], h['y0'], h['x1'], h['y1']; ym = (y0+y1)/2; ax0, ay0, ax1, ay1 = h['ada']
    R = [(x0, y0, x1, y0+RD), (x0, y1-RD, x1, y1)]
    if h['acik'] == 'E':
        R += [(x0, y0+RD, x0+RD, y1-RD), (x1-RD, y0+RD, x1, ym-2.0), (x1-RD, ym+2.0, x1, y1-RD)]
    else:
        R += [(x1-RD, y0+RD, x1, y1-RD), (x0, y0+RD, x0+RD, ym-2.0), (x0, ym+2.0, x0+RD, y1-RD)]
    R += [(ax0, ay0, ax1, ay0+RD), (ax0, ay1-RD, ax1, ay1), (ax0, ay0+RD, ax0+RD, ay1-RD), (ax1-RD, ay0+RD, ax1, ay1-RD)]
    return R

if __name__ == '__main__':
    import json, sys
    L = json.load(open(sys.argv[1] if len(sys.argv) > 1 else '/home/claude/work/out/layout.json'))
    for h in L['HUCRE']:
        G = gozler(h); print(h['ad'], len(G), 'göz ×', 5, '=', len(G)*5, '| döngü', round(sum(math.hypot(b[0]-a[0], b[1]-a[1]) for a, b in zip(path(h), path(h)[1:])), 1), 'm')
        print([(g['no'], g['yuz'], g['kenar'], round(g['s'], 1)) for g in G])
