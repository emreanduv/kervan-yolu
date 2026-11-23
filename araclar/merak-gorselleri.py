#!/usr/bin/env python3
# Kervan Yolu ön lansman (merak) görselleri: 4:5 (LinkedIn/Instagram akış) ve 9:16 (hikâye). Çıktı: pazarlama/
import asyncio, os
from playwright.async_api import async_playwright
KOK=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLACE=open(os.path.join(KOK,'araclar','merak-place.js')).read()
TARIH='28.11'
# (ad, bölge, yük, konum oranı, saat, kamera dönüşü, ek kurulum, büyük yazı, küçük yazı)
SAH=[
 ('1-yukleniyor','marmara','kanat',0.03,'gece',2.6,"",'Bir şey yükleniyor.','Bandırma Limanı · gece'),
 ('2-dar-sokak','ege','kanat',None,'aksam',0.95,"G.bl=G.blT=1;CARGO.kanat.rotation.x=-BL_ANG;placeVehicles(0);",'70 metrelik kanat. Dar bir köy sokağı.','Ege · Bergama yolu'),
 ('3-zincir','sivas','kanat',0.55,'sabah',1.4,"G.chain=1;truck.chains.forEach(c=>c.visible=true);",'Yokuş buz. Zinciri tak.','Sivas Yaylası'),
 ('4-yarin','trakya','kanat',0.2,'aksam',0.7,"G.wind=12;",'Yarın yoldayız.','Trakya · Ganos Dağı'),
]
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path=os.environ.get('CHROME','/usr/bin/google-chrome'),args=['--use-gl=swiftshader','--enable-webgl','--ignore-gpu-blocklist'])
        for oran,(w,h) in {'4x5':(540,675),'9x16':(540,960)}.items():
            pg=await b.new_page(viewport={'width':w,'height':h},device_scale_factor=2)
            await pg.goto('file://'+KOK+'/www/index.html');await pg.wait_for_timeout(600)
            await pg.click('#lang .btn[data-lang=tr]');await pg.wait_for_timeout(200)
            await pg.evaluate("()=>{startGame('free')}");await pg.wait_for_timeout(5000)
            for ad,reg,tip,frac,tod,yaw,ek,buyuk,kucuk in SAH:
                n=await pg.evaluate("([r,t])=>{for(let n=5;n<900;n++){const j=sefer(n);if(j.reg===r&&j.type===t)return n}}",[reg,tip])
                await pg.evaluate(f"()=>buildRegion('{reg}')")
                if frac is None: frac=await pg.evaluate("()=>(VZ.v0+14)/(NS-1)")
                await pg.evaluate(PLACE,[n,frac,False,0])
                await pg.evaluate(f"()=>{{setTOD('{tod}');{ek}camYaw={yaw};snapCam();showHud(false);for(const id of['hPause','hSnd','hFM','bcam','limB','fmTk'])document.getElementById(id)&&(document.getElementById(id).style.display='none')}}")
                for _ in range(50): await pg.evaluate("()=>new Promise(r=>requestAnimationFrame(()=>r()))")
                await pg.evaluate("""([b,k,t])=>{document.querySelectorAll('#coach,#toast,#act,.pad,#pedals,#steer,#hud .tb').forEach(e=>e.style.display='none');
                 let e=document.getElementById('merak');if(!e){e=document.createElement('div');e.id='merak';document.body.appendChild(e)}
                 e.style.cssText='position:fixed;inset:0;z-index:999;pointer-events:none;font-family:"Barlow Condensed",sans-serif;color:#fff;background:linear-gradient(180deg,rgba(0,0,0,.55) 0%,rgba(0,0,0,0) 26%,rgba(0,0,0,0) 58%,rgba(0,0,0,.78) 100%)';
                 e.innerHTML=`<div style="position:absolute;top:5%;left:0;right:0;text-align:center;letter-spacing:6px;font-size:15px;font-weight:700;color:#ffcf4a">KERVAN YOLU</div>
                 <div style="position:absolute;bottom:17%;left:7%;right:7%;font-size:38px;font-weight:800;line-height:1.02;text-shadow:0 2px 14px rgba(0,0,0,.7)">${b}</div>
                 <div style="position:absolute;bottom:12.5%;left:7%;font-size:15px;letter-spacing:2px;opacity:.85">${k.toUpperCase()}</div>
                 <div style="position:absolute;bottom:4.5%;left:7%;right:7%;display:flex;justify-content:space-between;align-items:flex-end">
                  <div style="font-size:44px;font-weight:800;color:#ffcf4a;line-height:1">${t}</div>
                  <div style="text-align:right;font-size:13px;opacity:.85;line-height:1.3">1923 sefer<br>Bir Mr. Anduv! yapımıdır.</div></div>`}""",[buyuk,kucuk,TARIH])
                await pg.wait_for_timeout(300)
                out=os.path.join(KOK,'pazarlama',f'{ad}-{oran}.png');await pg.screenshot(path=out);print(out)
                await pg.evaluate("()=>document.getElementById('merak').remove()")
            await pg.close()
        await b.close()
asyncio.run(main())
