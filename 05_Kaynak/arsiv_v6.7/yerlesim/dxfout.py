import json,ezdxf
from ezdxf.enums import TextEntityAlignment
L=json.load(open('/home/claude/work/out/layout.json'))
K=1001.96
X=lambda x:87883+(x-83.235)*K
Y=lambda y:200527-(y-30.2)*K
doc=ezdxf.new('R2010',setup=True);doc.units=4;msp=doc.modelspace()
LAY={'canopy':('PO_SACAK',6),'inbound':('PO_MAL_KABUL',3),'aisle':('PO_KORIDOR',8),'buffer':('PO_VAS_TAMPON',5),'conv':('PO_KONVEYOR',7),'dock':('PO_SEVK',9),
     'hp':('PO_HAZIR_PAKET',40),'cargo':('PO_KARGO',1),'reserve':('PO_REZERV',8)}
for n,c in list(LAY.values())+[('PO_DRIVEIN_YENI',30),('PO_B2B_YENI',30),('PO_VAS_HAT',5),('PO_ETICARET_HAT',4),('PO_BARIYER',2),('PO_BARIYER_KAPI',1),('PO_UYARI',1),('PO_YAZI',7)]:
    if n not in doc.layers:doc.layers.add(n,color=c)
def rect(layer,x0,y0,x1,y1):msp.add_lwpolyline([(X(x0),Y(y0)),(X(x1),Y(y0)),(X(x1),Y(y1)),(X(x0),Y(y1))],close=True,dxfattribs={'layer':layer})
def txt(s,x,y,h,layer='PO_YAZI',rot=0):
    t=msp.add_text(s,height=h*1000,rotation=rot,dxfattribs={'layer':layer,'style':'OpenSans'});t.set_placement((X(x),Y(y)),align=TextEntityAlignment.MIDDLE_CENTER)
for z in L['Z']:
    ly=LAY[z['k']][0];rect(ly,z['x0'],z['y0'],z['x1'],z['y1'])
    w,h=z['x1']-z['x0'],z['y1']-z['y0'];parts=z['n'].split(' · ')
    if not z['n']:continue
    th=max(.35,min(1.2,min(w,h)/(len(parts)+3),w/max(len(p) for p in parts)*1.5))
    if not z['n']:continue
    if min(w,h)<2.5:txt(z['n'],z['x0']+w/2,z['y0']+h/2,.45)
    else:
        for j,p in enumerate(parts):txt(p,z['x0']+w/2,z['y0']+h/2-(len(parts)-1)*th*.7+j*th*1.4,th if j==0 else th*.8)
        if z['k'] not in('aisle','conv','dock'):txt(f"{w*h:,.0f} m2".replace(',','.'),z['x0']+w/2,z['y0']+h/2+(len(parts)+.3)*th*.75,th*.7)
