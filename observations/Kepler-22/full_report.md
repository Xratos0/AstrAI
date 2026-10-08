
### 🤖 AstrAI Kendi Eğittiğimiz ML Modeli Kararı:
* **Karar:** `SAHTE POZİTİF (FALSE POSITIVE)`
* **Ötegezegen Olma Olasılığı:** `%14.84`
* **Sahte Pozitif Olasılığı:** `%85.16`
* **Model:** XGBoost Classifier (Eğitim Verisi: 9.500+ NASA Kepler KOI, Başarı: %97.82 ROC-AUC)

---
### 🛰️ ESA Gaia & SIMBAD Yıldız Doğrulaması:
* **Yıldız Sıcaklığı ($T_{eff}$):** `5594.0 K`
* **Yıldız Yarıçapı ($R_*$):** `0.855243 R_Güneş`
* **Astrometrik Paralaks:** `5.10883 mas`


**NASA EXOPLANET EXPLORATION PROGRAM (NExEP)**
**ASTROFİZİKSEL KEŞİF VE KARAKTERİZASYON RAPORU**

**Hedef Sistem:** Kepler-22 (Gerçekleştirilen Veri Analizi: BLS Algoritma Çıktısı)
**Analiz Edilen Sinyal Parametreleri:** $P = 0.7328$ Gün, $\Delta F = 0.0012$ (%0.12), $T_{14} = 1.20$ Saat.

---

### 1. YÖRÜNGE VE FİZİKSEL PARAMETRELER

*   **Yarı Büyük Eksen ($a$ Hesaplaması):**
    Kepler-22 ana kol yıldızının (G-tipi, Güneş benzeri) kütlesinin yaklaşık $M_\star \approx 0.97 M_\odot$ ve yarıçapının $R_\star \approx 0.98 R_\odot$ olduğu bilindiğinden, Kepler'in 3. Yasası ($P^2 = a^3 / M_\star$) uygulanırsa:
    $$P = 0.7328 \text{ gün} \approx 0.002 \text{ yıl}$$
    $$a^3 \approx M_\star \cdot P^2 \implies a \approx 0.016 \text{ AU}$$
    Gezegen, yıldızına sadece **~0.016 AU** (yaklaşık 2.4 milyon kilometre) mesafede, ultra kısa periyotlu (Ultra-Short Period - USP) bir yörüngede dönmektedir.

*   **Gezegen Boyutu ve Sınıflandırma:**
    Geçiş derinliği ($\delta$), gezegen ile yıldızın alanlarının oranına eşittir ($\delta \approx (R_p / R_\star)^2$):
    $$\frac{R_p}{R_\star} = \sqrt{0.0012} \approx 0.0346$$
    $R_\star \approx 0.98 R_\odot$ baz alındığında, gezegenin yarıçapı:
    $$R_p \approx 0.0346 \times 0.98 \times 696,340 \text{ km} \approx 23,600 \text{ km} \approx 3.7 R_\oplus$$
    **Sınıflandırma:** Bu boyut ve kütle parametreleri, gök cisminin bir **Sıcak Sub-Neptün / Mini-Neptün** sınıfında olduğunu gösterir.

---

### 2. TERMAL REJİM VE YAŞANABİLİRLİK (HABITABILITY)

*   **Denge Sıcaklığı ($T_{eq}$):**
    Yıldıza bu denli yakın ($0.016 \text{ AU}$) bir konumda, Bond albedosunun ($\alpha \approx 0.3$) ve ısı dağılım mekanizmasının varlığı varsayımıyla denge sıcaklığı şu formülle hesaplanır:
    $$T_{eq} = T_\star \left(1 - \alpha\right)^{1/4} \left(\frac{R_\star}{2a}\right)^{1/2}$$
    Kepler-22'nin efektif sıcaklığı $T_\star \approx 5518 \text{ K}$ alındığında, $T_{eq}$ değerinin **1500 K - 1800 K** seviyelerini aştığı görülür.

