"""
strapi_client.py — Strapi API İstemci Modülü
=============================================
Strapi CMS ile REST API üzerinden iletişim kuran istemci sınıfı.
Şehir, kategori ve yemek verilerini oluşturma, okuma ve
medya dosyası yükleme işlemlerini gerçekleştirir.
JWT veya API Token tabanlı kimlik doğrulama destekler.
"""

import os
import requests


class StrapiClient:
    """
    Strapi CMS REST API istemcisi.
    Tüm CRUD işlemleri ve medya yükleme bu sınıf üzerinden yapılır.
    """

    def __init__(self, base_url=None, api_token=None):
        """
        StrapiClient sınıfını başlatır.

        Parametreler:
            base_url (str): Strapi sunucu adresi (varsayılan: .env'den okunur)
            api_token (str): Strapi API Token (varsayılan: .env'den okunur)
        """
        self.base_url = (base_url or os.getenv("STRAPI_URL", "http://localhost:1337")).rstrip("/")
        self.api_token = api_token or os.getenv("STRAPI_API_TOKEN", "")

        # İstek başlıkları (API Token ile yetkilendirme)
        self.headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json",
        }

    def entry_ref(self, entry):
        """
        Strapi relation alanlarında kullanılacak güvenli referansı döndürür.

        Strapi 5 REST API belge ilişkilerinde documentId kullanır; eski Strapi
        yapılarıyla uyumluluk için documentId yoksa sayısal id'ye düşülür.
        """
        if not entry:
            return None
        return entry.get("documentId") or entry.get("id")

    # =========================================================
    # Bağlantı Kontrolü
    # =========================================================

    def check_connection(self):
        """
        Strapi sunucusuna bağlantıyı kontrol eder.

        Dönüş:
            bool: Bağlantı başarılıysa True, değilse False
        """
        try:
            response = requests.get(
                f"{self.base_url}/api/cities",
                headers=self.headers,
                params={"pagination[pageSize]": 1},
                timeout=10,
            )
            if response.status_code == 200:
                print("[✓] Strapi bağlantısı başarılı.")
                return True
            else:
                print(f"[✗] Strapi bağlantı hatası: HTTP {response.status_code}")
                return False
        except requests.exceptions.ConnectionError:
            print(f"[✗] Strapi sunucusuna bağlanılamadı: {self.base_url}")
            print("    Strapi'nin çalıştığından emin olun: npm run develop")
            return False

    # =========================================================
    # Şehir (City) İşlemleri
    # =========================================================

    def get_cities(self):
        """
        Strapi'deki tüm şehirleri getirir.

        Dönüş:
            list: Şehir kayıtlarının listesi
        """
        response = requests.get(
            f"{self.base_url}/api/cities?pagination[pageSize]=100",
            headers=self.headers,
        )
        response.raise_for_status()
        return response.json().get("data", [])

    def find_city_by_name(self, name):
        """
        İsme göre şehir arar.

        Parametreler:
            name (str): Aranacak şehir adı

        Dönüş:
            dict veya None: Bulunan şehir kaydı veya None
        """
        response = requests.get(
            f"{self.base_url}/api/cities",
            headers=self.headers,
            params={"filters[name][$eq]": name},
        )
        response.raise_for_status()
        data = response.json().get("data", [])
        return data[0] if data else None

    def create_city(self, city_data):
        """
        Yeni bir şehir kaydı oluşturur.

        Parametreler:
            city_data (dict): Şehir verileri {"name": ..., "country": ..., "short_description": ...}

        Dönüş:
            dict: Oluşturulan şehir kaydı
        """
        # Önce aynı isimde şehir var mı kontrol et
        existing = self.find_city_by_name(city_data["name"])
        if existing:
            print(f"  [ATLANDI] '{city_data['name']}' şehri zaten mevcut (ID: {existing['id']})")
            return existing

        payload = {"data": city_data}
        response = requests.post(
            f"{self.base_url}/api/cities",
            headers=self.headers,
            json=payload,
        )
        response.raise_for_status()
        result = response.json().get("data", {})
        print(f"  [✓] '{city_data['name']}' şehri oluşturuldu (ID: {result.get('id')})")
        return result

    # =========================================================
    # Mekan (Place) İşlemleri
    # =========================================================

    def get_places(self, populate=True):
        """
        Strapi'deki tüm mekanları getirir.

        Parametreler:
            populate (bool): İlişkili verileri de getir (city, category, cover_image)

        Dönüş:
            list: Mekan kayıtlarının listesi
        """
        params = {"pagination[pageSize]": 100}
        if populate:
            params["populate"] = "*"

        response = requests.get(
            f"{self.base_url}/api/places",
            headers=self.headers,
            params=params,
        )
        response.raise_for_status()
        return response.json().get("data", [])

    def find_place_by_name(self, name):
        """
        İsme göre mekan arar.

        Parametreler:
            name (str): Aranacak mekan adı

        Dönüş:
            dict veya None: Bulunan mekan kaydı veya None
        """
        response = requests.get(
            f"{self.base_url}/api/places",
            headers=self.headers,
            params={"filters[name][$eq]": name},
        )
        response.raise_for_status()
        data = response.json().get("data", [])
        return data[0] if data else None

    def create_place(self, place_data):
        """
        Yeni bir mekan kaydı oluşturur.

        Parametreler:
            place_data (dict): Mekan verileri. name, description_tr,
                description_en, rating, city, category ve cover_image alanlarını
                içerebilir.

        Dönüş:
            dict: Oluşturulan mekan kaydı
        """
        existing = self.find_place_by_name(place_data["name"])
        if existing:
            print(f"  [ATLANDI] '{place_data['name']}' mekanı zaten mevcut (ID: {existing['id']})")
            return existing

        payload = {"data": place_data}
        response = requests.post(
            f"{self.base_url}/api/places",
            headers=self.headers,
            json=payload,
        )
        response.raise_for_status()
        result = response.json().get("data", {})
        print(f"  [✓] '{place_data['name']}' mekanı oluşturuldu (ID: {result.get('id')})")
        return result

    # =========================================================
    # Kategori (Category) İşlemleri
    # =========================================================

    def get_categories(self):
        """
        Strapi'deki tüm kategorileri getirir.

        Dönüş:
            list: Kategori kayıtlarının listesi
        """
        response = requests.get(
            f"{self.base_url}/api/categories?pagination[pageSize]=100",
            headers=self.headers,
        )
        response.raise_for_status()
        return response.json().get("data", [])

    def find_category_by_name(self, name):
        """
        İsme göre kategori arar.

        Parametreler:
            name (str): Aranacak kategori adı

        Dönüş:
            dict veya None: Bulunan kategori kaydı veya None
        """
        response = requests.get(
            f"{self.base_url}/api/categories",
            headers=self.headers,
            params={"filters[name][$eq]": name},
        )
        response.raise_for_status()
        data = response.json().get("data", [])
        return data[0] if data else None

    def create_category(self, category_data):
        """
        Yeni bir kategori kaydı oluşturur.

        Parametreler:
            category_data (dict): Kategori verileri {"name": ..., "description": ...}

        Dönüş:
            dict: Oluşturulan kategori kaydı
        """
        # Önce aynı isimde kategori var mı kontrol et
        existing = self.find_category_by_name(category_data["name"])
        if existing:
            print(f"  [ATLANDI] '{category_data['name']}' kategorisi zaten mevcut (ID: {existing['id']})")
            return existing

        payload = {"data": category_data}
        response = requests.post(
            f"{self.base_url}/api/categories",
            headers=self.headers,
            json=payload,
        )
        response.raise_for_status()
        result = response.json().get("data", {})
        print(f"  [✓] '{category_data['name']}' kategorisi oluşturuldu (ID: {result.get('id')})")
        return result

    # =========================================================
    # Medya Yükleme (Upload) İşlemleri
    # =========================================================

    def upload_image(self, file_path):
        """
        Görsel dosyasını Strapi Media Library'ye yükler.

        Parametreler:
            file_path (str): Yüklenecek görsel dosyasının yolu

        Dönüş:
            dict: Yüklenen medya kaydı (id, url vb. bilgileri içerir)
        """
        if not os.path.exists(file_path):
            print(f"  [HATA] Dosya bulunamadı: {file_path}")
            return None

        # Medya yükleme için Content-Type başlığını kaldır (multipart/form-data kullanılacak)
        upload_headers = {
            "Authorization": f"Bearer {self.api_token}",
        }

        with open(file_path, "rb") as f:
            files = {"files": (os.path.basename(file_path), f, "image/png")}
            response = requests.post(
                f"{self.base_url}/api/upload",
                headers=upload_headers,
                files=files,
            )

        response.raise_for_status()
        result = response.json()

        # Strapi upload API liste olarak döndürür
        if isinstance(result, list) and len(result) > 0:
            uploaded = result[0]
            print(f"  [✓] Görsel yüklendi: {uploaded.get('name')} (ID: {uploaded.get('id')})")
            return uploaded
        else:
            print(f"  [HATA] Görsel yükleme başarısız: {result}")
            return None

    # =========================================================
    # Yemek (Food) İşlemleri
    # =========================================================

    def get_foods(self, populate=True):
        """
        Strapi'deki tüm yemekleri getirir.

        Parametreler:
            populate (bool): İlişkili verileri de getir (city, category, cover_image)

        Dönüş:
            list: Yemek kayıtlarının listesi
        """
        params = {"pagination[pageSize]": 100}
        if populate:
            params["populate"] = "*"

        response = requests.get(
            f"{self.base_url}/api/foods",
            headers=self.headers,
            params=params,
        )
        response.raise_for_status()
        return response.json().get("data", [])

    def find_food_by_name(self, name):
        """
        İsme göre yemek arar.

        Parametreler:
            name (str): Aranacak yemek adı

        Dönüş:
            dict veya None: Bulunan yemek kaydı veya None
        """
        response = requests.get(
            f"{self.base_url}/api/foods",
            headers=self.headers,
            params={"filters[name][$eq]": name},
        )
        response.raise_for_status()
        data = response.json().get("data", [])
        return data[0] if data else None

    def create_food(self, food_data):
        """
        Yeni bir yemek kaydı oluşturur.

        Parametreler:
            food_data (dict): Yemek verileri. Aşağıdaki alanları içermelidir:
                - name (str): Yemek adı
                - description_tr (str): Türkçe açıklama
                - description_en (str): İngilizce açıklama
                - ingredients (str): Malzeme listesi
                - rating (float): Puan
                - city (int): Şehir ID'si (ilişki)
                - category (int): Kategori ID'si (ilişki)
                - cover_image (int, opsiyonel): Medya ID'si (ilişki)

        Dönüş:
            dict: Oluşturulan yemek kaydı
        """
        # Önce aynı isimde yemek var mı kontrol et
        existing = self.find_food_by_name(food_data["name"])
        if existing:
            print(f"  [ATLANDI] '{food_data['name']}' yemeği zaten mevcut (ID: {existing['id']})")
            return existing

        payload = {"data": food_data}
        response = requests.post(
            f"{self.base_url}/api/foods",
            headers=self.headers,
            json=payload,
        )
        response.raise_for_status()
        result = response.json().get("data", {})
        print(f"  [✓] '{food_data['name']}' yemeği oluşturuldu (ID: {result.get('id')})")
        return result
