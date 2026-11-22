# v8.11 (21.11.2026): e-ticaret bandı 17,03 m doğuya, kampanya + koli duvarın doğusunda, VAS 5–6 eski kampanya alanında, saçak X 167,5 · v6.6: e-ticaret 2 kare hücre + paketleme + HP doğuda (hucre_geo.py) · v6.5 DXF — okunaklı etiketler (Arial, Türkçe karakter), kutuya sığan MTEXT, ADEYA raf referans katmanı
# python3 dxfout_v65.py <layout.json> <çıktı.dxf> [oksuz]
import json, math, sys, os, ezdxf
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import hucre_geo as HG
from ezdxf.enums import MTextEntityAlignment
LJ, OUT, BASE = sys.argv[1], sys.argv[2], sys.argv[3]; OKSUZ = len(sys.argv) > 4 and sys.argv[4] == 'oksuz'
L = json.load(open(LJ))
# v7.0: as-built 20.11 DWG (cm) içine çizilir. Plan (m) → as-built (cm): kolon aksları X 48,1 = 8706, Y 35,3 = 8648
X = lambda x: 8706+(x-48.1)*100
Y = lambda y: 11530-(y-6.48)*100
from ezdxf import recover
FLAT = BASE.endswith('.pkl')
if FLAT:   # DWG yazımı için düz R2000: as-built geometri katman katman çizgi olarak
    import pickle
    doc = ezdxf.new('R2000', setup=True); doc.units = 5; msp = doc.modelspace()
    ASB = pickle.load(open(BASE, 'rb'))
    for ly, segs in ASB.items():
        if ly in ('AGAC',): continue
        lyn = 'ASB_' + ly.translate(str.maketrans('İıŞşĞğÜüÖöÇç ', 'IiSsGgUuOoCc_'))
        if lyn not in doc.layers: doc.layers.add(lyn, color=8)
        for sg in segs: msp.add_lwpolyline(sg, dxfattribs={'layer': lyn})
else:
    doc, _ = recover.readfile(BASE); msp = doc.modelspace()
if 'DASHED' not in doc.linetypes: doc.linetypes.add('DASHED', pattern=[50, 30, -20])
doc.header['$DWGCODEPAGE'] = 'ANSI_1254'
'PO_ARIAL' in doc.styles or doc.styles.add('PO_ARIAL', font='arial.ttf')
LAY = {'canopy': ('PO_SACAK', 6), 'inbound': ('PO_MAL_KABUL', 3), 'aisle': ('PO_KORIDOR', 8), 'buffer': ('PO_VAS_TAMPON', 5), 'conv': ('PO_KONVEYOR', 7),
       'dock': ('PO_SEVK', 9), 'hp': ('PO_HAZIR_PAKET', 40), 'cargo': ('PO_KARGO', 1), 'reserve': ('PO_REZERV', 8), 'cell': ('PO_ETICARET_HUCRE', 4), 'pack': ('PO_PAKETLEME', 4), 'office': ('PO_OFIS_SOSYAL', 211)}
EXTRA = [('PO_DRIVEIN_YENI', 30), ('PO_B2B_YENI', 30), ('PO_VAS_HAT', 5), ('PO_ETICARET_HAT', 4), ('PO_BARIYER', 2), ('PO_BARIYER_KAPI', 1),
         ('PO_UYARI', 1), ('PO_YAZI', 7), ('PO_HP_RAF', 42), ('PO_B2B_TOPLAMA_YUZU', 6), ('PO_B2B_ESNEK', 6), ('PO_ADEYA_RAF_REF', 253), ('PO_HUCRE_RAF', 150), ('PO_HUCRE_DONGU', 4), ('PO_KAMPANYA_PALET', 30)]
for n, c in list(LAY.values())+EXTRA:
    if n not in doc.layers: doc.layers.add(n, color=c)

def rect(layer, x0, y0, x1, y1):
    msp.add_lwpolyline([(X(x0), Y(y0)), (X(x1), Y(y0)), (X(x1), Y(y1)), (X(x0), Y(y1))], close=True, dxfattribs={'layer': layer})
