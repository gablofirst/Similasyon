# Kazan WMS lokasyon ana verisi + ürün-lokasyon ataması · v6.6 (e-ticaret 2 kare hücre, hucre_slot.py; drive-in 4 kat × 5 derinlik, ADEYA teyidi) · 19.11.2026
# Çalıştırma: python3 lok.py <hat_stogu klasörü (df.pkl, hucre_cells.json, hucre_slotted.pkl, hucre_ozet.json)> <layout.json> <B2B_yuz_v6.4.xlsx> <çıktı klasörü>
import sys, os, json, math, copy, re
import pandas as pd, numpy as np

HS, LAYJ, B2BX, OUT = sys.argv[1:5]
L = json.load(open(LAYJ))

# ---------------- PARAMETRELER (ADEYA / ERP teyidi gelince burası değişir) ----------------
GOZ = 2.82            # back-to-back göz adımı (m)
KAT_BB = 4            # back-to-back kat (1 = zemin)
POZ = 'ABC'           # göz başına 3 palet
TUNEL_GOZ = 5         # her sırada güneyden 5. göz tünel: kat 1–2 yok
DI_KAT, DI_DER = 4, 5 # drive-in: zemin + 3 kat = 4 kat × 5 derinlik = 20 palet/şerit (ADEYA, İhsan 18.11)
HAT_KAT = 5
REZ_GUN = 14          # rezerv kapsama (gün): başlangıç yerleşimi için; ERP stoğu gelince gerçek stokla değiştir
PAL_M3 = 1.20*0.80*1.50*0.80   # palet başı net ürün hacmi (m³): 120×80×150, %80 koli/istif verimi
BAR_PAL = 12*875      # bar: 12'li display, 875 display/palet (v6.4 varsayımı)
DI_ESIK = 8           # rezerv ihtiyacı ≥ 8 palet olan SKU drive-in'e (tek SKU / şerit)
KARMA_ESIK = 0.34     # 1/3 paletten küçük rezerv: karma palet (aynı pozisyonda en çok 3 SKU)

ROWS = L['ADEYA_ROWS']            # 12 ADEYA sırası [x0,y0,x1,y1]
GOZ_ORJ = [9,10,10,9,10,10,9,7,7,6,7,7]   # çizimden: sıra boyu / 2,82 m
EXT_N = 3                          # 8–12. sıra uzatması (Y 35,8 → 44,2), güney uca 3 göz
R13 = L['ROWS'][0]                 # 13. sıra, tek yüz (batı)

LOC = []   # lokasyon ana verisi
def add(**k): LOC.append(k)

# ---------------- B · BACK-TO-BACK ----------------
for s in range(1, 14):
    if s <= 12:
        x0, y0, x1, y1 = ROWS[s-1]
        ext = EXT_N if s >= 8 else 0
        ng = GOZ_ORJ[s-1] + ext
        ysouth = 44.2 if s >= 8 else y1
        faces = 'BD'
    else:
        x0, y0, x1, y1 = R13; ng = 10; ysouth = y1; faces = 'B'; ext = 0
    for f in faces:
        X = round(x0+0.6 if f == 'B' else x1-0.6, 2)
        for g in range(1, ng+1):
            if s >= 8 and s <= 12 and g > ext:      # uzatma bitti → ADEYA'nın orijinal gözleri Y 35,8'den kuzeye
                ys = (35.8 if s != 10 else 34.89) - (g-ext-0.5)*GOZ
            else:
                ys = ysouth - (g-0.5)*GOZ
            for k in range(1, KAT_BB+1):
                if g == TUNEL_GOZ and k <= 2: continue
                for p in POZ:
                    add(kod=f"B{s:02d}{f}-{g:02d}-{k}{p}", bolge='B', bolge_ad='Back-to-back', blok=f"B{s:02d}",
                        sira=s, yuz={'B':'Batı','D':'Doğu'}[f], goz=g, kat=k, poz=p,
                        x=X, y=round(ys + {'A':-0.9,'B':0,'C':0.9}[p], 2),
                        kap=1, birim='palet', kaynak='uzatma' if (s>=8 and s<=12 and g<=ext) else ('13. sıra' if s==13 else 'ADEYA'))

# lokasyon tipi (v6.4 kuralları)
def bb_tip(r):
    if r['sira'] == 1 and r['kat'] == 1:
        return 'B2B-TOPLAMA' if r['goz'] <= 3 else 'B2B-ESNEK'
    return 'REZERV'
