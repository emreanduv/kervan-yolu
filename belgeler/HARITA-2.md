# Harita 2: büyük, gerçek, çeşitli haritalar (dal: harita-2)

Kural: mağazadaki sürüm (main, 1.1.4) olduğu gibi kalır. Bu dal bitip sekiz denetim + telefon denemesi + Emre'nin testi geçmeden main'e birleşmez.

## Bugün
- Her bölge tek yol: 700 örnek nokta, ≈1,5 km (`REGIONS[*].rp`, `buildRegion`, `RS/NS/ROADLEN`).
- Arazi gürültüyle; gerçek yükseklik yok.

## Hedef
1. **Gerçek yükseklik:** rota boyunca SRTM 90 m (OpenTopoData) profili; dağ geçidi, kıyı, yayla gerçeğe uygun. (İskenderun kıyısı 9 m → Belen 543 m doğrulandı.)
2. **Uzun rota, kesimlerle:** her sefer 8–15 km; kesim türleri: liman çıkışı, çevreyolu/kavşak, bölünmüş devlet yolu, kasaba içi (dönel kavşak, ışık), köy yolu, dağ geçidi (serpantin), saha yolu (stabilize). Her kesimin kendi şerit genişliği, hız sınırı, trafiği, etüt engelleri.
3. **Akışlı dünya:** yol ve arazi parça parça yüklenir/boşaltılır (telefon belleği); uzak görünüm basit (LOD). KATI sistemi, yol zarfı ve sekiz denetim parçalı dünyaya taşınır.
4. **Çeşitlilik:** bazı seferlerde iki rota (kısa ama dar/alçak telli ↔ uzun ama geniş) — gerçek güzergâh etüdü gibi; harita ekranı; mevsim ve hava.
5. **Yeni bölgeler** (evren kuralı: önce Türkiye'nin güzellikleri), iş verisi ya da proje konumu kullanılmadan, yalnız kamuya açık coğrafya.

## Sıra
1. Altyapı: kesimli rota + akışlı dünya, sekiz denetim parçalı dünyada (pilot: Hatay, İskenderun → Belen, gerçek profil).
2. Pilotu web önizleme olarak Emre'ye aç (mağazaya değil).
3. Emre'nin notlarından sonra öteki bölgeler.

## Durum (28 Kasım 2026, akşamüstü)
- Hatay rotası oyunda: 23 km gerçek D-817, Copernicus DEM arazisi (150 m koridor), akan 320 m karolar, parçalı ağaçlar.
- Sekiz denetim marmara + hatay geçti; önizleme: emreanduv.github.io/kervan-yolu/harita2/?bolge=hatay
- Bilinen eksikler: liman yerleşimi oyundaki gibi denizi solda varsayıyor, gerçek kıyı sağda (liman yerleşimini gerçek kıyıya göre çevir);
  İskenderun kent kesimi, Belen kasabası, kesim türleri; trafik, tesis, kamera sayısı 23 km'ye göre; mini harita; harita ekranı.

## Durum (28 Kasım 2026, öğle)
- Liman gerçek kıyıya oturdu: dünya 180° çevrildi, liman yol ile deniz arasında; limandan U dönüşlü bağlantı yolu D-817'ye bağlanır.
- Gerçek yerleşim: OSM'deki 3839 bina izinin 80 m'lik hücre özeti (sayı, taban alanı, yön) ve 11 caminin gerçek konumu. Kent kesimi (50 km/sa) kurulan binalardan hesaplanır.
- Yön levhaları gerçek uzaklıkla (Belen, geçit, RES); takograf gerçek ölçekli haritada gerçek süre sayar.
- Sıradaki: D-817 gerçekte bölünmüş yol (2×2 şerit, orta refüj) — yol kesiti bölge verisinden; alçak evlere kiremit çatı; Belen RES'in gerçek türbin konumları (OSM power=generator); diğer bölgeler.

## Durum (28 Kasım 2026, akşam)
- Çanakkale gerçek rota: Karabiga Limanı → Biga yöresi rüzgâr sahası, 16,6 km (OSRM/OSM), Copernicus DEM, OSM yerleşim ve 19 gerçek türbin. Gerçek kıyı liman yerleşimiyle aynı tarafta (bağlantı yolu yok); kasaba içi ilk 480 m atıldı. En dar viraj ≈24 m yarıçaplı gerçek firkete.
- rota.js genel: veri dosyaları `veri/{rota,dem,bina,res}-<bölge>.js`, bölge ayarı `AYAR` (yon, bas, bag, kes).
- Bölünmüş yolda aynı yönde akan trafik: sol şeritte önde uzaklaşan ve arkadan gelip sollayan araçlar; tır sol şeritteyse arkadaki araç onu izler.
- Dokuz denetim (sekiz katı cisim + rampa) Çanakkale'de geçti.
