import numpy as np, itertools, sys
sys.argv=['x','/home/claude/z/05_Kaynak/veri/layout.json']
exec(open('kacis.py').read().split('g0=base()')[0])
g0=base()
mask=np.zeros_like(g0,bool); mask[iy(7.3):, ix(48.4):ix(151.6)]=True
def ev(t):
    g,D=run(g0,SOUTH,NORTH_OPEN+list(t),list(t))
    M=np.where((g==0)&mask&np.isfinite(D),D,np.nan)
    a,b=np.unravel_index(np.nanargmax(M),M.shape)
    cw=M[iy(12.6):iy(16.0), ix(48.4):ix(98.8)]; cm=M[iy(12.6):iy(16.0), ix(99.5):ix(151.5)]
    return round(float(np.nanmax(M)),1),(round(X0+b*R,1),round(Y0+a*R,1)),round(float(np.nansum(M>45)*R*R)),round(float(np.nanmax(cw)),1),round(float(np.nanmax(cm)),1)
print('0 tünel',ev([]))
N=[60.8,86.4,121.9]
for k in (1,2):
    for t in itertools.combinations(N,k): print(t,ev(t))
for t in [(73.0,),(73.0,125.0),(70.0,120.0),(75.0,135.0)]: print('serbest',t,ev(t))
