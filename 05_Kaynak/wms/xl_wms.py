# wms.pkl → Kazan_WMS_Lokasyon_ve_Atama_v7.5.xlsx
import sys, math
import pandas as pd, numpy as np
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter

W = pd.read_pickle(sys.argv[1]); OUTX = sys.argv[2]
LOC, P, BIN = W['LOC'].copy(), W['P'], W['BIN']; par = W['par']
slt = pd.read_pickle(sys.argv[3])   # hucre_slotted.pkl: hücre başı stok (A+B+C)
H = Font(bold=True, color='FFFFFF'); HF = PatternFill('solid', fgColor='1F4E78'); B = Font(bold=True); IN = Font(color='0000FF')
ZF = {'B': 'DDEBF7', 'D': 'FCE4D6', 'H': 'E2EFDA', 'K': 'FFF2CC', 'P': 'EDEDED'}

def sheet(wb, title, cols, rows, widths=None, freeze='A2'):
    ws = wb.create_sheet(title); ws.append([c for c, _ in cols])
    for r in rows: ws.append(r)
    for j, (c, f) in enumerate(cols, 1):
        ws.cell(1, j).font = H; ws.cell(1, j).fill = HF; ws.cell(1, j).alignment = Alignment(wrap_text=True, vertical='center')
        ws.column_dimensions[get_column_letter(j)].width = (widths or {}).get(c, max(10, min(40, len(c)+2)))
        if f:
            for k in range(2, ws.max_row+1): ws.cell(k, j).number_format = f
    ws.row_dimensions[1].height = 32
    ws.freeze_panes = freeze; ws.auto_filter.ref = ws.dimensions
    return ws
nz = lambda v: None if (v is None or (isinstance(v, float) and math.isnan(v)) or v == '') else v

wb = Workbook(); ws0 = wb.active; ws0.title = 'Özet'

# ---------- Lokasyonlar ----------
LOC['blok_s'] = LOC.blok
cols = [('Lokasyon kodu', None), ('Bölge', None), ('Bölge adı', None), ('Blok / hat', None), ('Sıra / şerit / hat no', None),
        ('Yüz / taraf', None), ('Göz', None), ('Kat', None), ('Pozisyon / bölme', None), ('Lokasyon tipi', None), ('Rezerv bölgesi', None),
        ('Kapasite', '0.000'), ('Birim', None), ('X (m)', '0.00'), ('Y (m)', '0.00'), ('Toplama sırası', None), ('Durum', None),
        ('Atanan SKU', None), ('Atanan ürün', None), ('Kaynak', None)]
rows = []
for _, r in LOC.iterrows():
    rows.append([r.kod, r.bolge, r.bolge_ad, r.blok, nz(r.sira if r.bolge != 'K' else None), nz(r.yuz), nz(r.goz), r.kat, nz(r.poz), r.tip,
                 nz(r.rez_bolge), r.kap, r.birim, r.x, r.y, nz(r.toplama_sira), r.durum, nz(r.sku), nz(r.urun), r.kaynak])
wsL = sheet(wb, 'Lokasyonlar', cols, rows, {'Lokasyon kodu': 15, 'Bölge adı': 22, 'Lokasyon tipi': 22, 'Rezerv bölgesi': 30, 'Atanan ürün': 46, 'Atanan SKU': 16, 'Kaynak': 14})
for k in range(2, wsL.max_row+1):
    wsL.cell(k, 1).fill = PatternFill('solid', fgColor=ZF[wsL.cell(k, 2).value]); wsL.cell(k, 1).font = B
NL = wsL.max_row

# ---------- E-ticaret hücre ataması ----------
stmap = slt.set_index(slt.sku.astype(str))[['stok_adet', 'goz']].to_dict('index')
BIN['goz_top'] = BIN.groupby(['hat', 'sku']).pay.transform('sum')
def bmax(b):
    if b.st == b.st and b.st: tot = b.st
    else: tot = stmap.get(str(b.sku), {}).get('stok_adet', np.nan)
    return int(round(tot*b.pay/b.goz_top)) if tot == tot else None
BIN['max'] = BIN.apply(bmax, axis=1); BIN['min'] = (BIN['max']*0.5).round()
rows = []
for _, b in BIN.sort_values(['hat', 'kod']).iterrows():
    rows.append([b.hat, b.kod, b.parent, b.sku, b.ad, b.abc, b.goz, b.kat, b.pay, nz(b['min']), nz(b['max'])])
