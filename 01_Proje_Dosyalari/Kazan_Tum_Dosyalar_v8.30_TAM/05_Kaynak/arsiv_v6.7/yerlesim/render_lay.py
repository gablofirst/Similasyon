import pickle,json,matplotlib,sys,os;sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)));import hucre_geo as HG;matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.patches import Rectangle
L=json.load(open('/home/claude/work/out/layout.json'))
import os,math
fx=lambda x:83.235+(x-87883)/1001.96
fy=lambda y:30.2-(y-200527)/1001.96
DWG='/home/claude/work/out/dwgbg.pkl'
if os.path.exists(DWG):
    from ezdxf.colors import aci2rgb
    fig,ax=plt.subplots(figsize=(30,12.5))
    for c,segs in pickle.load(open(DWG,'rb')).items():
        S=[q for q in segs if all(30<p[0]<225 and -2<p[1]<80 for p in q)]
        r,g,bb=aci2rgb(c) if 0<c<256 else (0,0,0)
        if (r,g,bb)==(255,255,255):r=g=bb=0
        k=.55;ax.add_collection(LineCollection(S,colors=[((r/255)*(1-k)+k*.82,(g/255)*(1-k)+k*.82,(bb/255)*(1-k)+k*.82)],linewidths=.28,zorder=0))
    X=None;BGNOTE='Gri zemin: ADEYA 22.10 DWG (ihsan orijinal hali).'
elif os.path.exists('/home/claude/work/out/xps.pkl'):
    X=pickle.load(open('/home/claude/work/out/xps.pkl','rb'))
    gx=lambda x:48.1+(x-5534)*0.01913
    gy=lambda y:16.1+(y-3317)*0.019166
    BGNOTE='Gri zemin: ADEYA 22.10 DWFX.'
else:X=None;BGNOTE='Gri zemin: ADEYA 22.10 DWG blok sınırları.'
if 'ax' not in globals():fig,ax=plt.subplots(figsize=(30,12.5))
if X:
    bg={'S#00FFFF':('#7fb3c4',.6),'S#FFFF00':('#c9b84a',.4),'S#B85C00':('#999',.5),'S#FF00FF':('#c040c0',.9),'F#FF00FF':('#c040c0',.9),
        'F#F26722':('#e08a4a',.6),'S#0000FF':('#8aa0d8',.25),'S#808080':('#bbb',.3)}
    for k,(c,w) in bg.items():
        segs=[[(gx(a),gy(b)) for a,b in p] for p,_ in X.get(k,[]) if all(3150<b<6000 for _,b in p) and len(p)>1]
        ax.add_collection(LineCollection(segs,colors=c,linewidths=w))
elif not os.path.exists(DWG):
    segs=[]
    for e in json.load(open('/home/claude/work/out/ins.json')):
        if e['t']=='I' and e.get('bb'):
            a,b,c2,d=e['bb'];r=math.radians(e['r'] or 0);sx,sy=e['sx'],e['sy']
            pts=[]
            for u,v in [(a,b),(c2,b),(c2,d),(a,d),(a,b)]:
                u*=sx;v*=sy;pts.append((fx(e['x']+u*math.cos(r)-v*math.sin(r)),fy(e['y']+u*math.sin(r)+v*math.cos(r))))
            if all(30<p[0]<225 and 0<p[1]<80 for p in pts):segs.append(pts)
        elif e['t']=='P':
            pts=[(fx(x),fy(y)) for x,y in e['pts']]
            if all(30<p[0]<225 and 0<p[1]<80 for p in pts):segs.append(pts)
    ax.add_collection(LineCollection(segs,colors='#a9b3b6',linewidths=.45,zorder=0))
