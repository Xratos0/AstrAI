import os
import time
from pathlib import Path
from dotenv import load_dotenv
from google import genai
from google.genai import errors

# .env dosyasını yükle
current_dir = Path(__file__).resolve().parent
load_dotenv(dotenv_path=current_dir / ".env")

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY bulunamadı!")

client = genai.Client(api_key=api_key)

# 503 durumunda sırayla devreye girecek yedek model havuzu
FALLBACK_MODELS = [
    "gemini-3.5-flash-lite",  # Anında yanıt veren ana model
    "gemini-3.8-flash",       # Yedek
    "gemini-3.7-flash"        # Yedek
]

def generate_astrophysics_report(transit_data):
    """
    Sinyal işleme motorundan gelen sayısal verileri alır,
    Gemini modelleriyle astrofiziksel karakterizasyon ve doğrulama raporu üretir.
    503 sunucu yoğunluğu durumunda otomatik yedek modele geçer.
    """
    target = transit_data["target"]
    period = transit_data["period_days"]
    depth = transit_data["transit_depth_percent"]
    duration = transit_data["transit_duration_hours"]

    prompt = f"""
Sen NASA Exoplanet Exploration ve Astrofizik alanında uzmanlaşmış kıdemli bir araştırma yapay zekasısın.
Aşağıda NASA uzay teleskobu fotometrisi ve Box Least Squares (BLS) algoritmasıyla tespit edilen gerçek bir geçiş sinyalinin verileri bulunmaktadır:

HEDEF YILDIZ / SİSTEM: {target}
- Tespit Edilen Yörünge Periyodu: {period:.4f} Gün
- Geçiş Derinliği (Flux Dip): %{depth:.4f}
- Geçiş Süresi: {duration:.2f} Saat

Lütfen bu verileri ilk astrofizik ilkelerine göre analiz et ve şu 4 başlık altında net, profesyonel ve teknik bir 'Astrofiziksel Keşif ve Karakterizasyon Raporu' hazırla:

1. YÖRÜNGE VE FİZİKSEL PARAMETRELER:
   - Kepler'in 3. Yasasını kullanarak yıldız-gezegen mesafesini (AU cinsinden yarı büyük eksen 'a') yaklaşık hesapla.
   - Geçiş derinliğini kullanarak gezegenin tahmini boyutunu (Dünya yarıçapı R_earth veya Jüpiter yarıçapı R_jup cinsinden) sınıflandır (Süper-Dünya, Sıcak Jüpiter, Gaz Devi vb.).

2. TERMAL REJİM VE YAŞANABİLİRLİK (HABITABILITY):
   - Bu periyot ve mesafeye göre gezegenin tahmini denge sıcaklığı (T_eq) ve yüzey koşulları nedir?
   - Yaşanabilir Bölge (Goldilocks Zone) içinde midir, yoksa gelgit kilitli (tidally locked) bir lav dünyası mıdır?

3. SİNYAL DOĞRULAMA (FALSE POSITIVE CHECK):
   - Bu sinyalin gerçek bir ötegezegen olma olasılığı nedir? 
   - Bir 'Örten Çift Yıldız' (Eclipsing Binary) veya arka plan yıldız gürültüsü olma ihtimalini geçiş süresi ve derinliğine bakarak değerlendir.

4. NİHAİ KARAR VE BİLİMSEL SONUÇ:
   - Sinyalin resmi literatürdeki durumu (Kepler/TESS teyidi var mı?) ve gözlem özeti.

Not: Açıklamaların akademik, net, gereksiz dolgudan uzak ve tamamen fiziksel temellere dayalı olsun.
"""

    response_text = None
    
    for model_name in FALLBACK_MODELS:
        print(f"[+] Model deneniyor: {model_name}...")
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=prompt,
            )
            response_text = response.text
            print(f"[✓] Başarılı! Rapor {model_name} tarafından üretildi.")
            break
        except errors.ServerError:
            print(f"[!] {model_name} 503 meşgul uyarısı verdi. Sıradaki yedek modele geçiliyor...")
            time.sleep(1)
        except Exception as e:
            print(f"[!] {model_name} hata verdi ({e}). Sıradakine geçiliyor...")
            
    if not response_text:
        raise RuntimeError("Tüm yedek modeller meşgul. Lütfen kısa bir süre sonra tekrar deneyin.")

    return response_text

if __name__ == "__main__":
    # Elde ettiğimiz Kepler-10 verisiyle test
    ornek_veri = {
        "target": "Kepler-10",
        "period_days": 0.8373,
        "transit_depth_percent": 0.0012,
        "transit_duration_hours": 1.92,
        "plot_path": "Kepler-10_transit_plot.png"
    }
    
    rapor = generate_astrophysics_report(ornek_veri)
    print("\n" + "=" * 70)
    print("ASTR-AI AKADEMİK ÖTEGEZEGEN RAPORU")
    print("=" * 70)
    print(rapor)
    print("=" * 70)