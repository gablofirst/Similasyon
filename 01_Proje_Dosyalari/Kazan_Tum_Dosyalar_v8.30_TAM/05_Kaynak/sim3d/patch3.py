# sim v2.2 (v8.12 çizimi): K5 kesin (Y 64,85) · K4 + masalar 0,3 m güneye (eksen 65,65) · kafes Y 66,1'den · K1 kapıdan K4'e
# · masalar kaçış geçitlerinde bölünür (124,8–126,0 / 159,5–160,7) · K5 geçit bölümü (yangın kapısı 160,1) · tel çit X 167,6
# Kullanım: python3 patch3.py giris_v2.1.html cikis_v2.2.html
import sys, re, json
s = open(sys.argv[1]).read()
i = s.find('const D={"H"'); j = s.find('\n', i); D, code = s[:j], s[j:]
def rep(t, a, b, n=None):
    c = t.count(a); assert c and (n is None or c == n), (a, c); return t.replace(a, b)
# --- veri (D)
for k, a, b in [('sorter', '[127.0,65.0,140.13,65.7', '[127.0,65.3,140.13,66.0'), ('sorter2', '[140.13,65.0,156.0,65.7', '[140.13,65.3,156.0,66.0'),
                ('ayirma', '[121.0,65.0,127.0,65.7', '[121.0,65.3,127.0,66.0'), ('ayirma2', '[156.0,65.0,162.0,65.7', '[156.0,65.3,162.0,66.0'),
                ('k_hj', '[100.2,65.8,139.8,71.0', '[100.2,66.1,139.8,71.0'), ('k_ty', '[140.1,65.8,163.5,71.0', '[140.1,66.1,163.5,71.0'),
                ('k_yk', '[163.8,65.8,167.5,71.0', '[163.8,66.1,167.5,71.0')]:
    D = rep(D, f'"{k}":{a}', f'"{k}":{b}', 1)
for a in ('[140.13,65.35]', '[127.4,65.35]', '[140.6,65.35]', '[155.6,65.35]'): D = rep(D, a, a.replace('65.35', '65.65'))
D = rep(D, '[[166.63,64.0],[156.0,64.0],[156.0,67.6]],"t":"H6 → güney kapı 156 → kafes (TY/YK yanında, HJ araba)"',
        '[[166.63,63.05],[156.0,63.05],[156.0,64.85],[141.0,64.85]],"t":"H6 → K5 → kapı 156 → K1 (tek tarayıcı + saptırıcı)"', 1)
D = rep(D, "DIŞ ALAN · ÜSTÜ KAPALI SAÇAK · Y 64,7–71,0 · v8.11: X 167,5'e uzar", "DIŞ ALAN · ÜSTÜ KAPALI SAÇAK · Y 64,7–71,0 · v8.12: K4 + kafes 0,3 m güneye", 1)
# tel çit X ≈150,8 → +17,05 (X 167,6–167,9)
mT = re.search(r'"TEL":(\[\[.*?\]\])', D); T = json.loads(mT.group(1)); n = 0
for r in T:
    if r[0] > 150.4 and r[2] < 150.95 and r[1] > 64.3: r[0] = round(r[0]+17.05, 3); r[2] = round(r[2]+17.05, 3); n += 1
D = D[:mT.start(1)] + json.dumps(T, separators=(',', ':')) + D[mT.end(1):]
print('tel çit parçası', n)
# --- kod
code = rep(code, 'box(6,.05,.8,tab,124,.88,65.35);box(6,.05,.8,tab,159,.88,65.35);',
           'box(3.8,.05,.8,tab,122.9,.88,65.65);box(1,.05,.8,tab,126.5,.88,65.65);box(3.5,.05,.8,tab,157.75,.88,65.65);box(1.3,.05,.8,tab,161.35,.88,65.65);', 1)
code = rep(code, '121.5+Math.random()*5', '121.3+Math.random()*3.3'); code = rep(code, '156.5+Math.random()*5', '156.3+Math.random()*3.0')
code = rep(code, 'box(.6,.06,1.5,belt,K1X,.8,64.6)', 'box(.6,.06,1.8,belt,K1X,.8,64.75)', 1)
for nm in ('kH', 'kT', 'kY'):
    m = re.search(nm + r'=poly\((\[\[.*?\]\])\)', code); P = json.loads(m.group(1))
    code = code[:m.start(1)] + json.dumps([[x, round(y+0.3, 2)] for x, y in P], separators=(',', ':')) + code[m.end(1):]
code = rep(code, '65.35', '65.65')
code = rep(code, 'const K5P=[[166.6,63.05],[156.0,63.05],[156.0,64.7],[140.6,64.7],[K1X,64.7]];', 'const K5P=[[166.6,63.05],[156.0,63.05],[156.0,64.85],[140.6,64.85],[K1X,64.85]];', 1)
code = rep(code, "(Y 64,7) → K1 birleşme (öneri v8.22)", "(Y 64,85) → K1 birleşme (v8.12, onaylı)", 1)
code = rep(code, "tag('K5 · HP → K1 · tek tarayıcı + saptırıcı (öneri)',149,1.6,64.7,'camp');",
           "tag('K5 · HP → K1 · tek tarayıcı + saptırıcı',149,1.6,64.85,'camp');"
           "box(1.2,.07,.47,M(0xc0392b),160.1,.83,63.05,false);tag('K5 geçit (yangın kapısı 160,1)',160.1,1.5,62.4,'warn');"
           "[[124.8,126.0,125.4],[159.5,160.7,160.1]].forEach(([a,b,x])=>{flr(a,64.4,b,71.0,0x3fae5a,.55);tag('kaçış geçidi '+String(x).replace('.',','),x,1.3,68.0,'sm')});", 1)
code = rep(code, '(K5, öneri)', '(K5)', 1)
code = rep(code, 'duvar ile K4 arasındaki 0,6 m şeritte', 'duvar ile K4 arasındaki 0,9 m şeritte (K4 0,3 m güneye alındı)', 1)
D = rep(D, '<title>Kazan v8.11 · E-ticaret akış simülasyonu 3D</title>', '<title>Kazan v8.12 · E-ticaret akış simülasyonu 3D (v2.2)</title>', 1)
D = rep(D, 'Kazan v8.11 · e-ticaret akışı · sim v2', 'Kazan v8.12 · e-ticaret akışı · sim v2.2', 1)
open(sys.argv[2], 'w').write(D + code); print('ok')
