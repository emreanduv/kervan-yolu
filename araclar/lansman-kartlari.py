#!/usr/bin/env python3
# Rapor kartı ve kapanış kartı: oyun karesi zemin, aynı yazı dili. kart.py oran(4x5|9x16)
import asyncio,sys,base64,os
from playwright.async_api import async_playwright
O=sys.argv[1]; W,H={'4x5':(540,675),'9x16':(540,960)}[O]
F='/home/claude/kervan-yolu/www/fonts/'
b64=lambda p:base64.b64encode(open(p,'rb').read()).decode()
def font(w): return f"@font-face{{font-family:'BC';font-weight:{w};src:url(data:font/woff2;base64,{b64(F+f'barlow-condensed-latin-{w}-normal.woff2')}) format('woff2');unicode-range:U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD}}@font-face{{font-family:'BC';font-weight:{w};src:url(data:font/woff2;base64,{b64(F+f'barlow-condensed-latin-ext-{w}-normal.woff2')}) format('woff2');unicode-range:U+0100-02BA,U+02BD-02C5,U+02C7-02CC,U+02CE-02D7,U+02DD-02FF,U+0304,U+0308,U+0329,U+1D00-1DBF,U+1E00-1E9F,U+1EF2-1EFF,U+2020,U+20A0-20AB,U+20AD-20C0,U+2113,U+2C60-2C7F,U+A720-A7FF}}"
CSS=font(500)+font(700)+font(800)+"*{margin:0;box-sizing:border-box}body{width:%dpx;height:%dpx;overflow:hidden;font-family:'BC',sans-serif;color:#fff;position:relative;background:#111}"%(W,H)
def bg(p,blur): return f'<img src="data:image/png;base64,{b64(p)}" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;filter:blur({blur}px) brightness(.55);transform:scale(1.06)">'
UST='<div style="position:absolute;top:5%;left:0;right:0;text-align:center;letter-spacing:6px;font-size:15px;font-weight:700;color:#ffcf4a">KERVAN YOLU</div>'
ALT=lambda sol:f'<div style="position:absolute;bottom:4.5%;left:7%;right:7%;display:flex;justify-content:space-between;align-items:flex-end"><div style="font-size:24px;font-weight:800;color:#ffcf4a;line-height:1">{sol}</div><div style="text-align:right;font-size:13px;opacity:.85;line-height:1.3">1923 sefer<br>Bir Mr. Anduv! yapımıdır.</div></div>'
tall=O=='9x16'
rapor=f'''{bg(f'son-{O}/zemin-rapor.png',3)}{UST}
<div style="position:absolute;top:{'17%' if tall else '13%'};left:7%;right:7%">
 <div style="font-size:36px;font-weight:800;line-height:1.02">Her seferin hesabı çıkar.</div>
 <div style="margin-top:8px;font-size:15px;letter-spacing:2px;opacity:.88">NAVLUN, BELGE, CEZA, HASAR, SİGORTA, PRİM</div>
</div>
<img src="data:image/png;base64,{b64('rapor-tablo.png')}" style="position:absolute;left:{'7%' if tall else '12%'};width:{'86%' if tall else '76%'};top:{'33%' if tall else '27%'};border-radius:10px;box-shadow:0 18px 50px rgba(0,0,0,.6);border:1px solid rgba(255,255,255,.15)">
{ALT('App Store’da')}'''
son=f'''{bg(f'son-{O}/zemin-son.png',2)}{UST}
<div style="position:absolute;top:{'24%' if tall else '17%'};left:0;right:0;text-align:center">
 <img src="data:image/png;base64,{b64('ikon-kaynak.png')}" style="width:150px;height:150px;border-radius:34px;box-shadow:0 16px 44px rgba(0,0,0,.6)">
 <div style="margin-top:18px;font-size:50px;font-weight:800;line-height:1">Kervan Yolu</div>
 <div style="margin-top:8px;font-size:22px;font-weight:500;opacity:.9">Rüzgâr türbini lojistiği</div>
 <div style="margin:26px auto 0;display:inline-block;padding:12px 30px;border-radius:999px;background:#ffcf4a;color:#1d1a10;font-size:26px;font-weight:800">App Store’da</div>
 <div style="margin-top:22px;font-size:30px;font-weight:800;color:#ffcf4a">İlk 3 sefer ücretsiz.</div>
 <div style="margin-top:6px;font-size:18px;opacity:.9">Tam Sürüm tek seferlik ödemeyle 1923 seferin tamamını açar.</div>
 <div style="margin-top:18px;font-size:15px;letter-spacing:2px;opacity:.85">REKLAM YOK · İNTERNET GEREKMEZ · TÜRKÇE · ENGLISH</div>
</div>
{ALT('')}'''
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch();pg=await b.new_page(viewport={'width':W,'height':H},device_scale_factor=2)
        for ad,h in [('09-rapor',rapor),('10-son',son)]:
            await pg.set_content(f'<html><head><meta charset="utf-8"><style>{CSS}</style></head><body>{h}</body></html>')
            await pg.evaluate("document.fonts.load('800 20px BC','ıİşŞğĞçÇöÖüÜ')");await pg.wait_for_timeout(400)
            await pg.screenshot(path=f'son-{O}/{ad}.png');print(ad)
        await b.close()
asyncio.run(main())
