"""
Modül A: Veri Girişi ve Doğrulama
=================================
Veri ızgarasından (st.data_editor) kopyala/yapıştır yoluyla veya opsiyonel
CSV/Excel dosyasından gelen verilerin okunması, Türkçe sayı biçimlerinin
çözümlenmesi ve temizlenmesi ile ilgili yardımcı fonksiyonlar.
"""

import re

import numpy as np
import pandas as pd

from modules import i18n

AYLAR = i18n.METINLER["tr"]["aylar"]


def ay_yil_ekle(ay, yil, kac_ay):
    """
    Verilen ay/yıl çiftine belirtilen sayıda ay ekler (yıl devri dâhil).
    Dönüş: (ay, yil) — ay 1-12 aralığındadır.
    """
    toplam = yil * 12 + (ay - 1) + kac_ay
    return toplam % 12 + 1, toplam // 12


def generate_period_labels(baslangic_ay, baslangic_yil, adet, aylar=None):
    """
    Seçilen başlangıç ayından itibaren 'Ocak 2025', 'Şubat 2025', ...
    biçiminde aylık dönem etiketleri üretir. aylar parametresiyle farklı
    dildeki ay adları kullanılabilir.
    """
    aylar = aylar or AYLAR
    etiketler = []
    for i in range(adet):
        ay, yil = ay_yil_ekle(baslangic_ay, baslangic_yil, i)
        etiketler.append(f"{aylar[ay - 1]} {yil}")
    return etiketler


def ay_farki(bas_ay, bas_yil, bit_ay, bit_yil):
    """
    Başlangıç ve bitiş dönemi (ay/yıl) arasındaki ay sayısını,
    her iki uç dâhil olacak şekilde döndürür.
    """
    return (bit_yil * 12 + bit_ay) - (bas_yil * 12 + bas_ay) + 1


def create_period_grid(donem_etiketleri, veri_sutunlari, donem_sutunu="Dönem"):
    """
    Dönem sütunu seçilen aralığın etiketleriyle önceden doldurulmuş,
    veri sütunları boş bir ızgara şablonu üretir. Satır sayısı dönem
    aralığı tarafından belirlendiği için tabloya ayrıca satır eklenmez.
    """
    df = pd.DataFrame({donem_sutunu: list(donem_etiketleri)})
    for col in veri_sutunlari:
        df[col] = ""
    return df


def create_empty_grid(sutunlar, satir_sayisi=12):
    """
    Kopyala/yapıştır girişi için boş bir veri ızgarası şablonu üretir.
    Tüm hücreler metin olarak tutulur; böylece Excel'den yapıştırılan
    Türkçe sayı biçimleri (örn. '1.234,56') kayıpsız alınır.
    """
    return pd.DataFrame(
        [[""] * len(sutunlar) for _ in range(satir_sayisi)],
        columns=sutunlar,
    )


def _sayiya_cevir(deger):
    """
    Türkçe ('1.234,56') ve uluslararası ('1234.56') sayı biçimlerini
    float değere çevirir. Çevrilemeyen değerler NaN olur.
    """
    if deger is None or (isinstance(deger, float) and np.isnan(deger)):
        return np.nan
    if isinstance(deger, (int, float)):
        return float(deger)

    s = str(deger).strip().replace(" ", "").replace(" ", "")
    if s == "":
        return np.nan

    if "," in s and "." in s:
        # '1.234,56' -> binlik ayracı nokta, ondalık ayracı virgül
        s = s.replace(".", "").replace(",", ".")
    elif "," in s:
        # '1234,56' -> ondalık ayracı virgül
        s = s.replace(",", ".")
    elif re.fullmatch(r"-?\d{1,3}(\.\d{3})+", s):
        # '1.250' veya '12.345.678' -> yalnızca binlik ayracı olarak nokta
        s = s.replace(".", "")

    try:
        return float(s)
    except ValueError:
        return np.nan


