import re,sys,pickle,collections
F=sys.argv[1]
s=open(F,encoding='utf-8').read()
tok=re.compile(r'[MmLlHhVvZzAaCcQqSsTt]|-?\d*\.?\d+(?:[eE][-+]?\d+)?')
def parse(data):
    t=tok.findall(data);i=0;cx=cy=0;sx=sy=0;cmd=None;polys=[];cur=[]
    def num():
        nonlocal i;v=float(t[i]);i+=1;return v
    while i<len(t):
        if t[i].isalpha():cmd=t[i];i+=1
        if cmd in'Zz':
            if cur:cur.append((sx,sy));polys.append(cur);cur=[]
            cx,cy=sx,sy;continue
        if i>=len(t) or t[i].isalpha() and cmd not in'Zz':
            continue
        if cmd in'Mm':
            x,y=num(),num()
            if cmd=='m':x+=cx;y+=cy
            if cur:polys.append(cur)
            cur=[(x,y)];cx,cy=x,y;sx,sy=x,y;cmd='l' if cmd=='m' else 'L'
        elif cmd in'Ll':
            x,y=num(),num()
            if cmd=='l':x+=cx;y+=cy
            cx,cy=x,y;cur.append((x,y))
        elif cmd in'Hh':
            x=num();cx=x+cx if cmd=='h' else x;cur.append((cx,cy))
        elif cmd in'Vv':
            y=num();cy=y+cy if cmd=='v' else y;cur.append((cx,cy))
        elif cmd in'Aa':
            for _ in range(5):num()
            x,y=num(),num()
            if cmd=='a':x+=cx;y+=cy
            cx,cy=x,y;cur.append((x,y))
        elif cmd in'Cc':
            for _ in range(4):num()
            x,y=num(),num()
            if cmd=='c':x+=cx;y+=cy
            cx,cy=x,y;cur.append((x,y))
        elif cmd in'QqSs':
            for _ in range(2):num()
            x,y=num(),num()
            if cmd in'qs':x+=cx;y+=cy
            cx,cy=x,y;cur.append((x,y))
        else: i+=1
    if cur:polys.append(cur)
    return polys
out=collections.defaultdict(list)
for m in re.finditer(r'<Path ([^>]*?)/?>',s):
    a=m.group(1)
    dm=re.search(r'Data="([^"]*)"',a)
    if not dm:continue
    st=re.search(r'Stroke="(#\w+)"',a);fi=re.search(r'Fill="(#\w+)"',a);w=re.search(r'StrokeThickness="([\d.]+)"',a)
    key=('S'+st.group(1)) if st else ('F'+fi.group(1) if fi else 'X')
    try:
        for p in parse(dm.group(1)):
            if len(p)>1 or key[0]=='F':out[key].append((p,float(w.group(1)) if w else 0))
    except Exception as e:pass
pickle.dump(dict(out),open('xps.pkl','wb'))
for k,v in sorted(out.items(),key=lambda kv:-len(kv[1]))[:25]:
    xs=[q[0] for p,_ in v for q in p];ys=[q[1] for p,_ in v for q in p]
    print(k,len(v),round(min(xs)),round(max(xs)),round(min(ys)),round(max(ys)))