def mt(lines, x, y, h, layer='PO_YAZI', rot=0, width=None):
    if FLAT:   # LibreDWG MTEXT rotasyonunu okuyamıyor → satır başına TEXT
        from ezdxf.enums import TextEntityAlignment
        n = len(lines); r = math.radians(rot); px, py = -math.sin(r), math.cos(r)
        for k, ln in enumerate(lines):
            off = ((n-1)/2-k)*h*1.45*100
            t = msp.add_text(ln, dxfattribs={'layer': layer, 'style': 'PO_ARIAL', 'height': h*100, 'rotation': rot})
            t.set_placement((X(x)+px*off, Y(y)+py*off), align=TextEntityAlignment.MIDDLE_CENTER)
        return t
    m = msp.add_mtext('\\P'.join(lines), dxfattribs={'layer': layer, 'style': 'PO_ARIAL', 'char_height': h*100, 'rotation': rot})
    if width: m.dxf.width = width*100
    m.set_location((X(x), Y(y)), attachment_point=MTextEntityAlignment.MIDDLE_CENTER)
    return m
def fit(lines, x0, y0, x1, y1, layer='PO_YAZI', hmax=1.1, hmin=0.22):
    """Metni kutuya sığdır; dar-uzun kutuda 90° döndür. Sığmazsa alt satırları at."""
    w, h = x1-x0, y1-y0; rot = 90 if (h > 1.8*w and w < 12) else 0
    W, H = (h, w) if rot else (w, h)
    lines = [l for l in lines if l]
    while lines:
        n = len(lines); mx = max(len(l) for l in lines)
        th = min(hmax, H*0.82/(n*1.5), W*0.9/(mx*0.68))
        if th >= hmin or n == 1: break
        lines = lines[:-1]
    th = max(th, 0.15)
    mt(lines, (x0+x1)/2, (y0+y1)/2, th, layer, rot)

# ---- ADEYA raf referansı (bağımsız açılınca raflar görünsün; ADEYA DWG'sine eklenince katman kapatılır)
GOZ = 2.82; GOZ_ORJ = [9, 10, 10, 9, 10, 10, 9, 7, 7, 6, 7, 7]
for no, x0, y0, x1, y1, yuz in L['ADEYA_SEG']:
    rect('PO_ADEYA_RAF_REF', x0, y0, x1, y1)
    if yuz == 'BD': msp.add_line((X((x0+x1)/2), Y(y0)), (X((x0+x1)/2), Y(y1)), dxfattribs={'layer': 'PO_ADEYA_RAF_REF'})
    i = no-1; ys0 = L['ADEYA_ROWS'][i][3] if i < 7 else 35.8
    if i == 9: ys0 = 34.89
    for g in range(1, 12):
        yy = ys0-g*GOZ
        if y0 < yy < y1: msp.add_line((X(x0), Y(yy)), (X(x1), Y(yy)), dxfattribs={'layer': 'PO_ADEYA_RAF_REF'})
mt(['BACK-TO-BACK · ADEYA 22.10', f"12 sıra · {L['cap']['adeya']:,} palet".replace(',', '.')], 108.5, 30.5, 1.0, 'PO_ADEYA_RAF_REF')

