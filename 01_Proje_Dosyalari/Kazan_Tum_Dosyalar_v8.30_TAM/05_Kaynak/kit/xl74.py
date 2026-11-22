import pandas as pd, json
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter as CL
F='Arial'; f=Font(name=F,size=10); fb=Font(name=F,size=10,bold=True); fh=Font(name=F,size=10,bold=True,color='FFFFFF')
blue=Font(name=F,size=10,color='0000FF'); hdr=PatternFill('solid',fgColor='1F4E78'); yel=PatternFill('solid',fgColor='FFFF00')
def head(ws,r,cols,w=None):
    for j,c in enumerate(cols,1):
        x=ws.cell(r,j,c); x.font=fh; x.fill=hdr; x.alignment=Alignment(wrap_text=True,vertical='center')
    if w:
        for j,v in enumerate(w,1): ws.column_dimensions[CL(j)].width=v
R=pd.read_csv('kit_patlatma.csv',dtype={'kit':str}); R=R.sort_values('lines',ascending=False)
R['ek']=(R.lines*(R.n_hucre.fillna(1)-1)).where(R.durum=='bileşen',0)
top5=set(R[R.durum=='HP'].kit)
d0=pd.read_pickle('/home/claude/v70/hat_stogu/df.pkl'); d1=pd.read_pickle('df_kit.pkl')
d0=d0.reset_index(drop=True); d1=d1.reset_index(drop=True); d0['key']=d0.index; d1['key']=d1.index; o=d0.set_index('key'); n=d1.set_index('key')
D=pd.read_pickle('kutu.pkl'); OZ0=json.load(open('/home/claude/v70/hat_stogu/hucre_ozet.json')); OZ1=json.load(open('hs/hucre_ozet.json'))
wb=Workbook()
# ---------- Kit Patlatma
k=wb.active; k.title='Kit Patlatma'
head(k,1,['ikas kit SKU','Kit adı','Durum','Kit satırı/gün','Kit adedi/gün','Hücre bileşen sayısı','Paket masası bileşeni','Hücre satırı/gün','Ön paketle kalırsa tasarruf (satır/gün)','Hazır paket kiti (5)'],[12,46,26,11,11,11,11,12,14,12])
r=2
for _,x in R.iterrows():
    nh=x.n_hucre if pd.notna(x.n_hucre) else (0 if x.durum=='HP' else 1)
    vals=[x.kit,x.ad,x.durum,round(x.lines,2),round(x.d,2),nh,(x.n_masa if pd.notna(x.n_masa) else 0)]
    for j,v in enumerate(vals,1): k.cell(r,j,v).font=f
    k.cell(r,8,f'=D{r}*F{r}').font=f
    k.cell(r,9,f'=IF(C{r}="bileşen",D{r}*(F{r}-1),0)').font=f
    k.cell(r,10,'E' if x.kit in top5 else '').font=f
    for c in (4,5,8,9): k.cell(r,c).number_format='0.0'
    r+=1
KN=r-1
k.cell(r+1,1,'Kaynak: Logo karma koli BOM (Fitness paketi vb tüm bomlar.xlsx) × ikas 2026 Oca–Eki (SKU_Profil). Satır/gün = toplama satırı / 304 gün. HP: hazır pakette yapılan 5 kit (Sedat 20.11: 3 → 5); tekli siparişleri HP\'den çıkar, çok ürünlü siparişte hazır kit kutusu hücreden 1 satır (Hücre bileşen sayısı = 1 − tekli pay). "BOM yok": BOM\'da tanımı olmayan kit kutusu, tek ürün gibi hücreden toplanır (varsayım).').font=Font(name=F,size=9,italic=True)
k.freeze_panes='C2'
# ---------- Bileşen ek talep
b=wb.create_sheet('Bileşen Ek Talep')
head(b,1,['ikas SKU','Ürün','Önceki grup','Önceki günlük adet','Kitten gelen ek adet/gün','Yeni günlük adet','Önceki satır/gün','Yeni satır/gün','Ek satır/gün'],[12,46,12,12,12,12,12,12,12])
r=2
chg=[s for s in n.index if abs(n.at[s,'d_top']-o.at[s,'d_top'])>1e-6 or n.at[s,'grup']!=o.at[s,'grup']]
for s in sorted(chg,key=lambda s:-(n.at[s,'toplama_satiri']-o.at[s,'toplama_satiri'])):
    vals=[n.at[s,'sku'],f"{n.at[s,'urun_adi']} {n.at[s,'varyant'] if pd.notna(n.at[s,'varyant']) else ''}".strip(),o.at[s,'grup'],round(o.at[s,'d_top'],2),round(n.at[s,'d_top']-o.at[s,'d_top'],2),None,round(o.at[s,'toplama_satiri']/304,2),round(n.at[s,'toplama_satiri']/304,2),None]
    for j,v in enumerate(vals,1):
        if v is not None: b.cell(r,j,v).font=f
    b.cell(r,6,f'=D{r}+E{r}').font=f; b.cell(r,9,f'=H{r}-G{r}').font=f
    for c in (4,5,6,7,8,9): b.cell(r,c).number_format='0.0'
    r+=1
