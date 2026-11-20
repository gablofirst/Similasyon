import pandas as pd,matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
h=pd.read_pickle('slotted.pkl');ABC='ABC_satir(toplama_sikligi)'
side=9;GW=1.78;GD=0.88;L=18.02;W=6.56
# göz × kat doluluk ve ABC
occ={}
for _,x in h[h.yer=='göz rafı'].iterrows():
    for tok in str(x.lokasyonlar).split(', '):
        s,rest=tok[0],tok[1:];g,k=rest.split('-K');occ.setdefault((s,int(g)),[]).append((int(k),x[ABC],x.urun_adi+' '+str(x.varyant)))
fig,ax=plt.subplots(figsize=(14,24))
ax.add_patch(Rectangle((0,0),W,L,fill=False,lw=2))
y0=L-2.0  # raf kuzeyden başlar? göz 1 güney (konveyör) ucunda
for s,x0 in [('B',0),('D',W-GD)]:
    for g in range(1,side+1):
        yb=2.0+(g-1)*GW      # güney ucu y=0 tarafında konveyör
        items=occ.get((s,g),[])
        a=sum(1 for k,c,n in items if c=='A');b=len(items)-a
        col='#d9822b' if a>=b and items else ('#5b8bc9' if items else '#eee')
        ax.add_patch(Rectangle((x0,yb),GD,GW,fc=col,alpha=.55,ec='k',lw=.8))
        ax.text(x0+GD/2,yb+GW/2,f'{s}{g}',ha='center',va='center',fontsize=12,fontweight='bold',rotation=90)
        tx=x0-0.12 if s=='B' else x0+GD+0.12
        ax.text(tx,yb+GW/2,f'{len(set(n for k,c,n in items))} SKU\nA {len(set(n for k,c,n in items if c=="A"))} · B {len(set(n for k,c,n in items if c=="B"))}',ha='right' if s=='B' else 'left',va='center',fontsize=9)
# masalar
for i,(ys) in enumerate([1.5+0.0,1.5+5.0+1.28]):
    ax.add_patch(Rectangle(((W-1.8)/2,ys+0.9),1.8,5.0,fc='#c9b48a',ec='k'))
    ax.text(W/2,ys+0.9+2.5,f'MASA {i+1}\n5,0 × 1,8 m',ha='center',va='center',fontsize=11,fontweight='bold')
ax.annotate('',xy=(W/2,-1.2),xytext=(W/2,0.3),arrowprops=dict(arrowstyle='->',lw=2))
ax.text(W/2,-1.6,'GÜNEY UCU · konveyör → sorter → kargo',ha='center',fontsize=12,fontweight='bold')
ax.annotate('',xy=(W/2,L-0.3),xytext=(W/2,L+1.2),arrowprops=dict(arrowstyle='->',lw=2))
ax.text(W/2,L+1.5,'KUZEY UCU · B2B\'den 2 günde bir besleme girişi (masa ile uç arası 4,3 m)',ha='center',fontsize=12,fontweight='bold')
ax.text(-2.2,L/2,'18,02 m',rotation=90,va='center',ha='right',fontsize=12)
ax.text(W/2,L+3.0,'E-TİCARET HAT MODÜLÜ · 2 GÜNDE BİR BESLEME · 18,02 × 6,56 m = 118 m² · 2 × 9 göz × 5 kat = 90 göz (85 dolu, 5 boş)',ha='center',fontsize=13,fontweight='bold')
ax.text(W/2,-2.6,'Göz 1 = konveyör ucu · A ürünler 2.–3. kat ve 1.–3. göz · ağır kavanoz 1.–2. kat · kapsül kutuları 4.–5. kat · SKU listesi: Excel "Hat Stoğu"',ha='center',fontsize=9)
ax.text(W/2,L+2.3,'Kesit: 0,88 raf | 1,50 toplama | 1,80 masa | 1,50 toplama | 0,88 raf  ·  Göz 178 × 88 × 50 cm  ·  Turuncu: ağırlık A · Mavi: B',ha='center',fontsize=10)
ax.set_xlim(-3.0,W+3.0);ax.set_ylim(-3.0,L+3.6);ax.set_aspect('equal');ax.axis('off')
fig.savefig('/home/claude/out/Kazan_Eticaret_Hat_Modulu.png',dpi=110,bbox_inches='tight',facecolor='white')
