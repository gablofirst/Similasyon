import pandas as pd,numpy as np,re,unicodedata
o=pd.read_excel('/home/claude/olcu/o.xlsx');o.columns=['kod','ad','en','boy','yuk','agirlik','tip','not']
o=o.dropna(subset=['en','boy','yuk'])
def vol(r):
    if str(r.tip).upper()=='DOYPACK': return r.en*r.boy*8.0          # poşet: en × boy × ~8 cm
    if abs(r.boy-r.yuk)<1e-6: return r.en*r.en*r.boy   # en = çap/taban, boy = yükseklik (tekrar)
    return r.en*r.boy*r.yuk
o['hacim_olcu']=o.apply(vol,axis=1)
TR=str.maketrans('çğıöşüÇĞİÖŞÜ','cgiosuCGIOSU')
def norm(s):
    s=str(s).translate(TR).lower().replace(',','.')
    s=re.sub(r'\[.*?\]','',s);s=re.sub(r'(\d)\s*(gr|g)\b',r'\1g',s);s=re.sub(r'(\d)\s*kg',r'\1kg',s);s=re.sub(r'(\d)\s*ml',r'\1ml',s)
    s=re.sub(r'[^a-z0-9\.\+ ]',' ',s);return set(t for t in s.split() if t not in('1','x','adet','/','kutu') or t=='kutu')
def wt(ts):return {t for t in ts if re.fullmatch(r'\d+(\.\d+)?(g|kg|ml|lt|l)',t)}
o['tok']=o.ad.map(norm)
d=pd.read_pickle('df.pkl')
d=d.drop(columns=[c for c in ['olcu_ad','hacim_olcu','olcu_tip','skor','agirlik','hacim_kural','hacim_kaynak'] if c in d.columns])
if 'hacim_kural0' in d.columns: d['hacim']=d.hacim_kural0
else: d['hacim_kural0']=d.hacim
rx=re.compile(r'\s*x\s*\d+\s*(Adet|Kutu)\s*$',re.I)
res=[]
for i,r in d.iterrows():
    v=rx.sub('',str(r.varyant) if r.varyant==r.varyant else '')
    t=norm(f'{r.urun_adi} {v}');w=wt(t);best=(0,None)
    for j,q in o.iterrows():
        wq=wt(q.tok)
        if ('tekli' in q.tok)!=('tekli' in t): continue
        if re.search(r'12 Adet',str(r.varyant)) and '12li' not in q.tok: continue
        if w and wq and not (w&wq): continue
        sc=len(t&q.tok)/max(1,len(t|q.tok))
        if sc>best[0]:best=(sc,j)
    if best[0]>=0.5:
        q=o.loc[best[1]];res.append((i,q.ad,q.hacim_olcu,q.tip,best[0],q.agirlik))
m=pd.DataFrame(res,columns=['i','olcu_ad','hacim_olcu','olcu_tip','skor','agirlik']).set_index('i')
d=d.join(m)
d['hacim_kural']=d.hacim_kural0
# "x N Adet" satışlar ana SKU'dan toplanır, hacim tek birim
d['hacim']=np.where(d.hacim_olcu.notna(),d.hacim_olcu,d.hacim_kural)
d['hacim_kaynak']=np.where(d.hacim_olcu.notna(),'güncel ölçü listesi','kap tipi kuralı')
d.to_pickle('df.pkl')
ABC='ABC_satir(toplama_sikligi)'
h=d[(d.grup=='hat')&d[ABC].isin(['A','B'])&(d.d_top>0)]
print('hat SKU',len(h),'ölçüyle eşleşen',h.hacim_olcu.notna().sum())
x=h[h.hacim_olcu.notna()].copy();x['oran']=x.hacim_olcu/x.hacim_kural
print(x[['urun_adi','varyant','olcu_ad','hacim_kural','hacim_olcu','skor']].sort_values('skor').head(15).to_string())
print('oran medyan',x.oran.median().round(2),'büyük sapma',(abs(np.log(x.oran))>0.4).sum())
print(x[abs(np.log(x.oran))>0.4][['urun_adi','varyant','olcu_ad','hacim_kural','hacim_olcu']].head(25).to_string())
print('eşleşmeyen top A:',h[h.hacim_olcu.isna()&(h[ABC]=='A')][['urun_adi','varyant']].head(20).to_string())
