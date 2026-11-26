# Gövde denetimi: tır yol kenarındaki katı nesnelere (levha, direk, bina, kulübe) doğru sürülür; tırın, dorsenin ya da yükün
# dış çizgisindeki hiçbir nokta nesnenin içine girmemeli. Yük olarak konteyner (geniş, yüksek) kullanılır.
import os,sys
from playwright.sync_api import sync_playwright
KOK='file://'+os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..','www','index.html'))
REG=(sys.argv[1] if len(sys.argv)>1 else 'marmara,sivas').split(',')
HEDEF="""(k)=>{const L=[];for(const[key,a]of KD.h)for(const e of a){if(L.includes(e)||(e.o&&!kdGorunur(e.o)))continue;const sz=e.boy;if(sz[1]<1.2)continue;const i=roadIdx({x:e.position.x,z:e.position.z});if(i<90||i>NS-90)continue;const p=sideAt(i,0);const d=Math.hypot(p.x-e.position.x,p.z-e.position.z);if(d>5.5&&d<14)L.push(e)}
 L.sort((a,b)=>a.position.x-b.position.x);const e=L[Math.floor(L.length*k/8)];if(!e)return null;window._E=e;const i=roadIdx({x:e.position.x,z:e.position.z});const p0=sideAt(i,0),p1=sideAt(i,1);const sag=((e.position.x-p0.x)*(p1.x-p0.x)+(e.position.z-p0.z)*(p1.z-p0.z))>0;
 const j=i-Math.round(16/(ROADLEN/(NS-1)));const q=sideAt(j,sag?LANE:-LANE);const v=truck.v;v.x=q.x;v.z=q.z;v.speed=3;v.h=Math.atan2(-(RS[j+1].x-RS[j].x),-(RS[j+1].z-RS[j].z));trailer.th=v.h;snapCam();window._sag=sag;return [i,e.tip,e.boy.join('x'),sag]}"""
OLC="""()=>{const e=_E;let ic=0;for(const[g,y]of[[truck.g,false],[trailer.g,false],[trailer.g,true]]){const b=cevreKutu(g,y);g.updateMatrixWorld();for(const[x,yy,z]of cevreNoktalari(b,1)){const w=new THREE.Vector3(x,yy,z).applyMatrix4(g.matrixWorld);const p=w.applyMatrix4(e.inv);const B=e.b;const d=Math.min(p.x-B.min.x,B.max.x-p.x,p.z-B.min.z,B.max.z-p.z,p.y-B.min.y,B.max.y-p.y);if(d>.25)ic=Math.max(ic,d)}}return ic}"""
kotu=[]
with sync_playwright() as p:
    b=p.chromium.launch(args=['--use-gl=swiftshader','--enable-webgl','--ignore-gpu-blocklist']);pg=b.new_page(viewport={'width':400,'height':300});errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto(KOK);pg.wait_for_timeout(900);pg.evaluate("pickLang('tr')")
    for r in REG:
        pg.evaluate(f"SAVE.reg='{r}';SAVE.tips={{gas:1,fork:1,strap:1,drone:1,cam:1,off:1,kanat:1,night:1,hard:1,lifter:1,chain:1,wind:1}};startGame('free')");pg.wait_for_timeout(4500)
        pg.evaluate(f"(()=>{{let n=5;for(;n<900;n++){{const j=sefer(n);if(j.type==='konteyner')break}}SAVE.reg='{r}';resetGame('career',n);document.getElementById('docs').classList.remove('on');G.docs=true;G.pst='yolda';G.gateOk=true;phase='drive';doStrap()}})()");pg.wait_for_timeout(2000)
        for k in range(8):
            h=pg.evaluate(HEDEF,k)
            if not h: continue
            # kinematik süpürme (kare hızından bağımsız): tır nesneye doğru 10 cm adımlarla itilir; oyunun kendi engel() kararı uygulanır
            mx=pg.evaluate("""()=>{const v=truck.v,e=_E;let mx=0;const olc=%s;for(let s=0;s<450;s++){const hx=e.position.x-v.x,hz=e.position.z-v.z;const hh=Math.atan2(-hx,-hz);let dh=hh-v.h;while(dh>Math.PI)dh-=2*Math.PI;while(dh<-Math.PI)dh+=2*Math.PI;v.h+=Math.max(-.02,Math.min(.02,dh));
              const nx=v.x-Math.sin(v.h)*.1,nz=v.z-Math.cos(v.h)*.1;if(engel(v,nx,nz))break;const dx=nx-v.x,dz=nz-v.z;v.x=nx;v.z=nz;truck.g.position.x+=dx;truck.g.position.z+=dz;truck.g.rotation.y=v.h;trailer.g.position.x+=dx;trailer.g.position.z+=dz;truck.g.updateMatrixWorld(true);trailer.g.updateMatrixWorld(true);mx=Math.max(mx,olc())}return mx}""" % OLC)
            print(r,k,h,'girdi' if mx else 'temiz',round(mx,2))
            if mx: kotu.append((r,h,round(mx,2)))
        pg.evaluate("toMenu()");pg.wait_for_timeout(300)
    print('SONUÇ',kotu,errs[:3])
raise SystemExit(1 if kotu or errs else 0)
