import pandas as pd,numpy as np,json,math
d=pd.read_pickle('df.pkl');A='ABC_satir(toplama_sikligi)'
s=d[d.grup.isin(['hat','hediye_masa'])&(d.d_top>0)].copy().sort_values('toplama_satiri',ascending=False).reset_index(drop=True)
s['sira']=range(1,len(s)+1)
# pozisyonlar: sıra -> taraf başı göz sayısı; tünel = orta göz (varsayım), göz başı 3 palet yeri (A,B,C)
ROWS={1:9,2:10,3:10,5:10,6:10}
TUN={r:(n+1)//2 for r,n in ROWS.items()}
pos=[]
for r,n in ROWS.items():
    for g in range(1,n+1):           # göz 1 = güney uç (ana koridor / B1 çıkışı)
        if g==TUN[r]:continue
        for f in ['B','D']:
            for p in 'ABC':
                pos.append(dict(sira=r,yuz=f,goz=g,yer=p,bolge='hızlı' if r<=3 else 'yavaş'))
P=pd.DataFrame(pos)
# yürüme sırası: hızlı bölge: sıra 1→3, göz güneyden kuzeye; yavaş: sıra 5→6
P['oncelik']=P.sira*100+P.goz*2+(P.yuz=='D')
P=P.sort_values('oncelik').reset_index(drop=True)
nF=(P.bolge=='hızlı').sum();nS=(P.bolge=='yavaş').sum();print('hızlı',nF,'yavaş',nS)
# hedef: hızlı bölgeye en hızlı SKU'lar, ilk K tanesi 2 göz. yavaş bölgede tam palet + yarım palet (kuyruk)
def plan(K):
    fast=s.iloc[:0]
    # hızlı bölge: K SKU ×2 + M SKU ×1 = nF  → M = nF-2K
    M=nF-2*K;nfast=K+M
    rest=len(s)-nfast
    # yavaş: x tam + y yarım; x + y/2 <= nS ; x+y=rest → y = 2*(rest - nS) (en az)
    y=max(0,2*(rest-nS));x=rest-y
    return K,M,x,y
for K in [20,30,40]:print(plan(K))
K,HALF=30,60
nF1=nF-2*K
s['bolge']=np.where(s.sira<=K+nF1,'hızlı (1–3. sıra)','yavaş (5–6. sıra)')
s['goz_tipi']=np.select([s.sira<=K,s.sira<=K+nF1,s.sira<=len(s)-HALF],['tam palet ×2','tam palet','tam palet'],'yarım palet')
fpP=P[P.bolge=='hızlı'];sp=P[P.bolge=='yavaş'].to_dict('records')
loc=lambda p,h='':f"S{p['sira']}-{p['yuz']}-{p['goz']:02d}-{p['yer']}{h}"
tri=[g.sort_values('yer').to_dict('records') for _,g in sorted(fpP.groupby(['sira','goz','yuz']),key=lambda t:t[1].oncelik.min())]
pairs=[(t[0],t[1]) for t in tri[:K]]
singles=sorted([t[2] for t in tri[:K]]+[q for t in tri[K:] for q in t],key=lambda q:q['oncelik']*10+'ABC'.index(q['yer']))
L=[];pi=0;qi=0
for _,x in s.iterrows():
    if x.sira<=K:a1,b1=pairs[pi];pi+=1;L.append(loc(a1)+' + '+b1['yer'])
    elif x.sira<=K+nF1:L.append(loc(singles[qi]));qi+=1
    else:L.append(None)
assert qi==len(singles),(qi,len(singles))
si=0;half=0
for i,x in s.iterrows():
    if L[i] is not None:continue
    if x.goz_tipi=='tam palet':L[i]=loc(sp[si]);si+=1
s['lokasyon']=L
# yarım paletler: kalan yavaş pozisyonlardan, pozisyon başı 2 SKU (sol/sağ)
hs=s[s.goz_tipi=='yarım palet'].index.tolist()
for j,i in enumerate(hs):
    p=sp[si+j//2];s.at[i,'lokasyon']=loc(p,'1' if j%2==0 else '2')
si+=math.ceil(len(hs)/2)
bos=len(sp)-si
tot=s.toplama_satiri.sum()
ozet=s.groupby(['bolge','goz_tipi']).agg(sku=('sku','count'),satir=('toplama_satiri','sum')).reset_index()
ozet['satir_pay']=ozet.satir/tot
print(ozet.to_string());print('yavaş bölgede boş pozisyon',bos,'(yarım: ',bos*2,')')
print('ABC dağılımı',pd.crosstab(s.bolge,s[A]))
s[['sira','sku','urun_adi','varyant',A,'toplama_satiri','d_top','bolge','goz_tipi','lokasyon']].to_pickle('/home/claude/b2b_atama.pkl')
json.dump(dict(nF=int(nF),nS=int(nS),K=K,HALF=HALF,bos=int(bos)),open('/home/claude/b2b_ozet.json','w'))
