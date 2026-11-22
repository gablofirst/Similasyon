import pandas as pd,numpy as np
from openpyxl import Workbook
from openpyxl.styles import Font,PatternFill,Alignment,Border,Side
from openpyxl.utils import get_column_letter as CL
from openpyxl.comments import Comment
h=pd.read_pickle('slotted.pkl');d=pd.read_pickle('df.pkl');R=pd.read_pickle('runs.pkl')
def wms(l):   # model kodu B1-K2 → WMS E1G-01-2 (Batı raf = Kuzey, Doğu raf = Güney)
    if not isinstance(l,str) or not l or l=='-':return ''
    out=[]
    for t in l.split(', '):
        s_,rest=t[0],t[1:];g,k=rest.split('-K');out.append(f"E1{ {'B':'K','D':'G'}[s_]}-{int(g):02d}-{k}")
    return ', '.join(out)
ABC='ABC_satir(toplama_sikligi)'
F=lambda **k:Font(name='Arial',size=k.pop('size',10),**k)
BLUE=F(color='0000FF');BOLD=F(bold=True);HDR=F(bold=True,color='FFFFFF');GRN=F(color='008000')
HFILL=PatternFill('solid',fgColor='1F4E5A');YEL=PatternFill('solid',fgColor='FFF2CC');LG=PatternFill('solid',fgColor='EEF3F4')
thin=Side(style='thin',color='CCCCCC');BR=Border(bottom=thin)
wb=Workbook()
# ---------- Parametreler
P=wb.active;P.title='Parametreler'
P['A1']='Parametreler';P['A1'].font=F(bold=True,size=14)
P['A2']='Mavi hücreler girdidir, değiştirince Hat Stoğu ve Özet güncellenir. Sarı = karar parametresi.';P['A2'].font=F(italic=True,color='555555')
rows=[('Kapsama günü (besleme aralığı)',2,'gün','2 = 2 günde bir besleme (baz, 17.11.2026 kararı). 1 = her gün. Hat stoğu bu kadar günlük tasarım talebini karşılar.',True),
('Aktif e-ticaret hat sayısı',2,'hat','2026: 2 hat. 2027 (%50 büyüme): 3 hat. Her SKU her hatta bulunur, talep hatlara eşit bölünür.',True),
('Raf kat sayısı',5,'kat','Göz yüksekliği 50 cm: 4 kat = 2,0 m, 5 kat = 2,5 m (5. kat hafif / küçük ürün).',True),
('Güvenlik çarpanı',1.2,'x','Gün içi dalgalanma ve besleme gecikmesi payı.',False),
('Pik katsayısı tavanı (P95/ortalama)',3,'x','SKU bazlı P95/ortalama bu değerle sınırlanır. Lansman sıçramaları kampanya lokasyonunda karşılanır.',False),
('Göz eni',1.78,'m','Ostim Hat-1 as-is ölçüsü (Yeni_Depo_Eticaret_Hat_Stogu_Plani, Layout sayfası).',False),
('Göz derinliği',0.88,'m','Ostim Hat-1 as-is.',False),
('Göz yüksekliği',0.50,'m','Ostim Hat-1 as-is.',False),
('Doluluk oranı',0.65,'oran','Kutu / silindir dizilimi ve separatör kaybı. Pilot gözde ölçülerek düzeltilmeli.',False),
('Kullanılabilir göz hacmi','=B9*B10*B11*B12','m³','Formül.',None),
('Kampanya lokasyonu eşiği',2,'göz','Lansman + Z sınıfı SKU bu kadar gözden fazla isterse hat dışında palet lokasyonuna alınır.',False),
('Masa boyu (2 masa + ara)',11.28,'m','2 × 5,0 m masa + 1,28 m boşluk (as-is).',False),
('Masa uç boşluğu',3.0,'m','Hat iki ucunda geçiş (kuzey: besleme girişi, güney: konveyör çıkışı).',False),
('Raf uç boşluğu',2.0,'m','Raf bitişinden hat ucuna geçiş.',False),
('Hat eni',6.56,'m','0,88 raf + 1,50 toplama koridoru + 1,80 masa + 1,50 toplama koridoru + 0,88 raf.',False),
('Talep büyüme çarpanı',1.0,'x','2027 için 1,5 (e-ticaret %50) ve hat sayısı 3.',True),
('Ostim Hat-1 as-is alanı','=18.14*8.45','m²','Kıyas için: 18,14 × 8,45 m.',None)]
P['A3']='Parametre';P['B3']='Değer';P['C3']='Birim';P['D3']='Açıklama / kaynak'
for c in 'ABCD':P[c+'3'].font=HDR;P[c+'3'].fill=HFILL
for i,(a,b,u,n,key) in enumerate(rows,start=4):
    P[f'A{i}']=a;P[f'B{i}']=b;P[f'C{i}']=u;P[f'D{i}']=n
    for c in 'ABCD':P[f'{c}{i}'].font=F()
    if key is not None:P[f'B{i}'].font=BLUE
    if key:P[f'B{i}'].fill=YEL
    P[f'B{i}'].number_format='0.00' if isinstance(b,float) or (isinstance(b,str) and b.startswith('=')) else '0'
