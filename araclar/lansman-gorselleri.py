#!/usr/bin/env python3
# Kervan Yolu lansman görselleri (merak-gorselleri.py'nin dili). Kullanım: cek.py sahneler.json oran(4x5|9x16) cikti_klasoru
import asyncio, os, sys, json
from playwright.async_api import async_playwright
KOK=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLACE=open(os.path.join(KOK,'araclar','merak-place.js')).read()
SAH=json.load(open(sys.argv[1])); ORAN=sys.argv[2]; OUT=sys.argv[3]; os.makedirs(OUT,exist_ok=True)
W,H={'4x5':(540,675),'9x16':(540,960),'1x1':(540,540)}[ORAN]
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(args=['--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist'])
        pg=await b.new_page(viewport={'width':W,'height':H},device_scale_factor=2)
        pg.on('pageerror',lambda e:print('HATA',str(e)[:200]))
        await pg.goto('file://'+KOK+'/www/index.html');await pg.wait_for_timeout(800)
        await pg.click('#lang .btn[data-lang=tr]');await pg.wait_for_timeout(200)
        await pg.evaluate("()=>{startGame('free')}");await pg.wait_for_timeout(5000)
        for s in SAH:
            reg,tip=s['reg'],s['tip']
            n=s.get('n') or await pg.evaluate("([r,t,m])=>{for(let n=m;n<1900;n++){const j=sefer(n);if(j.reg===r&&j.type===t)return n}}",[reg,tip,s.get('min',7)])
            await pg.evaluate(f"()=>buildRegion('{reg}')")
            frac=s.get('frac')
            if frac is None: frac=await pg.evaluate("()=>(VZ.v0+14)/(NS-1)")
            await pg.evaluate(PLACE,[n,frac,s.get('back',False),s.get('cm',0)])
            yaw=s.get('yaw',(66,-13,.4))
            cam=f"window._cam=null;camYaw={yaw};" if not isinstance(yaw,list) else f"window._cam=[{yaw[0]},{yaw[1]},{yaw[2]}];"
            look=s.get('look',[18,3.5])
            await pg.evaluate(f"()=>{{setTOD('{s.get('tod','aksam')}');{s.get('ek','')}{cam}if(window._cam){{if(!window._ct)window._ct=camTarget;camTarget=()=>{{const v=truck.v,[D,R,H]=window._cam;const cx=v.x+Math.sin(v.h)*D,cz=v.z+Math.cos(v.h)*D;const p=new THREE.Vector3(cx+Math.cos(v.h)*R,0,cz-Math.sin(v.h)*R);p.y=Math.max(getH(p.x,p.z),truck.g.position.y)+Math.abs(R)*H;return{{p,l:new THREE.Vector3(v.x+Math.sin(v.h)*{look[0]},truck.g.position.y+{look[1]},v.z+Math.cos(v.h)*{look[0]})}}}}}}else if(window._ct)camTarget=window._ct;snapCam();showHud(false);for(const id of['hPause','hSnd','hFM','bcam','limB','fmTk'])document.getElementById(id)&&(document.getElementById(id).style.display='none')}}")
            if s.get('ek2'): await pg.evaluate("()=>{"+s['ek2']+"}")
            for _ in range(s.get('kare',50)): await pg.evaluate("()=>new Promise(r=>requestAnimationFrame(()=>r()))")
            if s.get('ek3'): await pg.evaluate("()=>{"+s['ek3']+"}")
            await pg.evaluate("""([b,k,alt,kapak])=>{document.querySelectorAll('#coach,#toast,#act,.pad,#pedals,#steer,#hud .tb').forEach(e=>e.style.display='none');
             let e=document.getElementById('merak');if(!e){e=document.createElement('div');e.id='merak';document.body.appendChild(e)}
             if(b===null){e.remove();return}
             e.style.cssText='position:fixed;inset:0;z-index:999;pointer-events:none;font-family:"Barlow Condensed",sans-serif;color:#fff;background:linear-gradient(180deg,rgba(0,0,0,.55) 0%,rgba(0,0,0,0) 26%,rgba(0,0,0,0) 56%,rgba(0,0,0,.8) 100%)';
             e.innerHTML=`<div style="position:absolute;top:5%;left:0;right:0;text-align:center;letter-spacing:6px;font-size:15px;font-weight:700;color:#ffcf4a">KERVAN YOLU</div>
             <div style="position:absolute;bottom:17%;left:7%;right:7%;font-size:${kapak?44:36}px;font-weight:800;line-height:1.02;text-shadow:0 2px 14px rgba(0,0,0,.7)">${b}</div>
             <div style="position:absolute;bottom:12.5%;left:7%;right:7%;font-size:15px;letter-spacing:2px;opacity:.88">${k.toLocaleUpperCase('tr-TR')}</div>
             <div style="position:absolute;bottom:4.5%;left:7%;right:7%;display:flex;justify-content:space-between;align-items:flex-end">
              <div style="font-size:${kapak?30:24}px;font-weight:800;color:#ffcf4a;line-height:1">${alt}</div>
              <div style="text-align:right;font-size:13px;opacity:.85;line-height:1.3">1923 sefer<br>Bir Mr. Anduv! yapımıdır.</div></div>`}""",[s.get('buyuk'),s.get('kucuk',''),s.get('alt','App Store’da'),s.get('kapak',False)])
            await pg.wait_for_timeout(300)
            out=os.path.join(OUT,f"{s['ad']}.png");await pg.screenshot(path=out);print(out,n)
            await pg.evaluate("()=>{const m=document.getElementById('merak');m&&m.remove()}")
        await b.close()
asyncio.run(main())
