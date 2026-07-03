"""
Modül E: Görselleştirme
=======================
Raporlama dönemi için minimalist, kurumsal temalı interaktif Plotly grafiklerini
üretir. Tüm grafikler tema duyarlıdır: açık temada plotly_white, koyu temada
plotly_dark tabanı kullanılır; zeminler her iki temada da şeffaftır (dolgu yok)
ve çizgi/yazı renkleri bulunulan temada rahat okunacak şekilde seçilir.

  - Çizgi Grafiği 1: Gerçek Tüketim ile Beklenen Tüketimin kıyaslanması
  - Grafik 2: CUSUM (kümülatif tasarruf) performans grafiği
  - Grafik 3: Yıllık tasarruf dağılımı halka (donut) grafikleri
"""

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from modules import i18n

SEFFAF = "rgba(0,0,0,0)"

# Açık ve koyu tema renk takımları — doğrulanmış paletin ilgili tema adımları
TEMALAR = {
    "acik": dict(
        gercek="#2a78d6",    # mavi (seri 1: gerçek tüketim)
        beklenen="#1baf7a",  # yeşil (seri 2: beklenen tüketim / model)
        tasarruf="#0ca30c",  # durum: iyi
        asim="#d03b3b",      # durum: kritik
        notr="#c3c2b7",      # halka grafiğinde tüketim payı
        grid="#e1e0d9",
        eksen="#c3c2b7",
        metin="#52514e",
        baslik="#104281",    # lacivert başlık
        yuzey="#ffffff",     # işaretçi halkası / dilim ayracı (uygulama zemini)
    ),
    "koyu": dict(
        gercek="#3987e5",
        beklenen="#199e70",
        tasarruf="#0ca30c",
        asim="#e66767",
        notr="#52514e",
        grid="#2c2c2a",
        eksen="#4a4a47",
        metin="#c3c2b7",
        baslik="#86b6ef",
        yuzey="#0e1117",     # Streamlit koyu tema zemini
    ),
}


def _tema(koyu):
    return TEMALAR["koyu" if koyu else "acik"]


def _kurumsal_duzen(fig, baslik, koyu=False):
    """Tüm grafiklere ortak minimalist kurumsal düzeni uygular (tema duyarlı)."""
    r = _tema(koyu)
    fig.update_layout(
        template="plotly_dark" if koyu else "plotly_white",
        title=dict(text=baslik, font=dict(color=r["baslik"], size=16)),
        plot_bgcolor=SEFFAF,
        paper_bgcolor=SEFFAF,
        font=dict(color=r["metin"], size=13, family="system-ui, -apple-system, 'Segoe UI', sans-serif"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
        margin=dict(t=70, l=10, r=10, b=10),
        hovermode="x unified",
    )
    fig.update_xaxes(
        showgrid=False,
        linecolor=r["eksen"],
        ticks="outside",
        tickcolor=r["eksen"],
        tickfont=dict(size=12, color=r["metin"]),
    )
    fig.update_yaxes(
        showgrid=True,
        gridcolor=r["grid"],
        gridwidth=1,
        zeroline=False,
        linecolor=r["eksen"],
        tickfont=dict(size=12, color=r["metin"]),
    )
    return fig


def create_comparison_chart(donem, gercek, beklenen, koyu=False, m=None):
    """
    Çizgi Grafiği 1: Gerçek Tüketim ile Beklenen Tüketimin dönemler boyunca kıyaslanması.
    """
    m = m or i18n.METINLER["tr"]
    r = _tema(koyu)
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=donem, y=gercek,
        mode="lines+markers",
        name=m["seri_gercek"],
        line=dict(color=r["gercek"], width=2),
        marker=dict(size=8, color=r["gercek"], line=dict(width=2, color=r["yuzey"])),
    ))

    fig.add_trace(go.Scatter(
        x=donem, y=beklenen,
        mode="lines+markers",
        name=m["seri_beklenen"],
        line=dict(color=r["beklenen"], width=2, dash="dash"),
        marker=dict(size=8, color=r["beklenen"], line=dict(width=2, color=r["yuzey"])),
    ))

    return _kurumsal_duzen(fig, m["g1_baslik"], koyu)