P.column_dimensions['A'].width=38;P.column_dimensions['B'].width=12;P.column_dimensions['C'].width=8;P.column_dimensions['D'].width=95
# isimler
N=dict(T='Parametreler!$B$4',NH='Parametreler!$B$5',KAT='Parametreler!$B$6',GUV='Parametreler!$B$7',PIK='Parametreler!$B$8',GW='Parametreler!$B$9',
       GV='Parametreler!$B$13',KE='Parametreler!$B$14',MASA='Parametreler!$B$15',MU='Parametreler!$B$16',RU='Parametreler!$B$17',EN='Parametreler!$B$18',BUY='Parametreler!$B$19',ASIS='Parametreler!$B$20')
# ---------- Hat Stoğu
S=wb.create_sheet('Hat Stoğu')
cols=['Sıra','SKU','Ürün','Varyant','ABC (satır)','XYZ','Toplama satırı (Oca–Eki)','Günlük talep, güncel (adet)','P95 / ortalama','Birim hacim (cm³)','Hacim kaynağı','Göz bölmesi (1/n)','Lansman','Tasarım günlük talep (adet)','Hat başı stok (adet)','Hat başı stok (m³)','Bölme sayısı','Göz','Yer','Taraf','Göz no','Kat','Lokasyonlar (baz: 2 günde bir, 5 kat)','WMS göz kodu (E1; E2 aynı göz)']
S.append(['E-ticaret hat stoğu · A+B SKU · ABC (toplama satırı) sırasına göre'])
S['A1'].font=F(bold=True,size=13)
S.append(['Mavi: veri (ikas 2026 SKU_Profil). Siyah: formül. Talep = son 90 / son 30 gün günlük ortalamasının büyüğü + "x N Adet" satışların ana SKU payı. Göz no 1 = konveyör (doğu) ucu, Kat 1 = alt (0–50 cm). v6.5: ergonomik yerleşim, en sık toplanan ürün kat 3–2\'de (50–150 cm).'])
S['A2'].font=F(italic=True,color='555555')
S.append(cols)
for j,c in enumerate(cols,1):
    x=S.cell(3,j);x.font=HDR;x.fill=HFILL;x.alignment=Alignment(wrap_text=True,vertical='center')