def bb_rez_bolge(r):
    s = r['sira']
    if s == 1: return 'B2B kanal rezervi'
    if s in (2, 3): return 'B2B / VAS rezervi'
    if 4 <= s <= 9: return 'E-ticaret besleme rezervi'
    return 'Genel rezerv'
for r in LOC:
    r['tip'] = bb_tip(r); r['rez_bolge'] = bb_rez_bolge(r)

# ---------------- D · DRIVE-IN ----------------
DI = sorted(L['DI'], key=lambda t: t[1])
for i, (tag, x0, y0, x1, y1) in enumerate(DI, 1):
    for k in range(1, DI_KAT+1):
        add(kod=f"D{i:02d}-{k}", bolge='D', bolge_ad='Drive-in', blok='Batı blok' if tag == 'W' else 'Orta blok',
            sira=i, yuz='', goz=None, kat=k, poz='', x=round((x0+x1)/2, 2), y=round((y0+y1)/2, 2),
            kap=DI_DER, birim='palet', kaynak='plan v6.4', tip='REZERV-BLOK', rez_bolge='Drive-in · tek SKU + tek lot / şerit')

# ---------------- H · E-TİCARET KARE HÜCRE GÖZLERİ (v6.6) ----------------
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'yerlesim')); import hucre_geo as HG
hcells = json.load(open(f"{HS}/hucre_cells.json"))
df = pd.read_pickle(f"{HS}/df.pkl"); A = 'ABC_satir(toplama_sikligi)'
slt = pd.read_pickle(f"{HS}/hucre_slotted.pkl"); HOZ = json.load(open(f"{HS}/hucre_ozet.json"))
stk = slt.set_index(slt.sku.astype(str)).stok_adet.to_dict()
BIN = []
for hc in L['HUCRE']:
    geo = {g['no']: g for g in HG.gozler(hc)}
    for cc in hcells:
        g = geo[cc['no']]; k = cc['k']
        parent = f"{hc['ad']}{cc['yuz']}-{cc['no']:02d}-{k}"
        items = [dict(ad=a, abc=b, pay=t, sku=sk) for a, b, t, sk in cc['items']]; used = sum(i['pay'] for i in items)
        if 1-used > 1e-3: items.append(dict(ad='', abc='', pay=round(1-used, 3), sku=''))
        for j, it in enumerate(items):
            kod = parent+'ABCDEFGH'[j]
            add(kod=kod, bolge='H', bolge_ad='E-ticaret hücresi', blok=hc['ad'], sira=int(hc['ad'][1]), yuz={'D': 'Dış raf', 'A': 'Ada'}[cc['yuz']], goz=cc['no'], kat=k,
                poz='ABCDEFGH'[j], x=g['x'], y=g['y'], kap=round(it['pay'], 3), birim='göz payı', kaynak=f"kenar {g['kenar']}",
                tip='HÜCRE-GÖZ' if it['sku'] else 'HÜCRE-GÖZ (boş)', rez_bolge='')
            if it['sku']: BIN.append(dict(hat=hc['ad'], kod=kod, parent=parent, sku=it['sku'], ad=it['ad'], abc=it['abc'], pay=it['pay'], kat=k, goz=cc['no'], st=stk.get(str(it['sku']))))
json.dump(hcells, open(f"{OUT}/cells_H_3d.json", 'w'), ensure_ascii=False)
# paket istasyonları (alt lokasyon, sabit)
for p in L['PST']:
    add(kod=p['id'], bolge='P', bolge_ad='Paket istasyonu', blok='Paketleme', sira=int(p['id'][1:]), yuz={'B': 'Batı', 'D': 'Doğu'}[p['taraf']], goz=None, kat=1, poz='',
        x=p['x'], y=round(p['y'], 2), kap=1, birim='istasyon', kaynak='plan v6.6', tip='PAKET-İSTASYONU', rez_bolge='')

# ---------------- K · E-TİCARET KAMPANYA LOKASYONU + diğer alanlar (zemin / sanal) ----------------
K_N = 24   # 163 m² zemin: taslak 24 palet yeri (2 × 12), sahada zemin çizgisiyle teyit
kx0, ky0, kx1, ky1 = 85.0, 48.6, 98.8, 64.3
for i in range(1, K_N+1):
    col = 0 if i <= 12 else 1
    add(kod=f"K-{i:02d}", bolge='K', bolge_ad='E-ticaret kampanya lokasyonu', blok='K', sira=None, yuz='', goz=None, kat=1, poz='',
        x=round(kx0+1.5+col*6.0, 2), y=round(ky0+0.8+((i-1) % 12)*1.25, 2), kap=1, birim='palet', kaynak='taslak',
        tip='KAMPANYA-TOPLAMA', rez_bolge='')
