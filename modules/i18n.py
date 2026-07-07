"""
İki dilli (Türkçe / İngilizce) arayüz metinleri.
================================================
Tüm kullanıcıya görünen metinler bu modülde tutulur; uygulama ve diğer
modüller metinlere METINLER[dil][anahtar] üzerinden erişir.
"""

METINLER = {
    "tr": {
        # Genel / veri sütunları
        "aylar": ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran",
                  "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"],
        "donem": "Dönem",
        "gercek": "Gerçek Tüketim",
        "beklenen": "Beklenen Tüketim",
        "sapma": "Sapma (Tasarruf + / Aşım -)",
        "durum": "Durum",
        "tasarruf_saglandi": "Tasarruf Sağlandı",
        "asim_olustu": "Aşım Oluştu",
        "tum_donem": "Tüm Dönem",
        "donem_etiket": "Dönem {n}",

        # Sayfa
        "sayfa_basligi": "ATLASCert® — Enerji Temel Çizgisi (EnB) Analiz ve Raporlama Portalı",
        "portal_basligi": "Enerji Temel Çizgisi (EnB) Analiz ve Raporlama Portalı",
        "alt_baslik": "IPMVP ve ASHRAE Guideline 14 ile uyumlu çoklu doğrusal regresyon yöntemiyle "
                      "enerji temel çizgisi (baseline) oluşturma, doğrulama ve tasarruf raporlama",
        "dil_label": "Dil / Language",

        # Bölüm 1 — Veri Girişi
        "b1": "1. Veri Girişi",
        "giris_aciklama": "Önce dönem aralığını (başlangıç ve bitiş ay/yıl) seçin; tablo, aralıktaki tüm "
                          "dönemler hazır olarak aşağıda belirir. Ardından Excel'den kopyaladığınız "
                          "**Enerji Tüketimi** ve **Bağımsız Değişken** (Üretim, HDD, CDD vb.) verilerini "
                          "ilgili sütunlara doğrudan yapıştırabilirsiniz.",
        "sutun_ozellestir": "Tablo sütunlarını özelleştirin",
        "sutun_ipucu": "Sütun adlarını, değişken sayısını veya dili dilediğiniz zaman değiştirebilirsiniz; "
                       "girdiğiniz veriler korunur.",
        "tuketim_sutun_label": "Enerji tüketimi sütununun adı",
        "tuketim_varsayilan": "Tüketim (kWh)",
        "degisken_sayisi_label": "Bağımsız değişken sayısı",
        "degisken_adi_label": "{i}. değişkenin adı",
        "degisken_varsayilan": "Değişken {i}",
        "aralik_baslik": "**Dönem aralığı** (yalnızca ay ve yıl seçin)",
        "bas_ay": "Başlangıç ayı",
        "bas_yil": "Başlangıç yılı",
        "bit_ay": "Bitiş ayı",
        "bit_yil": "Bitiş yılı",
        "ters_aralik": "Bitiş dönemi, başlangıç döneminden önce olamaz. Lütfen aralığı kontrol edin.",
        "ayni_ad_hatasi": "Sütun adları birbirinden farklı olmalıdır. Lütfen aynı adı taşıyan sütunları "
                          "yeniden adlandırın.",
        "alternatif_expander": "Alternatif: dosyadan yükleme (CSV / Excel)",
        "dosya_upload_label": "Dilerseniz veri setinizi dosya olarak da yükleyebilirsiniz.",
        "dosya_okundu": "Dosya başarıyla okundu: {satir} satır, {sutun} sütun.",
        "y_label": "Bağımlı değişken (Y) — Enerji Tüketimi",
        "x_label": "Bağımsız değişkenler (X) — Üretim, HDD, CDD vb.",
        "donem_sutun_label": "Dönem / tarih sütunu (isteğe bağlı, grafiklerde etiket olarak kullanılır)",
        "donem_yok": "Yok (otomatik numaralandır)",
        "seciniz": "Seçiniz...",
        "demo_bilgi": "Örnek veri modu etkin (?demo=1). Gerçek analiz için adres çubuğundan bu "
                      "parametreyi kaldırın.",
        "secilen_aralik": "Seçilen aralık: {ilk} – {son} ({adet} dönem). Dönem sütunu otomatik "
                          "doldurulur ve düzenlenemez; aralığı değiştirseniz bile girdiğiniz veriler korunur.",
        "donem_help": "Seçilen aralığa göre otomatik oluşturuldu",
        "tuketim_help": "Dönemlik enerji tüketimi",
        "degisken_help": "Bağımsız değişken (Üretim, HDD, CDD vb.)",
        "x_model_label": "Modelde kullanılacak bağımsız değişkenler (X)",
        "veri_bekleniyor": "Analize başlamak için lütfen tabloya veri girin veya yapıştırın.",

        # Bölüm 2 — Referans dönemi
        "b2": "2. Referans (Baseline) Dönemi Aralığı",
        "slider_label": "Referans (baseline) dönemi olarak kullanılacak satır sayısı (baştan itibaren)",
        "slider_help": "1 yıllık (örn. 12 satır) veya 5 yıllık (örn. 60 satır) geçmiş veriyi referans "
                       "dönemi olarak seçebilirsiniz; kalan satırlar raporlama (kıyaslama) dönemi için "
                       "kullanılabilir. Alt sınırın {min_ref} olmasının nedeni istatistikseldir: {kx} "
                       "bağımsız değişkenli bir regresyon modelinin kurulabilmesi için gözlem sayısının "
                       "değişken sayısından en az 2 fazla ({min_ref}) olması gerekir; daha az gözlemle "
                       "model matematiksel olarak çözülemez.",
        "referans_caption": "Referans dönemi: {ref} satır • Aynı tablodan raporlama dönemi için "
                            "ayrılabilecek veri: {kalan} satır",
        "yetersiz_veri": "Temizleme sonrasında kalan {satir} satır, {kx} değişkenli bir model için "
                         "yeterli değil (en az {min_ref} satır gereklidir). Lütfen veri ekleyin.",

        # Bölüm 3 — İstatistiksel analiz
        "b3": "3. İstatistiksel Analiz ve Model Doğrulama",
        "r2_metric": "R² (Determinasyon Katsayısı)",
        "adjr2_metric": "Düzeltilmiş R²",
        "cv_metric": "CV(RMSE)",
        "fp_metric": "F-testi p-değeri",
        "r2_help": "IPMVP / ASHRAE Guideline 14 eşiği: ≥ {esik}",
        "adjr2_help": "Değişken sayısına göre düzeltilmiş determinasyon katsayısı (bilgi amaçlı)",
        "cv_help": "Varyasyon katsayısı; ASHRAE Guideline 14 eşiği: ≤ %{esik}",
        "fp_help": "Modelin bütünsel anlamlılığı; eşik: p < {esik}",
        "ayrintili_expander": "Ayrıntılı istatistiksel geçerlilik tablosu",
        "anlamsiz_uyari": "Şu değişkenlerin p-değeri 0.05 eşiğinin üzerinde olduğu için istatistiksel "
                          "olarak anlamlı kabul edilmemektedir: {degiskenler}. Bu değişkenleri modelden "
                          "çıkarmayı değerlendirebilirsiniz.",
        "model_uygun": "Model sonucu: Enerji temel çizgisi (EnB) oluşturmaya **uygundur**.",
        "model_uygun_degil": "Model sonucu: Enerji temel çizgisi (EnB) oluşturmaya **uygun değildir**. "
                             "Değişken seçimini veya referans dönemi aralığını gözden geçirmenizi öneririz.",
        "regresyon_hatasi": "Regresyon modeli kurulurken bir sorun oluştu: {hata}",

        # İstatistiksel geçerlilik tablosu (regression modülü)
        "olcut": "Ölçüt",
        "esik_deger": "Eşik Değer",
        "hesaplanan": "Hesaplanan Değer",
        "sonuc": "Sonuç",
        "uygun": "Uygun",
        "uygun_degil": "Uygun Değil",
        "bilgi_amacli": "Bilgi amaçlı",
        "dusuk_olmali": "Mümkün olduğunca düşük",
        "hesaplanamadi": "Hesaplanamadı",
        "r2_adi": "R² (Determinasyon Katsayısı)",
        "adjr2_adi": "Düzeltilmiş R² (Adjusted R²)",
        "see_adi": "Tahminin Standart Hatası (SEE)",
        "p_adi": "p-değeri (bağımsız değişkenler)",
        "f_adi": "F-istatistiği (Modelin Anlamlılığı)",
        "rmse_adi": "RMSE (Hata Karelerinin Ortalamasının Karekökü)",
        "nrmse_adi": "NRMSE (Normalize Edilmiş RMSE)",
        "cv_adi": "CV(RMSE) — Varyasyon Katsayısı",
        "cv_esik": "≤ %{esik} (ASHRAE Guideline 14)",
        "f_esik": "p < {esik}",

        # Bölüm 4 — Formül
        "b4": "4. Model Formülü ve Katsayılar",
        "katsayi_degisken": "Değişken",
        "katsayi": "Katsayı",
        "p_degeri": "p-değeri",
        "kesisim": "Kesişim Terimi (β0)",
        "temkin_bilgi": "Model istatistiksel eşikleri sağlamadığı için aşağıdaki kıyaslama ve grafik "
                        "bölümleri yine de görüntülenecektir; ancak sonuçları yorumlarken lütfen "
                        "temkinli olun.",

        # Bölüm 5 — Raporlama dönemi
        "b5": "5. Raporlama (Kıyaslama) Dönemi Verisi",
        "kaynak_label": "Raporlama dönemi verisinin kaynağı",
        "kaynak_ayni": "Aynı tablonun kalan satırları",
        "kaynak_ayri": "Ayrı bir tablo olarak girin",
        "rap_aciklama": "Raporlama (reel) dönemi aralığını seçin; tablo dönem etiketleriyle birlikte "
                        "aşağıda belirir. Veri sütunları: **{y}** (gerçek tüketim), {xler}.",
        "rap_aciklama_dosya": "Raporlama (reel) dönemine ait verileri aşağıdaki tabloya yapıştırın. "
                              "Sütunlar: **{donem}**, **{y}** (gerçek tüketim), {xler}.",
        "rap_bekleniyor": "Kıyaslama tablosu ve grafikler için raporlama dönemi verisi bekleniyor.",
        "kiyaslama_baslik": "Kıyaslama Tablosu",
        "toplam_tasarruf": "Toplam Tasarruf",
        "toplam_asim": "Toplam Aşım",
        "net_tasarruf": "Net Tasarruf",
        "net_tasarruf_yuzde": "Net Tasarruf Yüzdesi",

        # Bölüm 6 — Grafikler
        "b6": "6. Grafikler",
        "cusum_caption": "Yeşil çubuklar kümülatif tasarrufun pozitif olduğu (tasarruf sağlanan) "
                         "dönemleri, kırmızı çubuklar kümülatif tasarrufun negatif olduğu (aşım oluşan) "
                         "dönemleri gösterir.",
        "yillik_baslik": "Yıllık Tasarruf Dağılımı",
        "halka_caption": "Her halka, ilgili yılın beklenen (temel çizgi) tüketim toplamını temsil eder; "
                         "yeşil dilim net tasarrufun bu toplam içindeki payını gösterir. Net tasarrufun "
                         "negatif olduğu yıllarda halka, gerçek tüketim içindeki aşım payını kırmızı "
                         "dilimle gösterir.",
        "g1_baslik": "Gerçek Tüketim ve Beklenen Tüketim Kıyaslaması",
        "seri_gercek": "Gerçek Tüketim",
        "seri_beklenen": "Beklenen Tüketim (Model)",
        "cusum_baslik": "CUSUM — Kümülatif Tasarruf Performansı",
        "cusum_poz": "Tasarruf (CUSUM ≥ 0)",
        "cusum_neg": "Aşım (CUSUM < 0)",
        "halka_baslik": "Yıllık Tasarruf Dağılımı — Beklenen Tüketim İçindeki Pay",
        "halka_tasarruf": "Net Tasarruf",
        "halka_asim": "Aşım",
        "merkez_tasarruf": "tasarruf",
        "merkez_asim": "aşım",

        # Veri işleme mesajları (data_handler)
        "dosya_secilmedi": "Herhangi bir dosya seçilmedi.",
        "format_desteklenmiyor": "Bu dosya biçimi desteklenmiyor. Lütfen CSV veya Excel (.xlsx) dosyası yükleyin.",
        "dosya_hata": "Dosya okunurken bir sorun oluştu: {hata}",
        "dosya_bos": "Yüklenen dosya boş görünüyor. Lütfen içeriğini kontrol edip yeniden deneyin.",
        "eksik_uyari": "Doldurulmuş {toplam} satırın {eksik} tanesinde eksik veya sayısal olmayan değer "
                       "bulunduğu için bu satırlar analiz dışında bırakıldı.",
        "sutun_bulunamadi": "Seçilen sütunlar veri tablosunda bulunamadı.",
        "y_sec_uyari": "Lütfen bağımlı değişkeni (enerji tüketimi, Y) seçin.",
        "x_sec_uyari": "Lütfen en az bir bağımsız değişken (X) seçin.",
        "y_x_cakisma": "Bağımlı değişken (Y), bağımsız değişkenler (X) arasında yer alamaz.",
        "min_gozlem": "Seçilen değişken sayısına göre en az {min_gozlem} gözlem (satır) gereklidir. "
                      "Mevcut veri: {mevcut} satır. Lütfen veri ekleyin veya değişken sayısını azaltın.",

        # Ham tüketim (ortalama temel çizgi) modu
        "ham_mod_uyari": "Bağımsız değişken seçilmedi: kıyaslama yalnızca tüketim verileri üzerinden, "
                         "referans dönemi ortalaması temel çizgi kabul edilerek yapılıyor. Regresyon "
                         "istatistikleri bu modda uygulanmaz.",
        "ham_mod_oneri": "Öneri: Değişkenler regresyon için uygun değilse, bağımsız değişken (X) "
                         "seçimlerinin tümünü kaldırarak analizi yalnızca ham tüketim verileri "
                         "(referans dönemi ortalaması) üzerinden sürdürebilirsiniz.",
        "ort_metric": "Referans Ortalaması",
        "std_metric": "Standart Sapma",
        "cv_ham_metric": "Değişkenlik Katsayısı (CV)",
        "gozlem_metric": "Gözlem Sayısı",
        "ham_formul": "{y} = {ort}   (referans dönemi ortalaması)",
        "ham_formul_aylik": "{y} = eşleşen ayın referans ortalaması   (aylık eşleştirme)",
        "ham_ozet_baslik": "İstatistiksel Özet (Ham Tüketim Verisi)",
        "temel_cizgi_ort": "Temel Çizgi (Referans Ortalaması)",
        "ham_yontem_label": "Temel çizgi yöntemi",
        "ham_yontem_aylik": "Aylık eşleştirme (önerilen)",
        "ham_yontem_ortalama": "Genel ortalama",
        "ham_yontem_help": "Aylık eşleştirme: her raporlama ayı, referans dönemindeki aynı ayın "
                           "ortalamasıyla kıyaslanır; mevsimsellik korunur (örn. Ocak ↔ Ocak). "
                           "Genel ortalama: tüm raporlama ayları tek bir referans ortalamasıyla "
                           "kıyaslanır; mevsimsellik göstermeyen tüketimler için uygundur.",
        "ay_kolonu": "Ay",

        # Kayıtlar (kaydet / aç)
        "kayitlar_expander": "💾 Kayıtlar — Kaydet / Aç",
        "kayit_adi_label": "Kayıt adı",
        "kaydet_btn": "Kaydet",
        "kayit_ok": "Kayıt oluşturuldu: {ad}",
        "kayit_adi_bos": "Lütfen bir kayıt adı girin.",
        "kayit_sec_label": "Kayıtlı analizler",
        "ac_btn": "Aç",
        "kayit_yok": "Henüz kayıt yok. Analizinizi adlandırıp kaydettiğinizde burada listelenir.",
        "kayit_yuklendi": "Kayıt yüklendi: {ad}",
        "kayit_hata": "Kayıt işlemi sırasında bir sorun oluştu: {hata}",
        "kayit_bulut_bilgi": "Kayıtlar sunucuda saklanmaz: analizinizi JSON dosyası olarak "
                             "bilgisayarınıza indirin, daha sonra aynı dosyayı yükleyerek geri açın.",
        "kayit_indir_btn": "⬇️ Kaydı indir (JSON)",
        "kayit_yukle_label": "Kayıt dosyası yükle (JSON)",

        # CSV dışa aktarma
        "csv_indir": "⬇️ Tabloyu CSV olarak indir (Excel uyumlu)",
        "csv_giris_dosya": "veri_girisi.csv",
        "csv_kiyaslama_dosya": "kiyaslama_tablosu.csv",

        # PDF raporu
        "rapor_baslik": "7. Rapor",
        "rapor_aciklama": "Analizin tamamını (veriler, istatistikler, formül, kıyaslama ve grafikler) "
                          "her kenardan 2,5 cm boşluklu A4 sayfa düzeninde, tarayıcı ayarlarından "
                          "bağımsız bir PDF dosyası olarak indirebilirsiniz. Ayrıca, sunucu gerektirmeyen, "
                          "tarayıcıda çevrimdışı açılabilen ve interaktif grafiklere sahip bir HTML rapor da indirebilirsiniz.",
        "rapor_olustur": "📄 PDF raporu oluştur",
        "rapor_indir": "PDF raporunu indir",
        "rapor_indir_html": "📊 HTML raporunu indir",
        "rapor_hazirlaniyor": "Rapor hazırlanıyor...",
        "rapor_hata": "Rapor oluşturulurken bir sorun oluştu: {hata}",
        "rapor_dosya_adi": "ATLASCert_EnB_Raporu.pdf",
        "rapor_dosya_adi_html": "ATLASCert_EnB_Raporu.html",
        "rapor_tarih": "Rapor tarihi",
        "rapor_giris_tablosu": "Giriş Verileri",
        "rapor_gecerlilik": "İstatistiksel Geçerlilik Tablosu",

        # Alt bilgi
        "footer_metin": "© 2026 ATLASCert®. Tüm hakları saklıdır. ATLASCert® tescilli bir markadır. "
                        "Analiz yöntemleri IPMVP ve ASHRAE Guideline 14 ilkeleri esas alınarak hazırlanmıştır.",
        "footer_html": """
            <div style="text-align:center; color:#898781; font-size:0.85rem; line-height:1.7; padding:0.5rem 0 1.5rem 0;">
                <span style="color:#104281; font-weight:600;">ATLASCert®</span>
                — Enerji Temel Çizgisi (EnB) Analiz ve Raporlama Portalı<br>
                © 2026 ATLASCert®. Tüm hakları saklıdır. ATLASCert® tescilli bir markadır.<br>
                Analiz yöntemleri IPMVP ve ASHRAE Guideline 14 ilkeleri esas alınarak hazırlanmıştır.<br>
                <span style="font-size:0.9em;">Sürüm: v{surum}</span>
            </div>
        """,
        "yasal_uyari": "© 2026 ATLASCert®. Bu yazılım, sektör profesyonellerine yardımcı olmak "
                       "amacıyla geliştirilmiş ve erişime sunulmuştur. Yazılımın izinsiz klonlanması, "
                       "farklı markalar altında sunulması veya başka kurum platformlarında yayınlanması "
                       "kesinlikle yasaktır. Tüm fikri mülkiyet hakları saklıdır.",

        # Uyku bildirimi
        "uyku_uyari": "⏰ **Önemli:** Bu portal, barındırma hizmeti tarafından uzun süre kullanılmadığında uyku moduna alınır. "
                      "Sayfayı ilk açtığınızda veya uzun bir aradan sonra 'Yes, get this app back up!' düğmesine basıp yaklaşık 1-3 dakika "
                      "beklemeniz gerekebilir; bu tek seferlik bir başlatma süresidir. Uygulama bir kez başladığında normal şekilde çalışır.",
    },

    "en": {
        # General / data columns
        "aylar": ["January", "February", "March", "April", "May", "June",
                  "July", "August", "September", "October", "November", "December"],
        "donem": "Period",
        "gercek": "Actual Consumption",
        "beklenen": "Expected Consumption",
        "sapma": "Deviation (Savings + / Overrun -)",
        "durum": "Status",
        "tasarruf_saglandi": "Savings Achieved",
        "asim_olustu": "Overrun Occurred",
        "tum_donem": "Entire Period",
        "donem_etiket": "Period {n}",

        # Page
        "sayfa_basligi": "ATLASCert® — Energy Baseline (EnB) Analysis and Reporting Portal",
        "portal_basligi": "Energy Baseline (EnB) Analysis and Reporting Portal",
        "alt_baslik": "Energy baseline development, validation and savings reporting with multiple "
                      "linear regression, in accordance with IPMVP and ASHRAE Guideline 14",
        "dil_label": "Dil / Language",

        # Section 1 — Data Entry
        "b1": "1. Data Entry",
        "giris_aciklama": "First select the period range (start and end month/year); the table appears "
                          "below with all periods pre-filled. Then paste your **Energy Consumption** and "
                          "**Independent Variable** (Production, HDD, CDD etc.) data copied from Excel "
                          "directly into the corresponding columns.",
        "sutun_ozellestir": "Customise table columns",
        "sutun_ipucu": "You may change column names, the number of variables or the language at any "
                       "time; the data you have entered is preserved.",
        "tuketim_sutun_label": "Name of the energy consumption column",
        "tuketim_varsayilan": "Consumption (kWh)",
        "degisken_sayisi_label": "Number of independent variables",
        "degisken_adi_label": "Name of variable {i}",
        "degisken_varsayilan": "Variable {i}",
        "aralik_baslik": "**Period range** (select month and year only)",
        "bas_ay": "Start month",
        "bas_yil": "Start year",
        "bit_ay": "End month",
        "bit_yil": "End year",
        "ters_aralik": "The end period cannot be earlier than the start period. Please check the range.",
        "ayni_ad_hatasi": "Column names must be unique. Please rename the duplicated columns.",
        "alternatif_expander": "Alternative: load from file (CSV / Excel)",
        "dosya_upload_label": "You may also upload your data set as a file.",
        "dosya_okundu": "File read successfully: {satir} rows, {sutun} columns.",
        "y_label": "Dependent variable (Y) — Energy Consumption",
        "x_label": "Independent variables (X) — Production, HDD, CDD etc.",
        "donem_sutun_label": "Period / date column (optional, used as labels in charts)",
        "donem_yok": "None (number automatically)",
        "seciniz": "Select...",
        "demo_bilgi": "Sample data mode is active (?demo=1). Remove this parameter from the address "
                      "bar for a real analysis.",
        "secilen_aralik": "Selected range: {ilk} – {son} ({adet} periods). The Period column is filled "
                          "automatically and cannot be edited; your data is preserved even if you "
                          "change the range.",
        "donem_help": "Generated automatically from the selected range",
        "tuketim_help": "Energy consumption per period",
        "degisken_help": "Independent variable (Production, HDD, CDD etc.)",
        "x_model_label": "Independent variables (X) to be used in the model",
        "veri_bekleniyor": "Please enter or paste data into the table to start the analysis.",

        # Section 2 — Baseline period
        "b2": "2. Baseline Period Range",
        "slider_label": "Number of rows to be used as the baseline period (from the top)",
        "slider_help": "You may select one year (e.g. 12 rows) or five years (e.g. 60 rows) of "
                       "historical data as the baseline period; the remaining rows can be used for the "
                       "reporting period. The lower limit of {min_ref} is statistical: fitting a "
                       "regression model with {kx} independent variable(s) requires at least the number "
                       "of variables plus 2 ({min_ref}) observations; with fewer observations the model "
                       "cannot be solved.",
        "referans_caption": "Baseline period: {ref} rows • Data available for the reporting period from "
                            "the same table: {kalan} rows",
        "yetersiz_veri": "The {satir} rows remaining after cleaning are not sufficient for a model with "
                         "{kx} variable(s) (at least {min_ref} rows are required). Please add data.",

        # Section 3 — Statistical analysis
        "b3": "3. Statistical Analysis and Model Validation",
        "r2_metric": "R² (Coefficient of Determination)",
        "adjr2_metric": "Adjusted R²",
        "cv_metric": "CV(RMSE)",
        "fp_metric": "F-test p-value",
        "r2_help": "IPMVP / ASHRAE Guideline 14 threshold: ≥ {esik}",
        "adjr2_help": "Coefficient of determination adjusted for the number of variables (informative)",
        "cv_help": "Coefficient of variation; ASHRAE Guideline 14 threshold: ≤ {esik}%",
        "fp_help": "Overall model significance; threshold: p < {esik}",
        "ayrintili_expander": "Detailed statistical validity table",
        "anlamsiz_uyari": "The following variables are not considered statistically significant because "
                          "their p-values exceed the 0.05 threshold: {degiskenler}. You may consider "
                          "removing them from the model.",
        "model_uygun": "Model result: **suitable** for establishing an energy baseline (EnB).",
        "model_uygun_degil": "Model result: **not suitable** for establishing an energy baseline (EnB). "
                             "We recommend reviewing the variable selection or the baseline period range.",
        "regresyon_hatasi": "A problem occurred while fitting the regression model: {hata}",

        # Statistical validity table (regression module)
        "olcut": "Criterion",
        "esik_deger": "Threshold",
        "hesaplanan": "Calculated Value",
        "sonuc": "Result",
        "uygun": "Compliant",
        "uygun_degil": "Non-compliant",
        "bilgi_amacli": "Informative",
        "dusuk_olmali": "As low as possible",
        "hesaplanamadi": "Not available",
        "r2_adi": "R² (Coefficient of Determination)",
        "adjr2_adi": "Adjusted R²",
        "see_adi": "Standard Error of the Estimate (SEE)",
        "p_adi": "p-value (independent variables)",
        "f_adi": "F-statistic (Model Significance)",
        "rmse_adi": "RMSE (Root Mean Square Error)",
        "nrmse_adi": "NRMSE (Normalised RMSE)",
        "cv_adi": "CV(RMSE) — Coefficient of Variation",
        "cv_esik": "≤ {esik}% (ASHRAE Guideline 14)",
        "f_esik": "p < {esik}",

        # Section 4 — Formula
        "b4": "4. Model Formula and Coefficients",
        "katsayi_degisken": "Variable",
        "katsayi": "Coefficient",
        "p_degeri": "p-value",
        "kesisim": "Intercept (β0)",
        "temkin_bilgi": "Although the model does not meet the statistical thresholds, the comparison and "
                        "chart sections below will still be displayed; please interpret the results "
                        "with caution.",

        # Section 5 — Reporting period
        "b5": "5. Reporting Period Data",
        "kaynak_label": "Source of the reporting period data",
        "kaynak_ayni": "Remaining rows of the same table",
        "kaynak_ayri": "Enter as a separate table",
        "rap_aciklama": "Select the reporting period range; the table appears below with period labels. "
                        "Data columns: **{y}** (actual consumption), {xler}.",
        "rap_aciklama_dosya": "Paste the reporting period data into the table below. "
                              "Columns: **{donem}**, **{y}** (actual consumption), {xler}.",
        "rap_bekleniyor": "Waiting for reporting period data for the comparison table and charts.",
        "kiyaslama_baslik": "Comparison Table",
        "toplam_tasarruf": "Total Savings",
        "toplam_asim": "Total Overrun",
        "net_tasarruf": "Net Savings",
        "net_tasarruf_yuzde": "Net Savings Percentage",

        # Section 6 — Charts
        "b6": "6. Charts",
        "cusum_caption": "Green bars indicate periods where cumulative savings are positive (savings "
                         "achieved); red bars indicate periods where cumulative savings are negative "
                         "(overrun).",
        "yillik_baslik": "Annual Savings Distribution",
        "halka_caption": "Each ring represents the total expected (baseline) consumption of the year; "
                         "the green slice shows the share of net savings within this total. For years "
                         "with negative net savings, the ring shows the overrun share within actual "
                         "consumption as a red slice.",
        "g1_baslik": "Actual vs Expected Consumption",
        "seri_gercek": "Actual Consumption",
        "seri_beklenen": "Expected Consumption (Model)",
        "cusum_baslik": "CUSUM — Cumulative Savings Performance",
        "cusum_poz": "Savings (CUSUM ≥ 0)",
        "cusum_neg": "Overrun (CUSUM < 0)",
        "halka_baslik": "Annual Savings Distribution — Share of Expected Consumption",
        "halka_tasarruf": "Net Savings",
        "halka_asim": "Overrun",
        "merkez_tasarruf": "savings",
        "merkez_asim": "overrun",

        # Data handling messages (data_handler)
        "dosya_secilmedi": "No file was selected.",
        "format_desteklenmiyor": "This file format is not supported. Please upload a CSV or Excel (.xlsx) file.",
        "dosya_hata": "A problem occurred while reading the file: {hata}",
        "dosya_bos": "The uploaded file appears to be empty. Please check its content and try again.",
        "eksik_uyari": "{eksik} of the {toplam} filled rows contained missing or non-numeric values and "
                       "were excluded from the analysis.",
        "sutun_bulunamadi": "The selected columns could not be found in the data table.",
        "y_sec_uyari": "Please select the dependent variable (energy consumption, Y).",
        "x_sec_uyari": "Please select at least one independent variable (X).",
        "y_x_cakisma": "The dependent variable (Y) cannot be among the independent variables (X).",
        "min_gozlem": "At least {min_gozlem} observations (rows) are required for the selected number "
                      "of variables. Current data: {mevcut} rows. Please add data or reduce the number "
                      "of variables.",

        # Raw consumption (mean baseline) mode
        "ham_mod_uyari": "No independent variables selected: the comparison is based on consumption "
                         "data only, using the baseline period average as the baseline. Regression "
                         "statistics do not apply in this mode.",
        "ham_mod_oneri": "Suggestion: If the variables are not suitable for regression, you can remove "
                         "all independent variable (X) selections and continue the analysis using raw "
                         "consumption data only (baseline period average).",
        "ort_metric": "Baseline Average",
        "std_metric": "Standard Deviation",
        "cv_ham_metric": "Coefficient of Variation (CV)",
        "gozlem_metric": "Number of Observations",
        "ham_formul": "{y} = {ort}   (baseline period average)",
        "ham_formul_aylik": "{y} = reference average of the matching month   (monthly matching)",
        "ham_ozet_baslik": "Statistical Summary (Raw Consumption Data)",
        "temel_cizgi_ort": "Baseline (Reference Average)",
        "ham_yontem_label": "Baseline method",
        "ham_yontem_aylik": "Monthly matching (recommended)",
        "ham_yontem_ortalama": "Overall average",
        "ham_yontem_help": "Monthly matching: each reporting month is compared with the average of "
                           "the same month in the baseline period; seasonality is preserved "
                           "(e.g. January ↔ January). Overall average: all reporting months are "
                           "compared with a single baseline average; suitable for non-seasonal "
                           "consumption.",
        "ay_kolonu": "Month",

        # Records (save / open)
        "kayitlar_expander": "💾 Records — Save / Open",
        "kayit_adi_label": "Record name",
        "kaydet_btn": "Save",
        "kayit_ok": "Record saved: {ad}",
        "kayit_adi_bos": "Please enter a record name.",
        "kayit_sec_label": "Saved analyses",
        "ac_btn": "Open",
        "kayit_yok": "No records yet. Name and save your analysis to see it listed here.",
        "kayit_yuklendi": "Record loaded: {ad}",
        "kayit_hata": "A problem occurred during the record operation: {hata}",
        "kayit_bulut_bilgi": "Records are not stored on the server: download your analysis as a "
                             "JSON file and re-open it later by uploading the same file.",
        "kayit_indir_btn": "⬇️ Download record (JSON)",
        "kayit_yukle_label": "Upload record file (JSON)",

        # CSV export
        "csv_indir": "⬇️ Download table as CSV (Excel-friendly)",
        "csv_giris_dosya": "input_data.csv",
        "csv_kiyaslama_dosya": "comparison_table.csv",

        # PDF report
        "rapor_baslik": "7. Report",
        "rapor_aciklama": "You can download the complete analysis (data, statistics, formula, "
                          "comparison and charts) as a PDF file with an A4 page layout and 2.5 cm "
                          "margins on all sides, independent of browser settings. Additionally, you can also download "
                          "an interactive HTML report that works offline in your browser without requiring a server.",
        "rapor_olustur": "📄 Generate PDF report",
        "rapor_indir": "Download PDF report",
        "rapor_hazirlaniyor": "Preparing the report...",
        "rapor_hata": "A problem occurred while generating the report: {hata}",
        "rapor_dosya_adi": "ATLASCert_EnB_Report.pdf",
        "rapor_dosya_adi_html": "ATLASCert_EnB_Report.html",
        "rapor_tarih": "Report date",
        "rapor_giris_tablosu": "Input Data",
        "rapor_gecerlilik": "Statistical Validity Table",

        # Footer
        "footer_metin": "© 2026 ATLASCert®. All rights reserved. ATLASCert® is a registered trademark. "
                        "Analysis methods are based on the principles of IPMVP and ASHRAE Guideline 14.",
        "footer_html": """
            <div style="text-align:center; color:#898781; font-size:0.85rem; line-height:1.7; padding:0.5rem 0 1.5rem 0;">
                <span style="color:#104281; font-weight:600;">ATLASCert®</span>
                — Energy Baseline (EnB) Analysis and Reporting Portal<br>
                © 2026 ATLASCert®. All rights reserved. ATLASCert® is a registered trademark.<br>
                Analysis methods are based on the principles of IPMVP and ASHRAE Guideline 14.<br>
                <span style="font-size:0.9em;">Version: v{surum}</span>
            </div>
        """,
        "yasal_uyari": "© 2026 ATLASCert®. This software has been developed and made available to "
                       "assist industry professionals. Unauthorized cloning of the software, offering "
                       "it under different brands, or publishing it on other corporate platforms is "
                       "strictly prohibited. All intellectual property rights reserved.",

        # Sleep notification
        "uyku_uyari": "⏰ **Important:** This portal may be put to sleep by the hosting service if not used for an extended period. "
                      "When you first open the page or after a long break, you may need to click 'Yes, get this app back up!' and "
                      "wait approximately 1-3 minutes; this is a one-time startup delay. Once the app has started, it works normally.",

        "rapor_indir_html": "📊 Download HTML report",
    },
}


def metinler(dil):
    """Seçilen dilin metin sözlüğünü döndürür; bilinmeyen dilde Türkçeye düşer."""
    return METINLER.get(dil, METINLER["tr"])
