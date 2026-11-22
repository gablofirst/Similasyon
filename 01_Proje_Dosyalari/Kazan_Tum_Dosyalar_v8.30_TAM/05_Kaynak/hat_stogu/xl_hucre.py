# v7.3 — Kazan e-ticaret hücre stoğu Excel'i (formüllü). python3 xl_hucre.py <çıktı.xlsx>
# Girdi: df.pkl, hucre_slotted.pkl, hucre_cells.json, hucre_ozet.json (hucre_slot.py çıktısı)
import sys, json
import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.comments import Comment
OUT = sys.argv[1]
h = pd.read_pickle('hucre_slotted.pkl'); oz = json.load(open('hucre_ozet.json')); cells = json.load(open('hucre_cells.json'))
A = 'ABC_satir(toplama_sikligi)'
F = 'Arial'; HF = PatternFill('solid', fgColor='0B6E6E'); H = Font(name=F, bold=True, color='FFFFFF'); B = Font(name=F, bold=True)
IN = Font(name=F, color='0000FF'); KEY = PatternFill('solid', fgColor='FFFF00'); N = Font(name=F)
wb = Workbook()
def hdr(ws, r, vals):
    for j, v in enumerate(vals, 1):
        c = ws.cell(r, j, v); c.font = H; c.fill = HF; c.alignment = Alignment(wrap_text=True, vertical='center')
# ---- Parametreler
P = wb.active; P.title = 'Parametreler'
P['A1'] = 'Parametreler · mavi hücreler girdi, sarı = karar parametresi'; P['A1'].font = Font(name=F, bold=True, size=13)
hdr(P, 3, ['Parametre', 'Değer', 'Birim', 'Açıklama / kaynak'])
par = [('Besleme sıklığı (kapsama)', oz['T'], 'gün', 'Hücre kapasitesinin taşıdığı en uzun süre (hucre_slot.py). Değiştirince göz ihtiyacı yeniden hesaplanır.', True),
       ('Hücre sayısı', 2, 'hücre', 'H1 + H2; her hücrede tüm SKU, sipariş hücrelere eşit bölünür.', True),
       ('Emniyet katsayısı', 1.2, '×', 'Tasarım talebi × 1,2', False),
       ('En az stok', 2, 'adet', 'Her gözde en az 2 adet', False),
       ('Göz genişlik', 1.78, 'm', 'ADEYA göz rafı', False), ('Göz derinlik', 0.88, 'm', '', False), ('Göz yükseklik', 0.50, 'm', '', False),
       ('Göz doluluk', 0.65, 'oran', 'Pilotta ölçülecek', False),
       ('Hücre göz kapasitesi', 145, 'göz', '29 göz × 5 kat (dış raf 17 + ada 12), 11,2 × 11,2 m hücre, 1,8 m koridor', False),
       ('Besleme kalemi süresi', 3, 'dk', 'B2B rezervden göze', False)]
for i, (a, v, u, n, key) in enumerate(par, 4):
    P.cell(i, 1, a).font = N; c = P.cell(i, 2, v); c.font = IN
    if key: c.fill = KEY
    P.cell(i, 3, u).font = N; P.cell(i, 4, n).font = N
P['A15'] = 'Göz net hacmi (m³)'; P['B15'] = '=B8*B9*B10*B11'; P['B15'].number_format = '0.000'
P['A15'].font = N
for c, w in zip('ABCD', (30, 12, 8, 90)): P.column_dimensions[c].width = w
T, NH, SF, MN, GV, CAP = 'Parametreler!$B$4', 'Parametreler!$B$5', 'Parametreler!$B$6', 'Parametreler!$B$7', 'Parametreler!$B$15', 'Parametreler!$B$12'
# ---- Hücre Stoğu
S = wb.create_sheet('Hücre Stoğu')
cols = ['ikas SKU', 'Ürün', 'Varyant', 'ABC', 'Toplama satırı (10 ay)', 'Tasarım talebi (adet/gün)', 'Hacim (cm³)', 'Yer',
        'Hücre başı stok (adet)', 'Stok hacmi (m³)', 'Bölme (1/n göz)', 'Bölme sayısı', 'Göz', 'Lokasyon (her iki hücrede)']
