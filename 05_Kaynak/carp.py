# raf / alan × as-built duvar ve kolon çakışma kontrolü
import json,pickle
L=json.load(open('/home/claude/work/out/layout.json'))
P=pickle.load(open('/home/claude/work/out/asb_plan.pkl','rb'))
W=[]
for ly in ('DUVAR','PARAPET DUVAR','İÇ CEPHE SANDWICH PANEL','KOLON'):
    for s in P.get(ly,[]):
        xs=[p[0] for p in s];ys=[p[1] for p in s]
        if 40<min(xs)<225 and 0<min(ys)<70: W.append((ly,min(xs),min(ys),max(xs),max(ys)))
R=[('ADEYA',n,a,b,c,d) for n,a,b,c,d,_ in L['ADEYA_SEG']]+[('EXT',i+8,*r) for i,r in enumerate(L['EXT'])]+[('ROW13',13,*r) for r in L['ROWS']]
R+=[('DI',t,x0,y0,x1,y1) for t,x0,y0,x1,y1 in L['DI']]+[('HPR',n,x0,y0,x1,y1) for n,x0,y0,x1,y1,k in L['HPR']]
R+=[('VAS',i+1,*v) for i,v in enumerate(L['VAS'])]
for z in L['Z']:
    if z['k'] not in('canopy','cargo','dock','reserve','cell'): R.append(('ALAN',z['id'],z['x0'],z['y0'],z['x1'],z['y1']))
H=[]
for k,n,a,b,c,d in R:
    for ly,x0,y0,x1,y1 in W:
        if ly=='KOLON' and k=='ALAN': continue
        if ly=='KOLON' and k=='VAS' and n<=4: continue   # tasarım gereği: X 65,1 kolonu hat içinde, masalar bölünür
        if min(c,x1)-max(a,x0)>0.02 and min(d,y1)-max(b,y0)>0.02: H.append((k,str(n),ly,round(float(max(a,x0)),2),round(float(max(b,y0)),2)))
for h in sorted(set(H)): print(h)
print('toplam çakışma',len(set(H)))
