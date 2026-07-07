"""
ATLASCert® — Enerji Temel Çizgisi (EnB) Analiz ve Raporlama Portalı
===================================================================
Modül A: Veri girişi (kopyala/yapıştır ızgarası) ve değişken/dönem seçimi
Modül B: İstatistiksel analiz ve model doğrulama (IPMVP / ASHRAE Guideline 14)
Modül C: Formül çıktısı
Modül D: Kıyaslama ve performans ölçümü (CUSUM ve tasarruf)
Modül E: Raporlama ve görselleştirme
Arayüz iki dillidir (Türkçe / İngilizce); metinler modules/i18n.py içindedir.
"""

import json
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

from modules import charts, comparison, data_handler, html_report, i18n, regression, report

st.set_page_config(
    page_title="ATLASCert® EnB Portalı",
    page_icon="⚡",
    layout="wide",
)

# ---------------------------------------------------------------------------
# Baskı (PDF) düzeni: A4, her kenardan 2,5 cm boşluk. İçerik, yazdırılabilir
# 16 cm genişliğe sabitlenir; grafikler viewBox sayesinde (aşağıdaki betik)
# resim gibi oransal ölçeklenir, tablolar baskıya özel HTML kopyalarıyla
# eksiksiz basılır, başlıklar takip eden içerikten kopmaz.
# ---------------------------------------------------------------------------
st.markdown(
    """
    <style>
    /* Baskıya özel HTML tablo kopyaları ekranda gizlidir. */
    .sadece-baski { display: none; }

    @media print {
        @page { size: A4 portrait; margin: 2.5cm; }

        header[data-testid="stHeader"],
        [data-testid="stSidebar"],
        [data-testid="stToolbar"],
        [data-testid="stDecoration"],
        [data-testid="stStatusWidget"],
        .stDeployButton,
        .stAppDeployButton,
        iframe { display: none !important; }

        /* Sayfa gövdesine doğrudan eklenen görünmez ölçüm SVG'si ~9000 px
           genişliğindedir ve tarayıcının tüm sayfayı küçültmesine (dev kenar
           boşluklarına) yol açar; baskıda tamamen gizlenir. */
        body > svg { display: none !important; }

        /* İçerik A4'ün yazdırılabilir genişliğine (21 - 2 x 2,5 = 16 cm) sabitlenir;
           böylece tarayıcının öngörülemeyen "küçülterek sığdır" ölçeklemesi devreye girmez. */
        .block-container {
            width: 16cm !important;
            max-width: 16cm !important;
            padding: 0 !important;
            margin: 0 auto !important;
        }

        /* Grafikler: viewBox + aspect-ratio sayesinde kapsayıcıyla birlikte
           oransal ölçeklenir ve sayfada ortalanır. */
        .stPlotlyChart,
        .stPlotlyChart .js-plotly-plot,
        .stPlotlyChart .plot-container {
            width: 100% !important;
            max-width: 100% !important;
            margin: 0 auto !important;
        }
        .stPlotlyChart .svg-container {
            width: 100% !important;
            height: auto !important;
        }
        .stPlotlyChart svg.main-svg {
            width: 100% !important;
            height: 100% !important;
        }

        /* Ekrandaki kanvas tabanlı tablolar baskıda güvenilir çizilemez (yalnızca
           görünür satırlar işlenir); bu yüzden baskıda gizlenir ve yerlerine
           gerçek HTML kopyaları görünür. */
        [data-testid="stDataFrame"],
        [data-testid="stDataEditor"] { display: none !important; }

        .sadece-baski { display: block !important; }
        .sadece-baski table {
            width: 100%;
            border-collapse: collapse;
            font-size: 9pt;
        }
        .sadece-baski th, .sadece-baski td {
            border-bottom: 0.5pt solid #c3c2b7;
            padding: 3pt 5pt;
            text-align: left;
        }
        .sadece-baski thead { display: table-header-group; }
        .sadece-baski tr { break-inside: avoid; }
        .sadece-baski h3 {
            font-size: 13pt;
            margin: 0 0 6pt 0;
        }

        /* Yalnızca ekranda görünen başlıklar (baskıdaki kopyasıyla değiştirilir). */
        .yalniz-ekran { display: none !important; }

        /* Model formülü gibi kod blokları satır sonunda kırpılmasın, sarılsın. */
        pre, code {
            white-space: pre-wrap !important;
            word-break: break-word !important;
        }

        /* Başlıklar takip eden içerikten (grafik/tablo) kopmasın. Streamlit her
           öğeyi ayrı kapsayıcıya sardığı için kural, başlığı içeren kapsayıcıya
           uygulanır. */
        h1, h2, h3, h4,
        [data-testid="stHeading"],
        [data-testid="stElementContainer"]:has([data-testid="stHeading"]),
        [data-testid="stElementContainer"]:has(h1, h2, h3, h4) {
            break-after: avoid-page !important;
            break-inside: avoid !important;
        }

        /* Grafikler, metrik kartları ve paneller sayfa sonunda ikiye bölünmesin. */
        .stPlotlyChart,
        [data-testid="stMetric"],
        [data-testid="stExpander"] {
            break-inside: avoid !important;
            page-break-inside: avoid !important;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Plotly SVG'lerine viewBox ekleyen betik: baskıda (PDF) grafiklerin bir resim
# gibi oransal ölçeklenmesini sağlar; ekran görünümünü değiştirmez.
components.html(
    """
    <script>
    (function () {
        const P = window.parent;
        if (P.__atlasCizimOlcekleme) { return; }
        P.__atlasCizimOlcekleme = true;

        const uygula = () => {
            P.document.querySelectorAll('.stPlotlyChart svg.main-svg').forEach((svg) => {
                const w = parseFloat(svg.getAttribute('width'));
                const h = parseFloat(svg.getAttribute('height'));
                if (!w || !h) { return; }
                const vb = '0 0 ' + w + ' ' + h;
                if (svg.getAttribute('viewBox') !== vb) {
                    svg.setAttribute('viewBox', vb);
                    svg.setAttribute('preserveAspectRatio', 'xMidYMid meet');
                }
                const kap = svg.closest('.svg-container');
                if (kap) { kap.style.aspectRatio = w + ' / ' + h; }
            });
        };

        uygula();
        new P.MutationObserver(uygula).observe(P.document.body, { childList: true, subtree: true });
        P.addEventListener('resize', () => setTimeout(uygula, 400));
    })();
    </script>
    """,
    height=0,
)

# ---------------------------------------------------------------------------
# Kayıt sistemi: yerel kurulumda analizler "kayitlar" klasörüne JSON olarak
# kaydedilir ve listeden seçilerek geri yüklenir. Bulut dağıtımında (Streamlit
# Community Cloud) sunucu diski geçicidir ve tüm ziyaretçiler için ortaktır;
# bu yüzden kayıtlar sunucuya yazılmaz, kullanıcının bilgisayarına JSON olarak
# indirilir ve dosya yüklenerek geri açılır. Yükleme, bileşen durumlarını
# değiştirdiği için mutlaka hiçbir bileşen çizilmeden ÖNCE (burada) işlenmelidir.
# ---------------------------------------------------------------------------
BULUT_MODU = Path("/mount/src").exists()  # Streamlit Community Cloud imzası
SURUM = "1.1.1"

KAYIT_KLASORU = Path(__file__).parent / "kayitlar"
if not BULUT_MODU:
    KAYIT_KLASORU.mkdir(exist_ok=True)


def kayit_yukle(kayit, ad):
    """Sözlük olarak verilen kaydı okuyup tüm giriş durumlarını geri yükler."""
    ss = st.session_state
    kayit_dili = kayit.get("dil", "tr")
    kayit_metinleri = i18n.METINLER.get(kayit_dili, i18n.METINLER["tr"])
    ss["dil_secimi"] = "English" if kayit_dili == "en" else "Türkçe"

    a = kayit.get("ayarlar", {})
    ss[f"tuketim_adi_{kayit_dili}"] = a.get("tuketim_adi", kayit_metinleri["tuketim_varsayilan"])
    ss["degisken_sayisi"] = int(a.get("degisken_sayisi", 2))
    for i, degisken_ad in enumerate(a.get("degisken_adlari", [])):
        ss[f"degisken_adi_{kayit_dili}_{i}"] = degisken_ad
    for anahtar in ("bas_ay", "bas_yil", "bit_ay", "bit_yil"):
        if a.get(anahtar) is not None:
            ss[anahtar] = int(a[anahtar])
    for anahtar in ("rap_bas_ay", "rap_bas_yil", "rap_bit_ay", "rap_bit_yil"):
        if a.get(anahtar) is not None:
            ss[anahtar] = int(a[anahtar])
    if a.get("referans") is not None:
        ss["referans_slideri"] = int(a["referans"])

    for depo_adi in ("ana_depo", "rap_depo"):
        depo = kayit.get(depo_adi)
        if depo:
            ss[depo_adi] = pd.DataFrame(depo["veri"], columns=depo["sutunlar"])
        # Izgaraların yüklenen depodan yeniden kurulmasını zorla.
        ss.pop(depo_adi + "_imza", None)
        ss.pop(depo_adi + "_girdi", None)

    ss["_kayit_yuklendi"] = ad


# "Aç" düğmesi / dosya yükleyici yalnızca bekleyen yükleme isteği bırakır;
# asıl yükleme burada, tüm bileşenlerden önce gerçekleşir.
if "_bekleyen_kayit" in st.session_state:
    yol = Path(st.session_state.pop("_bekleyen_kayit"))
    try:
        kayit_yukle(json.loads(yol.read_text(encoding="utf-8")), yol.stem)
    except Exception as e:
        st.session_state["_kayit_hatasi"] = str(e)

if "_bekleyen_kayit_metni" in st.session_state:
    bekleyen = st.session_state.pop("_bekleyen_kayit_metni")
    try:
        kayit_yukle(json.loads(bekleyen["icerik"]), bekleyen["ad"])
    except Exception as e:
        st.session_state["_kayit_hatasi"] = str(e)

# ---------------------------------------------------------------------------
# Üst satır: Logo | Başlık | Dil seçimi (dikeyde ortalanmış)
# ---------------------------------------------------------------------------
@st.cache_data
def logo_svg():
    """Kurumsal logoyu (UTF-16 kodlu SVG) okuyup st.image'ın beklediği biçime getirir."""
    yol = Path(__file__).parent / "img" / "Logo_01.svg"
    try:
        ham = yol.read_text(encoding="utf-16")
    except UnicodeError:
        ham = yol.read_text(encoding="utf-8")
    return ham[ham.find("<svg"):]


logo_col, baslik_col, dil_col = st.columns([1.5, 4.7, 1.1], vertical_alignment="center")
with dil_col:
    dil_secim = st.selectbox("Dil / Language", options=["Türkçe", "English"], key="dil_secimi")
dil = "en" if dil_secim == "English" else "tr"
M = i18n.METINLER[dil]

with logo_col:
    st.image(logo_svg(), use_container_width=True)
with baslik_col:
    st.title(M["portal_basligi"])
st.caption(M["alt_baslik"])

st.info(M["uyku_uyari"])

st.divider()

# ---------------------------------------------------------------------------
# Kalıcı widget durumları: dil değişse, kayıt açılsa veya sütunlar değişse bile
# girişler kaybolmasın diye tüm bileşenler anahtarlıdır ve varsayılanları
# burada tohumlanır (bileşen oluşturulmadan önce).
# ---------------------------------------------------------------------------
st.session_state.setdefault("bas_ay", 1)
st.session_state.setdefault("bas_yil", 2025)
st.session_state.setdefault("bit_ay", 12)
st.session_state.setdefault("bit_yil", 2025)
st.session_state.setdefault("degisken_sayisi", 2)
st.session_state.setdefault(f"tuketim_adi_{dil}", M["tuketim_varsayilan"])

def kayit_verisi_olustur(ad):
    """
    Mevcut oturumdaki tüm girişleri JSON kayıt metnine çevirir.
    Dönüş: (guvenli_ad, json_metni) — diske yazma çağıranın sorumluluğundadır.
    """
    ss = st.session_state
    adet = int(ss.get("degisken_sayisi", 2))
    ayarlar = {
        "tuketim_adi": ss.get(f"tuketim_adi_{dil}", M["tuketim_varsayilan"]),
        "degisken_sayisi": adet,
        "degisken_adlari": [
            ss.get(f"degisken_adi_{dil}_{i}", M["degisken_varsayilan"].format(i=i + 1))
            for i in range(adet)
        ],
        "bas_ay": int(ss.get("bas_ay", 1)),
        "bas_yil": int(ss.get("bas_yil", 2025)),
        "bit_ay": int(ss.get("bit_ay", 12)),
        "bit_yil": int(ss.get("bit_yil", 2025)),
        "rap_bas_ay": ss.get("rap_bas_ay"),
        "rap_bas_yil": ss.get("rap_bas_yil"),
        "rap_bit_ay": ss.get("rap_bit_ay"),
        "rap_bit_yil": ss.get("rap_bit_yil"),
        "referans": ss.get("referans_slideri"),
    }
    kayit = {
        "surum": 1,
        "tarih": datetime.now().isoformat(timespec="seconds"),
        "dil": dil,
        "ayarlar": ayarlar,
    }
    for depo_adi in ("ana_depo", "rap_depo"):
        depo = ss.get(depo_adi)
        kayit[depo_adi] = (
            None if depo is None
            else {"sutunlar": list(depo.columns), "veri": depo.astype(str).values.tolist()}
        )

    guvenli_ad = "".join(c for c in ad if c.isalnum() or c in " -_()").strip() or "kayit"
    return guvenli_ad, json.dumps(kayit, ensure_ascii=False, indent=1)


def kayitlar_paneli(konum):
    """
    Kaydet / Aç panelini çizer. Panel hem sayfanın başında hem sonunda yer
    aldığı için tüm bileşen anahtarları 'konum' ile ayrıştırılır.

    Bulutta kayıt iki aşamalıdır: önce Kaydet'e basılır (o anki tüm veriden
    JSON üretilip oturum durumuna konur), ardından beliren düğmeyle indirilir.
    JSON'un indirme düğmesi çizilirken değil, Kaydet tıklandığında üretilmesi
    önemlidir: indirme düğmesi tıklandığında betik yeniden çalışmaz, son
    hazırlanan yükü verir — yük panelde (veri tabloları depoya yazılmadan
    önce) üretilseydi eksik/boş kayıt inerdi.
    """
    with st.expander(M["kayitlar_expander"], expanded=False):
        if BULUT_MODU:
            st.caption(M["kayit_bulut_bilgi"])
        kayit_col1, kayit_col2 = st.columns(2)
        with kayit_col1:
            kayit_adi = st.text_input(M["kayit_adi_label"], key=f"kayit_adi_{konum}")
            if st.button(M["kaydet_btn"], key=f"kaydet_dugmesi_{konum}"):
                if not kayit_adi.strip():
                    st.warning(M["kayit_adi_bos"])
                else:
                    try:
                        yazilan_ad, kayit_json = kayit_verisi_olustur(kayit_adi)
                        if BULUT_MODU:
                            st.session_state["_kayit_json"] = kayit_json.encode("utf-8")
                            st.session_state["_kayit_json_adi"] = yazilan_ad
                        else:
                            (KAYIT_KLASORU / f"{yazilan_ad}.json").write_text(
                                kayit_json, encoding="utf-8"
                            )
                        st.success(M["kayit_ok"].format(ad=yazilan_ad))
                    except Exception as e:
                        st.error(M["kayit_hata"].format(hata=e))
            if BULUT_MODU and st.session_state.get("_kayit_json"):
                st.download_button(
                    M["kayit_indir_btn"],
                    data=st.session_state["_kayit_json"],
                    file_name=f"{st.session_state['_kayit_json_adi']}.json",
                    mime="application/json",
                    key=f"kayit_indir_dugmesi_{konum}",
                )
        with kayit_col2:
            if BULUT_MODU:
                yuklenen_kayit = st.file_uploader(
                    M["kayit_yukle_label"], type=["json"], key=f"kayit_dosyasi_{konum}"
                )
                if yuklenen_kayit is not None:
                    # Aynı dosya her çalıştırmada yeniden yüklenmesin diye imzalanır;
                    # file_id her yükleme işleminde değişir, böylece aynı dosyanın
                    # yeniden yüklenmesi de kaydı tekrar açar.
                    imza = getattr(yuklenen_kayit, "file_id", None) or (
                        yuklenen_kayit.name, yuklenen_kayit.size
                    )
                    if st.session_state.get("_islenen_kayit_imzasi") != imza:
                        st.session_state["_islenen_kayit_imzasi"] = imza
                        st.session_state["_bekleyen_kayit_metni"] = {
                            "ad": Path(yuklenen_kayit.name).stem,
                            "icerik": yuklenen_kayit.getvalue().decode("utf-8"),
                        }
                        st.rerun()
            else:
                kayit_dosyalari = sorted(
                    KAYIT_KLASORU.glob("*.json"), key=lambda p: p.stat().st_mtime, reverse=True
                )
                if not kayit_dosyalari:
                    st.caption(M["kayit_yok"])
                else:
                    secilen_kayit = st.selectbox(
                        M["kayit_sec_label"],
                        options=kayit_dosyalari,
                        format_func=lambda p: p.stem,
                        key=f"kayit_secimi_{konum}",
                    )
                    if st.button(M["ac_btn"], key=f"ac_dugmesi_{konum}"):
                        # Yükleme bir sonraki çalıştırmanın başında, bileşenler
                        # çizilmeden önce yapılır (bkz. _bekleyen_kayit işleme bloğu).
                        st.session_state["_bekleyen_kayit"] = str(secilen_kayit)
                        st.rerun()


kayitlar_paneli("ust")

if "_kayit_yuklendi" in st.session_state:
    st.success(M["kayit_yuklendi"].format(ad=st.session_state.pop("_kayit_yuklendi")))
if "_kayit_hatasi" in st.session_state:
    st.error(M["kayit_hata"].format(hata=st.session_state.pop("_kayit_hatasi")))


def izgara_yuksekligi(satir_sayisi):
    """Tablonun iç kaydırma çubuğu olmadan tüm satırları göstermesi için gereken yükseklik (px)."""
    return int(35 * (satir_sayisi + 1) + 3)


def baski_tablosu(tablo_df, baslik=None):
    """
    Ekrandaki kanvas tabanlı tablonun, yalnızca baskıda (PDF) görünen gerçek
    HTML kopyasını üretir; böylece PDF'te tüm satırlar eksiksiz yer alır.
    Başlık verilirse tabloyla aynı blokta basılır ve başlık tablodan kopmaz.
    """
    baslik_html = f"<h3>{baslik}</h3>" if baslik else ""
    st.markdown(
        "<div class='sadece-baski'>"
        + baslik_html
        + tablo_df.to_html(index=False, border=0, float_format=lambda v: f"{v:,.2f}")
        + "</div>",
        unsafe_allow_html=True,
    )


def csv_indirme_dugmesi(tablo_df, dosya_adi, anahtar):
    """
    Tabloyu Türkçe Excel'in doğrudan sütunlara ayırdığı biçimde (';' ayraçlı,
    ',' ondalıklı, UTF-8 BOM'lu) CSV olarak indiren düğme. Streamlit'in yerleşik
    tablo dışa aktarımı virgül ayraçlı olduğundan Türkçe Excel'de tek sütuna
    yığılır; bu düğme onun yerine kullanılır.
    """
    st.download_button(
        M["csv_indir"],
        data=tablo_df.to_csv(index=False, sep=";", decimal=",").encode("utf-8-sig"),
        file_name=dosya_adi,
        mime="text/csv",
        key=anahtar,
    )


def kalici_izgara(depo_adi, etiketler, veri_sutunlari, yukseklik, kolon_ayarlari=None):
    """
    Girilen değerleri st.session_state deposunda konumsal olarak saklayan veri
    ızgarası. Dil, sütun adı, değişken sayısı veya dönem aralığı değişse bile
    girilmiş veriler kaybolmaz (azaltılan değişken/dönem verileri de depoda
    saklı kalır; geri artırıldığında geri gelir).

    Önemli: Düzenleyiciye, yapı (dil/sütun/aralık) değişmediği sürece her
    çalıştırmada AYNI girdi verilir. Girdi her seferinde depodan yeniden
    kurulursa Streamlit bekleyen düzenlemeleri sıfırlar ve ilk yapıştırma /
    ilk hücre düzenlemesi "geri dönmüş" gibi görünür.
    """
    n = len(etiketler)
    k = len(veri_sutunlari)

    depo = st.session_state.get(depo_adi)
    if depo is None:
        depo = pd.DataFrame("", index=range(n), columns=[f"_v{i}" for i in range(k)])
    if len(depo) < n:
        depo = depo.reindex(index=range(n), fill_value="")
    for i in range(k):
        if f"_v{i}" not in depo.columns:
            depo[f"_v{i}"] = ""
    depo = depo.fillna("")
    st.session_state[depo_adi] = depo

    # Yapı imzası: değişirse (ve yalnızca o zaman) düzenleyici girdisi depodan
    # yeniden kurulur ve düzenleyici yeni bir anahtar ile tazelenir.
    imza = f"{dil}|{n}|{k}|" + "|".join(veri_sutunlari) + f"|{etiketler[0]}|{etiketler[-1]}"
    imza_anahtari = depo_adi + "_imza"
    girdi_anahtari = depo_adi + "_girdi"

    if st.session_state.get(imza_anahtari) != imza:
        gosterim = pd.DataFrame({M["donem"]: list(etiketler)})
        for i, ad in enumerate(veri_sutunlari):
            gosterim[ad] = depo[f"_v{i}"].astype(str).iloc[:n].values
        st.session_state[girdi_anahtari] = gosterim
        st.session_state[imza_anahtari] = imza
        # Yeni anahtar üretilsin ki eski düzenleme durumu taze girdinin üstüne binmesin.
        st.session_state[depo_adi + "_nonce"] = st.session_state.get(depo_adi + "_nonce", 0) + 1

    duzenlenen = st.data_editor(
        st.session_state[girdi_anahtari],
        num_rows="fixed",
        disabled=[M["donem"]],
        hide_index=True,
        height=yukseklik,
        use_container_width=True,
        key=f"{depo_adi}_{st.session_state.get(depo_adi + '_nonce', 0)}_" + imza,
        column_config=kolon_ayarlari,
    )

    # Düzenlenen değerler depoya konumsal olarak geri yazılır (kaydet/aç ve
    # yapı değişimlerinde veri kaynağı bu depodur).
    for i, ad in enumerate(veri_sutunlari):
        temiz = duzenlenen[ad].fillna("").astype(str).replace({"None": "", "nan": "", "<NA>": ""})
        depo.loc[:n - 1, f"_v{i}"] = temiz.values
    st.session_state[depo_adi] = depo

    return duzenlenen


def koyu_tema_mi():
    """Kullanıcının Streamlit temasını algılar; koyu temada True döner."""
    try:
        return st.context.theme.type == "dark"
    except Exception:
        return False


KOYU_TEMA = koyu_tema_mi()

# ---------------------------------------------------------------------------
# 1. Veri Girişi (Modül A)
# ---------------------------------------------------------------------------
st.header(M["b1"])
st.markdown(M["giris_aciklama"])

with st.expander(M["sutun_ozellestir"], expanded=False):
    st.caption(M["sutun_ipucu"])
    ayar_col1, ayar_col2 = st.columns(2)
    tuketim_adi = ayar_col1.text_input(M["tuketim_sutun_label"], key=f"tuketim_adi_{dil}")
    degisken_sayisi = int(ayar_col2.number_input(
        M["degisken_sayisi_label"], min_value=1, max_value=4, step=1, key="degisken_sayisi"
    ))

    isim_kolonlari = st.columns(degisken_sayisi)
    degisken_adlari = []
    for i in range(degisken_sayisi):
        st.session_state.setdefault(f"degisken_adi_{dil}_{i}", M["degisken_varsayilan"].format(i=i + 1))
        degisken_adlari.append(
            isim_kolonlari[i].text_input(
                M["degisken_adi_label"].format(i=i + 1),
                key=f"degisken_adi_{dil}_{i}",
            )
        )

st.markdown(M["aralik_baslik"])
aralik_col1, aralik_col2, aralik_col3, aralik_col4 = st.columns(4)
bas_ay = aralik_col1.selectbox(
    M["bas_ay"],
    options=list(range(1, 13)),
    format_func=lambda i: M["aylar"][i - 1],
    key="bas_ay",
)
bas_yil = int(aralik_col2.number_input(M["bas_yil"], min_value=2000, max_value=2100, key="bas_yil"))
bit_ay = aralik_col3.selectbox(
    M["bit_ay"],
    options=list(range(1, 13)),
    format_func=lambda i: M["aylar"][i - 1],
    key="bit_ay",
)
bit_yil = int(aralik_col4.number_input(M["bit_yil"], min_value=2000, max_value=2100, key="bit_yil"))

donem_adedi = data_handler.ay_farki(bas_ay, bas_yil, bit_ay, bit_yil)
if donem_adedi < 1:
    st.info(M["ters_aralik"])
    st.stop()

grid_sutunlari = [M["donem"], tuketim_adi] + degisken_adlari

if len(set(grid_sutunlari)) != len(grid_sutunlari):
    st.error(M["ayni_ad_hatasi"])
    st.stop()

with st.expander(M["alternatif_expander"], expanded=False):
    uploaded_file = st.file_uploader(
        M["dosya_upload_label"],
        type=["csv", "xlsx", "xls"],
        key="opsiyonel_dosya",
    )

df = None
y_col = None
x_cols = []
donem_col = None

# Gizli örnek veri modu (?demo=1): baskı düzeni ve grafiklerin uçtan uca
# doğrulanması için sentetik 24 aylık veri üretir.
demo_modu = st.query_params.get("demo") == "1"

if demo_modu:
    st.info(M["demo_bilgi"])
    ay_sayisi = 24
    bas_ay, bas_yil, bit_ay, bit_yil = 1, 2025, 12, 2026
    demo_etiketler = data_handler.generate_period_labels(bas_ay, bas_yil, ay_sayisi, aylar=M["aylar"])
    rng = np.random.default_rng(42)
    demo_uretim = np.round(rng.uniform(80, 120, ay_sayisi), 1)
    demo_hdd = np.round(rng.uniform(0, 400, ay_sayisi), 0)
    demo_tuketim = 2000 + 30 * demo_uretim + 5 * demo_hdd + rng.normal(0, 120, ay_sayisi)
    demo_tuketim[12:] *= 0.88  # raporlama döneminde ~%12 tasarruf simüle edilir

    df = pd.DataFrame({
        M["donem"]: demo_etiketler,
        tuketim_adi: np.round(demo_tuketim, 1),
        degisken_adlari[0]: demo_uretim,
    })
    if len(degisken_adlari) > 1:
        df[degisken_adlari[1]] = demo_hdd

    y_col = tuketim_adi
    x_cols = list(df.columns[2:])
    donem_col = M["donem"]
elif uploaded_file is not None:
    df, hata = data_handler.load_data(uploaded_file, m=M)
    if hata:
        st.error(hata)
        st.stop()

    st.success(M["dosya_okundu"].format(satir=df.shape[0], sutun=df.shape[1]))

    tum_sutunlar = list(df.columns)
    sec_col1, sec_col2 = st.columns(2)
    with sec_col1:
        y_col = st.selectbox(
            M["y_label"],
            options=[None] + tum_sutunlar,
            format_func=lambda x: M["seciniz"] if x is None else x,
        )
    with sec_col2:
        x_cols = st.multiselect(
            M["x_label"],
            options=[c for c in tum_sutunlar if c != y_col],
        )
    donem_col = st.selectbox(
        M["donem_sutun_label"],
        options=[None] + [c for c in tum_sutunlar if c not in [y_col] + x_cols],
        format_func=lambda x: M["donem_yok"] if x is None else x,
    )
else:
    ana_etiketler = data_handler.generate_period_labels(bas_ay, bas_yil, donem_adedi, aylar=M["aylar"])
    st.caption(M["secilen_aralik"].format(ilk=ana_etiketler[0], son=ana_etiketler[-1], adet=donem_adedi))

    girdi_df = kalici_izgara(
        "ana_depo",
        ana_etiketler,
        [tuketim_adi] + degisken_adlari,
        izgara_yuksekligi(donem_adedi),
        kolon_ayarlari={
            M["donem"]: st.column_config.TextColumn(M["donem"], help=M["donem_help"]),
            tuketim_adi: st.column_config.TextColumn(tuketim_adi, help=M["tuketim_help"]),
            **{
                ad: st.column_config.TextColumn(ad, help=M["degisken_help"])
                for ad in degisken_adlari
            },
        },
    )

    df = girdi_df
    y_col = tuketim_adi
    donem_col = M["donem"]

    x_cols = st.multiselect(
        M["x_model_label"],
        options=degisken_adlari,
        default=degisken_adlari,
    )

gecerli, mesaj = data_handler.validate_selection(df, y_col, x_cols, m=M)
if not gecerli:
    st.info(mesaj)
    st.stop()

# Ham tüketim modu: hiç bağımsız değişken seçilmediyse referans dönemi
# ortalaması temel çizgi kabul edilir; kıyaslama ve grafikler aynen çalışır.
ham_mod = len(x_cols) == 0
ham_ort = 0.0
ham_harita = {}
aylik_mod = False
if ham_mod:
    st.info(M["ham_mod_uyari"])

secili_sutunlar = [y_col] + x_cols
temiz_df_tum, uyarilar = data_handler.clean_numeric_columns(df, secili_sutunlar, m=M)

for uyari in uyarilar:
    st.warning(uyari)

if temiz_df_tum.empty:
    st.info(M["veri_bekleniyor"])
    st.stop()

baski_tablosu(temiz_df_tum)
csv_indirme_dugmesi(temiz_df_tum, M["csv_giris_dosya"], "csv_giris_dugmesi")


def donem_etiketleri_uret(alt_df, baslangic=1):
    """Dönem sütunu boşsa veya seçilmemişse otomatik 'Dönem N' etiketleri üretir."""
    if donem_col is not None and donem_col in alt_df.columns:
        etiketler = alt_df[donem_col].astype(str).tolist()
        return [
            e if e.strip() and e.strip().lower() != "nan" else M["donem_etiket"].format(n=baslangic + i)
            for i, e in enumerate(etiketler)
        ]
    return [M["donem_etiket"].format(n=i) for i in range(baslangic, baslangic + len(alt_df))]


st.divider()

# ---------------------------------------------------------------------------
# 2. Referans (Baseline) Dönemi Aralığı (Modül A)
# ---------------------------------------------------------------------------
st.header(M["b2"])

toplam_satir = len(temiz_df_tum)
min_referans = len(x_cols) + 2

if toplam_satir < min_referans:
    st.info(M["yetersiz_veri"].format(satir=toplam_satir, kx=len(x_cols), min_ref=min_referans))
    st.stop()

referans_varsayilan = max(min_referans, 12) if demo_modu and toplam_satir >= 12 else toplam_satir
mevcut_referans = st.session_state.get("referans_slideri", referans_varsayilan)
st.session_state["referans_slideri"] = int(min(max(mevcut_referans, min_referans), toplam_satir))

referans_sayisi = st.slider(
    M["slider_label"],
    min_value=min_referans,
    max_value=toplam_satir,
    key="referans_slideri",
    help=M["slider_help"].format(min_ref=min_referans, kx=len(x_cols)),
)

referans_df = temiz_df_tum.iloc[:referans_sayisi].reset_index(drop=True)
raporlama_hazir_df = temiz_df_tum.iloc[referans_sayisi:].reset_index(drop=True)

st.caption(M["referans_caption"].format(ref=len(referans_df), kalan=len(raporlama_hazir_df)))

st.divider()

# ---------------------------------------------------------------------------
# 3. İstatistiksel Analiz ve Model Doğrulama (Modül B)
# ---------------------------------------------------------------------------
st.header(M["b3"])

if ham_mod:
    referans_degerler = referans_df[y_col].astype(float)
    ham_ort = float(referans_degerler.mean())
    ham_std = float(referans_degerler.std(ddof=1)) if len(referans_degerler) > 1 else 0.0
    ham_cv = ham_std / ham_ort if ham_ort != 0 else float("nan")

    model = None
    model_uygun_mu = True
    anlamsiz_degiskenler = []

    # Aylık eşleştirme yalnızca dönem etiketleri mevcutsa mümkündür.
    aylik_mumkun = donem_col is not None and donem_col in referans_df.columns
    if aylik_mumkun:
        ham_yontem = st.radio(
            M["ham_yontem_label"],
            options=[M["ham_yontem_aylik"], M["ham_yontem_ortalama"]],
            horizontal=True,
            help=M["ham_yontem_help"],
        )
        aylik_mod = ham_yontem == M["ham_yontem_aylik"]
    else:
        aylik_mod = False

    ham_harita = (
        comparison.monthly_baseline_map(referans_df, donem_col, y_col) if aylik_mod else {}
    )

    ham_col1, ham_col2, ham_col3, ham_col4 = st.columns(4)
    ham_col1.metric(M["ort_metric"], f"{ham_ort:,.2f}")
    ham_col2.metric(M["std_metric"], f"{ham_std:,.2f}")
    ham_col3.metric(
        M["cv_ham_metric"],
        f"%{ham_cv * 100:.2f}" if ham_cv == ham_cv else "—",
    )
    ham_col4.metric(M["gozlem_metric"], f"{len(referans_degerler)}")

    kriterler_df = pd.DataFrame([
        {M["olcut"]: M["ort_metric"], M["hesaplanan"]: f"{ham_ort:,.2f}"},
        {M["olcut"]: M["std_metric"], M["hesaplanan"]: f"{ham_std:,.2f}"},
        {M["olcut"]: M["cv_ham_metric"],
         M["hesaplanan"]: f"%{ham_cv * 100:.2f}" if ham_cv == ham_cv else "—"},
        {M["olcut"]: M["gozlem_metric"], M["hesaplanan"]: f"{len(referans_degerler)}"},
    ])
    baski_tablosu(kriterler_df, baslik=M["ham_ozet_baslik"])

    if aylik_mod and ham_harita:
        # Ay bazında temel çizgi tablosu (takvim sırasıyla)
        aylik_satirlar = [
            {M["ay_kolonu"]: ay, M["ort_metric"]: f"{ham_harita[ay.lower()]:,.2f}"}
            for ay in M["aylar"] if ay.lower() in ham_harita
        ]
        aylik_df = pd.DataFrame(aylik_satirlar)
        st.dataframe(aylik_df, use_container_width=True, hide_index=True)
        baski_tablosu(aylik_df)
else:
    try:
        model = regression.run_regression(referans_df, y_col, x_cols)
    except Exception as e:
        st.error(M["regresyon_hatasi"].format(hata=e))
        st.stop()

    metrics = regression.calculate_metrics(model, referans_df, y_col, x_cols)
    kriterler, model_uygun_mu, anlamsiz_degiskenler = regression.evaluate_model(metrics, m=M)
    kriterler_df = pd.DataFrame(kriterler)

    metrik_col1, metrik_col2, metrik_col3, metrik_col4 = st.columns(4)
    metrik_col1.metric(
        M["r2_metric"],
        f"{metrics['r2']:.3f}",
        help=M["r2_help"].format(esik=regression.ESIK_R2),
    )
    metrik_col2.metric(
        M["adjr2_metric"],
        f"{metrics['adj_r2']:.3f}",
        help=M["adjr2_help"],
    )
    metrik_col3.metric(
        M["cv_metric"],
        f"%{metrics['cv_rmse'] * 100:.2f}" if not np.isnan(metrics["cv_rmse"]) else "—",
        help=M["cv_help"].format(esik=f"{regression.ESIK_CV_RMSE * 100:.0f}"),
    )
    metrik_col4.metric(
        M["fp_metric"],
        f"{metrics['f_pdegeri']:.4f}",
        help=M["fp_help"].format(esik=regression.ESIK_F_PDEGERI),
    )

    with st.expander(M["ayrintili_expander"], expanded=False):
        st.dataframe(kriterler_df, use_container_width=True, hide_index=True)

    baski_tablosu(kriterler_df)

    if anlamsiz_degiskenler:
        st.warning(M["anlamsiz_uyari"].format(degiskenler=", ".join(anlamsiz_degiskenler)))

    if model_uygun_mu:
        st.success(M["model_uygun"])
    else:
        st.error(M["model_uygun_degil"])
        st.info(M["ham_mod_oneri"])

st.divider()

# ---------------------------------------------------------------------------
# 4. Model Formülü ve Katsayılar (Modül C)
# ---------------------------------------------------------------------------
st.header(M["b4"])

if ham_mod:
    if aylik_mod:
        formul = M["ham_formul_aylik"].format(y=y_col)
        katsayilar_df = pd.DataFrame([
            {M["ay_kolonu"]: ay, M["ort_metric"]: f"{ham_harita[ay.lower()]:,.2f}"}
            for ay in M["aylar"] if ay.lower() in ham_harita
        ])
    else:
        formul = M["ham_formul"].format(y=y_col, ort=f"{ham_ort:,.2f}")
        katsayilar_df = pd.DataFrame([{
            M["katsayi_degisken"]: M["temel_cizgi_ort"],
            M["katsayi"]: f"{ham_ort:.4f}",
            M["p_degeri"]: "—",
        }])

    st.code(formul, language=None)
    st.dataframe(katsayilar_df, use_container_width=True, hide_index=True)
    baski_tablosu(katsayilar_df)
else:
    formul = regression.get_formula_string(model, y_col, x_cols)
    st.code(formul, language=None)

    katsayilar_df = regression.get_katsayilar_tablosu(model, x_cols, m=M)
    st.dataframe(katsayilar_df, use_container_width=True, hide_index=True)
    baski_tablosu(katsayilar_df)

    if not model_uygun_mu:
        st.info(M["temkin_bilgi"])

st.divider()

# ---------------------------------------------------------------------------
# 5. Raporlama (Kıyaslama) Dönemi Verisi (Modül D)
# ---------------------------------------------------------------------------
st.header(M["b5"])

kaynak_secenekleri = []
if not raporlama_hazir_df.empty:
    kaynak_secenekleri.append(M["kaynak_ayni"])
kaynak_secenekleri.append(M["kaynak_ayri"])

kaynak = st.radio(M["kaynak_label"], options=kaynak_secenekleri, horizontal=True)

raporlama_df = None
donem_etiketleri = []

if kaynak == M["kaynak_ayni"]:
    raporlama_df = raporlama_hazir_df
    donem_etiketleri = donem_etiketleri_uret(raporlama_df, baslangic=referans_sayisi + 1)
else:
    x_listesi = ", ".join(f"**{x}**" for x in x_cols)

    if uploaded_file is None:
        st.markdown(M["rap_aciklama"].format(y=y_col, xler=x_listesi))

        vars_bas_ay, vars_bas_yil = data_handler.ay_yil_ekle(bit_ay, bit_yil, 1)
        vars_bit_ay, vars_bit_yil = data_handler.ay_yil_ekle(vars_bas_ay, vars_bas_yil, 11)
        st.session_state.setdefault("rap_bas_ay", vars_bas_ay)
        st.session_state.setdefault("rap_bas_yil", vars_bas_yil)
        st.session_state.setdefault("rap_bit_ay", vars_bit_ay)
        st.session_state.setdefault("rap_bit_yil", vars_bit_yil)

        rap_col1, rap_col2, rap_col3, rap_col4 = st.columns(4)
        rap_bas_ay = rap_col1.selectbox(
            M["bas_ay"],
            options=list(range(1, 13)),
            format_func=lambda i: M["aylar"][i - 1],
            key="rap_bas_ay",
        )
        rap_bas_yil = int(rap_col2.number_input(
            M["bas_yil"], min_value=2000, max_value=2100, key="rap_bas_yil"
        ))
        rap_bit_ay = rap_col3.selectbox(
            M["bit_ay"],
            options=list(range(1, 13)),
            format_func=lambda i: M["aylar"][i - 1],
            key="rap_bit_ay",
        )
        rap_bit_yil = int(rap_col4.number_input(
            M["bit_yil"], min_value=2000, max_value=2100, key="rap_bit_yil"
        ))

        rap_adedi = data_handler.ay_farki(rap_bas_ay, rap_bas_yil, rap_bit_ay, rap_bit_yil)
        if rap_adedi < 1:
            st.info(M["ters_aralik"])
            st.stop()

        rap_etiketler = data_handler.generate_period_labels(
            rap_bas_ay, rap_bas_yil, rap_adedi, aylar=M["aylar"]
        )
        rap_girdi = kalici_izgara(
            "rap_depo",
            rap_etiketler,
            [y_col] + x_cols,
            izgara_yuksekligi(rap_adedi),
        )
    else:
        st.markdown(M["rap_aciklama_dosya"].format(donem=M["donem"], y=y_col, xler=x_listesi))
        rap_sutunlar = [M["donem"], y_col] + x_cols
        rap_sablon = data_handler.create_empty_grid(rap_sutunlar, satir_sayisi=12)
        rap_girdi = st.data_editor(
            rap_sablon,
            num_rows="dynamic",
            use_container_width=True,
            key=f"raporlama_grid_{dil}_" + "|".join(rap_sutunlar),
        )

    raporlama_df, rap_uyarilar = data_handler.clean_numeric_columns(rap_girdi, [y_col] + x_cols, m=M)
    for uyari in rap_uyarilar:
        st.warning(uyari)

    if raporlama_df is not None and not raporlama_df.empty:
        baski_tablosu(raporlama_df)

    if not raporlama_df.empty:
        # Ayrı tablo akışında dönem etiketleri her zaman ızgaranın Dönem sütunundan alınır.
        donem_etiketleri = [
            e if e.strip() and e.strip().lower() != "nan" else M["donem_etiket"].format(n=i + 1)
            for i, e in enumerate(raporlama_df[M["donem"]].astype(str).tolist())
        ] if M["donem"] in raporlama_df.columns else [
            M["donem_etiket"].format(n=i + 1) for i in range(len(raporlama_df))
        ]

if raporlama_df is None or raporlama_df.empty:
    st.info(M["rap_bekleniyor"])
    st.stop()

# ---------------------------------------------------------------------------
# 6. Kıyaslama Tablosu ve CUSUM (Modül D)
# ---------------------------------------------------------------------------
if ham_mod:
    if aylik_mod:
        beklenen_tuketim = comparison.expected_from_monthly(donem_etiketleri, ham_harita, ham_ort)
    else:
        beklenen_tuketim = np.full(len(raporlama_df), ham_ort)
else:
    beklenen_tuketim = comparison.calculate_expected_consumption(model, raporlama_df, x_cols)
gercek_tuketim = raporlama_df[y_col].astype(float).values

kiyaslama_tablosu = comparison.build_comparison_table(
    donem_etiketleri, gercek_tuketim, beklenen_tuketim, m=M
)
ozet = comparison.summarize_savings(kiyaslama_tablosu, m=M)

st.markdown(f'<h3 class="yalniz-ekran">{M["kiyaslama_baslik"]}</h3>', unsafe_allow_html=True)
st.dataframe(
    kiyaslama_tablosu.style.format({
        M["gercek"]: "{:,.2f}",
        M["beklenen"]: "{:,.2f}",
        M["sapma"]: "{:,.2f}",
        "CUSUM": "{:,.2f}",
    }),
    use_container_width=True,
    hide_index=True,
    height=izgara_yuksekligi(len(kiyaslama_tablosu)),
)
baski_tablosu(kiyaslama_tablosu, baslik=M["kiyaslama_baslik"])
csv_indirme_dugmesi(kiyaslama_tablosu, M["csv_kiyaslama_dosya"], "csv_kiyaslama_dugmesi")

ozet_col1, ozet_col2, ozet_col3, ozet_col4 = st.columns(4)
ozet_col1.metric(M["toplam_tasarruf"], f"{ozet['toplam_tasarruf']:,.2f}")
ozet_col2.metric(M["toplam_asim"], f"{ozet['toplam_asim']:,.2f}")
ozet_col3.metric(M["net_tasarruf"], f"{ozet['net_tasarruf']:,.2f}")
if np.isnan(ozet["net_tasarruf_yuzdesi"]):
    ozet_col4.metric(M["net_tasarruf_yuzde"], "—")
else:
    ozet_col4.metric(M["net_tasarruf_yuzde"], f"%{ozet['net_tasarruf_yuzdesi']:.2f}")

st.divider()

# ---------------------------------------------------------------------------
# 7. Grafikler (Modül E)
# ---------------------------------------------------------------------------
st.header(M["b6"])

st.plotly_chart(
    charts.create_comparison_chart(
        kiyaslama_tablosu[M["donem"]],
        kiyaslama_tablosu[M["gercek"]],
        kiyaslama_tablosu[M["beklenen"]],
        koyu=KOYU_TEMA,
        m=M,
    ),
    use_container_width=True,
)

st.plotly_chart(
    charts.create_cusum_chart(
        kiyaslama_tablosu[M["donem"]], kiyaslama_tablosu["CUSUM"], koyu=KOYU_TEMA, m=M
    ),
    use_container_width=True,
)
st.caption(M["cusum_caption"])

st.subheader(M["yillik_baslik"])
yillik_ozet = comparison.summarize_by_year(kiyaslama_tablosu, m=M)
st.plotly_chart(
    charts.create_savings_donut_chart(yillik_ozet, koyu=KOYU_TEMA, m=M),
    use_container_width=True,
)
st.caption(M["halka_caption"])

st.divider()

# ---------------------------------------------------------------------------
# 8. PDF Raporu (Modül F) — tarayıcıdan bağımsız, 2,5 cm kenar boşluğu garantili
# ---------------------------------------------------------------------------
st.header(M["rapor_baslik"])
st.markdown(M["rapor_aciklama"])

if st.button(M["rapor_olustur"], key="rapor_olustur_dugmesi"):
    with st.spinner(M["rapor_hazirlaniyor"]):
        try:
            # Rapor grafikleri her zaman açık temada (kağıt için) üretilir.
            rapor_figleri = [
                charts.create_comparison_chart(
                    kiyaslama_tablosu[M["donem"]],
                    kiyaslama_tablosu[M["gercek"]],
                    kiyaslama_tablosu[M["beklenen"]],
                    koyu=False,
                    m=M,
                ),
                charts.create_cusum_chart(
                    kiyaslama_tablosu[M["donem"]], kiyaslama_tablosu["CUSUM"], koyu=False, m=M
                ),
                charts.create_savings_donut_chart(yillik_ozet, koyu=False, m=M),
            ]
            if ham_mod:
                model_sonucu = None
            elif model_uygun_mu:
                model_sonucu = (M["model_uygun"].replace("**", ""), True)
            else:
                model_sonucu = (M["model_uygun_degil"].replace("**", ""), False)

            # PDF oluşturma (hata olsa da HTML devam etsin)
            try:
                grafik_pngler = [
                    fig.to_image(format="png", width=1100, height=520, scale=2)
                    for fig in rapor_figleri
                ]
                st.session_state["pdf_rapor"] = report.build_pdf(
                    M,
                    temiz_df_tum,
                    kriterler_df,
                    katsayilar_df,
                    formul,
                    model_sonucu,
                    kiyaslama_tablosu,
                    ozet,
                    grafik_pngler,
                    gecerlilik_baslik=(M["ham_ozet_baslik"] if ham_mod else None),
                )
            except Exception as e_pdf:
                st.session_state.pop("pdf_rapor", None)
                st.warning(f"⚠️ PDF oluşturmada sorun: {str(e_pdf)[:150]}")

            # HTML oluşturma (PDF hatasından bağımsız)
            try:
                st.session_state["html_rapor"] = html_report.build_html(
                    M,
                    temiz_df_tum,
                    kriterler_df,
                    katsayilar_df,
                    formul,
                    model_sonucu,
                    kiyaslama_tablosu,
                    ozet,
                    rapor_figleri,
                    logo_svg(),
                    SURUM,
                    gecerlilik_baslik=(M["ham_ozet_baslik"] if ham_mod else None),
                )
            except Exception as e_html:
                st.session_state.pop("html_rapor", None)
                st.warning(f"⚠️ HTML oluşturmada sorun: {str(e_html)[:150]}")

        except Exception as e:
            st.error(M["rapor_hata"].format(hata=e))

if st.session_state.get("pdf_rapor") or st.session_state.get("html_rapor"):
    col_pdf, col_html = st.columns(2)
    with col_pdf:
        if st.session_state.get("pdf_rapor"):
            st.download_button(
                M["rapor_indir"],
                data=st.session_state["pdf_rapor"],
                file_name=M["rapor_dosya_adi"],
                mime="application/pdf",
                key="rapor_indir_dugmesi",
            )
    with col_html:
        if st.session_state.get("html_rapor"):
            st.download_button(
                M["rapor_indir_html"],
                data=st.session_state["html_rapor"],
                file_name=M["rapor_dosya_adi_html"],
                mime="text/html",
                key="rapor_indir_html_dugmesi",
            )

# ---------------------------------------------------------------------------
# Sayfa sonu kayıt paneli: analiz tamamlandığında kullanıcı sayfanın altındadır;
# kaydetmek için başa dönmesi gerekmesin diye panel burada yinelenir.
# ---------------------------------------------------------------------------
st.divider()
kayitlar_paneli("alt")

# ---------------------------------------------------------------------------
# Alt Bilgi (Footer) ve yasal uyarı
# ---------------------------------------------------------------------------
st.divider()
st.markdown(M["footer_html"].format(surum=SURUM), unsafe_allow_html=True)
st.markdown(
    '<div style="text-align:center; color:#898781; font-size:0.78rem; '
    'line-height:1.6; padding:0 2rem 1.5rem 2rem;">'
    + M["yasal_uyari"]
    + "</div>",
    unsafe_allow_html=True,
)
