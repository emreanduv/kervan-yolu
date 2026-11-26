# Hava hattı denetimi: yolun üstünden geçen her telin (TubeGeometry) şerit üstündeki en alçak noktası ölçülür.
# Kural: hiçbir tel (görünmeyen etüt telleri dahil) boş tırın tepesine (kabin) değecek kadar alçakta olamaz; etüt telleri yalnız yüksek yüke değer.
import os,sys,json
from playwright.sync_api import sync_playwright
KOK='file://'+os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..','www','index.html'))
REG=(sys.argv[1] if len(sys.argv)>1 else 'marmara,ege,sivas,trakya,canakkale,hatay,karadeniz,kapadokya').split(',')
J="""(()=>{const out=[];const v=new THREE.Vector3();scene.updateMatrixWorld(true);
 scene.traverse(o=>{if(!o.isMesh||!o.geometry||o.geometry.type!=='TubeGeometry'||!o.geometry.parameters.path)return;let vis=true;for(let q=o;q;q=q.parent)if(!q.visible){vis=false;break}
  const P=o.geometry.parameters.path.getPoints(60);let mn=1e9,at=-1;for(const p of P){v.copy(p).applyMatrix4(o.matrixWorld);let bi=0,bd=1e9;for(let i=1;i<NS-1;i++){const d=(RS[i].x-v.x)**2+(RS[i].z-v.z)**2;if(d<bd){bd=d;bi=i}}
   if(Math.sqrt(bd)<6.5){const c=v.y-yolTepe(bi);if(c<mn){mn=c;at=bi}}}
  if(at>=0)out.push([+mn.toFixed(2),at,vis])});
 const tep=aracTepe()-yolTepe(roadIdx(truck.v));return {teller:out.sort((a,b)=>a[0]-b[0]).slice(0,8),bos:+tep.toFixed(2)}})()"""
YUK="""(()=>{const r={};for(const t of['kule','kanat','raf','yedek'])if(CARGO[t]){for(const k in CARGO)CARGO[k].visible=false;CARGO[t].visible=true;r[t]=+(aracTepe()-yolTepe(roadIdx(truck.v))).toFixed(2)}
 if(CARGO.kanat){for(const k in CARGO)CARGO[k].visible=false;CARGO.kanat.visible=true;const y=CARGO.kanat.position.y;CARGO.kanat.position.y=3.3;r.kanat_alcak=+(aracTepe()-yolTepe(roadIdx(truck.v))).toFixed(2);CARGO.kanat.position.y=y}for(const k in CARGO)CARGO[k].visible=false;return r})()"""
kotu=0
with sync_playwright() as p:
    b=p.chromium.launch(args=['--use-gl=swiftshader']);pg=b.new_page();errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto(KOK);pg.wait_for_timeout(900);pg.evaluate("pickLang('tr')")
    for n,r in enumerate(REG):
        pg.evaluate(f"SAVE.reg='{r}';startGame('free')");pg.wait_for_timeout(4000)
        d=pg.evaluate(J)
        if n==0:
            y=pg.evaluate(YUK);print('yük tepeleri',y)
            # etüt telleri: düzenlenmemiş tel 6,0 m, köy kablosu 5,85 m. Yüksek yük değer, boş/raf/alçak kanat geçer.
            kural=[y['kule']>6.05,y['kanat']>6.05,y['kanat_alcak']<5.8,y['raf']<5.8]
            if not all(kural):print('KURAL TUTMADI',kural);kotu+=1
        alcak=[t for t in d['teller'] if t[0]<d['bos']+.3]  # gizli (düzenlenmemiş etüt) teller dahil
        print(r,'boş tır',d['bos'],'en alçak teller',d['teller'][:4],'KÖTÜ' if alcak else '');kotu+=len(alcak)
        pg.evaluate("toMenu()");pg.wait_for_timeout(300)
    print('hata',errs[:3])
raise SystemExit(1 if kotu or errs else 0)
