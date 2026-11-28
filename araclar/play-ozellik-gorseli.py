"""Google Play öne çıkan görseli (1024x500): Kervan Yolu ekran görüntüsünden (Ege, kanat seferi) kesit + başlık.
Kullanım: python3 araclar/play-ozellik-gorseli.py  →  store/play-feature-1024x500.png"""
import asyncio, os, shutil
from PIL import Image
from playwright.async_api import async_playwright
KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
Image.open(os.path.join(KOK, 'store/screenshots/tr/play/02.png')).convert('RGB').crop((427, 100, 1494, 620)).resize((1024, 500), Image.LANCZOS).save('/tmp/fg-bg.png')
s = open(os.path.join(KOK, 'araclar/play-ozellik/sablon.html')).read().replace('/tmp/h2/main/www', os.path.join(KOK, 'www'))
open('/tmp/fg.html', 'w').write(s)
async def m():
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={'width': 1024, 'height': 500})
        await pg.goto('file:///tmp/fg.html'); await pg.evaluate("document.fonts.load('800 40px BC','ıİşŞğĞçÇöÖüÜ')"); await pg.wait_for_timeout(500)
        await pg.screenshot(path=os.path.join(KOK, 'store/play-feature-1024x500.png')); await b.close()
asyncio.run(m())