# ---- alanlar
SHORT = {'rampa': ['RAMPA · 2 kapı', 'mal kabul + VAS/Bim + B2B sevk'],
         'vas_c': ['SEVK TAMPONU', 'VAS/Bim + B2B', '27 palet'], 'vas_str': ['Streç · palet kartı'], 'vas_stk': ['STOKLA', 'stoğa dönüş'],
         'vas_g': ['YARI MAMÜL BEKLEME', 'VAS giriş tamponu'], 'kalite': ['Kalite · iade · karantina', 'K1 61,5'],
         'serbest': ['SERBEST ALAN', 'VAS kullanımı olası'], 'serbest2': ['SERBEST', 'eski VAS 5–6 yeri'], 'vas56_kor': ['VAS 5–6 koridoru'], 'vas56_tamp': ['VAS 5–6 giriş / çıkış tamponu'],
         'konv': ['Konveyör K1 → kapı 139'], 'sorter': ['K4-batı ← HepsiJet'], 'sorter2': ['K4-doğu → Trendyol + Yurtiçi'], 'ayirma': ['Batı masası'], 'ayirma2': ['Doğu masası'], 'hp_cikis': ['HP çıkış → kapı 156'], 'soyunma': ['SOYUNMA ODASI', 'as-built'], 'sef_ofis': ['ŞEF OFİSİ'], 'vas_kor': ['VAS transpalet koridoru'], 'vas_tamp': ['VAS giriş · boş palet'], 'x99_gecis': ['X 99,1 geçişi'], 'kor2': ['Ana forklift koridoru'], 'di_kor2': ['Drive-in koridoru · orta'], 'kit': ['Koli · dolgu', 'paketlemeye parti besleme'], 'h_guney1': ['Boş araba · koli'], 'h_guney2': ['Boş araba · koli'], 'hp_fatura': ['Toplama · fatura'], 'hp_kor1': ['HP istif koridoru'], 'hp_kor2': ['HP istif koridoru'], 'kapi1': ['K2 141'],
         'k_hj': ['HepsiJet · %65,6', 'batı masası'], 'k_ty': ['Trendyol · %30,7', 'doğu masası + HP'], 'k_yk': ['Yurtiçi', '%3,4'],
         'sacak': ['DIŞ ALAN · ÜSTÜ KAPALI SAÇAK'], 'serit': ['Kargo aracı yanaşma şeridi ≈ 3,6 m · otopark taşınmalı'],
         'rezerv': ['KALAN ALAN / REZERV'], 'rezerv_k': ['REZERV · kuzey', 'e-ticaret bandının kuzeyi'],
         'hp_kit': ['Kit / ön paketleme', 'HP kampanya yedeği'], 'hp_hat': ['HP paketleme hattı'], 'hp_paketli': ['Toplama', 'fatura / etiket'],
         'hp_mamul': ['Mamül stok', '7 gün'], 'hp_ambalaj': ['Koli', 'dolgu'], 'hp_kor': ['HP iç istif koridoru 3,1 m'],
         'kabul': ['Mal kabul', 'FTL boşaltma'], 'di_kor': ['Drive-in koridoru · batı'], 'kor': ['Ana forklift koridoru'], 'lane_w': ['Batı forklift şeridi'],
         'lane_hp': ['HP besleme şeridi']}
NOAREA = ('aisle', 'conv', 'dock')
for z in L['Z']:
    ly = LAY[z['k']][0]; rect(ly, z['x0'], z['y0'], z['x1'], z['y1'])
    if z['k'] in ('cell', 'pack') or z['id'] == 'et_kamp': continue
    if not z['n'] and z['id'] not in SHORT: continue
    lines = list(SHORT.get(z['id'], [p for p in z['n'].split(' · ')][:3]))
    if z['id'] == 'sacak': continue   # saçak yazısı kargo kutularıyla çakışmasın: başlık ayrı
    w, h = z['x1']-z['x0'], z['y1']-z['y0']
    if z['k'] not in NOAREA and z['id'] not in ('kapi0', 'kapi1', 'kapi2', 'rampa'):
        lines.append(f"{w*h:,.0f} m²".replace(',', '.'))
    if z['id'] == 'rampa': lines.append('303 m²')
    fit(lines, z['x0'], z['y0'], z['x1'], z['y1'], ly)
mt(['DIŞ ALAN · ÜSTÜ KAPALI SAÇAK · Y 64,7–71,0 · v8.11: X 150,5 → 167,5 uzar (ruhsat)'], 133.8, 72.0, 0.38, 'PO_SACAK')

