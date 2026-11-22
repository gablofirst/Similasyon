# v8.30: tünelsiz kaçış (v8.12). Kullanım: python3 tunelsiz.py veri/layout.json kacis/kacis.py → 2 tünel 44,3 m · tünelsiz 61,6 m (596 m² > 45)
# v8.30: tünelsiz kaçış mesafesi, v8.12 yerleşimi (K5 + geçit, saçakta yalnız 125,4/160,1)
import numpy as np, sys
LJ,KP=sys.argv[1],sys.argv[2]; sys.argv=['x',LJ]; exec(open(KP).read().split('g0=base()')[0])
g0=base()
for r in L.get('KAMP_PAL',[]): block(g0,*r)
block(g0,155.75,62.8,166.6,63.3); block(g0,155.75,62.8,156.25,64.4); block(g0,159.5,62.8,160.7,63.3,0)
SA=[60.8,86.4,104.5,121.3,139.1,156.0,173.2,190.0,207.2,81.2,108.4,125.4,143.1,160.1,177.1,194.1,211.1]
SAC=[x for x in SA if not 100<x<165]+[125.4,160.1]
mask=np.zeros_like(g0,bool); mask[iy(7.3):, ix(48.4):ix(168.5)]=True
for ad,N,T in [('2 tünel (81,2/125,4) + 160,1/194,1',[160.1,194.1,81.2,125.4],[81.2,125.4]),
               ('tünelsiz: kuzeyde yalnız 160,1/194,1',[160.1,194.1],[])]:
    g,D=run(g0,SAC,N,T); M=np.where((g==0)&mask&np.isfinite(D),D,np.nan)
    a,b=np.unravel_index(np.nanargmax(M),M.shape)
    print(f'{ad:40s} en uzun {np.nanmax(M):5.1f} m @({X0+b*R:.1f},{Y0+a*R:.1f}) · 45 m üstü {np.nansum(M>45)*R*R:.0f} m²')
