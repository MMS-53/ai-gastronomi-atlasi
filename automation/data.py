"""
data.py — Gastronomi Atlası Veri Modülü
========================================
Bu dosya, sistemde kullanılacak tüm şehir, kategori ve yemek verilerini içerir.
Veriler Python sözlük (dictionary) ve liste (list) yapılarında tanımlanmıştır.
Otomasyon scripti (main.py) bu verileri okuyarak Strapi CMS'e aktarır.
"""

# =============================================
# Şehir Verileri
# Her şehir için: isim, ülke ve kısa açıklama
# =============================================
CITIES = [
    {
        "name": "İstanbul",
        "country": "Türkiye",
        "short_description": (
            "Avrupa ile Asya'yı birleştiren İstanbul, Osmanlı mutfağının "
            "başkenti olarak bilinir. Boğaz kıyısında taze deniz ürünlerinden "
            "sokak lezzetlerine kadar geniş bir gastronomi yelpazesi sunar."
        ),
    },
    {
        "name": "Gaziantep",
        "country": "Türkiye",
        "short_description": (
            "UNESCO Yaratıcı Şehirler Ağı'na gastronomi alanında dahil edilen "
            "Gaziantep, Türk mutfağının en zengin şehirlerinden biridir. "
            "Baklava, kebap ve lahmacun ile dünyaca ünlüdür."
        ),
    },
    {
        "name": "Adana",
        "country": "Türkiye",
        "short_description": (
            "Adana, acılı ve lezzetli yemekleriyle tanınan bir Akdeniz şehridir. "
            "Adana kebabı başta olmak üzere et ağırlıklı mutfak kültürüyle "
            "Türkiye'nin gastronomi haritasında önemli bir yere sahiptir."
        ),
    },
    {
        "name": "Trabzon",
        "country": "Türkiye",
        "short_description": (
            "Karadeniz'in incisi Trabzon, hamsi ve mısır unu bazlı yemekleriyle "
            "öne çıkar. Yöresel lezzetleri doğanın cömertliğini yansıtır."
        ),
    },
    {
        "name": "Hatay",
        "country": "Türkiye",
        "short_description": (
            "Medeniyetler beşiği Hatay, Arap, Türk ve Akdeniz mutfaklarının "
            "harmanlandığı eşsiz bir gastronomi kültürüne ev sahipliği yapar. "
            "Künefe ve kebap çeşitleriyle meşhurdur."
        ),
    },
]

# =============================================
# Kategori Verileri
# Her kategori için: isim ve açıklama
# =============================================
CATEGORIES = [
    {
        "name": "Ana Yemek",
        "description": "Et, sebze veya baklagil bazlı, öğünün ana parçasını oluşturan doyurucu yemekler.",
    },
    {
        "name": "Tatlı",
        "description": "Yemek sonrası veya özel günlerde tüketilen şekerli ve hamurlu lezzetler.",
    },
    {
        "name": "Meze",
        "description": "Ana yemekten önce servis edilen, genellikle küçük porsiyonlarda sunulan başlangıçlar.",
    },
    {
        "name": "İçecek",
        "description": "Geleneksel ve yöresel içecekler; şerbetler, ayranlar ve sıcak içecekler.",
    },
    {
        "name": "Sokak Lezzeti",
        "description": "Sokak tezgâhlarında ve küçük büfelerde satılan, hızlı tüketilen lezzetler.",
    },
]

