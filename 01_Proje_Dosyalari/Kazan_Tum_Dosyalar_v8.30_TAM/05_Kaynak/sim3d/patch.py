import sys
src,dst=sys.argv[1],sys.argv[2]
s=open(src,encoding='utf-8').read()
def R(a,b,cnt=1):
    global s
    n=s.count(a)
    assert n==cnt, (n,a[:80])
    s=s.replace(a,b)
# ---------- CSS
R('.tag.sm{display:none}body.allTags .tag.sm{display:block}',
  '.tag.sm{display:none}body.allTags .tag.sm{display:block}\n#lab .tag{pointer-events:auto;cursor:pointer}.tag.cl{opacity:.82;font-weight:600}.tag.cl.big{font-size:11px}\n'
  'details.sec{border-top:1px solid #e3e7e8;margin-top:5px;padding-top:3px}details.sec>summary{cursor:pointer;font-weight:600;font-size:11px;text-transform:uppercase;letter-spacing:.04em;color:var(--mute);list-style:none}details.sec>summary::before{content:"▸ ";}details.sec[open]>summary::before{content:"▾ "}details.sec .g{margin-top:3px}\n'
  '#info details.st{margin:3px 0}#info details.st>summary{cursor:pointer}#stk input{width:70px;font:inherit;padding:1px 4px;border:1px solid var(--line);border-radius:4px}\n.src{font-size:11px;color:var(--mute);margin:3px 0}')
# ---------- başlık / panel
R('<title>Kazan v8.11 · E-ticaret akış simülasyonu 3D</title>','<title>Kazan v8.11 · E-ticaret akış simülasyonu 3D</title>')
R('<h1>Kazan v8.11 · e-ticaret akışı</h1>','<h1>Kazan v8.11 · e-ticaret akışı · sim v2</h1>')
R('<p>As-built 20.11.2026 koordinatları. Kampanya paletinden kargo kafesine kadar her adım canlı.</p>',
  '<p>As-built 20.11.2026 koordinatları. Talep: ikas Oca–Eki 2026; 2027 = ×1,5. Başlıklara ve sahnedeki yazılara tıklayınca açılır/kapanır.</p>')
R('<div class="g" id="cnt"></div>','<div id="cnt"></div><div id="stk"></div>')
# gün tipi varsayılan 2027 normal
R('<button data-d="n26" aria-pressed="true">2026 normal</button>','<button data-d="n26">2026 normal</button>')
R('<button data-d="n27">2027 normal</button>','<button data-d="n27" aria-pressed="true">2027 normal</button>')
R('<button data-k="0.10">%10</button>','<button data-k="0.115">%11,5</button>')
R("<p class=\"hint\">%2,7 = veri: 5 lansman SKU'su, Oca–Eki 2026 hücre satırlarının payı. %10 ve %25 senaryo.</p>",
  "<p class=\"hint\">%2,7 = yıl ortalaması (5 lansman SKU'su, Oca–Eki 2026). %11,5 = son 90 gün hızı, aktif lansmanlarla (v8.17). %25 senaryo.</p>")
R('<button id="bTagAll" aria-pressed="false">Ayrıntılı etiketler</button>',
  '<button id="bTagAll" aria-pressed="false">Ayrıntılı etiketler</button><button id="bShort" aria-pressed="false">Tüm yazıları kısalt</button><button id="bPanels">Panelleri kapat / aç</button>')
R('<div class="pn" id="info">','<div class="pn closed" id="info">')
# ---------- etiket: tıklayınca kısa/uzun
R("function tag(t,X,y,Y,cls=''){const d=document.createElement('div');d.className='tag '+cls;d.textContent=t;lab.appendChild(d);const o={d,v:W(X,y,Y),g:null};tags.push(o);return o}",
  "function tag(t,X,y,Y,cls=''){const d=document.createElement('div');d.className='tag '+cls;d.textContent=t;lab.appendChild(d);const sh=t.split(' · ')[0].split(' → ')[0];const o={d,v:W(X,y,Y),g:null,t,sh,c:false};o.set=c=>{o.c=c&&sh!==t;d.textContent=o.c?sh+' …':t;d.classList.toggle('cl',o.c)};d.onclick=e=>{e.stopPropagation();o.set(!o.c)};d.title='tıkla: aç / kapat';tags.push(o);return o}")
# ---------- model: hücre siparişi / HP ayrımı
R("const PM={ort:5291,spo:1.762,rate:120,pk:71,hp:140,sa:7.5};",
  "const PM={ort:5291,spo:1.762,rate:120,pk:71,hp:140,sa:7.5,hpP:1055/5291,spoC:9322/4235};\n// v2: tekli HP siparişleri (≈1.055/gün, %19,9) hücreye girmez; hücre siparişi 4.235/gün, 2,20 hücre satırı/sipariş (9.322 satır korunur)\nconst HPCAR=[.525,.443,.032];")
