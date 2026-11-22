import sys,asyncio
from playwright.async_api import async_playwright
async def main(h,p):
    async with async_playwright() as pw:
        b=await pw.chromium.launch(executable_path='/usr/bin/google-chrome'); pg=await b.new_page(viewport={'width':1920,'height':1080})
        await pg.goto('file://'+h); await pg.wait_for_timeout(1500)
        await pg.pdf(path=p,width='1920px',height='1080px',print_background=True,margin={'top':'0','bottom':'0','left':'0','right':'0'})
        await b.close()
asyncio.run(main(*sys.argv[1:3]))
