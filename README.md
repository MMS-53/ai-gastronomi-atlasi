# 🍽️ YZ Destekli Çok Dilli Gastronomi Atlası

> **Final teslim notu:** Proje, yönergedeki `Şehirler (Cities)` + `Mekanlar (Places)` ilişkisel yapısına uyacak şekilde güncellendi. Strapi tarafında `City`, `Place` ve `Category` koleksiyonları; Python otomasyonunda `/api/places` veri aktarımı; Streamlit tarafında şehir seçimine göre mekan listeleme akışı kullanılır. PDF raporu için hazır metin `report/final_project_report.md` dosyasındadır.

## 📌 Proje Amacı

Bu proje, kullanıcıların farklı şehirleri seçerek o şehirlere ait yöresel yemekleri görebileceği, **çok dilli ve dinamik bir gastronomi atlası** oluşturmayı amaçlamaktadır. Yemekler Türkçe ve İngilizce açıklamalara, malzeme bilgilerine, kategoriye, puana ve YZ tarafından üretilmiş kapak görseline sahiptir.

**İçerik Yönetimi Dersi — Final Projesi**

---

## 🛠️ Kullanılan Teknolojiler

| Bileşen | Teknoloji | Açıklama |
|---------|-----------|----------|
| **Backend (CMS)** | Strapi v4 | Headless CMS — İçerik yönetimi ve REST API |
| **Veritabanı** | SQLite | Strapi varsayılan veritabanı (lokal geliştirme) |
| **Otomasyon** | Python 3.10+ | Veri aktarımı, çeviri ve görsel üretimi |
| **Frontend** | Streamlit | Modern, interaktif web arayüzü |
| **Çeviri** | Mock / Google Translate API | Türkçe → İngilizce çeviri |
| **Görsel Üretimi** | Mock / OpenAI DALL-E API | Yemek kapak görseli üretimi |

---

## 📁 Klasör Yapısı

```
ai-gastronomy-atlas/
├── backend-strapi/          # Strapi CMS projesi
│   ├── src/
│   │   └── api/             # Content type tanımları
│   │       ├── city/
│   │       ├── category/
│   │       └── food/
│   ├── config/
│   ├── package.json
│   └── ...
├── automation/              # Python otomasyon motoru
│   ├── main.py              # Ana orkestrasyon scripti
│   ├── data.py              # Şehir, kategori ve yemek verileri
│   ├── translator.py        # Çeviri modülü (mock/API)
│   ├── image_generator.py   # Görsel üretim modülü (mock/API)
│   ├── strapi_client.py     # Strapi REST API istemcisi
│   ├── requirements.txt     # Python bağımlılıkları
│   └── .env.example         # Ortam değişkenleri şablonu
├── frontend-streamlit/      # Streamlit arayüzü
│   ├── app.py               # Ana uygulama dosyası
│   ├── requirements.txt     # Python bağımlılıkları
│   └── .env.example         # Ortam değişkenleri şablonu
├── report/                  # Proje raporu
│   └── screenshots/         # Ekran görüntüleri
├── .gitignore
└── README.md
```

---

## 🚀 Kurulum Adımları

### Ön Gereksinimler