sheet(wb, 'E-ticaret Hücre Ataması', [('Hücre', None), ('Lokasyon (bölme)', None), ('Göz (üst lokasyon)', None), ('ikas SKU', None), ('Ürün', None),
      ('ABC', None), ('Göz', None), ('Kat', None), ('Göz payı', '0.000'), ('Min (adet)', '#,##0'), ('Max (adet)', '#,##0')], rows,
      {'Ürün': 46, 'Lokasyon (bölme)': 16, 'Göz (üst lokasyon)': 16})

# ---------- B2B toplama + rezerv ----------
rows = []
for x in W['B2BROW']:
    k = x['key']; p = P.loc[k]; pa = int(p.pal_adet); npick = len(x['toplama'])
    rz = W['REZ'].get(k, []); di = W['DIREZ'].get(k, [])
    rz_txt = ', '.join(rz) if rz else (', '.join(f"D{int(s):02d} (şerit, 5 kat)" for s in di) if di else '')
    mx = npick*pa if npick else None
    rows.append([x['urun_kpi'], p.erp, nz(p.ikas), p.kanal, x['satir_gun'], x['adet_gun'], nz(x['pal_gun']), ', '.join(x['toplama']) or 'yüz yok · rezervden',
                 npick, pa, nz(mx), nz(round(mx*0.3) if mx else None), rz_txt, len(rz) if rz else len(di)*par['DI_KAT']*par['DI_DER'], round(p.rez_palet, 2)])
wsB = sheet(wb, 'B2B Toplama ve Rezerv', [('Ürün (KPI raporu)', None), ('ERP malzeme kodu', None), ('ikas SKU', None), ('Kanal', None), ('Satır / gün', '0.00'),
      ('Adet / gün', '#,##0'), ('Palet / gün (toplam)', '0.00'), ('Toplama gözü', None), ('Toplama palet yeri', None), ('Adet / palet', '#,##0'),
      ('Toplama max (adet)', '#,##0'), ('İkmal noktası min (adet)', '#,##0'), ('Rezerv lokasyonları', None), ('Rezerv yeri (palet)', None),
      (f"{par['REZ_GUN']} gün ihtiyaç (palet)", '0.00')], rows, {'Ürün (KPI raporu)': 32, 'Toplama gözü': 26, 'Rezerv lokasyonları': 70, 'ERP malzeme kodu': 15})

# ---------- Rezerv ataması (tüm SKU) ----------
rows = []
for k, p in P.sort_values(['kanal', 'satir'], ascending=[True, False]).iterrows():
    rz = W['REZ'].get(k, []); di = W['DIREZ'].get(k, [])
    pick = W['PICK'].get(k, []) + W['KPICK'].get(k, [])
    if not pick:
        e = BIN[BIN.sku == k]
        pick = [f"{h}: " + ', '.join(e[e.hat == h].kod) for h in ('H1', 'H2') if (e.hat == h).any()]
        if not pick: pick = ['P01–P16 (paket istasyonu)'] if p.grup == 'hediye_masa' else (['HP rafı (hazır paket)'] if p.grup == 'kit_HP' else [])
    where = 'Drive-in ' + ', '.join(f"D{int(s):02d}" for s in di) if di else ', '.join(rz)
    rows.append([nz(p.ikas), nz(p.erp), p.urun, p.kanal, p.abc, {'hat': 'E-ticaret hücresi', 'hediye_masa': 'Hediye / paket masası', 'kit_HP': 'Kit / hazır paket', 'b2b': 'B2B'}.get(p.grup, p.grup),
                 p.d_eco, p.d_b2b, int(p.pal_adet), p.rez_palet, 'Evet' if p.karma else '', len(di)*par['DI_KAT']*par['DI_DER'] if di else len(rz), where, ' | '.join(pick)])