# bina dış hattı ve kuzey şerit (DWFX'te kırpılmış) — as-built kolon ızgarası
ax.add_patch(Rectangle((48.1,6.5),170.8,57.9,fill=False,ec='#222',lw=1.6))
for x in [48.1,65.1,82.1,99.1,116.1,133.2,150.8,167.8,184.8,201.8,218.9]:
    for y in [6.8,16.1,25.7,35.3,44.9,54.5,64.1]:ax.add_patch(Rectangle((x-.3,y-.3),.6,.6,color='#555'))
# as-built iç duvar (ADEYA çiziminde yok)
for y0,y1 in [(7.1,25.7),(45.5,64.1)]:ax.plot([99.4,99.4],[y0,y1],color='#d00',lw=3.2,solid_capstyle='butt')
ax.text(100.3,18.2,'İÇ DUVAR (as-built) · ADEYA çiziminde yok',color='#d00',fontsize=8,fontweight='bold',va='center',zorder=11,bbox=dict(fc='white',ec='#d00',lw=.6,alpha=.92,boxstyle='round,pad=.25'))
ax.add_patch(Rectangle((98.6,44.3),1.6,3.9,fill=False,ec='#d00',lw=1.4,ls='--'))
ax.text(96.9,47.4,'koridor için\n3 m açıklık',color='#d00',fontsize=7.5,ha='right')
# kapılar
for x,w in [(62.5,5),(88.1,5),(123.1,4.15),(157.8,4.15),(191.8,4.15)]:ax.add_patch(Rectangle((x-w/2,6.2),w,.6,color='#2a7'))
for x,w in [(61.5,3),(87.1,3)]+[(c,5.15) for c in (106.1,123.1,140.8,157.8,174.8,191.8,208.8)]:ax.add_patch(Rectangle((x-w/2,64.2),w,.6,color='#2a7'))
C={'canopy':('#6b7a80',.04),'inbound':('#2d7a3e',.16),'aisle':('#8e999c',.10),'buffer':('#3b6ea5',.16),'conv':('#1b2427',.6),'dock':('#5d6b70',.08),'hp':('#9a6a00',.2),'cargo':('#b4491f',.17),'reserve':('#8e999c',.06),'cell':('#0b6e6e',.10),'pack':('#0b6e6e',.06)}
LBL={
 'vas_c':('SEVK TAMPONU\nYÜKLE → 2 rampa\nVAS/Bim + B2B\n97 m²',54.2,29.8,6.5,0),
 'vas_str':('Streç\n34 m²',53.6,36.8,6,0),
 'vas_stk':('STOKLA\n→ B2B / drive-in\n42 m²',54.5,41.7,6,0),
 'vas_g':('YARI MAMÜL BEKLEME · 120 m²',73.2,34.5,6,90),
 'k_hj':('HepsiJet · %65,6 · 199 m²\nayırma masası yanında',116.0,68.9,7,0),
 'hp_hat':('HP paketleme hattı',146.0,55.8,6,90),
 'konv':('',0,0,0,0),'sorter':('K4 saçak bandı ← batıya (K2 141 + K2 123 girer)',127.5,66.3,6,0),'ayirma':('Ayırma masası',107.0,65.35,5.5,0),'kit':('Koli · dolgu\nboş araba parkı\nyedek alan\n86 m²',103.0,56.7,6.5,90),'h_guney1':('Boş araba · koli',111.6,62.2,6.5,0),'h_guney2':('Boş araba · koli',134.6,62.2,6.5,0),'hp_kor1':('HP istif koridoru',143.35,55.7,6,90),'hp_kor2':('HP istif koridoru',148.65,55.7,6,90),'hp_fatura':('Toplama · fatura',147.5,63.05,5.5,0),'hp_konv':('',0,0,0,0),
 'kalite':('Kalite · iade kabul · karantina · K1 61,5\n100 m²',59.6,61.9,7.5,0),
 'rampa':('RAMPA · 303 m² · 2 kapı (Y ≈ 23–34)\nmal kabul + VAS/Bim + B2B sevk\n(teyit: iç mekâna eklenecek alan 1)',42.8,24.0,7,90),
 'et_kamp':('E-TİCARET\nKAMPANYA\nLOKASYONU\nlansman / Z palet\n+ hücre besleme\ntamponu\n216 m²',91.9,56.4,7,0),
 'kor':('Ana forklift koridoru',126.0,46.3,8,0),'di_kor':('Drive-in koridoru',131.0,14.25,8,0),
 'k_ty':('Trendyol · %30,7\ndolu kafes · 95 m²',135.4,67.9,7,0),'lane_w':('Batı forklift şeridi',80.4,28.0,6.5,90),
 'kapi1':('',0,0,0,0),
}
for zz in L['Z']:
    c,a=C[zz['k']];w,h=zz['x1']-zz['x0'],zz['y1']-zz['y0']
    ax.add_patch(Rectangle((zz['x0'],zz['y0']),w,h,fc=c,alpha=a,ec=c,lw=1.1,ls='--' if zz['k'] in('reserve','canopy') else '-'))
    if zz['k']=='canopy':ax.text(zz['x0']+0.4,zz['y1']+0.75,zz['n'],fontsize=6.5,fontweight='bold',color='#3d4a50',ha='left')
    ax.add_patch(Rectangle((zz['x0'],zz['y0']),w,h,fill=False,ec=c,lw=1.1,ls='--' if zz['k']=='reserve' else '-'))
    if zz['k'] in ('cell','pack'):continue
    if zz['id'] in LBL:
        t,lx,ly,fs,rot=LBL[zz['id']]
        if t:ax.text(lx,ly,t,ha='center',va='center',fontsize=fs,fontweight='bold',color='#1b2427',rotation=rot,zorder=6)
    elif (min(w,h)>2.5 or zz['k'] in('conv',)) and zz['n'] and zz['k']!='canopy':
        parts=zz['n'].split(' · ');rot=90 if h>2*w else 0;W=h if rot else w
        fs=max(6.5,min(10.5,W*.9/max(len(s) for s in parts)*3.2))
        txt='\n'.join(parts)+('' if zz['k'] in('aisle','conv','dock') else f'\n{w*h:,.0f} m²'.replace(',','.'))
        ax.text(zz['x0']+w/2,zz['y0']+h/2,txt,ha='center',va='center',rotation=rot,fontsize=fs if zz['k']!='conv' else 7,fontweight='bold' if zz['k']!='aisle' else 'normal',color='#1b2427')