hdr(S, 1, cols)
hh = h.sort_values('toplama_satiri', ascending=False)
for r, (_, x) in enumerate(hh.iterrows(), 2):
    vals = [str(x.sku), x.urun_adi, x.varyant if x.varyant == x.varyant else '', x[A], int(x.toplama_satiri), round(float(x.d_tasarim), 2), round(float(x.hacim), 1), x.yer]
    for j, v in enumerate(vals, 1): S.cell(r, j, v).font = N
    S.cell(r, 6).font = IN; S.cell(r, 7).font = IN
    S.cell(r, 9, f'=MAX({MN},ROUNDUP(F{r}/{NH}*{T}*{SF},0))')
    S.cell(r, 10, f'=I{r}*G{r}/1000000'); S.cell(r, 10).number_format = '0.0000'
    S.cell(r, 11, f'=IF(OR(G{r}<=300,J{r}<={GV}/8),8,4)')
    S.cell(r, 12, f'=MAX(1,ROUNDUP(J{r}/({GV}/K{r}),0))')
    S.cell(r, 13, f'=IF(H{r}="hücre gözü",L{r}/K{r},0)'); S.cell(r, 13).number_format = '0.000'
    loc = x.lokasyonlar if isinstance(x.lokasyonlar, str) else 'K (kampanya lokasyonu, palet önü)'
    S.cell(r, 14, loc).font = N
NR = S.max_row
S.cell(1, 6).comment = Comment('ikas 2026 YTD, son 90/30 gün büyük olanı × SKU P95/ort (en çok 3). Kaynak: SKU_Profil.csv, model.py', 'Claude')
S.cell(1, 7).comment = Comment('Ürünlere ait ölçüler GÜNCEL 17.11.2026 (dims.py); eksikler kap tipi kuralı', 'Claude')
for c, w in zip('ABCDEFGHIJKLMN', (11, 34, 26, 6, 12, 12, 10, 22, 12, 11, 10, 10, 8, 46)): S.column_dimensions[c].width = w
S.freeze_panes = 'C2'
# ---- Göz haritası
G = wb.create_sheet('Göz Haritası')
hdr(G, 1, ['Göz kodu (H1 / H2)', 'Göz no (döngü)', 'Yüz', 'Kat', 'Doluluk (göz payı)', 'Ürünler (ABC · pay)'])
for r, c in enumerate(sorted(cells, key=lambda c: (c['no'], c['k'])), 2):
    G.cell(r, 1, f"H*{c['yuz']}-{c['no']:02d}-{c['k']}").font = N; G.cell(r, 2, c['no']); G.cell(r, 3, {'D': 'Dış raf', 'A': 'Ada'}[c['yuz']]); G.cell(r, 4, c['k'])
    G.cell(r, 5, c['fill']).number_format = '0.00'
    G.cell(r, 6, ' | '.join(f"{a.strip()} ({b} · {t:g})" for a, b, t, s in c['items'])).font = N