sheet(wb, 'Rezerv Ataması', [('ikas SKU', None), ('ERP kodu', None), ('Ürün', None), ('Kanal', None), ('ABC', None), ('Toplama yeri türü', None),
      ('E-ticaret adet/gün', '#,##0.0'), ('B2B adet/gün', '#,##0.0'), ('Adet / palet (tahmin)', '#,##0'), (f"{par['REZ_GUN']} gün ihtiyaç (palet)", '0.00'),
      ('Karma palet', None), ('Rezerv yeri (palet)', None), ('Rezerv lokasyonları', None), ('Toplama lokasyonu', None)], rows,
      {'Ürün': 46, 'Rezerv lokasyonları': 60, 'Toplama lokasyonu': 60, 'Toplama yeri türü': 20})

# ---------- WMS ürün-lokasyon (düz liste, içe aktarma) ----------
rows = []
def pr(k): p = P.loc[k] if k in P.index else None; return (nz(p.ikas) if p is not None else k, nz(p.erp) if p is not None else None, p.urun if p is not None else '')
for x in W['B2BROW']:
    k = x['key']; ik, erp, u = pr(k); pa = int(P.loc[k, 'pal_adet'])
    for l in x['toplama']: rows.append([l, ik, erp, u, 'Sabit toplama · B2B', pa, round(pa*0.3), 'adet'])
for _, b in BIN.iterrows():
    ik, erp, u = pr(b.sku) if b.sku in P.index else (b.sku, None, b.ad)
    rows.append([b.kod, ik, erp, u or b.ad, f"Sabit toplama · hücre {b.hat}", nz(b['max']), nz(b['min']), 'adet'])
for k, ls in W['KPICK'].items():
    ik, erp, u = pr(k)
    for l in ls: rows.append([l, ik, erp, u, 'Sabit toplama · kampanya (palet önü)', int(P.loc[k, 'pal_adet']) if k in P.index else None, None, 'adet'])
for k, ls in W['REZ'].items():
    ik, erp, u = pr(k)
    for l in ls: rows.append([l, ik, erp, u, 'Rezerv (başlangıç yerleşimi)', None, None, 'palet'])
for k, ls in W['DIREZ'].items():
    ik, erp, u = pr(k)
    for s in ls:
        for kk in range(1, par['DI_KAT']+1): rows.append([f"D{int(s):02d}-{kk}", ik, erp, u, 'Rezerv · drive-in (tek SKU / şerit)', None, None, 'palet'])
sheet(wb, 'WMS Ürün-Lokasyon', [('Lokasyon kodu', None), ('ikas SKU', None), ('ERP kodu', None), ('Ürün', None), ('Rol', None), ('Max', '#,##0'), ('Min (ikmal)', '#,##0'), ('Birim', None)],
      rows, {'Ürün': 46, 'Rol': 34, 'Lokasyon kodu': 15})

# ---------- Diğer alanlar ----------
sheet(wb, 'Diğer Alanlar (öneri)', [('Kod', None), ('Alan', None), ('Tip', None), ('Palet / adet', None), ('Konum (plan)', None)],
      [list(a) for a in W['ALAN']], {'Kod': 24, 'Alan': 60, 'Konum (plan)': 30})

