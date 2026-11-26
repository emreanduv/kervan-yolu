# Hareketli katı cisim denetimi: hemzemin geçitte tren tırın içinden geçmez; tır geçitteyse tren acil fren yapar, değip durur, yol açılınca devam eder.
import os
from playwright.sync_api import sync_playwright
KOK='file://'+os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..','www','index.html'))
with sync_playwright() as p:
    b=p.chromium.launch(args=['--use-gl=swiftshader','--enable-webgl','--ignore-gpu-blocklist'])
    pg=b.new_page(viewport={'width':800,'height':450});errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto(KOK);pg.wait_for_timeout(900);pg.evaluate("pickLang('tr')")
    pg.evaluate("SAVE.reg='marmara';SAVE.tips={gas:1,fork:1,strap:1,drone:1,cam:1,off:1,kanat:1,night:1,hard:1,lifter:1,chain:1,wind:1};startGame('free')");pg.wait_for_timeout(5000)
    pg.evaluate("(()=>{let n=5;for(;n<900;n++){const j=sefer(n);if(j.type==='kule'&&j.reg==='marmara')break}resetGame('career',n);document.getElementById('docs').classList.remove('on');G.docs=true;G.pst='yolda';G.gateOk=true;doStrap();phase='drive'})()");pg.wait_for_timeout(2000)
    H=pg.evaluate("(()=>{const H=SANTIYE.HZ();return H?[H.ri,H.st]:null})()");print('HZ',H)
    # 1) tır geçidin üstünde dururken tren gelir
    pg.evaluate("(()=>{const H=SANTIYE.HZ();const i=H.ri;const p=sideAt(i,LANE);truck.v.x=p.x;truck.v.z=p.z;truck.v.speed=0;truck.v.h=Math.atan2(-(RS[i+1].x-RS[i].x),-(RS[i+1].z-RS[i].z));snapCam();H.tetik=true;H.st='kapali';H.s=-22;H.t=4})()")
    for k in range(10):
        pg.wait_for_timeout(1000)
    r=pg.evaluate("(()=>{const H=SANTIYE.HZ();return [Math.round(H.s),H.fren,H.kaza,G.dmg,aracaDegiyor(H.train)]})()");print('tren tırda',r)
    # 2) tır çekilince tren devam eder
    pg.evaluate("(()=>{const H=SANTIYE.HZ();const i=H.ri-30;const p=sideAt(i,LANE);truck.v.x=p.x;truck.v.z=p.z;snapCam();H.s=Math.max(H.s,-10)})()");pg.wait_for_timeout(6000)
    print('tır çekildi',pg.evaluate("(()=>{const H=SANTIYE.HZ();return [Math.round(H.s),H.fren,H.st]})()"))
    # 3) tır trene doğru sürülür
    pg.evaluate("(()=>{const H=SANTIYE.HZ();H.st='kapali';H.s=-8;H.fren=false;const i=H.ri-12;const p=sideAt(i,LANE);truck.v.x=p.x;truck.v.z=p.z;truck.v.speed=6;truck.v.h=Math.atan2(-(RS[i+1].x-RS[i].x),-(RS[i+1].z-RS[i].z));window._s0=()=>{H.s=-8}})()")
    for k in range(8):
        pg.evaluate("_s0();input.gas=1");pg.wait_for_timeout(500)
    pg.evaluate("input.gas=0")
    print('tır trene',pg.evaluate("(()=>{const H=SANTIYE.HZ();return [aracaDegiyor(H.train),Math.round(((H.ri-roadF(truck.v))*ROADLEN/(NS-1))*10)/10]})()"))
    a=pg.evaluate("(()=>{const H=SANTIYE.HZ();return [H.s,H.fren,H.kaza]})()")
    print(errs)
    raise SystemExit(0 if (r[1] and r[2] and not r[4] and not errs) else 1)
