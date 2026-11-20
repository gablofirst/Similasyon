import json, heapq, numpy as np, sys
L=json.load(open(sys.argv[1]))
R=0.2; X0,X1,Y0,Y1=37.0,219.0,6.4,64.5
nx=int((X1-X0)/R)+1; ny=int((Y1-Y0)/R)+1
def ix(x): return int(round((x-X0)/R))
def iy(y): return int(round((y-Y0)/R))
def block(g,x0,y0,x1,y1,v=1):
    g[iy(min(y0,y1)):iy(max(y0,y1))+1, ix(min(x0,x1)):ix(max(x0,x1))+1]=v
def base():
    g=np.ones((ny,nx),np.uint8)               # 1 = engel
    block(g,48.3,6.6,218.7,64.3,0)            # bina içi
    block(g,37.3,6.4,47.8,39.9,0)             # rampa annex
    block(g,47.8,6.4,48.3,64.4,1); block(g,47.8,16,48.3,30,0)   # X48 duvarı, Y16–30 açık
    block(g,99.0,6.8,99.2,25.4); block(g,99.0,45.2,99.2,63.8)   # X99,1 iç duvar
    for r in L['DI']: block(g,*r[1:5])
    for s in L['ADEYA_SEG']: block(g,s[1],s[2],s[3],s[4])
    for r in L['ROWS']+L['EXT']: block(g,*r)
    for r in L['HPR']: block(g,*r[1:5])
    for h in L['HUCRE']: block(g,h['x0'],h['y0'],h['x1'],h['y1'])
    for z in L['Z']:
        if z['k']=='office': block(g,z['x0'],z['y0'],z['x1'],z['y1'])
    return g
SOUTH=[60.8,81.2,86.4,104.3,121.3,139.0,156.0,173.0,190.0,207.0]
NORTH_OPEN=[156.6,190.6]   # rezerv alanda, drive-in önünde değil
def run(g,exits_s,exits_n,tunnels):
    g=g.copy()
    for x in tunnels: block(g,x-0.7,6.6,x+0.7,12.5,0)
    src=[]
    for x in exits_s:
        for d in np.arange(-0.6,0.61,R): src.append((iy(64.3),ix(x+d)))
    for x in exits_n:
        for d in np.arange(-0.6,0.61,R): src.append((iy(6.6),ix(x+d)))
    D=np.full(g.shape,np.inf); h=[]
    for s in src:
        if g[s]==0: D[s]=0; heapq.heappush(h,(0,s))
    st=[(1,0,1),(-1,0,1),(0,1,1),(0,-1,1),(1,1,2**.5),(1,-1,2**.5),(-1,1,2**.5),(-1,-1,2**.5)]
    while h:
        d,(a,b)=heapq.heappop(h)
        if d>D[a,b]: continue
        for da,db,c in st:
            p,q=a+da,b+db
            if 0<=p<ny and 0<=q<nx and g[p,q]==0:
                nd=d+c*R
                if nd<D[p,q]: D[p,q]=nd; heapq.heappush(h,(nd,(p,q)))
    return g,D
g0=base()
# yalnız depo kullanılan alan (X ≤ 151.5) raporlanır
mask=np.zeros_like(g0,bool); mask[:, :ix(151.6)]=True; mask[:, :ix(48.3)]=False
sc={'A_yalniz_guney':(SOUTH,NORTH_OPEN,[]),
    'B_3_tunel_60.8_86.4_121.9':(SOUTH,NORTH_OPEN+[60.8,86.4,121.9],[60.8,86.4,121.9]),
    'C_5_kapi_tunel':(SOUTH,NORTH_OPEN+[60.8,86.4,121.9],[60.8,86.4,121.9]),}
out={}
for k,(s,n,t) in sc.items():
    g,D=run(g0,s,n,t)
    M=np.where((g==0)&mask&np.isfinite(D),D,np.nan)
    i=np.nanargmax(M); a,b=np.unravel_index(i,M.shape)
    over=np.nansum(M>45)*R*R
    out[k]=dict(max=round(float(np.nanmax(M)),1),yer=(round(X0+b*R,1),round(Y0+a*R,1)),alan_45ustu_m2=round(float(over)),
                p_over=round(float(np.nanmean(M>45))*100,1))
    np.save(f'/home/claude/kacis/D_{k}.npy',np.nan_to_num(M,nan=-1))
    print(k,out[k])
np.save('/home/claude/kacis/g0.npy',g0)
