import os
from pathlib import Path
from dotenv import load_dotenv
from google import genai
from google.genai import errors

# .env dosyasını yükle
current_dir = Path(__file__).resolve().parent
load_dotenv(dotenv_path=current_dir / ".env")
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("HATA: .env dosyasında GEMINI_API_KEY bulunamadı!")

client = genai.Client(api_key=api_key)

# Sırayla denenecek en kararlı güncel modeller
candidate_models = [
    "gemini-2.5-flash",
    "gemini-2.5-flash-lite",
    "gemini-1.5-flash",
    "gemini-1.5-pro",
    "gemini-2.5-pro",
    "gemini-3.8-flash"
]

print("=" * 60)
print("AstrAI Otomatik Model Doğrulama Başlatılıyor...")
print("=" * 60)

active_model = None

for model_name in candidate_models:
    print(f"-> Deneniyor: {model_name}...", end=" ")
    try:
        response = client.models.generate_content(
            model=model_name,
            contents="1 kelimeyle 'HAZIR' yaz.",
        )
        print(" [BAŞARILI!]")
        active_model = model_name
        print("\n" + "=" * 60)
        print(f"SEÇİLEN AKTİF MODEL : {active_model}")
        print(f"MODEL YANITI        : {response.text.strip()}")
        print("=" * 60)
        break
    except errors.ServerError as e:
        print(" [503 Yoğunluk - Sıradakine geçiliyor]")
    except Exception as e:
        print(f" [Hata: {e}]")

if not active_model:
    print("\n[!] Tüm aday modeller sunucu yoğunluğu bildirdi. Lütfen birkaç dakika sonra tekrar deneyin.")
else:
    print(f"\nSistem {active_model} üzerinden sorunsuz çalışmaya hazır.")