S.row_dimensions[3].height=42
r0=4
for k,(i,x) in enumerate(h.iterrows()):
    r=r0+k
    vals=[k+1,x.sku,x.urun_adi,x.varyant if x.varyant==x.varyant else '',x[ABC],x.XYZ,int(x.toplama_satiri),round(x.d_top,2),round(float(x['pik_katsayi_p95/ort']) if x['pik_katsayi_p95/ort']==x['pik_katsayi_p95/ort'] else 2.0,2),round(float(x.hacim),1),(x.hacim_kaynak if x.hacim_kaynak==x.hacim_kaynak else 'kap tipi kuralı'),int(x.bolme),'E' if x.lansman else 'H']
    for j,v in enumerate(vals,1):
        c=S.cell(r,j,v);c.font=BLUE if j in(8,9,10,12,13) else F()
    S.cell(r,14,f'=H{r}*{N["BUY"]}*MIN(I{r},{N["PIK"]})')
    S.cell(r,15,f'=ROUNDUP(N{r}/{N["NH"]}*{N["T"]}*{N["GUV"]},0)')
    S.cell(r,16,f'=O{r}*J{r}/1000000')
    S.cell(r,17,f'=MAX(1,ROUNDUP(P{r}/({N["GV"]}/L{r}),0))')
    S.cell(r,18,f'=Q{r}/L{r}')
    S.cell(r,19,f'=IF(AND(M{r}="E",R{r}>{N["KE"]}),"Kampanya lokasyonu","Göz rafı")')
    for j,v in zip((20,21,22,23),(x.taraf,x.goz_no,x.kat,x.lokasyonlar)):S.cell(r,j,v if v==v else '')
    S.cell(r,24,wms(x.lokasyonlar))
    for j in range(14,25):S.cell(r,j).font=F()
    S.cell(r,8).number_format='#,##0.0';S.cell(r,14).number_format='#,##0';S.cell(r,15).number_format='#,##0';S.cell(r,16).number_format='0.000';S.cell(r,18).number_format='0.000';S.cell(r,9).number_format='0.0';S.cell(r,10).number_format='#,##0'
    if x[ABC]=='A':
        for j in range(1,6):S.cell(r,j).fill=LG
rl=r0+len(h)-1
W=[5,10,30,30,7,5,11,11,8,9,11,8,8,11,10,9,8,7,18,7,6,5,26,30]
for j,w in enumerate(W,1):S.column_dimensions[CL(j)].width=w
S.freeze_panes='C4';S.auto_filter.ref=f'A3:{CL(len(cols))}{rl}'
rng=lambda c:f"'Hat Stoğu'!${c}${r0}:${c}${rl}"
# ---------- Özet
O=wb.create_sheet('Özet',0)
O['A1']='Kazan e-ticaret hattı · ABC hat stoğu ve hat ölçüsü';O['A1'].font=F(bold=True,size=14)
O['A2']='v6.5 (17.11.2026): ergonomik yerleşim, A ürünleri kat 3–2\'de. Canlı hesap: Parametreler sayfasındaki besleme günü, kat ve hat sayısına göre. Tüm değerler formül.';O['A2'].font=F(italic=True,color='555555')
L=[('Besleme aralığı (gün)',f'={N["T"]}','0'),('Hat sayısı',f'={N["NH"]}','0'),('Kat sayısı',f'={N["KAT"]}','0'),
('Hatta tutulan SKU (A+B)',f'=COUNTIF({rng("S")},"Göz rafı")','0'),('Kampanya lokasyonuna alınan lansman SKU',f'=COUNTIF({rng("S")},"Kampanya lokasyonu")','0'),
('  A sınıfı göz',f'=SUMIFS({rng("R")},{rng("S")},"Göz rafı",{rng("E")},"A")','0.0'),('  B sınıfı göz',f'=SUMIFS({rng("R")},{rng("S")},"Göz rafı",{rng("E")},"B")','0.0'),
('Hat başı göz ihtiyacı',f'=ROUNDUP(SUMIF({rng("S")},"Göz rafı",{rng("R")}),0)','0'),
('Kat başı göz',f'=ROUNDUP(B11/B6,0)','0'),('Taraf başı göz (her katta)',f'=ROUNDUP(B12/2,0)','0'),
('Raf boyu (m)',f'=B13*{N["GW"]}','0.00'),('Masa ile gereken boy (m)',f'={N["MASA"]}+{N["MU"]}','0.00'),
('HAT BOYU (m)',f'=MAX(B15,B14+{N["RU"]})','0.00'),('HAT ENİ (m)',f'={N["EN"]}','0.00'),('HAT ALANI (m²)','=B16*B17','#,##0.0'),
('Toplam e-ticaret hat alanı (m²)','=B18*B5','#,##0'),('Ostim Hat-1 as-is (m²)',f'={N["ASIS"]}','#,##0.0'),('Hat başı fark (as-is\'e göre)','=B18/B20-1','0%'),
('Bağlayıcı kısıt',f'=IF(B15>=B14+{N["RU"]},"Masa boyu","Raf boyu")','@'),('Raf kapasitesi (göz)','=B13*2*B6','0'),('Boş göz (büyüme / yeni SKU)','=B23-B11','0'),
('Hat başı günlük ikmal, ortalama gün (m³)',f'=SUMPRODUCT({rng("H")},{rng("J")})/1000000/B5*{N["BUY"]}','0.0'),
('Hat başı günlük ikmal, tasarım günü (m³)',f'=SUMPRODUCT({rng("N")},{rng("J")})/1000000/B5','0.0')]
O['A3']='Gösterge';O['B3']='Değer'
for c in 'AB':O[c+'3'].font=HDR;O[c+'3'].fill=HFILL
for i,(a,f,nf) in enumerate(L,start=4):
    O[f'A{i}']=a;O[f'B{i}']=f;O[f'A{i}'].font=F(bold=a.isupper() or a.startswith('HAT'));O[f'B{i}'].font=GRN if 'Parametreler' in f else F(bold=a.startswith('HAT'));O[f'B{i}'].number_format=nf
    if a.startswith('HAT ALANI') or a.startswith('HAT BOYU'):O[f'A{i}'].fill=YEL;O[f'B{i}'].fill=YEL