for t,x0,y0,x1,y1 in L['DI']:rect('PO_DRIVEIN_YENI',x0,y0,x1,y1)
cp=L['cap']
txt(f"DRIVE-IN BATI {L['nW']} SERIT x 20 = {cp['di_w']} PALET",74,10,.8,'PO_DRIVEIN_YENI')
txt(f"DRIVE-IN ORTA {L['nM']} SERIT x 20 = {cp['di_m']} PALET",125.5,10,.8,'PO_DRIVEIN_YENI')
for x0,y0,x1,y1 in L['EXT']:rect('PO_B2B_YENI',x0,y0,x1,y1);rect('PO_B2B_YENI',x0,y0,(x0+x1)/2-.125,y1)
for x0,y0,x1,y1 in L['ROWS']:rect('PO_B2B_YENI',x0,y0,x1,y1)
txt(f"8-12. SIRA UZATMA Y 35,8-44,2 = +{cp['ext_8_12']} PALET",133,45.0-0.5,.5,'PO_B2B_YENI')
txt(f"13. SIRA TEK YUZ = +{cp['row13']} PALET",150,15.4,.45,'PO_B2B_YENI')
msp.add_line((X(L['RES_X']),Y(6.5)),(X(L['RES_X']),Y(64.4)),dxfattribs={'layer':'PO_UYARI'})
txt('REZERV SINIRI X=151,9 - DOGUSU KULLANILMADI',L['RES_X']+12,4.5,.7,'PO_UYARI')
for i,(x0,y0,x1,y1) in enumerate(L['VAS']):rect('PO_VAS_HAT',x0,y0,x1,y1);txt(f"VAS {i+1}"+(' 2027 yedek' if i>3 else ' - cikis bati ucu rampaya')+' 65 m2',(x0+x1)/2,(y0+y1)/2,.55,'PO_VAS_HAT',0 if (x1-x0)>(y1-y0) else 90)
for i,(x0,y0,x1,y1) in enumerate(L['E']):rect('PO_ETICARET_HAT',x0,y0,x1,y1);txt((f"E{i+1} aktif 18,02x6,56=118 m2 - 2 gunde bir besleme - bati ucu besleme, dogu ucu cikis" if i<2 else "E3 2027 14,26x6,56 - gunluk besleme"),(x0+x1)/2,(y0+y1)/2,.42,'PO_ETICARET_HAT')
B=L['BAR'];y=B['a'][1];cur=B['a'][0]
for c,w in sorted(B['gates']):
    msp.add_line((X(cur),Y(y)),(X(c-w/2),Y(y)),dxfattribs={'layer':'PO_BARIYER'});msp.add_line((X(c-w/2),Y(y)),(X(c+w/2),Y(y)),dxfattribs={'layer':'PO_BARIYER_KAPI'});cur=c+w/2
msp.add_line((X(cur),Y(y)),(X(B['b'][0]),Y(y)),dxfattribs={'layer':'PO_BARIYER'})
for y0,y1 in [(7.1,25.7),(45.5,64.1)]:msp.add_line((X(99.4),Y(y0)),(X(99.4),Y(y1)),dxfattribs={'layer':'PO_UYARI'})
txt('AS-BUILT IC DUVAR - ADEYA CIZIMINDE YOK - TEYIT',104,26.8,.6,'PO_UYARI')
rect('PO_UYARI',98.6,44.3,100.2,48.2);txt('KORIDOR ICIN 3 M ACIKLIK',104,49.6-3,.45,'PO_UYARI')
txt(f"PROTEIN OCEAN KAZAN - 3.800 PALET YERLESIM ONERISI v6.4 - 2 RAMPA - B2B YUZU 1. SIRA - C HATTA - VAS RAMPADA - KARGO DIS SACAKTA - 2 GUNLUK HAT STOGU - 17.11.2026 - TOPLAM {cp['total']} PALET",130,75.8,1.4)
txt(f"ADEYA B2B {cp['adeya']} + 8-12 UZATMA {cp['ext_8_12']} + 13. SIRA {cp['row13']} + DRIVE-IN {cp['di_w']+cp['di_m']} - REZERV KULLANILMADI | Bu dosya ADEYA 22.10 DWG ile ayni koordinatta: 0,0 noktasina olcek 1 ile INSERT/XREF",130,77.4,.7)

import math
TR=str.maketrans('çğıöşüÇĞİÖŞÜ→≥·','cgiosuCGIOSU>>-')
a=lambda t:t.translate(TR)
FL={'purple':('PO_AKIS_B2B_SEVK',6),'green':('PO_AKIS_MAL_KABUL',3),'blue':('PO_AKIS_VAS',5),'amber':('PO_AKIS_HAZIR_PAKET',40),'teal':('PO_AKIS_ETICARET',4)}
for n,c in list(FL.values())+[('PO_HP_RAF',42),('PO_B2B_TOPLAMA_YUZU',6),('PO_B2B_ESNEK',6)]:
    if n not in doc.layers:doc.layers.add(n,color=c)
def arrow(ly,pts):
    P=[(X(x),Y(y)) for x,y in pts]
    (x1,y1),(x2,y2)=P[-2],P[-1];L=math.hypot(x2-x1,y2-y1);ux,uy=(x2-x1)/L,(y2-y1)/L;hl,hw=1100,520
    bx,by=x2-ux*hl,y2-uy*hl
    msp.add_lwpolyline(P[:-1]+[(bx,by)],dxfattribs={'layer':ly,'const_width':220})
    msp.add_solid([(x2,y2),(bx-uy*hw,by+ux*hw),(bx+uy*hw,by-ux*hw)],dxfattribs={'layer':ly})
