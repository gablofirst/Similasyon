# Kullanım: python3 pptx_measure.py sunum.html cikis.json  (Arial ile ölçer, animasyonsuz)
import sys, json, asyncio, os
from playwright.async_api import async_playwright
JS = open(os.path.join(os.path.dirname(__file__), 'pptx_extract.js')).read()
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path='/usr/bin/google-chrome')
        pg = await b.new_page(viewport={'width': 1920, 'height': 1080})
        await pg.goto('file://' + os.path.abspath(sys.argv[1])); await pg.wait_for_timeout(1500)
        await pg.add_style_tag(content="*{font-family:Arial,'Liberation Sans',sans-serif !important;animation:none !important;transition:none !important}")
        await pg.wait_for_timeout(800)
        d = await pg.evaluate(JS); open(sys.argv[2], 'w').write(json.dumps(d, ensure_ascii=False).replace(': NaN', ': null'))
        print(len(d), 'slayt', sum(len(s['items']) for s in d), 'öğe')
        await b.close()
asyncio.run(main())
