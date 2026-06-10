"""
main.py — Ana Otomasyon Scripti
================================
Tüm modülleri (data, translator, image_generator, strapi_client)
orkestre ederek verileri Strapi CMS'e aktarır.

Çalıştırma:
    cd automation
    python main.py

Gereksinimler:
    - .env dosyasının oluşturulmuş olması (.env.example'dan kopyalayın)
    - Strapi sunucusunun çalışıyor olması (npm run develop)
    - requirements.txt'teki paketlerin kurulu olması
"""

import os
import sys
import time

from dotenv import load_dotenv

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# .env dosyasını yükle (ortam değişkenlerini oku)
load_dotenv()

# Proje modüllerini içe aktar
from data import CITIES, CATEGORIES, FOODS
from translator import translate_text
from image_generator import generate_image
from strapi_client import StrapiClient


def print_banner():
    """Başlangıç banner'ını yazdırır."""
    banner = """
╔══════════════════════════════════════════════════════╗
║       🍽️  YZ Destekli Gastronomi Atlası              ║
║       Otomasyon Motoru v1.0                          ║
╚══════════════════════════════════════════════════════╝
    """
    print(banner)


def step_1_create_categories(client):
    """
    Adım 1: Kategori verilerini Strapi'ye ekler.

    Parametreler:
        client (StrapiClient): Strapi API istemcisi

    Dönüş:
        dict: Kategori adı → Strapi ID eşleme sözlüğü
    """
    print("\n" + "=" * 50)
    print("📂 ADIM 1: Kategoriler oluşturuluyor...")
    print("=" * 50)

    category_map = {}

    for cat in CATEGORIES:
        result = client.create_category({
            "name": cat["name"],
            "description": cat["description"],
        })
        # Kategori ID'sini haritaya ekle (yemek ilişkileri için gerekli)
        if result:
            category_map[cat["name"]] = client.entry_ref(result)

    print(f"\n  Toplam {len(category_map)} kategori işlendi.")
    return category_map


def step_2_create_cities(client):
    """
    Adım 2: Şehir verilerini Strapi'ye ekler.

    Parametreler:
        client (StrapiClient): Strapi API istemcisi

    Dönüş:
        dict: Şehir adı → Strapi ID eşleme sözlüğü
    """
    print("\n" + "=" * 50)
    print("🏙️  ADIM 2: Şehirler oluşturuluyor...")
    print("=" * 50)

    city_map = {}

    for city in CITIES:
        result = client.create_city({
            "name": city["name"],
            "country": city["country"],
            "short_description": city["short_description"],
        })
        # Şehir ID'sini haritaya ekle (yemek ilişkileri için gerekli)
        if result:
            city_map[city["name"]] = client.entry_ref(result)

    print(f"\n  Toplam {len(city_map)} şehir işlendi.")
    return city_map


def step_3_create_places(client, city_map, category_map):
    """
    Adım 3: Yemek verilerini işler ve Strapi'ye ekler.
    Her yemek için:
        1. Çeviri kontrolü yapılır
        2. Kapak görseli üretilir
        3. Görsel Strapi Media'ya yüklenir
        4. Yemek kaydı ilişkileriyle birlikte oluşturulur

    Parametreler:
        client (StrapiClient): Strapi API istemcisi
        city_map (dict): Şehir adı → ID eşleme sözlüğü
        category_map (dict): Kategori adı → ID eşleme sözlüğü
    """
    print("\n" + "=" * 50)
    print("🍲 ADIM 3: Yemekler oluşturuluyor...")
    print("=" * 50)

    total = len(FOODS)
    success_count = 0

    for i, food in enumerate(FOODS, 1):
        print(f"\n--- [{i}/{total}] {food['name']} ---")

        # 3a. Çeviri (eğer İngilizce açıklama yoksa çeviriye gönder)
        description_en = food.get("description_en")
        if not description_en:
            print("  📝 Türkçe açıklama İngilizceye çevriliyor...")
            description_en = translate_text(food["description_tr"])
        else:
            print("  📝 İngilizce açıklama zaten mevcut.")

        # 3b. Kapak görseli üret
        print("  🖼️  Kapak görseli üretiliyor...")
        image_path = generate_image(food["name"], food["description_tr"])

        # 3c. Görseli Strapi Media Library'ye yükle
        image_id = None
        if image_path:
            print("  ☁️  Görsel Strapi'ye yükleniyor...")
            uploaded = client.upload_image(image_path)
            if uploaded:
                image_id = uploaded["id"]

        # 3d. Şehir ve kategori ID'lerini bul
        city_ref = city_map.get(food["city"])
        category_ref = category_map.get(food["category"])

        if not city_ref:
            print(f"  [UYARI] '{food['city']}' şehri bulunamadı. Yemek atlanıyor.")
            continue
        if not category_ref:
            print(f"  [UYARI] '{food['category']}' kategorisi bulunamadı. Yemek atlanıyor.")
            continue

        # 3e. Yemek kaydını oluştur
        place_data = {
            "name": food["name"],
            "description_tr": food["description_tr"],
            "description_en": description_en,
            "category_name": food["category"],
            "rating": food["rating"],
            "city": city_ref,
            "category": category_ref,
        }

        # Görsel başarıyla yüklendiyse ilişkilendir
        if image_id:
            place_data["cover_image"] = image_id

        result = client.create_place(place_data)
        if result:
            success_count += 1

    print(f"\n  Toplam {success_count}/{total} yemek başarıyla işlendi.")


def main():
    """
    Ana fonksiyon — Otomasyon akışını başlatır.
    """
    print_banner()

    # Strapi istemcisini oluştur
    client = StrapiClient()

    # Bağlantı kontrolü
    print("🔗 Strapi bağlantısı kontrol ediliyor...")
    if not client.check_connection():
        print("\n[HATA] Strapi sunucusuna bağlanılamadı!")
        print("Lütfen aşağıdaki adımları kontrol edin:")
        print("  1. backend-strapi klasörüne gidin")
        print("  2. 'npm run develop' komutuyla Strapi'yi başlatın")
        print("  3. .env dosyasındaki STRAPI_URL değerini kontrol edin")
        print("  4. .env dosyasındaki STRAPI_API_TOKEN değerini kontrol edin")
        sys.exit(1)

    # Otomasyon başlangıç zamanı
    start_time = time.time()

    # Adım 1: Kategorileri oluştur
    category_map = step_1_create_categories(client)

    # Adım 2: Şehirleri oluştur
    city_map = step_2_create_cities(client)

    # Adım 3: Yemekleri oluştur (çeviri, görsel, ilişkiler dahil)
    step_3_create_places(client, city_map, category_map)

    # Tamamlanma özeti
    elapsed = time.time() - start_time
    print("\n" + "=" * 50)
    print("✅ OTOMASYON TAMAMLANDI!")
    print(f"⏱️  Toplam süre: {elapsed:.1f} saniye")
    print("=" * 50)
    print("\nStrapi admin panelinden verileri kontrol edebilirsiniz:")
    print(f"  {client.base_url}/admin")


if __name__ == "__main__":
    main()
