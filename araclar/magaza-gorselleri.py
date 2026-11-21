#!/usr/bin/env python3
# Kervan Yolu mağaza ekran görüntüleri (App Store iPhone 6.9", iPad 13", Google Play telefon) TR + EN.
# Kullanım: python3 araclar/magaza-gorselleri.py   (www/index.html'i açıp sahneleri kurar, kareleri store/ altına yazar)
# WebGL için Chrome gerekir: CHROME=/usr/bin/google-chrome (varsayılan) ya da playwright chromium.
import asyncio, os
from playwright.async_api import async_playwright
KOK=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SIZES={'iphone69':(956,440,3),'ipad13':(1376,1032,2),'play':(960,540,2)}
CAP={'tr':['40 metrelik kanadı rüzgâr sahasına taşı','Drone ile hasar tespiti','Depoda forkliftle yükle','Kabin içi: göstergeler, tesbih ve çay','Gece seferi: farlarla yolda','1923 sefer: navlun, sigorta, prim'],
     'en':['Haul a 40 m blade to the wind farm','Drone damage inspection','Load crates with the forklift','Cab view: gauges, prayer beads and tea','Night job: drive by your headlights','1923 jobs: freight, insurance, bonus']}
PLACE=r'''([job,frac,back,cam])=>{SAVE.tips={gas:1,fork:1,strap:1,drone:1,cam:1,off:1,kanat:1,night:1};SAVE.muted=true;resetGame('career',job);if(G.job.type!=='kasa')doStrap();
 const i=Math.round(frac*(NS-1));const j=back?i-1:i+1;truck.v.x=RS[i].x;truck.v.z=RS[i].z;truck.v.h=Math.atan2(-(RS[j].x-RS[i].x),-(RS[j].z-RS[i].z));trailer.th=truck.v.h+0.02;truck.v.speed=0;camMode=cam;camYaw=0.35;snapCam();setAct(null);coachHide();}'''
async def frames(pg,n=40):
    for _ in range(n): await pg.evaluate("()=>new Promise(r=>requestAnimationFrame(()=>r()))")
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path=os.environ.get('CHROME','/usr/bin/google-chrome'),args=['--use-gl=swiftshader','--enable-webgl','--ignore-gpu-blocklist'])
        for lang in ['tr','en']:
            for k,(w,h,d) in SIZES.items():
                out=os.path.join(KOK,'store','screenshots',lang,k);os.makedirs(out,exist_ok=True)
                pg=await b.new_page(viewport={'width':w,'height':h},device_scale_factor=d)
                await pg.goto('file://'+KOK+'/www/index.html');await pg.wait_for_timeout(600)
                await pg.click(f'#lang .btn[data-lang={lang}]');await pg.wait_for_timeout(200)
                await pg.evaluate("()=>{SAVE.tab='career';startGame('free')}");await pg.wait_for_timeout(5000)
                ns=await pg.evaluate("()=>{const o={};for(let n=4;n<400;n++){const j=sefer(n);if(!o[j.type+j.tod])o[j.type+j.tod]=n}return o}")
                for i in range(6):
                    if i==0: await pg.evaluate(PLACE,[3,0.62,False,0]); await pg.evaluate("()=>{camYaw=0.9}")
                    if i==1:
                        await pg.evaluate(PLACE,[ns.get('kanataksam',3),0.995,False,0]); await pg.evaluate("()=>{G.dmg=18;startDrone();G.orb=1.2}")
                        await frames(pg,20); await pg.evaluate("()=>{const m=world.markers;[0,1].forEach(k=>{if(m[k]){m[k].userData.scanned=true;m[k].material=new THREE.SpriteMaterial({map:TEX.soft,color:k?0xff3b2f:0x46ff7a,transparent:true,depthTest:false,blending:THREE.AdditiveBlending});m[k].userData.bad=!!k}})}")
                    if i==2:
                        await pg.evaluate("()=>{SAVE.tips={gas:1,fork:1,strap:1,drone:1,cam:1,off:1,kanat:1,night:1};resetGame('career',1);const c=crates[0];fork.car.add(c);c.position.set(0,.02,-.78);G.carry=0;fork.car.position.y=1.95;G.lift=1.95;fork.v.x=6;fork.v.z=8;fork.v.h=Math.PI/2-0.3;camYaw=-0.7;snapCam();coachHide()}")
                    if i==3: await pg.evaluate(PLACE,[ns.get("kuleaksam",6),0.12,False,1]); await pg.evaluate("()=>{camYaw=0;truck.v.speed=14;input.gas=1}")
                    if i==4: await pg.evaluate(PLACE,[ns.get('kulegece',8),0.45,False,0]); await pg.evaluate("()=>{camYaw=0.15}")
                    if i==5:
                        await pg.evaluate(PLACE,[2,0.995,False,0]); await pg.evaluate("()=>{G.deliverT=168;G.dmg=0;startDrone();world.markers.forEach(m=>m.userData.scanned=true);G.scanned=world.markers.length;showReport();document.getElementById('rateBox').style.display='none'}")
                    await frames(pg,45 if i!=1 else 25)
                    if i==3: await pg.evaluate("()=>{input.gas=0}")
                    await pg.evaluate("()=>{$('coach').style.display='none';$('toast').style.opacity=0}")
                    await pg.evaluate("""(t)=>{let e=document.getElementById('shotcap');if(!e){e=document.createElement('div');e.id='shotcap';document.body.appendChild(e);}
                      e.style.cssText='position:fixed;left:50%;transform:translateX(-50%);bottom:'+(innerHeight*.30)+'px;z-index:40;padding:8px 22px;border-radius:6px;background:linear-gradient(180deg,rgba(45,74,54,.95),rgba(15,26,19,.95));border:2px solid #f2b632;color:#fff;font:800 '+Math.round(Math.min(innerWidth,innerHeight)*.068)+'px \"Barlow Condensed\";letter-spacing:.02em;white-space:nowrap;box-shadow:0 8px 24px rgba(0,0,0,.5)';e.textContent=t;}""",CAP[lang][i])
                    await pg.wait_for_timeout(150)
                    await pg.screenshot(path=os.path.join(out,f'0{i+1}.png'))
                    await pg.evaluate("()=>{const e=document.getElementById('shotcap');if(e)e.remove();show(null);showHud(true)}")
                if k=='iphone69' and lang=='tr':
                    await pg.evaluate("()=>{openFull(4)}");await pg.wait_for_timeout(400)
                    await pg.screenshot(path=os.path.join(KOK,'store','iap-inceleme.png'))
                await pg.close()
        await b.close()
asyncio.run(main())
