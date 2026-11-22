# sim v2.3 → v2.4 (21.11.2026, Sedat): ekrana tam sığma (fit to page).
# Sorun: #c canvas'ında CSS genişlik/yükseklik yoktu; R.setSize(...,false) yalnız çizim tamponunu ayarlıyor.
# devicePixelRatio > 1 olan ekranda (yüksek DPI ya da tarayıcı yakınlaştırması) canvas 2× büyük görünüyor,
# sahnenin yalnız sol üst çeyreği ekranda kalıyor, etiketler (innerWidth'e göre) nesnelerden kopuyordu.
# Çözüm: canvas CSS 100vw × 100vh, display:block; boyut değişiminde fit yeniden hesaplanır.
# Kullanım: python3 patch5.py sim_v2.3.html sim_v2.4.html
import sys
s = open(sys.argv[1], encoding='utf-8').read()
old = "#c{position:fixed;inset:0}"
assert s.count(old) == 1
s = s.replace(old, "#c{position:fixed;left:0;top:0;width:100vw;height:100vh;display:block}html,body{overflow:hidden}")
s = s.replace('sim v2.3', 'sim v2.4')
open(sys.argv[2], 'w', encoding='utf-8').write(s)
print('ok', len(s))

# 2) Sığdırma alanı panellerin dışındaki boş dikdörtgen (açık panellere göre dinamik).
s = open(sys.argv[2], encoding='utf-8').read()
old = "window.__fit=()=>JSON.stringify(V.iso);"
assert s.count(old) == 1
new = old + r"""
function freeBox(){const w=innerWidth,h=innerHeight;let L=8,R=w-8,T=8,B=h-8;
 document.querySelectorAll('.pn').forEach(p=>{const r=p.getBoundingClientRect();if(!r.width||!r.height||getComputedStyle(p).display==='none')return;
  if(r.right<=L||r.left>=R||r.bottom<=T||r.top>=B)return;
  const c=[];if(r.left-L<R-r.right){c.push([Math.max(L,r.right+6),R,T,B])}else{c.push([L,Math.min(R,r.left-6),T,B])}
  if(r.top-T<B-r.bottom){c.push([L,R,Math.max(T,r.bottom+6),B])}else{c.push([L,R,T,Math.min(B,r.top-6)])}
  const a=q=>Math.max(0,q[1]-q[0])*Math.max(0,q[3]-q[2]);const best=a(c[0])>=a(c[1])?c[0]:c[1];[L,R,T,B]=best});
 if(R-L<w*.3||B-T<h*.3){L=8;R=w-8;T=8;B=h-8}
 window.FIT_BOX={x0:L/w*2-1,x1:R/w*2-1,y0:1-B/h*2,y1:1-T/h*2}}
function refit(){freeBox();fitView('iso');fitView('top');if(!userMoved&&!follow){fly=null;C.position.set(...V.iso[0]);O.target.set(...V.iso[1])}}
let rfT=0;const rfQ=()=>{clearTimeout(rfT);rfT=setTimeout(refit,60)};
new MutationObserver(rfQ).observe(document.body,{subtree:true,attributes:true,attributeFilter:['class','open']});
addEventListener('resize',rfQ);document.addEventListener('toggle',rfQ,true);
refit();"""
s = s.replace(old, new)
# Genel/Üstten düğmeleri de güncel panel alanını kullansın
s = s.replace("function view(k){if(k==='iso'||k==='top'){fitView(k)}", "function view(k){if(k==='iso'||k==='top'){freeBox();fitView(k)}")
s = s.replace("<title>Kazan v8.12 · E-ticaret akış simülasyonu 3D (v2.2)</title>", "<title>Kazan v8.12 · E-ticaret akış simülasyonu 3D (sim v2.4)</title>")
open(sys.argv[2], 'w', encoding='utf-8').write(s)
print('ok2', len(s))
