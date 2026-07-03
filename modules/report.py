"""
Modül F: PDF Rapor Üretimi
==========================
Analizin tamamını (giriş verileri, istatistikler, formül, kıyaslama, özet ve
grafikler) tarayıcıdan bağımsız, her kenardan tam 2,5 cm boşluklu A4 sayfa
düzeninde bir PDF dosyası olarak üretir (reportlab + kaleido).
"""

from datetime import datetime
from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    Image, KeepTogether, PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table,
    TableStyle,
)

# Kurumsal renkler
LACIVERT = colors.HexColor("#104281")
GRI = colors.HexColor("#52514e")
ACIK_GRI = colors.HexColor("#c3c2b7")
YESIL = colors.HexColor("#006300")
KIRMIZI = colors.HexColor("#d03b3b")

_font_hazir = False


def _fontlari_yukle():
    """
    Türkçe karakterleri tam destekleyen bir TTF font kaydeder.
    Windows'ta Arial/Calibri, Linux'ta (ör. Streamlit Community Cloud,
    packages.txt ile kurulan) DejaVu Sans denenir.
    """
    global _font_hazir
    if _font_hazir:
        return
    adaylar = [
        ("C:\\Windows\\Fonts\\arial.ttf", "C:\\Windows\\Fonts\\arialbd.ttf"),
        ("C:\\Windows\\Fonts\\calibri.ttf", "C:\\Windows\\Fonts\\calibrib.ttf"),
        ("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
         "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"),
    ]
    for normal, kalin in adaylar:
        try:
            pdfmetrics.registerFont(TTFont("Rapor", normal))
            pdfmetrics.registerFont(TTFont("Rapor-Kalin", kalin))
            _font_hazir = True
            return
        except Exception:
            continue
    raise RuntimeError("Türkçe destekli TTF font bulunamadı (Arial/Calibri).")


def _stil(ad, boyut, renk=GRI, kalin=False, hiza=None, bosluk_sonra=6):
    return ParagraphStyle(
        ad,
        fontName="Rapor-Kalin" if kalin else "Rapor",
        fontSize=boyut,
        leading=boyut * 1.35,
        textColor=renk,
        spaceAfter=bosluk_sonra,
        alignment=hiza if hiza is not None else 0,
    )


