# as-built (cm) -> plan (m) dönüşümü ve PNG kontrol
import pickle,sys,matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
S=pickle.load(open('/home/claude/asb/asb_raw.pkl','rb'))
px=lambda x:48.1+(x-8706)/100
py=lambda y:6.48+(11530-y)/100
COL={'DUVAR':'#c00','KOLON':'#000','SEKSİYONEL KAPI':'#0a0','KAPI YANGIN':'#f80','DOĞRAMA':'#06c','PARAPET DUVAR':'#a0a','İÇ CEPHE SANDWICH PANEL':'#f0f','CEPHE SANDWICH PANEL':'#555','0':'#08a','MOB':'#888','ZEMIN':'#999','NPI PROFİL':'#666','BETON ÇATI MAKASI':'#ddd','YAZI':'#333'}
P={}
for L,v in S.items():
    P[L]=[[(px(a),py(b)) for a,b in s] for s in v]
pickle.dump(P,open('/home/claude/work/out/asb_plan.pkl','wb'))
x0,x1,y0,y1=[float(a) for a in sys.argv[1:5]] if len(sys.argv)>4 else (30,225,-5,80)
fig,ax=plt.subplots(figsize=(min(30,(x1-x0)/4),min(18,(y1-y0)/4)))
for L,v in P.items():
    if L in('AGAC','ANTED','TEL ÇİT','BAHÇE DUVARI','KOT','DÖŞEME','TOPRAK ALTI','BETON ÇATI MAKASI'):continue
    ss=[s for s in v if any(x0<p[0]<x1 and y0<p[1]<y1 for p in s)]
    ax.add_collection(LineCollection(ss,colors=COL.get(L,'#bbb'),linewidths=.7,label=L))
ax.set_xlim(x0,x1);ax.set_ylim(y1,y0);ax.set_aspect('equal');ax.grid(alpha=.3)
ax.set_xticks(range(int(x0),int(x1),5 if x1-x0<80 else 10))
plt.savefig(sys.argv[5] if len(sys.argv)>5 else '/home/claude/asb/asb.png',dpi=110,bbox_inches='tight')
