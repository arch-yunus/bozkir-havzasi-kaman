#!/usr/bin/env python3
"""
Bozkır Havzası Kaman - Açık Kaynak CBS ve Sosyo-Mekânsal Veri Analiz Aracı (Gelişmiş Versiyon)
Bu script; GeoJSON ve CSV veri setlerini ayrıştırarak mekânsal istatistikler,
rakım dağılımları, mesafe matrisleri, ağırlık merkezi (centroid) ve dönem/kategori metriklerini hesaplar.
"""

import json
import csv
import math
import os
import sys

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371.0 # Dünya yarıçapı (km)
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def analyze_geojson(geojson_path):
    with open(geojson_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    features = data.get('features', [])
    print("=" * 70)
    print(f"   BOZKIR HAVZASI KAMAN - CBS & ARKEOMETRİK MEKÂNSAL ANALİZ")
    print(f"   Toplam Envanter Noktası: {len(features)}")
    print("=" * 70)
    
    categories = {}
    elevations = []
    lats, lons = [], []
    
    kalehoyuk_coords = (39.3582, 33.7236)
    
    print("\n📍 SİT ALANLARI VE REFERANS MESAFE LİSTESİ:")
    print("-" * 70)
    print(f"{'ID':<8} | {'Ad':<28} | {'Rakım':<7} | {'K.Höyük Mesafe':<14} | {'Kategori'}")
    print("-" * 70)

    for feat in features:
        props = feat.get('properties', {})
        geom = feat.get('geometry', {})
        coords = geom.get('coordinates', [0, 0])
        lon, lat = coords[0], coords[1]
        lats.append(lat)
        lons.append(lon)
        
        cat = props.get('category', 'Diğer')
        categories[cat] = categories.get(cat, 0) + 1
        
        elev = props.get('elevation_m', 0)
        if elev:
            elevations.append(elev)
            
        dist = haversine_distance(kalehoyuk_coords[0], kalehoyuk_coords[1], lat, lon)
        name = props.get('name', 'İsimsiz')
        if len(name) > 26:
            name = name[:23] + '...'
        
        print(f"{props.get('id', 'N/A'):<8} | {name:<28} | {elev:>4} m | {dist:>10.2f} km   | {cat}")
        
    print("-" * 70)

    # Coğrafi Ağırlık Merkezi (Centroid)
    centroid_lat = sum(lats) / len(lats)
    centroid_lon = sum(lons) / len(lons)

    print("\n📊 MEKÂNSAL VE JEOMORFOLOJİK İSTATİSTİKLER:")
    print(f"  • Havza Ağırlık Merkezi (Centroid): Lat={centroid_lat:.4f}°, Lon={centroid_lon:.4f}°")
    print(f"  • Kalehöyük - Centroid Uzaklığı    : {haversine_distance(kalehoyuk_coords[0], kalehoyuk_coords[1], centroid_lat, centroid_lon):.2f} km")
    
    if elevations:
        print(f"\n⛰️ RAKIM DAĞILIMI VE HİPSOMETRİK VERİLER:")
        print(f"  • Minimum Rakım : {min(elevations)} m (Kızılırmak Tabanı / Hirfanlı Koyu)")
        print(f"  • Maksimum Rakım: {max(elevations)} m (Baranlı Dağı Doruğu)")
        print(f"  • Ortalama Rakım: {sum(elevations) / len(elevations):.1f} m")
        print(f"  • Rakım Genliği : {max(elevations) - min(elevations)} m")

    print("\n🏛️ FONKSİYONEL KATEGORİ DAĞILIMI:")
    for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
        bar = "█" * (count * 2)
        print(f"  • {cat:<32}: {count:>2} adet {bar}")

def analyze_csv(csv_path):
    print("\n" + "=" * 70)
    print(f"   KAMAN YERLEŞİM, OYMAK VE TARIMSAL ÜRETİM VERİ ANALİZİ")
    print("=" * 70)
    
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        
    print(f"Kayıtlı Yerleşim Sayısı: {len(rows)}")
    
    boy_origins = {}
    products = {}
    elev_groups = {"800-999m (Vadi/Göl Tabanı)": 0, "1000-1199m (Plato/Etek)": 0, "1200m+ (Dağlık/Yayla)": 0}
    
    for r in rows:
        boy = r.get('boy_origin', 'Bilinmiyor')
        boy_origins[boy] = boy_origins.get(boy, 0) + 1
        
        prod_list = [p.strip() for p in r.get('primary_product', '').split('/')]
        for p in prod_list:
            if p:
                products[p] = products.get(p, 0) + 1
                
        try:
            elev = float(r.get('elevation_m', 0))
            if elev < 1000:
                elev_groups["800-999m (Vadi/Göl Tabanı)"] += 1
            elif elev < 1200:
                elev_groups["1000-1199m (Plato/Etek)"] += 1
            else:
                elev_groups["1200m+ (Dağlık/Yayla)"] += 1
        except ValueError:
            pass

    print("\n📜 TARİHSEL BOY / OYMAK KÖKENLERİ:")
    for b, count in sorted(boy_origins.items(), key=lambda x: x[1], reverse=True):
        print(f"  • {b:<28}: {count} yerleşim")

    print("\n🌾 BAŞLICA TARIMSAL VE EKONOMİK ÜRÜNLER:")
    for p, count in sorted(products.items(), key=lambda x: x[1], reverse=True):
        print(f"  • {p:<24}: {count} köyde temel geçim")

    print("\n📈 RAKIM KUŞAKLARI VE YERLEŞİM DAĞILIMI:")
    for group, count in elev_groups.items():
        bar = "▓" * (count * 2)
        print(f"  • {group:<30}: {count:>2} yerleşim {bar}")

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    geojson_file = os.path.join(base_dir, '05_gorsel_ve_kartografik_arsiv', 'haritalar', 'sit_alanlari.geojson')
    csv_file = os.path.join(base_dir, '05_gorsel_ve_kartografik_arsiv', 'haritalar', 'kaman_koyler_ve_nufus.csv')
    
    if os.path.exists(geojson_file):
        analyze_geojson(geojson_file)
    if os.path.exists(csv_file):
        analyze_csv(csv_file)
    print("\n" + "=" * 70 + "\n")

if __name__ == '__main__':
    main()