def _tablo(df, genislik):
    """DataFrame'i, sayfa genişliğine yayılan biçimli bir reportlab tablosuna çevirir."""
    basliklar = [str(c) for c in df.columns]
    hucre_stili = _stil("hucre", 8, bosluk_sonra=0)
    baslik_stili = _stil("tablo_baslik", 8, kalin=True, bosluk_sonra=0)

    def bicimle(v):
        if isinstance(v, float):
            return f"{v:,.2f}"
        return str(v)

    veri = [[Paragraph(b, baslik_stili) for b in basliklar]]
    for _, satir in df.iterrows():
        veri.append([Paragraph(bicimle(v), hucre_stili) for v in satir])

    tablo = Table(veri, colWidths=[genislik / len(basliklar)] * len(basliklar), repeatRows=1)
    tablo.setStyle(TableStyle([
        ("LINEBELOW", (0, 0), (-1, 0), 0.8, LACIVERT),
        ("LINEBELOW", (0, 1), (-1, -1), 0.4, ACIK_GRI),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    return tablo


def build_pdf(m, veri_df, kriterler_df, katsayilar_df, formul, model_sonucu,
              kiyaslama_df, ozet, grafik_pngler, gecerlilik_baslik=None):
    """
    Analiz raporunu PDF baytları olarak üretir.

    m: dil metinleri sözlüğü; grafik_pngler: PNG bayt dizilerinin listesi.
    model_sonucu: (metin, uygun_mu) çifti veya None (ham tüketim modunda sonuç
    satırı basılmaz). gecerlilik_baslik: istatistik bölümünün başlığı
    (varsayılan: m["rapor_gecerlilik"]).
    """
    _fontlari_yukle()

    tampon = BytesIO()
    dokuman = SimpleDocTemplate(
        tampon,
        pagesize=A4,
        leftMargin=2.5 * cm,
        rightMargin=2.5 * cm,
        topMargin=2.5 * cm,
        bottomMargin=2.5 * cm,
        title=m["sayfa_basligi"],
        author="ATLASCert®",
    )
    genislik = A4[0] - 5 * cm  # 16 cm içerik genişliği

    baslik = _stil("baslik", 16, renk=LACIVERT, kalin=True, bosluk_sonra=4)
    altyazi = _stil("altyazi", 9, bosluk_sonra=12)
    bolum = _stil("bolum", 12, renk=LACIVERT, kalin=True, bosluk_sonra=6)
    govde = _stil("govde", 9, bosluk_sonra=6)
    mono = ParagraphStyle(
        "mono", fontName="Rapor", fontSize=9, leading=13, textColor=colors.black,
        backColor=colors.HexColor("#f6f6f4"), borderPadding=6, spaceAfter=8,
    )
    sonuc_iyi = _stil("sonuc_iyi", 10, renk=YESIL, kalin=True, bosluk_sonra=8)
    sonuc_kotu = _stil("sonuc_kotu", 10, renk=KIRMIZI, kalin=True, bosluk_sonra=8)
    footer = _stil("footer", 7.5, renk=ACIK_GRI, hiza=TA_CENTER, bosluk_sonra=0)

    icerik = []

    # Başlık
    icerik.append(Paragraph(m["sayfa_basligi"], baslik))
    icerik.append(Paragraph(
        f"{m['alt_baslik']}<br/>{m['rapor_tarih']}: {datetime.now().strftime('%d.%m.%Y %H:%M')}",
        altyazi,
    ))

    # 1. Giriş verileri
    icerik.append(Paragraph(m["rapor_giris_tablosu"], bolum))
    icerik.append(_tablo(veri_df, genislik))
    icerik.append(Spacer(1, 12))

    # 2. İstatistiksel geçerlilik / özet
    gecerlilik_parcalari = [
        Paragraph(gecerlilik_baslik or m["rapor_gecerlilik"], bolum),
        _tablo(kriterler_df, genislik),
    ]
    if model_sonucu is not None:
        metin, uygun_mu = model_sonucu
        gecerlilik_parcalari.append(Spacer(1, 4))
        gecerlilik_parcalari.append(Paragraph(metin, sonuc_iyi if uygun_mu else sonuc_kotu))
    icerik.append(KeepTogether(gecerlilik_parcalari))
    icerik.append(Spacer(1, 8))

    # 3. Formül ve katsayılar
    icerik.append(KeepTogether([
        Paragraph(m["b4"].split(". ", 1)[-1], bolum),
        Paragraph(formul, mono),
        _tablo(katsayilar_df, genislik),
    ]))
    icerik.append(Spacer(1, 12))

    # 4. Kıyaslama tablosu ve özet
    ozet_df_veri = {
        m["toplam_tasarruf"]: f"{ozet['toplam_tasarruf']:,.2f}",
        m["toplam_asim"]: f"{ozet['toplam_asim']:,.2f}",
        m["net_tasarruf"]: f"{ozet['net_tasarruf']:,.2f}",
        m["net_tasarruf_yuzde"]: (
            f"%{ozet['net_tasarruf_yuzdesi']:.2f}"
            if ozet["net_tasarruf_yuzdesi"] == ozet["net_tasarruf_yuzdesi"]
            else "—"
        ),
    }
    import pandas as pd
    ozet_df = pd.DataFrame([ozet_df_veri])

    icerik.append(Paragraph(m["kiyaslama_baslik"], bolum))
    icerik.append(_tablo(kiyaslama_df, genislik))
    icerik.append(Spacer(1, 6))
    icerik.append(_tablo(ozet_df, genislik))
    icerik.append(Spacer(1, 12))

    # 5. Grafikler (her biri başlığı grafiğin içinde; sayfada ortalanır).
    # "Grafikler" başlığı ilk grafikle aynı blokta tutulur ki başlık önceki
    # sayfada tek başına kalmasın; son grafik (yıllık tasarruf dağılımı)
    # sayfa kesmesiyle son sayfada tek başına yer alır.
    gorseller = []
    for png in grafik_pngler:
        gorsel = Image(BytesIO(png))
        oran = gorsel.imageHeight / gorsel.imageWidth
        gorsel.drawWidth = genislik
        gorsel.drawHeight = genislik * oran
        gorsel.hAlign = "CENTER"
        gorseller.append(gorsel)

    if gorseller:
        icerik.append(KeepTogether([
            Paragraph(m["b6"].split(". ", 1)[-1], bolum),
            gorseller[0],
            Spacer(1, 10),
        ]))
        for gorsel in gorseller[1:-1]:
            icerik.append(KeepTogether([gorsel, Spacer(1, 10)]))
        if len(gorseller) > 1:
            icerik.append(PageBreak())
            icerik.append(KeepTogether([gorseller[-1], Spacer(1, 10)]))

    # Alt bilgi ve yasal uyarı
    icerik.append(Spacer(1, 14))
    icerik.append(Paragraph(m["footer_metin"], footer))
    if m.get("yasal_uyari"):
        icerik.append(Spacer(1, 4))
        icerik.append(Paragraph(m["yasal_uyari"], footer))

    dokuman.build(icerik)
    return tampon.getvalue()
