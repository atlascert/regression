"""
Modül B: İstatistiksel Analiz ve Eşik Değerler (Model Doğrulama)
Modül C: Formül Çıktısı
================================================================
statsmodels OLS kullanılarak çoklu doğrusal regresyon kurulur; model geçerliliği
IPMVP ve ASHRAE Guideline 14 eşik değerlerine göre değerlendirilir.
"""

import numpy as np
import pandas as pd
import statsmodels.api as sm

from modules import i18n


# IPMVP / ASHRAE Guideline 14 kapsamında kabul edilen eşik değerler
ESIK_R2 = 0.75
ESIK_PDEGERI = 0.05
ESIK_F_PDEGERI = 0.05
ESIK_CV_RMSE = 0.15  # %15 (aylık veri için ASHRAE Guideline 14 önerisi)


def run_regression(df, y_col, x_cols):
    """
    Çoklu doğrusal regresyon modelini kurar.
    Dönüş: statsmodels OLS sonuç nesnesi (RegressionResults)
    """
    y = df[y_col].astype(float)
    X = df[x_cols].astype(float)
    X = sm.add_constant(X)  # Kesişim terimi (β0) eklenir

    model = sm.OLS(y, X).fit()
    return model


def calculate_metrics(model, df, y_col, x_cols):
    """
    Modelin istatistiksel metriklerini hesaplar.
    Dönüş: metrikleri içeren bir sözlük (dict)
    """
    y_gercek = df[y_col].astype(float).values
    y_tahmin = model.fittedvalues.values

    hata = y_gercek - y_tahmin
    rmse = float(np.sqrt(np.mean(hata ** 2)))

    y_ortalama = float(np.mean(y_gercek))
    y_araligi = float(np.max(y_gercek) - np.min(y_gercek))

    nrmse = rmse / y_araligi if y_araligi != 0 else np.nan
    cv_rmse = rmse / y_ortalama if y_ortalama != 0 else np.nan

    # Tahminin standart hatası (Standard Error of the Estimate, SEE)
    standart_hata = float(np.sqrt(model.mse_resid))

    p_degerleri = {x: float(model.pvalues[x]) for x in x_cols}

    return {
        "r2": float(model.rsquared),
        "adj_r2": float(model.rsquared_adj),
        "standart_hata": standart_hata,
        "p_degerleri": p_degerleri,
        "f_istatistigi": float(model.fvalue),
        "f_pdegeri": float(model.f_pvalue),
        "rmse": rmse,
        "nrmse": nrmse,
        "cv_rmse": cv_rmse,
    }