O.column_dimensions['A'].width=44;O.column_dimensions['B'].width=14
# senaryo tablosu (sabit, Python ile aynı model)
O['D3']='Senaryo karşılaştırması (aynı model, 17.11.2026 hesap)';O['D3'].font=BOLD
hd=['Yıl','Hat','Besleme','Kat','Göz / hat','Hat boyu (m)','Hat eni (m)','m² / hat','Toplam m²','as-is\'e göre']
for j,c in enumerate(hd):x=O.cell(4,4+j,c);x.font=HDR;x.fill=HFILL;x.alignment=Alignment(wrap_text=True)
rr=5
for x in R:
    v=['2026' if x['g']==1 else '2027 (×1,5)',x['n'],'Her gün' if x['T']==1 else '2 günde bir',x['lv'],x['goz'],x['L'],x['W'],x['m2_hat'],x['m2_top'],x['m2_hat']/153.283-1]
    for j,val in enumerate(v):
        c=O.cell(rr,4+j,val);c.font=F(bold=(x['T']==2 and x['lv']==5 and x['g']==1))
        c.number_format=['@','0','@','0','0','0.00','0.00','0.0','#,##0','0%'][j]
    if x['T']==2 and x['lv']==5 and x['g']==1:
        for j in range(10):O.cell(rr,4+j).fill=YEL
    rr+=1
