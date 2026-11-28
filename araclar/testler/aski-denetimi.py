# Vinç bağlaması denetimi (Emre, 28 Kasım 2026): yük tek halatla bir ucundan asılmaz.
# Limanda gemiden dorseye tahliyede (nasel, kanat): kaldırma kirişi + dört sapan görünür, kanca yükün ağırlık merkezinin
# (parçaların hacimle ağırlıklı ortası) düşey üstündedir (yatay sapma < 0,3 m) ve yükün tepesinden yüksektedir.
import os,sys
from playwright.sync_api import sync_playwright
KOK='file://'+os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..','www','index.html'))
REG=(sys.argv[1] if len(sys.argv)>1 else 'marmara,karadeniz').split(',')
kotu=[]
with sync_playwright() as p:
    b=p.chromium.launch(args=['--use-gl=swiftshader']);pg=b.new_page(viewport={'width':500,'height':500});errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto(KOK);pg.wait_for_timeout(900);pg.evaluate("pickLang('tr')")
    for r in REG:
        for typ in ['nasel','kanat']:
            n=pg.evaluate(f"(()=>{{for(let n=1;n<900;n++){{const j=sefer(n);if(j.reg==='{r}'&&j.type==='{typ}')return n}}return -1}})()")
            if n<0: print(r,typ,'sefer yok');continue
            pg.evaluate(f"startGame('career',{n})");pg.wait_for_timeout(4000)
            if pg.evaluate("phase")!='tahliye': print(r,typ,'tahliye yok');pg.evaluate("toMenu()");continue
            o=[]
            for k in range(6):
                pg.wait_for_timeout(700)
                o.append(pg.evaluate("""(()=>{const A=window._ASKI,V=PORTOPS.lv;if(!A||!V||!V.aski||!V.aski.g.visible)return null;const bb=new THREE.Box3();trailer.cargo.traverse(q=>{if(q.isMesh&&!q.userData.aski){let z=q;while(z){if(!z.visible)return;z=z.parent}bb.expandByObject(q)}});
                  return [+Math.hypot(A.H.x-A.merkez.x,A.H.z-A.merkez.z).toFixed(2),+(A.H.y-bb.max.y).toFixed(2),V.aski.s.length]})()"""))
            o=[x for x in o if x]
            print(r,typ,o)
            if not o or any(x[0]>.3 or x[1]<1 or x[2]<6 for x in o): kotu.append((r,typ,o))
            pg.evaluate("toMenu()");pg.wait_for_timeout(300)
    print('SONUÇ',kotu,errs[:3])
raise SystemExit(1 if kotu or errs else 0)
