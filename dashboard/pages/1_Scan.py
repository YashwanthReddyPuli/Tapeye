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

from dashboard.utils import inject_custom_css, generate_plotly_spectrogram, generate_radar_chart
from fusion.predict import predict_final_verdict

st.set_page_config(page_title="TapEye OS - Quality Scanner", page_icon="🔍", layout="wide")
inject_custom_css()

st.title("🔍 TapEye OS: Interactive Quality Scanner")
st.markdown("Upload produce **impact audio (.wav)** and **surface photo (.jpg/.png)** to run real-time dual-modal late-fusion quality prediction.")

# Side-by-side file uploaders with immediate preview
col_aud, col_img = st.columns(2)

with col_aud:
    st.markdown("### 🎙️ 1. Acoustic Impact Recording")
    uploaded_audio = st.file_uploader("Drop audio recording (.wav) here", type=["wav"], key="audio_uploader")
    if uploaded_audio is not None:
        st.audio(uploaded_audio, format="audio/wav")
        st.caption(f"Audio File Ready: `{uploaded_audio.name}` ({len(uploaded_audio.getbuffer()) / 1024:.1f} KB)")

with col_img:
    st.markdown("### 📷 2. Surface Inspection Photo")
    uploaded_image = st.file_uploader("Drop produce photo (.jpg, .png) here", type=["jpg", "jpeg", "png"], key="image_uploader")
    if uploaded_image is not None:
        pil_preview = Image.open(uploaded_image)
        st.image(pil_preview, caption=f"Uploaded Preview: {uploaded_image.name}", use_container_width=True)

# Enable scan button only when both files are uploaded
scan_enabled = (uploaded_audio is not None) and (uploaded_image is not None)

st.markdown("---")
btn_col1, btn_col2 = st.columns([1, 4])
with btn_col1:
    run_button = st.button("🚀 Run Scan Engine", type="primary", disabled=not scan_enabled, use_container_width=True)

if not scan_enabled:
    st.info("💡 **Ready to Scan**: Upload both an audio file (.wav) and an image file (.jpg/.png) above to activate the scanner.")