O.cell(rr+1,4,'Sarı satır = baz (2 günde bir besleme, 5 kat). 2027\'de hat başı talep aynı kalır (talep ×1,5, hat 2→3), bu yüzden hat ölçüsü değişmez, hat sayısı artar.').font=F(italic=True,color='555555')
for j,w in enumerate([12,6,12,6,9,10,9,9,10,10]):O.column_dimensions[CL(4+j)].width=w
# ---------- C Hat Ataması + C Atama (c_slot.py çıktısı; v6.4'te xl.py'ye eklendi)
import json as _json,os as _os
_cdir='/home/claude'
if _os.path.exists(f'{_cdir}/C_2026.csv'):
    C26=pd.read_csv(f'{_cdir}/C_2026.csv',dtype={'sku':str});C27=pd.read_csv(f'{_cdir}/C_2027.csv',dtype={'sku':str})
    CO=_json.load(open(f'{_cdir}/C_ozet.json'))
    nC=len(C26)
    CH=wb.create_sheet('C Hat Ataması');CA=wb.create_sheet('C Atama ')
    tx=[f'C kategorisi ({nC} aktif SKU) · E1 / E2 / E3 hat ataması',
    "Kural: her C SKU yalnız bir hatta tutulur. WMS, C SKU içeren siparişi o hatta yönlendirir. C, hat toplama satırlarının %1,5'i.",
    'Neden tek hat: C her hatta tutulsaydı hat başı ≈8,5–9 göz gerekirdi; hatta boş yer 5,9 göz (baz yerleşim, 2 günlük, 5 kat). Tek hatta dağıtınca sığıyor.',
    'Yer (v6.5): B2B besleme ucundaki (göz 6–9) 5. kat boşlukları; C yavaş olduğu için kat 5 kabul edilebilir. Yavaş C için 1/8 göz separatör (sığarsa), aksi halde 1/4 göz. Stok = tasarım günü × besleme günü × 1,2, en az 2 adet.',
    '2027: talep ×1,5; E3 14,26 m (taraf başı 7 göz × 5 kat = 70), günlük besleme. Hat dağılımı toplama satırına göre dengelendi.',
    "Varsayım: iki farklı hattaki C SKU aynı siparişte nadir; olursa sipariş C payı yüksek hatta gider, diğer kalem RF ile B2B'den tamamlanır. Pilotta ölçülmeli."]
    for i,t in enumerate(tx,1):CH.cell(i,1,t).font=F(bold=(i==1),size=13 if i==1 else 10)
    CH.cell(8,1,'Özet').font=BOLD
    for j,c in enumerate(['Yıl','Hat','C SKU','C göz','C toplama satırı (10 ay)','Kalan boş göz'],1):x=CH.cell(9,j,c);x.font=HDR;x.fill=HFILL
    r=10
    for y,key in (('2026','S26'),('2027','S27')):
        for hat,v in CO[key].items():
            CH.cell(r,1,y);CH.cell(r,2,hat)
            CH.cell(r,3,f"=COUNTIFS('C Atama '!$A:$A,A{r},'C Atama '!$G:$G,B{r})")
            CH.cell(r,4,f"=SUMIFS('C Atama '!$I:$I,'C Atama '!$A:$A,A{r},'C Atama '!$G:$G,B{r})").number_format='0.00'
            CH.cell(r,5,int(v['C_satir'])).font=BLUE;CH.cell(r,6,float(v['kalan_bos'])).font=BLUE
            r+=1
    CH.cell(r+1,1,'Kalan boş göz: C yerleştikten sonra hattaki boş kapasite (sabit, c_slot.py çıktısı).').font=F(italic=True,color='555555')
    for j,w in enumerate([10,8,10,10,22,14],1):CH.column_dimensions[CL(j)].width=w
    CH.column_dimensions['A'].width=10
    hd=['Yıl','SKU','Ürün','Varyant','Günlük adet','Toplama satırı (10 ay)','Hat','Lokasyon (taraf+göz-kat)','Göz','Stok adet']
    CA.append(hd)
    for j in range(1,11):CA.cell(1,j).font=HDR;CA.cell(1,j).fill=HFILL
    for y,Cx in (('2026',C26),('2027',C27)):
        for _,x in Cx.iterrows():
            CA.append([y,x.sku,x.urun,x.varyant if x.varyant==x.varyant else None,x.gunluk_adet,int(x.toplama_satiri_10ay),x.hat,x.lokasyon,x.goz,int(x.stok_adet)])
    for row in CA.iter_rows(min_row=2):
        for c in row:c.font=F()
        row[8].number_format='0.000'
    CA.append(['Lokasyon: B = batı kenar, D = doğu kenar; göz 1 konveyör ucu, 9 B2B besleme ucu; K = kat (1 alt). E3 (2027) taraf başı 7 göz.'])
    for j,w in enumerate([7,10,30,24,11,12,6,14,7,9],1):CA.column_dimensions[CL(j)].width=w
    CA.freeze_panes='A2'
    # sayfa sırası: Hat Stoğu'ndan hemen sonra
    for nm in ('C Atama ','C Hat Ataması'):
        sh=wb[nm];wb._sheets.remove(sh);wb._sheets.insert(wb.sheetnames.index('Hat Stoğu')+1,sh)
