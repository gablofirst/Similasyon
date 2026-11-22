# v8.11 ek kontrol: hücre raf bantları, döngü koridoru, kampanya palet sıraları × as-built duvar/kolon
import json,pickle,sys
sys.path.insert(0,'yerlesim'); import hucre_geo as HG
L=json.load(open('/home/claude/work/out/layout.json')); P=pickle.load(open('/home/claude/work/out/asb_plan.pkl','rb'))
W=[]
for ly in ('DUVAR','PARAPET DUVAR','İÇ CEPHE SANDWICH PANEL','KOLON'):
    for s in P.get(ly,[]):
        xs=[p[0] for p in s];ys=[p[1] for p in s]
        if 95<min(xs)<175 and 40<min(ys)<70: W.append((ly,min(xs),min(ys),max(xs),max(ys)))
def hit(a,b,c,d):
    return [(ly,round(x0,2),round(y0,2)) for ly,x0,y0,x1,y1 in W if min(c,x1)-max(a,x0)>0.02 and min(d,y1)-max(b,y0)>0.02]
R=[]
for h in L['HUCRE']:
    for r in HG.raf_bantlari(h): R.append((h['ad']+' raf',)+tuple(r))
    c=HG.RD; R.append((h['ad']+' ada',)+tuple(h['ada']))
for i,r in enumerate(L['KAMP_PAL']): R.append(('kampanya palet sırası %d'%(i+1),)+tuple(r))
for i,r in enumerate(L['VAS'][4:]): R.append(('VAS %d'%(i+5),)+tuple(r))
bad=0
for n,a,b,c,d in R:
    H=hit(a,b,c,d)
    if H: bad+=1; print('ÇAKIŞMA',n,[round(v,2) for v in (a,b,c,d)],H)
# döngü koridoru içinde kolon var mı (H2 adası içi beklenir)
for h in L['HUCRE']:
    for ly,x0,y0,x1,y1 in W:
        if ly!='KOLON': continue
        if h['x0']-0.5<x0<h['x1']+0.5 and h['y0']-0.5<y0<h['y1']+0.5:
            ax0,ay0,ax1,ay1=h['ada']; yer='ada içi' if (ax0<=x0 and x1<=ax1 and ay0<=y0 and y1<=ay1) else 'çevre'
            print(h['ad'],'kolon',round(x0,2),round(x1,2),round(y0,2),round(y1,2),yer)
print('raf/palet çakışması',bad)
