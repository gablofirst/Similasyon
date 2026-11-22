import pandas as pd,numpy as np,math,json
d=pd.read_pickle('df.pkl')
G_W,G_D,G_H,FILL=1.78,0.88,0.50,0.65
GV=G_W*G_D*G_H*FILL
SAFE=1.2
ABC='ABC_satir(toplama_sikligi)'
W_LINE=0.88+1.5+1.8+1.5+0.88
TABLE_L=2*5.0+1.28
base=d[(d.grup=='hat')&(d[ABC].isin(['A','B']))&(d.d_top>0)].copy().sort_values('toplama_satiri',ascending=False)
# lansman/kampanya: güncel hız çok yüksek ve Z → hat sonu palet önü
base['lansman']=base.urun_adi.str.contains('LANSMAN')&(base.XYZ=='Z')
def run(T,n_lines=2,levels=4,growth=1.0,pallet_thr=2.0):
    h=base.copy();h['d_tasarim']=h.d_tasarim*growth
    h['hat_basi_d']=h.d_tasarim/n_lines
    h['stok_adet']=np.ceil(h.hat_basi_d*T*SAFE)
    h['stok_m3']=h.stok_adet*h.hacim/1e6
    h['bolme']=np.where(h.hacim<=300,8,4)          # küçük ürün 1/8 göz, diğer 1/4
    h['slot']=np.maximum(1,np.ceil(h.stok_m3/(GV/h.bolme)))
    h['goz']=h.slot/h.bolme
    h['yer']=np.where(h.lansman&(h.goz>pallet_thr),'kampanya lokasyonu (palet)','göz rafı')
    g=h[h.yer=='göz rafı'];p=h[h.yer!='göz rafı']
    goz=math.ceil(g.goz.sum())
    h['palet']=np.where(h.yer!='göz rafı',np.ceil(h.stok_m3/1.0),0)   # palet başı ~1,0 m3 ürün
    npal=int(h.palet.sum())
    per_lvl=math.ceil(goz/levels)
    side=math.ceil(per_lvl/2)                       # iki uzun kenar, uçlar açık
    L=max(TABLE_L+3.0, side*G_W+2.0)
    # palet önü: hat sonunda arka tarafta 1,2 m derin şerit, palet başına 0,9 m
    A=L*W_LINE
    return dict(T=T,n=n_lines,lv=levels,g=growth,sku=len(h),sku_pal=len(p),goz=goz,palet=npal,L=round(L,2),W=round(W_LINE,2),per_lvl=per_lvl,side=side,
                m2_hat=round(A,1),m2_top=round(A*n_lines,1),h=h)
out=[]
for growth,n in [(1.0,2),(1.5,3)]:
    for T in [1,2]:
        for lv in [4,5]:
            r=run(T,n,lv,growth);out.append(r);print({k:v for k,v in r.items() if k!='h'})
r=run(1,2,4);h=r['h']
print(h[h.yer!='göz rafı'][['urun_adi','varyant','d_tasarim','stok_adet','goz','palet']])
print(h.groupby(ABC).goz.sum())
pd.to_pickle(out,'runs.pkl')
