/* Yeni bölgeler (gerçek liman → gerçek RES bölgesi): Çanakkale (Karabiga Limanı → Biga Tepeleri), Hatay (İskenderun Limanı → Belen Geçidi),
   Karadeniz (Trabzon Limanı → Çaykara Yaylası), Kapadokya (Mersin Limanı → Niğde-Kayseri Yaylası). Yatırımcı adları isim bozma yöntemiyle. */
(function(){
'use strict';
Object.assign(REGIONS,{
 canakkale:{name:{tr:'Çanakkale',en:'Çanakkale'},from:{tr:'Karabiga Limanı',en:'Karabiga Port'},to:{tr:'Biga Tepeleri',en:'Biga Hills'},
  rp:[[0,40],[0,-70],[34,-190],[110,-280],[150,-400],[120,-520],[170,-640],[262,-710],[330,-820],[310,-950],[360,-1070],[452,-1150],[520,-1270],[540,-1400]],
  amp:70,rid:14,climb:.04,coastW:24,sea:0x1d6c8c,fee:1.08,olive:1,cols:{g1:'#8a9a4e',g2:'#5d7036',dry:'#b9a66a',rock:'#9a8f7c'}},
 hatay:{name:{tr:'Hatay',en:'Hatay'},from:{tr:'İskenderun Limanı',en:'İskenderun Port'},to:{tr:'Belen Geçidi',en:'Belen Pass'},
  rp:[[0,40],[0,-60],[40,-160],[120,-220],[190,-300],[180,-410],[110,-500],[150,-610],[250,-660],[330,-760],[300,-880],[360,-990],[470,-1040],[540,-1160],[560,-1300]],
  amp:120,rid:24,climb:.075,coastW:26,sea:0x1b6f93,fee:1.16,citrus:1,cols:{g1:'#7f9448',g2:'#506a30',dry:'#b49c63',rock:'#8f8576'}},
 karadeniz:{name:{tr:'Karadeniz',en:'Black Sea'},from:{tr:'Trabzon Limanı',en:'Trabzon Port'},to:{tr:'Çaykara Yaylası',en:'Çaykara Plateau'},
  rp:[[0,40],[0,-70],[30,-180],[-20,-300],[40,-410],[140,-460],[200,-560],[150,-680],[200,-800],[300,-860],[360,-980],[320,-1100],[400,-1200],[500,-1260],[540,-1400]],
  amp:130,rid:22,climb:.08,coastW:20,sea:0x1d4c66,fee:1.22,snow:1,snowLine:115,tea:1,fog:1,cols:{g1:'#4f7d3a',g2:'#2f5a26',dry:'#7d8a55',rock:'#6f6d68'}},
 kapadokya:{name:{tr:'Kapadokya',en:'Cappadocia'},from:{tr:'Mersin Limanı',en:'Mersin Port'},to:{tr:'Niğde-Kayseri Yaylası',en:'Niğde-Kayseri Plateau'},
  rp:[[0,40],[0,-80],[60,-210],[170,-290],[300,-330],[400,-430],[430,-570],[380,-700],[430,-830],[540,-890],[620,-1010],[600,-1150],[660,-1280],[700,-1420]],
  amp:50,rid:10,climb:.06,coastW:18,sea:0x1f6d8a,fee:1.2,snow:1,snowLine:62,peri:1,cols:{g1:'#9a9a5c',g2:'#78794a',dry:'#c7b383',rock:'#c9b08a'}}});
REG_KEYS.push('canakkale','hatay','karadeniz','kapadokya');
Object.assign(RES,{canakkale:{tr:'Biga RES',en:'Biga Wind Farm'},hatay:{tr:'Belen RES',en:'Belen Wind Farm'},karadeniz:{tr:'Çaykara RES',en:'Çaykara Wind Farm'},kapadokya:{tr:'Niğde-Kayseri RES',en:'Niğde-Kayseri Wind Farm'}});
Object.assign(INV,{canakkale:['İçdeş Enerji','Sanka Enerji'],hatay:['Göriş Enerji','Fena Enerji'],karadeniz:['Kalyan Enerji','Ordan Enerji'],kapadokya:['Enarjisa','Esengöç Enerji']});
if(typeof REAL_KM!=='undefined')Object.assign(REAL_KM,{canakkale:35,hatay:30,karadeniz:95,kapadokya:260});
if(typeof DUZ_REG!=='undefined')Object.assign(DUZ_REG,{hatay:.6,karadeniz:.7});
// Belen geçidi meşhur rüzgârı: kanatta limanda bekleme olasılığı yüksek
const _wh=windHoldOf;windHoldOf=function(j){if(j.type==='kanat'&&j.reg==='hatay'){const h=hash2(j.n,913);return h<.4?Math.round(16+hash2(j.n,57)*5):0}return _wh(j)};

// ---------- bölgeye özgü süsler ----------
function peri(root){const tuff=P('#d8c19a',{shininess:6}),cap=P('#7a6a58',{shininess:6});for(let k=0;k<90;k++){const i=40+Math.floor(Math.random()*(NS-80));const off=(Math.random()<.5?-1:1)*(26+Math.random()*120);const p=sideAt(i,off);if(onPad&&onPad(p.x,p.z))continue;const y=getH(p.x,p.z);
  const n=1+Math.floor(Math.random()*3);for(let m=0;m<n;m++){const h=6+Math.random()*12,r=1.6+Math.random()*1.8;const dx=(Math.random()-.5)*7,dz=(Math.random()-.5)*7;const c=new THREE.Mesh(new THREE.ConeGeometry(r,h,9),tuff);c.position.set(p.x+dx,y+h/2-.5,p.z+dz);c.castShadow=true;root.add(c);
   const s=new THREE.Mesh(new THREE.ConeGeometry(r*.75,r*.9,9),cap);s.position.set(c.position.x,y+h-.2,c.position.z);root.add(s)}}
 const er=new THREE.Mesh(new THREE.ConeGeometry(520,420,24),P('#8c8a86',{shininess:2}));const sp=RS[NS-1];er.position.set(sp.x+900,-20,sp.z-1400);root.add(er);const kar=new THREE.Mesh(new THREE.ConeGeometry(190,155,24),P('#f4f6f8',{shininess:20}));kar.position.set(er.position.x,er.position.y+210-72,er.position.z);root.add(kar)}
function cay(root){const bush=P('#2f6b2c',{shininess:8});const geo=new THREE.SphereGeometry(.9,8,6);const N=900;const im=new THREE.InstancedMesh(geo,bush,N);let c=0;const M=new THREE.Matrix4(),q=new THREE.Quaternion(),s=new THREE.Vector3(1.3,.7,1.3);
 for(let i=60;i<NS*.55&&c<N;i+=7){for(const side of[-1,1]){for(let row=0;row<6&&c<N;row++){const off=side*(16+row*3.2);const p=sideAt(i,off);const y=getH(p.x,p.z);if(onPad&&onPad(p.x,p.z))continue;M.compose(new THREE.Vector3(p.x,y+.45,p.z),q,s);im.setMatrixAt(c++,M)}}}im.count=c;im.receiveShadow=true;root.add(im);
 // yayla evleri (serender biçimli ahşap)
 const ah=P('#7a5232',{shininess:10}),cat=P('#4a4f55',{shininess:20});for(let k=0;k<7;k++){const i=Math.floor(NS*.62)+k*28;const p=sideAt(i,(k%2?1:-1)*(18+k%3*5));const y=getH(p.x,p.z);const g=new THREE.Group();g.position.set(p.x,y,p.z);g.rotation.y=p.ang+k;root.add(g);
  for(const x of[-1.6,1.6])for(const z of[-1.6,1.6])addBox(.3,1.4,.3,ah,x,.7,z,g);addBox(4,2.4,4,ah,0,2.6,0,g);const r=new THREE.Mesh(new THREE.ConeGeometry(3.4,1.8,4),cat);r.rotation.y=Math.PI/4;r.position.y=4.7;g.add(r)}}
function narenciye(root){const yap=P('#2e5a24',{shininess:20}),por=new THREE.MeshStandardMaterial({color:0xf08a1a,roughness:.5});const geo=new THREE.SphereGeometry(1.5,8,7),og=new THREE.SphereGeometry(.16,6,5);const N=420;const im=new THREE.InstancedMesh(geo,yap,N),io=new THREE.InstancedMesh(og,por,N*4);let c=0,co=0;const M=new THREE.Matrix4(),q=new THREE.Quaternion(),one=new THREE.Vector3(1,1,1);
 for(let i=50;i<NS*.4&&c<N;i+=6){for(const side of[-1,1])for(let row=0;row<4&&c<N;row++){const p=sideAt(i,side*(14+row*6));const y=getH(p.x,p.z);if(onPad&&onPad(p.x,p.z))continue;M.compose(new THREE.Vector3(p.x,y+1.7,p.z),q,one);im.setMatrixAt(c++,M);for(let o=0;o<4;o++){const a=Math.random()*6.28,b=Math.random()*1.2-.2;M.compose(new THREE.Vector3(p.x+Math.cos(a)*1.4,y+1.7+b,p.z+Math.sin(a)*1.4),q,one);io.setMatrixAt(co++,M)}}}
 im.count=c;io.count=co;root.add(im);root.add(io)}
const _br=buildRegion;buildRegion=function(r){_br(r);try{const R=REGIONS[r];if(!R||!(R.peri||R.tea||R.citrus))return;const root=new THREE.Group();scene.add(root);if(typeof WOBJ!=='undefined')WOBJ.push(root);if(R.peri)peri(root);if(R.tea)cay(root);if(R.citrus)narenciye(root)}catch(e){console.log(e)}};
// Karadeniz sisi
const _sT=setTOD;setTOD=function(k){_sT(k);if(REGIONS[REG]&&REGIONS[REG].fog&&scene.fog){scene.fog.near*=.6;scene.fog.far*=.62;scene.fog.color.lerp(new THREE.Color(0xb9c4c8),.35)}};
})();