if run_button and scan_enabled:
    try:
        # Step-by-step pipeline status animation using st.status()
        with st.status("🚀 Processing Dual-Modal Quality Pipeline...", expanded=True) as status_box:
            st.write("🔊 **Step 1/4**: Extracting 13-coefficient MFCCs & Spectral Centroid features...")
            time.sleep(0.3)

            st.write("👁️ **Step 2/4**: Preprocessing image & passing through MobileNetV2 Transfer model...")
            time.sleep(0.3)

            st.write("🔗 **Step 3/4**: Concatenating probability vectors [P_acoustic ∥ P_visual]...")
            time.sleep(0.3)

            st.write("🎯 **Step 4/4**: Executing Logistic Regression Late-Fusion Meta-Classifier...")

            # Save uploaded files to temporary storage
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_aud:
                tmp_aud.write(uploaded_audio.getbuffer())
                tmp_audio_path = tmp_aud.name

            with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_img:
                tmp_img.write(uploaded_image.getbuffer())
                tmp_image_path = tmp_img.name

            start_time = time.perf_counter()
            verdict_result = predict_final_verdict(tmp_audio_path, tmp_image_path)
            inference_time_ms = (time.perf_counter() - start_time) * 1000.0

            status_box.update(label=f"✅ Scan Complete! Inference Time: {inference_time_ms:.1f} ms", state="complete", expanded=False)

        st.markdown("<br>", unsafe_allow_html=True)

        # ----------------------------------------------------
        # 1. Unimodal Branch Cards (Side-by-Side)
        # ----------------------------------------------------
        st.markdown("### 📊 Dual-Modal Branch Predictions")
        branch_cols = st.columns(2)

        # Acoustic Branch Card
        ac_res = verdict_result["acoustic_branch"]
        ac_label = ac_res["predicted_class"].upper()
        ac_prob = ac_res["probabilities"].get(ac_res["predicted_class"], 0.0) * 100.0

        with branch_cols[0]:
            st.markdown(
                f"""
                <div class="tapeye-card" style="border-left: 4px solid #29b6f6;">
                    <h4 style="margin:0; color:#81d4fa;">🔊 Acoustic Branch</h4>
                    <p style="font-size: 13px; color:#8b949e; margin-bottom: 12px;">Impact Resonance Signal Analysis</p>
                    <h2 style="margin:0; color:#29b6f6; font-size: 28px;">{ac_label}</h2>
                    <h3 style="margin:4px 0 0 0; color:#e6edf3;">{ac_prob:.1f}% <span style="font-size:14px; font-weight:normal; color:#8b949e;">confidence</span></h3>
                </div>
                """,
                unsafe_allow_html=True
            )

        # Visual Branch Card
        vis_res = verdict_result["visual_branch"]
        vis_label = vis_res["predicted_class"].upper()
        vis_prob = vis_res["probabilities"].get(vis_res["predicted_class"], 0.0) * 100.0

        with branch_cols[1]:
            st.markdown(
                f"""
                <div class="tapeye-card" style="border-left: 4px solid #ab47bc;">
                    <h4 style="margin:0; color:#ce93d8;">👁️ Visual Branch</h4>
                    <p style="font-size: 13px; color:#8b949e; margin-bottom: 12px;">MobileNetV2 Deep Surface Inspection</p>
                    <h2 style="margin:0; color:#ab47bc; font-size: 28px;">{vis_label}</h2>
                    <h3 style="margin:4px 0 0 0; color:#e6edf3;">{vis_prob:.1f}% <span style="font-size:14px; font-weight:normal; color:#8b949e;">confidence</span></h3>
                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown("<br>", unsafe_allow_html=True)

        # ----------------------------------------------------
        # 2. Full-Width Glowing Fused Verdict Card
        # ----------------------------------------------------
        final_verdict = verdict_result["final_verdict"].lower()
        fusion_conf = verdict_result["fusion_confidence"] * 100.0

        if final_verdict == "good":
            verdict_display = "GOOD (FRESH PRODUCE)"
            card_class = "verdict-card-good"
            verdict_color = "#81c784"
        elif final_verdict == "borderline":
            verdict_display = "BORDERLINE (CONSUME SOON)"
            card_class = "verdict-card-borderline"
            verdict_color = "#ffd54f"
        else:
            verdict_display = "REJECT / BAD (DECAY DETECTED)"
            card_class = "verdict-card-bad"
            verdict_color = "#ef5350"

        st.markdown(
            f"""
            <div class="{card_class}">
                <p style="font-size: 14px; letter-spacing: 1px; color:#e6edf3; margin-bottom: 6px; text-transform: uppercase;">🎯 Final Multimodal Late-Fusion Decision</p>
                <h1 style="margin:0; color:{verdict_color}; font-size: 38px; font-weight: 800;">{verdict_display}</h1>
                <h3 style="margin:8px 0 0 0; color:#e6edf3;">{fusion_conf:.1f}% <span style="font-size:15px; font-weight:normal; color:#8b949e;">fused meta-confidence</span></h3>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown("<br>", unsafe_allow_html=True)

        # ----------------------------------------------------
        # 3. Interactive Plotly Visualizations
        # ----------------------------------------------------
        st.markdown("### 📈 Interactive Signal & Multimodal Probability Analysis")
        chart_cols = st.columns(2)

        with chart_cols[0]:
            fig_spectrogram = generate_plotly_spectrogram(tmp_audio_path)
            st.plotly_chart(fig_spectrogram, use_container_width=True)

        with chart_cols[1]:
            ac_p_dict = {str(k): float(v) for k, v in ac_res["probabilities"].items()}
            vis_p_dict = {str(k): float(v) for k, v in vis_res["probabilities"].items()}
            fused_p_dict = {str(k): float(v) for k, v in verdict_result["fused_probabilities"].items()}

            fig_radar = generate_radar_chart(ac_p_dict, vis_p_dict, fused_p_dict)
            st.plotly_chart(fig_radar, use_container_width=True)

        # Cleanup temporary files
        os.remove(tmp_audio_path)
        os.remove(tmp_image_path)

    except Exception as err:
        st.error(f"❌ **Scanner Execution Error**: Unable to process input files. Details: {err}")
