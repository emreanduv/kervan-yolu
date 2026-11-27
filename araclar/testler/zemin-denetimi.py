# Zemin denetimi: tır tekerleği nerede duruyorsa (getH + 0,2) görünen sürüş yüzeyi (yol şeridi, cep, rıhtım, saha) da orada olmalı.
# Yolun her iki şeridi, cep giriş-çıkış yolları ve sahaya giriş yukarıdan aşağı ışınla taranır; yüzey tekerlekten 0,1 m yüksekse tır yola gömülür,
# 0,35 m alçaksa havada durur. İkisi de hatadır.
import os,sys
from playwright.sync_api import sync_playwright
KOK='file://'+os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..','www','index.html'))
REG=(sys.argv[1] if len(sys.argv)>1 else 'marmara,ege,sivas,trakya,canakkale,hatay,karadeniz,kapadokya').split(',')
J="""(()=>{const rc=new THREE.Raycaster();rc.camera=camera;const out=[];const ex=new Set();for(const g of [truck.g,trailer.g])g.traverse(o=>ex.add(o));
 const obj=[];scene.traverse(o=>{if(!o.isMesh||ex.has(o)||!o.visible||(o.material&&o.material.transparent))return;for(let q=o;q;q=q.parent){if(q.userData&&(q.userData.dinamik||q.userData.gecirgen))return}if(!o.geometry.boundingBox)o.geometry.computeBoundingBox();const b=o.geometry.boundingBox.clone().applyMatrix4(o.matrixWorld);if(Math.max(b.max.x-b.min.x,b.max.z-b.min.z)>8&&(()=>{const lb=o.geometry.boundingBox;const d=[lb.max.x-lb.min.x,lb.max.y-lb.min.y,lb.max.z-lb.min.z].sort((a,c)=>c-a);return d[1]>1.5})()&&b.max.y-b.min.y<3)obj.push(o)/* sürüş yüzeyi: geniş ve yassı; bordür, ray sayılmaz */});
 const yokla=(x,z,lab)=>{const t=getH(x,z)+.2;rc.set(new THREE.Vector3(x,t+3,z),new THREE.Vector3(0,-1,0));rc.far=4;const h=rc.intersectObjects(obj,false).filter(q=>{const n=q.face&&q.face.normal.clone().transformDirection(q.object.matrixWorld);return n&&n.y>.85})[0];if(!h)return;const d=h.point.y-t;if(d>.1||d<-.35)out.push([lab,+d.toFixed(2),Math.round(x),Math.round(z)])};
 for(let i=2;i<NS-1;i++)for(const o of[-LANE,LANE])yokla(...(p=>[p.x,p.z])(sideAt(i,o)),'yol'+i);
 try{for(const p of cepNoktalari())yokla(p.x,p.z,'cep')}catch(e){}
 const a=RS[NS-12];for(let k=0;k<=20;k++){const f=k/20;yokla(a.x+(SITE.x-a.x)*f,a.z+(SITE.z-a.z)*f,'saha')}
 return out})()"""
kotu=0
with sync_playwright() as p:
    b=p.chromium.launch(args=['--use-gl=swiftshader']);pg=b.new_page();errs=[];pg.on('pageerror',lambda e:errs.append(str(e)));pg.goto(KOK);pg.wait_for_timeout(900);pg.evaluate("pickLang('tr')")
    for r in REG:
        pg.evaluate(f"SAVE.reg='{r}';startGame('free')");pg.wait_for_timeout(4000);o=pg.evaluate(J);print(r,len(o),sorted(o,key=lambda q:-abs(q[1]))[:6]);kotu+=len(o);pg.evaluate("toMenu()");pg.wait_for_timeout(300)
    print('hata',errs[:3])
raise SystemExit(1 if kotu or errs else 0)
