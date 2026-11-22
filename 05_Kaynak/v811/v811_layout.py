# v8.11 (21.11.2026): e-ticaret bandı (H1, paketleme, H2, HP) 17,03 m doğuya (1 kolon aksı: 116,12 → 133,15);
# duvarın doğusunda kampanya + koli/dolgu + boş araba birleşik alanı; VAS 5–6 eski kampanya alanına dikey; saçak ve K4 yeniden.
import json, copy
S = 17.03
L = json.load(open('out/layout_v810.json'))
sx = lambda v: round(v+S, 3)
SHIFT_Z = {'h1','h2','paket','konv','h_guney1','h_guney2','hp_kor1','hp_kor2','hp_hat','hp_fatura','hp_cikis'}
Z = []
for z in L['Z']:
    z = dict(z)
    if z['id'] in SHIFT_Z: z['x0'], z['x1'] = sx(z['x0']), sx(z['x1'])
    if z['id'] == 'konv': z['n'] = 'Konveyör K1 → güney kapı X 139,0 → X 140,1 saptırıcı → K4'
    if z['id'] == 'hp_cikis': z['n'] = 'HP çıkış yolu → güney kapı X 156,0'
    if z['id'] == 'kor2': z['x1'] = 168.5
    if z['id'] == 'rezerv': z['x0'] = 168.9; z['n'] = 'KALAN ALAN / REZERV · v8.11: e-ticaret 17 m doğuya kaydı (−262 m²)'
    if z['id'] in ('et_kamp', 'kit', 'sacak', 'sorter', 'sorter2', 'ayirma', 'ayirma2', 'k_hj', 'k_ty', 'k_yk', 'serit'): continue
    Z.append(z)
def z(i,k,n,x0,y0,x1,y1): Z.append(dict(id=i,k=k,n=n,x0=x0,y0=y0,x1=x1,y1=y1))
# duvarın doğusu: kampanya (X 100,2–115,6) · kolon 115,82–116,42 boşlukta · koli/dolgu (X 116,6–122,3)
z('et_kamp','buffer','E-TİCARET KAMPANYA · lansman palet yüzü + rezerv · boş araba buradan',100.2,49.0,115.6,63.9)
z('kit','hp','Koli · dolgu · paketlemeye parti besleme',116.6,49.0,122.3,63.9)
# eski kampanya alanı → VAS 5–6 (dikey) + transpalet koridoru
z('vas56_kor','aisle','VAS 5–6 transpalet koridoru 2,2 m',90.9,49.0,93.1,63.9)
z('vas56_tamp','buffer','VAS 5–6 giriş/çıkış tamponu',85.0,62.2,98.8,63.9)
# eski VAS 5–6 yeri boşalır
z('serbest2','reserve','SERBEST · eski VAS 5–6 yeri · VAS 7–8 olası',70.6,49.0,81.7,61.0)
# saçak + kargo: K1 X 140,13 → güney kapı 139,0; HepsiJet batıda, Trendyol + Yurtiçi doğuda HP yanında
z('sacak','canopy','DIŞ ALAN · ÜSTÜ KAPALI SAÇAK · Y 64,7–71,0 · v8.11: X 167,5\'e uzar',100.2,64.7,167.5,71.0)
z('sorter','conv','K4-batı ← HepsiJet',127.0,65.0,140.13,65.7)
z('sorter2','conv','K4-doğu → Trendyol + Yurtiçi',140.13,65.0,156.0,65.7)
z('ayirma','conv','Batı masası · HepsiJet',121.0,65.0,127.0,65.7)
z('ayirma2','conv','Doğu masası · Trendyol + Yurtiçi',156.0,65.0,162.0,65.7)
z('k_hj','cargo','HepsiJet · %65,6 · batı masası',100.2,65.8,139.8,71.0)
z('k_ty','cargo','Trendyol · %30,7 · doğu masası + HP',140.1,65.8,163.5,71.0)
z('k_yk','cargo','Yurtiçi · %3,4',163.8,65.8,167.5,71.0)
z('serit','dock','Kargo aracı yanaşma şeridi ≈3,6 m · mevcut otopark taşınmalı',100.2,71.0,167.5,74.6)
L['Z'] = Z
for h in L['HUCRE']:
    h['x0'], h['x1'] = sx(h['x0']), sx(h['x1'])
    a = h['ada']; h['ada'] = [sx(a[0]), a[1], sx(a[2]), a[3]]
for p in L['PST']: p['x'] = sx(p['x'])
L['HPR'] = [[n, sx(x0), y0, sx(x1), y1, k] for n, x0, y0, x1, y1, k in L['HPR']]
L['VAS'] = L['VAS'][:4] + [[85.5, 50.0, 90.9, 62.0], [93.1, 50.0, 98.5, 62.0]]
# kampanya palet sıraları (yerde, 1,2 × 0,8): duvar tarafı tek sıra, ortada çift sıra, doğuda tek sıra; aralarda 3,0 m koridor
L['KAMP_PAL'] = [[100.4, 49.4, 101.6, 63.6], [104.6, 49.4, 107.0, 63.6], [110.0, 49.4, 111.2, 63.6]]
L['KAMP_PAL_N'] = 18*4
B = L['BAR']; B['b'] = [168.5, 48.3]
B['gates'] = [[60, 3.5], [79.3, 3.5], [91.9, 3.5], [105.6, 3.5], [113.4, 3.0], [128.6, 3.5], [151.6, 3.5], [163.0, 3.5]]
L['RES_X'] = 168.9
F = []
for f in L['FLOW']:
    f = copy.deepcopy(f)
    if f['f'] in ('HP', 'ET'): f['p'] = [[sx(x), y] for x, y in f['p']]
    if f['t'].startswith('H6'): f['p'] = [[sx(149.6), 64.0], [156.0, 64.0], [156.0, 67.6]]; f['t'] = 'H6 → güney kapı 156 → kafes (TY/YK yanında, HJ araba)'
    if f['t'].startswith('E3'): f['p'] = [[140.13, 51.0], [140.13, 65.35], [127.4, 65.35]]; f['t'] = 'E3 K1 → kapı 139 → saptırıcı → K4-batı (HepsiJet)'
    if f['t'].startswith('E4'): f['p'] = [[140.6, 65.35], [155.6, 65.35]]
    if f['t'].startswith('E2'): f['t'] = 'E2 18 gözlü araba → paket istasyonu'
    F.append(f)
F.insert(0, dict(f='ET', c='teal', p=[[113.4, 50.2], [113.4, 62.4], [133.0, 62.4], [135.0, 62.4], [135.0, 56.4], [134.2, 56.4]], t='E0 boş araba + lansman (kampanya) → H1 girişi'))
F.insert(1, dict(f='ET', c='teal', p=[[105.6, 44.2], [105.6, 46.4], [105.6, 49.6]], t='E5 lansman rezervi → kampanya (ana koridordan)'))
F.append(dict(f='VAS', c='blue', p=[[91.9, 44.2], [91.9, 46.4], [92.0, 50.4]], t='V6 VAS 5–6 girdi (ana koridordan)'))
L['FLOW'] = F
L['MARK'] = [m if m[0] != 'H2' else ['H2', sx(m[1]), m[2], m[3]] for m in L['MARK']]
L['V811'] = dict(shift=S, not_='e-ticaret bandı 1 kolon aksı doğuya; kampanya+koli duvarın doğusunda; VAS 5–6 eski kampanya alanında')
json.dump(L, open('out/layout.json', 'w'), ensure_ascii=False)
print('ok', [ (h['ad'],h['x0'],h['x1'],h['ada']) for h in L['HUCRE']])
