import pandas as pd, numpy as np, sys, math
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter
kpi,outx=sys.argv[1],sys.argv[2]
BAR_DISP=12; DISP_PAL=875; ESIK_2YER=0.20  # palet/gün (yüzden), üstü 2 palet yeri
d=pd.read_excel(kpi,sheet_name='Perakende Sipariş',header=3); d=d[d['Ürün'].notna()].copy()
d=d[~(d['BİM siparişi (otomatik)'].eq('Evet')|d['Müşteri'].str.upper().str.startswith('BİM'))]
d['urun']=d['Ürün'].str.strip().str.replace('Protein bar','Protein Bar').str.replace('Fıstık Ezmesi-parçacıklı','Fıstık Ezmesi Parçacıklı')
d['ad']=d.urun+' '+d.Gramaj.astype(int).astype(str)+np.where(d.urun.str.contains('Yağı'),'ml','g')
d['grup']=np.where(d.urun.str.startswith('Protein Bar'),'Protein Bar','Supplement')
w=d[d['Sipariş Tarihi']>='2026-08-01'].copy()
t0,t1=w['Sipariş Tarihi'].min(),w['Sipariş Tarihi'].max()
G=int(np.busday_count(t0.date(),(t1+pd.Timedelta(days=1)).date(),weekmask='1111110'))
w['palet']=np.where(w.grup=='Protein Bar',w['Sipariş Adet']/BAR_DISP/DISP_PAL,np.nan)
w['tam_palet']=w.palet>=1
w['yuz_adet']=np.where(w.tam_palet,(w['Sipariş Adet']-np.floor(w.palet)*BAR_DISP*DISP_PAL),w['Sipariş Adet'])  # tam paletler rezervden, artığı yüzden
g=w.groupby(['grup','ad']).agg(satir=('ad','size'),musteri=('Müşteri','nunique'),adet=('Sipariş Adet','sum'),yuz_adet=('yuz_adet','sum'),tam_palet_satir=('tam_palet','sum')).reset_index()
g['adet_gun']=g.adet/G; g['satir_gun']=g.satir/G
g['yuz_palet_gun']=np.where(g.grup=='Protein Bar',g.yuz_adet/G/BAR_DISP/DISP_PAL,np.nan)
g['toplam_palet_gun']=np.where(g.grup=='Protein Bar',g.adet/G/BAR_DISP/DISP_PAL,np.nan)
g=g.sort_values(['satir'],ascending=False).reset_index(drop=True)
g['yer']=np.where(g.yuz_palet_gun>=ESIK_2YER,2,1)
g.loc[(g.grup=='Protein Bar')&(g.satir<3),'yer']=0  # tek seferlik bar (Batman, Muz?) -> esnek
g.loc[g.ad.str.contains('Muz'),'yer']=1
g.loc[g.ad.str.contains('Batman'),'yer']=0
# pozisyonlar: S1, 9 göz/taraf, 5. göz tünel; göz 1 güney uç
pos=[]
for gz in range(1,10):
    if gz==5: continue
    for f in 'BD':
        for p in 'ABC': pos.append((gz,f,p))
pos.sort(key=lambda t:(t[0],t[1],t[2]))
# yerleştirme: satır sıklığına göre güneyden; 2 yerliler aynı göz/yüz A+B
L=[];used=set()
tri=[(gz,f) for gz in range(1,10) if gz!=5 for f in 'BD']
free=[(gz,f,p) for gz,f in tri for p in 'ABC']
def take(n):
    for i,(gz,f,p) in enumerate(free):
        if n==2 and p=='A' and (gz,f,'B') in free:
            free.remove((gz,f,'A'));free.remove((gz,f,'B'));return f"S1-{f}-{gz:02d}-A + B"
        if n==1:
            free.remove((gz,f,p));return f"S1-{f}-{gz:02d}-{p}"
for _,r in g.iterrows():
    L.append(take(int(r.yer)) if r.yer>0 else 'yüz yok · rezervden / esnek')
g['lokasyon']=L
nposT=len(pos); nused=int(g.yer.sum()); nfree=len(free)
print('pencere',t0.date(),t1.date(),G,'iş günü; satır',len(w),'sipariş',w.groupby(['Müşteri','Sipariş Tarihi']).ngroups)
print(g[['grup','ad','satir','satir_gun','adet_gun','toplam_palet_gun','yuz_palet_gun','tam_palet_satir','yer','lokasyon']].round(2).to_string())
print('S1 palet yeri',nposT,'kullanılan',nused,'esnek',nfree)
b=w[w.grup=='Protein Bar']
pay_tam=b.loc[b.tam_palet,'Sipariş Adet'].sum()/b['Sipariş Adet'].sum()
print('bar tam palet satır payı (adet)',round(pay_tam,3),'satır',int(b.tam_palet.sum()),'/',len(b))
S=dict(G=G,t0=str(t0.date()),t1=str(t1.date()),satir=len(w),siparis=int(w.groupby(['Müşteri','Sipariş Tarihi']).ngroups),
 urun=int((g.satir>0).sum()),bar_gun=float(b['Sipariş Adet'].sum()/G),bar_pal_gun=float(b['Sipariş Adet'].sum()/G/BAR_DISP/DISP_PAL),
 pay_tam=float(pay_tam),nposT=nposT,nused=nused,nfree=nfree,bar_satir_pay=float(len(b)/len(w)))
