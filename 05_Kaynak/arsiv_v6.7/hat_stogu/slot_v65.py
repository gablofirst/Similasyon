# v6.5 — ergonomik hat yerleşimi (17.11.2026, personel geri bildirimi: A ürünleri en alt katta, eğilip kalkma)
# Kural: göz başına toplama satırı (yoğunluk) yüksek olan ürün altın bölgeye (kat 3, kat 2 = 50–150 cm),
# sonra kat 4, sonra kat 1, en son kat 5. 5,5 L kavanoz (≥ 5.000 cm³) yalnız kat 2 / kat 1 (bel hizası öncelikli).
# 1,5 L kutu (≥ 2.400 cm³) kat 5'e ancak yer kalmazsa (ek ceza). Bir SKU tek tarafta. Göz 1 = konveyör ucu.
# Çalıştırma: size2.py → slot_v65.py [T_A_GUNLUK_N] → c_slot.py → xl.py
import pandas as pd, numpy as np, math, json, sys
R = pd.read_pickle('runs.pkl')
r = [x for x in R if x['T'] == 2 and x['lv'] == 5 and x['g'] == 1.0][0]
h = r['h'].copy(); side = r['side']; LV = 5
GV = 1.78*0.88*0.50*0.65
ERG = {3: 0.0, 2: 0.2, 4: 1.0, 1: 2.0, 5: 3.0}   # kat cezası (sıra: 3, 2, 4, 1, 5)
W_ERG, W_GOZ = 3.0, 0.25                          # kat 3 göz 9 (2,0) < kat 4 göz 1 (3,0): ergonomi önce
HEAVY, MID = 5000, 2400
ABC = 'ABC_satir(toplama_sikligi)'

def allowed(k, hv):
    if hv >= HEAVY: return k in (1, 2)
    return True
def score(p, hv):
    k = p['kat']
    e = {2: 0.0, 1: 0.6}[k] if hv >= HEAVY else ERG[k] + (1.0 if (hv >= MID and k == 5) else 0)
    return e*W_ERG + (p['goz']-1)*W_GOZ

def place(h, pos):
    g = h[h.yer == 'göz rafı'].copy()
    g['dens'] = g.toplama_satiri/g.goz
    g['heavy'] = g.hacim >= HEAVY
    rows = {}
    for i, x in g.sort_values(['heavy', 'dens'], ascending=[False, False]).iterrows():
        best = None
        for sd in (('Batı',), ('Doğu',), ('Batı', 'Doğu')):   # önce tek taraf; sığmazsa iki tarafa bölünür
            if best is not None and len(sd) == 2: break
            cand = sorted([p for p in pos if p['cap'] > 1e-6 and p['taraf'] in sd and allowed(p['kat'], x.hacim)], key=lambda p: score(p, x.hacim))
            need = x.goz; plan = []; sc = 0
            for p in cand:
                if need <= 1e-9: break
                t = min(p['cap'], need); need -= t; plan.append((p, t)); sc += score(p, x.hacim)*t
            if need <= 1e-9 and (best is None or sc < best[0]): best = (sc, plan)
        if best is None: raise SystemExit(f'SIĞMADI {x.urun_adi} {x.varyant}')
        for p, t in best[1]:
            p['cap'] -= t; p.setdefault('items', []).append([x.urun_adi+' '+(str(x.varyant) if x.varyant == x.varyant else ''), x[ABC], round(t, 3)])
        f = best[1][0][0]
        rows[i] = (f['taraf'], f['goz'], f['kat'], ', '.join(f"{p['taraf'][0]}{p['goz']}-K{p['kat']}" for p, t in best[1]))
    return rows

if __name__ == '__main__':
    pos = [dict(taraf=s, goz=g, kat=k, cap=1.0) for s in ('Batı', 'Doğu') for g in range(1, side+1) for k in range(1, LV+1)]
    rows = place(h, pos)
    S = pd.DataFrame.from_dict(rows, orient='index', columns=['taraf', 'goz_no', 'kat', 'lokasyonlar'])
    h = h.join(S)
    h.to_pickle('slotted.pkl')
    cells = [dict(s=p['taraf'][0], g=p['goz'], k=p['kat'], fill=round(1-p['cap'], 3), items=p.get('items', [])) for p in pos]
    json.dump(cells, open('cells.json', 'w'), ensure_ascii=False)
    free = sum(p['cap'] for p in pos); print('kapasite', len(pos), 'boş göz', round(free, 2))
    # kat dağılımı
    sat = {k: 0.0 for k in range(1, 6)}; nm = {(x.urun_adi+' '+(str(x.varyant) if x.varyant == x.varyant else '')): x for _, x in h.iterrows()}
    for c in cells:
        for a, b, t in c['items']: sat[c['k']] += nm[a].toplama_satiri*t/nm[a].goz
    T = sum(sat.values()); print({k: round(v/T, 3) for k, v in sat.items()})
