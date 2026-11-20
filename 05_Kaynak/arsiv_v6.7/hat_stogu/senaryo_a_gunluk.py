# v6.5 senaryo: ilk N A ürünü (toplama satırına göre) her gün beslenir, kalanı 2 günde bir.
# Soru: kat 1'i toplama gözü olmaktan çıkarmak (yalnız aynı ürünün yedek stoğu / boş) için N kaç olmalı, besleme yükü ne olur?
import pandas as pd, numpy as np, math, json, copy
import importlib.util
spec = importlib.util.spec_from_file_location('sv', 'slot_v65.py'); sv = importlib.util.module_from_spec(spec); spec.loader.exec_module(sv)
d = pd.read_pickle('df.pkl'); A = 'ABC_satir(toplama_sikligi)'
GV = 1.78*0.88*0.50*0.65; SAFE = 1.2; NH = 2; GUN = 304
base = d[(d.grup == 'hat') & (d[A].isin(['A', 'B'])) & (d.d_top > 0)].copy().sort_values('toplama_satiri', ascending=False)
base['lansman'] = base.urun_adi.str.contains('LANSMAN') & (base.XYZ == 'Z')
C_GOZ = 5.0     # E1'e düşen C (2026), en kötü hat
def build(N):
    h = base.copy(); rank = (h[A] == 'A').cumsum()
    h['T'] = np.where((h[A] == 'A') & (rank <= N), 1, 2)
    h['stok_adet'] = np.ceil(h.d_tasarim/NH*h['T']*SAFE)
    h['stok_m3'] = h.stok_adet*h.hacim/1e6
    h['bolme'] = np.where(h.hacim <= 300, 8, 4)
    h['slot'] = np.maximum(1, np.ceil(h.stok_m3/(GV/h.bolme))); h['goz'] = h.slot/h.bolme
    h['yer'] = np.where(h.lansman & (h.goz > 2.0), 'kampanya lokasyonu (palet)', 'göz rafı')
    return h
res = []
nA = int((base[A] == 'A').sum())
for N in [0, 10, 20, 30, 40, 50, 60, 70, 80, nA]:
    h = build(N); g = h[h.yer == 'göz rafı']
    need = g.goz.sum() + C_GOZ
    feeds = (g['T'] == 1).sum() + (g['T'] == 2).sum()/2           # hat başı günlük besleme kalemi (SKU)
    res.append(dict(N=N, goz=round(need, 2), kat1_serbest=bool(need <= 72), besleme_kalem=round(feeds, 1)))
def dist_for(N, kats):
    h = build(N); pos = [dict(taraf=s, goz=g, kat=k, cap=1.0) for s in ('Batı', 'Doğu') for g in range(1, 10) for k in kats]
    sv.place(h, pos); sat = {k: 0.0 for k in range(1, 6)}
    key = (h.urun_adi+' '+h.varyant.fillna('').astype(str)).str.strip()
    for p in pos:
        for a, b, t in p.get('items', []):
            x = h[key == a.strip()].iloc[0]; sat[p['kat']] += x.toplama_satiri*t/x.goz
    T = sum(sat.values()); k1 = round(sum(1-p['cap'] for p in pos if p['kat'] == 1), 2)
    return {k: round(v/T, 3) for k, v in sat.items()}, k1
for r in res:
    try: dd, k1 = dist_for(r['N'], range(1, 6)); r.update({f'kat{k}': v for k, v in dd.items()}); r['kat1_goz'] = k1
    except SystemExit: pass
R = pd.DataFrame(res); print(R.to_string())
# kat 1 serbest kalan en küçük N: yerleşimi kat 2–5'te yap
Nmin = int(R[R.kat1_serbest].N.min())
h = build(Nmin)
h['taraf'] = None
pos = [dict(taraf=s, goz=g, kat=k, cap=1.0) for s in ('Batı', 'Doğu') for g in range(1, 10) for k in range(2, 6)]
rows = sv.place(h, pos)
sat = {k: 0.0 for k in range(1, 6)}
for p in pos:
    for a, b, t in p.get('items', []):
        x = h[(h.urun_adi+' '+h.varyant.fillna('').astype(str)).str.strip() == a.strip()].iloc[0]
        sat[p['kat']] += x.toplama_satiri*t/x.goz
T = sum(sat.values()); dist = {k: round(v/T, 3) for k, v in sat.items()}
free = round(sum(p['cap'] for p in pos), 2)
print('Nmin', Nmin, 'kat dağılımı', dist, 'kat2–5 boş', free)
# kat 1 = aynı ürünün yedek stoğu: kat 2–3'teki en yoğun ürünlerin altına 1 günlük ek stok (besleme kaçarsa tampon)
json.dump(dict(tablo=res, Nmin=Nmin, dist=dist, bos_k25=free, nA=nA,
               gunluk=[x for x in h[(h['T'] == 1)].apply(lambda x: x.urun_adi+' '+(str(x.varyant) if x.varyant == x.varyant else ''), axis=1)]),
          open('/home/claude/senaryo_a_gunluk.json', 'w'), ensure_ascii=False)
