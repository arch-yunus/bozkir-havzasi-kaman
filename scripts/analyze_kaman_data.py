#!/usr/bin/env python3
"""
Bozkır Havzası Kaman - Açık Kaynak CBS ve Sosyo-Mekânsal Veri Analiz Aracı
Bu script; GeoJSON ve CSV veri setlerini ayrıştırarak mekânsal istatistikler,
rakım dağılımları ve dönem/kategori metriklerini hesaplar.
"""

import json
import csv
import math
import os

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
    print(f"=== GEOJSON VERİ ANALİZİ ({len(features)} Nokta) ===")
    
    categories = {}
    elevations = []
    
    kalehoyuk_coords = (39.3582, 33.7236)
    
    for feat in features:
        props = feat.get('properties', {})
        geom = feat.get('geometry', {})
        coords = geom.get('coordinates', [0, 0])
        lon, lat = coords[0], coords[1]
        
        cat = props.get('category', 'Diğer')
        categories[cat] = categories.get(cat, 0) + 1
        
        elev = props.get('elevation_m', 0)
        if elev:
            elevations.append(elev)
            
        dist = haversine_distance(kalehoyuk_coords[0], kalehoyuk_coords[1], lat, lon)
        print(f"- [{props.get('id', 'N/A')}] {props.get('name', 'İsimsiz')}: Rakım={elev}m, Kalehöyük'e Mesafe={dist:.2f} km")
        
    print("\n--- Kategori Dağılımı ---")
    for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
        print(f"  * {cat}: {count} adet")
        
    if elevations:
        print(f"\n--- Rakım İstatistikleri ---")
        print(f"  * Minimum Rakım : {min(elevations)} m (Kızılırmak Tabanı / Hirfanlı)")
        print(f"  * Maksimum Rakım: {max(elevations)} m (Baranlı Dağı Doruğu)")
        print(f"  * Ortalama Rakım: {sum(elevations) / len(elevations):.1f} m")

def analyze_csv(csv_path):
    print(f"\n=== CSV YERLEŞİM ENVENTARİ ANALİZİ ===")
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        
    print(f"Toplam Kayıtlı Köy/Yerleşim: {len(rows)}")
    boy_origins = {}
    for r in rows:
        boy = r.get('boy_origin', 'Bilinmiyor')
        boy_origins[boy] = boy_origins.get(boy, 0) + 1
        
    print("\n--- Tarihsel Boy ve Oymak Dağılımı ---")
    for b, count in sorted(boy_origins.items(), key=lambda x: x[1], reverse=True):
        print(f"  * {b}: {count} yerleşim")

if __name__ == '__main__':
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    geojson_file = os.path.join(base_dir, '05_gorsel_ve_kartografik_arsiv', 'haritalar', 'sit_alanlari.geojson')
    csv_file = os.path.join(base_dir, '05_gorsel_ve_kartografik_arsiv', 'haritalar', 'kaman_koyler_ve_nufus.csv')
    
    if os.path.exists(geojson_file):
        analyze_geojson(geojson_file)
    if os.path.exists(csv_file):
        analyze_csv(csv_file)
