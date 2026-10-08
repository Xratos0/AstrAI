import numpy as np
import lightkurve as lk
from catalog_engine import get_stellar_parameters
from ml_validator import evaluate_exoplanet_signal

def run_blind_survey(target_list):
    """
    Verilen yıldız listesini otonom olarak tarar,
    XGBoost ML modelinden geçirir ve bir Keşif Tablosu (Discovery Table) döndürür.
    """
    survey_results = []
    
    print("\n" + "=" * 65)
    print(f"AstrAI Otonom Tarama Robotu Başlatıldı: {len(target_list)} Hedef Taranacak")
    print("=" * 65)
    
    for idx, target in enumerate(target_list):
        clean_target = target.strip()
        if not clean_target:
            continue
            
        print(f"\n[{idx+1}/{len(target_list)}] Taranıyor: {clean_target}...")
        
        try:
            # 1. Hızlı Işık Eğrisi İndirme
            search_lc = lk.search_lightcurve(clean_target, mission="Kepler", author="Kepler")
            if len(search_lc) == 0:
                search_lc = lk.search_lightcurve(clean_target, mission="TESS")
                
            if len(search_lc) == 0:
                survey_results.append({
                    "Hedef Yıldız": clean_target,
                    "Durum": "VERİ BULUNAMADI",
                    "Periyot (Gün)": "-",
                    "Gezegen Olasılığı": "-",
                    "Teşhis": "NASA arşivinde gözlem verisi yok"
                })
                continue
                
            lc = search_lc[0].download()
            clean_lc = lc.remove_nans().remove_outliers(sigma=5)
            flat_lc = clean_lc.flatten(window_length=101)
            
            # 2. Hızlı BLS Taraması
            period_grid = np.linspace(0.5, 10, 2000)
            bls = flat_lc.to_periodogram(method="bls", period=period_grid, duration=np.linspace(0.05, 0.25, 6))
            
            best_period = float(bls.period_at_max_power.value)
            transit_duration = float(bls.duration_at_max_power.value)
            transit_depth = float(bls.depth_at_max_power.value)
            
            transit_data = {
                "period_days": round(best_period, 4),
                "transit_depth_percent": round(transit_depth * 100, 4),
                "transit_duration_hours": round(transit_duration * 24, 2)
            }
            
            # 3. ESA Gaia & Kendi ML Modelimizle Karar
            stellar_data = get_stellar_parameters(clean_target)
            ml_res = evaluate_exoplanet_signal(transit_data, stellar_data)
            
            # Keşif Kriteri: ML Olasılığı >= %50
            is_candidate = ml_res["planet_prob"] >= 50.0
            status_badge = "🟢 GEZEGEN KEŞFİ" if is_candidate else "🔴 SAHTE POZİTİF / GÜRÜLTÜ"
            
            survey_results.append({
                "Hedef Yıldız": clean_target,
                "Durum": status_badge,
                "Periyot (Gün)": f"{best_period:.4f}",
                "Gezegen Olasılığı": f"%{ml_res['planet_prob']}",
                "Teşhis": f"{ml_res['decision']} (R: {ml_res['estimated_radius_earth']} R_Dünya)"
            })
            print(f"-> Sonuç: {status_badge} (%{ml_res['planet_prob']})")
            
        except Exception as e:
            survey_results.append({
                "Hedef Yıldız": clean_target,
                "Durum": "HATA",
                "Periyot (Gün)": "-",
                "Gezegen Olasılığı": "-",
                "Teşhis": f"İşlem hatası: {str(e)[:30]}"
            })
            
    return survey_results