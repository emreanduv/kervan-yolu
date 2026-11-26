# Animasyon denetimi: vinçle yapılan her taşıma (limanda gemiden dorseye tahliye, sahada dorseden istife indirme ve kuleye montaj)
# adım adım oynatılır; taşınan yükün yüzeyindeki noktalar katı dünyaya (katiDunyaVar) sorulur. Yük hiçbir katı nesnenin içinden geçmemeli.
# Hedef kule (montajda yerine oturan parça) ve istifteki eski parçalar sayılmaz.
import os,sys
from playwright.sync_api import sync_playwright
KOK='file://'+os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..','www','index.html'))
REG=(sys.argv[1] if len(sys.argv)>1 else 'marmara,ege,sivas,trakya,canakkale,hatay,karadeniz,kapadokya').split(',')
ORT="""window.__yuzey=(root,haric)=>{const out=[];const B=new THREE.Box3(),v=new THREE.Vector3();root.updateWorldMatrix(true,true);root.traverseVisible(o=>{if(!o.isMesh||!o.geometry)return;if(!o.geometry.boundingBox)o.geometry.computeBoundingBox();const b=o.geometry.boundingBox;
  for(const fx of[0,.5,1])for(const fy of[0,.5,1])for(const fz of[0,.5,1]){if(fx===.5&&fy===.5&&fz===.5)continue;v.set(b.min.x+(b.max.x-b.min.x)*fx,b.min.y+(b.max.y-b.min.y)*fy,b.min.z+(b.max.z-b.min.z)*fz).applyMatrix4(o.matrixWorld);
   const e=katiDunyaVar(v.x,v.y,v.z);if(e&&!haric(e.o)){out.push([e.tip||'?',e.boy&&e.boy.join('x'),+v.y.toFixed(1)]);return}}});return out};
 window.__altinda=(o,kok)=>{for(let q=o;q;q=q.parent)if(q===kok)return true;return false};"""
TAH="""((tip)=>{for(const k in CARGO)CARGO[k].visible=false;CARGO[tip].visible=true;tahliyeStart();const bad=[];let n=0;while(phase==='tahliye'&&n<400){tahliyeStep(.05);n++;const h=__yuzey(trailer.cargo,o=>false);if(h.length)bad.push([n,h[0]])}return [n,bad.length,bad.slice(0,3)]})"""
MON="""((tip,ind)=>{const S=SANTIYE;let bitti=0;S.montajBasla(tip,()=>{bitti=1},ind);const M=S.MT();if(!M)return 'MT yok';M.oto=true;const K=S.KULE();const ist=S.ISTIF().slice();const bad=[];let n=0;
  while(S.MT()&&n<600){S.mtAdim(.05);n++;const m=S.MT();if(!m)break;const h=__yuzey(m.parca,o=>__altinda(o,K.g)||(tip==='ankraj'&&!ind&&__altinda(o,K.tg))||ist.some(x=>__altinda(o,x)));if(h.length)bad.push([n,h[0]])}phase='drive';return [n,bad.length,bad.slice(0,3)]})"""
kotu=0
with sync_playwright() as p:
    b=p.chromium.launch(args=['--use-gl=swiftshader']);pg=b.new_page();errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto(KOK);pg.wait_for_timeout(900);pg.evaluate("pickLang('tr')")
    for r in REG:
        pg.evaluate(f"SAVE.reg='{r}';startGame('free')");pg.wait_for_timeout(4000);pg.evaluate(ORT)
        for t in ['kule','kanat','nasel','hub','konteyner']:
            if not pg.evaluate(f"!!CARGO['{t}']"):continue
            res=pg.evaluate(TAH+f"('{t}')");print(r,'tahliye',t,res);kotu+=res[1]
        for t in ['kule','kanat','nasel','hub','ankraj']:
            for ind in [True,False]:
                pg.evaluate(f"for(const k in CARGO)CARGO[k].visible=false;if(CARGO['{t}'])CARGO['{t}'].visible=true;truck.v.x=SITE.x;truck.v.z=SITE.z;placeVehicles(0)")
                res=pg.evaluate(MON+f"('{t}',{'true' if ind else 'false'})");print(r,'indir' if ind else 'montaj',t,res)
                if isinstance(res,list):kotu+=res[1]
        pg.evaluate("toMenu()");pg.wait_for_timeout(300)
    print('hata',errs[:3])
raise SystemExit(1 if kotu or errs else 0)