ALAN = [('MK-01','Mal kabul alanı (169 m²)','ALAN-KABUL',None,'X 49,2–76 / Y 16,1–22,4'),
        ('ST-01..27','Ortak sevk tamponu VAS/Bim + B2B (27 palet)','ALAN-SEVK',27,'X 49,2–57,6 / Y 22,8–34,4'),
        ('STR-01','Streç / palet kartı / WMS etiket','ALAN-SEVK',None,'X 49,2–57,6 / Y 34,8–38,8'),
        ('VS-01','VAS stoğa dönüş tamponu','ALAN-VAS',None,'X 49,2–57,6 / Y 39,2–44,2'),
        ('VG-01..20','VAS giriş / yarı mamül bekleme tamponu V2 (20 palet)','ALAN-VAS',20,'X 70,4–76 / Y 22,8–44,2'),
        ('VAS1..VAS4','VAS hatları (hat başı WIP lokasyonu)','ALAN-VAS',4,'X 58–70 / Y 22,6–44,2'),
        ('Q-IADE / Q-KAR / Q-IMHA','Kalite: iade kabul, karantina, imha','ALAN-KALITE',3,'X 49,2–70 / Y 59,5–64,3'),
        ('P01..P16','Paket istasyonu: hediye / eklenti (Pocket Shaker, tester, huni, pillbox) istasyonda','ALAN-PAKET',16,'X 121,9–124,3 / Y 49,6–64,4'),
        ('ARB-01..30','12 gözlü toplama arabası (göz = sipariş) · boş araba parkı','ALAN-ARABA',30,'Hücre güneyi + paketleme doğu şeridi'),
        ('HP-…','Hazır paket rafları (mamül 2 × 24 + koli + paketli 24 + 36 palet)','ALAN-HP',108,'X 140,6–151,4 / Y 49,4–63,5'),
        ('KIT-01','Kit / ön paketleme · koli-dolgu','ALAN-HP',None,'X 100,2–105,8 / Y 49,0–64,4'),
        ('KRG-HJ / KRG-TY / KRG-YK','Kargo kafesi çıkışı: HepsiJet, Trendyol, Yurtiçi','ALAN-KARGO',3,'Dış saçak Y 64,7–71,0')]
LOCdf = pd.DataFrame(LOC)

# ---------------- ÜRÜN TALEBİ ve PALET ----------------
b2b = pd.read_excel(B2BX, sheet_name='Atama'); b2b = b2b[b2b['Ürün'].notna() & b2b['Grup'].notna()].copy()
ERP = {'Protein Bar Tiramisu 50g': ('120100200011', 'PROTEİN BAR TEKLİ Tiramisu'),
       'Protein Bar Çikolata&Fındık 50g': ('120100200017', 'PROTEİN BAR TEKLİ Chocolate&Hazelnut'),
       'Protein Bar Birthdaycake 50g': ('120100200012', 'PROTEİN BAR TEKLİ Birthday Cake'),
       'Protein Bar Çilek 50g': ('120100200018', 'PROTEİN BAR TEKLİ Strawberry Cheesecake'),
       'Protein Bar Hindistan Cevizi 50g': ('120100200019', 'PROTEİN BAR TEKLİ Coconut'),
       'Protein Bar Cookie&Cream 50g': ('120100200048', 'PROTEİN BAR TEKLİ Cookie&Cream'),
       'Protein Bar Salted Caramel 50g': ('120100200059', 'PROTEİN BAR TEKLİ Salted Caramel'),
       'Protein Bar Çikolata 50g': ('120100200010', 'PROTEİN BAR TEKLİ Çikolata'),
       'Protein Bar Muz 50g': ('120100200015', 'PROTEİN BAR TEKLİ Muz'),
       'Protein Bar Batman 50g': ('120100200052', 'PROTEİN BAR TEKLİ BATMAN Chocolate & Banana'),
       'Whey Protein Bisküvi 200g': ('120100100037', 'WHEY PROTEIN Bisküvi 200 g'),
       'Whey Protein Çikolata 200g': ('120100100057', 'WHEY PROTEIN Çikolata 200 g'),
       'Collagen Ahududu 150g': ('120400100022', 'COLLAGEN Ahududu 150g'),
       'Creatine Aromasız 120g': ('120200100017', 'CREATINE Aromasız 120g'),
       'Fıstık Ezmesi 330g': ('10100200003', 'FISTIK EZMESİ 330 g'),
       'Fıstık Ezmesi Parçacıklı 330g': ('120500200004', 'FISTIK EZMESİ PARÇACIKLI 330g'),
       'Hindistan Cevizi Yağı 300ml': ('120500400001', 'HİNDİSTAN CEVİZİ YAĞI 300 ML')}
