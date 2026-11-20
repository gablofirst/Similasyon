import pandas as pd,numpy as np,math,json,copy
d=pd.read_pickle('df.pkl');A='ABC_satir(toplama_sikligi)'
GV=1.78*0.88*0.50*0.65
c=d[(d.grup=='hat')&(d[A]=='C')&(d.d_top>0)].copy().sort_values('toplama_satiri',ascending=False)
cells0=json.load(open('cells.json'))   # E1/E2 baz hücreleri (2 gün, 5 kat, 9 göz/taraf)
def need(h,T,g):
    st=np.ceil(h.d_tasarim*g*T*1.2).clip(lower=2)   # en az 2 adet
    m3=st*h.hacim/1e6
    b=np.where(m3<=GV/8,8,4)                         # yavaş C: sığarsa 1/8 göz
    slot=np.maximum(1,np.ceil(m3/(GV/b)))
    return st,slot/b
def free_cells(cells):
    # boş kapasiteyi sırala: göz no büyük (B2B besleme ucu) ve üst kat önce → C uzak uca
    fc=[dict(s=x['s'],g=x['g'],k=x['k'],cap=round(1-x['fill'],3)) for x in cells if 1-x['fill']>1e-3]
    return sorted(fc,key=lambda p:(-p['k'],-p['g']))
def plan(lines,g):
    # lines: [(ad,T,cells)]
    h=c.copy();rows=[];L={a:dict(T=T,fc=free_cells(cl),load=0.0,sat=0) for a,T,cl in lines}
    for i,x in h.iterrows():
        # en az yüklü (satır) ve yeri olan hat
        best=None
        for a,v in L.items():
            st,gz=need(h.loc[[i]],v['T'],g);gz=float(gz.iloc[0])
            if sum(p['cap'] for p in v['fc'])+1e-9<gz: continue
            key=(v['sat'],-sum(p['cap'] for p in v['fc']))
            if best is None or key<best[0]: best=(key,a,gz,int(st.iloc[0]))
        if best is None: rows.append([x.sku,x.urun_adi,x.varyant,x.d_top,x.toplama_satiri,'SIĞMADI','',0,0]);continue
        _,a,gz,st=best;v=L[a];left=gz;locs=[]
        for p in v['fc']:
            if left<=1e-9:break
            t=min(p['cap'],left);p['cap']=round(p['cap']-t,3);left-=t;locs.append(f"{p['s']}{p['g']}-K{p['k']}")
        v['fc']=[p for p in v['fc'] if p['cap']>1e-3];v['load']+=gz;v['sat']+=x.toplama_satiri
        rows.append([x.sku,x.urun_adi,x.varyant if x.varyant==x.varyant else '',round(x.d_top,2),int(x.toplama_satiri),a,', '.join(dict.fromkeys(locs)),round(gz,3),st])
    R=pd.DataFrame(rows,columns=['sku','urun','varyant','gunluk_adet','toplama_satiri_10ay','hat','lokasyon','goz','stok_adet'])
    S={a:dict(C_goz=round(v['load'],2),C_satir=v['sat'],kalan_bos=round(sum(p['cap'] for p in v['fc']),2)) for a,v in L.items()}
    return R,S
# E3 2027: 14,26 m → taraf başı 7 göz × 5 kat = 70; günlük besleme. A+B baz yerleşim aynı sırayla (yaklaşık): E3 A+B göz ihtiyacı T=1
import importlib.util,sys
spec=importlib.util.spec_from_file_location('s2','size2.py')
base=d[(d.grup=='hat')&(d[A].isin(['A','B']))&(d.d_top>0)].copy()
def ab_goz(T,n,g):
    h=base.copy();h['st']=np.ceil(h.d_tasarim*g/n*T*1.2);m3=h.st*h.hacim/1e6
    b=np.where(h.hacim<=300,8,4);s=np.maximum(1,np.ceil(m3/(GV/b)));gz=s/b
    lans=h.urun_adi.str.contains('LANSMAN')&(h.XYZ=='Z')&(gz>2)
    return float(gz[~lans].sum())
e3_ab=ab_goz(1,3,1.5);print('E3 A+B göz (günlük besleme, 2027)',round(e3_ab,1),'/ 70')
# E3 hücrelerini kaba kur: 70 göz, A+B dolum sırayla alt-orta katlardan; boşluk üst kat uzak uç
e3=[];rem=e3_ab
order=sorted([(s,g,k) for s in 'BD' for g in range(1,8) for k in range(1,6)],key=lambda t:({2:0,3:0,1:1,4:2,5:3}[t[2]],t[1]))
for s,g,k in order:
    f=min(1,rem);rem-=f;e3.append(dict(s=s,g=g,k=k,fill=f))
R26,S26=plan([('E1',2,copy.deepcopy(cells0)),('E2',2,copy.deepcopy(cells0))],1.0)
R27,S27=plan([('E1',2,copy.deepcopy(cells0)),('E2',2,copy.deepcopy(cells0)),('E3',1,e3)],1.5)
print('2026',S26,'sığmayan',(R26.hat=='SIĞMADI').sum())
print('2027',S27,'sığmayan',(R27.hat=='SIĞMADI').sum())
# herkes her hatta senaryosu
st,gz=need(c,2,1.0);print('C her hatta olsaydı hat başı göz',round(gz.sum()/1,1),'(2 günlük, hat başı talep = toplam/2 değil, min-slot baskın)')
R26.to_csv('/home/claude/C_2026.csv',index=False);R27.to_csv('/home/claude/C_2027.csv',index=False)
json.dump(dict(S26=S26,S27=S27,e3_ab=e3_ab),open('/home/claude/C_ozet.json','w'))
print(R26.head(12).to_string())
