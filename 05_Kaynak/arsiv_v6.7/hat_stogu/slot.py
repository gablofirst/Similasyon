import pandas as pd,numpy as np,math
R=pd.read_pickle('runs.pkl')
r=[x for x in R if x['T']==2 and x['lv']==5 and x['g']==1.0][0]
h=r['h'].copy();side=r['side'];LV=5
# pozisyonlar: taraf (B/D), göz no 1 = konveyör (güney) ucu, kat 1 alt
pos=[]
for s in ['Batı','Doğu']:
    for g in range(1,side+1):
        for k in range(1,LV+1):
            pos.append(dict(taraf=s,goz=g,kat=k,cap=1.0))
pen={1:1.0,2:0.0,3:0.0,4:1.2,5:2.5}
def score(p,heavy,small):
    k=p['kat'];pp=pen[k]
    if heavy: pp+= {1:-0.5,2:0,3:1.0,4:9,5:99}[k]
    if small: pp+= {1:2,2:0.5,3:0,4:-0.6,5:-0.8}[k]
    return p['goz']*1.0+pp
ABC='ABC_satir(toplama_sikligi)'
h=h.sort_values('toplama_satiri',ascending=False)
rows=[]
for i,x in h.iterrows():
    if x.yer!='göz rafı':
        rows.append((i,'-','-','-',''));continue
    heavy=x.hacim>=2434;small=x.hacim<=300
    best=None
    for sd in ['Batı','Doğu']:
        order=sorted([p for p in pos if p['cap']>1e-6 and p['taraf']==sd],key=lambda p:score(p,heavy,small))
        need=x.goz;plan=[];sc=0
        for p in order:
            if need<=1e-9:break
            t=min(p['cap'],need);need-=t;plan.append((p,t));sc+=score(p,heavy,small)*t
        if need<=1e-9 and (best is None or sc<best[0]):best=(sc,plan)
    used=best[1]
    for p,t in used:
        p['cap']-=t;p.setdefault('items',[]).append([x.urun_adi+' '+(str(x.varyant) if x.varyant==x.varyant else ''),x[ABC],round(t,3)])
    f=used[0][0]
    span=', '.join(f"{p['taraf'][0]}{p['goz']}-K{p['kat']}" for p,t in used)
    rows.append((i,f['taraf'],f['goz'],f['kat'],span))
S=pd.DataFrame(rows,columns=['i','taraf','goz_no','kat','lokasyonlar']).set_index('i')
h=h.join(S)
h.to_pickle('slotted.pkl')
free=sum(p['cap'] for p in pos);print('kapasite',len(pos),'boş göz',round(free,2))
print(h[['urun_adi','varyant',ABC,'goz','taraf','goz_no','kat','lokasyonlar']].head(30).to_string())

import json
cells=[dict(s=p['taraf'][0],g=p['goz'],k=p['kat'],fill=round(1-p['cap'],3),items=p.get('items',[])) for p in pos]
json.dump(cells,open('cells.json','w'),ensure_ascii=False)
print('cells',len(cells))
