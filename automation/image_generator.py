"""
image_generator.py — YZ Görsel Üretim Modülü
==============================================
Yemekler için yapay zekâ destekli kapak görseli üretimi yapar.
Gerçek API (DALL-E, Stable Diffusion) veya mock (placeholder) modunu destekler.
Mock modda, her yemek için otomatik olarak bir placeholder görsel oluşturulur.
"""

import os
from PIL import Image, ImageDraw, ImageFont


# Üretilen görsellerin kaydedileceği klasör
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "generated_images")


def generate_image(food_name, description="", output_dir=None):
    """
    Verilen yemek adı ve açıklaması için kapak görseli üretir.

    Parametreler:
        food_name (str): Yemeğin adı (görsel adı ve içeriği için kullanılır)
        description (str): Yemeğin açıklaması (API promptu için kullanılır)
        output_dir (str): Görselin kaydedileceği klasör (varsayılan: generated_images/)

    Dönüş:
        str: Üretilen görselin dosya yolu
    """
    if output_dir is None:
        output_dir = OUTPUT_DIR

    # Çıktı klasörünü oluştur (yoksa)
    os.makedirs(output_dir, exist_ok=True)

    # Ortam değişkeninden mock modunun aktif olup olmadığını kontrol et
    use_mock = os.getenv("USE_MOCK_IMAGES", "true").lower() == "true"

    if use_mock:
        return _generate_mock_image(food_name, output_dir)
    else:
        return _generate_api_image(food_name, description, output_dir)


def _generate_mock_image(food_name, output_dir):
    """
    Mock (placeholder) görsel üretir.
    Pillow kütüphanesi ile basit bir gradient arka plan üzerine
    yemek adı yazılarak bir görsel oluşturulur.

    Bu fonksiyon API anahtarı olmadan çalışabilmek için tasarlanmıştır.
    """
    # Dosya adını temizle (Türkçe karakterler ve boşluklar için)
    safe_name = _sanitize_filename(food_name)
    file_path = os.path.join(output_dir, f"{safe_name}.png")

    # 800x600 boyutunda gradient arka planlı görsel oluştur
    width, height = 800, 600
    img = Image.new("RGB", (width, height))
    draw = ImageDraw.Draw(img)

    # Gradient arka plan (turuncu-kırmızı tonları — yemek teması)
    for y in range(height):
        # Üstten alta renk geçişi
        r = int(220 - (y / height) * 80)   # 220 → 140
        g = int(120 - (y / height) * 70)   # 120 → 50
        b = int(50 + (y / height) * 30)    # 50 → 80
        draw.line([(0, y), (width, y)], fill=(r, g, b))

    # Yemek adını görsele yaz
    try:
        # Büyük font kullanmayı dene
        font = ImageFont.truetype("arial.ttf", 36)
    except (IOError, OSError):
        # Sistem fontu bulunamazsa varsayılan fontu kullan
        font = ImageFont.load_default()

    # Metin konumlandırma (ortala)
    text = food_name
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (width - text_width) // 2
    y = (height - text_height) // 2

    # Gölge efekti
    draw.text((x + 2, y + 2), text, fill=(0, 0, 0, 180), font=font)
    # Ana metin
    draw.text((x, y), text, fill=(255, 255, 255), font=font)

    # Alt bilgi yazısı
    subtitle = "🍽️ AI Gastronomi Atlası"
    try:
        small_font = ImageFont.truetype("arial.ttf", 18)
    except (IOError, OSError):
        small_font = ImageFont.load_default()

    sub_bbox = draw.textbbox((0, 0), subtitle, font=small_font)
    sub_width = sub_bbox[2] - sub_bbox[0]
    draw.text(((width - sub_width) // 2, height - 50), subtitle, fill=(255, 255, 255, 200), font=small_font)

    # Görseli kaydet
    img.save(file_path, "PNG")
    print(f"  [MOCK GÖRSEL] '{food_name}' için placeholder görsel oluşturuldu: {file_path}")
    return file_path


def _generate_api_image(food_name, description, output_dir):
    """
    Gerçek YZ API'si ile görsel üretir.
    OpenAI DALL-E veya Stable Diffusion API kullanılabilir.

    Kullanım için .env dosyasında IMAGE_API_KEY tanımlanmalıdır.

    Not: Bu fonksiyon şablondur. Gerçek API entegrasyonu için
    aşağıdaki kodu aktif hale getirin.
    """
    api_key = os.getenv("IMAGE_API_KEY")

    if not api_key:
        print("  [UYARI] IMAGE_API_KEY bulunamadı. Mock görsel üretimine geçiliyor.")
        return _generate_mock_image(food_name, output_dir)

    # =========================================================
    # OpenAI DALL-E API Örneği
    # =========================================================
    # import requests
    #
    # headers = {
    #     "Authorization": f"Bearer {api_key}",
    #     "Content-Type": "application/json",
    # }
    #
    # prompt = (
    #     f"A professional food photography of {food_name}. "
    #     f"{description}. "
    #     "Beautifully plated, warm lighting, high resolution, appetizing."
    # )
    #
    # payload = {
    #     "model": "dall-e-3",
    #     "prompt": prompt,
    #     "n": 1,
    #     "size": "1024x1024",
    # }
    #
    # response = requests.post(
    #     "https://api.openai.com/v1/images/generations",
    #     headers=headers,
    #     json=payload,
    # )
    # response.raise_for_status()
    # image_url = response.json()["data"][0]["url"]
    #
    # # Görseli indir ve kaydet
    # img_response = requests.get(image_url)
    # safe_name = _sanitize_filename(food_name)
    # file_path = os.path.join(output_dir, f"{safe_name}.png")
    # with open(file_path, "wb") as f:
    #     f.write(img_response.content)
    # return file_path

    # Şimdilik mock görsele geri dön
    print("  [BİLGİ] API görsel üretimi henüz aktif değil. Mock görsele geçiliyor.")
    return _generate_mock_image(food_name, output_dir)


def _sanitize_filename(name):
    """
    Dosya adını güvenli hale getirir.
    Türkçe karakterleri dönüştürür ve boşlukları alt çizgi ile değiştirir.
    """
    # Türkçe karakter dönüşüm tablosu
    tr_chars = {
        "ç": "c", "Ç": "C", "ğ": "g", "Ğ": "G",
        "ı": "i", "İ": "I", "ö": "o", "Ö": "O",
        "ş": "s", "Ş": "S", "ü": "u", "Ü": "U",
        "â": "a", "Â": "A",
    }
    for tr_char, en_char in tr_chars.items():
        name = name.replace(tr_char, en_char)

    # Boşlukları alt çizgi ile değiştir, özel karakterleri kaldır
    safe = "".join(c if c.isalnum() or c in ("_", "-") else "_" for c in name)
    return safe.lower()
