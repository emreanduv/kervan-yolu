/* Harita 2: gerçek rota ve gerçek arazi (yalnız açık kaynak veri: OpenStreetMap + Copernicus DEM).
   Gerçek dünya (doğu e, kuzey n; metre) oyun düzlemine döndürülerek taşınır: başlangıç (0,40), ilk yön -z (oyundaki liman çıkışı),
   deniz liman yerleşimindeki gibi solda (-x) kalır. Ölçek değişmez: 1 m gerçekte 1 m oyunda.
   ROTA.yol(ad)  → {x,z,h,s,L}  40 m aralıklı gerçek noktalar (oyun koordinatı) ve ham DEM yüksekliği
   ROTA.dem(ad)  → (x,z) => gerçek arazi yüksekliği (oyun koordinatı), veri yoksa NaN
   ROTA.profil(ad, s[]) → s uzaklıklarındaki yol yüksekliği (yumuşatılmış, eğim sınırlı) */
(function(){
'use strict';
/* yon: gerçek rotanın ilk yönü (oyunda atan2(x,z)); bas: gerçek rotanın oyundaki başlangıcı; bag: limandan gerçek yola bağlantı yolu.
   Hatay: gerçek deniz yolun sağında (batıda); oyundaki liman da denizi solunda bekler. Rota +z'ye döndürülür, liman yol ile deniz arasında kalır,
   limandan çıkan yol U dönüşüyle (liman bağlantı yolu) D-817'ye bağlanır. */
const BAG_U=[[0,40],[0,-60],[0,-120],[25,-175],[80,-200],[140,-182],[172,-130],[180,-60],[180,20],[180,95]];
/* kes: baştan atılan nokta sayısı (Karabiga'da OSRM rotası ilk 480 m'de kasaba içinde dönüyor; liman yolu D-200 bağlantısından başlar) */
/* Trakya: Tekirdağ Limanı'ndan çıkan rota ilk 160 m'de kentin içinde kuzeye kıvrılıyor; sahil yolundan başlar, deniz (Marmara) liman yerleşimindeki gibi solda kalır; son 240 m saha içinde geri kıvrıldığı için atılır */
/* Ege: Aliaport'tan çıkan yol önce 800 m güneye inip geri döner; rota dönüş noktasından başlar, Aliağa körfezi solda kalır */
/* Marmara: Bandırma Limanı'ndan çıkan rota ilk 1,8 km'de liman çevresinde dolanır (atılır); Edincik yolu batıya gider, Bandırma körfezi Hatay'daki gibi sağda kalır: rota +z'ye döner, liman bağlantı yoluyla bağlanır */
const AYAR={marmara:{kes:44,yon:0,bas:[180,150],bag:BAG_U},ege:{kes:20},hatay:{yon:0,bas:[180,150],bag:BAG_U},canakkale:{kes:12},trakya:{kes:4,son:6}};
/* veri dosyaları: veri/rota-<ad>.js (ROTA_<AD>), dem-<ad>.js (DEM_<AD>), bina-<ad>.js (BINA_<AD>), res-<ad>.js (RES_<AD>) */
const KAYNAK=new Proxy({},{get:(_,ad)=>()=>{const U=String(ad).toUpperCase();return Object.assign({yol:window['ROTA_'+U],dem:window['DEM_'+U],bina:window['BINA_'+U],res:window['RES_'+U]},AYAR[ad]||{})}});
const ON=400,EGIM=0.08;const onbellek={};
function coz(ad){if(onbellek[ad])return onbellek[ad];const k=KAYNAK[ad]&&KAYNAK[ad]();if(!k||!k.yol)return null;
 const E=[],N=[],H=[];let e=0,n=0;for(const t of k.yol.split(';')){if(!t)continue;const a=t.split(',');e+=+a[0];n+=+a[1];E.push(e);N.push(n);H.push(+a[2])}
 /* kes: baştaki noktalar atılır; DEM, bina ve türbin verisi ilk başlangıca göre olduğundan kayma O ile taşınır */
 /* son: sondan atılan nokta sayısı (rota sahanın içinde geri kıvrılıyorsa saha yerleşimi yolun üstüne düşer) */
 if(k.son){E.splice(-k.son);N.splice(-k.son);H.splice(-k.son)}
 const O=[0,0];if(k.kes){const q=k.kes;E.splice(0,q);N.splice(0,q);H.splice(0,q);O[0]=E[0];O[1]=N[0];for(let i=0;i<E.length;i++){E[i]-=O[0];N[i]-=O[1]}}
 /* ilk ON metrenin yönü oyundaki -z olacak şekilde döndür */
 let j=0,s=0;while(j<E.length-1&&s<ON){s+=Math.hypot(E[j+1]-E[j],N[j+1]-N[j]);j++}
 const hx=E[j]-E[0],hz=-(N[j]-N[0]);const a0=Math.atan2(hx,hz),fi=(k.yon==null?Math.PI:k.yon)-a0;const B=k.bas||[0,40];const c=Math.cos(fi),si=Math.sin(fi);
 /* oyun tabanı: x=e, z=-n; döndürme atan2(x,z) açısına fi ekler */
 const ileri=(ee,nn)=>{const x=ee-O[0],z=-(nn-O[1]);return[x*c+z*si+B[0],-x*si+z*c+B[1]]};
 const geri=(x,z)=>{x-=B[0];z-=B[1];const bx=x*c-z*si,bz=x*si+z*c;return[bx+O[0],-bz+O[1]]};
 const X=[],Z=[],S=[];let L=0;for(let i=0;i<E.length;i++){const p=ileri(E[i]+O[0],N[i]+O[1]);X.push(p[0]);Z.push(p[1]);if(i)L+=Math.hypot(X[i]-X[i-1],Z[i]-Z[i-1]);S.push(L)}
 let demF=null;if(k.dem){const D=k.dem,nx=Math.round((D.x1-D.x0)/D.C)+1,nz=Math.round((D.z1-D.z0)/D.C)+1;const g=new Float32Array(nx*nz).fill(NaN);
  const rows=D.v.split('|');for(let r=0;r<rows.length&&r<nz;r++){const v=rows[r].split(',');for(let q=0;q<v.length&&q<nx;q++)if(v[q]!=='')g[r*nx+q]=+v[q]}
  demF=(x,z)=>{const p=geri(x,z);let fx=(p[0]-D.x0)/D.C,fz=(p[1]-D.z0)/D.C;if(fx<0||fz<0||fx>=nx-1||fz>=nz-1)return NaN;const i=fx|0,jj=fz|0;fx-=i;fz-=jj;
   const A=g[jj*nx+i],B=g[jj*nx+i+1],C=g[(jj+1)*nx+i],DD=g[(jj+1)*nx+i+1];const w=[(1-fx)*(1-fz),fx*(1-fz),(1-fx)*fz,fx*fz],v=[A,B,C,DD];let t=0,ws=0;for(let q=0;q<4;q++)if(v[q]===v[q]){t+=v[q]*w[q];ws+=w[q]}return ws>.2?t/ws:NaN}}
 return onbellek[ad]={x:X,z:Z,h:H,s:S,L,dem:demF,ileri,geri,bag:k.bag||null,bina:k.bina||null,res:k.res||null}}
function profil(ad,ss){const r=coz(ad);const n=ss.length,out=new Float32Array(n);let k=0;
 for(let i=0;i<n;i++){const s=ss[i];while(k<r.s.length-2&&r.s[k+1]<s)k++;const t=Math.min(1,Math.max(0,(s-r.s[k])/((r.s[k+1]-r.s[k])||1)));out[i]=r.h[k]+(r.h[k+1]-r.h[k])*t}
 /* DEM yol yarmasını ve köprüyü bilmez: Gauss yumuşatma (σ≈60 m), sonra gerçek devlet yolu sınırına göre eğim en çok %8 */
 const ds=n>1?(ss[n-1]-ss[0])/(n-1):1,R=Math.max(1,Math.round(150/ds)),sg=60/ds;const w=[];let ws=0;for(let q=-R;q<=R;q++){const v=Math.exp(-q*q/(2*sg*sg));w.push(v);ws+=v}
 for(let pass=0;pass<2;pass++){const t=out.slice();for(let i=0;i<n;i++){let a=0;for(let q=-R;q<=R;q++)a+=t[Math.min(n-1,Math.max(0,i+q))]*w[q+R];out[i]=a/ws}}
 const g=EGIM*ds;for(let i=1;i<n;i++)out[i]=Math.min(out[i-1]+g,Math.max(out[i-1]-g,out[i]));for(let i=n-2;i>=0;i--)out[i]=Math.min(out[i+1]+g,Math.max(out[i+1]-g,out[i]));
 return out}
window.ROTA={yol:coz,dem:ad=>{const r=coz(ad);return r&&r.dem},profil,EGIM};
})();
