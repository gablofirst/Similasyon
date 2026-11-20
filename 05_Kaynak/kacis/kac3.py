import numpy as np, sys
sys.argv=['x','/home/claude/z/05_Kaynak/veri/layout.json']
exec(open('kacis.py').read().split('g0=base()')[0])
g0=base()
mask=np.zeros_like(g0,bool); mask[iy(7.3):, ix(48.4):ix(151.6)]=True
SOUTH_ALL=[60.8,86.4,104.5,121.3,139.1,156.0,173.2,190.0,207.2]+[81.2,108.4,125.4,143.1,160.1,177.1,194.1,211.1]
def ev(south,north_exits,tunnels):
    g,D=run(g0,south,north_exits,tunnels)
    M=np.where((g==0)&mask&np.isfinite(D),D,np.nan)
    a,b=np.unravel_index(np.nanargmax(M),M.shape)
    return round(float(np.nanmax(M)),1),(round(X0+b*R,1),round(Y0+a*R,1)),round(float(np.nansum(M>45)*R*R)),g,M
for name,s,n,t in [
 ('yeni: tünelsiz, kuzey açık 160,1+194,1', SOUTH_ALL,[160.1,194.1],[]),
 ('yeni: tünel 81,2+125,4', SOUTH_ALL,[81.2,125.4,160.1,194.1],[81.2,125.4]),
 ('eski güney listesi + tünel 81,2+125,4', SOUTH,[81.2,125.4,160.1,194.1],[81.2,125.4]),
]:
    r=ev(s,n,t); print(name, r[:3])