def load_data(uploaded_file, m=None):
    """
    Opsiyonel olarak yüklenen dosyayı (CSV veya Excel) okuyup DataFrame döndürür.
    Hata durumunda (bozuk dosya, desteklenmeyen biçim vb.) (None, hata_mesajı) döndürür.
    """
    m = m or i18n.METINLER["tr"]
    if uploaded_file is None:
        return None, m["dosya_secilmedi"]

    dosya_adi = uploaded_file.name.lower()

    try:
        if dosya_adi.endswith(".csv"):
            # Türkçe Excel çıktılarında genellikle ';' ayracı ve ',' ondalık kullanılır.
            # Önce standart virgül ayraçla denenir, tek sütun çıkarsa noktalı virgül denenir.
            try:
                df = pd.read_csv(uploaded_file)
                if df.shape[1] == 1:
                    uploaded_file.seek(0)
                    df = pd.read_csv(uploaded_file, sep=";", decimal=",")
            except Exception:
                uploaded_file.seek(0)
                df = pd.read_csv(uploaded_file, sep=";", decimal=",")
        elif dosya_adi.endswith((".xlsx", ".xls")):
            df = pd.read_excel(uploaded_file)
        else:
            return None, m["format_desteklenmiyor"]
    except Exception as e:
        return None, m["dosya_hata"].format(hata=e)

    if df is None or df.empty:
        return None, m["dosya_bos"]

    df.columns = [str(c).strip() for c in df.columns]
    return df, None


def clean_numeric_columns(df, columns, m=None):
    """
    Belirtilen sütunları sayısal tipe çevirir (Türkçe ondalık biçimleri dâhil).
    Tamamen boş satırlar (yapıştırılmamış şablon satırları) sessizce çıkarılır;
    kısmen eksik veya sayısal olmayan değer içeren satırlar kibarca raporlanıp
    analiz dışı bırakılır. Uygulama hiçbir durumda çökmez.

    Dönüş: (temiz_df, uyarı_mesajları_listesi)
    """
    m = m or i18n.METINLER["tr"]
    uyarilar = []
    calisma_df = df.copy()

    mevcut_sutunlar = [c for c in columns if c in calisma_df.columns]
    for col in mevcut_sutunlar:
        calisma_df[col] = calisma_df[col].map(_sayiya_cevir)

    if not mevcut_sutunlar:
        return calisma_df.iloc[0:0], [m["sutun_bulunamadi"]]

    # Tamamen boş satırlar: doldurulmamış şablon satırları kabul edilir, uyarı verilmez.
    tumu_bos = calisma_df[mevcut_sutunlar].isna().all(axis=1)
    calisma_df = calisma_df.loc[~tumu_bos].reset_index(drop=True)

    toplam_satir = len(calisma_df)
    eksik_maskesi = calisma_df[mevcut_sutunlar].isna().any(axis=1)
    eksik_sayisi = int(eksik_maskesi.sum())

    if eksik_sayisi > 0:
        uyarilar.append(m["eksik_uyari"].format(toplam=toplam_satir, eksik=eksik_sayisi))
        calisma_df = calisma_df.loc[~eksik_maskesi].reset_index(drop=True)

    return calisma_df, uyarilar


def validate_selection(df, y_col, x_cols, m=None):
    """
    Bağımlı (Y) ve bağımsız (X) değişken seçimlerinin geçerliliğini kontrol eder.
    X seçimi boş olabilir: bu durumda analiz, ham tüketim verileri üzerinden
    (referans dönemi ortalaması temel çizgi) yürütülür.
    Dönüş: (gecerli_mi: bool, mesaj: str veya None)
    """
    m = m or i18n.METINLER["tr"]
    if y_col is None:
        return False, m["y_sec_uyari"]

    if y_col in x_cols:
        return False, m["y_x_cakisma"]

    min_gozlem = len(x_cols) + 2  # asgari serbestlik derecesi için
    if len(df) < min_gozlem:
        return False, m["min_gozlem"].format(min_gozlem=min_gozlem, mevcut=len(df))

    return True, None
