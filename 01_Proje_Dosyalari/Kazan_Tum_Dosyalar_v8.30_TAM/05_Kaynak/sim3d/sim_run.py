import sys, json
from playwright.sync_api import sync_playwright
html=sys.argv[1]
cases=[('n26',0.027,'wave'),('n27',0.027,'wave'),('p27',0.027,'wave'),('n26',0.115,'wave'),('n27',0.115,'wave'),('n27',0.115,'goz'),('n27',0.115,'mix')]
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-gl=swiftshader','--enable-unsafe-swiftshader','--no-sandbox'])
    pg=b.new_page(viewport={'width':1200,'height':800})
    errs=[];pg.on('pageerror',lambda e:errs.append(str(e)));pg.goto('file://'+html); pg.wait_for_timeout(2500); print('ERR',errs)
    for d,k,r in cases:
        pg.evaluate(f"window.__set('{d}',{k},'{r}')")
        out=json.loads(pg.evaluate("window.__run(7200)"))
        kd=pg.evaluate("JSON.stringify({o:KD.o,n:KD.n,np:KD.np,npAct:KD.npAct,nh:KD.nh,araba:KD.araba})")
        s=out['stats'];kd=json.loads(kd)
        lph=[ s['linesC'][c]/(s['busy'][c]/3600) if s['busy'][c] else 0 for c in (0,1)]
        trip=[ s['tripS'][c]/s['trips'][c]/60 if s['trips'][c] else 0 for c in (0,1)]
        print(json.dumps(dict(case=f'{d} k={k} {r}',siparis_gun=round(kd['o']),topl=kd['n'],pak=kd['np'],pakAkt=kd['npAct'],araba=kd['araba'],
          paket_2sa=s['orders'],satir=s['lines'],lph=[round(x) for x in lph],sefer_dk=[round(x,1) for x in trip],sikisma_dk=[round(x/60,1) for x in s['cong']],
          kuyruk=out['Q'],dalga=out['QK'],istasyon_bekl=s['qst'],kamp_sefer=s['campTrips'],sefer=s['trips'],ek_m=round(s['extraM']/s['campTrips']) if s['campTrips'] else 0,
          ek_sn=round(s['extraS']/s['campTrips']) if s['campTrips'] else 0,kamp_bekl_dk=round(s['campWait']/s['campWaitN']/60) if s['campWaitN'] else 0,hp=s.get('hpc'),cikti_saat=round(s['orders']/2),gereken=round(kd['o']*0.8006/7.5),sik_pct=[round(100*s['cong'][c]/s['busy'][c]) for c in (0,1)],sapma_pct=round(100*s['extraS']/(s['busy'][0]+s['busy'][1]),1)),ensure_ascii=False))
    b.close()