for t,x0,y0,x1,y1 in L['DI']:ax.add_patch(Rectangle((x0,y0),x1-x0,y1-y0,fc='#b45f16',alpha=.35,ec='#b45f16',lw=.5))
ax.text(74,9.8,f"DRIVE-IN BATI · {L['nW']} şerit · {L['cap']['di_w']} palet",ha='center',fontsize=9,fontweight='bold',color='#5a2e08')
ax.text(125.5,9.8,f"DRIVE-IN ORTA · {L['nM']} şerit · {L['cap']['di_m']} palet",ha='center',fontsize=9,fontweight='bold',color='#5a2e08')
for x0,y0,x1,y1 in L['ADEYA_ROWS']:ax.add_patch(Rectangle((x0,y0),x1-x0,y1-y0,fc='#e08a4a',alpha=.35,ec='#b45f16',lw=.8))
for i in L.get('B2BPICK',[]):
    x0,y0,x1,y1=L['ADEYA_ROWS'][i];g=L.get('B2BFACE_GOZ',9);yf=y1-(y1-y0)*g/9
    ax.add_patch(Rectangle((x0-.12,y0),x1-x0+.24,yf-y0,fill=False,ec='#7b3fa0',lw=1.4,ls='--',zorder=5))
    ax.add_patch(Rectangle((x0-.12,yf),x1-x0+.24,y1-yf,fill=False,ec='#7b3fa0',lw=2.4,zorder=5));ax.add_patch(Rectangle((x0,yf),x1-x0,y1-yf,fc='#7b3fa0',alpha=.22,ec='none',zorder=5))
