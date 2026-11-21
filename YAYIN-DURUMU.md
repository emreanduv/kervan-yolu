# Kervan Yolu — Yayın durumu (21 Kasım 2026)

Kimlik: `com.anduv.kervanyolu` (iOS + Android) · SKU `kervan-yolu` · Mağazada ücretsiz, Tam Sürüm 1,99 $ (`com.anduv.kervanyolu.tamsurum`, ilk 3 sefer açık) · Dikey + yatay
Gizlilik: https://github.com/emreanduv/kervan-yolu/blob/main/docs/GIZLILIK.md · Mağaza metinleri: `store/magaza-metinleri.md`, `store/appstore-metadata/`
Görseller: `store/screenshots/{tr,en}/{iphone69,ipad13,play}` (`python3 araclar/magaza-gorselleri.py`), `store/play-icon-512.png`

## Durum
- [x] Oyun 1.0.0: 1923 sefer, 5 sefer türü (kasa/forklift, kule segmenti, 40 m kanat, acil yedek parça, dönüş), drone ile hasar tespiti, sigorta, gece/sabah/öğle/akşam, kabin içi kamera, çarpışmalar, Serbest Sürüş ilk sekme
- [x] Standart: dil sorusu, rehber, Nasıl Oynanır, puan, paylaş, Bize yaz, Verilerimi sil, Tam Sürüm + geri yükle, ekran uyanık, Mr. Anduv! pano seti, yayın öncesi kontrol
- [x] Capacitor iOS + Android projesi, simge ve açılış ekranı
- [x] Repo: emreanduv/kervan-yolu (Emre açtı, 21 Kas 2026)
- [x] Emre: `ASC_KEY_P8` girildi (21 Kas 2026) · [ ] Android sırları Google çalışmasında · [ ] değişken `FEEDBACK_MAIL`
- [x] Bundle ID kaydı tetiklendi (`asc-bundle-id.yml`, 21 Kas 2026)
- [x] App Store Connect kaydı açıldı (id 6837800818, 21 Kas 2026)
- [x] 21 Kas 2026: iOS 1.0.0 (1) TestFlight'ta, Mr. Anduv! Testçileri grubuna bağlı, beta incelemesi bekleniyor
- [x] App Store 1.0.0: metin + görseller TR/EN, fiyat ücretsiz, Tam Sürüm IAP (Prepare for Submission), inceleme notu, derleme 1 seçili
- [x] App Privacy "Data Not Collected" yayınlandı; gizlilik URL'si GitHub'daki docs/GIZLILIK.md
- [ ] Emre: TestFlight'ta dene → onay verince "Add for Review" (Tam Sürüm IAP'yi sürüme ekleyerek) ve gönder
- [ ] (Bekletiliyor, Emre 21 Kas 2026) Google Play: sonra bütün oyunlar için toplu çalışmada yapılacak. Android anahtarı hazır (`imza-anahtari/`, Emre'ye verildi)
- [ ] Steam (Electron) ve Meta Horizon (WebXR/Quest) paketleri: Apple ve Google'dan sonra
- [x] EN ekran görüntüleri yeniden üretildi (KM/H)

## Android yükleme anahtarı — KAYBETME
`kervanyolu-upload.jks`, alias `kervanyolu`, şifre `SIFRE-OKU.txt` (git dışında, `imza-anahtari/`; Google Drive "Kervan Yolu — Yedekler" klasörüne de koy)
SHA-256: 06:D1:CD:D6:E7:08:75:1E:29:FE:20:CC:54:BD:38:3D:B3:CB:63:A9:D5:C0:A0:B7:08:57:A1:75:85:5F:75:5C
