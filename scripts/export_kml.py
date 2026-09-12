#!/usr/bin/env python3
"""
Bozkır Havzası Kaman - KML & Google Earth Dışa Aktarıcı
Bu script; GeoJSON ve CSV veri setlerini birleştirerek Google Earth Pro ve CBS yazılımları
için zenginleştirilmiş, 3D yükselti ve stil tanımlı KML dosyası üretir.
"""

import os
import sys
import json
import csv
import xml.sax.saxutils as saxutils

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

def generate_kml(geojson_path, csv_path, output_kml_path):
    print(f"-> Veri setleri okunuyor...")
    
    with open(geojson_path, 'r', encoding='utf-8') as f:
        geo_data = json.load(f)
        
    csv_dict = {}
    if os.path.exists(csv_path):
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                csv_dict[row['id']] = row

    features = geo_data.get('features', [])
    
    kml_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<kml xmlns="http://www.opengis.net/kml/2.2">',
        '  <Document>',
        '    <name>Bozkır Havzası Kaman - Arkeoloji ve Kültür Atlası</name>',
        '    <description><![CDATA[Kırşehir / Kaman mikro-havzası arkeolojik sitleri, tümülüsleri, tarihi köyleri ve ekolojik odak noktaları.]]></description>',
        '    <!-- Stiller -->',
        '    <Style id="arkeolojik_sit">',
        '      <IconStyle>',
        '        <color>ff0000ff</color>',
        '        <scale>1.3</scale>',
        '        <Icon><href>http://maps.google.com/mapfiles/kml/shapes/placemark_circle.png</href></Icon>',
        '      </IconStyle>',
        '    </Style>',
        '    <Style id="koy_yerlesimi">',
        '      <IconStyle>',
        '        <color>ff00aa00</color>',
        '        <scale>1.1</scale>',
        '        <Icon><href>http://maps.google.com/mapfiles/kml/shapes/ranger_station.png</href></Icon>',
        '      </IconStyle>',
        '    </Style>',
        '    <Style id="dogal_sit">',
        '      <IconStyle>',
        '        <color>ffffaa00</color>',
        '        <scale>1.2</scale>',
        '        <Icon><href>http://maps.google.com/mapfiles/kml/shapes/triangle.png</href></Icon>',
        '      </IconStyle>',
        '    </Style>',
        '    <Folder>',
        '      <name>Sit Alanları ve Odak Noktaları</name>'
    ]

    for feat in features:
        props = feat.get('properties', {})
        geom = feat.get('geometry', {})
        coords = geom.get('coordinates', [0, 0])
        lon, lat = coords[0], coords[1]
        
        name = props.get('name', 'İsimsiz')
        cat = props.get('category', 'Diğer')
        period = props.get('period', 'Belirtilmemiş')
        elev = props.get('elevation_m', 0)
        status = props.get('status', 'Bilinmiyor')
        desc = props.get('description', '')
        village = props.get('village', '')

        # Kategoriye göre stil seçimi
        style_id = "arkeolojik_sit"
        if "Doğal" in cat or "Peyzaj" in cat:
            style_id = "dogal_sit"
        elif "Köy" in cat or "Yerleşim" in cat:
            style_id = "koy_yerlesimi"

        html_desc = f"""<![CDATA[
        <div style="font-family: Arial, sans-serif; font-size: 13px; line-height: 1.5;">
          <h3 style="margin-top:0; color: #1e3a8a;">{name}</h3>
          <p><b>Kategori:</b> {cat}</p>
          <p><b>Dönem:</b> {period}</p>
          <p><b>Rakım:</b> {elev} m</p>
          <p><b>Köy/Mevkii:</b> {village}</p>
          <p><b>Statü:</b> {status}</p>
          <hr style="border: 0; border-top: 1px solid #ccc;"/>
          <p>{desc}</p>
        </div>
        ]]>"""

        kml_lines.append('      <Placemark>')
        kml_lines.append(f'        <name>{saxutils.escape(name)}</name>')
        kml_lines.append(f'        <styleUrl>#{style_id}</styleUrl>')
        kml_lines.append(f'        <description>{html_desc}</description>')
        kml_lines.append('        <Point>')
        kml_lines.append('          <altitudeMode>relativeToGround</altitudeMode>')
        kml_lines.append(f'          <coordinates>{lon},{lat},{elev}</coordinates>')
        kml_lines.append('        </Point>')
        kml_lines.append('      </Placemark>')

    kml_lines.append('    </Folder>')
    kml_lines.append('  </Document>')
    kml_lines.append('</kml>')

    os.makedirs(os.path.dirname(output_kml_path), exist_ok=True)
    with open(output_kml_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(kml_lines))

    print(f"[OK] KML dosyası başarıyla üretildi: {output_kml_path}")
    print(f"Toplam {len(features)} mekânsal nokta Google Earth uyumlu hale getirildi.")

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    geojson_path = os.path.join(base_dir, '05_gorsel_ve_kartografik_arsiv', 'haritalar', 'sit_alanlari.geojson')
    csv_path = os.path.join(base_dir, '05_gorsel_ve_kartografik_arsiv', 'haritalar', 'kaman_koyler_ve_nufus.csv')
    out_kml = os.path.join(base_dir, '05_gorsel_ve_kartografik_arsiv', 'haritalar', 'kaman_arkeoloji_atlasi.kml')
    
    generate_kml(geojson_path, csv_path, out_kml)

if __name__ == '__main__':
    main()
