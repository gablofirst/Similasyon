import numpy as np, sys, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
LJ=sys.argv[1]; XM=float(sys.argv[2]); OUT=sys.argv[3] if len(sys.argv)>3 else None
sys.argv=['x',LJ]
exec(open('/home/claude/zipx/Kazan_Tum_Dosyalar_v8.10_TAM/05_Kaynak/kacis/kacis.py').read().split('g0=base()')[0])
g0=base()
for r in L.get('KAMP_PAL',[]): block(g0,*r)
mask=np.zeros_like(g0,bool); mask[iy(7.3):, ix(48.4):ix(XM)]=True
SA=[60.8,86.4,104.5,121.3,139.1,156.0,173.2,190.0,207.2,81.2,108.4,125.4,143.1,160.1,177.1,194.1,211.1]
g,D=run(g0,SA,[160.1,194.1,81.2,125.4],[81.2,125.4])
M=np.where((g==0)&mask&np.isfinite(D),D,np.nan)
a,b=np.unravel_index(np.nanargmax(M),M.shape)
print('en uzun',round(float(np.nanmax(M)),1),'m · yer',(round(X0+b*R,1),round(Y0+a*R,1)),'· 45 m üstü',round(float(np.nansum(M>45)*R*R)),'m²')
# e-ticaret bandı (Y 48,6–64) en uzun
Mb=M.copy(); Mb[:iy(48.6),:]=np.nan
a2,b2=np.unravel_index(np.nanargmax(Mb),Mb.shape); print('e-ticaret/güney bant en uzun',round(float(np.nanmax(Mb)),1),(round(X0+b2*R,1),round(Y0+a2*R,1)))
if OUT:
    fig,ax=plt.subplots(figsize=(15,6)); ext=[X0,X0+nx*R,Y0+ny*R,Y0]
    ax.imshow(np.where(g==1,1,np.nan),extent=ext,cmap='Greys',vmin=0,vmax=1.4,interpolation='nearest')
    im=ax.imshow(M,extent=ext,cmap='RdYlGn_r',vmin=0,vmax=60,interpolation='nearest')
    ax.contour(np.linspace(X0,X0+nx*R,nx),np.linspace(Y0,Y0+ny*R,ny),np.nan_to_num(M,nan=0),levels=[45],colors='k',linewidths=1.2)
    for x in SA: ax.plot(x,64.4,'bv',ms=6)
    for x in [81.2,125.4,160.1,194.1]: ax.plot(x,6.5,'b^',ms=6)
    ax.set_xlim(47,XM+1); ax.set_ylim(65.5,5.5); ax.set_aspect('equal')
    ax.set_title(f'v8.11 kaçış mesafesi · en uzun {np.nanmax(M):.1f} m (sınır 45 m) · e-ticaret bandı 17 m doğuda',fontsize=11)
    fig.colorbar(im,ax=ax,label='En yakın çıkışa yürüme (m)',shrink=0.8); plt.savefig(OUT,dpi=110,bbox_inches='tight')