for t, x0, y0, x1, y1 in L['DI']: rect('PO_DRIVEIN_YENI', x0, y0, x1, y1)
cp = L['cap']
mt([f"DRIVE-IN BATI · {L['nW']} şerit × 20 = {cp['di_w']} palet"], 74, 9.8, .75, 'PO_DRIVEIN_YENI')
mt([f"DRIVE-IN ORTA · {L['nM']} şerit × 20 = {cp['di_m']} palet"], 125.5, 9.8, .75, 'PO_DRIVEIN_YENI')
for x0, y0, x1, y1 in L['EXT']: rect('PO_B2B_YENI', x0, y0, x1, y1); msp.add_line((X((x0+x1)/2), Y(y0)), (X((x0+x1)/2), Y(y1)), dxfattribs={'layer': 'PO_B2B_YENI'})
for x0, y0, x1, y1 in L['ROWS']: rect('PO_B2B_YENI', x0, y0, x1, y1)
mt([f"8–12. sıra uzatma +{cp['ext_8_12']} palet"], 133, 39.9, .55, 'PO_B2B_YENI')
mt([f"13. sıra tek yüz +{cp['row13']}"], 149.95, 30.0, .45, 'PO_B2B_YENI', 90)
msp.add_line((X(L['RES_X']), Y(6.5)), (X(L['RES_X']), Y(44.3)), dxfattribs={'layer': 'PO_UYARI'})
mt([f"REZERV SINIRI X = 151,9 · v8.11: Y 44,3–64,3 bandında X 168,9 · rezerv {L['REZERV_M2']['eski']:,} → {L['REZERV_M2']['yeni']:,} m²".replace(',', '.')], L['RES_X']+18, 4.6, .6, 'PO_UYARI')
msp.add_line((X(151.9), Y(44.3)), (X(168.9), Y(44.3)), dxfattribs={'layer': 'PO_UYARI'}); msp.add_line((X(168.9), Y(44.3)), (X(168.9), Y(64.4)), dxfattribs={'layer': 'PO_UYARI'})
for i, (x0, y0, x1, y1) in enumerate(L['VAS']):
    rect('PO_VAS_HAT', x0, y0, x1, y1)
    fit([f"VAS {i+1}" + (' · 2027 yedek' if i > 3 else ''), f"{(x1-x0)*(y1-y0):.0f} m²"] + (['dikey · eski kampanya'] if i > 3 else []), x0, y0, x1, y1, 'PO_VAS_HAT', hmax=.9)
# ---- v6.6 e-ticaret kare hücreler
OZ = json.load(open(os.path.join(os.path.dirname(LJ), 'hucre_ozet.json'))) if os.path.exists(os.path.join(os.path.dirname(LJ), 'hucre_ozet.json')) else dict(T=3.25)
for hc in L['HUCRE']:
    rect('PO_ETICARET_HUCRE', hc['x0'], hc['y0'], hc['x1'], hc['y1'])
    for r in HG.raf_bantlari(hc): rect('PO_HUCRE_RAF', *r)
    for g in HG.gozler(hc):
        hw = HG.GW/2
        if g['rot'] == 0: msp.add_line((X(g['x']-hw), Y(g['y']-0.44)), (X(g['x']-hw), Y(g['y']+0.44)), dxfattribs={'layer': 'PO_HUCRE_RAF'}); msp.add_line((X(g['x']+hw), Y(g['y']-0.44)), (X(g['x']+hw), Y(g['y']+0.44)), dxfattribs={'layer': 'PO_HUCRE_RAF'})
        else: msp.add_line((X(g['x']-0.44), Y(g['y']-hw)), (X(g['x']+0.44), Y(g['y']-hw)), dxfattribs={'layer': 'PO_HUCRE_RAF'}); msp.add_line((X(g['x']-0.44), Y(g['y']+hw)), (X(g['x']+0.44), Y(g['y']+hw)), dxfattribs={'layer': 'PO_HUCRE_RAF'})
        mt([f"{g['yuz']}{g['no']:02d}"], g['x'], g['y'], .22, 'PO_HUCRE_RAF', 90 if g['rot'] else 0)
    P = HG.path(hc); msp.add_lwpolyline([(X(x), Y(y)) for x, y in P], dxfattribs={'layer': 'PO_HUCRE_DONGU', 'const_width': 6, 'linetype': 'DASHED'})
    (xa, ya), (xb, yb2) = P[0], P[1]; msp.add_solid([(X(xb), Y(ya-1.2)), (X(xb-0.35), Y(ya-0.6)), (X(xb+0.35), Y(ya-0.6))], dxfattribs={'layer': 'PO_HUCRE_DONGU'})
    ax0, ay0, ax1, ay1 = hc['ada']
    _ng = len(HG.gozler(hc)); _hs = hc['x1']-hc['x0']
    mt([f"HÜCRE {hc['ad'][1]}", f"{_hs:.1f} × {_hs:.1f} = {_hs*_hs:.0f} m²".replace('.', ','), f"{_ng} göz × 5 kat = {_ng*5} göz", f"≈{OZ['T']:.0f} günde bir besleme", "döngü koridoru 1,8 m"], (ax0+ax1)/2, (ay0+ay1)/2, .42, 'PO_ETICARET_HUCRE')
    ex = hc['x1'] if hc['acik'] == 'E' else hc['x0']; ym = (hc['y0']+hc['y1'])/2
    mt(['GİRİŞ'], ex+(0.9 if hc['acik'] == 'E' else -0.9), ym-1.0, .3, 'PO_HUCRE_DONGU', 90); mt(['ÇIKIŞ'], ex+(0.9 if hc['acik'] == 'E' else -0.9), ym+1.0, .3, 'PO_HUCRE_DONGU', 90)