else:
    print('UYARI: C_2026.csv yok; önce c_slot.py çalıştırın. C sayfaları eklenmedi.')
# ---------- Hat dışı SKU
X=wb.create_sheet('Hat Dışı SKU')
X.append(['Hatta göz açılmayan SKU\'lar ve gittikleri yer']);X['A1'].font=F(bold=True,size=13)
X.append(['Grup','SKU','Ürün','Varyant','ABC','Günlük talep, güncel (adet)','Nereye'])
for j in range(1,8):X.cell(2,j).font=HDR;X.cell(2,j).fill=HFILL
NE={'hediye_masa':'Paket masası (hediye / eklenti)','kit_HP':'Hazır paket alanı (kit / paket)','coklu_baza':'Ana SKU\'nun gözünden toplanır (talep ana SKU\'ya eklendi)'}
oth=d[(d.grup!='hat')|(~d[ABC].isin(['A','B']))|(d.d_top<=0)].copy()
oth['nereye']=[NE.get(g,'C kuyruğu: B2B alt seviye, RF ile toplama' if a=='C' else 'Talep yok (pasif)') for g,a in zip(oth.grup,oth[ABC])]
oth.loc[(oth.grup=='hat')&(oth.d_top<=0),'nereye']='Talep yok (pasif)'
oth=oth.sort_values(['nereye','toplama_satiri'],ascending=[True,False])
for _,x in oth.iterrows():
    X.append([x.grup,x.sku,x.urun_adi,x.varyant if x.varyant==x.varyant else '',x[ABC],round(x.d0,2),x.nereye])
for row in X.iter_rows(min_row=3):
    for c in row:c.font=F()
for j,w in enumerate([12,10,34,34,6,12,52],1):X.column_dimensions[CL(j)].width=w
X.freeze_panes='A3';X.auto_filter.ref=f'A2:G{X.max_row}'
# ---------- Yöntem
Y=wb.create_sheet('Yöntem')
txt=['Yöntem ve varsayımlar',
'1. Veri: ikas 2026 Oca–Eki SKU_Profil (814 SKU). ABC toplama satırına göre (A = satırların %80\'i, B = %80–95, C = %95–100).',
'2. Hatta A+B SKU tutulur. C kuyruğu (satırların %5\'i) B2B alt seviyede, RF ile toplanır.',
'3. Hediye / eklenti (Pocket Shaker, tester, huni, pillbox, tekli bar, karıştırıcı) paket masasında durur, hatta göz açılmaz.',
'4. Paket / kit SKU\'lar (fitness, vitamin, whey paketi, karma kutu) hazır paket alanında hazır tutulur. Bileşenlerden toplanıyorsa hat talebine eklenmeli: teyit edilecek.',
'5. "x N Adet / Kutu" satışlar ana SKU\'dan toplanır; talepleri N katıyla ana SKU\'ya eklendi.',
'6. Günlük talep = max(son 90 gün, son 30 gün) ortalaması. Tasarım günü = talep × min(SKU P95/ortalama, 3).',
'7. Hat başı stok = tasarım günü / hat sayısı × besleme günü × 1,2 güvenlik. Her SKU her hatta.',
'8. Birim hacim: Ürünlere ait ölçüler GÜNCEL 17.11.2026 (en × boy × yükseklik; kavanozda en = çap, doypack en × boy × 8 cm). 195 hat SKU\'sunun 186\'sı ölçüyle, 9\'u kap tipi kuralıyla (150 CC, 400 CC, 800 CC, 1,5 LT, 5,5 LT).',
'9. Göz 178 × 88 × 50 cm, doluluk %65. Separatörle en küçük yer 1/4 göz; ≤300 cm³ küçük ürünlerde 1/8 göz.',
'10. Hat: iki uzun kenarda raf, ortada 2 masa, iki uç açık (kuzey: B2B\'den besleme girişi, güney: konveyör çıkışı).',
'11. Yerleşim v6.5 (baz 2 günlük stok, 2 × 9 göz × 5 kat = 90 göz): göz başına toplama satırı en yüksek ürün önce. Kat sırası 3 → 2 → 4 → 1 → 5 (kat 2–3 = 50–150 cm, bel–omuz arası). 5,5 LT kavanoz (≥ 5.000 cm³) yalnız kat 2 / kat 1. 1,5 LT kutu kat 5\'e ancak yer kalmazsa. Aynı katta konveyöre yakın göz önce. Bir SKU tek tarafta.',
'11a. v6.4\'te 400 g kutular "ağır" sayılıp kat 1\'e itilmişti (eşik 2.434 cm³); A toplamalarının bir kısmı eğilerek yapılıyordu (personel geri bildirimi). v6.5\'te düzeltildi: kat 2–3 payı %39 → %69.',
'12. Lansman + Z sınıfı ve 2 gözden fazla isteyen SKU hat dışında kampanya lokasyonunda (palet) tutulur.',
'Kontrol edilecek: doluluk oranı (pilot göz), kit SKU\'ların toplama şekli, 5. kat ergonomisi, palet başı adet (ikmal sayısı için).']
for i,t in enumerate(txt,1):
    Y.cell(i,1,t).font=F(bold=(i==1),size=13 if i==1 else 10)
