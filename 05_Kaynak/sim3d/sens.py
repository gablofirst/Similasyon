import json
from playwright.sync_api import sync_playwright
cases=[(26.5,30,'temel (120 kadrosu, 7+7)'),(22,30,'satır süresi 22 sn'),(19,30,'satır süresi 19 sn'),(22,10,'22 sn + sefer hazırlık 10 sn'),(19,10,'19 sn + hazırlık 10 sn')]
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-gl=swiftshader','--enable-unsafe-swiftshader','--no-sandbox'])
    pg=b.new_page(); pg.goto('file:///home/claude/v3d/index.html'); pg.wait_for_timeout(2500)
    for tl,su,ad in cases:
        r=[]
        for rep in range(2):
            pg.evaluate(f"PM.rate=120;T_.tl={tl};T_.tsetup={su};window.__set('n27',0.027,'wave')")
            o=json.loads(pg.evaluate("window.__run(7200)"));s=o['stats']
            r.append(([s['linesC'][c]/(s['busy'][c]/3600) for c in (0,1)],[100*s['cong'][c]/s['busy'][c] for c in (0,1)],s['lines']))
        lph=sum(sum(x[0]) for x in r)/4; cg=sum(sum(x[1]) for x in r)/4; ln=sum(x[2] for x in r)/2
        print(f"{ad:32s} satır/adam-saat {lph:5.0f}  sıkışma %{cg:4.1f}  2 saatte satır {ln:5.0f} (gereken 3132)")
    b.close()
