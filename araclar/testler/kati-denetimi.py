# Genel "içinden geçme" denetimi: her hareketli araç, her katı cisme 8 yönden gaz vererek sürülür; gövde noktaları cismin içine girmemeli.
import os
from playwright.sync_api import sync_playwright
KOK='file://'+os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..','www','index.html'))
J="""([hedefSec,arac,ac])=>{const v=arac==='fork'?fork.v:truck.v;const g=eval(hedefSec);g.updateMatrixWorld();const c=new THREE.Vector3(),sz=new THREE.Vector3();const bb=new THREE.Box3().setFromObject(g);bb.getCenter(c);bb.getSize(sz);const R=Math.hypot(sz.x,sz.z)/2+(arac==='fork'?2.6:6.5);
 const h=ac;v.h=h;let RR=R;do{v.x=c.x+Math.sin(h)*RR;v.z=c.z+Math.cos(h)*RR;RR+=.5}while(collides(v,v.x,v.z,true).size&&RR<R+30);v.speed=0;v.steer=0;window._g={g,v,arac,max:0};return [c.x,c.z]}"""
K="""()=>{const {g,v,arac}=_g;const fx=-Math.sin(v.h),fz=-Math.cos(v.h),rx=-fz,rz=fx;const pts=arac==='fork'?[[.45,.7],[.45,-.7],[-.8,.7],[-.8,-.7],[-2,0]]:[[5.2,1],[5.2,-1],[2.5,1.1],[2.5,-1.1]];
 const b=yerelKutu(g);g.updateMatrixWorld();const inv=g.matrixWorld.clone().invert();let ic=0;for(const[a,bb]of pts){const p=new THREE.Vector3(v.x+fx*a+rx*bb,getH(v.x,v.z)+(arac==='fork'?.8:1),v.z+fz*a+rz*bb).applyMatrix4(inv);const d=Math.min(p.x-b.min.x,b.max.x-p.x,p.z-b.min.z,b.max.z-p.z);if(d>.15&&p.y>b.min.y&&p.y<b.max.y)ic=Math.max(ic,d)}return ic}"""
with sync_playwright() as p:
    b=p.chromium.launch(args=['--use-gl=swiftshader','--enable-webgl','--ignore-gpu-blocklist'])
    pg=b.new_page(viewport={'width':400,'height':300});errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto(KOK);pg.wait_for_timeout(900);pg.evaluate("pickLang('tr')")
    pg.evaluate("SAVE.tips={gas:1,fork:1,strap:1,drone:1,cam:1,off:1,kanat:1,night:1,hard:1,lifter:1,chain:1,wind:1};startGame('free')");pg.wait_for_timeout(4500)
    pg.evaluate("(()=>{let n=5;for(;n<900;n++){const j=sefer(n);if(j.type==='kasa')break}resetGame('career',n)})()");pg.wait_for_timeout(2500)
    kotu=[]
    for hedef in ["crates.filter(c=>c.parent===scene)[1]","trailer.g","truck.g"]:
        for k in range(8):
            ac=k*0.785
            pg.evaluate(J,[hedef,'fork',ac]);
            mx=0
            pg.evaluate("input.gas=1")
            for t in range(14):
                pg.wait_for_timeout(600);mx=max(mx,pg.evaluate(K))
            pg.evaluate("input.gas=0")
            if mx>0: kotu.append((hedef[:12],'fork',round(ac,2),round(mx,2)))
    print('forklift bitti',kotu)
    # tır sürüş evresinde forklifte ve yerdeki kasaya
    pg.evaluate("(()=>{phase='drive';G.pst='yolda'})()")
    for hedef in ["fork.g","crates.filter(c=>c.parent===scene)[0]"]:
        for k in range(4):
            ac=k*1.57;pg.evaluate(J,[hedef,'truck',ac]);mx=0;pg.evaluate("input.gas=1")
            for t in range(14):
                pg.wait_for_timeout(700);mx=max(mx,pg.evaluate(K))
            pg.evaluate("input.gas=0")
            if mx>0: kotu.append((hedef[:12],'truck',round(ac,2),round(mx,2)))
    # bölünmüş yol (Hatay, D-817): tır orta refüj bariyerine sürülür; refüjü geçemez, karşı yola inemez
    pg.evaluate("toMenu()");pg.wait_for_timeout(300);pg.evaluate("SAVE.reg='hatay';startGame('free')");pg.wait_for_timeout(5000)
    for f in [0.2,0.5,0.8]:
        r=pg.evaluate(f"""(async()=>{{const i=Math.round(NS*{f});const p=sideAt(i,-2.3),q=sideAt(i+8,-6.2);const v=truck.v;v.x=p.x;v.z=p.z;v.speed=0;v.h=Math.atan2(-(q.x-p.x),-(q.z-p.z));G.ri=i;
          input.gas=1;for(let k=0;k<40;k++)await new Promise(r=>setTimeout(r,100));input.gas=0;return [yanOf(v.x,v.z),yanOf(trailer.g.position.x,trailer.g.position.z)]}})()""")
        print('bariyer',f,[round(x,2) for x in r])
        if min(r)<-5.0: kotu.append(('bariyer',f,r))
    print('SONUÇ',kotu,errs[:3])
    raise SystemExit(1 if kotu or errs else 0)
