"""
Modül D: Kıyaslama ve Performans Ölçümü (CUSUM ve Tasarruf)
===========================================================
Kurulan regresyon modeli, raporlama dönemindeki bağımsız değişken verilerine
uygulanarak "Beklenen Enerji Tüketimi" (ayarlanmış temel çizgi) hesaplanır ve
gerçek tüketimle kıyaslanır. IPMVP terminolojisinde bu fark "Kaçınılan Enerji
Tüketimi" (Avoided Energy Use) olarak adlandırılır.

Tablo sütun adları, seçilen dilin metin sözlüğünden (i18n) gelir.
"""

import numpy as np
import pandas as pd

from modules import i18n


def calculate_expected_consumption(model, df, x_cols):
    """
    Kurulmuş regresyon modelini, raporlama dönemi bağımsız değişken verilerine
    uygulayarak "Beklenen Enerji Tüketimi" değerlerini hesaplar.
    """
    X = df[x_cols].astype(float).copy()
    X.insert(0, "const", 1.0)
    beklenen = model.predict(X)
    return beklenen.values


def _ay_anahtari(etiket):
    """'Ocak 2025' benzeri bir dönem etiketinden ay adını (küçük harfle) çıkarır."""
    parcalar = str(etiket).strip().split()
    return parcalar[0].lower() if parcalar else ""


def monthly_baseline_map(referans_df, donem_col, y_col):
    """
    Referans dönemi tüketimlerini, dönem etiketlerindeki ay adına göre gruplayıp
    her ay için ortalama temel çizgi değeri üretir (aylık eşleştirme yöntemi).
    Referans birden çok yıl içeriyorsa aynı ayın değerlerinin ortalaması alınır.
    Dönüş: {ay_adı: ortalama} sözlüğü.
    """
    aylar = referans_df[donem_col].map(_ay_anahtari)
    return referans_df[y_col].astype(float).groupby(aylar).mean().to_dict()


def expected_from_monthly(donem_etiketleri, harita, genel_ortalama):
    """
    Raporlama dönemi etiketlerini aylık temel çizgi haritasıyla eşleştirir.
    Haritada bulunmayan aylar (veya ay adı çözülemeyen etiketler) için genel
    ortalamaya düşülür.
    """
    return np.array([
        float(harita.get(_ay_anahtari(e), genel_ortalama)) for e in donem_etiketleri
    ])


def build_comparison_table(donem_etiketleri, gercek_tuketim, beklenen_tuketim, m=None):
    """
    Dönem, Gerçek Tüketim, Beklenen Tüketim, Sapma ve Kümülatif Toplam (CUSUM)
    sütunlarını içeren kıyaslama tablosunu oluşturur.

    Sapma = Beklenen - Gerçek  =>  Pozitif değer tasarrufu, negatif değer aşımı gösterir.
    """
    m = m or i18n.METINLER["tr"]
    gercek_tuketim = np.asarray(gercek_tuketim, dtype=float)
    beklenen_tuketim = np.asarray(beklenen_tuketim, dtype=float)

    sapma = beklenen_tuketim - gercek_tuketim
    cusum = np.cumsum(sapma)

    tablo = pd.DataFrame({
        m["donem"]: donem_etiketleri,
        m["gercek"]: gercek_tuketim,
        m["beklenen"]: beklenen_tuketim,
        m["sapma"]: sapma,
        "CUSUM": cusum,
    })

    tablo[m["durum"]] = np.where(sapma >= 0, m["tasarruf_saglandi"], m["asim_olustu"])

    return tablo


def summarize_by_year(tablo, m=None):
    """
    Dönem etiketlerindeki yıl bilgisine (örn. 'Ocak 2025') göre yıllık özet üretir.
    Yıl bilgisi bulunamayan satırlar 'Tüm Dönem' altında toplanır.
    Dönüş: yil, gercek, beklenen, net_tasarruf ve tasarruf_orani (%) sütunlu DataFrame
    (sütun adları içseldir, görüntülenmez).
    """
    m = m or i18n.METINLER["tr"]
    t = tablo.copy()
    t["_yil"] = t[m["donem"]].astype(str).str.extract(r"(\d{4})")[0].fillna(m["tum_donem"])

    grup = (
        t.groupby("_yil", sort=True)
        .agg(gercek=(m["gercek"], "sum"), beklenen=(m["beklenen"], "sum"))
        .reset_index()
        .rename(columns={"_yil": "yil"})
    )
    grup["net_tasarruf"] = grup["beklenen"] - grup["gercek"]
    grup["tasarruf_orani"] = np.where(
        grup["beklenen"] != 0,
        grup["net_tasarruf"] / grup["beklenen"] * 100,
        np.nan,
    )
    return grup


def summarize_savings(tablo, m=None):
    """
    Toplam tasarruf, toplam aşım, net tasarruf ve net tasarruf yüzdesi özetini hesaplar.
    """
    m = m or i18n.METINLER["tr"]
    sapma = tablo[m["sapma"]]
    toplam_tasarruf = float(sapma[sapma > 0].sum())
    toplam_asim = float(-sapma[sapma < 0].sum()) + 0.0  # -0.00 görüntüsünü engeller
    net_tasarruf = float(sapma.sum())
    toplam_gercek = float(tablo[m["gercek"]].sum())

    net_tasarruf_yuzdesi = (
        (net_tasarruf / (toplam_gercek + net_tasarruf) * 100)
        if (toplam_gercek + net_tasarruf) != 0
        else np.nan
    )

    return {
        "toplam_tasarruf": toplam_tasarruf,
        "toplam_asim": toplam_asim,
        "net_tasarruf": net_tasarruf,
        "net_tasarruf_yuzdesi": net_tasarruf_yuzdesi,
    }
