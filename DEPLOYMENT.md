# Canlı Yayınlama Adımları

Bu proje canlı teslim için iki ayrı servise ihtiyaç duyar:

1. Strapi backend: Strapi Cloud üzerinde yayınlanır.
2. Streamlit frontend: Streamlit Community Cloud üzerinde `streamlit.app` linki olarak yayınlanır.

## 1. GitHub'a Yükleme

Projeyi GitHub'a yüklerken gizli dosyaları yüklemeyin. `.gitignore` şu dosyaları dışarıda bırakır:

- `.env`
- `node_modules/`
- `.tmp/`
- `dist/`
- `.strapi/`
- `public/uploads/`
- `automation/generated_images/`

## 2. Strapi Cloud Deploy

1. https://cloud.strapi.io adresine GitHub hesabınızla giriş yapın.
2. `Create project` seçin.
3. GitHub reposunu bağlayın.
4. Strapi proje dizini olarak `backend-strapi` klasörünü seçin.
5. Deploy tamamlanınca canlı Strapi admin adresini açın.
6. Admin hesabı oluşturun veya giriş yapın.
7. `Settings > API Tokens` alanından `Full Access` token oluşturun.

## 3. Canlı Strapi'yi Doldurma

`automation/.env` dosyasında canlı Strapi bilgilerini kullanın:

```env
STRAPI_URL=https://canli-strapi-adresiniz
STRAPI_API_TOKEN=canli_strapi_token
USE_MOCK_TRANSLATION=true
USE_MOCK_IMAGES=true
```

Sonra:

```powershell
cd automation
python main.py
```

Bu işlem şehirleri, kategorileri, mekanları ve görselleri canlı Strapi'ye yükler.

## 4. Streamlit Cloud Deploy

1. https://share.streamlit.io veya https://streamlit.io/cloud adresinden Streamlit Community Cloud'a giriş yapın.
2. `Create app` seçin.
3. GitHub reposunu seçin.
4. Main file path olarak şunu yazın:

```text
streamlit_app.py
```

5. Advanced settings / Secrets alanına şunu girin:

```toml
STRAPI_URL = "https://canli-strapi-adresiniz"
STRAPI_API_TOKEN = "canli_strapi_token"
```

6. Deploy edin.

Sonuç linki şu formatta olur:

```text
https://proje-adiniz.streamlit.app
```
