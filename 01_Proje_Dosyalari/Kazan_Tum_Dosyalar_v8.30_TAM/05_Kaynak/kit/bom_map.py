# BOM (Logo karma koli) → ikas SKU eşleştirme
import pandas as pd, re, json
def n(x):
    x=str(x).upper().translate(str.maketrans('İIŞĞÜÖÇı','IISGUOCI'))
    x=x.replace('İ','I'); return re.sub(r'[^A-Z0-9]','',x)
d=pd.read_pickle('/home/claude/v70/hat_stogu/df.pkl')
d['ad']=d.urun_adi.fillna('')+' '+d.varyant.fillna(''); d['k']=d.ad.map(n)
b=pd.read_excel('in/bom.xlsx',dtype={'Karma Koli Kodu':str,'Ürün Kodu':str})
b=b[b['Karma Koli Kodu']!='02']
b['kk']=b['Karma Koli Adı'].map(n); b['ck']=b['Ürün Adı'].map(n)
idx={k:s for k,s in zip(d.k,d.sku)}
# önek eşleşmesi (Logo adı 50 karakterde kesik olabilir)
def find(k):
    if k in idx: return idx[k]
    c=[s for kk,s in idx.items() if kk.startswith(k) or k.startswith(kk) and len(kk)>=len(k)-3]
    return c[0] if len(c)==1 else None
b['kit_sku']=b.kk.map(find); b['comp_sku']=b.ck.map(find)
kits=d[d.grup=='kit_HP'].copy()
km=b.dropna(subset=['kit_sku']).kit_sku.unique()
kits['bom']=kits.sku.isin(km)
print('kit_HP SKU',len(kits),'BOM eşleşen',kits.bom.sum(),'talep payı',round(kits[kits.bom].d_top.sum()/kits.d_top.sum(),3))
print('BOM bileşen satırı',len(b),'bileşen eşleşen',b.comp_sku.notna().sum(), 'eşleşmeyen bileşen adları:',b[b.comp_sku.isna()]['Ürün Adı'].value_counts().head(25).to_dict())
miss=kits[~kits.bom].sort_values('d_top',ascending=False)[['sku','ad','d_top']].head(15);print(miss.to_string())
b.to_pickle('bom_m.pkl')
# --- bileşen eşleşmesini iyileştir: barkod + bulanık ad (kit olmayan SKU'lar içinde)
import difflib
d2=d[d.grup.isin(['hat','hediye_masa'])]   # çoklu paket (x2/x3) ve kitler aday değil
bar={str(x).split('.')[0]:s for x,s in zip(d.barkod,d.sku) if pd.notna(x)}
cand={k:s for k,s in zip(d2.k,d2.sku)}
STOP=['LANSMAN','ADET','KUTU','PAKET']
def norm2(k):
    for w in STOP: k=k.replace(w,'')
    return k.replace('G','')
c2={norm2(k):s for k,s in cand.items()}
def fz(name):
    m=re.search(r'\[\s*(\d{8,14})\s*\]',str(name))
    if m and m.group(1) in bar: return bar[m.group(1)],'barkod'
    nm=str(name).upper().replace('MANGO ANANAS','PINEAPPLE MANGO')
    if 'TEKLİ' in nm and 'BAR' in nm:   # tekli bar → 'PROTEİN BAR TEKLİ 30G <aroma>'
        aroma=n(nm.split('TEKLİ')[1]).replace('AND','')
        c=[s for k,s in cand.items() if 'TEKLI' in k and 'BAR' in k and aroma[:5] in k.replace('AND','')]
        return (c[0],'tekli bar') if len(c)>=1 else (None,None)
    k=norm2(n(nm)); nums=set(re.findall(r'\d+',re.sub(r'[,.]','',nm)))
    for r in difflib.get_close_matches(k,list(c2),n=5,cutoff=0.80):
        sku=c2[r]; ad=d.loc[d.sku==sku,'ad'].iloc[0].upper()
        an=set(re.findall(r'\d+',re.sub(r'[,.]','',ad)))
        if nums and not (nums & an): continue          # gramaj/adet tutmalı
        if bool(re.search(r'\bPEA\b',nm)) != bool(re.search(r'\bPEA\b',ad)): continue
        return sku,'ad~'
    return None,None
for i,r in b[b.comp_sku.isna()].iterrows():
    s,how=fz(r['Ürün Adı']); b.at[i,'comp_sku']=s; b.at[i,'how']=how
print('bileşen eşleşen (son)',b.comp_sku.notna().sum(),'/',len(b))
print(b[b.how=='ad~'][['Ürün Adı','comp_sku']].drop_duplicates().merge(d[['sku','ad']],left_on='comp_sku',right_on='sku')[['Ürün Adı','ad']].head(30).to_string())
print('hala yok:',b[b.comp_sku.isna()]['Ürün Adı'].value_counts().to_dict())
b.to_pickle('bom_m.pkl')

# --- ozet
b['comp_grup']=b.comp_sku.map(dict(zip(d.sku,d.grup)))
print(b.comp_grup.value_counts(dropna=False).to_dict())
print('bar tekli/shaker eşleşmeyen → paket masası varsayımı')
b.to_pickle('bom_m.pkl')