if L.get('B2BPICK'):
    ax.text(88.8,39.6,'B2B YÜZÜ · 1. sıra alt göz 1–3\n18 palet yeri · 17 ürün',ha='center',va='center',fontsize=7.0,fontweight='bold',color='#4b1f66',zorder=11,bbox=dict(fc='white',ec='#7b3fa0',lw=.8,alpha=.93,boxstyle='round,pad=.25'))
    ax.text(88.8,25.0,'1. sıra göz 4–9 · esnek 30\n(lansman / ara sıra B2B)',ha='center',va='center',fontsize=6.4,color='#4b1f66',zorder=11,bbox=dict(fc='white',ec='#7b3fa0',lw=.6,ls='--',alpha=.9,boxstyle='round,pad=.2'))
for x0,y0,x1,y1 in L['ROWS']+L['EXT']:ax.add_patch(Rectangle((x0,y0),x1-x0,y1-y0,fc='#b45f16',alpha=.55,ec='#7a3a0a',lw=1))
ax.text(135,40.0,f"8–12. sıra uzatma +{L['cap']['ext_8_12']}",ha='center',va='center',fontsize=8.5,fontweight='bold',color='#5a2e08',bbox=dict(fc='white',ec='none',alpha=.85))
ax.text(150.0,30.2,f"13. sıra\ntek yüz\n+{L['cap']['row13']}",ha='center',va='center',fontsize=7.5,fontweight='bold',color='#5a2e08',bbox=dict(fc='white',ec='none',alpha=.85))
ax.plot([L['RES_X']]*2,[6.5,64.4],color='#b4491f',lw=2.5,ls='--')
ax.text(113.5,30.2,f"BACK-TO-BACK · ADEYA 22.10\n12 sıra · {L['cap']['adeya']:,} palet".replace(',','.'),ha='center',va='center',fontsize=11,fontweight='bold',color='#5a2e08',bbox=dict(fc='white',ec='none',alpha=.8))
for i,(x0,y0,x1,y1) in enumerate(L['VAS']):
    ax.add_patch(Rectangle((x0,y0),x1-x0,y1-y0,fc='#3b6ea5',alpha=.25 if i<4 else .07,ec='#3b6ea5',lw=1,ls='-' if i<4 else '--'))
    rot=0 if (x1-x0)>(y1-y0) else 90
    ax.text((x0+x1)/2+(0.9 if i<4 else 0),(y0+y1)/2,(f'VAS {i+1} · 65 m²\n← çıkış rampaya' if i<4 else f'VAS {i+1}\n2027 yedek\n65 m²'),ha='center',va='center',fontsize=7.5,fontweight='bold',rotation=rot)
