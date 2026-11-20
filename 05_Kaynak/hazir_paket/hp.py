import pandas as pd, json, sys
t=pd.read_csv(sys.argv[1])
d=pd.read_pickle('/home/claude/hs/df.pkl').set_index('sku')
t['u']=t.son90_gunluk*t.adet
g=t.groupby('sku').agg(urun=('urun_adi','first'),var=('varyant','first'),sip=('son90_gunluk','sum'),u=('u','sum')).sort_values('sip',ascending=False)
g=g[~g.urun.str.contains('PAKET|KARMA|SHAKER|HUNİ|KORSE')]  # paket/kit ve aksesuar HP dışı
top=g.head(20).copy()
top['hacim']=[d.hacim.get(s,1500) for s in top.index]
top['pik']=[min(d['pik_katsayi_p95/ort'].get(s,1.8),3) for s in top.index]
PAL=1.2*0.8*1.5*0.75*1e6  # cm3 kullanılabilir/palet
top['mamul_m3_7g']=top.u*7*1.2*top.hacim/1e6
top['mamul_pal']=(top.u*7*1.2*top.hacim/PAL)
top['paket_pal']=(top.sip*7*1.2*top.hacim*1.9/PAL)  # koli+dolgu ≈1,9×
top['paket_pal_tepe']=(top.sip*7*top.pik*top.hacim*1.9/PAL)
pd.set_option('display.width',200)
print(top[['urun','var','sip','u','hacim','mamul_pal','paket_pal','paket_pal_tepe']].round(1))
s=dict(sip=top.sip.sum(),u=top.u.sum(),share=top.sip.sum()/ (t.son90_gunluk.sum()),mamul=top.mamul_pal.sum(),paket=top.paket_pal.sum(),tepe=top.paket_pal_tepe.sum(),
       mamul_lok=int(sum(max(1,round(x+0.49)) for x in top.mamul_pal)),paket_lok=int(sum(max(1,round(x+0.49)) for x in top.paket_pal)))
print(s);top.to_csv('hp_top20.csv');json.dump(s,open('hp_sum.json','w'))
