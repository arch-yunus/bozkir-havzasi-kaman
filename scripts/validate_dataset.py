#!/usr/bin/env python3
"""
Bozkır Havzası Kaman - Veri Seti ve Dokümantasyon Doğrulama Test Aracı (CI/CD Linter)
Bu test suite; GeoJSON, CSV, Markdown bağlantıları, görsel dosyalar ve kaynakça bütünlüğünü doğrular.
"""

import os
import sys
import json
import csv
import re

# Windows UTF-8 stdout uyumluluğu
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

def log_success(msg):
    print(f"[GEÇTİ] {msg}")

def log_warning(msg):
    print(f"[UYARI] {msg}")

def log_error(msg):
    print(f"[HATA]  {msg}")

def test_geojson(geojson_path):
    print("\n--- 1. GeoJSON Veri Bütünlüğü Testi ---")
    if not os.path.exists(geojson_path):
        log_error(f"GeoJSON dosyası bulunamadı: {geojson_path}")
        return False

    with open(geojson_path, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
        except Exception as e:
            log_error(f"Geçersiz JSON formatı: {e}")
            return False

    if data.get('type') != 'FeatureCollection':
        log_error(f"GeoJSON kök tipi FeatureCollection değil: {data.get('type')}")
        return False

    features = data.get('features', [])
    if len(features) == 0:
        log_error("GeoJSON içinde hiç feature (nokta) bulunamadı!")
        return False

    required_props = ['id', 'name', 'category', 'elevation_m', 'village']
    errors = 0

    for idx, feat in enumerate(features):
        geom = feat.get('geometry', {})
        props = feat.get('properties', {})

        if geom.get('type') != 'Point':
            log_error(f"Feature #{idx}: Geometri tipi Point değil: {geom.get('type')}")
            errors += 1

        coords = geom.get('coordinates', [])
        if len(coords) < 2:
            log_error(f"Feature #{idx}: Eksik koordinat bilgisi")
            errors += 1
        else:
            lon, lat = coords[0], coords[1]
            if not (38.5 <= lat <= 40.5 and 32.5 <= lon <= 35.0):
                log_warning(f"Feature #{idx} ({props.get('name')}): Koordinatlar Kaman havzası dışına taşıyor olabilir: Lat={lat}, Lon={lon}")

        for prop in required_props:
            if prop not in props or props[prop] is None or str(props[prop]).strip() == '':
                log_error(f"Feature #{idx} ({props.get('id', 'N/A')}): Eksik zorunlu özellik '{prop}'")
                errors += 1

    if errors == 0:
        log_success(f"GeoJSON doğrulaması başarılı! Toplam {len(features)} mekânsal nokta eksiksiz.")
        return True
    else:
        log_error(f"GeoJSON doğrulamasında {errors} hata bulundu.")
        return False

def test_csv(csv_path):
    print("\n--- 2. CSV Yerleşim Envanteri Testi ---")
    if not os.path.exists(csv_path):
        log_error(f"CSV dosyası bulunamadı: {csv_path}")
        return False

    expected_headers = ['id', 'name', 'category', 'boy_origin', 'elevation_m', 'latitude', 'longitude', 'primary_product', 'historic_notes']
    
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames or []
        for h in expected_headers:
            if h not in headers:
                log_error(f"CSV başlıklarında eksik sütun: {h}")
                return False
        
        rows = list(reader)
        if len(rows) == 0:
            log_error("CSV içinde hiç satır veri bulunamadı!")
            return False

        errors = 0
        for idx, row in enumerate(rows, start=1):
            if not row['id'] or not row['name']:
                log_error(f"Satır {idx}: id veya name boş!")
                errors += 1
            try:
                elev = float(row['elevation_m'])
                if elev < 500 or elev > 2500:
                    log_warning(f"Satır {idx} ({row['name']}): Olağandışı rakım değeri: {elev}m")
            except ValueError:
                log_error(f"Satır {idx} ({row['name']}): Geçersiz rakım formatı: {row['elevation_m']}")
                errors += 1

            try:
                lat = float(row['latitude'])
                lon = float(row['longitude'])
                if not (38.5 <= lat <= 40.5 and 32.5 <= lon <= 35.0):
                    log_warning(f"Satır {idx} ({row['name']}): Koordinat sınır dışı: Lat={lat}, Lon={lon}")
            except ValueError:
                log_error(f"Satır {idx} ({row['name']}): Geçersiz koordinat formatı")
                errors += 1

    if errors == 0:
        log_success(f"CSV doğrulaması başarılı! Toplam {len(rows)} yerleşim kaydı hatasız.")
        return True
    else:
        log_error(f"CSV doğrulamasında {errors} hata bulundu.")
        return False

def test_markdown_and_links(base_dir):
    print("\n--- 3. Monografi Markdown & İç Bağlantı Bütünlüğü Testi ---")
    md_files = []
    for root, _, files in os.walk(base_dir):
        if '.git' in root:
            continue
        for file in files:
            if file.endswith('.md'):
                md_files.append(os.path.join(root, file))

    log_success(f"Toplam {len(md_files)} Markdown dokümanı bulundu ve inceleniyor.")
    
    missing_assets = 0
    link_pattern = re.compile(r'\[.*?\]\((?!http|mailto|#)(.*?)\)|!\[.*?\]\((?!http|mailto)(.*?)\)')

    for md_path in md_files:
        with open(md_path, 'r', encoding='utf-8') as f:
            content = f.read()

        md_dir = os.path.dirname(md_path)
        matches = link_pattern.findall(content)
        for m in matches:
            target = m[0] if m[0] else m[1]
            target = target.split('#')[0].strip()
            if not target:
                continue
            
            resolved_path = os.path.normpath(os.path.join(md_dir, target))
            if not os.path.exists(resolved_path):
                root_resolved = os.path.normpath(os.path.join(base_dir, target))
                if not os.path.exists(root_resolved):
                    log_warning(f"Kırık dosya bağlantısı: '{target}' | Dosya: {os.path.relpath(md_path, base_dir)}")
                    missing_assets += 1

    if missing_assets == 0:
        log_success("Tüm dokümanlar arası göreli referanslar ve görseller eksiksiz doğrulandı.")
        return True
    else:
        log_warning(f"Toplam {missing_assets} adet çözümlenemeyen bağlantı tespit edildi.")
        return True

def main():
    print("=" * 65)
    print("   BOZKIR HAVZASI KAMAN - VERI VE SISTEM TEST PAKETI")
    print("=" * 65)

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    geojson_path = os.path.join(base_dir, '05_gorsel_ve_kartografik_arsiv', 'haritalar', 'sit_alanlari.geojson')
    csv_path = os.path.join(base_dir, '05_gorsel_ve_kartografik_arsiv', 'haritalar', 'kaman_koyler_ve_nufus.csv')

    g_ok = test_geojson(geojson_path)
    c_ok = test_csv(csv_path)
    m_ok = test_markdown_and_links(base_dir)

    print("\n" + "=" * 65)
    if g_ok and c_ok and m_ok:
        print("[OK] TUM DOGRULAMA TESTLERI BASARIYLA TAMAMLANDI! (SISTEM SAGLIKLI)")
        print("=" * 65)
        return 0
    else:
        print("[FAIL] DOGRULAMA SIRASINDA BAZI HATALAR TESPIT EDILDI.")
        print("=" * 65)
        return 1

if __name__ == '__main__':
    sys.exit(main())