# ---------- Kodlama ----------
wsK = wb.create_sheet('Kodlama', 1)
K = [['Lokasyon kodlama standardı · Kazan · v6.6'], [],
     ['Kural', 'Açıklama'],
     ['İlk harf = bölge', 'D drive-in · B back-to-back · H e-ticaret hücresi · K e-ticaret kampanya lokasyonu · P paket istasyonu. Kod okununca alan belli olur, raporlar bölgeye göre süzülür.'],
     ['Sabit uzunluk, büyük harf, tire', 'Barkod ve el terminalinde aynı okunur. Sıralama alfabetik = fiziksel sıra.'],
     ['Numara yönü', 'Göz 01 ana koridor (güney) ucunda; drive-in şerit 01 batıda; hücre gözü 01 döngü girişinde, numara toplama döngüsü sırasıyla artar (tek yön).'],
     ['Kat', '1 = zemin. Toplama gözleri hep zeminde ya da elle erişilen katta.'],
     [],
     ['Bölge', 'Biçim', 'Örnek', 'Okunuşu', 'Adet', 'Not'],
     ['B · Back-to-back', 'B{sıra 01–13}{yüz B/D}-{göz 01–10}-{kat 1–4}{poz A/B/C}', 'B01B-01-1A', '1. sıra, batı yüz, göz 1, zemin, A paleti', f'=COUNTIF(Lokasyonlar!B:B,"B")', 'Lokasyon = tek palet. Tünel gözünde (göz 05) kat 1–2 yok.'],
     ['D · Drive-in', 'D{şerit 01–54}-{kat 1–4}', 'D24-3', '24. şerit, 3. kat (5 palet derinlik)', f'=COUNTIF(Lokasyonlar!B:B,"D")', 'Lokasyon = şeridin bir katı, kapasite 5 palet (zemin + 3 kat, ADEYA teyidi 18.11). Şerit 01–24 batı blok, 25–54 orta blok.'],
     ['H · E-ticaret hücresi', 'H{hücre 1–2}{yüz D/A}-{göz 01–26}-{kat 1–5}{bölme A–H}', 'H1D-04-3A', 'Hücre 1, dış raf, göz 4, kat 3, A bölmesi', f'=COUNTIF(Lokasyonlar!B:B,"H")', 'D = dış çevre rafı, A = ada rafı. Göz no döngü sırası. Göz bölmelere ayrılır (1/8–1/4 göz), bölme = bir SKU. İki hücrede yerleşim aynı.'],
     ['K · Kampanya lokasyonu', 'K-{palet yeri 01–24}', 'K-05', 'Kampanya alanı, 5. palet yeri', f'=COUNTIF(Lokasyonlar!B:B,"K")', 'Lansman / Z ürün paleti, palet önünden toplanır. 24 yer taslak, sahada çizilecek.'],
     ['P · Paket istasyonu', 'P{01–16}', 'P05', '5. paket istasyonu (batı sıra)', f'=COUNTIF(Lokasyonlar!B:B,"P")', '12 gözlü araba istasyona bırakılır; göz = sipariş.'],
     [],
     ['Eski koddan yeni koda', 'Eski', 'Yeni', 'Not'],
     ['B2B toplama yüzü (v6.4 Excel)', 'S1-B-01-A', 'B01B-01-1A', 'Kat 1 eklendi, sıra iki haneli.'],
     ['v6.5 hat kodu', 'E1K-01-2A', 'H1D-xx-3A', 'v6.6 ile hatlar kaldırıldı; e-ticaret kare hücrede. Ürün-göz eşleşmesi hucre_slot.py ile yeniden üretildi.'],
     ['Hücreler', 'H1D-04-3A', 'H2D-04-3A', 'Aynı ürün iki hücrede aynı göz kodunda; sipariş dalgası hücrelere dönüşümlü verilir.'],
     [],
     ['WMS kuralları (öneri)'],
     ['· Toplama gözleri (B2B-TOPLAMA, HAT-GÖZ, KAMPANYA-TOPLAMA) sabit SKU atamalı; min/max ile ikmal emri üretir.'],
     ['· REZERV dinamik: atama sayfasındaki yerler başlangıç yerleşimi. Yerleştirmede WMS önce SKU\'nun rezerv bölgesindeki en yakın boş yeri önerir.'],
     ['· Drive-in: bir şerit tek SKU + tek lot. LIFO çalışır; FEFO isteyen ürün drive-in\'e konmaz.'],
     ['· B2B 1 palet ve üstü satır: rezervden tam palet → streç (STR-01) → sevk tamponu (ST) → rampa. Toplama gözünden çıkmaz.'],
     ['· Hücre toplama: 12 siparişlik dalga (batch), sipariş-göz eşleştirmesi, toplama listesi döngü sırasına göre (göz 01 → 26). Her iki hücrede tüm SKU var.'],
     ['· Etiket: lokasyon kodu + barkod (Code 128). Raf etiketinde kat okuma yönü aşağıdan yukarı.']]
for r in K: wsK.append(r)
wsK['A1'].font = Font(bold=True, size=13)
for row in (3, 9, 15):
    for j in range(1, 7):
        c = wsK.cell(row, j)
        if c.value: c.font = H; c.fill = HF
wsK['A20'].font = B
for j, w in zip('ABCDEF', (30, 52, 22, 40, 10, 70)): wsK.column_dimensions[j].width = w
for row in (10, 11, 12, 13, 14): wsK.cell(row, 1).fill = PatternFill('solid', fgColor=ZF[wsK.cell(row, 1).value[0]])

