// Katı dünya: bölge (ve bütün modüllerin eklediği nesneler) kurulduktan sonra sahne taranır; her fiziksel nesne katı olur.
// Bu dosya en son yüklenir ki bütün buildRegion sarmalayıcılarının nesneleri ızgaraya girsin.
(function(){'use strict';
const _br=buildRegion;buildRegion=function(r){_br(r);try{const n=katiDunyaKur();window._katiN=n}catch(e){console.log('kati kur',e)}};
})();