IKAS = {'Creatine Aromasız 120g': '6090019', 'Hindistan Cevizi Yağı 300ml': '6000544'}
VOL_B2B = {'Whey Protein Bisküvi 200g': 1589, 'Whey Protein Çikolata 200g': 1589, 'Collagen Ahududu 150g': 900,
           'Creatine Aromasız 120g': 729, 'Fıstık Ezmesi 330g': 800, 'Fıstık Ezmesi Parçacıklı 330g': 800, 'Hindistan Cevizi Yağı 300ml': 908}
def pal_adet(vol_cm3): return max(1, int(PAL_M3*1e6/vol_cm3)) if vol_cm3 and vol_cm3 > 0 else BAR_PAL

# e-ticaret SKU havuzu: hat (A/B/C), hediye masası, kit/hazır paket (x N adet satışlar ana SKU'da)
eco = df[(df.d_top > 0) & (df.grup.isin(['hat', 'hediye_masa', 'kit_HP']))].copy()
eco['urun'] = eco.urun_adi+' '+eco.varyant.fillna('').astype(str)
P = []
for i, x in eco.iterrows():
    P.append(dict(key=x.sku, ikas=x.sku, erp='', urun=x.urun.strip(), kanal='E-ticaret', abc=x[A], grup=x.grup,
                  d_eco=x.d_top, d_b2b=0.0, hacim=x.hacim if x.hacim == x.hacim and x.hacim > 0 else 1500, satir=x.toplama_satiri))
Pdf = pd.DataFrame(P).set_index('key')
for _, r in b2b.iterrows():
    nm = r['Ürün']; erp, erpad = ERP[nm]; ik = IKAS.get(nm)
    if ik and ik in Pdf.index:
        Pdf.loc[ik, 'd_b2b'] = r['Adet/gün']; Pdf.loc[ik, 'erp'] = erp; Pdf.loc[ik, 'kanal'] = 'E-ticaret + B2B'
    else:
        Pdf.loc[erp] = dict(ikas='', erp=erp, urun=erpad, kanal='B2B', abc='B2B', grup='b2b', d_eco=0.0, d_b2b=r['Adet/gün'],
                            hacim=VOL_B2B.get(nm, 0), satir=r['Satır'])
Pdf = Pdf[~((Pdf.grup == 'kit_HP') & ((Pdf.d_eco+Pdf.d_b2b)*REZ_GUN/[pal_adet(h) for h in Pdf.hacim] < 0.25))].copy()   # küçük kit/paket: HP rafında, rezerv açılmaz
Pdf['pal_adet'] = [BAR_PAL if 'BAR TEKLİ' in u else pal_adet(h) for u, h in zip(Pdf.urun, Pdf.hacim)]
Pdf['d_top'] = Pdf.d_eco+Pdf.d_b2b
Pdf['rez_palet'] = Pdf.d_top*REZ_GUN/Pdf.pal_adet
Pdf['rez_yer'] = np.where(Pdf.rez_palet >= DI_ESIK, 0, np.ceil(Pdf.rez_palet.clip(lower=1e-9)))
Pdf['karma'] = Pdf.rez_palet < KARMA_ESIK
Pdf['di_serit'] = np.where(Pdf.rez_palet >= DI_ESIK, np.ceil(Pdf.rez_palet/(DI_KAT*DI_DER)), 0)

# ---------------- B2B TOPLAMA YÜZÜ (v6.4 kabul) ----------------
def old2new(s):   # S1-B-01-A + B → [B01B-01-1A, B01B-01-1B]
    m = re.match(r'S1-([BD])-(\d+)-([ABC])(?: \+ ([ABC]))?', s)
    if not m: return []
    f, g, p1, p2 = m.groups(); out = [f"B01{f}-{int(g):02d}-1{p1}"]
    if p2: out.append(f"B01{f}-{int(g):02d}-1{p2}")
    return out