for p in L['PST']:
    x0 = p['x']-0.4 if p['taraf'] == 'B' else p['x']-0.4; rect('PO_PAKETLEME', p['x']-0.4, p['y']-0.75, p['x']+0.4, p['y']+0.75)
    mt([p['id']], p['x']+(-1.0 if p['taraf'] == 'B' else 1.0), p['y'], .28, 'PO_PAKETLEME', 90)
mt(['PAKETLEME · 16 istasyon', 'araba → istasyon → konveyör'], 123.1, 48.2+0.0, .32, 'PO_PAKETLEME') if False else None
S811 = L.get('V811', {}).get('shift', 0)
mt(['PAKETLEME', '16 istasyon'], 119.0+S811, 51.5, .42, 'PO_PAKETLEME', 90); mt(['araba park / dönüş'], 127.7+S811, 56.7, .34, 'PO_PAKETLEME', 90)
B = L['BAR']; yb = B['a'][1]; cur = B['a'][0]
for c, w in sorted(B['gates']):
    msp.add_line((X(cur), Y(yb)), (X(c-w/2), Y(yb)), dxfattribs={'layer': 'PO_BARIYER'})
    msp.add_line((X(c-w/2), Y(yb)), (X(c+w/2), Y(yb)), dxfattribs={'layer': 'PO_BARIYER_KAPI'}); cur = c+w/2
msp.add_line((X(cur), Y(yb)), (X(B['b'][0]), Y(yb)), dxfattribs={'layer': 'PO_BARIYER'})
mt(['4. sıra kuzey (Y 17–25,4): X 99,1 duvarı', 'batı yüz yok, yalnız doğu yüz (−36 palet)'], 104.6, 21.2, .3, 'PO_UYARI', 90)
mt(['4. sıra güney 1 göz kaldırıldı (−24 palet)', 'ana koridor X 99,1 duvarını burada geçer', 'alternatif: duvarda Y 45,2–48,2 açıklık'], 100.4, 38.6, .3, 'PO_UYARI')
mt(['VAS 1–4: X 65,1 kolonu hat içinde (tasarım gereği) · masalar kolonun iki yanında'], 65.1, 21.9, .25, 'PO_UYARI')
mt(['H1 kolonu X 133,15 + 133,80 doğu raf ucunda · giriş Y 55,5–59,3 kolonun güneyinde · döngüde net 1,62 m'], 128.3, 63.2, .22, 'PO_UYARI')
mt(['v8.11: tel çit X 150,7 → X 167,6 taşınmalı'], 158.0, 73.8, .3, 'PO_UYARI')
for x0, y0, x1, y1 in L.get('KAMP_PAL', []):
    rect('PO_KAMPANYA_PALET', x0, y0, x1, y1)
    k = 1
    while y0 + 0.8*k < y1 - 0.05: msp.add_line((X(x0), Y(y0+0.8*k)), (X(x1), Y(y0+0.8*k)), dxfattribs={'layer': 'PO_KAMPANYA_PALET'}); k += 1
    if x1 - x0 > 2: msp.add_line((X((x0+x1)/2), Y(y0)), (X((x0+x1)/2), Y(y1)), dxfattribs={'layer': 'PO_KAMPANYA_PALET'})
