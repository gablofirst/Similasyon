import sys
p='/home/claude/v3d/index.html'
s=open(p,encoding='utf-8').read()
def R(a,b,cnt=1):
    global s
    n=s.count(a); assert n==cnt,(n,a[:90]); s=s.replace(a,b)
# 1) Ayarlar paneli kapanır + gruplar
R('#ctl .bd{display:flex;flex-direction:column;gap:4px}',
  '#ctl .bd{display:flex;flex-direction:column;gap:4px}#ctl.closed .bd{display:none}#ctl.closed{max-height:none}\n'
  'details.cg>summary{cursor:pointer;font-weight:600;font-size:11px;letter-spacing:.05em;text-transform:uppercase;color:var(--mute);margin:8px 0 3px;list-style:none}details.cg>summary::before{content:"▸ "}details.cg[open]>summary::before{content:"▾ "}.cgb{display:flex;flex-direction:column;gap:4px}')
R("document.querySelectorAll('.pn .hd').forEach(h=>h.onclick=()=>h.closest('.pn').classList.toggle('closed'));",
  "document.querySelectorAll('.pn .hd').forEach(h=>h.onclick=()=>h.closest('.pn').classList.toggle('closed'));\n"
  "{const bd=document.querySelector('#ctl .bd');let cur=null;Array.from(bd.children).forEach(el=>{if(el.classList.contains('t')){const d=document.createElement('details');d.className='cg';d.open=!['Görünüm','Hız','Gösterim'].includes(el.textContent);const sm=document.createElement('summary');sm.textContent=el.textContent;const b=document.createElement('div');b.className='cgb';d.append(sm,b);bd.insertBefore(d,el);el.remove();cur=b}else if(cur)cur.appendChild(el)})}")
R("const ps=['top','info','kad'].map(","const ps=['top','info','kad','ctl'].map(")
# 2) hız 95
R("rate:120,","rate:95,")
R("(120 satır, 71 ve 140 sipariş/adam-saat, 7,5 saat)","(${PM.rate} satır, 71 ve 140 sipariş/adam-saat, 7,5 saat)")
R("Satır / adam-saat (model 120)","Satır / adam-saat (model ${PM.rate})")
R("(120 satır/adam-saat, 71 sipariş/paketçi-saat)","(${PM.rate} satır/adam-saat, 71 sipariş/paketçi-saat; hız 95 = sim v2 ölçümü, 21.11 kararı)")
# 3) K5: HP → K1 bandı
R("// ---- hazır paket\n",
  "// ---- K5: HP fatura → kapı 156 → duvar dibi şerit (Y 64,7) → K1 birleşme (öneri v8.22)\n"
  "const K5P=[[166.6,63.05],[156.0,63.05],[156.0,64.7],[140.6,64.7],[K1X,64.7]];\n"
  "{const k5m=M(0x2f6fb5,{roughness:.6});for(let i=1;i<K5P.length;i++){const[a,b]=[K5P[i-1],K5P[i]];const l=Math.hypot(b[0]-a[0],b[1]-a[1]);const m=box(l+.45,.06,.45,k5m,(a[0]+b[0])/2,.8,(a[1]+b[1])/2,false);m.rotation.y=-Math.atan2(b[1]-a[1],b[0]-a[0]);const f=box(l+.5,.06,.52,frame,(a[0]+b[0])/2,.74,(a[1]+b[1])/2,false);f.rotation.y=m.rotation.y}}\n"
  "// ---- hazır paket\n")
R("  const base=[[163.03,51.2],[163.03,60.4],[165.63,62.4],[165.63,63.9],[156,63.9],[156,65.9]];\n"
  "  hpk.push({m,s:0,car,path:poly(base.concat(car===0?[[150,66.2],[141,66.2],[134+Math.random()*5,67.2]]:car===1?[[152+Math.random()*8,66.6]]:[[165,66.6]]))})}\n"
  " for(let i=hpk.length-1;i>=0;i--){const q=hpk[i];q.s+=.6*dt;",
  "  const base=[[164.4+Math.random()*2.4,63.05]].concat(K5P.slice(1),[[K1X,65.35]]);\n"
  "  hpk.push({m,s:0,car,path:poly(base.concat(car===0?[[127,65.35],[121.5+Math.random()*5,65.35]]:[[156.5+Math.random()*5,65.35]]))})}\n"
  " for(let i=hpk.length-1;i>=0;i--){const q=hpk[i];q.s+=T_.belt*dt;")
R("q.m.position.copy(W(x,.95,y));if(q.s>=q.path.T){S.remove(q.m);hpk.splice(i,1)}}}",
  "q.m.position.copy(W(x,.93,y));if(q.s>=q.path.T){S.remove(q.m);hpk.splice(i,1)}}}")
R("tag('K1 bandı batı–doğu geçişi keser',142.6,2.6,60.8,'warn');",
  "tag('K1 bandı batı–doğu geçişi keser',142.6,2.6,60.8,'warn');tag('K5 · HP → K1 · tek tarayıcı + saptırıcı (öneri)',149,1.6,64.7,'camp');")
# info adımı
i=s.index("`<span class=\"k\">Hazır paket → kargo:</span>")
j=s.index("`];",i)
s=s[:i]+("`<span class=\"k\">Hazır paket → kargo (K5, öneri):</span> tekli siparişler (≈%19,9, günde ${fmt(KD.o*PM.hpP,0)}) hücreye girmez. HP fatura/etiket masasında koli <b>K5 bandına</b> konur; K5 HP çıkış yolundan kapı 156'dan çıkar, duvar ile K4 arasındaki 0,6 m şeritte batıya gider ve tarayıcıdan önce <b>K1'e birleşir</b>. Saptırıcı HepsiJet kolisini K4-batıya, Trendyol + Yurtiçi kolisini K4-doğuya ayırır. Elle taşıma ve K4/masa hattını elle geçme yok; tüm koliler tek tarayıcıdan geçer.`")+s[j:]
open(p,'w',encoding='utf-8').write(s); print('ok')
