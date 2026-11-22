# sim v2.2 → v2.3 (21.11.2026, Sedat): açılış görünümü ekrana ortalanır.
# Sorun: sabit kamera (iso) sol tarafı boş bırakıyor, hazır paket (X 157–168,5) sağda ekran dışına taşıyordu.
# Çözüm: e-ticaret bandının kutusu (plan X 84–169,5, Y 47–75, yükseklik 0–3 m) kamera yönüne göre
# ekranın kullanılabilir alanına (üst/alt panel payı) sığdırılır; pencere boyutu değişince yeniden sığdırılır
# (kullanıcı kamerayı elle oynatmadıysa). "Genel" ve "Üstten" düğmeleri de bu sığdırmayı kullanır.
# Kullanım: python3 patch4.py sim_v2.2.html sim_v2.3.html
import sys
s = open(sys.argv[1], encoding='utf-8').read()
old_init = "C.position.set(...V.iso[0]);O.target.set(...V.iso[1]);"
assert s.count(old_init) == 1
fit = r"""
const FITB=[];for(const X of [84,169.5])for(const Y of [47,75])for(const h of [0,3])FITB.push(W(X,h,Y));
const FITDIR={iso:[-12,52,46],top:[0,1,.04]};let userMoved=false;
function fitView(k){const d=new THREE.Vector3(...FITDIR[k]).normalize();const t=new THREE.Vector3(-6,0,4);let dist=90;
 const cam=C.clone();cam.aspect=innerWidth/innerHeight;cam.updateProjectionMatrix();const th=Math.tan(cam.fov*Math.PI/360);
 const vb=window.FIT_BOX||{x0:-.95,x1:.95,y0:-.80,y1:.84};const cx=(vb.x0+vb.x1)/2,cy=(vb.y0+vb.y1)/2,wx=vb.x1-vb.x0,wy=vb.y1-vb.y0;
 for(let i=0;i<60;i++){cam.position.copy(t).addScaledVector(d,dist);cam.lookAt(t);cam.updateMatrixWorld();
  let x0=1e9,x1=-1e9,y0=1e9,y1=-1e9;FITB.forEach(p=>{const v=p.clone().project(cam);x0=Math.min(x0,v.x);x1=Math.max(x1,v.x);y0=Math.min(y0,v.y);y1=Math.max(y1,v.y)});
  const mx=(x0+x1)/2-cx,my=(y0+y1)/2-cy,sc=Math.max((x1-x0)/wx,(y1-y0)/wy);
  const rt=new THREE.Vector3().setFromMatrixColumn(cam.matrixWorld,0),up=new THREE.Vector3().setFromMatrixColumn(cam.matrixWorld,1);
  t.addScaledVector(rt,mx*dist*th*cam.aspect*.9).addScaledVector(up,my*dist*th*.9);
  const k2=-t.y/d.y;t.addScaledVector(d,k2);dist-=k2;dist*=1+(sc-1)*.6}
 cam.position.copy(t).addScaledVector(d,dist);V[k]=[cam.position.toArray(),t.toArray()];return V[k]}
fitView('iso');fitView('top');
C.position.set(...V.iso[0]);O.target.set(...V.iso[1]);
O.addEventListener('start',()=>{userMoved=true});
addEventListener('resize',()=>{fitView('iso');fitView('top');if(!userMoved&&!fly&&!follow){C.position.set(...V.iso[0]);O.target.set(...V.iso[1])}});
window.__fit=()=>JSON.stringify(V.iso);
"""
s = s.replace(old_init, fit)
# "Genel"/"Üstten" düğmeleri: güncel pencereye göre yeniden sığdır
old_view = "function view(k){const[p,t]=V[k];"
assert s.count(old_view) == 1
s = s.replace(old_view, "function view(k){if(k==='iso'||k==='top'){fitView(k)}if(k==='iso')userMoved=false;const[p,t]=V[k];")
s = s.replace('sim v2.2', 'sim v2.3')
open(sys.argv[2], 'w', encoding='utf-8').write(s)
print('ok', len(s))
