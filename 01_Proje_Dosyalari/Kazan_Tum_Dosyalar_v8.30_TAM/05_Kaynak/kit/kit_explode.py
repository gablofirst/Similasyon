# Kit talebini bileşenlere aç → yeni df (hücre modeli için), etki özeti
import pandas as pd, numpy as np, json
d=pd.read_pickle('/home/claude/run/v70/hat_stogu/df.pkl').copy()
b=pd.read_pickle('bom_m.pkl')
d['ad']=d.urun_adi.fillna('')+' '+d.varyant.fillna('')
# çoklu paket → baz SKU
base={}
for _,r in d[d.grup=='coklu_baza'].iterrows():
    m=d[(d.urun_adi==r.bk_urun)&(d.varyant==r.bk_var)]
    if len(m): base[r.sku]=(m.sku.iloc[0],float(r.carpan or 1))
HP_KIT={'6568112','6567672','6568150','6678637','6550001','6520011'}   # v8.x: 6 HP kiti (+Fitness Çikolata/Ahududu)   # v7.5: 5 hazır paket kiti — Fitness Çikolata/Karpuz, Bisküvi/Ahududu, Günlük Vitamin, Whey Protein Paketi, Cream of Rice Paketi
bom={k:list(zip(g.comp_sku,g.Miktar,g.comp_grup)) for k,g in b.dropna(subset=['kit_sku']).groupby('kit_sku')}
grp=dict(zip(d.sku,d.grup))
def explode(sku,q=1.0,depth=0):
    out=[]
    for c,m,cg in bom.get(sku,[]):
        if pd.isna(c): out.append((None,q*m)); continue
        if c in base: c,k=base[c]; m=m*k
        if grp.get(c)=='kit_HP' and c in bom and depth<3: out+=explode(c,q*m,depth+1)
        else: out.append((c,q*m))
    return out
rows=[];add=dict()
kits=d[d.grup=='kit_HP']
for _,k in kits.iterrows():
    if k.sku in HP_KIT:   # tekli siparişler HP'den çıkar; çok ürünlü siparişte hazır kit kutusu hücreden 1 satır
        rows.append(dict(kit=k.sku,ad=k.ad,durum='HP',lines=k.toplama_satiri/304,d=k.d_top,n_hucre=round(1-float(k.tekli_siparis_pay or 0),3),n_masa=0)); continue
    if str(k.sku)=='6000490':   # v8.x: 32'li paket = 3 farklı aroma 12'li display, siparişte toplanır (3 satır)
        disp=d[(d.urun_adi=='PROTEİN BAR')&d.varyant.astype(str).str.endswith('/ 12 Adet')&(d.d_top>0)]
        w=disp.d_top/disp.d_top.sum()
        for c,wi in zip(disp.sku,w):
            a=add.setdefault(c,[0.0,0.0,0.0]); a[0]+=k.d_top*3*wi; a[1]+=k.d_tasarim*3*wi; a[2]+=k.toplama_satiri/304*3*wi
        rows.append(dict(kit=k.sku,ad=k.ad,durum='bileşen',lines=k.toplama_satiri/304,d=k.d_top,n_hucre=3,n_masa=0,n_yok=0)); continue
    comps=explode(k.sku)
    if not comps:
        rows.append(dict(kit=k.sku,ad=k.ad,durum='BOM yok → tek ürün (hücre)',lines=k.toplama_satiri/304,d=k.d_top,n_hucre=1,n_masa=0)); continue
    nh=nm=nx=0
    for c,q in comps:
        g=grp.get(c)
        if c is None: nx+=1; continue
        if g=='hediye_masa': nm+=1; continue
        nh+=1
        a=add.setdefault(c,[0.0,0.0,0.0]); a[0]+=k.d_top*q; a[1]+=k.d_tasarim*q; a[2]+=k.toplama_satiri/304
    rows.append(dict(kit=k.sku,ad=k.ad,durum='bileşen',lines=k.toplama_satiri/304,d=k.d_top,n_hucre=nh,n_masa=nm,n_yok=nx))
R=pd.DataFrame(rows)
# yeni df: bileşen talebi ekle, BOM'suz kitleri hücreye al
n=d.copy(); n['toplama_satiri']=n.toplama_satiri.astype(float)
for c,(a0,a1,ln) in add.items():
    i=n.index[n.sku==c]
    if not len(i): continue
    i=i[0]
    if n.at[i,'grup']!='hat': n.at[i,'grup']='hat'
    n.at[i,'d_top']+=a0; n.at[i,'d_tasarim']+=a1; n.at[i,'toplama_satiri']+=ln*304
nob=R[R.durum.str.startswith('BOM yok')|(R.durum=='HP')].kit   # BOM'suz kutular ve HP kit kutuları hücrede tek SKU
n.loc[n.sku.isin(nob),'grup']='hat'
for s_ in HP_KIT:   # HP kitlerinin yalnız çok ürünlü sipariş payı hücrede
    m=n.sku==s_; p=1-n.loc[m,'tekli_siparis_pay'].fillna(0)
    for c in ('toplama_satiri','d_top','d_tasarim'): n.loc[m,c]=n.loc[m,c]*p
n.to_pickle('df_kit.pkl')
S=dict(
 kit_satir_gun=round(R.lines.sum(),1),
 hp_kit_satir=round(R[R.durum=='HP'].lines.sum(),1),
 bilesen_kit_satir=round(R[R.durum=='bileşen'].lines.sum(),1),
 bomyok_kit_satir=round(R[R.durum.str.startswith('BOM yok')].lines.sum(),1),
 hucre_ek_satir=round((R.lines*R.n_hucre.fillna(0)).sum(),1),
 hp_kit_adet=round(R[R.durum=='HP'].d.sum(),1),
 masa_ek_satir=round((R.lines*R.n_masa.fillna(0)).sum(),1),
 eslesmeyen_bilesen_satir=round((R.lines*R.n_yok.fillna(0)).sum(),1),
 yeni_hucre_sku=int(sum(1 for c in add if grp.get(c)!='hat'))+int(len(nob)),
 bilesen_sku=len(add))
print(json.dumps(S,ensure_ascii=False,indent=1))
R.sort_values('lines',ascending=False).to_csv('kit_patlatma.csv',index=False)
print(R.sort_values('lines',ascending=False).head(15).to_string())
json.dump(S,open('kit_ozet.json','w'),ensure_ascii=False)