OZ=json.load(open('/home/claude/work/out/hucre_ozet.json')) if os.path.exists('/home/claude/work/out/hucre_ozet.json') else dict(T=3.25)
for hc in L['HUCRE']:
    for r in HG.raf_bantlari(hc):ax.add_patch(Rectangle((r[0],r[1]),r[2]-r[0],r[3]-r[1],fc='#0b6e6e',alpha=.38,ec='#06494a',lw=.6,zorder=3))
    for g in HG.gozler(hc):
        hw=HG.GW/2
        if g['rot']==0:ax.plot([g['x']-hw,g['x']-hw],[g['y']-.44,g['y']+.44],color='#06494a',lw=.5,zorder=3);ax.plot([g['x']+hw,g['x']+hw],[g['y']-.44,g['y']+.44],color='#06494a',lw=.5,zorder=3)
        else:ax.plot([g['x']-.44,g['x']+.44],[g['y']-hw,g['y']-hw],color='#06494a',lw=.5,zorder=3);ax.plot([g['x']-.44,g['x']+.44],[g['y']+hw,g['y']+hw],color='#06494a',lw=.5,zorder=3)
    P=HG.path(hc);xs_,ys_=zip(*P);ax.plot(xs_,ys_,color='#0b6e6e',lw=1.1,ls=(0,(3,2)),zorder=4)
    for k in range(1,len(P)):
        (xa,ya),(xb,yb)=P[k-1],P[k];ax.annotate('',xy=(xa+(xb-xa)*.6,ya+(yb-ya)*.6),xytext=(xa+(xb-xa)*.45,ya+(yb-ya)*.45),arrowprops=dict(arrowstyle='-|>',color='#0b6e6e',lw=1.1),zorder=4)
    ax0,ay0,ax1,ay1=hc['ada']
    ax.text((ax0+ax1)/2,(ay0+ay1)/2,f"HÜCRE {hc['ad'][1]}\n112 m² · 130 göz\n≈{int(OZ['T'])} günde bir\nbesleme",ha='center',va='center',fontsize=6.6,fontweight='bold',color='#063f40',zorder=6)
    ex=hc['x1']+.5 if hc['acik']=='E' else hc['x0']-.5;ym=(hc['y0']+hc['y1'])/2
    ax.text(ex,ym-1.0,'giriş',fontsize=5.5,ha='center',va='center',rotation=90,color='#063f40',zorder=6);ax.text(ex,ym+1.0,'çıkış',fontsize=5.5,ha='center',va='center',rotation=90,color='#063f40',zorder=6)
for p in L['PST']:
    ax.add_patch(Rectangle((p['x']-.4,p['y']-.75),.8,1.5,fc='#c9b48a',ec='#7a6a4a',lw=.5,zorder=3))
ax.text(119.6,56.7,'PAKETLEME · 16 istasyon',rotation=90,ha='center',va='center',fontsize=7,fontweight='bold',color='#063f40',zorder=6)
ax.text(126.6,56.7,'araba park · dönüş',rotation=90,ha='center',va='center',fontsize=6,color='#063f40',zorder=6)
ax.plot([123.1,123.1],[49.6,64.6],color='#1b2427',lw=3.2,zorder=4)