BN=r-1
b.cell(r+1,1,'Kitler hücrede bileşen olarak toplanır (v6.7 kararı). BOM\'suz kit kutuları ve kit bileşeni olarak hücreye giren yeni SKU\'lar "Önceki grup" sütununda kit_HP / coklu_baza görünür. Tasarım talebine kit P95 talebi bileşen adediyle eklendi (temkinli).').font=Font(name=F,size=9,italic=True)
b.freeze_panes='C2'
# ---------- Kutu dağılımı
u=wb.create_sheet('Kutu Dağılımı')
P=D.pivot_table(index='desi',columns='ay',values='n',aggfunc='sum').fillna(0)[['Ağustos','Eylül','Ekim']]
head(u,1,['Desi','Ağustos','Eylül','Ekim','Toplam','Pay','Kümülatif pay'],[8,11,11,11,11,9,12])
r=2
for ds,row in P.iterrows():
    u.cell(r,1,ds).font=f
    for j,m in enumerate(['Ağustos','Eylül','Ekim'],2): u.cell(r,j,row[m]).font=blue
    u.cell(r,5,f'=SUM(B{r}:D{r})').font=f; r+=1
UN=r-1
for rr in range(2,UN+1):
    u.cell(rr,6,f'=E{rr}/SUM($E$2:$E${UN})').number_format='0.0%'; u.cell(rr,7,f'=SUM($E$2:E{rr})/SUM($E$2:$E${UN})').number_format='0.0%'
    u.cell(rr,6).font=f; u.cell(rr,7).font=f