def evaluate_model(metrics, m=None):
    """
    IPMVP / ASHRAE Guideline 14 eşik değerlerine göre her ölçütü
    "Uygun" / "Uygun Değil" olarak değerlendirir. m ile farklı dildeki
    metin sözlüğü kullanılabilir.
    Dönüş: (degerlendirme_tablosu: list[dict], model_uygun_mu: bool, anlamsiz_degiskenler: list)
    """
    m = m or i18n.METINLER["tr"]
    anlamsiz_degiskenler = [x for x, p in metrics["p_degerleri"].items() if p > ESIK_PDEGERI]

    OLCUT, ESIK, HESAP, SONUC = m["olcut"], m["esik_deger"], m["hesaplanan"], m["sonuc"]
    UYGUN, UYGUN_DEGIL = m["uygun"], m["uygun_degil"]

    kriterler = [
        {
            OLCUT: m["r2_adi"],
            ESIK: f"≥ {ESIK_R2}",
            HESAP: f"{metrics['r2']:.4f}",
            SONUC: UYGUN if metrics["r2"] >= ESIK_R2 else UYGUN_DEGIL,
        },
        {
            OLCUT: m["adjr2_adi"],
            ESIK: m["bilgi_amacli"],
            HESAP: f"{metrics['adj_r2']:.4f}",
            SONUC: "—",
        },
        {
            OLCUT: m["see_adi"],
            ESIK: m["dusuk_olmali"],
            HESAP: f"{metrics['standart_hata']:.4f}",
            SONUC: "—",
        },
        {
            OLCUT: m["p_adi"],
            ESIK: f"≤ {ESIK_PDEGERI}",
            HESAP: ", ".join(f"{x}: {p:.4f}" for x, p in metrics["p_degerleri"].items()),
            SONUC: UYGUN if not anlamsiz_degiskenler else UYGUN_DEGIL,
        },
        {
            OLCUT: m["f_adi"],
            ESIK: m["f_esik"].format(esik=ESIK_F_PDEGERI),
            HESAP: f"F = {metrics['f_istatistigi']:.4f}, p = {metrics['f_pdegeri']:.4f}",
            SONUC: UYGUN if metrics["f_pdegeri"] < ESIK_F_PDEGERI else UYGUN_DEGIL,
        },
        {
            OLCUT: m["rmse_adi"],
            ESIK: m["dusuk_olmali"],
            HESAP: f"{metrics['rmse']:.4f}",
            SONUC: "—",
        },
        {
            OLCUT: m["nrmse_adi"],
            ESIK: m["dusuk_olmali"],
            HESAP: f"{metrics['nrmse']:.4f}" if not np.isnan(metrics["nrmse"]) else m["hesaplanamadi"],
            SONUC: "—",
        },
        {
            OLCUT: m["cv_adi"],
            ESIK: m["cv_esik"].format(esik=f"{ESIK_CV_RMSE * 100:.0f}"),
            HESAP: f"%{metrics['cv_rmse'] * 100:.2f}" if not np.isnan(metrics["cv_rmse"]) else m["hesaplanamadi"],
            SONUC: UYGUN if (not np.isnan(metrics["cv_rmse"]) and metrics["cv_rmse"] <= ESIK_CV_RMSE) else UYGUN_DEGIL,
        },
    ]

    # Genel uygunluk: R², tüm değişkenlerin p-değeri ve CV(RMSE) eşiklerinin tümü sağlanmalıdır.
    model_uygun_mu = (
        metrics["r2"] >= ESIK_R2
        and not anlamsiz_degiskenler
        and not np.isnan(metrics["cv_rmse"])
        and metrics["cv_rmse"] <= ESIK_CV_RMSE
    )

    return kriterler, model_uygun_mu, anlamsiz_degiskenler


def get_formula_string(model, y_col, x_cols):
    """
    Modül C: Kurulan modelin matematiksel formülünü okunabilir metin olarak döndürür.
    Örnek: Tüketim (kWh) = 120.45 + (3.21 × Üretim) - (1.05 × HDD)
    """
    intercept = model.params["const"]
    terimler = [f"{intercept:.4f}"]

    for x in x_cols:
        katsayi = model.params[x]
        isaret = "+" if katsayi >= 0 else "-"
        terimler.append(f"{isaret} ({abs(katsayi):.4f} × {x})")

    formul = f"{y_col} = " + " ".join(terimler)
    return formul


def get_katsayilar_tablosu(model, x_cols, m=None):
    """
    Beta katsayılarını ve kesişim terimini (β0) tablo hâlinde döndürür.
    """
    m = m or i18n.METINLER["tr"]
    satirlar = [{
        m["katsayi_degisken"]: m["kesisim"],
        m["katsayi"]: f"{model.params['const']:.4f}",
        m["p_degeri"]: f"{model.pvalues['const']:.4f}",
    }]

    for i, x in enumerate(x_cols, start=1):
        satirlar.append({
            m["katsayi_degisken"]: f"{x} (β{i})",
            m["katsayi"]: f"{model.params[x]:.4f}",
            m["p_degeri"]: f"{model.pvalues[x]:.4f}",
        })

    return pd.DataFrame(satirlar)