# ---------- Özet ----------
LR = f'Lokasyonlar!$B$2:$B${NL}'; LT = f'Lokasyonlar!$J$2:$J${NL}'; LK = f'Lokasyonlar!$L$2:$L${NL}'; LS = f'Lokasyonlar!$R$2:$R${NL}'
O = [['Kazan · WMS lokasyon ana verisi ve ürün-lokasyon ataması · v6.6 · 19.11.2026'],
     ['v6.6: e-ticaret 2 kare hücre (arabalı toplama), drive-in 4 kat × 5 derinlik (ADEYA). Ergonomik yerleşim (A ürünleri kat 3–2) korunur. Sayılar Lokasyonlar sayfasından formülle gelir. Canlı öncesi aktif tüm SKU ile güncellenecek.'], [],
     ['Bölge', 'Lokasyon tipi', 'Lokasyon', 'Palet / göz kapasitesi', 'Atanmış lokasyon', 'Not']]
tips = [('B', 'B2B-TOPLAMA', 'palet', '1. sıra zemin, göz 1–3: Bim dışı B2B 17 ürün'),
        ('B', 'B2B-ESNEK', 'palet', '1. sıra zemin, göz 4–9: lansman, kampanya, ara sıra B2B'),
        ('B', 'REZERV', 'palet', 'kat 1–4 rezerv; bölgeler: B2B kanal (1. sıra), B2B/VAS (2–3), e-ticaret besleme (4–9), genel (10–13)'),
        ('D', 'REZERV-BLOK', 'palet', '54 şerit × 4 kat, kat başına 5 palet'),
        ('H', 'HÜCRE-GÖZ', 'göz', 'H1 + H2, SKU başına bölme'),
        ('H', 'HÜCRE-GÖZ (boş)', 'göz', 'hücrelerde boş kalan pay'),
        ('P', 'PAKET-İSTASYONU', 'istasyon', '16 istasyon, konveyörün iki yanında'),
        ('K', 'KAMPANYA-TOPLAMA', 'palet', 'lansman / Z ürün paleti')]
for z, t, u, n in tips:
    r = len(O)+1
    O.append([z, t, f'=COUNTIFS({LR},"{z}",{LT},"{t}")', f'=SUMIFS({LK},{LR},"{z}",{LT},"{t}")', f'=COUNTIFS({LR},"{z}",{LT},"{t}",{LS},"<>")', n])
r0 = 5; r1 = len(O)
O.append(['Toplam', None, f'=SUM(C{r0}:C{r1})', None, f'=SUM(E{r0}:E{r1})', None])
O += [[], ['Palet kapasitesi', 'Bu dosya', 'Plan (v6.4)', 'Fark', 'Açıklama'],
      ['Back-to-back', f'=SUMIFS({LK},{LR},"B")', 2730, None, 'ADEYA 2.256 + uzatma 360 + 13. sıra 114. Çizimden sayılan göz: 1–7. sıra 9/10/10/9/10/10/9, 8–12. sıra 7/7/6/7/7. Göz 3 palet × 4 kat, her sırada 1 tünel. ADEYA etiketiyle 24 palet fark: İhsan\'ın kesin göz/tünel listesiyle kapanacak.'],
      ['Drive-in', f'=SUMIFS({LK},{LR},"D")', 1080, None, '54 şerit × 20 palet (4 kat × 5 derinlik, ADEYA teyidi)'],
      ['Toplam', None, None, None, None]]
for i in range(len(O)-2, len(O)):
    pass
