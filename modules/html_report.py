"""
Modül E/F: HTML Rapor Üretimi (Çevrimdışı)
===========================================
PDF rapor gibi kullanıcıya aynı veri ve istatistikleri sunan, ancak
Plotly grafiklerini interaktif (zoom/hover) tutarak ve tamamen çevrimdışı
çalışan (CDN'e istek atılmayan) bir HTML dosyası üretir. Tüm Plotly JS
kütüphanesi HTML'e gömülüdür.
"""

import base64

import pandas as pd
import plotly.io as pio

# Kurumsal renkler (report.py'deki ile birebir)
LACIVERT = "#104281"
GRI = "#52514e"
ACIK_GRI = "#c3c2b7"
YESIL = "#006300"
KIRMIZI = "#d03b3b"


def build_html(m, veri_df, kriterler_df, katsayilar_df, formul, model_sonucu,
               kiyaslama_df, ozet, figures, logo_svg_metni, surum, gecerlilik_baslik=None):
    """
    Analizin tamamını (veriler, istatistikler, formül, kıyaslama, özet, interaktif grafikler)
    sunucu gerektirmeyen, çevrimdışı çalışan bir HTML dosyası olarak üretir.

    Parametreler:
    - m: dil metinleri (i18n sözlüğü)
    - veri_df, kriterler_df, katsayilar_df, kiyaslama_df: DataFrame'ler
    - formul: str (regresyon formülü metni)
    - model_sonucu: (metin, uygun_mu) tuple veya None (ham mod)
    - ozet: dict (toplam_tasarruf, toplam_asim, net_tasarruf, net_tasarruf_yuzdesi)
    - figures: go.Figure nesnelerinin listesi (Plotly figürleri)
    - logo_svg_metni: ham SVG metni (string), data-URI'ye base64 ile kodlanacak
    - surum: sürüm numarası (str), örn. "1.1.0"
    - gecerlilik_baslik: istatistik bölümü başlığı (varsayılan: m["rapor_gecerlilik"])

    Dönüş: UTF-8 kodlu bytes (st.download_button için hazır)
    """
    gecerlilik_baslik = gecerlilik_baslik or m.get("rapor_gecerlilik", "Statistical Validity")

    # Plotly JS (bir kez), tüm grafikler için — get_plotlyjs ham JS döndürür,
    # <script> etiketiyle sarılarak sayfaya gömülür (CDN'e istek atılmaz).
    from plotly.offline import get_plotlyjs
    plotlyjs = "<script>" + get_plotlyjs() + "</script>"

    # Logo data-URI'ye
    logo_b64 = base64.b64encode(logo_svg_metni.encode("utf-8")).decode("utf-8")
    logo_data_uri = f'data:image/svg+xml;base64,{logo_b64}'

    # Grafikler interaktif HTML'ye (PNG'ye değil)
    grafik_htmller = []
    for fig in figures:
        grafik_html = pio.to_html(fig, full_html=False, include_plotlyjs=False)
        grafik_htmller.append(grafik_html)

    # DataFrame'leri HTML tablolara
    def df_to_html_table(df):
        return df.to_html(index=False, border=0, escape=False, float_format=lambda x: f"{x:,.2f}")

    veri_table = df_to_html_table(veri_df)
    kriterler_table = df_to_html_table(kriterler_df)
    katsayilar_table = df_to_html_table(katsayilar_df)
    kiyaslama_table = df_to_html_table(kiyaslama_df)

    # Özet tablosu
    ozet_df = pd.DataFrame([{
        m.get("toplam_tasarruf", "Total Savings"): f"{ozet['toplam_tasarruf']:,.2f}",
        m.get("toplam_asim", "Total Overrun"): f"{ozet['toplam_asim']:,.2f}",
        m.get("net_tasarruf", "Net Savings"): f"{ozet['net_tasarruf']:,.2f}",
        m.get("net_tasarruf_yuzde", "Savings %"):
            (f"%{ozet['net_tasarruf_yuzdesi']:.2f}" if ozet.get("net_tasarruf_yuzdesi") == ozet.get("net_tasarruf_yuzdesi") else "—"),
    }])
    ozet_table = df_to_html_table(ozet_df)

    # Model sonucu HTML
    model_sonucu_html = ""
    if model_sonucu is not None:
        metin, uygun_mu = model_sonucu
        renk = YESIL if uygun_mu else KIRMIZI
        model_sonucu_html = f'<p style="color: {renk}; font-weight: bold; margin-top: 10px;">{metin}</p>'

    # Bugün tarihini (Türkçe/İngilizce)
    from datetime import datetime
    rapor_tarihi = datetime.now().strftime("%d.%m.%Y %H:%M")

    html_icerigi = f"""<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{m.get("sayfa_basligi", "ATLASCert®")}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: system-ui, -apple-system, 'Segoe UI', sans-serif;
            color: {GRI};
            background-color: #fafaf8;
            line-height: 1.6;
        }}
        .container {{
            max-width: 900px;
            margin: 0 auto;
            padding: 40px 20px;
            background-color: white;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.05);
        }}
        header {{
            display: flex;
            align-items: center;
            gap: 20px;
            margin-bottom: 30px;
            border-bottom: 2px solid {LACIVERT};
            padding-bottom: 20px;
        }}
        header img {{
            width: 80px;
            height: 80px;
            object-fit: contain;
        }}
        header h1 {{
            color: {LACIVERT};
            font-size: 28px;
            font-weight: 600;
        }}
        header p {{
            color: {ACIK_GRI};
            font-size: 14px;
            margin-top: 5px;
        }}
        h2 {{
            color: {LACIVERT};
            font-size: 20px;
            font-weight: 600;
            margin-top: 30px;
            margin-bottom: 15px;
            border-left: 4px solid {LACIVERT};
            padding-left: 12px;
        }}
        h3 {{
            color: {GRI};
            font-size: 16px;
            font-weight: 600;
            margin-top: 20px;
            margin-bottom: 10px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 20px;
            font-size: 14px;
        }}
        table th {{
            background-color: {LACIVERT};
            color: white;
            padding: 10px;
            text-align: left;
            font-weight: 600;
        }}
        table td {{
            padding: 8px 10px;
            border-bottom: 1px solid {ACIK_GRI};
        }}
        table tr:hover {{
            background-color: #f9f9f7;
        }}
        .code-block {{
            background-color: #f6f6f4;
            border-left: 4px solid {LACIVERT};
            padding: 12px;
            margin-bottom: 20px;
            font-family: 'Courier New', monospace;
            font-size: 13px;
            white-space: pre-wrap;
            word-break: break-word;
            overflow-x: auto;
        }}
        .metric {{
            display: inline-block;
            background-color: #f9f9f7;
            border: 1px solid {ACIK_GRI};
            border-radius: 8px;
            padding: 15px 20px;
            margin-right: 15px;
            margin-bottom: 15px;
            min-width: 200px;
        }}
        .metric label {{
            display: block;
            font-size: 12px;
            color: {ACIK_GRI};
            font-weight: 600;
            margin-bottom: 5px;
            text-transform: uppercase;
        }}
        .metric value {{
            display: block;
            font-size: 20px;
            color: {LACIVERT};
            font-weight: 600;
        }}
        .chart {{
            margin-bottom: 30px;
            page-break-inside: avoid;
        }}
        .chart > h3 {{
            margin-bottom: 15px;
        }}
        .chart > div {{
            border: 1px solid {ACIK_GRI};
            border-radius: 4px;
            padding: 15px;
            background-color: white;
        }}
        footer {{
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid {ACIK_GRI};
            text-align: center;
            font-size: 12px;
            color: {ACIK_GRI};
            line-height: 1.8;
        }}
        .success {{ color: {YESIL}; font-weight: bold; }}
        .error {{ color: {KIRMIZI}; font-weight: bold; }}
        @media print {{
            body {{ background-color: white; }}
            .container {{ box-shadow: none; padding: 0; }}
            .chart {{ page-break-inside: avoid; }}
        }}
    </style>
    {plotlyjs}
</head>
<body>
    <div class="container">
        <!-- Başlık -->
        <header>
            <img src="{logo_data_uri}" alt="ATLASCert Logo">
            <div>
                <h1>{m.get("sayfa_basligi", "Energy Baseline Analysis")}</h1>
                <p>{m.get("rapor_tarih", "Report date")}: {rapor_tarihi}</p>
            </div>
        </header>

        <!-- 1. Giriş Verileri -->
        <h2>{m.get("rapor_giris_tablosu", "Input Data")}</h2>
        {veri_table}

        <!-- 2. İstatistiksel Geçerlilik -->
        <h2>{gecerlilik_baslik}</h2>
        {kriterler_table}
        {model_sonucu_html}

        <!-- 3. Formül ve Katsayılar -->
        <h2>{m.get("b4", "Formula")}</h2>
        <div class="code-block">{formul}</div>
        {katsayilar_table}

        <!-- 4. Kıyaslama Tablosu ve Özet -->
        <h2>{m.get("kiyaslama_baslik", "Comparison and Analysis")}</h2>
        {kiyaslama_table}

        <h3>{"Özet" if m.get("donem") == "Dönem" else "Summary"}</h3>
        {ozet_table}

        <!-- 5. Grafikler -->
        <h2>{m.get("b6", "Charts")}</h2>
"""

    # Grafikleri ekle
    chart_titles = [
        m.get("g1_baslik", "Actual vs Expected Consumption"),
        m.get("cusum_baslik", "Cumulative Savings (CUSUM)"),
        m.get("halka_baslik", "Annual Savings Distribution"),
    ]
    for i, grafik_html in enumerate(grafik_htmller):
        baslik = chart_titles[i] if i < len(chart_titles) else f"{m.get('grafik', 'Chart')} {i + 1}"
        html_icerigi += f'''
        <div class="chart">
            <h3>{baslik}</h3>
            <div>
                {grafik_html}
            </div>
        </div>
'''

    html_icerigi += f"""
        <!-- Footer -->
        <footer>
            <p><strong>ATLASCert®</strong> — {m.get("portal_basligi", "Energy Baseline Analysis Portal")}</p>
            <p>© 2026 ATLASCert®. {m.get("footer_metin", "All rights reserved.")}</p>
            <p>{"Sürüm" if m.get("donem") == "Dönem" else "Version"}: v{surum}</p>
        </footer>
    </div>
</body>
</html>
"""

    return html_icerigi.encode("utf-8")
