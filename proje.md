# PROJE BİLDİRGESİ: Enerji Temel Çizgisi (EnB) Regresyon Analizi ve Raporlama Aracı

## 1. Proje Özeti
Bu proje, endüstriyel tesisler veya binalar için enerji tüketim verileri ile bu tüketimi etkileyen bağımsız değişkenleri (üretim miktarı, ısıtma derece gün (HDD), soğutma derece gün (CDD) vb.) kullanarak Çoklu Doğrusal Regresyon (Multiple Linear Regression) analizi yapan bir yazılımın geliştirilmesini amaçlamaktadır. Yazılım, referans döneme ait temel çizgiyi (baseline) oluşturacak, istatistiksel uygunluğunu test edecek ve reel tüketim verileriyle kıyaslayarak enerji tasarrufunu hesaplayacaktır.

## 2. Teknoloji Yığını (Tavsiye Edilen)
- **Dil:** Python
- **Arayüz:** Streamlit (Veri yükleme, analiz ve grafik gösterimi için)
- **Veri İşleme:** Pandas, NumPy
- **İstatistik ve Regresyon:** Statsmodels veya Scikit-Learn
- **Görselleştirme:** Plotly (Etkileşimli grafikler için)

## 3. Temel Özellikler ve Modüller

### Modül A: Veri Girişi ve Esneklik
- Kullanıcı CSV veya Excel formatında veri yükleyebilmelidir.
- Referans yıl/yıllar esnek olmalıdır (Kullanıcı 1 yıllık veya 5 yıllık geçmiş veriyi seçebilmelidir).
- Kullanıcı, yüklenen veri setinden "Enerji Tüketimi" (Bağımlı Değişken - Y) ve "Etkileyen Değişkenleri" (Bağımsız Değişkenler - X1, X2, Xn) arayüz üzerinden seçebilmelidir.
- Raporlama (kıyaslama) dönemi verileri ayrı bir set olarak veya aynı tablonun devamı olarak seçilebilmelidir.

### Modül B: İstatistiksel Analiz ve Eşik Değerler (Model Doğrulama)
Model kurulduktan sonra aşağıdaki istatistiksel parametreler hesaplanmalı, arayüzde bir tablo halinde gösterilmeli ve modelin geçerliliği "Kabul/Ret" olarak belirtilmelidir:

- **R² (Belirtme Katsayısı):** Eşik değer >= 0.75
- **Düzeltilmiş R² (Adj. R²):** Değişken sayısına göre ceza uygulanan değer.
- **Standart Hata (Standard Error):** Mümkün olduğunca düşük olmalı.
- **p-değeri (P-value):** Her bir bağımsız değişken için <= 0.05 olmalıdır (0.05'ten büyükse o değişkenin anlamsız olduğu kullanıcıya bildirilmeli).
- **F-İstatistiği (F-Test):** Modelin genel anlamlılığı p < 0.05 eşiği ile test edilmeli.
- **RMSE (Kök Ortalama Kare Hata):** Hata payının mutlak değeri.
- **NRMSE (Normalize RMSE):** Veri aralığına bölünmüş hata oranı.
- **CV-RMSE (RMSE Varyasyon Katsayısı):** Eşik değer <= %15 (Aylık veriler için IPMVP/ASHRAE standardı).

Eğer p-değeri, R² ve CV-RMSE eşik değerleri sağlıyorsa sistem "Temel Çizgi Oluşturmaya Uygundur" onayı vermelidir.

### Modül C: Formül Çıktısı ve Temel Çizgi Oluşturma
- Model onay alırsa, sistem arka planda oluşturduğu matematiksel formülü kullanıcıya açıkça göstermelidir. 
  Örnek format: E = β0 + (β1 * X1) + (β2 * X2)
- Formüldeki katsayılar (β) ve kesişim noktası (Intercept) net olarak belirtilmelidir.

### Modül D: Kıyaslama ve Performans Ölçümü (CUSUM ve Tasarruf)
- Oluşturulan formül, raporlama (reel) dönemindeki bağımsız değişken verilerine uygulanarak "Beklenen Enerji Tüketimi" hesaplanmalıdır.
- Kullanıcının girdiği "Gerçekleşen Enerji Tüketimi" ile "Beklenen Tüketim" kıyaslanmalıdır.
- Her bir dönem (örneğin aylar) için fark alınarak "Tasarruf Sağlanan Bölümler" (Pozitif fark) ve "Tasarruf Sağlanamayan/Aşım Olan Bölümler" (Negatif fark) hesaplanmalıdır.
- Kümülatif Tasarruf (CUSUM - Kümülatif Toplam) hesabı yapılmalıdır.

### Modül E: Raporlama ve Görselleştirme
Sistem aşağıdaki çıktıları interaktif olarak sunmalıdır:
1. **İstatistiksel Geçerlilik Tablosu:** Hedeflenen eşikler ve gerçekleşen değerler.
2. **Kıyaslama Tablosu:** Dönem, Gerçek Tüketim, Beklenen Tüketim, Sapma Miktarı, CUSUM.
3. **Çizgi Grafiği 1:** Gerçek Tüketim vs Beklenen Tüketim (Zaman çizelgesinde yan yana).
4. **Çizgi Grafiği 2 (CUSUM):** Kümülatif tasarrufu gösteren, sıfır çizgisinin altı ve üstünü vurgulayan performans grafiği.

## 4. Geliştirici İçin Sistem Talimatları
- Kod modüler, temiz ve yorum satırlarıyla açıklanmış olmalıdır.
- Beklenmedik durumlarda (örneğin eksik veri, "NaN" değerleri) sistem çökmemeli, veriyi temizlemeli veya kullanıcıya uyarı vermelidir.
- Çıktılar ve arayüz Türkçe olmalıdır.
- İstatistik hesabı için `statsmodels.api` kütüphanesinin OLS metodu, detaylı istatistiksel verileri tek seferde verdiği için tercih edilmelidir.