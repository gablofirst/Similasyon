import numpy as np, sys, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
sys.argv=['x','/home/claude/z/05_Kaynak/veri/layout.json']
exec(open('kacis.py').read().split('g0=base()')[0])
g0=base()
mask=np.zeros_like(g0,bool); mask[iy(7.3):, ix(48.4):ix(151.6)]=True
SA=[60.8,86.4,104.5,121.3,139.1,156.0,173.2,190.0,207.2,81.2,108.4,125.4,143.1,160.1,177.1,194.1,211.1]
fig,ax=plt.subplots(2,1,figsize=(14,10))
for a,(t,ttl) in zip(ax,[([],'Kuzey depoda çıkış yok — en uzun 59,8 m (sınır 45 m)'),([81.2,125.4],'İSG planı: kuzey acil çıkış X 81,2 / 125,4 (tünel) + 160,1 / 194,1 — en uzun 44,5 m')]):
    g,D=run(g0,SA,[160.1,194.1]+t,t)
    M=np.where((g==0)&mask&np.isfinite(D),D,np.nan)
    ext=[X0,X0+nx*R,Y0+ny*R,Y0]
    a.imshow(np.where(g==1,1,np.nan),extent=ext,cmap='Greys',vmin=0,vmax=1.4,interpolation='nearest')
    im=a.imshow(M,extent=ext,cmap='RdYlGn_r',vmin=0,vmax=60,interpolation='nearest')
    a.contour(np.linspace(X0,X0+nx*R,nx),np.linspace(Y0,Y0+ny*R,ny),np.nan_to_num(M,nan=0),levels=[45],colors='k',linewidths=1.2)
    for x in SA: a.plot(x,64.4,'bv',ms=7)
    for x in [160.1,194.1]+t: a.plot(x,6.5,'b^',ms=7)
    a.set_xlim(47,152); a.set_ylim(65.5,5.5); a.set_title(ttl,fontsize=11); a.set_aspect('equal')
    a.set_xlabel('X (m) — kuzey üstte'); 
fig.colorbar(im,ax=ax,label='En yakın çıkışa yürüme mesafesi (m)',shrink=0.8)
plt.savefig('/home/claude/kacis/Kazan_Kacis_Mesafesi_v8.9.png',dpi=110,bbox_inches='tight')