R("const T_={v:.85,vw:1.15,tl:26.5,tsetup:30,tdrop:15,tpack:3600/PM.pk,n:18,belt:.5,wave:45*60};",
  "const T_={v:.85,vw:1.15,tl:26.5,tsetup:30,tdrop:15,tpack:3600/(PM.pk*(1-PM.hpP)),n:18,belt:.5,wave:45*60};")
R("let day='n26',","let day='n27',")
R("function newOrder(){const n=1+poisson(PM.spo-1);","function newOrder(){const n=1+poisson(PM.spoC-1);")
R("init(){clearDyn();KD=kadro();simT=8*3600;arrAcc=0;lamb=KD.o/(PM.sa*3600);",
  "init(){clearDyn();KD=kadro();simT=8*3600;arrAcc=0;lamb=KD.o*(1-PM.hpP)/(PM.sa*3600);hpT=0;hpk.length=0;")
R("cong:[0,0],cnt:[0,0,0],","cong:[0,0],cnt:[0,0,0],hpc:[0,0,0],")
# HP koli: veri hızında, HepsiJet HP kolisi HepsiJet kafesine
R("function stepHP(dt){hpT-=dt;if(hpT<=0){hpT=40/Math.max(.5,KD.o/4444);const m=new THREE.Mesh(PB,M(0xd9b98a));S.add(m);reg(m);const car=carrier();\n  hpk.push({m,s:0,path:poly([[163.03,51.2],[163.03,60.4],[165.63,62.4],[165.63,63.9],[156,63.9],[156,65.35],car===0?[150,66.0]:car===1?[152+Math.random()*8,66.0]:[165,66.0]])})}\n for(let i=hpk.length-1;i>=0;i--){const q=hpk[i];q.s+=.35*dt;const[x,y]=at(q.path,q.s);q.m.position.copy(W(x,.95,y));if(q.s>=q.path.T){S.remove(q.m);hpk.splice(i,1)}}}",
  "function hpCar(){const r=Math.random();return r<HPCAR[0]?0:r<HPCAR[0]+HPCAR[1]?1:2}\n"
  "function stepHP(dt){hpT-=dt;while(hpT<=0){hpT+=PM.sa*3600/(KD.o*PM.hpP);const car=hpCar();stats.hpc[car]++;if(hpk.length>60)continue;const m=new THREE.Mesh(PB,M(0xd9b98a));S.add(m);reg(m);\n"
  "  const base=[[163.03,51.2],[163.03,60.4],[165.63,62.4],[165.63,63.9],[156,63.9],[156,65.9]];\n"
  "  hpk.push({m,s:0,car,path:poly(base.concat(car===0?[[150,66.2],[141,66.2],[134+Math.random()*5,67.2]]:car===1?[[152+Math.random()*8,66.6]]:[[165,66.6]]))})}\n"
  " for(let i=hpk.length-1;i>=0;i--){const q=hpk[i];q.s+=.6*dt;const[x,y]=at(q.path,q.s);q.m.position.copy(W(x,.95,y));if(q.s>=q.path.T){S.remove(q.m);hpk.splice(i,1)}}}")
