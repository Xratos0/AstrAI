import joblib
import numpy as np
import pandas as pd

# Eğitilmiş modeli ve öznitelik şemasını yükle
model = joblib.load("exoplanet_classifier.pkl")
feature_names = joblib.load("feature_names.pkl")

def evaluate_exoplanet_signal(transit_data, stellar_data):
    """
    Sinyal işleme ve ESA Gaia verilerini birleştirerek 
    eğittiğimiz XGBoost modelinden onay olasılık skoru üretir.
    """
    period = transit_data["period_days"]
    duration = transit_data["transit_duration_hours"]
    depth_percent = transit_data["transit_depth_percent"]
    depth_ppm = depth_percent * 10000.0  # Yüzdeyi ppm'e çevir
    
    r_star = stellar_data["radius_srad"]
    teff = stellar_data["teff_k"]
    logg = stellar_data["logg"]
    
    # Gezegen yarıçapı tahmini (Dünya yarıçapı cinsinden): Rp/R* = sqrt(depth)
    # R_sun = 109.2 * R_earth
    r_planet_earth = np.sqrt(depth_percent / 100.0) * (r_star * 109.2)
    
    # Tahmini denge sıcaklığı ve akı
    a_au = (period / 365.25)**(2/3)
    t_eq = teff * np.sqrt(r_star * 0.00465 / (2 * a_au)) if a_au > 0 else 1000.0
    insol = (r_star**2) * ((teff / 5778.0)**4) / (a_au**2) if a_au > 0 else 1.0
    
    # Modelin beklediği tam öznitelik vektörü
    features = {
        'koi_period': period,
        'koi_duration': duration,
        'koi_depth': depth_ppm,
        'koi_prad': r_planet_earth,
        'koi_teq': t_eq,
        'koi_insol': insol,
        'koi_model_snr': 35.0,  # Ortalama güçlü sinyal SNR değeri
        'koi_steff': teff,
        'koi_slogg': logg,
        'koi_srad': r_star
    }
    
    input_df = pd.DataFrame([features])[feature_names]
    
    # Model tahmini
    prob_confirmed = float(model.predict_proba(input_df)[0][1])
    prob_false_positive = 1.0 - prob_confirmed
    
    decision = "ONAYLI ÖTEGEZEGEN (CONFIRMED)" if prob_confirmed >= 0.50 else "SAHTE POZİTİF (FALSE POSITIVE)"
    
    return {
        "decision": decision,
        "planet_prob": round(prob_confirmed * 100, 2),
        "false_positive_prob": round(prob_false_positive * 100, 2),
        "estimated_radius_earth": round(r_planet_earth, 2),
        "estimated_teq_k": round(t_eq, 1)
    }

if __name__ == "__main__":
    t_data = {"period_days": 0.8373, "transit_depth_percent": 0.0012, "transit_duration_hours": 1.92}
    s_data = {"radius_srad": 1.065, "teff_k": 5627.0, "logg": 4.34}
    print(evaluate_exoplanet_signal(t_data, s_data))