pd.Series(S).to_json('out/b2b_v64_ozet.json')
# ---- Excel
wb=Workbook();ws=wb.active;ws.title='Özet'
H=Font(bold=True,color='FFFFFF');HF=PatternFill('solid',fgColor='1F4E78');B=Font(bold=True);IN=Font(color='0000FF')
rows=[
 ['B2B (Bim dışı) toplama yüzü · v6.4 taslak · gerçek B2B satışına göre'],
 [f"Kaynak: Haftalık Operasyon KPI Raporu v3_17 (16.11.2026), Perakende Sipariş sayfası, BİM siparişleri hariç. Pencere {t0.date()} – {t1.date()}, {G} iş günü (Pzt–Cmt)."],
 [],
 ['Gösterge','Değer','Not'],
 ['Sipariş satırı',len(w),'Ağustos öncesi 5 satır pencere dışında'],
 ['Sipariş (müşteri + tarih)',S['siparis'],f"günde ≈ {S['siparis']/G:.1f} sipariş"],
 ['Satır / gün',round(len(w)/G,1),None],
 ['Farklı ürün',S['urun'],'10 bar aroması (50 g) + 7 supplement perakende ambalajı'],
 ['Protein bar satır payı',round(S['bar_satir_pay'],3),None],
 ['Bar adet / gün',round(S['bar_gun']),None],
 ['Bar palet / gün',round(S['bar_pal_gun'],2),'varsayım: 12\'li display, 875 display/palet'],
 ['Tam palet ve üstü satırların bar adet payı',round(pay_tam,3),'bu kısım yüzden değil, rezervden tam palet olarak çıkar'],
 [],
 ['Toplama yüzü','Palet yeri',None],
 ['1. sıra alt göz (S1, 9 göz × 2 yüz, 5. göz tünel)',nposT,'v6.3\'te 1.–3. + 5.–6. sıra: 264 palet yeri'],
 ['B2B ürünlerine ayrılan',nused,'günlük yüz tüketimi ≥ 0,20 palet olan bar 2 yer, diğerleri 1 yer'],
 ['Esnek (lansman, ara sıra B2B\'ye giden e-ticaret ürünü)',nfree,None],
 [],
 ['Varsayımlar (mavi = sabit girdi)'],
 ['Display başına bar',BAR_DISP,'12\'li kutu 15,5 × 16 × 6 cm, ≈ 670 g (Ürünlere ait ölçüler)'],
 ['Palet başına display',DISP_PAL,'120 × 80 × 150 cm: 35 display/kat × 25 kat. Gerçek koli/palet dizilimi teyit edilmeli'],
 ['2 palet yeri eşiği (palet/gün, yüzden)',ESIK_2YER,None],
 [],
 ['Kurallar'],
 ['· 1 palet ve üstü satır: rezerv gözünden tam palet indirilir, doğrudan streç → ortak sevk tamponu → rampa. Yüzden toplanmaz.'],
 ['· 1 paletten küçük satır: S1 alt gözünden display/koli toplanır (B1 akışı).'],
 ['· Tek seferlik ürün (ör. Batman bar) ve yüzü olmayan e-ticaret SKU\'su: rezerv gözünden ya da esnek yere indirilerek toplanır.'],
 ['· Paket/kit SKU\'lar (fitness paketi vb.) B2B\'de satılmıyor (Sedat, 17.11). Kapsam dışı.'],
 ['· 2.–3. ve 5.–6. sıraların alt gözleri B2B\'den çıkar, normal rezerv / hat besleme stoğuna döner. Kapasite (3.810) değişmez.'],
]
for r in rows: ws.append(r)
ws['A1'].font=Font(bold=True,size=13)
for c in ('A4','B4','C4','A14','B14','C14'): ws[c].font=H; ws[c].fill=HF
for c in ('A19','A24'): ws[c].font=B
for c in ('B20','B21','B22'): ws[c].font=IN
ws['B9'].number_format='0.0%';ws['B12'].number_format='0.0%'
ws.column_dimensions['A'].width=58;ws.column_dimensions['B'].width=14;ws.column_dimensions['C'].width=80
ws2=wb.create_sheet('Atama')
cols=[('Sıra (satır sıklığı)',None),('Grup',None),('Ürün',None),('Satır',None),('Satır/gün','0.00'),('Müşteri sayısı',None),('Adet/gün','#,##0'),('Palet/gün (toplam)','0.00'),('Palet/gün (yüzden)','0.00'),('Tam palet satır',None),('Palet yeri',None),('Lokasyon',None)]
ws2.append([c for c,_ in cols])
for i,r in g.iterrows():
    ws2.append([i+1,r.grup,r.ad,int(r.satir),r.satir_gun,int(r.musteri),r.adet_gun,None if pd.isna(r.toplam_palet_gun) else r.toplam_palet_gun,None if pd.isna(r.yuz_palet_gun) else r.yuz_palet_gun,int(r.tam_palet_satir),int(r.yer),r.lokasyon])
for j,(c,f) in enumerate(cols,1):
    ws2.cell(1,j).font=H;ws2.cell(1,j).fill=HF;ws2.cell(1,j).alignment=Alignment(wrap_text=True)
    ws2.column_dimensions[get_column_letter(j)].width=max(11,len(c)+2)
    if f:
        for k in range(2,ws2.max_row+1): ws2.cell(k,j).number_format=f
ws2.column_dimensions['C'].width=34;ws2.column_dimensions['L'].width=30
n=ws2.max_row
ws2.append([]);ws2.append(['Toplam',None,None,f'=SUM(D2:D{n})',f'=SUM(E2:E{n})',None,f'=SUM(G2:G{n})',f'=SUM(H2:H{n})',f'=SUM(I2:I{n})',f'=SUM(J2:J{n})',f'=SUM(K2:K{n})'])
for j in range(1,12): ws2.cell(n+2,j).font=B
ws2.freeze_panes='A2'
wb.save(outx)