# ---------- sayaç paneli: açılır kapanır bölümler + stok paneli
old_start="function renderCnt(){"
i=s.index(old_start); j=s.index("// ---- kontroller")
new_cnt=r'''const OPEN={hc:true,kp:true,kr:false,st:true};
document.addEventListener('toggle',e=>{const d=e.target;if(d.dataset&&d.dataset.sec)OPEN[d.dataset.sec]=d.open},true);
const sec=(id,t,body)=>`<details class="sec" data-sec="${id}" ${OPEN[id]?'open':''}><summary>${t}</summary><div class="g">${body}</div></details>`;
function renderCnt(){const s=stats,h=simT/3600;const lph=c=>s.busy[c]>600?fmt(s.linesC[c]/(s.busy[c]/3600),0):'–';const tm=c=>s.trips[c]?fmt(s.tripS[c]/s.trips[c]/60,1):'–';
 const qk=RULE==='wave'?` · dalga ${QK.length}`:'';const orderCamp=1-(1-PCAMP)*Math.exp(-(PM.spoC-1)*PCAMP);
 const el=(simT-8*3600)/3600,need=KD.o*(1-PM.hpP)/PM.sa;const thr=el>.25?s.orders/el:0;const cg=c=>{const b=s.busy[c];return b>600?fmt(100*s.cong[c]/b,0):'–'};
 const hpT_=s.hpc.reduce((a,b)=>a+b,0);
 document.getElementById('cnt').innerHTML=`<div class="g"><span>Simülasyon saati</span><b></b><b>${String(Math.floor(h)%24).padStart(2,'0')}:${String(Math.floor(simT/60)%60).padStart(2,'0')}</b>
 <span>Paketlenen sipariş · toplanan satır</span><b></b><b>${fmt(s.orders)} · ${fmt(s.lines)}</b>
 <span>Paketleme çıktısı / gereken (sip./saat)</span><b></b><b class="${thr&&thr<need*.95?'w':'ok'}">${thr?fmt(thr,0):'–'} / ${fmt(need,0)}</b></div>`
 +sec('hc','Hücreler',`<span></span><b>H1</b><b>H2</b>
 <span>Toplayıcı</span><b>${KD.n[0]}</b><b>${KD.n[1]}</b>
 <span>Satır / adam-saat (model 120)</span><b>${lph(0)}</b><b>${lph(1)}</b>
 <span>Ortalama sefer (dk)</span><b>${tm(0)}</b><b>${tm(1)}</b>
 <span>Döngüde sıkışma (dk · çalışma süresinin %)</span><b>${fmt(s.cong[0]/60,0)} · %${cg(0)}</b><b>${fmt(s.cong[1]/60,0)} · %${cg(1)}</b>
 <span>Bekleyen sipariş (başlangıç 45 dk birikim)</span><b class="${Q[0].length>Q[1].length*1.5+40?'w':''}">${fmt(Q[0].length)}${qk}</b><b>${fmt(Q[1].length)}</b>
 <span>İstasyon bekleyen araba</span><b class="${s.qst[0]?'w':''}">${s.qst[0]}</b><b class="${s.qst[1]?'w':''}">${s.qst[1]}</b>`)
 +sec('kp','Kampanya akışı',`<span>Sipariş payı (≥1 kampanya satırı)</span><b></b><b>%${fmt(orderCamp*100,1)}</b>
 <span>Kampanya satırı toplanan</span><b></b><b>${fmt(s.campL)}</b>
 <span>C şeridine sapan sefer</span><b></b><b>${RULE==='goz'?'– (göz)':fmt(s.campTrips)+' / '+fmt(s.trips[0]+pickers.filter(p=>p.cell===0&&p.st!=='waitOrd').length)}</b>
 <span>Sapma başına ek yol · ek süre</span><b></b><b>${s.campTrips?fmt(s.extraM/s.campTrips,0)+' m · '+fmt(s.extraS/s.campTrips,0)+' sn':'–'}</b>
 <span>Sapmanın toplayıcı zamanındaki payı</span><b></b><b>${s.busy[0]+s.busy[1]>600?'%'+fmt(100*s.extraS/(s.busy[0]+s.busy[1]),1):'–'}</b>
 ${RULE==='wave'?`<span>Kampanya siparişi ort. bekleme</span><b></b><b>${s.campWaitN?fmt(s.campWait/s.campWaitN/60,0)+' dk':'–'}</b>`:''}`)
 +sec('kr','Kargo (kafese inen)',`<span>Paketleme · HJ · TY · YK</span><b></b><b>${s.cnt.join(' · ')}</b>
 <span>Hazır paket · HJ · TY · YK</span><b></b><b>${s.hpc.join(' · ')}</b>
 <span>HP payı (veri %19,9)</span><b></b><b>${hpT_+s.orders?'%'+fmt(100*hpT_/(hpT_+s.orders),1):'–'}</b>`)}
// ---- stok · besleme · koli (hucre_slotted.pkl v8.10, ikas Oca–Eki 2026)
const STK={cov:{dtop:8.1,dtas:3.8},besK:203,lansM3:2.89,lansM3y:.67,palM3:1.0,face:9,kamp:72,koli:4235,desi:[[1,.63],[2,.77],[3,.86],[5,.96],[7,.986],[10,.9985]],koliYer:48};
let koliPal=null;
function renderStk(){const g=DAY[day].g,f=DAY[day].f;const c=STK.cov;const kb=STK.besK*g;const lp=STK.lansM3*g/STK.palM3;
 const kg=STK.koli*f*g;let prev=0;const ds=STK.desi.map(([d,p])=>{const v=(p-prev)*kg;prev=p;return`${d===1?'1':'≤'+d} desi: ${fmt(v,0)}`}).join(' · ');
 const kd=koliPal?fmt(STK.koliYer*koliPal/kg,1)+' gün':'palet başı koli girilince';
 document.getElementById('stk').innerHTML=sec('st',`Stok · besleme · koli (${g>1?'2027':'2026'})`,`
 <span>Hücre gözü kapsama · normal talep</span><b></b><b>${fmt(c.dtop/g,1)} gün</b>
 <span>Hücre gözü kapsama · tasarım (pik) talebi</span><b></b><b>${fmt(c.dtas/g,1)} gün</b>
 <span>Besleme kuralı · kalem/gün (2 hücre)</span><b></b><b>${g>1?'2':'3'} günde bir · ${fmt(kb,0)}</b>
 <span>Lansman tüketimi (son 30 gün hızı)</span><b></b><b>${fmt(lp,1)} palet/gün</b>
 <span>Lansman yüzü (sıra 3 alt kat, ${STK.face} palet)</span><b></b><b>≈${fmt(STK.face/lp,1)} gün</b>
 <span>Kampanya alanı ${STK.kamp} palet · son 30 gün / yıl ort. hızı</span><b></b><b>≈${fmt(STK.kamp/lp,0)} / ${fmt(STK.kamp/(STK.lansM3y*g),0)} gün</b>
 <span>Paketleme kolisi/gün (${DAY[day].ad})</span><b></b><b>${fmt(kg,0)}</b>
 <span>Koli alanı ${STK.koliYer} palet yeri · palet başı koli <input id="kpI" type="number" min="1" placeholder="veri yok" value="${koliPal||''}"></span><b></b><b>${kd}</b>`)
 +`<p class="src">Kapsama = hücre başı stok ÷ (talep/2), satır ağırlıklı; tasarım talebi = talep × min(P95/ort, 3) × 1,2 (hucre_slot.py). Palet = 1,0 m³ net ürün (varsayım). Koli desi dağılımı: ${ds}. Koli/palet verisi yok (§7 eksik 2).</p>`;
 const ip=document.getElementById('kpI');ip.onchange=()=>{koliPal=+ip.value||null;renderStk()}}
'''
s=s[:i]+new_cnt+s[j:]
R("renderKadro();renderInfo();\n}","renderKadro();renderInfo();renderStk();\n}")
# info: adımlar açılır/kapanır
R("<ol>${steps.map(s=>`<li>${s}</li>`).join('')}</ol>",
  "<ol>${steps.map(s=>{const k=s.match(/^<span class=\"k\">(.*?)<\\/span>/);return`<li><details class=\"st\"><summary>${k?k[1]:'adım'}</summary>${k?s.slice(k[0].length):s}</details></li>`}).join('')}</ol>")
