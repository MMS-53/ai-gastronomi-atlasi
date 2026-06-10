from html import escape
import os

import requests
import streamlit as st


st.set_page_config(
    page_title="YZ Destekli Gastronomi Atlası",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded",
)


def config_value(key, default=""):
    try:
        return st.secrets.get(key, os.getenv(key, default))
    except Exception:
        return os.getenv(key, default)


STRAPI_URL = config_value("STRAPI_URL", "").rstrip("/")
STRAPI_API_TOKEN = config_value("STRAPI_API_TOKEN", "")
HEADERS = {"Authorization": f"Bearer {STRAPI_API_TOKEN}"} if STRAPI_API_TOKEN else {}
REQUEST_TIMEOUT = 60


st.markdown(
    """
    <style>
    .block-container {max-width: 1180px; padding-top: 2rem;}
    .title {
        font-size: 2.8rem;
        font-weight: 800;
        text-align: center;
        color: #ff8a1d;
        margin-bottom: .3rem;
    }
    .subtitle {
        text-align: center;
        color: #9ca3af;
        font-size: 1.15rem;
        margin-bottom: 2rem;
    }
    .place-card {
        border: 1px solid rgba(255,255,255,.12);
        background: #111827;
        border-radius: 8px;
        overflow: hidden;
        margin-bottom: 1.2rem;
    }
    .place-card img {
        width: 100%;
        height: 210px;
        object-fit: cover;
        display: block;
    }
    .place-body {padding: 1rem 1.1rem 1.2rem;}
    .place-name {font-size: 1.35rem; font-weight: 750; color: white;}
    .meta {color: #fbbf24; margin: .35rem 0 .8rem;}
    .badge {
        display: inline-block;
        border: 1px solid rgba(255,255,255,.16);
        border-radius: 999px;
        padding: .18rem .55rem;
        margin-right: .4rem;
        color: #d1d5db;
        font-size: .82rem;
    }
    .label {color: #fb923c; font-weight: 700; margin-top: .7rem;}
    .text {color: #d1d5db; line-height: 1.55;}
    </style>
    """,
    unsafe_allow_html=True,
)


def get_attr(item, key, default=""):
    if isinstance(item, dict) and "attributes" in item:
        return item.get("attributes", {}).get(key, default)
    return item.get(key, default) if isinstance(item, dict) else default


def get_relation(item, relation_name, field="name"):
    attrs = item.get("attributes", item)
    relation = attrs.get(relation_name, {})
    if isinstance(relation, dict):
        data = relation.get("data", relation)
        if isinstance(data, dict):
            return data.get("attributes", data).get(field, "")
    return ""


def get_image_url(item):
    attrs = item.get("attributes", item)
    cover = attrs.get("cover_image", {})
    if isinstance(cover, dict):
        data = cover.get("data", cover)
        if isinstance(data, dict):
            image_attrs = data.get("attributes", data)
            url = image_attrs.get("url", "")
            if url:
                return f"{STRAPI_URL}{url}" if url.startswith("/") else url
    return ""


@st.cache_data(ttl=300)
def api_get(path, params=None):
    if not STRAPI_URL:
        raise RuntimeError("STRAPI_URL tanımlı değil.")
    response = requests.get(
        f"{STRAPI_URL}/api/{path}",
        headers=HEADERS,
        params=params or {},
        timeout=REQUEST_TIMEOUT,
    )
    response.raise_for_status()
    return response.json().get("data", [])


def stars(rating):
    try:
        value = float(rating or 0)
    except (TypeError, ValueError):
        value = 0
    full = int(value)
    return "★" * full + "☆" * max(0, 5 - full)


def render_place(place):
    attrs = place.get("attributes", place)
    name = escape(str(attrs.get("name", "Bilinmeyen Mekan")))
    desc_tr = escape(str(attrs.get("description_tr", "Açıklama mevcut değil.")))
    desc_en = escape(str(attrs.get("description_en", "Description not available.")))
    rating = attrs.get("rating", 0)
    city = escape(str(get_relation(place, "city")))
    category = escape(str(get_relation(place, "category") or attrs.get("category_name", "")))
    image_url = get_image_url(place)

    image_html = (
        f'<img src="{escape(image_url)}" alt="{name}">'
        if image_url
        else '<div style="height:210px;display:flex;align-items:center;justify-content:center;background:#1f2937;font-size:3rem;">🍽️</div>'
    )

    st.markdown(
        f"""
        <div class="place-card">
            {image_html}
            <div class="place-body">
                <div class="place-name">{name}</div>
                <div class="meta">{stars(rating)} {rating}/5</div>
                <span class="badge">📍 {city}</span>
                <span class="badge">🏷️ {category}</span>
                <div class="label">Türkçe Açıklama</div>
                <div class="text">{desc_tr}</div>
                <div class="label">English Description</div>
                <div class="text">{desc_en}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


with st.sidebar:
    st.markdown("## 🍽️ Gastronomi Atlası")
    st.divider()

    language = st.radio(
        "🌐 Arayüz Dili / Interface Language",
        ["Türkçe", "English"],
        index=0,
    )

    try:
        cities = api_get("cities", {"pagination[pageSize]": 100, "sort": "name:asc"})
    except Exception as exc:
        st.error(f"Şehirler yüklenirken hata oluştu: {exc}")
        cities = []

    city_names = [get_attr(city, "name") for city in cities]
    selected_city = st.selectbox(
        "Şehir Seçin" if language == "Türkçe" else "Select City",
        city_names,
        index=0 if city_names else None,
        placeholder="Şehir seçin",
    )

    st.divider()
    st.markdown("### 📊 İstatistikler")
    try:
        all_places = api_get("places", {"pagination[pageSize]": 100})
        categories = api_get("categories", {"pagination[pageSize]": 100})
    except Exception:
        all_places, categories = [], []
    st.metric("Şehir", len(city_names))
    st.metric("Mekan", len(all_places))
    st.metric("Kategori", len(categories))


st.markdown('<div class="title">🍽️ YZ Destekli Gastronomi Atlası</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Türkiye\'nin yöresel lezzetlerini keşfedin</div>',
    unsafe_allow_html=True,
)

if selected_city:
    try:
        places = api_get(
            "places",
            {
                "populate": "*",
                "filters[city][name][$eq]": selected_city,
                "pagination[pageSize]": 100,
                "sort": "rating:desc",
            },
        )
    except Exception as exc:
        st.error(f"Mekanlar yüklenirken hata oluştu: {exc}")
        places = []

    st.markdown(f"### 📍 {selected_city} - {len(places)} Gastronomi Mekanı")
    if places:
        cols = st.columns(2)
        for index, place in enumerate(places):
            with cols[index % 2]:
                render_place(place)
    else:
        st.info(f"{selected_city} için henüz mekan verisi bulunamadı.")
else:
    st.info("Şehir verisi bulunamadı. Strapi API ve Secrets ayarlarını kontrol edin.")

st.divider()
st.caption("🍽️ YZ Destekli Gastronomi Atlası - Strapi CMS + Python Otomasyon + Streamlit")