for c, w in zip('ABCDEF', (18, 12, 9, 6, 12, 110)): G.column_dimensions[c].width = w
G.freeze_panes = 'A2'
# ---- Özet
O = wb.create_sheet('Özet', 0)
O['A1'] = 'Kazan e-ticaret · 2 kare hücre stoğu · v7.3 · 20.11.2026'; O['A1'].font = Font(name=F, bold=True, size=13)
O['A2'] = 'Senaryo 3b: kapalı kare hücre, 12 gözlü arabayla toplama. Her hücrede tüm toplama SKU\'su, iki hücrede aynı göz. Değerler Hücre Stoğu sayfasından formülle gelir.'
hdr(O, 4, ['Kalem', 'Değer', 'Not'])
rows = [('Besleme sıklığı (gün)', f'={T}', 'Parametreler'),
        ('Hücre gözüne giren SKU', f'=COUNTIF(\'Hücre Stoğu\'!H2:H{NR},"hücre gözü")', 'A+B+C'),
        ('Kampanya lokasyonu SKU (lansman, palet önü)', f'=COUNTIF(\'Hücre Stoğu\'!H2:H{NR},"<>hücre gözü")', 'K-01…24'),
        ('Göz ihtiyacı (hücre başı)', f'=SUM(\'Hücre Stoğu\'!M2:M{NR})', 'bölme kaybı hariç'),
        ('Göz kapasitesi (hücre başı)', f'={CAP}', '29 göz × 5 kat'),
        ('Doluluk', '=B8/B9', 'kapasiteyi aşarsa besleme sıklığını düşürün'),
        ('Besleme kalemi / gün (2 hücre)', f'=ROUND(B6*{NH}/{T},0)', 'SKU × hücre / besleme günü'),
        ('Besleme iş yükü (FTE)', '=B11*Parametreler!B13/60/7.5', '7,5 verimli saat')]
for i, (a, v, n) in enumerate(rows, 5):
    O.cell(i, 1, a).font = N; O.cell(i, 2, v).font = B; O.cell(i, 3, n).font = N
O['B10'].number_format = '0.0%'; O['B8'].number_format = '0.0'; O['B12'].number_format = '0.0'
hdr(O, 15, ['Kat', 'Toplama satırı payı', 'Not'])
for i, (k, v) in enumerate(sorted(oz['kat_satir'].items(), key=lambda t: int(t[0])), 16):
    O.cell(i, 1, f'Kat {k}'); O.cell(i, 2, float(v)).number_format = '0.0%'; O.cell(i, 3, {'3': '100–150 cm, altın bölge', '2': '50–100 cm', '1': 'zemin', '4': '150–200 cm', '5': '200–250 cm'}[str(k)])
O['A22'] = 'Kat payı hucre_slot.py yerleşiminden (statik); Parametreler değişince yerleşim scriptle yeniden üretilir.'; O['A22'].font = Font(name=F, italic=True)
for c, w in zip('ABC', (44, 16, 70)): O.column_dimensions[c].width = w
# ---- Yöntem
Y = wb.create_sheet('Yöntem')
for i, t in enumerate(['Yöntem', 'Talep: ikas 2026 YTD SKU_Profil; günlük talep = max(son 90, son 30); "x N Adet" ana SKU\'ya eklenir; tasarım talebi = talep × min(P95/ort, 3).',
                       'SKU kapsamı: grup "hat" (hediye/eklenti paket istasyonunda, kit/paket SKU hazır paket ve kit alanında). Lansman Z ürünleri > 2 göz ise kampanya lokasyonunda palet önü.',
                       'Hücre: 11,2 × 11,2 m; dış çevre rafı (tek yüz, içe bakar) + ada (4 yüz, dışa bakar); 1,8 m tek yön döngü koridoru (araba 70×100×160); 29 göz × 5 kat.',
                       'Stok: hücre başı = tasarım talebi / 2 × besleme günü × 1,2 (en az 2). Göz = stok hacmi / (göz hacmi × %65 / bölme); küçük ürün 1/8, diğer 1/4 göz.',
                       'Yerleşim (hucre_slot.py): göz başına satırı yüksek ürün önce; kat sırası 3 → 2 → 4 → 1 → 5; 5,5 L kavanoz yalnız kat 2/1; A ürünleri döngü başı ve sonu, C ortası.',
                       'Göz no döngü sırası: 01 giriş, 29 çıkış. Lokasyon kodu: H{hücre}{yüz D/A}-{göz}-{kat}{bölme} (WMS Excel v7.3).'], 1):
    Y.cell(i, 1, t).font = B if i == 1 else N
Y.column_dimensions['A'].width = 150
wb.save(OUT); print('ok', OUT, NR-1, 'SKU')