# HP adımı ekle
R("`<span class=\"k\">Boş araba:</span> paketçi boşalan arabayı güney havuza iter; toplayıcı bir sonraki seferi oradan başlatır.`];",
  "`<span class=\"k\">Boş araba:</span> paketçi boşalan arabayı güney havuza iter; toplayıcı bir sonraki seferi oradan başlatır.`,\n"
  " `<span class=\"k\">Hazır paket → kargo:</span> tekli siparişler (≈%19,9, günde ${fmt(KD.o*PM.hpP,0)}) hücreye girmez; HP rafından güney kapı 156,0'dan saçağa çıkar. Trendyol + Yurtiçi kolisi doğu masası/kafes yanında biter. <b>HepsiJet HP kolisi (≈%52,5, günde ${fmt(KD.o*PM.hpP*HPCAR[0],0)}) K4-doğu bandının akış yönünün tersine, saçakta ≈17–22 m batıya, HepsiJet kafesine taşınır</b> (band yok; el arabası/kafes araba varsayımı).`];")
# kontroller: kısalt / paneller
R("tog('bKad',v=>document.getElementById('kad').style.display=v?'':'none');",
  "tog('bKad',v=>document.getElementById('kad').style.display=v?'':'none');tog('bShort',v=>tags.forEach(o=>o.set(v)));\n"
  "document.getElementById('bPanels').onclick=()=>{const ps=['top','info','kad'].map(i=>document.getElementById(i));const anyOpen=ps.some(p=>!p.classList.contains('closed'));ps.forEach(p=>p.classList.toggle('closed',anyOpen))};")
R("window.__run=sec=>{for(let t=0;t<sec;t+=2)tick(2);renderCnt();return JSON.stringify({simT,stats,Q:[Q[0].length,Q[1].length],QK:QK.length,st:pickers.map(p=>p.st).join(',')})};",
  "window.__run=sec=>{for(let t=0;t<sec;t+=2){tick(2)}renderCnt();return JSON.stringify({simT,stats,Q:[Q[0].length,Q[1].length],QK:QK.length,st:pickers.map(p=>p.st).join(',')})};")
open(dst,'w',encoding='utf-8').write(s)
print('ok',len(s))
