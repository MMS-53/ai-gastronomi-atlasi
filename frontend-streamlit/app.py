"""
app.py — Streamlit Gastronomi Atlası Arayüzü
=============================================
Strapi CMS'den yemek verilerini çekerek modern kart tasarımıyla
kullanıcıya sunan çok dilli gastronomi atlası arayüzü.

Çalıştırma:
    cd frontend-streamlit
    streamlit run app.py
"""

import os
from html import escape
import requests
import streamlit as st"""
app.py — Streamlit Gastronomi Atlası Arayüzü
=============================================
Strapi CMS'den yemek verilerini çekerek modern kart tasarımıyla
kullanıcıya sunan çok dilli gastronomi atlası arayüzü.

Çalıştırma:
    cd frontend-streamlit
    streamlit run app.py
"""

import os
from html import escape
import requests
import streamlit as st
from dotenv import load_dotenv

# .env dosyasını yükle
load_dotenv()

# =============================================
# Sayfa Yapılandırması
# =============================================
st.set_page_config(
    page_title="🍽️ YZ Destekli Gastronomi Atlası",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =============================================
# Strapi API Ayarları
# =============================================
def get_config_value(key, default=""):
    """Önce Streamlit Cloud secrets, yoksa yerel .env dosyasını okur."""
    try:
        return st.secrets.get(key, os.getenv(key, default))
    except Exception:
        return os.getenv(key, default)


STRAPI_URL = get_config_value("STRAPI_URL", "http://localhost:1337")
STRAPI_API_TOKEN = get_config_value("STRAPI_API_TOKEN", "")
REQUEST_TIMEOUT = 45

# API istek başlıkları
HEADERS = {
    "Authorization": f"Bearer {STRAPI_API_TOKEN}",
}


# =============================================
# Özel CSS Stilleri
# =============================================
def inject_custom_css():
    """Modern ve şık arayüz için özel CSS enjekte eder."""
    st.markdown("""
    <style>
        /* Google Fonts — Modern tipografi */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Outfit:wght@400;500;600;700&display=swap');

        /* Ana sayfa stili */
        .main .block-container {
            padding-top: 2rem;
            max-width: 1200px;
        }

        /* Başlık stili */
        .main-title {
            font-family: 'Outfit', sans-serif;
            font-size: 2.8rem;
            font-weight: 700;
            background: linear-gradient(135deg, #FF6B35 0%, #F7931E 50%, #FFD700 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-align: center;
            margin-bottom: 0.3rem;
        }

        .sub-title {
            font-family: 'Inter', sans-serif;
            font-size: 1.1rem;
            color: #888;
            text-align: center;
            margin-bottom: 2rem;
        }

        /* Yemek kartı */
        .food-card {
            background: linear-gradient(145deg, #1a1a2e 0%, #16213e 100%);
            border: 1px solid rgba(255, 107, 53, 0.15);
            border-radius: 16px;
            padding: 0;
            margin-bottom: 1.5rem;
            overflow: hidden;
            transition: all 0.3s ease;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        }

        .food-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 8px 30px rgba(255, 107, 53, 0.2);
            border-color: rgba(255, 107, 53, 0.4);
        }

        /* Kart görsel alanı */
        .food-card-image {
            width: 100%;
            height: 220px;
            object-fit: cover;
            border-bottom: 2px solid rgba(255, 107, 53, 0.2);
        }

        /* Kart içerik alanı */
        .food-card-content {
            padding: 1.2rem 1.5rem;
        }

        /* Yemek adı */
        .food-name {
            font-family: 'Outfit', sans-serif;
            font-size: 1.5rem;
            font-weight: 600;
            color: #ffffff;
            margin-bottom: 0.5rem;
        }

        /* Etiket (badge) stili */
        .badge-container {
            display: flex;
            gap: 0.5rem;
            flex-wrap: wrap;
            margin-bottom: 0.8rem;
        }

        .badge {
            font-family: 'Inter', sans-serif;
            font-size: 0.75rem;
            font-weight: 500;
            padding: 0.25rem 0.7rem;
            border-radius: 20px;
            display: inline-block;
        }

        .badge-city {
            background: rgba(99, 102, 241, 0.2);
            color: #a5b4fc;
            border: 1px solid rgba(99, 102, 241, 0.3);
        }

        .badge-category {
            background: rgba(236, 72, 153, 0.2);
            color: #f9a8d4;
            border: 1px solid rgba(236, 72, 153, 0.3);
        }

        /* Puan stili */
        .rating {
            font-family: 'Inter', sans-serif;
            font-size: 0.95rem;
            color: #FFD700;
            margin-bottom: 0.8rem;
        }

        /* Açıklama stili */
        .description-label {
            font-family: 'Inter', sans-serif;
            font-size: 0.8rem;
            font-weight: 600;
            color: #FF6B35;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 0.3rem;
            margin-top: 0.8rem;
        }

        .description-text {
            font-family: 'Inter', sans-serif;
            font-size: 0.9rem;
            color: #d1d5db;
            line-height: 1.6;
            margin-bottom: 0.5rem;
        }

        /* Sidebar stili */
        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #0f0f23 0%, #1a1a2e 100%);
        }

        /* Bilgi kartı */
        .info-card {
            background: linear-gradient(135deg, #1e3a5f 0%, #1a1a2e 100%);
            border: 1px solid rgba(99, 102, 241, 0.2);
            border-radius: 12px;
            padding: 1.2rem;
            margin-bottom: 1rem;
        }

        .info-card h4 {
            font-family: 'Outfit', sans-serif;
            color: #a5b4fc;
            margin-bottom: 0.5rem;
        }

        .info-card p {
            font-family: 'Inter', sans-serif;
            color: #d1d5db;
            font-size: 0.9rem;
            line-height: 1.5;
        }

        /* İstatistik kartları */
        .stat-card {
            background: linear-gradient(135deg, rgba(255, 107, 53, 0.1) 0%, rgba(255, 215, 0, 0.05) 100%);
            border: 1px solid rgba(255, 107, 53, 0.2);
            border-radius: 12px;
            padding: 1rem;
            text-align: center;
        }

        .stat-number {
            font-family: 'Outfit', sans-serif;
            font-size: 2rem;
            font-weight: 700;
            color: #FF6B35;
        }

        .stat-label {
            font-family: 'Inter', sans-serif;
            font-size: 0.85rem;
            color: #9ca3af;
            margin-top: 0.3rem;
        }

        /* Placeholder görsel */
        .placeholder-image {
            width: 100%;
            height: 220px;
            background: linear-gradient(135deg, #FF6B35 0%, #F7931E 50%, #e65100 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 3rem;
        }

        /* Footer */
        .footer {
            text-align: center;
            color: #6b7280;
            font-family: 'Inter', sans-serif;
            font-size: 0.8rem;
            margin-top: 3rem;
            padding: 1.5rem;
            border-top: 1px solid rgba(255, 255, 255, 0.1);
        }
    </style>
    """, unsafe_allow_html=True)


# =============================================
# API Fonksiyonları
# =============================================

@st.cache_data(ttl=300)
def fetch_cities():
    """
    Strapi API'den tüm şehirleri çeker.
    Sonuçlar 5 dakika (300 saniye) boyunca önbelleğe alınır.

    Dönüş:
        list: Şehir kayıtlarının listesi
    """
    try:
        response = requests.get(
            f"{STRAPI_URL}/api/cities",
            headers=HEADERS,
            params={"pagination[pageSize]": 100, "sort": "name:asc"},
            timeout=REQUEST_TIMEOUT,
        )
        response.raise_for_status()
        data = response.json().get("data", [])
        return data
    except requests.exceptions.ConnectionError:
        st.error("⚠️ Strapi sunucusuna bağlanılamadı. Lütfen Strapi'nin çalıştığından emin olun.")
        return []
    except Exception as e:
        st.error(f"⚠️ Şehirler yüklenirken hata oluştu: {str(e)}")
        return []


@st.cache_data(ttl=300)
def fetch_foods_by_city(city_name):
    """
    Belirtilen şehre ait yemekleri Strapi API'den çeker.
    İlişkili veriler (city, category, cover_image) dahil edilir.

    Parametreler:
        city_name (str): Filtrelenecek şehir adı

    Dönüş:
        list: Yemek kayıtlarının listesi (ilişkili verilerle birlikte)
    """
    try:
        response = requests.get(
            f"{STRAPI_URL}/api/places",
            headers=HEADERS,
            params={
                "populate": "*",
                "filters[city][name][$eq]": city_name,
                "pagination[pageSize]": 100,
                "sort": "rating:desc",
            },
            timeout=REQUEST_TIMEOUT,
        )
        response.raise_for_status()
        data = response.json().get("data", [])
        return data
    except requests.exceptions.ConnectionError:
        st.error("⚠️ Strapi sunucusuna bağlanılamadı.")
        return []
    except Exception as e:
        st.error(f"⚠️ Mekanlar yüklenirken hata oluştu: {str(e)}")
        return []


@st.cache_data(ttl=300)
def fetch_all_foods():
    """
    Tüm yemekleri Strapi API'den çeker (istatistikler için).

    Dönüş:
        list: Tüm yemek kayıtlarının listesi
    """
    try:
        response = requests.get(
            f"{STRAPI_URL}/api/places",
            headers=HEADERS,
            params={
                "populate": "*",
                "pagination[pageSize]": 100,
            },
            timeout=REQUEST_TIMEOUT,
        )
        response.raise_for_status()
        return response.json().get("data", [])
    except Exception:
        return []


@st.cache_data(ttl=300)
def fetch_categories():
    """
    Tüm kategorileri Strapi API'den çeker.

    Dönüş:
        list: Kategori kayıtlarının listesi
    """
    try:
        response = requests.get(
            f"{STRAPI_URL}/api/categories",
            headers=HEADERS,
            params={"pagination[pageSize]": 100},
            timeout=REQUEST_TIMEOUT,
        )
        response.raise_for_status()
        return response.json().get("data", [])
    except Exception:
        return []


# =============================================
# Yardımcı Fonksiyonlar
# =============================================

def get_attribute(item, key, default=""):
    """
    Strapi v4 veri yapısından alan değerini güvenli şekilde alır.
    Strapi v4'te veriler 'attributes' altında saklanır.

    Parametreler:
        item (dict): Strapi veri nesnesi
        key (str): Alan adı
        default: Varsayılan değer

    Dönüş:
        Alan değeri veya varsayılan değer
    """
    # Strapi v4 yapısı: data.attributes.field
    if "attributes" in item:
        return item.get("attributes", {}).get(key, default)
    # Düz yapı (bazı sorgularda)
    return item.get(key, default)


def get_relation(item, relation_name, field="name"):
    """
    Strapi v4 ilişkili veriyi alır.

    Parametreler:
        item (dict): Strapi veri nesnesi
        relation_name (str): İlişki adı (örn: "city", "category")
        field (str): İlişkili nesnenin hangi alanı alınacak

    Dönüş:
        str: İlişkili alan değeri veya boş string
    """
    attrs = item.get("attributes", item)
    relation = attrs.get(relation_name, {})

    # İlişki verisi data altında olabilir
    if isinstance(relation, dict):
        data = relation.get("data", relation)
        if isinstance(data, dict):
            return data.get("attributes", data).get(field, "")
    return ""


def get_cover_image_url(item):
    """
    Yemek kaydından kapak görseli URL'sini alır.

    Parametreler:
        item (dict): Strapi yemek veri nesnesi

    Dönüş:
        str veya None: Görselin tam URL'si veya None
    """
    attrs = item.get("attributes", item)
    cover = attrs.get("cover_image", {})

    if isinstance(cover, dict):
        data = cover.get("data", cover)
        if isinstance(data, dict):
            image_attrs = data.get("attributes", data)
            url = image_attrs.get("url", "")
            if url:
                # Göreceli URL ise tam URL'ye dönüştür
                if url.startswith("/"):
                    return f"{STRAPI_URL}{url}"
                return url
    return None


def render_stars(rating):
    """
    Puan değerini yıldız emojilerine dönüştürür.

    Parametreler:
        rating (float): Puan değeri (0-5 arası)

    Dönüş:
        str: Yıldız emoji dizisi
    """
    if not rating:
        return "☆☆☆☆☆"
    full_stars = int(rating)
    half_star = 1 if rating - full_stars >= 0.5 else 0
    empty_stars = 5 - full_stars - half_star
    return "★" * full_stars + "½" * half_star + "☆" * empty_stars


# =============================================
# Kart Render Fonksiyonu
# =============================================

def render_food_card(food):
    """
    Tek bir yemek için modern kart bileşenini oluşturur.

    Parametreler:
        food (dict): Strapi yemek veri nesnesi
    """
    # Veri alanlarını çıkar
    attrs = food.get("attributes", food)
    name = escape(str(attrs.get("name", "Bilinmeyen Mekan")))
    desc_tr = escape(str(attrs.get("description_tr", "Açıklama mevcut değil.")))
    desc_en = escape(str(attrs.get("description_en", "Description not available.")))
    rating = attrs.get("rating", 0)

    # İlişkili veriler
    city_name = escape(str(get_relation(food, "city")))
    category_name = escape(str(get_relation(food, "category") or attrs.get("category_name", "")))
    image_url = get_cover_image_url(food)

    # Görsel HTML'i
    if image_url:
        image_html = f'<img src="{image_url}" class="food-card-image" alt="{name}" />'
    else:
        image_html = f'<div class="placeholder-image">🍽️</div>'

    # Puan yıldızları
    stars = render_stars(rating)

    # Kart HTML'i
    card_html = f"""
    <div class="food-card">
        {image_html}
        <div class="food-card-content">
            <div class="food-name">{name}</div>
            <div class="badge-container">
                <span class="badge badge-city">📍 {city_name}</span>
                <span class="badge badge-category">🏷️ {category_name}</span>
            </div>
            <div class="rating">{stars} {rating}/5</div>

            <div class="description-label">🇹🇷 Türkçe Açıklama</div>
            <div class="description-text">{desc_tr}</div>

            <div class="description-label">🇬🇧 English Description</div>
            <div class="description-text">{desc_en}</div>
        </div>
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)


# =============================================
# Ana Uygulama
# =============================================

def main():
    """Ana Streamlit uygulama fonksiyonu."""
    # Özel CSS enjekte et
    inject_custom_css()

    # ---- Sidebar ----
    with st.sidebar:
        st.markdown("## 🍽️ Gastronomi Atlası")
        st.markdown("---")

        # Dil seçimi
        language = st.radio(
            "🌐 Arayüz Dili / Interface Language",
            ["Türkçe", "English"],
            index=0,
        )

        st.markdown("---")

        # Şehir listesini çek
        cities = fetch_cities()
        city_names = [get_attribute(c, "name") for c in cities]

        if city_names:
            selected_city = st.selectbox(
                "🏙️ Şehir Seçin" if language == "Türkçe" else "🏙️ Select City",
                options=city_names,
                index=0,
            )
        else:
            selected_city = None
            st.warning(
                "Henüz şehir verisi bulunamadı. Lütfen otomasyon scriptini çalıştırın."
                if language == "Türkçe"
                else "No city data found. Please run the automation script."
            )

        st.markdown("---")

        # Şehir bilgisi göster
        if selected_city and cities:
            selected_city_data = next(
                (c for c in cities if get_attribute(c, "name") == selected_city),
                None,
            )
            if selected_city_data:
                desc = get_attribute(selected_city_data, "short_description", "")
                country = get_attribute(selected_city_data, "country", "")
                st.markdown(f"""
                <div class="info-card">
                    <h4>📍 {selected_city}, {country}</h4>
                    <p>{desc}</p>
                </div>
                """, unsafe_allow_html=True)

        # İstatistikler
        st.markdown("### 📊 " + ("İstatistikler" if language == "Türkçe" else "Statistics"))
        all_foods = fetch_all_foods()
        categories = fetch_categories()

        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-number">{len(city_names)}</div>
                <div class="stat-label">{"Şehir" if language == "Türkçe" else "Cities"}</div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-number">{len(all_foods)}</div>
                <div class="stat-label">{"Mekan" if language == "Türkçe" else "Places"}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        col3, col4 = st.columns(2)
        with col3:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-number">{len(categories)}</div>
                <div class="stat-label">{"Kategori" if language == "Türkçe" else "Categories"}</div>
            </div>
            """, unsafe_allow_html=True)
        with col4:
            # Ortalama puan hesapla
            ratings = [
                get_attribute(f, "rating", 0)
                for f in all_foods
                if get_attribute(f, "rating", 0)
            ]
            avg_rating = sum(ratings) / len(ratings) if ratings else 0
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-number">{avg_rating:.1f}</div>
                <div class="stat-label">{"Ort. Puan" if language == "Türkçe" else "Avg. Rating"}</div>
            </div>
            """, unsafe_allow_html=True)

    # ---- Ana İçerik ----

    # Başlık
    if language == "Türkçe":
        st.markdown('<div class="main-title">🍽️ YZ Destekli Gastronomi Atlası</div>', unsafe_allow_html=True)
        st.markdown('<div class="sub-title">Türkiye\'nin yöresel lezzetlerini keşfedin</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="main-title">🍽️ AI-Powered Gastronomy Atlas</div>', unsafe_allow_html=True)
        st.markdown('<div class="sub-title">Discover the regional flavors of Türkiye</div>', unsafe_allow_html=True)

    # Seçili şehrin mekanlarını göster
    if selected_city:
        foods = fetch_foods_by_city(selected_city)

        if foods:
            food_count = len(foods)
            st.markdown(
                f"### 📍 {selected_city} — "
                + (f"{food_count} Gastronomi Mekanı" if language == "Türkçe" else f"{food_count} Gastronomy Places"),
            )

            # Yemek kartlarını iki sütunlu grid olarak göster
            cols = st.columns(2)
            for idx, food in enumerate(foods):
                with cols[idx % 2]:
                    render_food_card(food)
        else:
            st.info(
                f"📭 {selected_city} için henüz mekan verisi bulunamadı."
                if language == "Türkçe"
                else f"📭 No place data found for {selected_city}."
            )
    else:
        # Henüz veri yoksa bilgilendirme mesajı göster
        st.markdown("---")
        if language == "Türkçe":
            st.info(
                "🔗 Strapi sunucusunun çalıştığından ve verilerin yüklendiğinden emin olun.\n\n"
                "**Hızlı Başlangıç:**\n"
                "1. `backend-strapi/` klasöründe `npm run develop` çalıştırın\n"
                "2. `automation/` klasöründe `python main.py` çalıştırın\n"
                "3. Bu sayfayı yenileyin"
            )
        else:
            st.info(
                "🔗 Make sure Strapi is running and data has been loaded.\n\n"
                "**Quick Start:**\n"
                "1. Run `npm run develop` in `backend-strapi/`\n"
                "2. Run `python main.py` in `automation/`\n"
                "3. Refresh this page"
            )

    # ---- Footer ----
    st.markdown("""
    <div class="footer">
        🍽️ YZ Destekli Gastronomi Atlası — İçerik Yönetimi Dersi Final Projesi<br>
        Strapi CMS + Python Otomasyon + Streamlit
    </div>
    """, unsafe_allow_html=True)


# Uygulamayı başlat
if __name__ == "__main__":
    main()

from dotenv import load_dotenv

# .env dosyasını yükle
load_dotenv()

# =============================================
# Sayfa Yapılandırması
# =============================================
st.set_page_config(
    page_title="🍽️ YZ Destekli Gastronomi Atlası",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =============================================
# Strapi API Ayarları
# =============================================
def get_config_value(key, default=""):
    """Önce Streamlit Cloud secrets, yoksa yerel .env dosyasını okur."""
    try:
        return st.secrets.get(key, os.getenv(key, default))
    except Exception:
        return os.getenv(key, default)


STRAPI_URL = get_config_value("STRAPI_URL", "http://localhost:1337")
STRAPI_API_TOKEN = get_config_value("STRAPI_API_TOKEN", "")

# API istek başlıkları
HEADERS = {
    "Authorization": f"Bearer {STRAPI_API_TOKEN}",
}


# =============================================
# Özel CSS Stilleri
# =============================================
def inject_custom_css():
    """Modern ve şık arayüz için özel CSS enjekte eder."""
    st.markdown("""
    <style>
        /* Google Fonts — Modern tipografi */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Outfit:wght@400;500;600;700&display=swap');

        /* Ana sayfa stili */
        .main .block-container {
            padding-top: 2rem;
            max-width: 1200px;
        }

        /* Başlık stili */
        .main-title {
            font-family: 'Outfit', sans-serif;
            font-size: 2.8rem;
            font-weight: 700;
            background: linear-gradient(135deg, #FF6B35 0%, #F7931E 50%, #FFD700 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-align: center;
            margin-bottom: 0.3rem;
        }

        .sub-title {
            font-family: 'Inter', sans-serif;
            font-size: 1.1rem;
            color: #888;
            text-align: center;
            margin-bottom: 2rem;
        }

        /* Yemek kartı */
        .food-card {
            background: linear-gradient(145deg, #1a1a2e 0%, #16213e 100%);
            border: 1px solid rgba(255, 107, 53, 0.15);
            border-radius: 16px;
            padding: 0;
            margin-bottom: 1.5rem;
            overflow: hidden;
            transition: all 0.3s ease;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        }

        .food-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 8px 30px rgba(255, 107, 53, 0.2);
            border-color: rgba(255, 107, 53, 0.4);
        }

        /* Kart görsel alanı */
        .food-card-image {
            width: 100%;
            height: 220px;
            object-fit: cover;
            border-bottom: 2px solid rgba(255, 107, 53, 0.2);
        }

        /* Kart içerik alanı */
        .food-card-content {
            padding: 1.2rem 1.5rem;
        }

        /* Yemek adı */
        .food-name {
            font-family: 'Outfit', sans-serif;
            font-size: 1.5rem;
            font-weight: 600;
            color: #ffffff;
            margin-bottom: 0.5rem;
        }

        /* Etiket (badge) stili */
        .badge-container {
            display: flex;
            gap: 0.5rem;
            flex-wrap: wrap;
            margin-bottom: 0.8rem;
        }

        .badge {
            font-family: 'Inter', sans-serif;
            font-size: 0.75rem;
            font-weight: 500;
            padding: 0.25rem 0.7rem;
            border-radius: 20px;
            display: inline-block;
        }

        .badge-city {
            background: rgba(99, 102, 241, 0.2);
            color: #a5b4fc;
            border: 1px solid rgba(99, 102, 241, 0.3);
        }

        .badge-category {
            background: rgba(236, 72, 153, 0.2);
            color: #f9a8d4;
            border: 1px solid rgba(236, 72, 153, 0.3);
        }

        /* Puan stili */
        .rating {
            font-family: 'Inter', sans-serif;
            font-size: 0.95rem;
            color: #FFD700;
            margin-bottom: 0.8rem;
        }

        /* Açıklama stili */
        .description-label {
            font-family: 'Inter', sans-serif;
            font-size: 0.8rem;
            font-weight: 600;
            color: #FF6B35;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 0.3rem;
            margin-top: 0.8rem;
        }

        .description-text {
            font-family: 'Inter', sans-serif;
            font-size: 0.9rem;
            color: #d1d5db;
            line-height: 1.6;
            margin-bottom: 0.5rem;
        }

        /* Sidebar stili */
        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #0f0f23 0%, #1a1a2e 100%);
        }

        /* Bilgi kartı */
        .info-card {
            background: linear-gradient(135deg, #1e3a5f 0%, #1a1a2e 100%);
            border: 1px solid rgba(99, 102, 241, 0.2);
            border-radius: 12px;
            padding: 1.2rem;
            margin-bottom: 1rem;
        }

        .info-card h4 {
            font-family: 'Outfit', sans-serif;
            color: #a5b4fc;
            margin-bottom: 0.5rem;
        }

        .info-card p {
            font-family: 'Inter', sans-serif;
            color: #d1d5db;
            font-size: 0.9rem;
            line-height: 1.5;
        }

        /* İstatistik kartları */
        .stat-card {
            background: linear-gradient(135deg, rgba(255, 107, 53, 0.1) 0%, rgba(255, 215, 0, 0.05) 100%);
            border: 1px solid rgba(255, 107, 53, 0.2);
            border-radius: 12px;
            padding: 1rem;
            text-align: center;
        }

        .stat-number {
            font-family: 'Outfit', sans-serif;
            font-size: 2rem;
            font-weight: 700;
            color: #FF6B35;
        }

        .stat-label {
            font-family: 'Inter', sans-serif;
            font-size: 0.85rem;
            color: #9ca3af;
            margin-top: 0.3rem;
        }

        /* Placeholder görsel */
        .placeholder-image {
            width: 100%;
            height: 220px;
            background: linear-gradient(135deg, #FF6B35 0%, #F7931E 50%, #e65100 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 3rem;
        }

        /* Footer */
        .footer {
            text-align: center;
            color: #6b7280;
            font-family: 'Inter', sans-serif;
            font-size: 0.8rem;
            margin-top: 3rem;
            padding: 1.5rem;
            border-top: 1px solid rgba(255, 255, 255, 0.1);
        }
    </style>
    """, unsafe_allow_html=True)


# =============================================
# API Fonksiyonları
# =============================================

@st.cache_data(ttl=300)
def fetch_cities():
    """
    Strapi API'den tüm şehirleri çeker.
    Sonuçlar 5 dakika (300 saniye) boyunca önbelleğe alınır.

    Dönüş:
        list: Şehir kayıtlarının listesi
    """
    try:
        response = requests.get(
            f"{STRAPI_URL}/api/cities",
            headers=HEADERS,
            params={"pagination[pageSize]": 100, "sort": "name:asc"},
            timeout=10,
        )
        response.raise_for_status()
        data = response.json().get("data", [])
        return data
    except requests.exceptions.ConnectionError:
        st.error("⚠️ Strapi sunucusuna bağlanılamadı. Lütfen Strapi'nin çalıştığından emin olun.")
        return []
    except Exception as e:
        st.error(f"⚠️ Şehirler yüklenirken hata oluştu: {str(e)}")
        return []


@st.cache_data(ttl=300)
def fetch_foods_by_city(city_name):
    """
    Belirtilen şehre ait yemekleri Strapi API'den çeker.
    İlişkili veriler (city, category, cover_image) dahil edilir.

    Parametreler:
        city_name (str): Filtrelenecek şehir adı

    Dönüş:
        list: Yemek kayıtlarının listesi (ilişkili verilerle birlikte)
    """
    try:
        response = requests.get(
            f"{STRAPI_URL}/api/places",
            headers=HEADERS,
            params={
                "populate": "*",
                "filters[city][name][$eq]": city_name,
                "pagination[pageSize]": 100,
                "sort": "rating:desc",
            },
            timeout=10,
        )
        response.raise_for_status()
        data = response.json().get("data", [])
        return data
    except requests.exceptions.ConnectionError:
        st.error("⚠️ Strapi sunucusuna bağlanılamadı.")
        return []
    except Exception as e:
        st.error(f"⚠️ Mekanlar yüklenirken hata oluştu: {str(e)}")
        return []


@st.cache_data(ttl=300)
def fetch_all_foods():
    """
    Tüm yemekleri Strapi API'den çeker (istatistikler için).

    Dönüş:
        list: Tüm yemek kayıtlarının listesi
    """
    try:
        response = requests.get(
            f"{STRAPI_URL}/api/places",
            headers=HEADERS,
            params={
                "populate": "*",
                "pagination[pageSize]": 100,
            },
            timeout=10,
        )
        response.raise_for_status()
        return response.json().get("data", [])
    except Exception:
        return []


@st.cache_data(ttl=300)
def fetch_categories():
    """
    Tüm kategorileri Strapi API'den çeker.

    Dönüş:
        list: Kategori kayıtlarının listesi
    """
    try:
        response = requests.get(
            f"{STRAPI_URL}/api/categories",
            headers=HEADERS,
            params={"pagination[pageSize]": 100},
            timeout=10,
        )
        response.raise_for_status()
        return response.json().get("data", [])
    except Exception:
        return []


# =============================================
# Yardımcı Fonksiyonlar
# =============================================

def get_attribute(item, key, default=""):
    """
    Strapi v4 veri yapısından alan değerini güvenli şekilde alır.
    Strapi v4'te veriler 'attributes' altında saklanır.

    Parametreler:
        item (dict): Strapi veri nesnesi
        key (str): Alan adı
        default: Varsayılan değer

    Dönüş:
        Alan değeri veya varsayılan değer
    """
    # Strapi v4 yapısı: data.attributes.field
    if "attributes" in item:
        return item.get("attributes", {}).get(key, default)
    # Düz yapı (bazı sorgularda)
    return item.get(key, default)


def get_relation(item, relation_name, field="name"):
    """
    Strapi v4 ilişkili veriyi alır.

    Parametreler:
        item (dict): Strapi veri nesnesi
        relation_name (str): İlişki adı (örn: "city", "category")
        field (str): İlişkili nesnenin hangi alanı alınacak

    Dönüş:
        str: İlişkili alan değeri veya boş string
    """
    attrs = item.get("attributes", item)
    relation = attrs.get(relation_name, {})

    # İlişki verisi data altında olabilir
    if isinstance(relation, dict):
        data = relation.get("data", relation)
        if isinstance(data, dict):
            return data.get("attributes", data).get(field, "")
    return ""


def get_cover_image_url(item):
    """
    Yemek kaydından kapak görseli URL'sini alır.

    Parametreler:
        item (dict): Strapi yemek veri nesnesi

    Dönüş:
        str veya None: Görselin tam URL'si veya None
    """
    attrs = item.get("attributes", item)
    cover = attrs.get("cover_image", {})

    if isinstance(cover, dict):
        data = cover.get("data", cover)
        if isinstance(data, dict):
            image_attrs = data.get("attributes", data)
            url = image_attrs.get("url", "")
            if url:
                # Göreceli URL ise tam URL'ye dönüştür
                if url.startswith("/"):
                    return f"{STRAPI_URL}{url}"
                return url
    return None


def render_stars(rating):
    """
    Puan değerini yıldız emojilerine dönüştürür.

    Parametreler:
        rating (float): Puan değeri (0-5 arası)

    Dönüş:
        str: Yıldız emoji dizisi
    """
    if not rating:
        return "☆☆☆☆☆"
    full_stars = int(rating)
    half_star = 1 if rating - full_stars >= 0.5 else 0
    empty_stars = 5 - full_stars - half_star
    return "★" * full_stars + "½" * half_star + "☆" * empty_stars


# =============================================
# Kart Render Fonksiyonu
# =============================================

def render_food_card(food):
    """
    Tek bir yemek için modern kart bileşenini oluşturur.

    Parametreler:
        food (dict): Strapi yemek veri nesnesi
    """
    # Veri alanlarını çıkar
    attrs = food.get("attributes", food)
    name = escape(str(attrs.get("name", "Bilinmeyen Mekan")))
    desc_tr = escape(str(attrs.get("description_tr", "Açıklama mevcut değil.")))
    desc_en = escape(str(attrs.get("description_en", "Description not available.")))
    rating = attrs.get("rating", 0)

    # İlişkili veriler
    city_name = escape(str(get_relation(food, "city")))
    category_name = escape(str(get_relation(food, "category") or attrs.get("category_name", "")))
    image_url = get_cover_image_url(food)

    # Görsel HTML'i
    if image_url:
        image_html = f'<img src="{image_url}" class="food-card-image" alt="{name}" />'
    else:
        image_html = f'<div class="placeholder-image">🍽️</div>'

    # Puan yıldızları
    stars = render_stars(rating)

    # Kart HTML'i
    card_html = f"""
    <div class="food-card">
        {image_html}
        <div class="food-card-content">
            <div class="food-name">{name}</div>
            <div class="badge-container">
                <span class="badge badge-city">📍 {city_name}</span>
                <span class="badge badge-category">🏷️ {category_name}</span>
            </div>
            <div class="rating">{stars} {rating}/5</div>

            <div class="description-label">🇹🇷 Türkçe Açıklama</div>
            <div class="description-text">{desc_tr}</div>

            <div class="description-label">🇬🇧 English Description</div>
            <div class="description-text">{desc_en}</div>
        </div>
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)


# =============================================
# Ana Uygulama
# =============================================

def main():
    """Ana Streamlit uygulama fonksiyonu."""
    # Özel CSS enjekte et
    inject_custom_css()

    # ---- Sidebar ----
    with st.sidebar:
        st.markdown("## 🍽️ Gastronomi Atlası")
        st.markdown("---")

        # Dil seçimi
        language = st.radio(
            "🌐 Arayüz Dili / Interface Language",
            ["Türkçe", "English"],
            index=0,
        )

        st.markdown("---")

        # Şehir listesini çek
        cities = fetch_cities()
        city_names = [get_attribute(c, "name") for c in cities]

        if city_names:
            selected_city = st.selectbox(
                "🏙️ Şehir Seçin" if language == "Türkçe" else "🏙️ Select City",
                options=city_names,
                index=0,
            )
        else:
            selected_city = None
            st.warning(
                "Henüz şehir verisi bulunamadı. Lütfen otomasyon scriptini çalıştırın."
                if language == "Türkçe"
                else "No city data found. Please run the automation script."
            )

        st.markdown("---")

        # Şehir bilgisi göster
        if selected_city and cities:
            selected_city_data = next(
                (c for c in cities if get_attribute(c, "name") == selected_city),
                None,
            )
            if selected_city_data:
                desc = get_attribute(selected_city_data, "short_description", "")
                country = get_attribute(selected_city_data, "country", "")
                st.markdown(f"""
                <div class="info-card">
                    <h4>📍 {selected_city}, {country}</h4>
                    <p>{desc}</p>
                </div>
                """, unsafe_allow_html=True)

        # İstatistikler
        st.markdown("### 📊 " + ("İstatistikler" if language == "Türkçe" else "Statistics"))
        all_foods = fetch_all_foods()
        categories = fetch_categories()

        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-number">{len(city_names)}</div>
                <div class="stat-label">{"Şehir" if language == "Türkçe" else "Cities"}</div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-number">{len(all_foods)}</div>
                <div class="stat-label">{"Mekan" if language == "Türkçe" else "Places"}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        col3, col4 = st.columns(2)
        with col3:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-number">{len(categories)}</div>
                <div class="stat-label">{"Kategori" if language == "Türkçe" else "Categories"}</div>
            </div>
            """, unsafe_allow_html=True)
        with col4:
            # Ortalama puan hesapla
            ratings = [
                get_attribute(f, "rating", 0)
                for f in all_foods
                if get_attribute(f, "rating", 0)
            ]
            avg_rating = sum(ratings) / len(ratings) if ratings else 0
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-number">{avg_rating:.1f}</div>
                <div class="stat-label">{"Ort. Puan" if language == "Türkçe" else "Avg. Rating"}</div>
            </div>
            """, unsafe_allow_html=True)

    # ---- Ana İçerik ----

    # Başlık
    if language == "Türkçe":
        st.markdown('<div class="main-title">🍽️ YZ Destekli Gastronomi Atlası</div>', unsafe_allow_html=True)
        st.markdown('<div class="sub-title">Türkiye\'nin yöresel lezzetlerini keşfedin</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="main-title">🍽️ AI-Powered Gastronomy Atlas</div>', unsafe_allow_html=True)
        st.markdown('<div class="sub-title">Discover the regional flavors of Türkiye</div>', unsafe_allow_html=True)

    # Seçili şehrin mekanlarını göster
    if selected_city:
        foods = fetch_foods_by_city(selected_city)

        if foods:
            food_count = len(foods)
            st.markdown(
                f"### 📍 {selected_city} — "
                + (f"{food_count} Gastronomi Mekanı" if language == "Türkçe" else f"{food_count} Gastronomy Places"),
            )

            # Yemek kartlarını iki sütunlu grid olarak göster
            cols = st.columns(2)
            for idx, food in enumerate(foods):
                with cols[idx % 2]:
                    render_food_card(food)
        else:
            st.info(
                f"📭 {selected_city} için henüz mekan verisi bulunamadı."
                if language == "Türkçe"
                else f"📭 No place data found for {selected_city}."
            )
    else:
        # Henüz veri yoksa bilgilendirme mesajı göster
        st.markdown("---")
        if language == "Türkçe":
            st.info(
                "🔗 Strapi sunucusunun çalıştığından ve verilerin yüklendiğinden emin olun.\n\n"
                "**Hızlı Başlangıç:**\n"
                "1. `backend-strapi/` klasöründe `npm run develop` çalıştırın\n"
                "2. `automation/` klasöründe `python main.py` çalıştırın\n"
                "3. Bu sayfayı yenileyin"
            )
        else:
            st.info(
                "🔗 Make sure Strapi is running and data has been loaded.\n\n"
                "**Quick Start:**\n"
                "1. Run `npm run develop` in `backend-strapi/`\n"
                "2. Run `python main.py` in `automation/`\n"
                "3. Refresh this page"
            )

    # ---- Footer ----
    st.markdown("""
    <div class="footer">
        🍽️ YZ Destekli Gastronomi Atlası — İçerik Yönetimi Dersi Final Projesi<br>
        Strapi CMS + Python Otomasyon + Streamlit
    </div>
    """, unsafe_allow_html=True)


# Uygulamayı başlat
if __name__ == "__main__":
    main()
