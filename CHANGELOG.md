# CHANGELOG — ATLASCert® EnB Analiz ve Raporlama Portalı

Tüm versiyonlar arasındaki önemli değişiklikler bu dosyada belirtilir.

---

## v1.0.0 — Temel Sürüm (Başlangıç)

**Durum:** Streamlit Community Cloud'da canlı yayın başlangıcı.

### Özellikler
- ✅ **Veri Girişi:** Kopyala/yapıştır ızgarası veya CSV/Excel dosya yükleme
- ✅ **Regresyon Analizi:** Çoklu doğrusal regresyon (OLS), IPMVP/ASHRAE standartlarına uygun
- ✅ **Model Doğrulama:** R², CV-RMSE, p-değeri, F-testi eşik kontrolleri
- ✅ **Kıyaslama:** Beklenen vs. gerçek tüketim, CUSUM grafiği, tasarruf hesaplaması
- ✅ **İnteraktif Grafikler:** Plotly (çizgi, bar, donut) tema uyarlanabilir
- ✅ **PDF Rapor:** reportlab + kaleido, A4, 2,5 cm kenar boşluğu
- ✅ **JSON Kayıt Sistemi:** Yerel (JSON dosyası) / Bulut (indir/yükle)
- ✅ **İki Dil:** Türkçe (varsayılan) / İngilizce
- ✅ **Minimalist Tasarım:** Kurumsal renkler, st.metric kartları, st.divider

---

## v1.1.0 — HTML Rapor + Sürüm Takibi + Uyku Bildirimi

**Tarih:** 2026-07-07  
**Durum:** Kullanıcı deneyimi iyileştirmesi, çevrimdışı raporlama, sürüm takibi

### Yeni Özellikler
- ✅ **Sürüm Numarası:** Alt bilgiye semantik sürüm (v1.1.0) eklendi
- ✅ **Uyku Bildirimi:** Streamlit Cloud uyku modundan çıkış süresi hakkında bilgilendirici mesaj
- ✅ **HTML Rapor:** Sunucu gerektirmeyen, çevrimdışı çalışan interaktif rapor
  - Plotly grafikleri tam interaktif (zoom, hover, legend toggle)
  - Tüm Plotly JS (~4 MB) HTML'e gömülü (CDN'e istek yok)
  - Logo base64 data-URI'ye kodlanmış
  - Baskı/PDF yazdırma desteği CSS `@media print`
  - Tüm HTML tamamen bağımsız, başka dosya/bağlantı gerekmez

### Değişiklikler
- `modules/i18n.py`:
  - Yeni anahtar: `uyku_uyari` (tr/en)
  - Yeni anahtar: `rapor_indir_html` (tr/en)
  - Yeni anahtar: `rapor_dosya_adi_html` (tr/en)
  - `footer_html`: sürüm placeholder `{surum}` eklendi
  - `rapor_aciklama`: HTML rapor seçeneğinden bahsedecek şekilde güncellendi

- `modules/html_report.py` (YENİ):
  - `build_html()` fonksiyonu: PDF ile aynı girdileri alıp HTML bytes üretir
  - Interaktif Plotly grafikleri (`plotly.io.to_html`)
  - Kurumsal stil CSS (PDF'deki renkler, yazı tipi, düzen)
  - Logo base64 kodlaması, tam çevrimdışı çalışma

- `app.py`:
  - `SURUM = "1.1.0"` sabiti eklendi (satır ~186)
  - `from modules import ... html_report` importu eklendi
  - Başlık altına `st.info(M["uyku_uyari"])` eklendi (satır ~266)
  - Footer: `M["footer_html"].format(surum=SURUM)` (satır ~1129)
  - Rapor üretim bloğu: PDF hemen ardından HTML da üretiliyor (satır ~1104)
  - İndirme düğmeleri: yan yana `st.columns(2)` düzeni (satır ~1119)

### Bilinen Limitasyonlar
- Streamlit Cloud uyku modu hala etkindir (ilk açılışta ~1-3 dakika bekleme).
  Hibrit sistem bunu *tamamen* ortadan kaldırmaz, ancak rapor bir kez
  indirildiğinde sunucu gerekmediği için pratikte sorunu hafifletir.

### Doğrulama Edildi
- ✅ Yerel Streamlit sunucusu normal çalışır
- ✅ Demo modu (`?demo=1`) başlıkta uyku bildirimine ve footer'da sürüme bakıyor
- ✅ HTML rapor indiriliyor, tarayıcıda çevrimdışı açılıyor, tüm grafikler interaktif
- ✅ PDF rapor önceki davranışla birebir aynı
- ✅ Dil değiştirme (Türkçe/İngilizce) tüm bölümlerde çalışıyor

### Sonraki Adımlar (v1.2.0+)
- Opsiyonel: Grafikler statik PNG resimler olarak da HTML'ye eklenebilir
  (dosya boyutu küçük ama interaktivite kaybı)
- Opsiyonel: Kalkulo geçmişi ("Previous Analyses") bölümü
- Opsiyonel: Veri dışa aktarımı (Excel şablonu, veri yineleme şablonu)
