# Üst açıklık denetimi: tırın girebildiği yerlerde (yol şeridi, cepler, gümrük/akaryakıt sahası) yolun ÜSTÜNDE asılı duran
# hiçbir şey (tabela, kanopi, kiriş, köprü altı) en yüksek yükün tepesi + 0,4 m'den alçak olamaz. Tel denetimi ayrı (tel-denetimi.py).
import os,sys
from playwright.sync_api import sync_playwright
KOK='file://'+os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..','www','index.html'))
REG=(sys.argv[1] if len(sys.argv)>1 else 'marmara,ege,sivas,trakya,canakkale,hatay,karadeniz,kapadokya').split(',')
MAXY="""(()=>{let m=0;const R={};const r=yolTepe(roadIdx(truck.v));for(const t in CARGO){for(const k in CARGO)CARGO[k].visible=false;CARGO[t].visible=true;const h=aracTepe()-r;R[t]=+h.toFixed(2);m=Math.max(m,h)}for(const k in CARGO)CARGO[k].visible=false;return [m,R]})()"""
J="""((LIM)=>{const out=[];const B=new THREE.Box3(),v=new THREE.Vector3();scene.updateMatrixWorld(true);
 const surus=[];for(let i=2;i<NS-2;i+=1)for(const o of[-ZARF_YAN,-LANE,0,LANE,ZARF_YAN])surus.push(sideAt(i,o));
 const ek=[];const cep=(ri,off)=>{for(let d=-40;d<=14;d+=2){const i=Math.round(ri+d/(ROADLEN/(NS-1)));for(const w of[-2.5,0,2.5])ek.push(sideAt(Math.max(1,Math.min(NS-2,i)),off+w))}};
 if(PORTOPS.mola)cep(PORTOPS.mola.ri,CEP.yakit);if(PLAN&&PLAN.ki)cep(PLAN.ki,CEP.kantar);if(CZ)cep(CZ.ci,CEP.zincir);
 const P=surus.concat(ek);
 scene.traverse(o=>{if(!o.isMesh||!o.geometry||o===truck.g)return;for(let q=o;q;q=q.parent){if(q===truck.g||q===trailer.g||(q.userData&&(q.userData.dinamik||q.userData.etutKotu||q.userData.gecirgen)))return}
  if(o.geometry.type==='TubeGeometry')return;if(!o.geometry.boundingBox)o.geometry.computeBoundingBox();B.copy(o.geometry.boundingBox).applyMatrix4(o.matrixWorld);
  const sx=B.max.x-B.min.x,sz=B.max.z-B.min.z;if(sx>200||sz>200)return;
  const inv=new THREE.Matrix4().copy(o.matrixWorld).invert();const lb=o.geometry.boundingBox.clone();const ince=(a,b)=>{if(lb.max[a]-lb.min[a]<.3){const m=(lb.max[a]+lb.min[a])/2;lb.min[a]=m-.15;lb.max[a]=m+.15}};ince('x');ince('y');ince('z');
  for(const p of P){if(p.x<B.min.x-.05||p.x>B.max.x+.05||p.z<B.min.z-.05||p.z>B.max.z+.05)continue;const g=getH(p.x,p.z);let alt=null;
   for(let h=.7;h<LIM;h+=.25){v.set(p.x,g+h,p.z).applyMatrix4(inv);if(lb.containsPoint(v)){alt=h;break}}
   if(alt===null)continue;if(alt>2.5&&alt<LIM){const ri=roadIdx({x:p.x,z:p.z});const c=o.material&&o.material.color?o.material.color.getHexString():'-';const gp=o.geometry.parameters||{};const yer=Math.hypot(p.x-SITE.x,p.z-SITE.z)<60?'SAHA':PORTOPS.mola&&Math.abs(ri-PORTOPS.mola.ri)<30?'YAKIT':PLAN&&PLAN.ki&&Math.abs(ri-PLAN.ki)<30?'KANTAR':CZ&&Math.abs(ri-CZ.ci)<30?'ZINCIR':'yol'+ri;out.push([+(+alt).toFixed(2),o.geometry.type,+(B.max.y-g).toFixed(2),yer,c,JSON.stringify(gp).slice(0,60)]);break}}});
 return out.sort((a,b)=>a[0]-b[0])})"""
kotu=0
with sync_playwright() as p:
    b=p.chromium.launch(args=['--use-gl=swiftshader']);pg=b.new_page();errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto(KOK);pg.wait_for_timeout(900);pg.evaluate("pickLang('tr')")
    for n,r in enumerate(REG):
        pg.evaluate(f"SAVE.reg='{r}';startGame('free')");pg.wait_for_timeout(4000)
        m,R=pg.evaluate(MAXY);lim=m+.4
        zu=pg.evaluate('ZARF_UST')
        if lim>zu+.01:print('ZARF_UST küçük',lim,zu);kotu+=1
        if n==0:print(R)
        bad=pg.evaluate(J+f"({lim})")
        print(r,'en yüksek yük',round(m,2),'alçak üst yapı',len(bad),bad);kotu+=len(bad)
        pg.evaluate("toMenu()");pg.wait_for_timeout(300)
    print('hata',errs[:3])
raise SystemExit(1 if kotu or errs else 0)
