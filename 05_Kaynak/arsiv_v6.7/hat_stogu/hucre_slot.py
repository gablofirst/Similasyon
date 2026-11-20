# v6.6 — kare hücre stoğu ve göz ataması (19.11.2026)
# Her hücre (H1, H2) e-ticaret toplama SKU'larının tamamını (A+B+C, grup 'hat') tutar; sipariş hücrelere eşit bölünür.
# Kapasite: hücre başı 26 göz × 5 kat = 130 göz (hucre_geo.py). Besleme sıklığı = kapasitenin taşıdığı en uzun süre.
# Lansman (Z, > 2 göz) kampanya lokasyonundan palet önünden toplanır. Yerleşim iki hücrede aynıdır (ayna değil, aynı göz no).
# Ergonomi (v6.5 kuralı): göz başına satır yüksek ürün kat 3 → 2 → 4 → 1 → 5; 5,5 L kavanoz yalnız kat 2/1; A ürünleri döngü başı/sonu.
# Çalıştırma: python3 hucre_slot.py <layout.json>  → hucre_slotted.pkl, hucre_cells.json, hucre_ozet.json
import sys, json, math
import pandas as pd, numpy as np
sys.path.insert(0, '../yerlesim'); import hucre_geo as HG
L = json.load(open(sys.argv[1] if len(sys.argv) > 1 else '/home/claude/work/out/layout.json'))
d = pd.read_pickle('df.pkl'); A = 'ABC_satir(toplama_sikligi)'
GV = 1.78*0.88*0.50*0.65; SAFE = 1.2; LV = 5; NH = len(L['HUCRE'])
GOZ = HG.gozler(L['HUCRE'][0]); NG = len(GOZ)
ERG = {3: 0.0, 2: 0.2, 4: 1.0, 1: 2.0, 5: 3.0}; HEAVY, MID = 5000, 2400

base = d[(d.grup == 'hat') & (d.d_top > 0)].copy().sort_values('toplama_satiri', ascending=False)
base['lansman'] = base.urun_adi.str.contains('LANSMAN') & (base.XYZ == 'Z')
def need(h, T):
    st = np.maximum(2, np.ceil(h.d_tasarim/NH*T*SAFE))
    m3 = st*h.hacim/1e6
    b = np.where((h.hacim <= 300) | (m3 <= GV/8), 8, 4)
    slot = np.maximum(1, np.ceil(m3/(GV/b)))
    return st, slot/b
def fit(T):
    h = base.copy(); st, gz = need(h, T); h['stok_adet'] = st; h['goz'] = gz
    h['yer'] = np.where(h.lansman & (h.goz > 2), 'kampanya lokasyonu (palet)', 'hücre gözü')
    return h, float(h[h.yer == 'hücre gözü'].goz.sum())
best = None
for T in [x/4 for x in range(4, 25)]:
    h, g = fit(T)
    if g <= NG*LV*0.97: best = (T, h, g)   # %3 bölme kaybı payı
T, h, gneed = best
print(f'besleme sıklığı {T} gün · göz ihtiyacı {gneed:.1f} / {NG*LV}')

pos = [dict(no=g['no'], yuz=g['yuz'], kat=k, cap=1.0) for g in GOZ for k in range(1, LV+1)]
def ok(k, hv): return k in (1, 2) if hv >= HEAVY else True
def score(p, hv, cls):
    k = p['kat']; e = ({2: 0.0, 1: 0.6}[k] if hv >= HEAVY else ERG[k] + (1.0 if (hv >= MID and k == 5) else 0))
    # A ürünleri döngü başı/sonuna (giriş-çıkış), C ürünleri döngü ortasına
    m = min(p['no']-1, NG-p['no'])/(NG/2)
    pp = m if cls == 'A' else (0.5*m if cls == 'B' else (1-m))
    return e*3.0 + pp*1.2
g = h[h.yer == 'hücre gözü'].copy(); g['dens'] = g.toplama_satiri/g.goz; g['heavy'] = g.hacim >= HEAVY
rows = {}
for i, x in g.sort_values(['heavy', 'dens'], ascending=[False, False]).iterrows():
    cand = sorted([p for p in pos if p['cap'] > 1e-6 and ok(p['kat'], x.hacim)], key=lambda p: score(p, x.hacim, x[A]))
    left = x.goz; plan = []
    for p in cand:
        if left <= 1e-9: break
        t = min(p['cap'], left); left -= t; plan.append((p, t))
    if left > 1e-6: raise SystemExit(f'SIĞMADI {x.urun_adi}')
    for p, t in plan:
        p['cap'] = round(p['cap']-t, 4); p.setdefault('items', []).append([x.urun_adi+' '+(str(x.varyant) if x.varyant == x.varyant else ''), x[A], round(t, 3), str(x.sku)])
    f = plan[0][0]
    rows[i] = (f['no'], f['yuz'], f['kat'], ', '.join(f"{p['yuz']}{p['no']:02d}-K{p['kat']}" for p, t in plan))
S = pd.DataFrame.from_dict(rows, orient='index', columns=['goz_no', 'yuz', 'kat', 'lokasyonlar'])
h = h.join(S); h.to_pickle('hucre_slotted.pkl')
cells = [dict(no=p['no'], yuz=p['yuz'], k=p['kat'], fill=round(1-p['cap'], 3), items=p.get('items', [])) for p in pos]
json.dump(cells, open('hucre_cells.json', 'w'), ensure_ascii=False)
sat = {k: 0.0 for k in range(1, 6)}
for c in cells:
    for a, b, t, s in c['items']:
        r = h[h.sku.astype(str) == s].iloc[0]; sat[c['k']] += r.toplama_satiri*t/r.goz
TS = sum(sat.values()); kd = {k: round(v/TS, 3) for k, v in sat.items()}
oz = dict(T=T, goz_ihtiyac=round(gneed, 1), goz_kap=NG*LV, sku_hucre=int((h.yer == 'hücre gözü').sum()), sku_kampanya=int((h.yer != 'hücre gözü').sum()),
          abc=h[h.yer == 'hücre gözü'][A].value_counts().to_dict(), kat_satir=kd, bos_goz=round(sum(p['cap'] for p in pos), 2),
          besleme_kalem_gun=round(2*int((h.yer == 'hücre gözü').sum())/T))
json.dump(oz, open('hucre_ozet.json', 'w'), ensure_ascii=False); print(oz)
print(h[h.yer != 'hücre gözü'][['urun_adi', 'varyant', 'goz']])