Y.column_dimensions['A'].width=140
# ---------- v6.5 Kat Dağılımı + Senaryo
KD=_json.load(open('/home/claude/kat_dagilim.json'));SC=_json.load(open('/home/claude/senaryo_a_gunluk.json'))
K=wb.create_sheet('Kat Dağılımı',1)
K['A1']='Toplama satırının kat dağılımı · v6.4 → v6.5 (ergonomik)';K['A1'].font=F(bold=True,size=13)
K['A2']='Hat stoğu A+B ürünleri, 2 günde bir besleme. Kaynak: ikas 2026 Oca–Eki toplama satırı, gözdeki paya göre bölündü.';K['A2'].font=F(italic=True,color='555555')
hd=['Kat','Yükseklik','Duruş','v6.4 pay','v6.5 pay','Fark','v6.4 A payı','v6.5 A payı','Ek süre varsayımı (sn/satır)']
for j,c in enumerate(hd,1):x=K.cell(4,j,c);x.font=HDR;x.fill=HFILL;x.alignment=Alignment(wrap_text=True)
HT={1:('0–50 cm','eğilme',3),2:('50–100 cm','rahat (bel)',0),3:('100–150 cm','rahat (göğüs)',0),4:('150–200 cm','kol yukarı',1),5:('200–250 cm','omuz üstü / uzanma',3)}
for k in range(1,6):
    r=4+k;a,b,e=HT[k]
    for j,v in enumerate([k,a,b,KD['v64']['all'][str(k)],KD['v65']['all'][str(k)],f'=E{r}-D{r}',KD['v64']['A'][str(k)],KD['v65']['A'][str(k)],e],1):
        c=K.cell(r,j,v);c.font=BLUE if j==9 else F()
        if j in(4,5,6,7,8):c.number_format='0.0%'
    if k in(2,3):
        for j in range(1,9):K.cell(r,j).fill=YEL