def create_cusum_chart(donem, cusum, koyu=False, m=None):
    """
    Grafik 2: Kümülatif tasarrufu (CUSUM) gösteren, sıfır çizgisinin altını ve
    üstünü durum renkleriyle vurgulayan performans grafiği.
    """
    m = m or i18n.METINLER["tr"]
    r = _tema(koyu)
    cusum = np.asarray(cusum, dtype=float)
    pozitif = np.where(cusum >= 0, cusum, np.nan)
    negatif = np.where(cusum < 0, cusum, np.nan)

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=donem, y=pozitif,
        name=m["cusum_poz"],
        marker=dict(color=r["tasarruf"], line=dict(width=0)),
    ))

    fig.add_trace(go.Bar(
        x=donem, y=negatif,
        name=m["cusum_neg"],
        marker=dict(color=r["asim"], line=dict(width=0)),
    ))

    fig.add_hline(y=0, line_width=1, line_color=r["eksen"])

    fig = _kurumsal_duzen(fig, m["cusum_baslik"], koyu)
    fig.update_layout(hovermode="x", bargap=0.35)
    return fig


def create_savings_donut_chart(yillik_ozet, koyu=False, m=None):
    """
    Grafik 3: Yıllık halka (donut) grafikleri. Her halka, ilgili yılın beklenen
    (temel çizgi) tüketimini temsil eder; yeşil dilim net tasarrufun toplam
    içindeki payını gösterir. Net tasarrufun negatif olduğu (aşım) yıllarda
    halka, gerçek tüketim içindeki aşım payını kırmızı dilimle gösterir.
    """
    m = m or i18n.METINLER["tr"]
    r = _tema(koyu)
    n = len(yillik_ozet)
    fig = make_subplots(
        rows=1,
        cols=n,
        specs=[[{"type": "domain"}] * n],
        subplot_titles=[str(y) for y in yillik_ozet["yil"]],
    )

    for i, satir in enumerate(yillik_ozet.itertuples(index=False), start=1):
        oran_gecerli = not np.isnan(satir.tasarruf_orani)

        if satir.net_tasarruf >= 0:
            etiketler = [m["gercek"], m["halka_tasarruf"]]
            degerler = [satir.gercek, satir.net_tasarruf]
            renkler = [r["notr"], r["tasarruf"]]
            merkez = f"<b>%{satir.tasarruf_orani:.1f}</b><br>{m['merkez_tasarruf']}" if oran_gecerli else "—"
        else:
            etiketler = [m["beklenen"], m["halka_asim"]]
            degerler = [satir.beklenen, -satir.net_tasarruf]
            renkler = [r["notr"], r["asim"]]
            merkez = f"<b>%{abs(satir.tasarruf_orani):.1f}</b><br>{m['merkez_asim']}" if oran_gecerli else "—"

        fig.add_trace(
            go.Pie(
                labels=etiketler,
                values=degerler,
                hole=0.62,
                sort=False,
                direction="clockwise",
                textinfo="percent",
                marker=dict(colors=renkler, line=dict(color=r["yuzey"], width=2)),
                hovertemplate="%{label}: %{value:,.2f} (%{percent})<extra></extra>",
            ),
            row=1,
            col=i,
        )

        fig.add_annotation(
            x=(i - 0.5) / n,
            y=0.5,
            xref="paper",
            yref="paper",
            text=merkez,
            showarrow=False,
            font=dict(size=15, color=r["metin"]),
        )

    fig = _kurumsal_duzen(fig, m["halka_baslik"], koyu)
    # Sabit ve dengeli yükseklik: geniş ekranlarda da baskıda da halka ezilmez.
    fig.update_layout(hovermode="closest", height=480)
    return fig