PICK = {}   # key -> [lokasyon]
B2BROW = []
for _, r in b2b.iterrows():
    nm = r['Ürün']; erp, _ = ERP[nm]; key = IKAS.get(nm) if IKAS.get(nm) in Pdf.index else erp
    locs = old2new(str(r['Lokasyon'])); PICK[key] = locs
    B2BROW.append(dict(key=key, urun_kpi=nm, satir_gun=r['Satır/gün'], adet_gun=r['Adet/gün'], pal_gun=r['Palet/gün (toplam)'], yuz_pal_gun=r['Palet/gün (yüzden)'], toplama=locs))

# ---------------- REZERV ATAMASI ----------------
occ = {}   # lokasyon → [(key, pay)]
loc_bb = LOCdf[(LOCdf.bolge == 'B') & (LOCdf.tip == 'REZERV')].copy()
def cand(zones, ref, prefer_low=True):
    # göz-yüz grupları yakından uzağa; grup içinde kat 1→4, poz A→C (bir SKU'nun paletleri yan yana / üst üste kalır)
    z = loc_bb[loc_bb.rez_bolge.isin(zones)].copy()
    g = z.groupby(['sira', 'yuz', 'goz']).agg(gx=('x', 'mean'), gy=('y', 'mean'))
    g['gd'] = (g.gx-ref[0]).abs()+(g.gy-ref[1]).abs()
    z = z.join(g['gd'], on=['sira', 'yuz', 'goz'])
    return z.sort_values(['gd', 'sira', 'yuz', 'goz', 'kat', 'poz']).kod.tolist()
REF_E = (123.1, 45.0)   # H1/H2 besleme girişleri arası, ana koridor
REF_B = (83.2, 44.3)    # 1. sıra güney uç (B2B yüzü)
REZ = {}                # key -> [lok]
order = Pdf.sort_values(['d_top', 'satir'], ascending=False)
# 1) B2B kanal ürünleri: önce kendi toplama gözünün üstü (aynı göz/yüz, kat 2–4), sonra 1. sıra, sonra 2–3. sıra
for key, x in order[order.d_b2b >= order.d_eco].iterrows():
    if x.rez_yer == 0: continue
    above = []
    for l in PICK.get(key, []):
        b, gz = l.split('-')[0], l.split('-')[1]
        above += [f"{b}-{gz}-{k}{p}" for k in (2, 3, 4) for p in POZ]
    pool = above + cand(['B2B kanal rezervi'], REF_B) + cand(['B2B / VAS rezervi'], REF_B)
    got = []
    for l in pool:
        if len(got) >= x.rez_yer: break
        if l in occ or l in got: continue
        got.append(l)
    for l in got: occ[l] = [(key, 1.0)]
    REZ[key] = got
# 2) E-ticaret ürünleri: besleme rezervinde, satır sırasıyla en yakın + alçak pozisyon; karma palet küçükleri birleştirir
pool = cand(['E-ticaret besleme rezervi'], REF_E) + cand(['Genel rezerv'], REF_E)
pi = 0; karma_open = None
for key, x in order[order.d_b2b < order.d_eco].sort_values('satir', ascending=False).iterrows():
    if x.rez_yer == 0: continue
    if x.karma:
        if karma_open and len(occ[karma_open]) < 3:
            occ[karma_open].append((key, round(x.rez_palet, 3))); REZ[key] = [karma_open]; continue
    got = []
    while len(got) < x.rez_yer:
        l = pool[pi]; pi += 1
        if l in occ: continue
        got.append(l)
    for l in got: occ[l] = [(key, 1.0 if not x.karma else round(x.rez_palet, 3))]
    if x.karma: karma_open = got[0]
    REZ[key] = got
# 3) Drive-in: ≥ 8 palet ihtiyacı olan SKU, tek SKU / şerit. B2B baskın → batı blok (rampaya yakın), e-ticaret → orta blok
DIL = LOCdf[LOCdf.bolge == 'D'][['kod', 'blok', 'sira', 'x']].copy()
lane_free = {'Batı blok': sorted(DIL[DIL.blok == 'Batı blok'].sira.unique(), key=lambda s: -s),   # doğu uç (B2B'ye yakın) önce
             'Orta blok': sorted(DIL[DIL.blok == 'Orta blok'].sira.unique())}                    # batı uç önce