FC={'green':'#2d7a3e','blue':'#1f5fbf','amber':'#c06a00','teal':'#0b6e6e','purple':'#7b3fa0'}
for nm,x0,y0,x1,y1,kat in L['HPR']:
    ax.add_patch(Rectangle((x0,y0),x1-x0,y1-y0,fc='#9a6a00',alpha=.45,ec='#5a3a00',lw=.8))
    dik=(y1-y0)>(x1-x0);n=int(((y1-y0) if dik else (x1-x0))//2.7)
    for i in range(1,n+1):
        if dik:ax.plot([x0,x1],[y0+2.7*i]*2,color='#5a3a00',lw=.6)
        else:ax.plot([x0+2.7*i]*2,[y0,y1],color='#5a3a00',lw=.6)
ax.text(141.2,57.8,'mamül 24 · koli · paketli 24',rotation=90,fontsize=5.2,ha='center',va='center',color='white',fontweight='bold')
ax.text(150.8,56.5,'mamül 24 · paketli 36',rotation=90,fontsize=5.2,ha='center',va='center',color='white',fontweight='bold')
for f in L['FLOW']:
    c=FC[f['c']];p=f['p'];code=f['t'].split(' ')[0]
    xs,ys=zip(*p);ax.plot(xs,ys,color=c,lw=3.0,alpha=.9,solid_capstyle='round',zorder=8)
    ax.annotate('',xy=p[-1],xytext=p[-2],arrowprops=dict(arrowstyle='-|>,head_length=1.0,head_width=.5',color=c,lw=3.0,shrinkA=0,shrinkB=0),zorder=9)
    ax.text(p[0][0],p[0][1],code,fontsize=8,fontweight='bold',color='white',ha='center',va='center',zorder=10,bbox=dict(boxstyle='circle,pad=.18',fc=c,ec='white',lw=1))
for code,x,y,c in L['MARK']:ax.text(x,y,code,fontsize=8,fontweight='bold',color='white',ha='center',va='center',zorder=10,bbox=dict(boxstyle='circle,pad=.18',fc=FC[c],ec='white',lw=1))
for x0,y0,x1,y1,t in L['OPEN']:
    ax.add_patch(Rectangle((x0,y0),x1-x0,y1-y0,fc='white',ec='#d00',lw=1.4,ls='--',zorder=7));ax.text(96.0,64.0,t,color='#d00',fontsize=7,ha='center')
G={'B2B':('purple','B2B SEVK (Bim dışı)'),'MK':('green','MAL KABUL'),'VAS':('blue','VAS SÜRECİ'),'HP':('amber','HAZIR PAKET SÜRECİ'),'ET':('teal','E-TİCARET HÜCRE')}
EXTRA={'V2':'V2 yarı mamül bekleme tamponu (giriş)','H2':'H2 mamül stok · 20 SKU · 7 gün · raf 2 × 24 = 48 ≥ 34 lokasyon'}
for k,x in [('MK',48.5),('VAS',70),('HP',112),('ET',176)]+[('B2B',176)]:
    c,n=G[k];ax.text(x,84.6,n,fontsize=10,fontweight='bold',color=FC[c])
    st=[f['t'] for f in L['FLOW'] if f['f']==k]
    if k=='VAS':st=st[:1]+[EXTRA['V2']]+st[1:]
    if k=='HP':st=st[:1]+[EXTRA['H2']]+st[1:]
    y0=86.4 if k!='B2B' else 93.6
    if k=='B2B':ax.texts[-1].set_y(91.9)
    for j,t in enumerate(st):ax.text(x,y0+j*1.55,t,fontsize=8.6,color='#1b2427')
B=L['BAR'];xs=[B['a'][0]];gs=sorted(B['gates'])
cur=B['a'][0]
for c,w in gs:
    ax.plot([cur,c-w/2],[B['a'][1]]*2,color='#9a6a00',lw=2.2);ax.plot([c-w/2,c+w/2],[B['a'][1]]*2,color='#b4491f',lw=1.2,ls=':');cur=c+w/2
ax.plot([cur,B['b'][0]],[B['a'][1]]*2,color='#9a6a00',lw=2.2)
cp=L['cap']
ax.text(48.5,78.6,f"Toplam {cp['total']:,} palet  =  ADEYA B2B {cp['adeya']:,}  +  8–12. sıra uzatma {cp['ext_8_12']}  +  13. sıra {cp['row13']}  +  drive-in {cp['di_w']+cp['di_m']:,}   ·   rezerv alan (X ≥ 151,9) kullanılmadı".replace(',','.'),fontsize=12.5,fontweight='bold')
ax.text(48.5,81.0,"Kuzey yukarıda. Ölçüler metre, as-built 02.11.2026 koordinatı. "+BGNOTE+" Kırmızı: ADEYA çiziminde olmayan as-built iç duvar. Yeşil: kapılar. Kesikli: yedek / rezerv.",fontsize=9.5,color='#444')
ax.set_title('PROTEIN OCEAN KAZAN · 3.800 PALET · E-TİCARET 2 KARE HÜCRE (ARABALI TOPLAMA) + HAZIR PAKET · KARGO DIŞ SAÇAKTA · 19.11.2026 · v6.7',fontsize=15,fontweight='bold',loc='left')
ax.plot([35,221],[74.6,74.6],color='#c040c0',lw=1.4,ls='-.');ax.text(36,74.2,'arsa sınırı',color='#c040c0',fontsize=8)
ax.set_xlim(35,221);ax.set_ylim(97.5,3.5);ax.set_aspect('equal');ax.axis('off')
fig.savefig('/home/claude/work/out/Kazan_3800_Palet_Yerlesim_Onerisi.png',dpi=130,bbox_inches='tight',facecolor='white')