if L.get('KAMP_PAL'):
    mt(['E-TİCARET KAMPANYA · lansman palet yüzü + rezerv', f"{L['KAMP_PAL_N']} yer paleti · 3,0 m koridor · 229 m²"], 102.95, 56.5, .36, 'PO_KAMPANYA_PALET', 90)
    mt(['koridor 3,0 m · transpalet + araba'], 108.5, 56.5, .32, 'PO_KAMPANYA_PALET', 90)
    mt(['BOŞ ARABA · toplama başlangıcı', 'lansman → H1 girişi'], 113.4, 56.5, .36, 'PO_KAMPANYA_PALET', 90)
mt(['Kuzey acil çıkış X 81,2 · 125,4 (drive-in tüneli) · 160,1 · 194,1 — PO_KACIS katmanı (v8.9, İSG)'], 100, 5.2, .45, 'PO_UYARI')
mt(['Rampa = as-built "iç mekâna eklenecek alan 1"', 'X 48 duvarı Y 16–30 açılmalı · teyit'], 42.6, 38.0, .3, 'PO_UYARI')
for nm, x0, y0, x1, y1, kat in L['HPR']:
    rect('PO_HP_RAF', x0, y0, x1, y1); dik = (y1-y0) > (x1-x0)
    n = int(round(((y1-y0) if dik else (x1-x0))/2.7, 3))
    for i in range(1, n+1):
        if dik: msp.add_line((X(x0), Y(y0+2.7*i)), (X(x1), Y(y0+2.7*i)), dxfattribs={'layer': 'PO_HP_RAF'})
        else: msp.add_line((X(x0+2.7*i), Y(y0)), (X(x0+2.7*i), Y(y1)), dxfattribs={'layer': 'PO_HP_RAF'})
    fit([{'mamul': 'Mamül raf 24', 'koli': 'Koli rafı', 'paketli': f"Paketli raf {n*12}"}[nm]], x0, y0, x1, y1, 'PO_HP_RAF', hmax=.45)
for i in L.get('B2BPICK', []):
    x0, y0, x1, y1 = L['ADEYA_ROWS'][i]; g = L.get('B2BFACE_GOZ', 9); yf = y1-(y1-y0)*g/9
    rect('PO_B2B_TOPLAMA_YUZU', x0-.12, yf, x1+.12, y1); rect('PO_B2B_ESNEK', x0-.12, y0, x1+.12, yf)
    mt(['B2B YÜZÜ · alt göz 1–3 · 18 palet yeri'], x0-1.3, (yf+y1)/2, .42, 'PO_B2B_TOPLAMA_YUZU', 90)
    mt(['1. sıra göz 4–9 · esnek 30 palet yeri'], x0-1.3, (y0+yf)/2, .42, 'PO_B2B_ESNEK', 90)
for x0, y0, x1, y1, t in L['OPEN']: rect('PO_UYARI', x0, y0, x1, y1)
mt([f"PROTEIN OCEAN KAZAN · YERLEŞİM v8.11 · AS-BUILT 20.11.2026 ÜZERİNE · E-TİCARET 2 KARE HÜCRE + HAZIR PAKET · TOPLAM {cp['total']} PALET"], 128, 76.2, 1.3)
mt([f"ADEYA B2B {cp['adeya']} (2.256 − {L['X99_KAYIP']} duvar) + 8–12 uzatma {cp['ext_8_12']} + 13. sıra {cp['row13']} + drive-in {cp['di_w']+cp['di_m']} · v8.11: e-ticaret bandı 17,03 m doğuya (rezervden 262 m²), kampanya + koli duvarın doğusunda, VAS 5–6 eski kampanya alanında · birim cm, as-built POCN_FABR_KA_PLAN_20112026 koordinatı · PO_ katmanları proje, diğerleri as-built"], 128, 78.0, .55)