DIREZ = {}
for key, x in order[order.di_serit > 0].iterrows():
    blk = 'Batı blok' if x.d_b2b >= x.d_eco else 'Orta blok'
    lanes = [lane_free[blk].pop(0) for _ in range(int(x.di_serit))]
    DIREZ[key] = lanes
    for s in lanes:
        for k in range(1, DI_KAT+1): occ[f"D{int(s):02d}-{k}"] = [(key, 1.0)]

# 4) Lansman / Z: kampanya lokasyonundan palet önünden toplanır (hat gözü açılmaz)
KPICK = {}; ki = 1
for _, x in slt[slt.yer != 'hücre gözü'].sort_values('toplama_satiri', ascending=False).iterrows():
    n = max(1, math.ceil(x.d_tasarim*2*1.2*x.hacim/1e6/1.0)); KPICK[x.sku] = [f"K-{ki+j:02d}" for j in range(n)]; ki += n
pk_k = {l: k for k, ls in KPICK.items() for l in ls}

# ---------------- ÇIKTI TABLOLARI ----------------
# lokasyon ana verisine atanan SKU
def occ_txt(l):
    v = occ.get(l);
    if not v: return '', ''
    return ', '.join(str(k) for k, _ in v), ' | '.join(Pdf.loc[k, 'urun'] for k, _ in v)
binmap = {b['kod']: b for b in BIN}
pk = {l: k for k, ls in PICK.items() for l in ls}
s1, s2 = [], []
for _, r in LOCdf.iterrows():
    if r.kod in binmap: s1.append(binmap[r.kod]['sku']); s2.append(binmap[r.kod]['ad'])
    elif r.kod in pk: s1.append(pk[r.kod]); s2.append(Pdf.loc[pk[r.kod], 'urun'])
    elif r.kod in pk_k: s1.append(pk_k[r.kod]); s2.append(Pdf.loc[pk_k[r.kod], 'urun'])
    else: a, b = occ_txt(r.kod); s1.append(a); s2.append(b)
LOCdf['sku'] = s1; LOCdf['urun'] = s2
# toplama sırası
def seq(r):
    if r.tip == 'B2B-TOPLAMA' or r.tip == 'B2B-ESNEK':
        return (0 if r.yuz == 'Batı' else 1)*100 + (r.goz if r.yuz == 'Batı' else 20-r.goz)*3 + 'ABC'.index(r.poz)
    if r.bolge == 'H': return int(r.goz)*10 + r.kat   # döngü sırası: göz 01 giriş
    return None
LOCdf['toplama_sira'] = LOCdf.apply(seq, axis=1)
LOCdf['durum'] = 'Aktif'

pd.to_pickle(dict(ALAN=ALAN, KPICK=KPICK, LOC=LOCdf, P=Pdf, BIN=pd.DataFrame(BIN), REZ=REZ, PICK=PICK, DIREZ=DIREZ, B2BROW=B2BROW, occ=occ,
                  par=dict(GOZ=GOZ, KAT_BB=KAT_BB, TUNEL_GOZ=TUNEL_GOZ, DI_KAT=DI_KAT, DI_DER=DI_DER, REZ_GUN=REZ_GUN, PAL_M3=PAL_M3,
                           BAR_PAL=BAR_PAL, DI_ESIK=DI_ESIK, KARMA_ESIK=KARMA_ESIK, GOZ_ORJ=GOZ_ORJ, HT=HOZ['T'])), f"{OUT}/wms.pkl")
print(LOCdf.groupby(['bolge', 'tip']).agg(n=('kod', 'size'), kap=('kap', 'sum')))
print('B palet', LOCdf[LOCdf.bolge=='B'].kap.sum(), 'D palet', LOCdf[LOCdf.bolge=='D'].kap.sum())
print('SKU', len(Pdf), 'rezerv yer', int(Pdf.rez_yer.sum()), 'karma', int(Pdf.karma.sum()), 'drive-in SKU', len(DIREZ), 'şerit', sum(len(v) for v in DIREZ.values()))
print('kullanılan rezerv B', sum(1 for l in occ if l.startswith('B')), 'D', sum(1 for l in occ if l.startswith('D')))
print('dup kod', LOCdf.kod.duplicated().sum())
