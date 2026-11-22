/* Mr. Anduv! SES KORUYUCU (bütün oyun ve uygulamalar, Emre'nin kuralı 22 Kasım 2026)
   Sorun: uygulama arka plana gidip (başka uygulama, bildirim, kilit ekranı, arama) geri gelince
   iOS WKWebView / Android WebView ses bağlamını "suspended" ya da "interrupted" bırakıyor; ses
   ancak uygulama kapatılıp açılınca geri geliyordu.
   Çözüm: sayfadaki BÜTÜN AudioContext'ler kayda alınır; görünür olunca, odağa dönünce, Capacitor
   appStateChange'te, yerelden (AppDelegate / MainActivity) gelen çağrıda ve ilk dokunuşta yeniden
   başlatılır; iOS kilidi için sessiz bir tampon çalınır; durmuş <audio>/<video> kaldığı yerden sürer.
   Bu dosya index.html'de BÜTÜN betiklerden ÖNCE yüklenmelidir (Phaser/Howler/oyun kodu AudioContext
   kurmadan önce). Yerel taraf: AppDelegate ve MainActivity'de window.sesKurtar() çağrısı. */
(function(){
  var W=window, AC=W.AudioContext||W.webkitAudioContext;
  if(W.__sesKurtar)return; W.__sesKurtar=1;
  var list=[], media=[];
  if(AC){
    var Wrap=function(){var a=[null].concat([].slice.call(arguments));var c=new (Function.prototype.bind.apply(AC,a))();list.push(c);return c};
    Wrap.prototype=AC.prototype; try{Object.setPrototypeOf(Wrap,AC)}catch(e){}
    W.AudioContext=Wrap; if(W.webkitAudioContext)W.webkitAudioContext=Wrap;
  }
  function kick(c){try{var b=c.createBuffer(1,1,22050),s=c.createBufferSource();s.buffer=b;s.connect(c.destination);s.start(0)}catch(e){}}
  function wake(){
    if(document.hidden)return;
    list=list.filter(function(c){return c.state!=='closed'});
    list.forEach(function(c){if(c.state!=='running'){try{var p=c.resume();if(p&&p.then)p.then(function(){kick(c)},function(){})}catch(e){}}kick(c)});
    media.forEach(function(m){try{var p=m.play();if(p&&p.catch)p.catch(function(){})}catch(e){}}); media=[];
  }
  function hide(){try{media=[].slice.call(document.querySelectorAll('audio,video')).filter(function(m){return !m.paused&&!m.ended})}catch(e){media=[]}}
  function later(){wake();setTimeout(wake,150);setTimeout(wake,600)}
  document.addEventListener('visibilitychange',function(){document.hidden?hide():later()});
  W.addEventListener('pageshow',later); W.addEventListener('focus',later); W.addEventListener('pagehide',hide);
  document.addEventListener('resume',later); document.addEventListener('pause',hide);
  ['pointerdown','touchstart','touchend','mousedown','keydown'].forEach(function(e){
    W.addEventListener(e,function(){if(media.length||list.some(function(c){return c.state!=='running'&&c.state!=='closed'}))wake()},{capture:true,passive:true});
  });
  function capHook(){try{var A=W.Capacitor&&W.Capacitor.Plugins&&W.Capacitor.Plugins.App;if(A&&A.addListener){A.addListener('appStateChange',function(s){s&&s.isActive?later():hide()});return true}}catch(e){}return false}
  if(!capHook())W.addEventListener('load',capHook);
  W.sesKurtar=later; W.sesKurtarDurum=function(){return list.map(function(c){return c.state})};
})();