if not OKSUZ:
    FL = {'purple': ('PO_AKIS_B2B_SEVK', 6), 'green': ('PO_AKIS_MAL_KABUL', 3), 'blue': ('PO_AKIS_VAS', 5), 'amber': ('PO_AKIS_HAZIR_PAKET', 40), 'teal': ('PO_AKIS_ETICARET', 4)}
    for n, c in FL.values():
        if n not in doc.layers: doc.layers.add(n, color=c)
    def arrow(ly, pts):
        P = [(X(x), Y(y)) for x, y in pts]
        (x1, y1), (x2, y2) = P[-2], P[-1]; Ln = math.hypot(x2-x1, y2-y1); ux, uy = (x2-x1)/Ln, (y2-y1)/Ln; hl, hw = 110, 52
        bx, by = x2-ux*hl, y2-uy*hl
        msp.add_lwpolyline(P[:-1]+[(bx, by)], dxfattribs={'layer': ly, 'const_width': 22})
        msp.add_solid([(x2, y2), (bx-uy*hw, by+ux*hw), (bx+uy*hw, by-ux*hw)], dxfattribs={'layer': ly})
    def mark(ly, code, x, y): msp.add_circle((X(x), Y(y)), 65, dxfattribs={'layer': ly}); mt([code], x, y, .55, ly)
    for f in L['FLOW']: ly = FL[f['c']][0]; arrow(ly, f['p']); mark(ly, f['t'].split(' ')[0], *f['p'][0])
    for code, x, y, c in L['MARK']: mark(FL[c][0], code, x, y)
    LEG = {'green': ('AKIŞ · MAL KABUL', ['M1 mal kabul → drive-in batı / B2B', 'M2 orta blok → ana koridor → X 99 geçişi']),
           'blue': ('AKIŞ · VAS', ['V1 yarı mamül al (drive-in / B2B)', 'V2 yarı mamül bekleme tamponu', 'V3 üret (VAS 1–4)', 'V4 VAS koridoru → streç → palet kartı', 'V5 yükle → rampa (Bim / FTL)', "V5' stokla → ana koridor", 'V6 VAS 5–6 girdi (eski kampanya alanı)']),
           'amber': ('AKIŞ · HAZIR PAKET', ['H1 20 SKU mamül al (ana koridordan)', 'H2 mamül stok 7 gün', 'H3 HP hattında paketle', 'H4 paketli stok 7 gün', 'H5 sipariş topla + fatura', 'H6 → kapı 156 → kafes (TY/YK yanında, HJ araba)']),
           'teal': ('AKIŞ · E-TİCARET (HÜCRE)', ['E1 B2B → hücre besleme (3 günde bir)', 'E0 boş araba + lansman (kampanya) → H1 girişi', 'E2 18 gözlü araba, tek yön döngü → paket istasyonu', 'E3 K1 → kapı 139 → X 140,1 saptırıcı → K4-batı (HepsiJet)', 'E4 → K4-doğu (Trendyol + Yurtiçi)', 'E5 lansman rezervi → kampanya (ana koridordan)']),
           'purple': ('AKIŞ · B2B SEVK', ['B1 1. sıra alt göz 1–3 → batı şeridi → sevk tamponu → rampa', '1 palet ve üstü: rezervden tam palet'])}
    for i, (c, (hd, lines)) in enumerate(LEG.items()):
        x = 50+i*24; ly = FL[c][0]
        if FLAT:
            for k, ln in enumerate([hd]+lines): msp.add_text(ln, dxfattribs={'layer': ly, 'style': 'PO_ARIAL', 'height': 48, 'insert': (X(x), Y(79.6+0.7*k+0.5))})
        else:
            m = msp.add_mtext('\\P'.join([hd]+lines), dxfattribs={'layer': ly, 'style': 'PO_ARIAL', 'char_height': 48})
            m.set_location((X(x), Y(79.6)), attachment_point=MTextEntityAlignment.TOP_LEFT)
doc.saveas(OUT); print('ok', OUT, len(msp))
