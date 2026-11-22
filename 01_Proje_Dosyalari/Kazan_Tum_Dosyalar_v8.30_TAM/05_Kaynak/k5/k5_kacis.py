# v8.26: K5 bandının kaçışa etkisi. Kullanım: python3 k5_kacis.py <layout.json> <kacis.py> [png]
import numpy as np, sys, json, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
LJ, KP = sys.argv[1], sys.argv[2]; OUT = sys.argv[3] if len(sys.argv) > 3 else None
sys.argv = ['x', LJ]; exec(open(KP).read().split('g0=base()')[0])
Z = {z['id']: z for z in L['Z']}; fz = Z['hp_fatura']; print('hp_fatura', fz['x0'], fz['y0'], fz['x1'], fz['y1'])
g0 = base()
for r in L.get('KAMP_PAL', []): block(g0, *r)
SA = [60.8, 86.4, 104.5, 121.3, 139.1, 156.0, 173.2, 190.0, 207.2, 81.2, 108.4, 125.4, 143.1, 160.1, 177.1, 194.1, 211.1]
N = [160.1, 194.1, 81.2, 125.4]; T = [81.2, 125.4]
mask = np.zeros_like(g0, bool); mask[iy(7.3):, ix(48.4):ix(168.5)] = True
def k5(g, gate):
    g = g.copy()
    block(g, 155.75, 62.8, 166.6, 63.3)        # K5 iç kol (HP fatura → batı)
    block(g, 155.75, 62.8, 156.25, 64.4)       # K5 kapı 156'ya inen kol
    if gate: block(g, gate[0], 62.8, gate[1], 63.3, 0)
    return g
res = {}
SAC = [x for x in SA if not 100 < x < 165] + [125.4, 160.1]   # saçakta yalnız kaçış geçitli kapılar
for ad, g, ex in [('K5 yok', g0, SA), ('K5, geçitsiz', k5(g0, None), SA), ('K5 + geçit X 159,5–160,7', k5(g0, (159.5, 160.7)), SA), ('v8.12: K5 + geçit, saçakta yalnız 125,4/160,1', k5(g0, (159.5, 160.7)), SAC)]:
    gg, D = run(g, ex, N, T)
    M = np.where((gg == 0) & mask & np.isfinite(D), D, np.nan)
    a, b = np.unravel_index(np.nanargmax(M), M.shape)
    hp = M[iy(49):iy(64.3), ix(157.4):ix(168.5)]
    # HP fatura önü (X 162–166, Y 62–62.6) en yakın çıkış
    fat = M[iy(62.0):iy(62.6), ix(162):ix(166)]
    res[ad] = (np.nanmax(M), (X0+b*R, Y0+a*R), np.nanmax(hp), np.nanmax(fat))
    print(f'{ad:28s} en uzun {np.nanmax(M):5.1f} m @({X0+b*R:.1f},{Y0+a*R:.1f}) · HP alanı en uzun {np.nanmax(hp):4.1f} m · fatura önü {np.nanmax(fat):4.1f} m · 45 m üstü {np.nansum(M>45)*R*R:.0f} m²')
    if OUT and ad.startswith('v8.12'):
        fig, ax = plt.subplots(figsize=(15, 6)); ext = [X0, X0+nx*R, Y0+ny*R, Y0]
        ax.imshow(np.where(gg == 1, 1, np.nan), extent=ext, cmap='Greys', vmin=0, vmax=1.4, interpolation='nearest')
        im = ax.imshow(M, extent=ext, cmap='RdYlGn_r', vmin=0, vmax=60, interpolation='nearest')
        for x in ex: ax.plot(x, 64.4, 'bv', ms=6)
        for x in N: ax.plot(x, 6.5, 'b^', ms=6)
        ax.set_xlim(47, 169.5); ax.set_ylim(65.5, 5.5); ax.set_aspect('equal')
        ax.set_title(f'v8.12 kaçış · K5 + geçit, saçakta yalnız kaçış geçitli 125,4 / 160,1 · en uzun {np.nanmax(M):.1f} m (sınır 45 m)', fontsize=11)
        fig.colorbar(im, ax=ax, label='En yakın çıkışa yürüme (m)', shrink=0.8); plt.savefig(OUT, dpi=110, bbox_inches='tight')