# =============================================
# Yemek Verileri
# Her yemek için: isim, Türkçe/İngilizce açıklama, malzemeler,
# puan, bağlı şehir ve kategori
# =============================================
FOODS = [
    # ---------- İstanbul ----------
    {
        "name": "Kumpir",
        "description_tr": (
            "Büyük bir patatesin fırında pişirildikten sonra ortadan yarılıp "
            "tereyağı ve kaşar peyniriyle karıştırılmasıyla hazırlanır. Üzerine "
            "sosis, mısır, rus salatası, turşu gibi çeşitli garnitürler eklenir. "
            "Ortaköy'ün simgesi haline gelmiş popüler bir sokak lezzetidir."
        ),
        "description_en": (
            "A large baked potato split open and mixed with butter and cheese, "
            "then topped with a variety of garnishes such as sausage, corn, "
            "Russian salad, and pickles. It has become an iconic street food "
            "of Istanbul's Ortaköy district."
        ),
        "ingredients": "Patates, tereyağı, kaşar peyniri, sosis, mısır, rus salatası, turşu, zeytin",
        "rating": 4.5,
        "city": "İstanbul",
        "category": "Sokak Lezzeti",
    },
    {
        "name": "Balık Ekmek",
        "description_tr": (
            "Taze ızgara edilmiş balığın, soğan, marul ve baharatlarla birlikte "
            "ekmek arasına konulmasıyla hazırlanan İstanbul'un en ikonik sokak "
            "yemeğidir. Eminönü'ndeki teknelerde satılan balık ekmek, "
            "şehrin sembollerinden biri haline gelmiştir."
        ),
        "description_en": (
            "A classic Istanbul street food made with freshly grilled fish "
            "served in bread with onions, lettuce, and spices. Sold on boats "
            "in Eminönü, it has become one of the city's most iconic culinary symbols."
        ),
        "ingredients": "Balık (uskumru veya palamut), ekmek, soğan, marul, limon, tuz, baharat",
        "rating": 4.7,
        "city": "İstanbul",
        "category": "Sokak Lezzeti",
    },
    {
        "name": "Hünkâr Beğendi",
        "description_tr": (
            "Osmanlı saray mutfağından günümüze ulaşan bu yemek, kızartılmış "
            "patlıcan püresi üzerine kuşbaşı etli yahni dökülerek servis edilir. "
            "Adını Osmanlı sultanlarının bu lezzetten çok etkilenmesinden almıştır."
        ),
        "description_en": (
            "A dish from Ottoman palace cuisine consisting of lamb stew "
            "served over a smoky eggplant puree enriched with béchamel sauce. "
            "Its name translates to 'the Sultan liked it,' referring to the "
            "sultan's delight upon tasting this dish."
        ),
        "ingredients": "Kuşbaşı et, patlıcan, süt, un, tereyağı, soğan, domates, biber",
        "rating": 4.8,
        "city": "İstanbul",
        "category": "Ana Yemek",
    },
    # ---------- Gaziantep ----------
    {
        "name": "Antep Baklavası",
        "description_tr": (
            "İnce yufka katmanları arasına özenle serilen Antep fıstığı iç harci, "
            "bol tereyağı ile pişirilip şerbetlenerek hazırlanır. Gaziantep'in "
            "dünyaca ünlü tatlısıdır ve UNESCO gastronomi mirası kapsamındadır."
        ),
        "description_en": (
            "Thin layers of phyllo dough filled with finely ground Antep pistachios, "
            "baked with generous amounts of butter, and soaked in sweet syrup. "
            "This world-renowned dessert is part of Gaziantep's UNESCO gastronomy heritage."
        ),
        "ingredients": "Yufka, Antep fıstığı, tereyağı, şeker, su, limon suyu",
        "rating": 4.9,
        "city": "Gaziantep",
        "category": "Tatlı",
    },
    {
        "name": "Lahmacun",
        "description_tr": (
            "İnce hamurun üzerine kıyma, soğan, domates, biber ve baharatlardan "
            "oluşan harç sürülerek taş fırında pişirilen geleneksel bir Gaziantep "
            "lezzetidir. Limon sıkılarak ve yeşilliklerle sarılarak yenir."
        ),
        "description_en": (
            "A thin flatbread topped with a mixture of minced meat, onions, "
            "tomatoes, peppers, and spices, baked in a stone oven. It is "
            "traditionally served with a squeeze of lemon and wrapped with fresh herbs."
        ),
        "ingredients": "Un, kıyma, soğan, domates, biber, maydanoz, limon, baharat",
        "rating": 4.6,
        "city": "Gaziantep",
        "category": "Sokak Lezzeti",
    },
    {
        "name": "Beyran Çorbası",
        "description_tr": (
            "Kuzu etinin uzun süre kaynatılmasıyla elde edilen yoğun bir çorbadır. "
            "Sarımsaklı et suyu, pirinç ve pul biber ile hazırlanır. "
            "Gaziantep'te özellikle sabah kahvaltısı olarak tüketilir ve enerji verici "
            "özelliğiyle bilinir."
        ),
        "description_en": (
            "A rich and hearty soup made by slow-cooking lamb in broth, "
            "seasoned with garlic, rice, and red pepper flakes. In Gaziantep, "
            "it is traditionally consumed for breakfast and is known for its "
            "energizing properties."
        ),
        "ingredients": "Kuzu eti, pirinç, sarımsak, pul biber, tereyağı, tuz",
        "rating": 4.4,
        "city": "Gaziantep",
        "category": "Ana Yemek",
    },
    # ---------- Adana ----------
    {
        "name": "Adana Kebabı",
        "description_tr": (
            "El ile çekilen kıymanın kuyruk yağı, pul biber ve tuz ile "
            "yoğrularak şişe geçirilip mangal ateşinde pişirilmesiyle hazırlanır. "
            "Türkiye'nin coğrafi işaret tescilli yemeklerinden biridir. "
            "Lavaş, soğan ve közlenmiş domates ile servis edilir."
        ),
        "description_en": (
            "Made from hand-minced meat mixed with tail fat, red pepper flakes, "
            "and salt, molded onto skewers and grilled over charcoal. It is one of "
            "Turkey's geographically certified dishes, served with flatbread, "
            "onions, and grilled tomatoes."
        ),
        "ingredients": "Dana kıyma, kuyruk yağı, pul biber, tuz, lavaş, soğan, domates",
        "rating": 4.9,
        "city": "Adana",
        "category": "Ana Yemek",
    },
    {
        "name": "Şalgam Suyu",
        "description_tr": (
            "Mor havuç, şalgam, bulgur unu ve tuz kullanılarak fermente edilen "
            "geleneksel bir Adana içeceğidir. Acılı ve acısız seçenekleri mevcuttur. "
            "Kebap yanında vazgeçilmez bir lezzettir."
        ),
        "description_en": (
            "A traditional fermented beverage from Adana made with purple carrots, "
            "turnips, bulgur flour, and salt. Available in spicy and mild versions, "
            "it is an indispensable accompaniment to kebabs."
        ),
        "ingredients": "Mor havuç, şalgam, bulgur unu, tuz, su",
        "rating": 4.3,
        "city": "Adana",
        "category": "İçecek",
    },
    {
        "name": "Bici Bici",
        "description_tr": (
            "Nişastadan hazırlanan jölemsi bir tatlının üzerine gül suyu şerbeti "
            "ve buzla servis edilmesiyle oluşan serinletici bir Adana sokak tatlısıdır. "
            "Yaz aylarında sokak satıcılarından sıkça tüketilir."
        ),
        "description_en": (
            "A refreshing street dessert from Adana made from starch-based jelly "
            "served with rose water syrup and ice. It is commonly enjoyed from "
            "street vendors during the hot summer months."
        ),
        "ingredients": "Nişasta, şeker, gül suyu, buz, hindistancevizi",
        "rating": 4.2,
        "city": "Adana",
        "category": "Tatlı",
    },
    # ---------- Trabzon ----------
    {
        "name": "Kuymak (Muhlama)",
        "description_tr": (
            "Mısır unu, tereyağı ve özel Trabzon peynirinin bakır bir sahanda "
            "karıştırılarak pişirilmesiyle hazırlanır. Uzayan peynir dokusu ve "
            "yoğun tereyağı aromasıyla Karadeniz'in en meşhur kahvaltılıklarından biridir."
        ),
        "description_en": (
            "A rich dish made by mixing cornmeal, butter, and local Trabzon cheese "
            "in a copper pan until the cheese melts into stretchy strings. Known for "
            "its intense butter flavor, it is one of the Black Sea region's most "
            "famous breakfast dishes."
        ),
        "ingredients": "Mısır unu, Trabzon peyniri, tereyağı, tuz",
        "rating": 4.7,
        "city": "Trabzon",
        "category": "Ana Yemek",
    },
    {
        "name": "Hamsi Tava",
        "description_tr": (
            "Karadeniz'in vazgeçilmez balığı hamsi, mısır ununa bulanarak sıcak "
            "yağda kıtır kıtır kızartılır. Yanında mısır ekmeği ve karalahana "
            "turşusuyla servis edilir. Trabzon mutfağının sembol yemeğidir."
        ),
        "description_en": (
            "The Black Sea's beloved anchovy coated in cornmeal and fried until "
            "crispy in hot oil. Served alongside corn bread and pickled collard greens, "
            "it is the signature dish of Trabzon cuisine."
        ),
        "ingredients": "Hamsi, mısır unu, tuz, sıvı yağ, limon",
        "rating": 4.6,
        "city": "Trabzon",
        "category": "Ana Yemek",
    },
    {
        "name": "Laz Böreği",
        "description_tr": (
            "İnce yufka katmanları arasına muhallebi harcı dökülerek fırında "
            "pişirilen ve üzerine pudra şekeri serpilen Trabzon'a özgü bir tatlıdır. "
            "Tatlı börek geleneğinin en güzel örneklerinden biridir."
        ),
        "description_en": (
            "A unique Trabzon dessert made of thin pastry layers filled with "
            "custard cream, baked in the oven, and sprinkled with powdered sugar. "
            "It is one of the finest examples of the sweet pastry tradition."
        ),
        "ingredients": "Yufka, süt, şeker, un, yumurta, tereyağı, pudra şekeri, vanilya",
        "rating": 4.5,
        "city": "Trabzon",
        "category": "Tatlı",
    },
    # ---------- Hatay ----------
    {
        "name": "Künefe",
        "description_tr": (
            "İnce kadayıf tellerinin arasına tuzsuz peynir konularak tereyağında "
            "pişirilen ve şerbetlenerek servis edilen Hatay'ın dünyaca ünlü tatlısıdır. "
            "Sıcak servis edilir ve üzerine Antep fıstığı serpilir."
        ),
        "description_en": (
            "A world-famous Hatay dessert made from thin shredded pastry (kadayıf) "
            "filled with unsalted cheese, cooked in butter, and soaked in syrup. "
            "It is served hot and garnished with crushed pistachios."
        ),
        "ingredients": "Kadayıf, tuzsuz peynir, tereyağı, şeker, su, limon suyu, Antep fıstığı",
        "rating": 4.9,
        "city": "Hatay",
        "category": "Tatlı",
    },
    {
        "name": "Kağıt Kebabı",
        "description_tr": (
            "Kuşbaşı et, sebzeler ve baharatların yağlı kağıda sarılarak fırında "
            "yavaş yavaş pişirilmesiyle hazırlanan geleneksel bir Hatay yemeğidir. "
            "Kağıt içinde buharla pişen et son derece yumuşak ve lezzetli olur."
        ),
        "description_en": (
            "A traditional Hatay dish made by wrapping diced meat, vegetables, "
            "and spices in parchment paper and slow-cooking in the oven. The steam "
            "cooking method inside the paper produces incredibly tender and flavorful meat."
        ),
        "ingredients": "Kuşbaşı et, domates, biber, soğan, sarımsak, baharat, yağlı kağıt",
        "rating": 4.6,
        "city": "Hatay",
        "category": "Ana Yemek",
    },
    {
        "name": "Humus",
        "description_tr": (
            "Haşlanmış nohutun tahin, limon suyu, sarımsak ve zeytinyağı ile "
            "ezilerek hazırlanan kremsi bir mezedir. Hatay'ın en bilinen "
            "başlangıç yemeklerinden biridir ve yanında pide veya lavaş ile servis edilir."
        ),
        "description_en": (
            "A creamy dip made from mashed chickpeas blended with tahini, "
            "lemon juice, garlic, and olive oil. It is one of Hatay's most "
            "well-known appetizers and is served with pita or flatbread."
        ),
        "ingredients": "Nohut, tahin, limon suyu, sarımsak, zeytinyağı, tuz, kimyon",
        "rating": 4.5,
        "city": "Hatay",
        "category": "Meze",
    },
]