K.cell(10,1,'Kat 2–3 (rahat bölge)').font=BOLD;K.cell(10,4,'=D6+D7').number_format='0.0%';K.cell(10,5,'=E6+E7').number_format='0.0%'
for j in (4,5):K.cell(10,j).font=BOLD
K.cell(11,1,'Toplama satırı / gün (hat stoğu, 2 hat)');K.cell(11,4,round(KD['v65']['T']/304)).number_format='#,##0';K.cell(11,4).font=BLUE
K.cell(12,1,'Eğilme / uzanma ek süresi (saat/gün)');K.cell(12,4,'=SUMPRODUCT(D5:D9,$I$5:$I$9)*$D$11/3600');K.cell(12,5,'=SUMPRODUCT(E5:E9,$I$5:$I$9)*$D$11/3600')
for j in (4,5):K.cell(12,j).number_format='0.0'
K.cell(14,1,'Süre kazancı küçük (≈ 0,15 kişi); asıl kazanç bel/omuz yükü, şikâyet ve iş kazası riskinin düşmesi. Ek süre değerleri varsayımdır, pilotta ölçülmeli.').font=F(italic=True,color='555555')
for j,w in enumerate([22,12,20,10,10,9,11,11,16],1):K.column_dimensions[CL(j)].width=w
G=wb.create_sheet('Senaryo A Günlük',2)
G['A1']='Senaryo: ilk N A ürünü her gün, kalanı 2 günde bir beslenir';G['A1'].font=F(bold=True,size=13)
G['A2']=f"Amaç: kat 1'i (0–50 cm) toplamadan çıkarmak. Hat başı göz ihtiyacına E1'e düşen C payı (5 göz) dahil. Kat 2–5 kapasitesi 72 göz. A sınıfı {SC['nA']} ürün.";G['A2'].font=F(italic=True,color='555555')
hd=['Her gün beslenen A ürünü (N)','Hat başı göz ihtiyacı','Kat 1 tamamen boşalır mı','Hat başı günlük besleme kalemi','Besleme kalemi artışı','Kat 1 pay','Kat 2 pay','Kat 3 pay','Kat 4 pay','Kat 5 pay','Kat 1\'de kalan göz']
for j,c in enumerate(hd,1):x=G.cell(4,j,c);x.font=HDR;x.fill=HFILL;x.alignment=Alignment(wrap_text=True,vertical='center')
G.row_dimensions[4].height=44
for i,t in enumerate(SC['tablo']):
    r=5+i
    v=[t['N'],t['goz'],'Evet' if t['kat1_serbest'] else 'Hayır',t['besleme_kalem'],f'=D{r}/$D$5-1',t.get('kat1'),t.get('kat2'),t.get('kat3'),t.get('kat4'),t.get('kat5'),t.get('kat1_goz')]
    for j,val in enumerate(v,1):
        c=G.cell(r,j,val);c.font=F(bold=(t['N'] in (0,30)))
        c.number_format=['0','0.0','@','0.0','0%','0.0%','0.0%','0.0%','0.0%','0.0%','0.0'][j-1]
    if t['N']==30:
        for j in range(1,12):G.cell(r,j).fill=YEL
rr=6+len(SC['tablo'])
nt=[f"N = 0: v6.5 baz (2 günde bir). Kat 1 payı %{round(SC['tablo'][0]['kat1']*100)}, kat 1'de yavaş B ürünleri ve 5,5 LT kavanoz fazlası durur.",
    "N = 30 (sarı, öneri): kat 1 payı %3,7'ye, kat 2–3 payı %82'ye çıkar; besleme kalemi +%15. Kat 1'de yalnız yavaş B ve kavanoz kalır.",
    f"N = {SC['Nmin']} (tüm A): kat 1 toplamadan tamamen çıkar ancak payı 0,1 göz; besleme kalemi +%48. Kırılgan, önerilmez.",
    "Göz ihtiyacı N ile düzgün düşmez: küçük ürünlerde en küçük bölme (1/4 ya da 1/8 göz) bağlayıcı, günlük beslemede de aynı yeri tutar.",
    "Alternatif (raf): en alt kirişi 25–30 cm yükseltmek ve öne eğimli raf. Kalan kat 1 toplamalarını eğilmeden yapılır hale getirir; ADEYA ile konuşulmalı."]
for i,t in enumerate(nt):G.cell(rr+i,1,t).font=F()
for j,w in enumerate([16,12,12,14,12,9,9,9,9,9,11],1):G.column_dimensions[CL(j)].width=w
import os as _o2;_o2.makedirs('/home/claude/out',exist_ok=True)
wb.save('/home/claude/out/Kazan_Eticaret_Hat_Stogu_ABC.xlsx')
print('ok',rl)
