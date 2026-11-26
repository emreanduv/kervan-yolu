# Katı dünya denetimi: her bölgede yol şeridinde, cep girişlerinde ve teslim noktasında tırı durduracak katı nesne olmamalı.
import os,sys
from playwright.sync_api import sync_playwright
KOK='file://'+os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..','www','index.html'))
REG=(sys.argv[1] if len(sys.argv)>1 else 'marmara,ege,sivas,trakya,canakkale,hatay,karadeniz,kapadokya').split(',')
J="""(()=>{katiDunyaKur();const dsm=ROADLEN/(NS-1);const bad=[];const ch=(nm,x,z)=>{for(const dy of[1,2.4]){const e=katiDunyaVar(x,getH(x,z)+dy,z);if(e){bad.push(nm+' '+e.tip+' '+e.boy.join('x'));return}}};
 for(let i=2;i<NS-2;i++)for(const off of[LANE,0,-LANE]){const p=sideAt(i,off);ch('yol'+i,p.x,p.z)}
 const cep=(nm,ri,off)=>{for(let d=-50;d<=14;d++){const i=Math.round(ri+d/dsm);const k=Math.max(0,Math.min(1,(d+45)/40));const o=LANE+(off-LANE)*k;for(const w of[-1.3,0,1.3]){const p=sideAt(i,o+w);ch(nm+d,p.x,p.z)}}};
 if(PORTOPS.mola)cep('yakit',PORTOPS.mola.ri,CEP.yakit);if(PLAN&&PLAN.ki)cep('kantar',PLAN.ki,CEP.kantar);if(CZ)cep('zincir',CZ.ci,8.4);ch('teslim',SITE.x,SITE.z);return [KD.n,bad.slice(0,6),bad.length]})()"""
kotu=0
with sync_playwright() as p:
    b=p.chromium.launch(args=['--use-gl=swiftshader']);pg=b.new_page();errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto(KOK);pg.wait_for_timeout(900);pg.evaluate("pickLang('tr')")
    for r in REG:
        pg.evaluate(f"SAVE.reg='{r}';startGame('free')");pg.wait_for_timeout(4000)
        n,ornek,say=pg.evaluate(J);print(r,'katı nesne',n,'engel',say,ornek);kotu+=say
        pg.evaluate("toMenu()");pg.wait_for_timeout(300)
    print('hata',errs[:3])
raise SystemExit(1 if kotu or errs else 0)
