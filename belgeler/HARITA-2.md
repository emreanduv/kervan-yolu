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

## Satış düzeni (Emre ile anlaşıldı, 28 Kasım 2026)
- Hatay gerçek haritası herkese ücretsiz, serbest sürüşte açık.
- Öbür gerçek haritalar Tam Sürüm'e (1,99 $) dahil; ayrı tek tek harita satışı yok.
- Haritalar çoğalınca (6–8 bölge) ayrı "Gerçek Türkiye haritaları" paketi (0,99 $) düşünülebilir; Tam Sürüm sahiplerine indirim/hediye.

## Durum (28 Kasım 2026, gece): Trakya, Marmara, Ege gerçek rotada
- **Trakya:** Tekirdağ Limanı → Ganos (Işıklar) Dağı rüzgâr sahası, ≈38 km (OSRM/OSM). Rota yüksekliği Copernicus DEM (Open-Meteo), arazi SRTM 1" (OpenTopoData; Open-Meteo günlük kotası dolduğu için). OSM'den 802 bina, 1 cami, rotaya 2,5 km içinde 4 gerçek türbin. Deniz solda (oyundaki liman düzeni gibi); kentte ilk 160 m'lik kuzey kıvrımı atıldı (`kes:4`), son 240 m saha içinde geri kıvrıldığı için atıldı (`son:6`).
- **Marmara:** Bandırma Çelebi Limanı → Bandırma batısı (Edincik yolu) rüzgâr sahası, ≈14 km. Rota ve arazi SRTM (OpenTopoData), 1527 bina, 3 cami, 31 gerçek türbin. Liman çevresindeki ilk 1,8 km dolanma atıldı (`kes:44`); körfez yolun sağında kaldığı için Hatay düzeni (rota +z, liman bağlantı yolu: `yon:0,bas,bag`).
  En yakın türbin kümesi (Bandırma'nın 6 km batısı) 7 km'lik rota veriyordu; aynı RES alanının batı ucuna (40.331 K, 27.830 D) uzatıldı.
- **Ege:** Aliaport (Aliağa) → Yuntdağı rüzgâr sahası (Aliağa-Bergama arası), ≈26 km. SRTM, 1107 bina, 4 cami, 47 gerçek türbin. Limandan çıkan yol önce 800 m güneye inip geri dönüyor; rota dönüş noktasından başlar (`kes:20`), körfez solda.
  Aliaport'un 2 km doğusunda da türbin var (Aliağa RES) ama 2 km'lik rota oyun için çok kısa; Bergama yönündeki en yakın küme seçildi.
- Genel düzeltmeler (bütün gerçek bölgeler):
  - `rota.js`: `kes` kullanılınca DEM, bina ve türbin verisi baştaki atılan kısım kadar kayıyordu (Çanakkale'de ≈360 m). Artık `ileri/geri` ilk başlangıca göre çalışır (kayma `O`). Yeni `son:N` (sondan nokta atma).
  - `dunya.js` `resKur`: sahanın 180 m çevresine (vinç çalışma alanı) gerçek türbin konmaz (Ege'de rota bir türbinin dibinde bitiyordu, indirme vinci ona değiyordu).
  - `animasyon-denetimi.py`: tır sahaya gelen yolun yönünde konur (gerçek rotalarda saha her yönden gelinir; eskiden yön hep -z sayılıyordu ve Trakya'da kanat saha ofisi konteynerine değiyordu).
- Veri kanalı notu: Open-Meteo Elevation günlük kotası ve Open-Elevation anonim aylık kotası bu gün doldu; OpenTopoData (srtm30m, 100 nokta/istek, 1 istek/sn, günde 1000 istek) kendi sekmesinden (aynı köken) çalışıyor. OSRM ve Overpass oradan da çağrılabiliyor.

## Öneri: limanı rüzgâr sahasından uzak bölgeler (uygulanmadı)
Sivas (Samsun Limanı → Sivas, ≈340 km), Karadeniz (Trabzon → Çaykara, ≈95 km), Kapadokya (Mersin → Niğde-Kayseri, ≈260 km) tek parça gerçek rota olarak oyuna sığmaz (bugünkü en uzun Trakya 38 km; karo dünyası ve denetimler bu boyda sınandı). Öneri:
1. **İki ayaklı sefer:** sefer gerçek limandan başlar, liman çıkışı + ilk 8–12 km gerçek rota (kent içi, çevreyolu); sonra "otoyol aktarması" ekranı (harita üzerinde gerçek güzergâh çizgisi, gerçek süre ve mazot hesabı, takograf molası), sonra son 15–25 km gerçek rota rüzgâr sahasına (geçit, köy yolu, saha yolu). Oynanan kısım iki ayrı gerçek rota dosyası (`rota-sivas-a.js`, `rota-sivas-b.js`), ortadaki otoyol oynanmaz ama ücret, süre ve yakıt gerçek uzaklıkla sayılır (REAL_KM zaten bu mantıkta).
2. **Seçilecek son ayaklar (yalnız açık kaynaktan doğrulanacak):** Sivas: Sivas'a yakın OSM'de işaretli bir RES kümesine son 20 km (Yıldızeli/Kangal tarafı, OSM'de türbin var mı önce Overpass ile bakılır). Karadeniz: Trabzon'dan sahile paralel değil, yaylaya çıkan dağ yolu (serpantin) gerçekte en güzel kesim; RES yoksa saha "yayla" teslim noktası olarak kalır, uydurma türbin konmaz. Kapadokya: Niğde/Kayseri yöresindeki OSM türbin kümesine son 20 km.
3. **İlk ayak:** Samsun, Trabzon, Mersin limanlarından ilk 10 km (kent içi + çevreyolu bağlantısı). Mersin ve Samsun'da limandan çıkış bölünmüş yol (cift:1).
4. Ortadaki aktarma ekranı Gelişim Defteri'ne yeni satır olarak eklenmeli (harita ekranı hedefiyle birlikte).
