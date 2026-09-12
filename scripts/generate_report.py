#!/usr/bin/env python3
"""
Bozkır Havzası Kaman - Otomatik Analiz ve Sentez Raporu Üreticisi
Bu script; GeoJSON, CSV ve monografi dizinlerini analiz ederek kapsamlı bir
markdown analiz raporu (docs/kaman_analiz_raporu.md) üretir.
"""

import os
import sys
import json
import csv
import math
from datetime import datetime

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def generate_report():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    geojson_path = os.path.join(base_dir, '05_gorsel_ve_kartografik_arsiv', 'haritalar', 'sit_alanlari.geojson')
    csv_path = os.path.join(base_dir, '05_gorsel_ve_kartografik_arsiv', 'haritalar', 'kaman_koyler_ve_nufus.csv')
    out_md_path = os.path.join(base_dir, 'docs', 'kaman_analiz_raporu.md')

    with open(geojson_path, 'r', encoding='utf-8') as f:
        geo_data = json.load(f)
    
    with open(csv_path, 'r', encoding='utf-8') as f:
        csv_rows = list(csv.DictReader(f))

    features = geo_data.get('features', [])
    kalehoyuk_coords = (39.3582, 33.7236)
    
    elevations = [f['properties'].get('elevation_m', 0) for f in features if f['properties'].get('elevation_m')]
    categories = {}
    for f in features:
        c = f['properties'].get('category', 'Diğer')
        categories[c] = categories.get(c, 0) + 1

    lines = [
        "# Bozkır Havzası Kaman - Kapsamlı Mekânsal ve Sosyo-Ekonomik Analiz Raporu",
        "",
        f"> **Rapor Üretim Tarihi:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  ",
        "> **Veri Tabanı:** Kaman Açık Kaynak CBS ve Yerel Hafıza Arşivi  ",
        "> **Kapsam:** Kaman İlçe Merkezi, Çağırkan, Baranlı Silsilesi ve Kızılırmak / Hirfanlı Kıyı Şeridi",
        "",
        "---",
        "",
        "## 1. Yönetici Özeti ve Temel Bulgular",
        "",
        "Bu rapor; Orta Anadolu platosunun çekirdek alanında yer alan **Kırşehir / Kaman** mikro-havzasındaki 20 tescilli sit/mekân odağını ve 20 kırsal yerleşimi disiplinlerarası metotlarla incelemektedir.",
        "",
        f"- **Toplam Kayıtlı Sit ve Odak Sayısı:** {len(features)} adet",
        f"- **Kayıtlı Kırsal Yerleşim Sayısı:** {len(csv_rows)} adet",
        f"- **Havza Rakım Aralığı:** {min(elevations)} m (Hirfanlı Koyu) – {max(elevations)} m (Baranlı Dağı Doruğu)",
        f"- **Ortalama Havza Rakımı:** {sum(elevations)/len(elevations):.1f} m",
        f"- **Stratejik Merkez:** Kalehöyük (Lat: 39.3582°, Lon: 33.7236°, Rakım: 1015 m)",
        "",
        "---",
        "",
        "## 2. Sit Alanları ve Mekânsal Dağılım Matrisi",
        "",
        "| Kod | Alan Adı | Kategori | Dönem | Rakım | Kalehöyük Mesafe | Bağlı Yerleşim |",
        "| :--- | :--- | :--- | :--- | :--- | :--- | :--- |"
    ]

    for f in features:
        p = f['properties']
        geom = f['geometry']['coordinates']
        dist = haversine_distance(kalehoyuk_coords[0], kalehoyuk_coords[1], geom[1], geom[0])
        lines.append(f"| **{p.get('id')}** | {p.get('name')} | {p.get('category')} | {p.get('period')} | {p.get('elevation_m')} m | {dist:.2f} km | {p.get('village')} |")

    lines.extend([
        "",
        "---",
        "",
        "## 3. Kırsal İskân ve Tarımsal Ekonomi Matrisi",
        "",
        "| Köy / Yerleşim | Boy / Oymak Kökeni | Rakım | Başlıca Ürünler | Tarihsel ve Kültürel Notlar |",
        "| :--- | :--- | :--- | :--- | :--- |"
    ])

    for r in csv_rows:
        lines.append(f"| **{r['name']}** | {r['boy_origin']} | {r['elevation_m']} m | {r['primary_product']} | {r['historic_notes']} |")

    lines.extend([
        "",
        "---",
        "",
        "## 4. Analitik Değerlendirmeler",
        "",
        "### 4.1. Hipsometrik Kademelenme",
        "1. **800 - 999 m (Kızılırmak & Hirfanlı Kıyı Kuşağı):** Savcılı Büyükoba, Bağbaşı ve Hirfanlı köyleri; ılıman mikroklima, bağcılık, köftür/pekmez ve balıkçılık ile ayrışır.",
        "2. **1000 - 1199 m (Orta Plato ve Ceviz Havzası):** Kaman Merkez, Çağırkan, Kurancılı ve Demirli; Kaman cevizi, tahıl tarımı ve arkeolojik katmanlaşmanın ana omurgasını oluşturur.",
        "3. **1200 m ve Üzeri (Baranlı Dağlık Kütlesi):** Baranlı köyü ve Kargın yaylaları; küçükbaş hayvancılık, geven balı ve Demir Çağı gözetleme/tümülüs sistemlerini barındırır.",
        "",
        "### 4.2. Tarihsel Süreklilik ve Kültürel Bellek",
        "- **Erken Tunç ve Demir Çağı:** Kalehöyük, Büklükale ve Yassıhöyük üçgeni nehir geçitleri ile kervan hatlarını tahkim etmiştir.",
        "- **Selçuklu ve Osmanlı İskânı:** Danişmendli, Dulkadirli, Bozok ve Mamalu oymakları yerleşik tarım ve zaviye ağlarını tesis etmiştir.",
        "- **Millî Mücadele ve Cumhuriyet:** 24-25 Aralık 1919'da Mustafa Kemal Paşa'nın Kaman'da ağırlanması ve Kaman Müdafaa-i Hukuk Cemiyeti'nin lojistik katkıları bölgenin Cumhuriyet tarihindeki müstesna yerini pekiştirmiştir.",
        "",
        "---",
        "*(Bu rapor `scripts/generate_report.py` tarafından otomatik olarak üretilmiştir.)*"
    ])

    os.makedirs(os.path.dirname(out_md_path), exist_ok=True)
    with open(out_md_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

    print(f"[OK] Analiz ve sentez raporu oluşturuldu: {out_md_path}")

if __name__ == '__main__':
    generate_report()
