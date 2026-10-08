import urllib.parse
import pandas as pd
import requests

def get_stellar_parameters(target_name="Kepler-10"):
    """
    Kullanıcının girdiği herhangi bir yıldızın parametrelerini (Teff, R*, log g)
    NASA Exoplanet Archive TAP API'sinden dinamik olarak çeker.
    """
    print(f"\n[NASA/ESA API] Hedef yıldız parametreleri taranıyor: {target_name}...")
    
    # Standart referans Güneş modeli (Eğer arşivde hedef bulunamazsa güvenli fallback)
    stellar_info = {
        "source": "NASA Exoplanet Archive / ESA Gaia",
        "star_name": target_name,
        "teff_k": 5778.0,
        "radius_srad": 1.0,
        "logg": 4.44,
        "parallax_mas": 10.0
    }
    
    try:
        # NASA TAP API üzerinden yıldız parametrelerini sorgula
        clean_name = target_name.strip()
        query = f"select pl_name, hostname, st_teff, st_rad, st_logg, sy_plx from ps where pl_name like '{clean_name}%' or hostname like '{clean_name}%'"
        encoded_query = urllib.parse.quote(query)
        url = f"https://exoplanetarchive.ipac.caltech.edu/TAP/sync?query={encoded_query}&format=csv"
        
        df = pd.read_csv(url)
        
        if len(df) > 0:
            row = df.iloc[0]
            if pd.notna(row.get('st_teff')):
                stellar_info["teff_k"] = float(row['st_teff'])
            if pd.notna(row.get('st_rad')):
                stellar_info["radius_srad"] = float(row['st_rad'])
            if pd.notna(row.get('st_logg')):
                stellar_info["logg"] = float(row['st_logg'])
            if pd.notna(row.get('sy_plx')):
                stellar_info["parallax_mas"] = float(row['sy_plx'])
                
            stellar_info["source"] = f"NASA Planetary Systems Archive ({row.get('hostname', clean_name)})"
            print(f"-> NASA Kataloğundan Doğrulandı: Teff = {stellar_info['teff_k']} K | R* = {stellar_info['radius_srad']} R_sun")
        else:
            print("-> Spesifik yıldız parametresi arşivde bulunamadı, standart güneş referansı alındı.")
            
        return stellar_info

    except Exception as e:
        print(f"[!] API sorgu uyarısı ({e}). Güvenli referans kullanılıyor.")
        return stellar_info

if __name__ == "__main__":
    print(get_stellar_parameters("Kepler-22"))