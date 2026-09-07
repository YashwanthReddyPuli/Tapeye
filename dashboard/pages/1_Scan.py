import os
import sys
import time
import tempfile
import streamlit as st
from PIL import Image

# Ensure repository root is on sys.path
repo_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from dashboard.utils import generate_audio_plots
from fusion.predict import predict_final_verdict

st.set_page_config(page_title="TapEye - Run Quality Scan", page_icon="🔍", layout="wide")

st.title("🔍 TapEye Quality Scanner")
st.markdown("Upload produce **impact audio (.wav)** and **surface photo (.jpg/.png)** to compute dual-modal quality prediction.")

# Side-by-side file uploaders
col_aud, col_img = st.columns(2)

with col_aud:
    st.subheader("1. Acoustic Input")
    uploaded_audio = st.file_uploader("Upload Produce Tap Sound (.wav)", type=["wav"])

with col_img:
    st.subheader("2. Visual Input")
    uploaded_image = st.file_uploader("Upload Produce Photo (.jpg, .png)", type=["jpg", "jpeg", "png"])

# Enable scan button only when both files are uploaded
scan_enabled = (uploaded_audio is not None) and (uploaded_image is not None)

st.markdown("---")
btn_col1, btn_col2 = st.columns([1, 4])
with btn_col1:
    run_button = st.button("🚀 Run Dual-Modal Scan", type="primary", disabled=not scan_enabled)

if not scan_enabled:
    st.info("💡 Please upload both an audio file and an image file above to enable the scanner.")

if run_button and scan_enabled:
    try:
        with st.spinner("Processing dual-modal scan and running late-fusion inference..."):
            # 1. Save uploaded files to temporary storage
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_aud:
                tmp_aud.write(uploaded_audio.getbuffer())
                tmp_audio_path = tmp_aud.name

            with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_img:
                tmp_img.write(uploaded_image.getbuffer())
                tmp_image_path = tmp_img.name

            # 2. Run inference and measure wall-clock latency
            start_time = time.perf_counter()
            verdict_result = predict_final_verdict(tmp_audio_path, tmp_image_path)
            inference_time_ms = (time.perf_counter() - start_time) * 1000.0

            # 3. Render Visual & Acoustic Inputs
            st.subheader("📷 Input Feature Inspection")
            inspect_cols = st.columns(2)

            with inspect_cols[0]:
                st.markdown("**Audio Waveform & MFCC Heatmap**")
                fig_plots = generate_audio_plots(tmp_audio_path)
                st.pyplot(fig_plots, use_container_width=True)

            with inspect_cols[1]:
                st.markdown("**Produce Surface Inspection Photo**")
                pil_img = Image.open(tmp_image_path)
                st.image(pil_img, caption="Uploaded Produce Image", use_container_width=True)

            st.caption(f"⚡ **Total Model Inference Time**: `{inference_time_ms:.1f} ms`")
            st.markdown("---")

            # 4. Display 3 Side-by-Side Metric Cards
            st.subheader("📊 Produce Quality Verdict Dashboard")
            card_cols = st.columns(3)

            # Unimodal Branch 1: Acoustic
            ac_res = verdict_result["acoustic_branch"]
            ac_label = ac_res["predicted_class"].upper()
            ac_prob = ac_res["probabilities"].get(ac_res["predicted_class"], 0.0) * 100.0

            with card_cols[0]:
                st.markdown(
                    f"""
                    <div style="background-color:#f8f9fa; border: 2px solid #e9ecef; border-radius: 12px; padding: 20px; text-align: center;">
                        <h4 style="margin:0; color:#495057;">🔊 Acoustic Branch</h4>
                        <p style="font-size: 13px; color:#6c757d; margin-bottom: 12px;">Internal Impact Response</p>
                        <h2 style="margin:0; color:#1976d2;">{ac_label}</h2>
                        <h3 style="margin:4px 0 0 0; color:#333;">{ac_prob:.1f}% <span style="font-size:14px; font-weight:normal;">confidence</span></h3>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            # Unimodal Branch 2: Visual
            vis_res = verdict_result["visual_branch"]
            vis_label = vis_res["predicted_class"].upper()
            vis_prob = vis_res["probabilities"].get(vis_res["predicted_class"], 0.0) * 100.0

            with card_cols[1]:
                st.markdown(
                    f"""
                    <div style="background-color:#f8f9fa; border: 2px solid #e9ecef; border-radius: 12px; padding: 20px; text-align: center;">
                        <h4 style="margin:0; color:#495057;">👁️ Visual Branch</h4>
                        <p style="font-size: 13px; color:#6c757d; margin-bottom: 12px;">MobileNetV2 Surface Inspection</p>
                        <h2 style="margin:0; color:#7b1fa2;">{vis_label}</h2>
                        <h3 style="margin:4px 0 0 0; color:#333;">{vis_prob:.1f}% <span style="font-size:14px; font-weight:normal;">confidence</span></h3>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            # Card 3: Highlighted Late-Fusion Final Verdict
            final_verdict = verdict_result["final_verdict"].lower()
            fusion_conf = verdict_result["fusion_confidence"] * 100.0

            if final_verdict == "good":
                verdict_display = "GOOD (FRESH)"
                bg_color = "#e8f5e9"
                border_color = "#2e7d32"
                text_color = "#1b5e20"
            elif final_verdict == "borderline":
                verdict_display = "BORDERLINE"
                bg_color = "#fffde7"
                border_color = "#f57f17"
                text_color = "#f57f17"
            else:
                verdict_display = "REJECT / BAD"
                bg_color = "#ffebee"
                border_color = "#c62828"
                text_color = "#b71c1c"

            with card_cols[2]:
                st.markdown(
                    f"""
                    <div style="background-color:{bg_color}; border: 3px solid {border_color}; border-radius: 12px; padding: 20px; text-align: center; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
                        <h4 style="margin:0; color:{text_color};">🎯 Final Fused Verdict</h4>
                        <p style="font-size: 13px; color:{text_color}; margin-bottom: 12px; opacity: 0.85;">Late-Fusion Meta-Classifier</p>
                        <h1 style="margin:0; color:{text_color}; font-size: 32px;">{verdict_display}</h1>
                        <h3 style="margin:4px 0 0 0; color:{text_color};">{fusion_conf:.1f}% <span style="font-size:14px; font-weight:normal;">fusion confidence</span></h3>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            # Clean up temporary files
            os.remove(tmp_audio_path)
            os.remove(tmp_image_path)

    except Exception as err:
        st.error(f"❌ **Scan Error**: Failed to process scan inputs. Details: {err}")