for r in O: ws0.append(r)
n = ws0.max_row
for rr in (n-2, n-1): ws0.cell(rr, 4).value = f'=B{rr}-C{rr}'
ws0.cell(n, 2).value = f'=B{n-2}+B{n-1}'; ws0.cell(n, 3).value = f'=C{n-2}+C{n-1}'; ws0.cell(n, 4).value = f'=B{n}-C{n}'
O2 = [[], ['Atama özeti', 'Değer', 'Not'],
      ['B2B (Bim dışı) ürün', len(W['B2BROW']), '16 ürüne toplama gözü (18 palet yeri), Batman bar yüzsüz (rezervden)'],
      ['E-ticaret hücre SKU (H1 / H2)', f"{BIN[BIN.hat=='H1'].sku.nunique()} / {BIN[BIN.hat=='H2'].sku.nunique()}", f"A+B+C her iki hücrede aynı gözde; besleme ≈{int(par['HT'])} günde bir"],
      ['Kampanya lokasyonu SKU', len(W['KPICK']), f"{sum(len(v) for v in W['KPICK'].values())} palet yeri"],
      ['Rezerv atanan SKU', len(P), 'e-ticaret (hat, hediye, büyük kit) + B2B'],
      ['Rezerv: back-to-back palet yeri', len({l for v in W['REZ'].values() for l in v}), f"karma palet: {int(P.karma.sum())} küçük SKU, pozisyon başına en çok 3"],
      ['Rezerv: drive-in şerit', sum(len(v) for v in W['DIREZ'].values()), f"≥ {par['DI_ESIK']} palet ihtiyacı olan SKU: " + ', '.join(P.loc[k, 'urun'] for k in W['DIREZ'])],
      [], ['Varsayımlar (mavi = değiştirilebilir girdi, scriptte)', 'Değer', 'Not'],
      ['Back-to-back göz', '3 palet × 4 kat', 'ADEYA teyidi (İhsan)'],
      ['Tünel', f"göz {par['TUNEL_GOZ']}, kat 1–2 yok", 'her sırada güneyden 5. göz; çapraz geçiş aynı hizada'],
      ['Drive-in şerit', f"{par['DI_KAT']} kat × {par['DI_DER']} derinlik", 'ADEYA teyidi'],
      ['Rezerv kapsama', f"{par['REZ_GUN']} gün", 'başlangıç yerleşimi; ERP stok listesi gelince gerçek stokla yeniden çalıştırılır'],
      ['Palet net ürün hacmi', f"{par['PAL_M3']:.2f} m³", '120×80×150 cm, %80 istif verimi; ürün bazında koli/palet dizilimi gelince değişir'],
      ['Bar palet', f"{par['BAR_PAL']:,} adet".replace(',', '.'), "12'li display × 875 display/palet (v6.4 varsayımı)"],
      ['Hücre gözü min / max', 'max = hücre başı stok, min = max × 0,5', f"≈{int(par['HT'])} günde bir besleme; B2B toplama gözü min = max × 0,3"],
      [], ['Açık konular'],
      ['1. ADEYA kesin göz / tünel listesi: back-to-back sayısı 24 palet farklı. Liste gelince GOZ_ORJ ve TUNEL_GOZ güncellenip yeniden üretilir.'],
      ['2. ERP stok listesi (SKU, lot, palet): rezerv yerleşimi tahmini talepten. Taşınma öncesi gerçek stokla yeniden çalıştırılmalı.'],
      ['3. B2B ürünlerinin ERP kod eşleşmesi ada göre yapıldı. "Çilek 50g" = Strawberry Cheesecake varsayıldı, teyit edilmeli.'],
      ['4. Kampanya lokasyonu 24 palet yeri, paket istasyonları ve HP rafı lokasyonları sahada netleşecek.'],
      ['5. WMS seçimi: kod uzunluğu (en çok 10 karakter) ve bölme (alt lokasyon) desteği teklif veren firmalara sorulmalı.']]
for r in O2: ws0.append(r)
ws0['A1'].font = Font(bold=True, size=13)
for row in ws0.iter_rows():
    for c in row:
        if c.value in ('Bölge', 'Palet kapasitesi', 'Atama özeti', 'Varsayımlar (mavi = değiştirilebilir girdi, scriptte)') or (c.row in (4,) ):
            for j in range(1, 7):
                cc = ws0.cell(c.row, j)
                if cc.value is not None: cc.font = H; cc.fill = HF
        if c.value in ('Toplam', 'Açık konular'): c.font = B
for c in ('A', 'B', 'C', 'D', 'E', 'F'): ws0.column_dimensions[c].width = {'A': 34, 'B': 22, 'C': 14, 'D': 22, 'E': 18, 'F': 70}[c]
for row in ws0.iter_rows(min_row=n+11, max_row=n+18):
    if row[1].value: row[1].font = IN
order=['Özet','Kodlama','Lokasyonlar','B2B Toplama ve Rezerv','E-ticaret Hücre Ataması','Rezerv Ataması','WMS Ürün-Lokasyon','Diğer Alanlar (öneri)']
wb._sheets=[wb[n] for n in order]
wb.save(OUTX); print('ok', OUTX, wb.sheetnames)