u.cell(UN+1,1,'Toplam').font=fb
for j in range(2,6): u.cell(UN+1,j,f'=SUM({CL(j)}2:{CL(j)}{UN})').font=fb
u.cell(UN+3,1,'Kaynak: "Ağustos-eylül-ekim kullanılan Kutu dağılımı.xlsx" (kargo adedi × desi). Günde ≈2.650 kargo; ikas siparişinin ≈%61\'i → büyük olasılıkla desi ile faturalanan taşıyıcılar (HepsiJet + Yurtiçi), Trendyol yok (varsayım).').font=Font(name=F,size=9,italic=True)
# ---------- Araba
a=wb.create_sheet('Araba Göz Tasarımı'); a.column_dimensions['A'].width=46; a.column_dimensions['B'].width=12; a.column_dimensions['C'].width=60
rows=[('GİRDİLER (sarı = değiştirilebilir)',None,None,None),
('Araba dış ölçü: uzunluk (cm)',100,'Sedat 20.11: 70 × 100 × 160',True),('Araba dış ölçü: genişlik (cm)',70,'',True),('Araba yükseklik (cm)',160,'',True),
('Göz hedef hacmi (desi)',10,'Siparişlerin en fazla 10 desi olduğu kabulü (kutu dağılımı ≤10 desi %99,8)',True),
('Göz sayısı: uzunluk boyunca',3,'100 cm / 3 ≈ 33 cm',True),('Göz sayısı: genişlik boyunca (iki yüz)',2,'70 cm / 2 = 35 cm; her yüzden bir sıra',True),
('Dikme / ayırıcı payı (cm)',1.0,'göz başına (1 cm ayırıcı plaka)',True),('Kat aralığı (cm)',30,'göz iç yüksekliği + 2 cm raf',True),('Raf kalınlığı (cm)',2,'',True),
('Ergonomik kat sayısı (taban 50 / 80 / 110 cm)',3,'en alt tabla (≈20 cm) yalnız >10 desi ve büyük sipariş',True),
('P95 dolaşımdaki sipariş-göz (WIP)',456,'Araba ergonomi analizi 19.11 (P95 günü)',True),('Göz doluluğu (sefer başına dolu göz payı)',0.94,'12 gözlü modelde 11,3 / 12',True),('Yedek araba payı',0.10,'',True),
('HESAP',None,None,None),
('Göz iç uzunluk (cm)','=B2/B6-B8','',False),('Göz iç derinlik (cm)','=B3/B7-B8','',False),('Göz iç yükseklik (cm)','=B9-B10','',False),
('Göz iç hacmi (L)','=B16*B17*B18/1000','',False),('Göz hacmi (desi = cm³/3000)','=B16*B17*B18/3000','10 desi = 30 L',False),
('Hedefi karşılıyor mu?','=IF(B20>=B5,"EVET","HAYIR")','',False),
('Göz / kat','=B6*B7','',False),('Göz / araba','=B22*B11','',False),('Sefer başına sipariş','=B23*B13','',False),
('Gereken araba (P95, yedekli)','=ROUNDUP(B12/B24*(1+B14),0)','eski 12 gözlü arabada 40',False),
('Taban kotları (cm)','50 / 80 / 110','en üst göz üst kenarı ≈140 cm; araba 160',False)]
for i,(lab,val,note,inp) in enumerate(rows,1):
    a.cell(i,1,lab).font=fb if val is None else f
    if val is not None:
        c=a.cell(i,2,val); c.font=blue if inp else f
        if inp: c.fill=yel
    if note: a.cell(i,3,note).font=Font(name=F,size=9,italic=True)
for rr in (13,14): a.cell(rr,2).number_format='0%'
for rr in (16,17,18,19,20,24): a.cell(rr,2).number_format='0.0'
# ---------- Kadro etkisi
q=wb.create_sheet('Toplama Yükü'); q.column_dimensions['A'].width=52; q.column_dimensions['B'].width=13; q.column_dimensions['C'].width=13; q.column_dimensions['D'].width=50
S=json.load(open('kit_ozet.json'))
tasarruf=round(R[R.kit.isin(top5)].ek.sum(),1)
hpnew=R[R.kit.isin(['6678637','6550001','6520011'])].d.sum()
L=[('GİRDİLER',None,None,None),('Ek hücre satırı/gün (yıl ortalaması · 5 HP kiti, diğer kitler bileşen)',S['hucre_ek_satir'],None,'kit_patlatma (v7.5)'),
('Karşılaştırma: yalnız 2 Fitness kiti HP (v7.4)',2742,None,'v7.4 hesabı'),
('Toplayıcı hızı (satır/saat)',120,None,'araba modeli (pilotta ölçülecek)'),('Net çalışma (saat/kişi/gün)',7.5,None,''),
('Normal gün / yıl ortalaması (135 bin/ay ÷ 5.291/gün)',0.84,None,'4.440 / 5.291'),('P95 günü / yıl ortalaması',1.60,None,'8.470 / 5.291'),
('SONUÇ','5 HP kiti (v7.5)','2 HP kiti (v7.4)',None),
('Ek satır/gün · normal gün','=B2*B6','=B3*B6',''),('Ek toplayıcı · normal gün','=B9/B4/B5','=C9/B4/B5','kişi'),
('Ek satır/gün · P95','=B2*B7','=B3*B7',''),('Ek toplayıcı · P95','=B11/B4/B5','=C11/B4/B5','kişi'),
('Yeni 3 HP kiti · kit/gün (yıl ort.)',round(hpnew,1),None,'Günlük Vitamin, Whey Protein Paketi, Cream of Rice Paketi'),
('HP kit kurma süresi (sn/kit/kişi)',45,None,'HP cycle time ölçümü: 2 desi 36 sn, 3 desi 53 sn/adet-kişi (varsayım 45)'),
('Ek HP işçiliği · normal gün (saat)','=B13*B6*B14/3600',None,''),('Ek HP işçiliği · P95 (saat)','=B13*B7*B14/3600',None,'')]
for i,(lab,v1,v2,note) in enumerate(L,1):
    q.cell(i,1,lab).font=fb if (v1 is None and v2 is None) or lab=='SONUÇ' else f
    for j,v in ((2,v1),(3,v2)):
        if v is None: continue
        c=q.cell(i,j,v)
        if lab=='SONUÇ': c.font=fb
        elif i<=7 or i in (13,14): c.font=blue; c.fill=yel
        else: c.font=f
        if isinstance(v,str) and v.startswith('='): c.number_format='0.0'
    if note: q.cell(i,4,note).font=Font(name=F,size=9,italic=True)
