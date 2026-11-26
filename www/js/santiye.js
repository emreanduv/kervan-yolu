// 1.1 "Şantiye": deneme sürüşü seferi, 80 m kanat sınıfı, alçak uç çerçevesi, hemzemin geçit, manevra alanı, vinçle montaj
// Yöntem gerçek bir güzergâh etüdü ve kanat taşıma çiziminden örnek alındı; ad, yer ve kişi bilgisi yok.
(function(){
'use strict';
const TRs={
 dsKart:'GÜZERGÂH DENEME SÜRÜŞÜ',dsTxt:'{r}: boş ve tam boy uzatılmış dorseyle güzergâhı sür, engelleri gördükçe işaretle. Yatırımcı öder; işaretlediğin her engel prim. Yapılınca etüt raporu eksiksiz çıkar.',dsBtn:'DENEME SÜRÜŞÜNE ÇIK',dsTamam:'{r}: deneme sürüşü yapıldı ✓',
 dsBaslik:'Deneme sürüşü',dsIpucu:'Deneme sürüşü: yük yok, dorse tam boy açık. Engeli gördüğünde İŞARETLE düğmesine bas.',a_isaret:'İŞARETLE: {e}',t_isaret:'İşaretlendi: {e}',t_kacti:'Kaçırdın: {e}',k_dsPrim:'Deneme sürüşü primi ({n} engel)',
 cerH:'KANAT UÇ ÇERÇEVESİ',cerStd:'Standart',cerAlc:'Alçak',cerTxt:'Alçak çerçeve kanadı yaklaşık 45 cm indirir: alçak kablo ve hatların altından geçer, ama en çok 40 km/sa ve uyarlama bedeli var.',k_cerceve:'Alçak uç çerçevesi uyarlaması',
 kl80:'Kanat: 80 m sınıfı · 28,5 t · 4,5 m genişlik',kl72:'Kanat: 72 m sınıfı · 24 t',
 hzTz:'Eskort 1: Hemzemin geçit, tren geliyor, bariyerler iniyor. Dur çizgisinde bekle.',t_hzKapi:'Hemzemin geçit! Bariyer iniyor, dur çizgisinde bekle.',t_hzCeza:'Kapalı bariyerden geçtin! Hemzemin geçit cezası.',t_hzKaza:'Trene çok yakın geçtin! Yük sarsıldı.',t_hzAcik:'Bariyer kalktı, geçebilirsin.',k_hemzemin:'Hemzemin geçit cezası',
 manRing:'MANEVRA',a_man:'GERİ MANEVRA (ESKORT YÖNLENDİRİR)',t_manDur:'Manevra alanı: sahaya önce geri geri girilir. Mavi halkada dur.',manTz1:'Eskort 2: Geri gel… geri… direksiyon sola, yavaş.',manTz2:'Eskort 2: Dorse ucu temiz, gelmeye devam… dur!',t_manOk:'Manevra tamam, sahaya düz devam.',
 mtH:'MONTAJ',mtTxt:'Vinç segmenti kaldırıyor. GAZ\'a basılı tut, rüzgâr 12 m/s üstüne çıkarsa bırak.',mtRuz:'Rüzgâr {w} m/s',mtOk:'Montaj tamam: {p}',mtDur:'Rüzgâr sert! Kaldırma durdu, bekle.',mtAtla:'OPERATÖRE BIRAK',pKule:'kule {k}/4',pNasel:'nasel yerinde',pKanat:'kanat {k}/3',pTur:'türbin tamamlandı, rotor dönüyor!',k_montaj:'Montaj primi',mtH2:'VİNÇLE İNDİRME',mtTxtI:'Vinç yükü dorseden alıp istif sahasına indiriyor. GAZ\'a basılı tut, rüzgâr 12 m/s üstüne çıkarsa bırak.',mtTxtA:'Vinç ankraj kafesini temel çukuruna indiriyor. GAZ\'a basılı tut, rüzgâr 12 m/s üstüne çıkarsa bırak.',mtTxtH:'Vinç göbeği nasele kaldırıyor. GAZ\'a basılı tut, rüzgâr 12 m/s üstüne çıkarsa bırak.',mtOkI:'İndirme tamam: {p}',pIndir:'yük istif sahasında',pAnk:'ankraj kafesi temelde',pHub:'göbek nasele takıldı',k_indirme:'Vinçle indirme primi'};
const ENs={
 dsKart:'ROUTE DUMMY RUN',dsTxt:'{r}: drive the route with an empty, fully extended trailer and mark obstacles as you see them. The investor pays; every marked obstacle earns a bonus. Afterwards the route survey is complete.',dsBtn:'START DUMMY RUN',dsTamam:'{r}: dummy run done ✓',
 dsBaslik:'Dummy run',dsIpucu:'Dummy run: no load, trailer fully extended. Press MARK when you see an obstacle.',a_isaret:'MARK: {e}',t_isaret:'Marked: {e}',t_kacti:'Missed: {e}',k_dsPrim:'Dummy run bonus ({n} obstacles)',
 cerH:'BLADE TIP FRAME',cerStd:'Standard',cerAlc:'Low',cerTxt:'The low frame drops the blade about 45 cm: it clears low cables and lines, but max 40 km/h and an adaptation fee.',k_cerceve:'Low tip frame adaptation',
 kl80:'Blade: 80 m class · 28.5 t · 4.5 m wide',kl72:'Blade: 72 m class · 24 t',
 hzTz:'Escort 1: Level crossing, train coming, barriers going down. Wait at the stop line.',t_hzKapi:'Level crossing! Barriers coming down, wait at the stop line.',t_hzCeza:'You crossed with the barriers down! Level crossing fine.',t_hzKaza:'Far too close to the train! The load was shaken.',t_hzAcik:'Barriers up, you can cross.',k_hemzemin:'Level crossing fine',
 manRing:'MANOEUVRE',a_man:'REVERSE IN (ESCORT GUIDES)',t_manDur:'Manoeuvring area: the site is entered in reverse. Stop in the blue ring.',manTz1:'Escort 2: Back… back… steer left, slowly.',manTz2:'Escort 2: Trailer tip is clear, keep coming… stop!',t_manOk:'Manoeuvre done, carry on straight to the site.',
 mtH:'ASSEMBLY',mtTxt:'The crane is lifting the section. Hold GAS, let go if the wind goes above 12 m/s.',mtRuz:'Wind {w} m/s',mtOk:'Assembly done: {p}',mtDur:'Gusts too strong! Lift stopped, wait.',mtAtla:'LEAVE IT TO THE OPERATOR',pKule:'tower {k}/4',pNasel:'nacelle in place',pKanat:'blade {k}/3',pTur:'turbine complete, the rotor is turning!',k_montaj:'Assembly bonus',mtH2:'CRANE OFFLOAD',mtTxtI:'The crane is lifting the load off the trailer onto the laydown area. Hold GAS, let go if the wind goes above 12 m/s.',mtTxtA:'The crane is lowering the anchor cage into the foundation pit. Hold GAS, let go if the wind goes above 12 m/s.',mtTxtH:'The crane is lifting the hub onto the nacelle. Hold GAS, let go if the wind goes above 12 m/s.',mtOkI:'Offload done: {p}',pIndir:'load on the laydown area',pAnk:'anchor cage in the foundation',pHub:'hub fitted to the nacelle',k_indirme:'Crane offload bonus'};
Object.assign(STR.tr,TRs);Object.assign(STR.en,ENs);
HELP.tr.unshift(['Deneme sürüşü, hemzemin geçit, manevra ve montaj','Yeni bir bölgede menüden deneme sürüşü yap: boş, tam boy uzatılmış dorseyle git, engelleri İŞARETLE; etüt raporu eksiksiz çıkar ve prim alırsın. Bazı kanat seferleri 80 m sınıfıdır. Alçak uç çerçevesi kanadı indirir, alçak kabloların altından geçersin ama en çok 40 km/sa. Hemzemin geçitte bariyer inerse dur çizgisinde bekle. Dağ sahalarında son kısma eskort yönlendirmesiyle geri geri girilir. Kule, nasel ve kanat teslim edince vinçle montajı sen yönetirsin; türbin parça parça yükselir.']);
HELP.en.unshift(['Dummy run, level crossing, manoeuvre and assembly','In a new region do a dummy run from the menu: drive with an empty, fully extended trailer and MARK obstacles; the survey becomes complete and you earn a bonus. Some blade jobs are 80 m class. A low tip frame lowers the blade so you pass under low cables, but max 40 km/h. At a level crossing wait at the stop line when the barriers come down. On mountain sites the last stretch is entered in reverse with an escort guiding. After delivering tower, nacelle or blade you run the crane assembly; the turbine rises piece by piece.']);

const HZ_ESIK=28;const RAIL=['marmara','ege','sivas','trakya','hatay','kapadokya'];
const MAN=['ege','karadeniz','kapadokya'];
const DSN=200000;
let HZ=null,MR=null,MT=null;

// ---------- seferler ----------
const _sf=sefer;sefer=function(n){if(n>=DSN&&n<DSN+50){const reg=REG_KEYS[n-DSN];let b=4;for(let k=4;k<900;k++){const j=_sf(k);if(j.reg===reg&&j.type==='kanat'){b=k;break}}const j=Object.assign({},_sf(b));j.n=n;j.dummy=true;j.reg=reg;j.night=false;j.tod='ogle';j.refakat=null;j.rain=false;j.mud=false;j.kl80=false;j.fee=Math.round(j.fee*.4/50)*50;return j}
 const j=_sf(n);if(j&&j.type==='kanat'&&n>12&&n%3===0&&!j.proje){j.kl80=true;j.fee=Math.round(j.fee*1.12/50)*50}return j};

function bladeMesh(){try{return CARGO.kanat.children[0].children[0]}catch(e){return null}}
const _rs=resetGame;resetGame=function(m,n){const dummy=m==='career'&&n>=DSN&&n<DSN+50;const ix=IMPORT.indexOf('kanat');if(dummy&&ix>=0)IMPORT.splice(ix,1);
 try{_rs(m,n)}finally{if(dummy&&ix>=0)IMPORT.splice(ix,0,'kanat')}
 if(!G)return;const j=G.job;G.alcak=false;G.dsIs=new Set();G.dsKac=new Set();G.manOk=false;G.mont=null;
 if(CARGO.kanat){CARGO.kanat.position.y=3.75;CARGO.kanat.children.forEach(c=>{if(c.userData._dsv!==undefined){c.visible=c.userData._dsv;delete c.userData._dsv}})}
 const bm=bladeMesh();if(bm)bm.scale.y=j.kl80?80/72:1;TON.kanat=j.kl80?28.5:24;
 const ix2=BLZ.indexOf(76);if(j.kl80&&ix2<0)BLZ.push(76);if(!j.kl80&&ix2>=0)BLZ.splice(ix2,1);
 if(j.dummy&&CARGO.kanat){CARGO.kanat.visible=true;CARGO.kanat.children.forEach(c=>{c.userData._dsv=c.visible;c.visible=false});setTimeout(()=>toast(T('dsIpucu'),'#bfe4ff',4.5),1200)}
 if(HZ){HZ.st='acik';HZ.tetik=false;HZ.ceza=false;HZ.kaza=false;HZ.s=-999;HZ.train.visible=false;HZ.kolA=HZ.kol0;HZ.isik.forEach(l=>l.material.color.setHex(0x3a0c0c))}
 if(MR){MR.ring.visible=false}};

// ---------- menü: deneme sürüşü kartı ----------
function dsBasla(reg){const n=DSN+REG_KEYS.indexOf(reg);if(needFull(nextSefer())&&!SAVE.full){openFull(nextSefer());return}startGame('career',n)}
window.dsBasla=dsBasla;
const _rm=renderMenu;renderMenu=function(){_rm();try{if(SAVE.tab!=='career')return;const b=$('mBody');if(!b)return;const n=nextSefer();const reg=sefer(n).reg;SAVE.ds=SAVE.ds||{};
 const ad=REGIONS[reg]&&REGIONS[reg].name?REGIONS[reg].name[L]||REGIONS[reg].name.tr:reg;const d=document.createElement('div');d.className='card';d.style.cssText='margin-top:10px;text-align:left';
 if(SAVE.ds[reg]){d.innerHTML=`<div class="small" style="color:#8ff0a4">${T('dsTamam').replace('{r}',ad)}</div>`}
 else{d.innerHTML=`<div style="font-weight:800;letter-spacing:.04em">${T('dsKart')}</div><div class="small" style="margin:4px 0 8px;opacity:.85">${T('dsTxt').replace('{r}',ad)}</div><button class="btn" id="dsB" style="width:100%">${T('dsBtn')}</button>`}
 b.appendChild(d);const bt=document.getElementById('dsB');if(bt)bt.onclick=()=>dsBasla(reg)}catch(e){console.log('ds menu',e)}};

// ---------- evrak: uç çerçevesi ve kanat sınıfı ----------
addEventListener('load',()=>{
 const _od=openDocs;openDocs=function(){_od();try{if(typeof mode==='undefined'||mode!=='career'||!G||G.job.type!=='kanat'||G.job.dummy||G.freeDocs)return;const box=document.createElement('div');box.id='cerB';
  box.style.cssText='text-align:left;margin:10px 0 4px;padding:8px;border:1px solid rgba(255,255,255,.14);border-radius:8px;background:rgba(0,0,0,.18)';
  const on=!!G.cerSec;box.innerHTML=`<div class="small" style="margin-bottom:6px;font-weight:700">${T(G.job.kl80?'kl80':'kl72')}</div><div style="font-weight:800;letter-spacing:.04em;margin-bottom:4px">${T('cerH')}</div><div class="small" style="margin-bottom:6px;opacity:.85">${T('cerTxt')}</div><div style="display:flex;gap:6px"><button class="btn sm${on?'':' gold'}" data-c="0" style="flex:1">${T('cerStd')}</button><button class="btn sm${on?' gold':''}" data-c="1" style="flex:1">${T('cerAlc')} · −${fmt(2500)}</button></div>`;
  const e=document.getElementById('cerB');if(e)e.remove();$('docsB').appendChild(box);box.querySelectorAll('button[data-c]').forEach(b=>b.onclick=()=>{G.cerSec=b.dataset.c==='1';box.querySelectorAll('button[data-c]').forEach(x=>x.classList.toggle('gold',(x.dataset.c==='1')===G.cerSec))})}catch(e){console.log('cer',e)}
  // deneme sürüşünde etüt raporu çıkmaz
  try{if(G&&G.job&&G.job.dummy){const e=document.getElementById('etutB');if(e)e.remove()}}catch(e){}};
 const _ok=$('docsOk').onclick;$('docsOk').onclick=function(){try{if(G&&G.job&&G.job.type==='kanat'&&G.cerSec&&!G.alcak&&!G.freeDocs&&!G.job.dummy){G.alcak=true;if(CARGO.kanat)CARGO.kanat.position.y=3.3;G.ext.push(['k_cerceve',-2500])}}catch(e){}return _ok.apply(this,arguments)};

 // ---------- sürüş adımı ----------
 const _st=EXT.step;EXT.step=function(dt,run){const r=_st?_st(dt,run):undefined;if(!G||!truck)return r;try{if(HZ)hzAdim(dt,run)}catch(e){console.log('santiye hz',e)}try{if(run&&phase==='drive'){if(G.job.dummy)dsAdim();manAdim(dt)}}catch(e){console.log('santiye ds',e)}try{if(MT)mtAdim(dt)}catch(e){console.log('santiye mt',e)}return r};

 // ---------- rapor: deneme sürüşü primi ve başlık; montaj ----------
 const _sr=showReport;showReport=function(){const j=G&&G.job;
  if(j&&j.dummy){const n=G.dsIs.size;if(n)G.ext.push(['k_dsPrim',n*1500]);SAVE.ds=SAVE.ds||{};SAVE.ds[j.reg]=true}
  if(j&&!j.dummy&&j.type&&j.type!=='donus'&&!G.mont&&KULE){const ind=mode!=='career'||!montajUygun(j.type);montajBasla(j.type,()=>{_sr();sonRapor(j)},ind);return}
  _sr();sonRapor(j)};
 function sonRapor(j){try{if(j&&j.dummy){delete SAVE.done[j.n];save();const ad=REGIONS[j.reg].name[L]||REGIONS[j.reg].name.tr;$('rSefer').textContent=T('dsBaslik')+' · '+ad}}catch(e){}}
});

// ---------- deneme sürüşü: işaretleme ----------
function dsAdim(){const E=window.ETUT&&ETUT.EN();if(!E||!E.length)return;const v=truck.v,ti=roadIdx(v);let yak=null;
 for(const o of E){if(G.dsIs.has(o.id)||G.dsKac.has(o.id))continue;if(ti>o.i+3){G.dsKac.add(o.id);toast(T('t_kacti').replace('{e}',T('e_'+o.tip)),'#ffb36b',2.2);continue}if(ti>=o.i-28&&ti<=o.i+3){yak=o;break}}
 if(yak){const lb=T('a_isaret').replace('{e}',T('e_'+yak.tip));if(!(actFn&&actFn.ds&&$('act').textContent===lb)){const o=yak;const fn=()=>{G.dsIs.add(o.id);setAct(null);blip(880,1320,.12);toast(T('t_isaret').replace('{e}',T('e_'+o.tip)),ETUT.RK[ETUT.TUR[o.tip].c],2)};fn.ds=1;setAct(lb,fn)}}
 else if(actFn&&actFn.ds)setAct(null)}

// ---------- hemzemin geçit ----------
function inst(geo,mat,n){const m=new THREE.InstancedMesh(geo,mat,n);m.count=0;return m}
function hzKur(root){HZ=null;if(!RAIL.includes(REG))return;const E=(window.ETUT&&ETUT.EN())||[];let best=-1,bs=1e9;
 for(let i=Math.round(NS*.09);i<Math.round(NS*.62);i+=2){if(VZ&&i>VZ.v0-60&&i<VZ.wi+10)continue;if(CZ&&CZ.ci&&Math.abs(i-CZ.ci)<25)continue;if(E.some(o=>Math.abs(o.i-i)<16))continue;if(PORTOPS.kantar&&Math.abs(PORTOPS.kantar.ki-i)<25)continue;if(PLAN&&((PLAN.ri&&Math.abs(PLAN.ri-i)<40)||(PLAN.ki&&Math.abs(PLAN.ki-i)<30)))continue;if(PORTOPS.dz&&Math.abs(PORTOPS.dz.i-i)<30)continue;
  const a=sideAt(i-8,0).ang,b=sideAt(i+8,0).ang;let d=Math.abs(angDiff(a,b))*20;for(const off of[-60,-35,-15,15,35,60]){const q=sideAt(i,off);d+=Math.abs(getH(q.x,q.z)-RY[i])}if(d<bs){bs=d;best=i}}
 window._hzBs=bs; if(best<0||bs>HZ_ESIK)return;const ri=best,c=sideAt(ri,0),ang=c.ang;const nx=Math.cos(ang),nz=-Math.sin(ang);// yola dik doğrultu
 const g=new THREE.Group();root.add(g);const pt=(s)=>{const p=sideAt(ri,s);return p};
 const trav=inst(new THREE.BoxGeometry(2.6,.16,.26),P('#5b4632',{shininess:2}),200),ray=inst(new THREE.BoxGeometry(.09,.14,1.25),P('#8c8f93',{shininess:60}),400),bal=inst(new THREE.BoxGeometry(3.4,.3,1.25),P('#77746e',{shininess:2}),420);g.add(trav,ray,bal);
 const M=new THREE.Matrix4(),Q=new THREE.Quaternion(),S=new THREE.Vector3(1,1,1),V=new THREE.Vector3();
 for(let s=-90;s<=90;s+=1.25){const p=pt(s);const y=Math.abs(s)<5.5?getH(p.x,p.z)+.22:Math.max(RY[ri]+.2,getH(p.x,p.z)+.12);Q.setFromAxisAngle(new THREE.Vector3(0,1,0),ang);
  V.set(p.x,y,p.z);M.compose(V,Q,S);if(Math.abs(s)>=5.5){bal.setMatrixAt(bal.count++,M);trav.setMatrixAt(trav.count++,M);const gh=getH(p.x,p.z);if(gh<y-1){V.set(p.x,(y+gh)/2,p.z);M.compose(V,Q,new THREE.Vector3(1.3,(y-gh)/.3,1));bal.setMatrixAt(bal.count++,M)}}
  for(const k of[-.72,.72]){V.set(p.x+Math.sin(ang)*k,y+.12,p.z+Math.cos(ang)*k);M.compose(V,Q,S);ray.setMatrixAt(ray.count++,M)}}
 [trav,ray,bal].forEach(m=>m.instanceMatrix.needsUpdate=true);
 // levhalar, bariyer, ışıklar (iki yaklaşım)
 const kol=[],isik=[];const yuk=P('#e9e9e6');
 for(const yon of[-1,1]){const q=sideAt(ri-yon*7,yon*5.4);const t=new THREE.Group();t.position.set(q.x,getH(q.x,q.z),q.z);t.rotation.y=q.ang+(yon>0?0:Math.PI);g.add(t);
  addBox(.14,3.4,.14,MAT.steel,0,1.7,0,t);for(const r of[.62,-.62]){const x=addBox(1.5,.22,.04,yuk,0,3.1,0,t);x.rotation.z=r;const kr=addBox(1.5,.08,.045,P('#c91d1d'),0,3.1,0,t);kr.rotation.z=r}
  for(const dx of[-.35,.35]){const l=new THREE.Mesh(new THREE.CircleGeometry(.16,12),new THREE.MeshBasicMaterial({color:0x3a0c0c}));l.position.set(dx,2.45,.09);t.add(l);isik.push(l)}
  const pv=new THREE.Group();pv.position.set(0,1.05,0);t.add(pv);const arm=new THREE.Group();pv.add(arm);for(let k=0;k<7;k++)addBox(.62,.16,.12,k%2?P('#c91d1d'):yuk,-.35-k*.62,0,0,arm);arm.rotation.z=Math.PI/2*.95;kol.push(arm)
  const dl=sideAt(ri-yon*9,yon*LANE);const dur=new THREE.Mesh(new THREE.PlaneGeometry(.35,4.2),new THREE.MeshBasicMaterial({color:0xf4f4f0,polygonOffset:true,polygonOffsetFactor:-6}));dur.rotation.x=-Math.PI/2;dur.rotation.z=dl.ang+Math.PI/2;dur.position.set(dl.x,getH(dl.x,dl.z)+.25,dl.z);g.add(dur)}
 // tren: lokomotif + 4 vagon
 const tr=new THREE.Group();const kir=P('#b8322a',{shininess:40}),gri=P('#5d6266',{shininess:20}),cam=MAT.glass;
 const lok=new THREE.Group();tr.add(lok);rbox(3,3.6,17,.3,kir,0,2.6,0,lok);addBox(2.9,1,16,gri,0,.8,0,lok);addBox(2.6,.9,.05,cam,0,3.6,8.52,lok);addBox(3.05,.25,17.1,P('#f2f2ee'),0,2.2,0,lok);
 for(let k=1;k<=4;k++){const w=new THREE.Group();w.position.z=-k*15.5;tr.add(w);rbox(2.9,3,14.5,.15,k%2?P('#6a6f4e'):P('#7b5d45'),0,2.4,0,w);addBox(2.8,.8,13.5,gri,0,.7,0,w)}
 tr.visible=false;g.add(tr);window.KATI_EK.push(tr);
 HZ={skor:bs,ri,g,kol,isik,train:tr,ang,nx,nz,st:'acik',s:-999,tetik:false,kol0:Math.PI/2*.95,kolA:Math.PI/2*.95}}
function hzAdim(dt,run){const H=HZ;const v=truck.v;const tf=(typeof roadF==='function')?roadF(v):roadIdx(v);const ds=ROADLEN/(NS-1);const ileri=(H.ri-tf)*ds;// tıra göre ileride +
 if(run&&phase==='drive'&&!H.tetik&&ileri>0&&ileri<140&&Math.abs(v.speed)>1){H.tetik=true;if(mode==='career'||Math.random()<.6){H.st='kapaniyor';H.t=0;H.s=-260;toast(T('t_hzKapi'),'#ffb36b',3);if(HEAVY.includes(G.job.type)&&mode==='career')telsiz(T('hzTz'))}}
 if(H.st!=='acik'){H.t+=dt;if(run&&G&&G.deadline&&Math.abs(v.speed)<1&&ileri>0&&ileri<90)G.deadline+=dt;const f=Math.floor(H.t*2.4)%2;H.isik.forEach((l,k)=>l.material.color.setHex((k%2)===f?0xff2a1a:0x3a0c0c));if(H.t%0.84<dt)blip(1100,1100,.05)}
 const hedef=(H.st==='kapaniyor'||H.st==='kapali')?0:H.kol0;H.kolA+=clamp(hedef-H.kolA,-dt*.6,dt*.6);H.kol.forEach(a=>a.rotation.z=H.kolA);
 if(H.st==='kapaniyor'&&H.t>3.5){H.st='kapali'}
 if(H.st==='kapali'){H.train.visible=true;const s0=H.s;
  // tren katı cisimdir: önünde tır varsa içinden geçmez; acil fren yapar, çarpar ve yol açılana kadar bekler
  const koy=ss=>{const p=sideAt(H.ri,ss),q=sideAt(H.ri,ss+1);H.train.position.set(p.x,Math.max(RY[H.ri]+.45,getH(p.x,p.z)+.35),p.z);H.train.rotation.y=Math.atan2(q.x-p.x,q.z-p.z)};
  H.s+=dt*(H.fren?6:24);koy(H.s);if(aracaDegiyor(H.train)){H.s=s0;koy(s0);if(!H.fren){H.fren=true;blip(330,260,.6)}if(!H.kaza&&run){H.kaza=true;if(mode==='career')G.dmg=Math.min(100,G.dmg+20);toast(T('t_hzKaza'),'#ff5a5a',3);titre&&titre(2)}}else H.fren=false;
  if(Math.abs(H.s)<45&&H.s>-45&&H.s%6<dt*24)blip(140,120,.18);
  if(H.s>200){H.st='aciliyor';H.t2=0;H.train.visible=false}}
 if(H.st==='aciliyor'){H.t2+=dt;if(H.t2>3){H.st='acik';H.isik.forEach(l=>l.material.color.setHex(0x3a0c0c));toast(T('t_hzAcik'),'#8ff0a4',1.8)}}
 // kural: kapalıyken dur çizgisini geçme
 if(run&&phase==='drive'&&H.st!=='acik'&&!H.ceza&&ileri<6.5&&ileri>-4&&v.speed>.4){H.ceza=true;if(mode==='career'){G.fines=(G.fines||0)+5000;G.ext.push(['k_hemzemin',-5000])}toast(T('t_hzCeza'),'#ff8a7f',3);titre&&titre(2)}
}

// ---------- manevra alanı ----------
function manKur(root){MR=null;if(!MAN.includes(REG))return;const i=NS-1-64-6;const ring=stopRing(0x3d8bff,T('manRing'));ringAt(ring,i);WOBJ.push(ring);MR={i,ring}}
function manAdim(dt){if(!MR||!G||mode!=='career'||!HEAVY.includes(G.job.type)||G.job.dummy){if(MR)MR.ring.visible=false;return}const v=truck.v,ti=roadIdx(v),sp=Math.abs(v.speed);MR.ring.visible=!G.manOk;
 if(G.manOk||G.manT!==undefined&&G.manT>=0)return;
 if(ti>MR.i+2&&v.speed>0){v.speed=0;if(G.warnT<=0){toast(T('t_manDur'),'#ffb36b',3);G.warnT=3}}
 if(Math.abs(ti-MR.i)<=3&&sp<.6){if(!(actFn&&actFn.man)){const fn=()=>{setAct(null);manBasla()};fn.man=1;fn.blade=1;setAct(T('a_man'),fn)}}
 else if(actFn&&actFn.man)setAct(null)}
function manBasla(){const v=truck.v;G.manT=0;if(G.deadline)G.deadline+=10;G.manX={i0:roadIdx(v)};showCtl&&showCtl(false);telsiz(T('manTz1'));const ds=ROADLEN/(NS-1);
 const bip=setInterval(()=>{if(G.manT<0||G.manT>9)return clearInterval(bip);blip(1250,1250,.08)},700);
 const t0=performance.now();const tick=()=>{if(!G||G.manT<0)return;const k=(performance.now()-t0)/1000;G.manT=k;const geri=k<4.5?k/4.5:k<6?1:1-(k-6)/3;const fi=G.manX.i0-geri*(26/ds);
  const i0=Math.floor(fi),f=fi-i0;const a=sideAt(i0,LANE),b=sideAt(i0+1,LANE);v.x=lerp(a.x,b.x,f);v.z=lerp(a.z,b.z,f);v.speed=0;
  if(k>5&&!G.manX.t2){G.manX.t2=1;telsiz(T('manTz2'))}
  if(k<9)requestAnimationFrame(tick);else{G.manOk=true;G.manT=-1;showCtl&&showCtl(true);MR.ring.visible=false;toast(T('t_manOk'),'#8ff0a4',2.4);blip(523,784,.3);G.bonus=(G.bonus||0)+5}};requestAnimationFrame(tick)}

// ---------- montaj ve türbin ilerlemesi ----------
function mtKayit(){SAVE.mont=SAVE.mont||{};return SAVE.mont[REG]=SAVE.mont[REG]||{k:0,n:0,b:0}}
function montajUygun(t){const m=mtKayit();const hub=m.h||m.b>0;if(t==='kule')return m.k<4;if(t==='nasel')return m.k>=4&&!m.n;if(t==='hub')return m.n&&!hub;if(t==='kanat')return m.n&&hub&&m.b<3;if(t==='ankraj')return !m.a;return false}
let KULE=null;
function kuleKur(){KULE=null;ISTIF.length=0;try{const s=world.site;if(!s)return;const ap=RS[NS-40];let ax=ap.x-SITE.x,az=ap.z-SITE.z;const al=Math.hypot(ax,az);ax/=al;az/=al;const px=-az,pz=ax;
 const u=-46,w=-10;const x=SITE.x+u*ax+w*px,z=SITE.z+u*az+w*pz;const g=new THREE.Group();g.position.set(x,SITE_Y,z);scene.add(g);WOBJ.push(g);
 const seg=[];for(let k=0;k<4;k++){const r0=2.3-k*.22,r1=2.3-(k+1)*.22;const m=addCyl(r1,r0,22,24,MAT.turb,0,25+k*22+11,0,g);m.visible=false;seg.push(m);const fl=addCyl(r1+.08,r1+.08,.3,24,MAT.flange,0,25+(k+1)*22,0,g);fl.visible=false;m.userData.fl=fl}
 const top=25+4*22;const nac=new THREE.Group();nac.position.set(0,top+2,0);g.add(nac);rbox(3.9,3.9,10.4,.6,MAT.turb,0,0,1.5,nac);nac.visible=false;
 const hub=new THREE.Group();hub.position.set(0,top+2,-4.6);g.add(hub);const hb=addCyl(1.6,2.2,3.4,20,MAT.turb,0,0,0,hub);hb.rotation.x=Math.PI/2;hub.visible=false;
 const bls=[];const bg=bladeGeom(56);for(let k=0;k<3;k++){const b=new THREE.Mesh(bg,MAT.turb);b.rotation.z=k*Math.PI*2/3;b.position.z=-1;hub.add(b);b.visible=false;bls.push(b)}
 // bir sonraki türbinin temel çukuru: ankraj kafesi buraya iner, sonra beton dökülmüş temel ve ankraj civataları görünür
 const tg=new THREE.Group();{const tx=x-px*44-ax*14,tz=z-pz*44-az*14;let ym=getH(tx,tz);for(let k=0;k<12;k++){const a=k/12*Math.PI*2;ym=Math.max(ym,getH(tx+Math.cos(a)*10,tz+Math.sin(a)*10))}tg.position.set(tx,ym-.15,tz)};scene.add(tg);WOBJ.push(tg);
 const cuk=new THREE.Group();tg.add(cuk);const toprak=P('#6b5540'),beton=P('#b4b0a6'),demir=P('#5a4a3c');
 addCyl(11,11.4,4,28,toprak,0,-1.85,0,cuk);addCyl(9.6,9.6,.1,28,P('#3b2f24'),0,.2,0,cuk);for(let k=0;k<10;k++){const a=k/10*Math.PI*2;const t=rbox(3.2,1.4,2.2,.4,toprak,Math.cos(a)*12.6,.6,Math.sin(a)*12.6,cuk);t.rotation.y=-a}
 const cit=P('#e8531f');for(let k=0;k<16;k++){const a=k/16*Math.PI*2;addCyl(.05,.05,1.1,5,cit,Math.cos(a)*15,.55,Math.sin(a)*15,cuk)}
 const tem=new THREE.Group();tg.add(tem);addCyl(9.5,10.4,4.2,32,beton,0,-.9,0,tem);addCyl(3,3.2,.9,28,beton,0,1.6,0,tem);for(let k=0;k<36;k++){const a=k/36*Math.PI*2;addCyl(.05,.05,.5,4,demir,Math.cos(a)*2.55,2.3,Math.sin(a)*2.55,tem)}
 KULE={g,seg,nac,hub,bls,top,cuk,tem,tg};kuleGoster()}catch(e){console.log('kule',e)}}
function kuleGoster(){if(!KULE)return;const m=mtKayit();KULE.seg.forEach((s,k)=>{s.visible=k<m.k;s.userData.fl.visible=k<m.k});KULE.nac.visible=!!m.n;KULE.hub.visible=!!(m.n&&(m.h||m.b>0));KULE.bls.forEach((b,k)=>b.visible=k<m.b);if(KULE.cuk){KULE.cuk.visible=!m.a;KULE.tem.visible=!!m.a}}
const ISTIF=[];
function montajBasla(tip,bitti,ind){if(!KULE){bitti();return}const m=mtKayit();phase='montaj';showHud(false);showCtl&&showCtl(true);
 const parca=new THREE.Group();scene.add(parca);let hedefY,hedef=new THREE.Vector3();
 const govde=()=>{if(tip==='kule'){const c=addCyl(2.1,2.3,22,24,MAT.turb,0,0,0,parca);if(ind)c.rotation.z=Math.PI/2}else if(tip==='nasel')rbox(3.9,3.9,10.4,.6,MAT.turb,0,0,0,parca);else if(tip==='kanat'){const b=new THREE.Mesh(bladeGeom(56),MAT.turb);b.rotation.x=Math.PI/2;if(ind)b.rotation.set(0,0,Math.PI/2);parca.add(b)}
  else{const src=CARGO[{kasa:'raf',yedek:'raf'}[tip]||tip];if(src){const c=src.clone(true);c.position.set(0,0,0);c.rotation.set(0,0,0);c.traverse(o=>{o.visible=true});parca.add(c)}else rbox(2.4,2.4,6,.1,P('#8a6b3c'),0,1.2,0,parca)}};govde();
 const KP=KULE.g.position;const ax=KP.x-SITE.x,az=KP.z-SITE.z;const al=Math.hypot(ax,az)||1;
 if(ind){const n=ISTIF.length%4;hedef.set(KP.x+(-az/al)*(34+n*7)+(ax/al)*14,KP.y+1.2,KP.z+(ax/al)*(34+n*7)+(az/al)*14)}
 else if(tip==='ankraj'){const t=KULE.tg.position;hedef.set(t.x,t.y-.4,t.z)}
 else{hedefY=tip==='kule'?25+m.k*22+11:KULE.top+2;if(tip==='hub')hedef.set(KP.x,KP.y+hedefY,KP.z-4.6);else hedef.set(KP.x,KP.y+hedefY,KP.z)}const bas=new THREE.Vector3(KULE.g.position.x+18,KULE.g.position.y+3,KULE.g.position.z+10);parca.position.copy(bas);
 const hook=new THREE.Mesh(new THREE.CylinderGeometry(.05,.05,1,4),new THREE.MeshBasicMaterial({color:0x111111}));scene.add(hook);
 const ov=document.createElement('div');ov.style.cssText='position:fixed;left:50%;top:calc(env(safe-area-inset-top) + 70px);transform:translateX(-50%);z-index:40;background:rgba(12,16,14,.86);color:#fff;padding:10px 14px;border-radius:10px;text-align:center;font:600 14px "Barlow Condensed",sans-serif;max-width:88vw';document.body.appendChild(ov);
 MT={tip,ind:!!ind,p:0,parca,bas,hedef,hook,ov,ruz:7,bitti,durT:0,oto:false};const ab=document.createElement('button');ab.className='btn sm';ab.id='mtAtla';ab.textContent=T('mtAtla');ab.style.cssText='position:fixed;left:calc(env(safe-area-inset-left) + 14px);top:calc(env(safe-area-inset-top) + 14px);z-index:41';ab.onclick=()=>{if(MT){MT.oto=true;ab.remove()}};document.body.appendChild(ab);MT.ab=ab;const KCT=window.camTarget;MT.kct=KCT;
 window.camTarget=()=>{const c=MT?MT.parca.position:hedef;return{p:new THREE.Vector3(KULE.g.position.x+70,KULE.g.position.y+60,KULE.g.position.z+70),l:new THREE.Vector3((KULE.g.position.x+c.x)/2,c.y*.6+KULE.g.position.y*.4,(KULE.g.position.z+c.z)/2)}};snapCam&&snapCam()}
function mtAdim(dt){const M=MT;M.ruz=clamp(M.ruz+(Math.random()-.5)*dt*6+Math.sin(G.t*.5)*dt*1.4,4,14.5);const ruzgar=M.ruz>12;
 const bas=input.gas>0||M.oto;if(M.oto)M.p=Math.min(1,M.p+dt*.5);else if(bas&&!ruzgar)M.p=Math.min(1,M.p+dt*(M.ind||M.tip==='ankraj'?.24:.15));if(bas&&ruzgar&&!M.oto){M.durT+=dt;if(M.durT>1.2&&mode==='career'){G.dmg=Math.min(100,G.dmg+dt*4)}}else M.durT=0;
 const k=M.p;const P2=new THREE.Vector3().lerpVectors(M.bas,M.hedef,k);P2.y=(M.ind||M.tip==='ankraj')?M.bas.y+(M.hedef.y-M.bas.y)*k+Math.sin(Math.PI*k)*12:M.bas.y+(M.hedef.y-M.bas.y)*Math.min(1,k*1.25);M.parca.position.copy(P2);M.parca.rotation.y=Math.sin(G.t*.8)*(ruzgar?.12:.04);
 const ust=M.parca.position.clone();ust.y+=14;M.hook.position.copy(ust).add(M.parca.position).multiplyScalar(.5);M.hook.scale.y=14;
 M.ov.innerHTML=`<b style="letter-spacing:.06em">${T(M.ind?'mtH2':'mtH')}</b> · ${Math.round(k*100)}%<br><span style="opacity:.85">${T(M.ind?'mtTxtI':M.tip==='ankraj'?'mtTxtA':M.tip==='hub'?'mtTxtH':'mtTxt')}</span><br><b style="color:${ruzgar?'#ff8a7f':'#8ff0a4'}">${T('mtRuz').replace('{w}',M.ruz.toFixed(1))}</b>${ruzgar&&bas?'<br><b style="color:#ff8a7f">'+T('mtDur')+'</b>':''}`;
 if(k>=1){const m=mtKayit();let p='';if(M.ind)p=T('pIndir');else if(M.tip==='kule'){m.k++;p=T('pKule').replace('{k}',m.k)}else if(M.tip==='nasel'){m.n=1;p=T('pNasel')}else if(M.tip==='hub'){m.h=1;p=T('pHub')}else if(M.tip==='ankraj'){m.a=1;p=T('pAnk')}else{m.h=1;m.b++;p=m.b>=3?T('pTur'):T('pKanat').replace('{k}',m.b)}if(!M.ind)save();kuleGoster();
  if(mode==='career'&&!M.oto)G.ext.push(M.ind?['k_indirme',1000]:['k_montaj',2500]);if(M.ab)M.ab.remove();blip(392,523,.25);setTimeout(()=>blip(523,784,.3),220);toast(T(M.ind?'mtOkI':'mtOk').replace('{p}',p),'#8ff0a4',3);
  if(M.ind){WOBJ.push(M.parca);ISTIF.push(M.parca);if(ISTIF.length>4){scene.remove(ISTIF.shift())}M.parca.rotation.y=0}else scene.remove(M.parca);scene.remove(M.hook);M.ov.remove();window.camTarget=M.kct;const fn=M.bitti;MT=null;G.mont=true;setTimeout(fn,1400)}}
// türbin tamamlanınca rotor döner
const _st2=window.EXT&&EXT.step;

// ---------- bölge kurulumu ----------
const _br=buildRegion;buildRegion=function(r){_br(r);try{const root=new THREE.Group();scene.add(root);WOBJ.push(root);hzKur(root);manKur(root);kuleKur()}catch(e){console.log('santiye kur',e)}};
setInterval(()=>{try{if(KULE&&KULE.hub.visible&&mtKayit().b>=3)KULE.hub.rotation.z+=.012}catch(e){}},33);
window.SANTIYE={ISTIF:()=>ISTIF,hzSkor:()=>HZ&&HZ.skor,HZ:()=>HZ,MR:()=>MR,KULE:()=>KULE,MT:()=>MT};
})();
