# Rampa denetimi (TAKILMA YOK kuralı): hiçbir bölgede, en ağır yükle (nasel), tır kalıcı olarak takılmaz.
# 1) Yolun en dik yerinde (karlıysa zincirli) gaza basılınca 12 saniyede en az 8 m ilerler.
# 2) Yağmurlu seferde saha yolunun çamurunda: ya ilerler ya da 6 saniye içinde "Dozer çağır" düğmesi çıkar (kurtarma yazısı onu örtmez).
# 3) Zorunlu durağı (geri manevra halkası) geçip duran tır kilitlenmez: durduğu yerde manevra düğmesi çıkar, kurtarma yazısı onu örtmez.
# 4) Aynı yerde ikinci kez "Aracı yola çıkar" gerekirse çekici tırı en az 60 m ileri çeker.
# Kaynak: Emre, 28 Kasım 2026, Karadeniz saha rampasında yağmurlu nasel seferi kaldı.
import os,sys
from playwright.sync_api import sync_playwright
KOK='file://'+os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..','www','index.html'))
REG=(sys.argv[1] if len(sys.argv)>1 else 'marmara,ege,sivas,trakya,canakkale,hatay,karadeniz,kapadokya').split(',')
KUR="""(async([i0,mud,chain])=>{phase='drive';G.pst='yolda';G.strapped=true;G.job.type='nasel';G.chain=chain;G.mud=mud;G.dozT=null;G.mudS=0;G.stuckT=0;G.manOk=true;setAct(null);
 const v=truck.v;v.x=RS[i0].x;v.z=RS[i0].z;rescue();G.rsc=null;window.__adim(5);const s0=roadIdx(v);clearInterval(window.__oto);input.gas=1;let doz=false;
 for(let k=0;k<24;k++){window.__adim(15);if(actFn&&actFn.dozer)doz=true}input.gas=0;window.__oto=setInterval(()=>window.__adim(1),40);const s1=roadIdx(v);return [(s1-s0)*ROADLEN/(NS-1),doz,+(v.slope||0).toFixed(3)]})"""
kotu=[]
with sync_playwright() as p:
    b=p.chromium.launch(args=['--use-gl=swiftshader']);pg=b.new_page(viewport={'width':500,'height':500});errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.add_init_script("""(()=>{const cbs=[];let T=0;window.__adim=(n)=>{for(let k=0;k<n;k++){T+=1000/30;const c=cbs.splice(0);for(const f of c)try{f(T)}catch(e){console.error(e)}}};window.requestAnimationFrame=f=>{cbs.push(f);return cbs.length};window.__oto=setInterval(()=>window.__adim(1),40)})()""");pg.goto(KOK);pg.wait_for_timeout(900);pg.evaluate("pickLang('tr')")
    for r in REG:
        n=pg.evaluate(f"(()=>{{for(let n=1;n<900;n++){{const j=sefer(n);if(j.reg==='{r}'&&j.type!=='donus')return n}}return -1}})()")
        if n<0: print(r,'sefer yok');continue
        pg.evaluate(f"startGame('career',{n})");pg.wait_for_timeout(4500)
        dik=pg.evaluate("(()=>{let bi=80,bs=-1;const ds=ROADLEN/(NS-1),w=Math.max(2,Math.round(20/ds));for(let i=80;i<NS-140;i+=2){const s=(RY[i+w]-RY[i])/(w*ds);if(s>bs){bs=s;bi=i}}return [bi,bs]})()")
        kar=pg.evaluate("RG().snow?1:0")
        a=pg.evaluate(KUR,[dik[0],False,kar]);print(r,'en dik',round(dik[1]*100,1),'%',a)
        if a[0]<8: kotu.append((r,'yokuş',dik,a))
        sa=pg.evaluate("NS-1-64-4")
        c=pg.evaluate(KUR,[sa,True,kar]);print(r,'çamur',c)
        if c[0]<8 and not c[1]: kotu.append((r,'çamur',c))
        mr=pg.evaluate("""(()=>{const M=window.SANTIYE&&SANTIYE.MR();if(!M)return null;phase='drive';G.manOk=false;G.manT=undefined;G.job.type='nasel';G.job.dummy=false;G.mud=false;setAct(null);G.stuckT=0;
          const v=truck.v;const i=M.i+6;v.x=RS[i].x;v.z=RS[i].z;rescue();G.rsc=null;clearInterval(window.__oto);input.gas=1;let man=false;for(let k=0;k<10;k++){window.__adim(15);input.gas=k<4?1:0;if(actFn&&actFn.man)man=true}input.gas=0;window.__oto=setInterval(()=>window.__adim(1),40);return man})()""")
        if mr is not None:
            print(r,'manevra halkası geçildi, düğme',mr)
            if not mr: kotu.append((r,'manevra',mr))
        t=pg.evaluate("""(()=>{phase='drive';G.mud=false;const v=truck.v;const i=Math.round(NS*.4);v.x=RS[i].x;v.z=RS[i].z;rescue();const a=roadIdx(v);rescue();const b=roadIdx(v);return (b-a)*ROADLEN/(NS-1)})()""")
        print(r,'çekici',round(t,1))
        if t<60: kotu.append((r,'çekici',t))
        pg.evaluate("toMenu()");pg.wait_for_timeout(300)
    print('SONUÇ',kotu,errs[:3])
raise SystemExit(1 if kotu or errs else 0)