# ---------- Özet
z=wb.create_sheet('Özet',0); z.column_dimensions['A'].width=60; z.column_dimensions['B'].width=16; z.column_dimensions['C'].width=16
z['A1']='Kazan · kit BOM (5 hazır paket kiti), kutu dağılımı ve araba göz tasarımı · v7.5 · 20.11.2026'; z['A1'].font=Font(name=F,size=13,bold=True)
Z=[('Kit satırı/gün (tüm kit SKU\'ları)',S['kit_satir_gun']),('  HP\'de yapılan 5 kit',S['hp_kit_satir']),('  BOM\'dan bileşene açılan',S['bilesen_kit_satir']),('  BOM\'suz kit kutusu (tek ürün)',S['bomyok_kit_satir']),
('Ek hücre satırı/gün (kitler bileşen olunca)',"='Toplama Yükü'!B2"),('Paket masasına giden bileşen satırı/gün (bar, shaker)',S['masa_ek_satir']),
('Hücre SKU sayısı (önce → sonra)',f"{OZ0['sku_hucre']} → {OZ1['sku_hucre']}"),('Hücre göz ihtiyacı / kapasite (sonra)',f"{OZ1['goz_ihtiyac']} / {OZ1['goz_kap']}"),
('Besleme sıklığı (gün, önce → sonra)',f"{OZ0['T']} → {OZ1['T']}"),('Besleme kalemi/gün (önce → sonra)',f"{OZ0['besleme_kalem_gun']} → {OZ1['besleme_kalem_gun']}"),
('HP\'de yapılan kit (5) satırı/gün',S['hp_kit_satir']),('Ek toplayıcı · normal gün (5 HP kiti)',"='Toplama Yükü'!B10"),('Ek toplayıcı · P95 (5 HP kiti)',"='Toplama Yükü'!B12"),('Ek HP işçiliği · normal gün (saat)',"='Toplama Yükü'!B15"),
('Kargoların 10 desi ve altı payı',"='Kutu Dağılımı'!G11"),('Ortalama desi (3 ay)',round((D.desi*D.n).sum()/D.n.sum(),2)),
('Araba göz hacmi (desi)',"='Araba Göz Tasarımı'!B20"),('Göz / araba',"='Araba Göz Tasarımı'!B23"),('Gereken araba (P95, yedekli)',"='Araba Göz Tasarımı'!B25")]
for i,(lab,v) in enumerate(Z,3):
    z.cell(i,1,lab).font=f; c=z.cell(i,2,v); c.font=f
    if lab.startswith('Kargo'): c.number_format='0.0%'
    elif isinstance(v,str) and v.startswith('='): c.number_format='0.0'
z.cell(len(Z)+4,1,'Sarı hücreler girdi (Araba Göz Tasarımı, Toplama Yükü). Mavi: veri/varsayım, siyah: formül. Kaynaklar her sayfanın altında.').font=Font(name=F,size=9,italic=True)
wb.save('out/Kazan_Kit_Kutu_Araba_v7.5.xlsx'); print('ok',KN,BN,UN,tasarruf)
