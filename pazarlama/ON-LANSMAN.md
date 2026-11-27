# Kervan Yolu ön lansman (25 – 28 Kasım 2026)

Çıkış: **Cumartesi 28 Kasım 2026, 09:00 (TSİ)** (Emre, 24 Kas: 5 Aralık'tan öne alındı). App Store'da "onaydan sonra, en erken bu tarihte" ayarlı (`store/YAYIN-TARIHI`). Apple onayı 28'i sabahından sonra gelirse oyun onay anında çıkar; çıkış paylaşımı ancak oyun mağazada görünce yapılır.

Kural: her paylaşım önce LinkedIn, sonra Instagram, X ve öteki hesaplar. Görseller yalnız oyundan; gerçek saha, proje ya da işyeri bilgisi/görseli yok, işveren adı geçmez.
Görseller: `pazarlama/*-4x5.png` (akış), `*-9x16.png` (hikâye). Üretici: `araclar/merak-gorselleri.py`.

| Gün | Görsel | Metin |
|---|---|---|
| Çar 25 Kas | 1-yukleniyor | Bandırma Limanı, gece yarısı. Brandanın altında 70 metrelik bir şey bekliyor. Yola çıkmasına az kaldı. 28.11 |
| Per 26 Kas | 2-dar-sokak | 70 metrelik bir kanadı Ege'de dar bir köy sokağından geçirmenin tek yolu var: kanadı göğe kaldırmak. Evlere, tellere dikkat. 28.11 |
| Cum 27 Kas (sabah) | 3-zincir | Sivas yolunda yokuş buz tuttu. Mavi halkada dur, zinciri tak, sonra tırman. Rüzgâr sahası seni bekliyor. 28.11 |
| Cum 27 Kas (akşam) | 4-yarin | Trakya'da yan rüzgâr, ayçiçekleri ve Ganos'un eteklerinde bir rüzgâr sahası. Yarın yoldayız. |
| Cmt 28 Kas 09:00 | mağaza görselleri + bağlantı | Kervan Yolu App Store'da. Tırla limandan rüzgâr sahasına kule, kanat, nasel taşı; Ege'den Karadeniz'e, Hatay'dan Kapadokya'ya sekiz bölgede 1923 sefer. Gece konvoyu, polis refakati, kendi nakliye firman. Kabinde Mr. Anduv! FM çalıyor. İlk seferler ücretsiz. https://apps.apple.com/tr/app/id6837800818 |

Etiketler (her paylaşımda 3–5): #KervanYolu #TırOyunu #RüzgarEnerjisi #MobilOyun #MrAnduv

"Sektörden biri" cümlesi (isteğe bağlı, bir kez, çıkış gününde): "Rüzgâr türbini taşımanın ne demek olduğunu yakından bilen biri olarak bu oyunu yaptım."

## Lansman seti (27 Kasım 2026, en güncel derlemeden)
- `pazarlama/lansman/kv-01…10.png` (4:5 akış), `hikaye/kv-hikaye-01…10.png` (9:16), metinler `PAYLASIM-METINLERI-KERVAN-YOLU.md`.
- Üretim: `python3 araclar/lansman-gorselleri.py pazarlama/lansman/final2.json 4x5 <klasör>` (+ `9x16`), kartlar `araclar/lansman-kartlari.py` (zemin için `zemin.json`).
- Sahneler: Ege kanat kaldırıcı (kapak), Bandırma liman vinci, Marmara gece nasel, Sivas zincir, Karadeniz çay bahçeleri, Kapadokya peri bacaları, Hatay Belen, Trakya ayçiçeği, sefer raporu, kapanış.
- Yalnız yayındaki sürümde (1.1.1) olan şeyler gösterildi; sahada vinçle montaj (1.1.3, incelemede) bilerek konmadı.
- Ders: küçük yazılar `toLocaleUpperCase('tr-TR')` ile büyütülür (yoksa "LIMANI", "LOJISTIĞI"). Merak görsellerinde bu hata vardı, üretici düzeltildi.