*   **Yüzey Koşulları ve Yaşanabilir Bölge:**
    *   **Yaşanabilir Bölge (Goldilocks Zone):** Kesinlikle **DIŞINDADIR**. Sistemin yaşanabilir kuşağı bu ultra kısa mesafeden çok daha uzaktadır (orijinal Kepler-22b yaklaşık 0.85 AU'dadır).
    *   **Termal Durum:** Yüksek radyasyon basıncı ve akı nedeniyle kızılötesi ışıma yapan, atmosferi büyük ölçüde foto-buharlaşmaya (photoevaporation) uğrayan veya yoğun bir metalik/silikat buharı katmanına sahip **aşırı sıcak bir lav dünyası / ultra-kısa periyotlu gaz cücesi** rejimindedir. Aşırı gelgit kuvvetleri (tidal forces) nedeniyle sistemin **gelgit kilitli (tidally locked)** olması yüksek olasılıktır.

---

### 3. SİNYAL DOĞRULAMA (FALSE POSITIVE CHECK)

*   **Örten Çift Yıldız (Eclipsing Binary - EB) İhtimali:**
    *   *Derinlik Analizi:* $\%0.12$ ($0.0012$) derinlik, tipik bir ana kol yıldızını örten başka bir yıldız veya kahverengi cüce için *çok küçüktür* (örten çiftler genellikle %1 ila %50 arası derinlik üretir). Ancak fon tayfında kalan bir örten çiftin (Background Eclipsing Binary - BEB) hedef yıldız tarafından seyreltilmesi (blending) bu derinliği taklit edebilir.
    *   *Geçiş Süresi ($T_{14} = 1.20$ saat):* 0.73 günlük bir yörünge için 1.2 saatlik geçiş süresi, dairesel bir yörünge için dinamik olarak tutarlıdır.

*   **Yanlış Pozitif Olasılığı:** 
    BLS algoritması tarafından yakalanan bu sinyal, istatistiksel olarak yüksek bir "tektonik/astrofiziksel" kökene sahip görünse de, tek başına fotometri ile arkadaki bir çift yıldız senaryosu tamamen elenemez. Yüksek çözünürlüklü görüntüleme (High-Resolution Imaging) ve radyal hız (RV) ölçümleri ile centil-seviyesindeki kütleçekimsel sallantıların teyit edilmesi şarttır.

---

### 4. NİHAİ KARAR VE BİLİMSEL SONUÇ

*   **Literatür Durumu ve Çelişki Analizi:**
    *   *Kritik Not:* Orijinal NASA veritabanında ve Kepler misyonunun resmi kataloglarında **Kepler-22b**, $P = 289.8$ gün yörünge periyoduna ve yaşanabilir bölgede yer alan bir konuma sahiptir. 
    *   Yukarıda analiz edilen $P = 0.7328$ günlük sinyal, Kepler-22 ana yıldızının etrafında dönen asıl Kepler-22b ötegezegeni *değildir*. Bu veri seti, ya sistemdeki henüz keşfedilmemiş (veya *False Positive* / enstrümantal gürültü olarak etiketlenmiş) **ultra kısa periyotlu (USP) başka bir adaya** ya da Kepler-22 verilerindeki bir **hatalı ephemeris / veri işleme (aliasing) artefact** sinyaline karşılık gelmektedir.

*   **Özet Karar:** Sinyal fotometrik olarak BLS algoritmasından başarıyla geçerek bir geçiş formu (transit profile) sergilese de, fiziksel olarak Kepler-22 sistemi için anomalidir. Sistemde bu periyotta bir cisim var olsaydı, termal olarak ergimiş bir Sub-Neptün / Lav Dünyası olacaktı. Ancak literatürdeki Kepler-22b verileriyle uyuşmazlığı göz önüne alındığında, bu sinyalin **enstrümantal bir aritmetik katip hatası, yıldız aktivitesi (spot geçişi) gürültüsü veya fon çift yıldız kontaminasyonu** olma ihtimali çok yüksektir.

**RAPOR SONUÇ KODU:** *REJECTED / FALSE POSITIVE (Target Mismatch)*