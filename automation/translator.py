"""
translator.py — Çeviri Modülü
==============================
Türkçe yemek açıklamalarını İngilizceye (veya diğer dillere) çevirmek için
kullanılan modül. Gerçek API bağlantısı (Google Translate, DeepL vb.) veya
mock (sahte) çeviri modu destekler.
"""

import os


def translate_text(text, source_lang="tr", target_lang="en"):
    """
    Verilen metni kaynak dilden hedef dile çevirir.

    Parametreler:
        text (str): Çevrilecek metin
        source_lang (str): Kaynak dil kodu (varsayılan: "tr")
        target_lang (str): Hedef dil kodu (varsayılan: "en")

    Dönüş:
        str: Çevrilmiş metin
    """
    # Ortam değişkeninden mock modunun aktif olup olmadığını kontrol et
    use_mock = os.getenv("USE_MOCK_TRANSLATION", "true").lower() == "true"

    if use_mock:
        return _mock_translate(text, source_lang, target_lang)
    else:
        return _api_translate(text, source_lang, target_lang)


def _mock_translate(text, source_lang, target_lang):
    """
    Mock (sahte) çeviri fonksiyonu.
    Gerçek API olmadan çalışabilmek için metni olduğu gibi döndürür.
    Geliştirme ve test aşamasında kullanılır.

    Not: data.py dosyasında zaten İngilizce açıklamalar hazır olduğu için,
    bu fonksiyon genellikle çeviri gerekmediğinde çağrılır.
    """
    print(f"  [MOCK ÇEVİRİ] '{text[:50]}...' metni mock olarak döndürüldü.")
    return text


def _api_translate(text, source_lang, target_lang):
    """
    Gerçek çeviri API'si ile çeviri yapar.
    Google Translate API veya DeepL API kullanılabilir.

    Kullanım için .env dosyasında TRANSLATE_API_KEY tanımlanmalıdır.

    Not: Bu fonksiyon şablondur. Gerçek API entegrasyonu için
    aşağıdaki kodu aktif hale getirin ve uygun kütüphaneyi yükleyin.
    """
    api_key = os.getenv("TRANSLATE_API_KEY")

    if not api_key:
        print("  [UYARI] TRANSLATE_API_KEY bulunamadı. Mock çeviriye geçiliyor.")
        return _mock_translate(text, source_lang, target_lang)

    # =========================================================
    # Google Translate API Örneği (googletrans kütüphanesi ile)
    # =========================================================
    # from googletrans import Translator
    # translator = Translator()
    # result = translator.translate(text, src=source_lang, dest=target_lang)
    # return result.text

    # =========================================================
    # DeepL API Örneği (requests kütüphanesi ile)
    # =========================================================
    # import requests
    # url = "https://api-free.deepl.com/v2/translate"
    # params = {
    #     "auth_key": api_key,
    #     "text": text,
    #     "source_lang": source_lang.upper(),
    #     "target_lang": target_lang.upper(),
    # }
    # response = requests.post(url, data=params)
    # response.raise_for_status()
    # return response.json()["translations"][0]["text"]

    # Şimdilik mock çeviriye geri dön
    print("  [BİLGİ] API çevirisi henüz aktif değil. Mock çeviriye geçiliyor.")
    return _mock_translate(text, source_lang, target_lang)
