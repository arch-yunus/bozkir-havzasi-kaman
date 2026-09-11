# Bozkır Havzası Kaman Projesi Katkı ve Araştırma Kılavuzu

Bu belge, **Bozkır Havzası Kaman** açık kaynak monografi ve araştırma külliyatına katkı sunacak araştırmacılar, tarihçiler, arkeologlar, halk bilimciler ve yerel hafıza derleyicileri için akademik ve teknik standartları belirlemektedir.

---

## 1. Temel Araştırma İlkeleri

1. **Akademik Tarafsızlık ve Doğrulanabilirlik:**
   - Her iddia ve analiz birincil arşiv belgelerine (Cumhurbaşkanlığı Devlet Arşivleri Başkanlığı Osmanlı Arşivi [BOA], Şer'iyye Sicilleri, Vakıflar Genel Müdürlüğü Arşivi), hakemli kazı raporlarına (*Kazı Sonuçları Toplantısı*, *Anatolian Archaeological Studies*) veya ses/görüntü kaydı arşivlenmiş sözlü tarih mülakatlarına dayandırılmalıdır.
   - İkincil kaynaklardan yapılan alıntılarda tahrifat, anakronizm ve sübjektif yorumlardan kaçınılmalıdır.

2. **Disiplinlerarası Metodoloji:**
   - Monografi; arkeoloji, jeomorfoloji, paleobotanik, tarihsel sosyoloji, toponimi ve etnomüzikolojiyi birbirini tamamlayan katmanlar olarak ele alır. Yazılan her bölüm havzanın bütüncül bağlamını gözetmelidir.

---

## 2. Transkripsiyon ve İmla Standartları

### Osmanlı Türkçesi ve Tarihî Metinler
- Osmanlı Türkçesi arşiv belgeleri ve kitabeler Latin alfabesine aktarılırken **Türk Tarih Kurumu (TTK)** ve **TDV İslâm Ansiklopedisi** transkripsiyon elifbası kuralları esas alınır:
  - Uzun ünlüler: `â`, `î`, `û`
  - Hemze / Ayn: `’` (hemze), `‘` (ayn)
  - Özel ünsüzler: `ḫ` (hı), `ẕ` (zel), `ṣ` (sad), `ż` (dad), `ṭ` (tı), `ẓ` (zı), `ġ` (gayın), `ñ` (sağır kef / kâf-ı nûnî), `ç` (çim), `p` (pe), `g` (gef).
- Belge transkripsiyonlarının altında sadeleştirilmiş günümüz Türkçesi özeti ve vesikanın arşiv tasnif numarası (örn. `BOA, TT.d. 998, s. 142`) eksiksiz verilmelidir.

### Yerel Ağız ve Sözlü Hafıza
- Kaman ve Kırşehir yöresi derlemelerinde yerel söyleyiş hususiyetleri (damak n'si / ñ, kapalı e / é, diftonglar) korunmalı; kelimenin standart Türkçe karşılığı ve etimolojik kökeni dipnot veya parantez içinde belirtilmelidir.

---

## 3. CBS ve Açık Veri Formatları

- Konumsal veri içeren tüm maddeler (höyükler, tümülüsler, kaleler, hanlar, çeşmeler, yatırlar, ceviz plantasyonları) `05_gorsel_ve_kartografik_arsiv/haritalar/sit_alanlari.geojson` dosyasına eklenmelidir.
- **Koordinat Referans Sistemi:** WGS84 (`EPSG:4326` / Enlem-Boylam ondalık derece formatı: `[longitude, latitude]`).
- **GeoJSON Özellik Şeması:**
  ```json
  {
    "type": "Feature",
    "geometry": {
      "type": "Point",
      "coordinates": [33.7236, 39.3582]
    },
    "properties": {
      "id": "KH-01",
      "name": "Kaman-Kalehöyük",
      "category": "Arkeolojik Sit",
      "period": "Erken Tunç - Osmanlı",
      "elevation_m": 1015,
      "status": "1. Derece Arkeolojik Sit",
      "description": "JIAA tarafından 1986'dan beri kazılan stratigrafik merkez höyük."
    }
  }
  ```

---

## 4. Kaynakça ve Atıf Formatı

- Metin içi atıflarda yazar-tarih sistemi (**Chicago 17th / APA 7th**) tercih edilir:
  - Metin içi: `(Omura 2008: 45)` veya `(Sümer 1999: 112)`
  - Kaynakça listesi `BIBLIOGRAPHY.md` dosyasına alfabetik sırayla ve tam künye ile eklenmelidir.

---

## 5. Dizin Yapısı ve Dosya İsimlendirme

- Tüm dosya isimleri küçük harfle, boşluksuz ve alt çizgi (`_`) ile yazılmalıdır (Örn: `01_kalehoyuk_stratigrafi.md`).
- Markdown başlık hiyerarşisi (`#`, `##`, `###`) standart biçimde korunmalıdır.
- Kod blokları, alıntılar ve tablolar GitHub Flavored Markdown (GFM) sözdizimine uygun olmalıdır.
