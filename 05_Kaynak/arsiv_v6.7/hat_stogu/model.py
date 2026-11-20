import pandas as pd,numpy as np,re,math,json,sys
P=pd.read_csv('prof.csv',encoding='utf-8-sig',dtype={'sku':str})
sys.path.insert(0,'.')
from vol import vol
P['sku']=P['sku'].str.strip();df=P.copy()
# --- sınıflar
rx=re.compile(r'\s*x\s*(\d+)\s*(Adet|Kutu)\s*$',re.I)
def base_key(r):
    v=str(r.varyant) if pd.notna(r.varyant) else ''
    m=rx.search(v)
    return (r.urun_adi.strip(), rx.sub('',v).strip(), int(m.group(1)) if m else 1)
k=df.apply(base_key,axis=1);df['bk_urun']=[a for a,b,c in k];df['bk_var']=[b for a,b,c in k];df['carpan']=[c for a,b,c in k]
HED=re.compile(r'POCKET SHAKER|TESTER|HUNİ|PILLBOX|PROTEİN BAR TEKLİ|KARIŞTIRICI',re.I)
KIT=re.compile(r'PAKET|KARMA KUTU|PRATİK KUTU',re.I)   # hazır paket / kit
df['grup']='hat'
df.loc[df.urun_adi.str.contains(HED),'grup']='hediye_masa'
df.loc[(df.grup=='hat')&df.urun_adi.str.contains(KIT),'grup']='kit_HP'
df.loc[df.carpan>1,'grup']='coklu_baza'   # x N adet -> ana SKU'ya eklenir
act=df.aktif_son30.astype(str).str.lower().eq('true')
# talep: güncel hız
df['d0']=df[['son90_gunluk_ort','son30_gunluk_ort']].max(axis=1).fillna(0)
# çoklu satışları ana SKU'ya ekle
idx={(r.bk_urun,r.bk_var):i for i,r in df[df.carpan==1].iterrows()}
df['d_ek']=0.0;orph=0
for i,r in df[df.grup=='coklu_baza'].iterrows():
    j=idx.get((r.bk_urun,r.bk_var))
    if j is not None: df.at[j,'d_ek']+=r.d0*r.carpan
    else: orph+=1
df['d_top']=df.d0+df.d_ek
pk=df['pik_katsayi_p95/ort'].fillna(2).clip(upper=3.0)
df['d_tasarim']=df.d_top*pk
# hacim (ölçü listesi kap tipleri)
vv=[vol(a,b) for a,b in zip(df.urun_adi,df.varyant)]
df['hacim']=[a for a,b in vv];df['kap']=[b for a,b in vv]
df.to_pickle('df.pkl')
print('SKU',len(df),'orph',orph)
print(df.groupby(['ABC_satir(toplama_sikligi)','grup']).size().unstack(fill_value=0))
print(df.kap.value_counts().head(20))