- **Node.js** (v18 veya üzeri) — [nodejs.org](https://nodejs.org/)
- **Python** (v3.10 veya üzeri) — [python.org](https://www.python.org/)
- **npm** (Node.js ile birlikte gelir)
- **pip** (Python ile birlikte gelir)

---

### 1️⃣ Strapi Backend Kurulumu ve Çalıştırma

```bash
# Proje klasörüne gidin
cd backend-strapi

# Bağımlılıkları yükleyin
npm install

# Strapi'yi geliştirme modunda başlatın
npm run develop
```

Strapi ilk çalıştırmada admin panelini açacaktır:
- **URL:** http://localhost:1337/admin
- İlk açılışta admin kullanıcısı oluşturmanız istenecektir.

#### Strapi API Token Oluşturma

1. Admin paneline giriş yapın
2. **Settings → API Tokens** bölümüne gidin
3. **Create new API Token** butonuna tıklayın
4. Token ayarları:
   - **Name:** `automation-token`
   - **Token type:** `Full access`
   - **Token duration:** `Unlimited`
5. Oluşturulan token'ı kopyalayın ve `.env` dosyalarına yapıştırın

#### Content Type İzinleri

1. **Settings → Roles → Public** bölümüne gidin
2. `city`, `category` ve `food` için **find** ve **findOne** izinlerini aktif edin
3. **Upload** için de izinleri aktif edin
4. **Save** butonuna tıklayın

---

### 2️⃣ Python Otomasyon Kurulumu ve Çalıştırma

```bash
# Otomasyon klasörüne gidin
cd automation

# Sanal ortam oluşturun (önerilen)
python -m venv venv

# Sanal ortamı aktifleştirin
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Bağımlılıkları yükleyin
pip install -r requirements.txt

# .env dosyasını oluşturun
copy .env.example .env
# .env dosyasını düzenleyerek Strapi API Token'ınızı girin

# Otomasyon scriptini çalıştırın
python main.py
```

Script çalıştırıldığında sırasıyla:
1. ✅ Kategorileri Strapi'ye ekler
2. ✅ Şehirleri Strapi'ye ekler
3. ✅ Her yemek için görsel üretir (mock)
4. ✅ Görselleri Strapi Media Library'ye yükler
5. ✅ Yemek kayıtlarını ilişkileriyle birlikte oluşturur

---

### 3️⃣ Streamlit Frontend Kurulumu ve Çalıştırma

```bash
# Frontend klasörüne gidin
cd frontend-streamlit

# Sanal ortam oluşturun (önerilen)
python -m venv venv

# Sanal ortamı aktifleştirin
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Bağımlılıkları yükleyin
pip install -r requirements.txt

# .env dosyasını oluşturun
copy .env.example .env
# .env dosyasını düzenleyerek Strapi API Token'ınızı girin

# Streamlit uygulamasını başlatın
streamlit run app.py
```

Uygulama açıldığında:
- **URL:** http://localhost:8501
- Sol kenar çubuğundan şehir seçerek yöresel yemekleri görüntüleyebilirsiniz

---

## 🔑 API Token ve .env Kullanım Notları

### .env Dosyası Oluşturma

Hem `automation/` hem de `frontend-streamlit/` klasörlerinde `.env.example` dosyalarını `.env` olarak kopyalayıp düzenlemeniz gerekmektedir:

```bash
# Otomasyon için
cd automation
copy .env.example .env

# Frontend için
cd frontend-streamlit
copy .env.example .env
```

### Ortam Değişkenleri

| Değişken | Açıklama | Zorunlu |
|----------|----------|---------|
| `STRAPI_URL` | Strapi sunucu adresi | ✅ Evet |
| `STRAPI_API_TOKEN` | Strapi API erişim token'ı | ✅ Evet |
| `TRANSLATE_API_KEY` | Çeviri API anahtarı | ❌ Hayır (mock mod) |
| `IMAGE_API_KEY` | Görsel üretim API anahtarı | ❌ Hayır (mock mod) |
| `USE_MOCK_TRANSLATION` | Mock çeviri kullanımı (`true`/`false`) | ❌ Hayır |
| `USE_MOCK_IMAGES` | Mock görsel kullanımı (`true`/`false`) | ❌ Hayır |

> ⚠️ **Önemli:** `.env` dosyaları `.gitignore` tarafından hariç tutulmuştur ve GitHub'a yüklenmez. API anahtarlarınızı asla doğrudan kodda paylaşmayın.

---

## 📸 Ekran Görüntüleri

Proje ekran görüntüleri `report/screenshots/` klasöründe bulunmaktadır.

| Ekran | Açıklama |
|-------|----------|
| Strapi Admin | Content type ve veri yönetimi |
| Otomasyon Çıktısı | Python script çalışma sonucu |
| Streamlit Arayüzü | Şehir seçimi ve yemek kartları |

> 📌 Ekran görüntülerini projeyi çalıştırdıktan sonra ekleyebilirsiniz.

---

## 📄 Lisans

Bu proje eğitim amaçlı hazırlanmıştır. — İçerik Yönetimi Dersi Final Projesi
