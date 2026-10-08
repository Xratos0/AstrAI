import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, roc_auc_score, confusion_matrix, ConfusionMatrixDisplay
import xgboost as xgb
import joblib

print("=" * 60)
print("AstrAI: Kendi Ötegezegen Sınıflandırma Modelini Eğitiyor")
print("=" * 60)

# 1. NASA Exoplanet Archive'dan Gerçek Etiketli Veri Setini İndir
url = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync?query=select+koi_disposition,koi_period,koi_duration,koi_depth,koi_prad,koi_teq,koi_insol,koi_model_snr,koi_steff,koi_slogg,koi_srad+from+cumulative&format=csv"

print("[1/5] NASA Exoplanet Archive'dan 9.500+ etiketli veri çekiliyor...")
df = pd.read_csv(url)

# 2. Veri Ön İşleme (Preprocessing)
print("[2/5] Veri temizleniyor ve filtreleniyor...")
# Sadece CONFIRMED (1) ve FALSE POSITIVE (0) hedefleri alalım (CANDIDATE'leri eğitime katmayalım)
df = df[df['koi_disposition'].isin(['CONFIRMED', 'FALSE POSITIVE'])].copy()
df['target'] = (df['koi_disposition'] == 'CONFIRMED').astype(int)

# Kritik Astrofiziksel Öznitelikler
feature_cols = [
    'koi_period',     # Yörünge periyodu (gün)
    'koi_duration',   # Geçiş süresi (saat)
    'koi_depth',      # Geçiş derinliği (ppm)
    'koi_prad',       # Gezegen yarıçapı (Dünya yarıçapı cinsinden)
    'koi_teq',        # Denge sıcaklığı (Kelvin)
    'koi_insol',      # Yıldızdan alınan ışınım akısı
    'koi_model_snr',  # Sinyal-gürültü oranı (SNR)
    'koi_steff',      # Yıldızın etkin sıcaklığı (K)
    'koi_slogg',      # Yıldızın yüzey çekimi (log g)
    'koi_srad'        # Yıldızın yarıçapı (Güneş yarıçapı cinsinden)
]

X = df[feature_cols].copy()
y = df['target'].copy()

# Eksik verileri medyan değer ile doldur
X = X.fillna(X.median())

# 3. Eğitim ve Test Kümelerine Böl (%80 Eğitim, %20 Test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42, stratify=y)
print(f"-> Eğitim Kümesi: {len(X_train)} hedef | Test Kümesi: {len(X_test)} hedef")

# 4. XGBoost Modelini Eğit
print("[3/5] XGBoost Sınıflandırıcı optimize ediliyor ve eğitiliyor...")
model = xgb.XGBClassifier(
    n_estimators=300,
    max_depth=5,
    learning_rate=0.05,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42,
    eval_metric='logloss'
)

model.fit(X_train, y_train)

# 5. Modeli Değerlendir
print("[4/5] Model test kümesinde doğrulanıyor...")
y_pred = model.predict(X_test)
y_prob = model.predict_proba(X_test)[:, 1]

auc_score = roc_auc_score(y_test, y_prob)
print("\n" + "=" * 50)
print(f"ROC-AUC BAŞARI SKORU : %{auc_score * 100:.2f}")
print("=" * 50)
print(classification_report(y_test, y_pred, target_names=['FALSE POSITIVE', 'CONFIRMED']))

# Karmaşıklık Matrisini (Confusion Matrix) Çiz ve Kaydet
cm = confusion_matrix(y_test, y_pred)
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=['Sahte Pozitif', 'Onaylı Gezegen'])
disp.plot(cmap="Blues")
plt.title(f"AstrAI ML Sınıflandırıcı - Doğruluk Matrisi (AUC: %{auc_score*100:.1f})")
plt.tight_layout()
plt.savefig("model_performance_cm.png", dpi=150)
plt.close()

# 6. Modeli Diske Kaydet
joblib.dump(model, "exoplanet_classifier.pkl")
joblib.dump(feature_cols, "feature_names.pkl")

print("\n[5/5] BAŞARILI: Model 'exoplanet_classifier.pkl' olarak kaydedildi!")
print("[+] Performans grafiği kaydedildi: model_performance_cm.png")