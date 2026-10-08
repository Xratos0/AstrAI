from pathlib import Path
import pandas as pd
import gradio as gr
from transit_analyzer import analyze_target
from astro_agent import generate_astrophysics_report
from catalog_engine import get_stellar_parameters
from ml_validator import evaluate_exoplanet_signal
from survey_engine import run_blind_survey

# 1. Sekme: Tekil Derin Analiz
def run_astrai_pipeline(target_name):
    if not target_name or target_name.strip() == "":
        return None, None, "Hedef adı boş olamaz."
    
    clean_target = target_name.strip()
    try:
        transit_data = analyze_target(clean_target)
        plot_path = transit_data["plot_path"]
        corner_path = transit_data["corner_path"]
        output_dir = Path(transit_data["output_dir"])
        
        stellar_data = get_stellar_parameters(clean_target)
        ml_results = evaluate_exoplanet_signal(transit_data, stellar_data)
        
        dashboard_summary = f"""
### 📊 Bayesian MCMC Parametre Tahminleri:
* **Geçiş Derinliği:** `%{transit_data['transit_depth_percent']} (+{transit_data['depth_err_plus']} / -{transit_data['depth_err_minus']})`
* **Yörünge Periyodu:** `{transit_data['period_days']} Gün`
* **Tahmini Eğim Açısı:** `{transit_data['inclination_deg']}°`

---
### 🎯 2D CCD Centroid (Ağırlık Merkezi) Doğrulaması:
* **Durum:** **`{transit_data['centroid_status']}`**

---
### 🌌 James Webb (JWST) Atmosferik Spektroskopi:
* **Atmosferik Ölçek Yüksekliği ($H$):** `{transit_data['scale_height_km']} km`
* **JWST Durumu:** **`{transit_data['jwst_status']}`**

---
### 🤖 AstrAI ML Modeli Kararı:
* **Karar:** `{ml_results['decision']}`
* **Ötegezegen Olasılığı:** `%{ml_results['planet_prob']}` (XGBoost %97.82 ROC-AUC)
"""
        transit_data["ml_decision"] = ml_results["decision"]
        transit_data["ml_confidence"] = ml_results["planet_prob"]
        report_text = generate_astrophysics_report(transit_data)
        
        full_report = dashboard_summary + "\n\n" + report_text
        with open(output_dir / "full_report.md", "w", encoding="utf-8") as f:
            f.write(full_report)
            
        return plot_path, corner_path, full_report
    except Exception as e:
        return None, None, f"HATA OLUŞTU:\n{str(e)}"

# 2. Sekme: Otonom Kör Tarama
def execute_batch_survey(targets_str):
    if not targets_str:
        return pd.DataFrame()
    target_list = [t.strip() for t in targets_str.split(",") if t.strip()]
    results = run_blind_survey(target_list)
    return pd.DataFrame(results)

custom_theme = gr.themes.Soft(primary_hue="indigo", secondary_hue="slate")

with gr.Blocks(theme=custom_theme, title="AstrAI Enterprise") as demo:
    gr.Markdown("# 🪐 AstrAI: Otonom Ötegezegen Keşif & Spektroskopi Platformu")
    
    with gr.Tabs():
        # 1. SEKME: DERİN ANALİZ LABORATUVARI
        with gr.TabItem("🔬 Tekil Derin Analiz & MCMC Laboratuvarı"):
            with gr.Row():
                with gr.Column(scale=1):
                    target_input = gr.Textbox(label="Hedef Yıldız", value="Kepler-7")
                    analyze_button = gr.Button("🚀 Derin Analizi Başlat", variant="primary")
                    output_report = gr.Markdown(label="Rapor ve Gösterge Paneli")
                with gr.Column(scale=2):
                    output_plot = gr.Image(label="NASA Işık Eğrisi + Model Fit + 2D CCD", type="filepath")
                    output_corner = gr.Image(label="Bayesian MCMC Corner Plot", type="filepath")

            analyze_button.click(
                fn=run_astrai_pipeline,
                inputs=[target_input],
                outputs=[output_plot, output_corner, output_report]
            )

        # 2. SEKME: OTONOM KÖR TARAMA ROBOTU
        with gr.TabItem("🔭 Otonom Kör Gezegen Avcısı (Batch Survey)"):
            gr.Markdown(
                """
                ### 🌌 Çoklu Yıldız Taraması ve Otonom Triyaj
                Aşağıya virgülle ayrılmış yıldız isimleri girin. Robot her hedefi NASA arşivinden otonom olarak çekecek, 
                BLS sinyal analizinden geçirip kendi eğittiğimiz **XGBoost (%97.82 AUC)** modeline sokacak ve keşif tablosuna dökecektir.
                """
            )
            batch_input = gr.Textbox(
                label="Taranacak Hedef Yıldızlar (Virgülle ayırın)",
                value="Kepler-7, Kepler-10, Kepler-8, WASP-12",
                lines=2
            )
            survey_button = gr.Button("⚡ Otonom Taramayı Başlat", variant="primary")
            survey_table = gr.Dataframe(label="Otonom Keşif ve Triyaj Tablosu", interactive=False)

            survey_button.click(
                fn=execute_batch_survey,
                inputs=[batch_input],
                outputs=[survey_table]
            )

if __name__ == "__main__":
    demo.launch(share=False)