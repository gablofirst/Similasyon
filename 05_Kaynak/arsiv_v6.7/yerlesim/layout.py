# v6.6 — e-ticaret: 2 kare hücre (10,6 × 10,6, arabalı toplama, tek yön döngü) + ortada paketleme (16 istasyon, konveyör K2 123) + HP doğuda (ana koridordan beslenir); hat (E1–E3) ve ana konveyör kaldırıldı · v6.4 — B2B yüzü yalnız 1. sıra alt göz 1–3 (18 yer) + esnek; 5.–6. sıra ve B1' kaldırıldı; serbest alan VAS için · v6.3 — 2 rampa VAS sevk tamponu hizasında; B2B (Bim dışı) toplama rampaya yakın 1–3. sıra alt göz; sevk tamponu VAS/Bim + B2B ortak; eski B2B hazırlık → e-ticaret kampanya lokasyonu; C kategorisi hatlarda · v6.2 — etiket çakışmaları giderildi (rozet konumu 'b', V1/V3/V4/V5/H3/H5/H6 yolları) · v6 — akış okları, VAS/HP süreç sırası · v3 — rezerv (X ≥ 151,9) kullanılmadan
import json
LANE_W,LANE_D,LANE_P=1.43,5.2,20
ROW_W,ROW_LEN,GOZ=2.37,28.2,2.82
RES_X=151.9
Z=[]
def z(i,k,n,x0,y0,x1,y1):Z.append(dict(id=i,k=k,n=n,x0=x0,y0=y0,x1=x1,y1=y1))
DI=[]
def lanes(tag,x0,x1,y0=7.2):
    n=int((x1-x0+1e-6)//LANE_W)
    for i in range(n):DI.append((tag,x0+i*LANE_W,y0,x0+(i+1)*LANE_W,y0+LANE_D))
    return n
nW=sum(lanes('W',a,b) for a,b in [(49.0,59.0),(66.0,84.6),(91.6,99.0)])
nM=sum(lanes('M',a,b) for a,b in [(100.0,120.0),(126.2,151.5)])
# ADEYA 8–12. sıraların uzatılması (Y 35,8 → 44,2): 3 göz × 2 yüz × 12
EXT=[(x0,35.8,x0+ROW_W,44.2) for x0 in (121.11,126.75,132.42,138.12,143.82)]
EXT_P=len(EXT)*3*2*12
# 13. sıra: tek yüz (doğu yüzü rezerve bakar), tam boy, 10 göz × 12 − 1 tünel (6)
ROWS=[(149.47,16.1,149.47+1.05,44.3)]
ROW13_P=10*12-6
z('rampa','inbound','RAMPA · 2 kapı (VAS sevk tamponu hizası) · mal kabul + VAS/Bim + B2B sevk',37.6,7.0,48.0,36.1)
z('kabul','inbound','Mal kabul · FTL boşaltma · rampa kuzey yarısı',49.2,16.1,76.0,22.4)
z('vas_c','buffer','YÜKLE · sevk tamponu · VAS/Bim + B2B (Bim dışı) → 2 rampa',49.2,22.8,57.6,34.4)
z('vas_str','buffer','Streç · palet kartı · WMS etiket',49.2,34.8,57.6,38.8)
z('vas_stk','buffer','STOKLA · stoğa dönüş tamponu',49.2,39.2,57.6,44.2)
z('vas_g','buffer','YARI MAMÜL BEKLEME · VAS giriş tamponu · drive-in / B2B\'den',70.4,22.8,76.0,44.2)
z('kalite','inbound','Kalite · iade kabul · karantina · K1 61,5',49.2,59.5,70.0,64.3)
z('serbest','reserve','SERBEST ALAN · VAS kullanımı olası',49.2,48.6,70.0,59.1)
z('et_kamp','buffer','E-TİCARET KAMPANYA LOKASYONU · lansman / Z palet · hücre besleme tamponu',85.0,48.6,98.8,64.3)
z('di_kor','aisle','Drive-in koridoru',49.0,12.4,151.5,16.1)
z('kor','aisle','Ana forklift koridoru',49.2,44.3,151.5,48.2)
z('lane_w','aisle','Batı forklift şeridi',76.0,16.1,82.0,44.3)
# VAS: 4 aktif hat yatay (12 × 5,4), giriş doğu ucu, çıkış batı ucu → rampa tamponu
VAS=[(58.0,22.6+i*5.4,70.0,22.6+(i+1)*5.4) for i in range(4)]+[(70.6,49.0,76.0,61.0),(76.6,49.0,82.0,61.0)]
# ---- v6.6 e-ticaret: 2 kare hücre + paketleme + HP ----
E=[]   # hat yok (geriye uyum)
HS=10.6; RD=0.88; AI=1.5; GW=1.78; HLV=5
def hucre(ad,x0,y0,acik):   # acik: 'E' (doğu kenarında giriş/çıkış) | 'W'
    x1,y1=x0+HS,y0+HS; ym=(y0+y1)/2
    return dict(ad=ad,x0=x0,y0=y0,x1=x1,y1=y1,acik=acik,giris=(ym-2.0,ym),cikis=(ym,ym+2.0),
                ada=(x0+RD+AI,y0+RD+AI,x1-RD-AI,y1-RD-AI))
HUCRE=[hucre('H1',106.3,49.0,'E'),hucre('H2',129.3,49.0,'W')]
for h in HUCRE:z(h['ad'].lower(),'cell',f"HÜCRE {h['ad'][1]}",h['x0'],h['y0'],h['x1'],h['y1'])
z('paket','pack','PAKETLEME · 16 istasyon',117.4,49.0,128.8,64.4)
z('konv','conv','Konveyör K1 → K2 123 → K4 saçak bandı',122.7,49.6,123.5,64.4)
z('kit','hp','Koli-dolgu · boş araba parkı · yedek alan',100.2,49.0,105.8,64.4)
z('h_guney1','aisle','Boş araba · koli',106.3,60.0,116.9,64.4)
z('h_guney2','aisle','Boş araba · koli',129.3,60.0,139.9,64.4)
# HP (doğu): kuzeyden ana koridordan beslenir, güneyde K2 141'den saçağa
z('hp_kor1','aisle','HP istif koridoru',141.8,49.0,144.9,62.4)
z('hp_kor2','aisle','HP istif koridoru',147.1,49.0,150.2,62.4)
z('hp_hat','hp','HP paketleme hattı',145.0,50.0,147.0,61.6)
z('hp_fatura','hp','Toplama · fatura / etiket',144.9,62.5,150.2,63.6)
z('hp_konv','conv','',140.8,63.7,150.2,64.3)
z('kapi1','aisle','K2 141',139.3,63.7,140.8,64.4)
# raf hatları (tek derin, 2,7 m göz × 3 palet; dikey = göz Y boyunca)
HPR=[('mamul',140.6,49.4,141.8,54.8,4),('mamul',150.2,49.4,151.4,54.8,4),('koli',140.6,55.1,141.8,57.8,3),('paketli',140.6,58.1,141.8,63.5,4),('paketli',150.2,55.1,151.4,63.5,4)]
PST=[]   # paket istasyonları: konveyörün iki yanında 8'er
for i in range(8):
    y=49.6+i*1.85+0.925
    PST.append(dict(id=f'P{i+1:02d}',taraf='B',x=122.3,y=y)); PST.append(dict(id=f'P{i+9:02d}',taraf='D',x=123.9,y=y))
# DIŞ ALAN · üstü kapalı saçak (aynı X hizası)
z('sacak','canopy','DIŞ ALAN · ÜSTÜ KAPALI SAÇAK · Y 64,7–71,0',100.2,64.7,151.5,71.0)
z('sorter','conv','K4 saçak toplama bandı · doğudan batıya',110.0,65.0,141.0,65.7)
z('ayirma','conv','Biriktirme · ayırma masası · kargo ekibi',104.0,65.0,110.0,65.7)
z('k_hj','cargo','HepsiJet · %65,6 · ayırma masası yanında',100.2,65.8,132.3,71.0)
z('k_ty','cargo','Trendyol · %30,7 · dolu kafes itilir',132.6,65.8,148.0,71.0)
z('k_yk','cargo','Yurtiçi · %3,4',148.3,65.8,151.5,71.0)
z('serit','dock','Kargo aracı yanaşma şeridi ≈3,6 m · mevcut otopark taşınmalı',100.2,71.0,151.5,74.6)
z('rezerv','reserve','KALAN ALAN / REZERV · uzatmayla 4.000 m² üzeri · bu planda kullanılmadı',RES_X,6.8,218.6,64.3)
FLOW=[
 dict(f='MK',c='green',p=[(43,11),(55,14.2),(110,14.2)],t='M1 mal kabul → drive-in / B2B'),
 dict(f='VAS',c='blue',p=[(70,12.6),(79,14.2),(79,24.6),(75.6,24.6)],t='V1 yarı mamül al'),
 dict(f='VAS',c='blue',p=[(72.6,42.6),(69.6,42.6)],t='V3 üret'),
 dict(f='VAS',c='blue',p=[(59.4,36.6),(57.3,36.6)],t='V4 paletle · streç'),
 dict(f='VAS',c='blue',p=[(50.3,35.6),(50.3,24.3),(46.5,24.3)],t='V5 yükle → rampa'),
 dict(f='VAS',c='blue',p=[(50.3,40.6),(50.3,46.6),(90,46.6)],t='V5\' stokla → B2B / drive-in'),
 dict(f='HP',c='amber',p=[(146.0,44.2),(146.0,46.4),(143.3,46.4),(143.3,50.6)],t='H1 20 SKU mamül al (ana koridordan)'),
 dict(f='HP',c='amber',p=[(146.0,51.2),(146.0,60.4)],t='H3 paketle'),
 dict(f='HP',c='amber',p=[(147.5,57.0),(149.8,57.0)],t='H4 paketli stok · palet 7 gün'),
 dict(f='HP',c='amber',p=[(148.6,59.2),(148.6,62.4)],t='H5 sipariş topla · fatura yapıştır'),
 dict(f='HP',c='amber',p=[(149.6,64.0),(141.0,64.0),(141.0,65.35),(133.0,65.35)],t='H6 → K2 141 → K4 bant (batıya)'),
 dict(f='B2B',c='purple',p=[(88.3,44.2),(88.3,45.9),(51.7,45.9),(51.7,32.6),(46.5,32.6)],t='B1 B2B topla (1. sıra alt göz 1–3) → streç → sevk → rampa'),
 dict(f='ET',c='teal',p=[(118.0,44.2),(118.0,46.4),(111.6,46.4),(111.6,49.4)],t='E1 B2B → hücre besleme (3 günde bir)'),
 dict(f='ET',c='teal',p=[(116.4,54.3),(119.4,54.3)],t='E2 12 gözlü araba → paket istasyonu'),
 dict(f='ET',c='teal',p=[(123.1,51.0),(123.1,65.35),(110.4,65.35)],t='E3 konveyör → K2 123 → K4 → ayırma masası'),
]
MARK=[('V2',73.2,27.2,'blue'),('H2',141.2,52.0,'amber')]
OPEN=[]
BAR=dict(a=(49.2,48.3),b=(151.5,48.3),gates=[(60,3.5),(79.3,3.5),(91.9,3.5),(111.6,3.5),(134.6,3.5),(146.0,3.5)])
ADEYA_B2B=2256
B2BSLOW=[]        # v6.4: yavaş bölge kaldırıldı (5.–6. sıra rezerve döndü)
B2BPICK=[0]       # v6.4: yalnız 1. sıra (X 82–84,4). Güney 3 göz B2B yüzü, kalan göz esnek
B2BFACE_GOZ=3     # güney uçtan B2B'ye ayrılan göz sayısı (9 gözün)
cap=dict(adeya=ADEYA_B2B,ext_8_12=EXT_P,row13=ROW13_P,di_w=nW*LANE_P,di_m=nM*LANE_P)
cap['total']=sum(cap.values())
json.dump(dict(Z=Z,DI=DI,ROWS=ROWS,EXT=EXT,VAS=VAS,E=E,HUCRE=HUCRE,PST=PST,HS=HS,BAR=BAR,FLOW=FLOW,HPR=HPR,MARK=MARK,OPEN=OPEN,cap=cap,nW=nW,nM=nM,RES_X=RES_X,B2BPICK=B2BPICK,B2BSLOW=B2BSLOW,B2BFACE_GOZ=B2BFACE_GOZ,ADEYA_ROWS=json.load(open('/home/claude/work/out/layout_v61.json'))['ADEYA_ROWS']),open('/home/claude/work/out/layout.json','w'),ensure_ascii=False)
print(cap,nW,nM)