def mark(ly,code,x,y):
    msp.add_circle((X(x),Y(y)),650,dxfattribs={'layer':ly});txt(code,x,y,.6,ly)
for f in L['FLOW']:
    ly=FL[f['c']][0];arrow(ly,f['p']);mark(ly,f['t'].split(' ')[0],*f['p'][0])
for code,x,y,c in L['MARK']:mark(FL[c][0],code,x,y)
for nm,x0,y0,x1,y1,kat in L['HPR']:
    rect('PO_HP_RAF',x0,y0,x1,y1)
    for i in range(1,int((x1-x0)//2.7)+1):msp.add_line((X(x0+2.7*i),Y(y0)),(X(x0+2.7*i),Y(y1)),dxfattribs={'layer':'PO_HP_RAF'})
    txt(a({'mamul':'MAMUL RAF 2 goz x3x4 = 24','koli':'KOLI / AMBALAJ RAFI','paketli':'PAKETLI STOK RAF 4 goz x3x4 = 48 - zemin toplama yuzu'}[nm]),(x0+x1)/2,(y0+y1)/2,.35,'PO_HP_RAF')
for i in L.get('B2BPICK',[]):
    x0,y0,x1,y1=L['ADEYA_ROWS'][i];g=L.get('B2BFACE_GOZ',9);yf=y1-(y1-y0)*g/9
    rect('PO_B2B_TOPLAMA_YUZU',x0-.12,yf,x1+.12,y1);rect('PO_B2B_ESNEK',x0-.12,y0,x1+.12,yf)
txt('B2B YUZU - 1. SIRA ALT GOZ 1-3 - 18 PALET YERI - 17 URUN',88.8,39.6,.45,'PO_B2B_TOPLAMA_YUZU')
txt('1. SIRA GOZ 4-9 - ESNEK 30 PALET YERI',88.8,25.0,.4,'PO_B2B_ESNEK')
for x0,y0,x1,y1,t in L['OPEN']:rect('PO_UYARI',x0,y0,x1,y1);txt(a(t),95.5,64.0,.4,'PO_UYARI')
LEG={'green':('MAL KABUL',['M1 mal kabul > drive-in / B2B']),
 'blue':('VAS',['V1 yari mamul al (drive-in W / B2B)','V2 yari mamul bekleme tamponu','V3 uret (VAS 1-4)','V4 hat sonu paletle > strec > palet karti','V5 YUKLE > rampa (Bim / FTL)',"V5' STOKLA > ana koridor > B2B / drive-in"]),
 'amber':('HAZIR PAKET',['H1 20 SKU mamul al (B2B > HP besleme seridi > duvar acikligi)','H2 mamul stok 7 gun: raf 24 + yer 10','H3 HP hattinda paketle','H4 paketli stok palette 7 gun: raf 48','H5 siparis topla + fatura/etiket yapistir','H6 konveyor > sorter > K2 141/106 > kargo kafesi']),
 'teal':('E-TICARET',['E1 B2B > hat besleme (2 gunde bir)','E2 hat cikisi > konveyor > sorter > K2 kapi > arac (yoksa sacak kafesi)']),
 'purple':('B2B SEVK',['B1 Bim disi topla (1. sira alt goz 1-3) > strec > sevk tamponu > rampa','1 palet ve ustu siparis: rezervden tam palet > strec > sevk tamponu'])}
for i,(c,(h,lines)) in enumerate(LEG.items()):
    x=50+i*24;ly=FL[c][0];txt("AKIS - "+h,x+8,79.2,.8,ly)
    for j,t in enumerate(lines):
        tt=msp.add_text(t,height=480,dxfattribs={'layer':ly,'style':'OpenSans'});tt.set_placement((X(x),Y(80.6+j*1.1)),align=TextEntityAlignment.LEFT)

doc.saveas('/home/claude/work/out/Kazan_3800_Palet_Yerlesim_Onerisi.dxf')
print('ok',len(msp))
