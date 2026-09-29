"""
NLP Classification Dashboard - Streamlit Web Application
========================================================
Interactive web app for Natural Language Processing tasks:
1. Sentiment Analysis (Stanford Sentiment Treebank / SST-2)
2. SMS & Message Spam Detection (UCI SMS Spam Collection)
3. Model Performance Analytics & Confusion Matrices
4. Batch Text Inference & CSV Export
5. Architecture & API Specs

Run via:
    streamlit run app.py
or:
    python app.py
"""

import sys
import os
import json
from pathlib import Path
import pandas as pd
import numpy as np

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st

# Import backend inference services
try:
    from backend.app.services.sentiment_service import sentiment_service
    from backend.app.services.spam_service import spam_service
except ImportError as e:
    st.error(f"Failed to import backend services: {e}")
    sentiment_service = None
    spam_service = None

# Optional Plotly import for interactive charts
try:
    import plotly.graph_objects as go
    import plotly.express as px
    HAS_PLOTLY = True
except ImportError:
    HAS_PLOTLY = False


# ==========================================
# PAGE CONFIGURATION & CUSTOM STYLING
# ==========================================
st.set_page_config(
    page_title="NLP Classification Dashboard",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
    /* Metric Card styling */
    .metric-card {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 16px 20px;
        margin-bottom: 12px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .metric-title {
        font-size: 0.85rem;
        font-weight: 600;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .metric-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #0f172a;
        margin-top: 4px;
    }
    .badge-positive {
        background-color: #dcfce7;
        color: #15803d;
        padding: 4px 12px;
        border-radius: 9999px;
        font-weight: 600;
        font-size: 0.9rem;
        display: inline-block;
    }
    .badge-negative {
        background-color: #fee2e2;
        color: #b91c1c;
        padding: 4px 12px;
        border-radius: 9999px;
        font-weight: 600;
        font-size: 0.9rem;
        display: inline-block;
    }
    .badge-spam {
        background-color: #fee2e2;
        color: #b91c1c;
        padding: 4px 12px;
        border-radius: 9999px;
        font-weight: 600;
        font-size: 0.9rem;
        display: inline-block;
    }
    .badge-ham {
        background-color: #dbeafe;
        color: #1d4ed8;
        padding: 4px 12px;
        border-radius: 9999px;
        font-weight: 600;
        font-size: 0.9rem;
        display: inline-block;
    }
</style>
""", unsafe_allow_html=True)


# ==========================================
# SIDEBAR
# ==========================================
with st.sidebar:
    st.title("🧠 NLP Suite")
    st.caption("Production-Grade Machine Learning")
    st.divider()

    st.subheader("Model Status")
    sentiment_ready = sentiment_service.is_ready() if sentiment_service else False
    spam_ready = spam_service.is_ready() if spam_service else False

    col_s1, col_s2 = st.columns([3, 2])
    with col_s1:
        st.write("Sentiment (SST-2)")
    with col_s2:
        if sentiment_ready:
            st.markdown("🟢 **Ready**")
        else:
            st.markdown("🔴 **Not Ready**")

    col_m1, col_m2 = st.columns([3, 2])
    with col_m1:
        st.write("Spam (UCI SMS)")
    with col_m2:
        if spam_ready:
            st.markdown("🟢 **Ready**")
        else:
            st.markdown("🔴 **Not Ready**")

    st.divider()
    st.subheader("Quick Stats")
    st.write("• **Sentiment Accuracy**: 77.10%")
    st.write("• **Spam Accuracy**: 98.38%")
    st.write("• **Framework**: scikit-learn + TF-IDF")
    
    st.divider()
    st.markdown("🔗 **Repository**: [GitHub Repo](https://github.com/vamsim2005-hue/NLP-project)")
    st.caption("Built with FastAPI, React, and Streamlit")


# ==========================================
# MAIN INTERACTION TABS
# ==========================================
tab_sentiment, tab_spam, tab_batch, tab_metrics, tab_arch = st.tabs([
    "💬 Sentiment Analysis",
    "🛡️ Spam Detection",
    "📁 Batch Inference",
    "📊 Model Performance",
    "🏗️ Architecture & API"
])


# ------------------------------------------
# TAB 1: SENTIMENT ANALYSIS
# ------------------------------------------
with tab_sentiment:
    st.header("💬 Sentiment Analysis")
    st.write(
        "Analyze emotional tone and subjectivity in text using a sublinear TF-IDF "
        "vectorizer and regularized Logistic Regression trained on the Stanford Sentiment Treebank (SST-2)."
    )

    col_presets, col_empty = st.columns([3, 1])
    with col_presets:
        preset_choice = st.selectbox(
            "Or load a sample sentence:",
            [
                "-- Select a preset --",
                "A visual masterpiece that captures emotional depth with breathtaking cinematography.",
                "Terrible screenplay with wooden acting and predictable plot twists.",
                "The film has striking moments of brilliance despite its occasional slow pacing.",
                "An unforgettable journey filled with warmth, genuine humor, and heart.",
                "Boring, uninspired, and completely fails to engage the audience."
            ],
            key="sentiment_preset"
        )

    default_sentiment_text = ""
    if preset_choice != "-- Select a preset --":
        default_sentiment_text = preset_choice
    elif "sentiment_input_text" in st.session_state:
        default_sentiment_text = st.session_state["sentiment_input_text"]

    sentiment_text = st.text_area(
        "Enter text to analyze sentiment:",
        value=default_sentiment_text,
        height=130,
        placeholder="Type or paste any product review, movie critique, tweet, or statement...",
        key="sentiment_input_area"
    )

    col_btn, col_clear = st.columns([1, 5])
    with col_btn:
        analyze_sentiment = st.button("Analyze Sentiment", type="primary", use_container_width=True)

    if analyze_sentiment and sentiment_text.strip():
        if not sentiment_ready:
            st.error("Sentiment model is not loaded. Ensure sentiment_model.pkl exists in backend/app/models/.")
        else:
            with st.spinner("Classifying sentiment..."):
                result = sentiment_service.predict(sentiment_text.strip())

            pred_label = result["prediction"]
            confidence = result["confidence"]
            probs = result["probabilities"]
            pos_prob = probs.get("positive", 0.0)
            neg_prob = probs.get("negative", 0.0)

            st.divider()
            st.subheader("Classification Result")

            col_res1, col_res2, col_res3 = st.columns([1.5, 1.5, 3])

            with col_res1:
                st.markdown("**Prediction**")
                if pred_label == "positive":
                    st.markdown("<span class='badge-positive'>POSITIVE 😊</span>", unsafe_allow_html=True)
                else:
                    st.markdown("<span class='badge-negative'>NEGATIVE 😞</span>", unsafe_allow_html=True)

            with col_res2:
                st.markdown("**Confidence**")
                st.markdown(f"<span style='font-size: 1.5rem; font-weight: 700;'>{confidence * 100:.1f}%</span>", unsafe_allow_html=True)

            with col_res3:
                st.markdown("**Probability Gauge**")
                st.progress(pos_prob)
                st.caption(f"Negative: {neg_prob*100:.1f}% | Positive: {pos_prob*100:.1f}%")

            if HAS_PLOTLY:
                fig = go.Figure(data=[
                    go.Bar(
                        x=["Negative", "Positive"],
                        y=[neg_prob * 100, pos_prob * 100],
                        marker_color=["#ef4444", "#22c55e"],
                        text=[f"{neg_prob*100:.1f}%", f"{pos_prob*100:.1f}%"],
                        textposition="auto"
                    )
                ])
                fig.update_layout(
                    title="Class Probability Distribution",
                    yaxis_title="Probability (%)",
                    yaxis_range=[0, 100],
                    height=280,
                    margin=dict(l=20, r=20, t=40, b=20)
                )
                st.plotly_chart(fig, use_container_width=True)


# ------------------------------------------
# TAB 2: SPAM DETECTION
# ------------------------------------------
with tab_spam:
    st.header("🛡️ SMS & Message Spam Detection")
    st.write(
        "Detect unsolicited advertising, phishing schemes, and fraudulent promotions "
        "using a Multinomial Naive Bayes classifier trained on the UCI SMS Spam dataset (98.38% test accuracy)."
    )

    spam_preset = st.selectbox(
        "Or load a sample message:",
        [
            "-- Select a preset --",
            "URGENT! You have won a 1 week FREE vacation to Hawaii! Call 09061743813 to claim your prize now! T&Cs apply.",
            "Hey, are we still meeting for lunch at 1 PM today? Let me know!",
            "FREE MSG: Your mobile number has won a £1000 gift card. Text WIN to 80082 immediately.",
            "Can you please review the attached slide deck before tomorrow morning's presentation?",
            "Bank Alert: Your debit card has been suspended. Click http://bit.ly/secure-verify to restore access."
        ],
        key="spam_preset_choice"
    )

    default_spam_text = ""
    if spam_preset != "-- Select a preset --":
        default_spam_text = spam_preset

    spam_text = st.text_area(
        "Enter message to analyze:",
        value=default_spam_text,
        height=130,
        placeholder="Paste an SMS, email, or message here...",
        key="spam_input_area"
    )

    col_sbtn, col_sclear = st.columns([1, 5])
    with col_sbtn:
        analyze_spam = st.button("Detect Spam", type="primary", use_container_width=True)

    if analyze_spam and spam_text.strip():
        if not spam_ready:
            st.error("Spam model is not loaded. Ensure spam_model.pkl exists in backend/app/models/.")
        else:
            with st.spinner("Analyzing message..."):
                spam_res = spam_service.predict(spam_text.strip())

            is_spam = spam_res["prediction"] == "SPAM"
            spam_conf = spam_res["confidence"]
            probs = spam_res["probabilities"]
            spam_prob = probs.get("spam", 0.0)
            ham_prob = probs.get("ham", 0.0)

            st.divider()
            st.subheader("Inspection Result")

            col_r1, col_r2, col_r3 = st.columns([1.5, 1.5, 3])
            with col_r1:
                st.markdown("**Status**")
                if is_spam:
                    st.markdown("<span class='badge-spam'>🚨 SPAM / FRAUD</span>", unsafe_allow_html=True)
                else:
                    st.markdown("<span class='badge-ham'>✅ HAM / LEGITIMATE</span>", unsafe_allow_html=True)

            with col_r2:
                st.markdown("**Confidence**")
                st.markdown(f"<span style='font-size: 1.5rem; font-weight: 700;'>{spam_conf * 100:.1f}%</span>", unsafe_allow_html=True)

            with col_r3:
                st.markdown("**Spam Risk Meter**")
                st.progress(spam_prob)
                st.caption(f"Legitimate (Ham): {ham_prob*100:.1f}% | Spam Risk: {spam_prob*100:.1f}%")

            if HAS_PLOTLY:
                fig = go.Figure(data=[
                    go.Bar(
                        x=["Legitimate (Ham)", "Spam"],
                        y=[ham_prob * 100, spam_prob * 100],
                        marker_color=["#3b82f6", "#ef4444"],
                        text=[f"{ham_prob*100:.1f}%", f"{spam_prob*100:.1f}%"],
                        textposition="auto"
                    )
                ])
                fig.update_layout(
                    title="Spam vs. Ham Probability Breakdown",
                    yaxis_title="Probability (%)",
                    yaxis_range=[0, 100],
                    height=280,
                    margin=dict(l=20, r=20, t=40, b=20)
                )
                st.plotly_chart(fig, use_container_width=True)


# ------------------------------------------
# TAB 3: BATCH INFERENCE
# ------------------------------------------
with tab_batch:
    st.header("📁 Batch Text Inference")
    st.write("Run predictions on multiple inputs simultaneously via file upload or multi-line text input.")

    batch_task = st.radio("Choose NLP Task:", ["Sentiment Analysis", "Spam Detection"], horizontal=True)

    batch_mode = st.radio("Input Method:", ["Enter Multiple Lines", "Upload CSV/TXT File"], horizontal=True)

    items_to_process = []

    if batch_mode == "Enter Multiple Lines":
        sample_multiline = (
            "This product exceeded all my expectations!\n"
            "Terrible customer service and broken item.\n"
            "Average quality, nothing special.\n"
            "CLAIM YOUR FREE REWARD NOW http://spam.com\n"
            "Will meet you tomorrow at 10am for the project review."
        )
        batch_text = st.text_area("One text per line:", value=sample_multiline, height=160)
        if batch_text.strip():
            items_to_process = [line.strip() for line in batch_text.strip().split("\n") if line.strip()]
    else:
        uploaded_file = st.file_uploader("Upload CSV or TXT file", type=["csv", "txt"])
        if uploaded_file is not None:
            if uploaded_file.name.endswith(".csv"):
                df_upload = pd.read_csv(uploaded_file)
                text_col = st.selectbox("Select Text Column:", df_upload.columns.tolist())
                items_to_process = df_upload[text_col].dropna().astype(str).tolist()
            else:
                content = uploaded_file.read().decode("utf-8")
                items_to_process = [line.strip() for line in content.split("\n") if line.strip()]

    st.write(f"Total inputs ready for processing: **{len(items_to_process)}**")

    if st.button("Run Batch Inference", type="primary") and items_to_process:
        results = []
        progress_bar = st.progress(0.0)

        for i, text in enumerate(items_to_process):
            if batch_task == "Sentiment Analysis":
                res = sentiment_service.predict(text)
                results.append({
                    "Text": text,
                    "Prediction": res["prediction"].upper(),
                    "Confidence": f"{res['confidence']*100:.2f}%",
                    "Score_Negative": res["probabilities"]["negative"],
                    "Score_Positive": res["probabilities"]["positive"]
                })
            else:
                res = spam_service.predict(text)
                results.append({
                    "Text": text,
                    "Prediction": res["prediction"],
                    "Confidence": f"{res['confidence']*100:.2f}%",
                    "Score_Ham": res["probabilities"]["ham"],
                    "Score_Spam": res["probabilities"]["spam"]
                })
            progress_bar.progress((i + 1) / len(items_to_process))

        res_df = pd.DataFrame(results)
        st.success(f"Batch processing completed for {len(res_df)} items!")
        st.dataframe(res_df, use_container_width=True)

        csv_download = res_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Download Results as CSV",
            data=csv_download,
            file_name=f"nlp_batch_predictions_{batch_task.lower().replace(' ', '_')}.csv",
            mime="text/csv"
        )


# ------------------------------------------
# TAB 4: MODEL PERFORMANCE & BENCHMARKS
# ------------------------------------------
with tab_metrics:
    st.header("📊 Model Performance & Benchmarks")
    st.write("Rigorous quantitative metrics evaluated on held-out test sets.")

    # 1. Sentiment Metrics
    st.subheader("1. Sentiment Analysis (SST-2 Benchmark)")
    sent_metrics = sentiment_service.get_metrics()
    if sent_metrics:
        col_m1, col_m2, col_m3, col_m4 = st.columns(4)
        m = sent_metrics.get("metrics", {})
        col_m1.metric("Accuracy", f"{m.get('accuracy', 0)*100:.2f}%")
        col_m2.metric("Precision", f"{m.get('precision', 0)*100:.2f}%")
        col_m3.metric("Recall", f"{m.get('recall', 0)*100:.2f}%")
        col_m4.metric("F1 Score", f"{m.get('f1_score', 0)*100:.2f}%")

        col_cm1, col_cr1 = st.columns([1, 1])
        with col_cm1:
            st.markdown("**Confusion Matrix (N = 1,384 test samples)**")
            cm = sent_metrics.get("confusion_matrix", [[479, 183], [134, 588]])
            cm_df = pd.DataFrame(
                cm,
                index=["Actual Negative", "Actual Positive"],
                columns=["Predicted Negative", "Predicted Positive"]
            )
            st.table(cm_df)

        with col_cr1:
            st.markdown("**Per-Class Breakdown**")
            cr = sent_metrics.get("classification_report", {})
            cr_display = {
                "Negative": {
                    "Precision": f"{cr.get('negative', {}).get('precision', 0)*100:.1f}%",
                    "Recall": f"{cr.get('negative', {}).get('recall', 0)*100:.1f}%",
                    "F1": f"{cr.get('negative', {}).get('f1-score', 0)*100:.1f}%",
                    "Support": int(cr.get('negative', {}).get('support', 0))
                },
                "Positive": {
                    "Precision": f"{cr.get('positive', {}).get('precision', 0)*100:.1f}%",
                    "Recall": f"{cr.get('positive', {}).get('recall', 0)*100:.1f}%",
                    "F1": f"{cr.get('positive', {}).get('f1-score', 0)*100:.1f}%",
                    "Support": int(cr.get('positive', {}).get('support', 0))
                }
            }
            st.table(pd.DataFrame(cr_display).T)

    st.divider()

    # 2. Spam Metrics
    st.subheader("2. Spam Detection (UCI SMS Spam Benchmark)")
    sp_metrics = spam_service.get_metrics()
    if sp_metrics:
        col_sm1, col_sm2, col_sm3, col_sm4 = st.columns(4)
        sm = sp_metrics.get("metrics", {})
        col_sm1.metric("Accuracy", f"{sm.get('accuracy', 0)*100:.2f}%")
        col_sm2.metric("Precision", f"{sm.get('precision', 0)*100:.2f}%")
        col_sm3.metric("Recall", f"{sm.get('recall', 0)*100:.2f}%")
        col_sm4.metric("F1 Score", f"{sm.get('f1_score', 0)*100:.2f}%")

        col_scm1, col_scr1 = st.columns([1, 1])
        with col_scm1:
            st.markdown("**Confusion Matrix (N = 1,114 test samples)**")
            scm = sp_metrics.get("confusion_matrix", [[965, 0], [18, 131]])
            scm_df = pd.DataFrame(
                scm,
                index=["Actual Ham (Legit)", "Actual Spam"],
                columns=["Predicted Ham", "Predicted Spam"]
            )
            st.table(scm_df)

        with col_scr1:
            st.markdown("**Per-Class Breakdown**")
            scr = sp_metrics.get("classification_report", {})
            scr_display = {
                "Ham (Legitimate)": {
                    "Precision": f"{scr.get('ham', {}).get('precision', 0)*100:.1f}%",
                    "Recall": f"{scr.get('ham', {}).get('recall', 0)*100:.1f}%",
                    "F1": f"{scr.get('ham', {}).get('f1-score', 0)*100:.1f}%",
                    "Support": int(scr.get('ham', {}).get('support', 0))
                },
                "Spam (Unsolicited)": {
                    "Precision": f"{scr.get('spam', {}).get('precision', 0)*100:.1f}%",
                    "Recall": f"{scr.get('spam', {}).get('recall', 0)*100:.1f}%",
                    "F1": f"{scr.get('spam', {}).get('f1-score', 0)*100:.1f}%",
                    "Support": int(scr.get('spam', {}).get('support', 0))
                }
            }
            st.table(pd.DataFrame(scr_display).T)


# ------------------------------------------
# TAB 5: ARCHITECTURE & API
# ------------------------------------------
with tab_arch:
    st.header("🏗️ Architecture & REST API Documentation")
    st.write("This application can be run standalone or paired with the FastAPI backend and React frontend.")

    st.markdown("""
    ### System Architecture Overview
    ```text
    +-----------------------------------------------------------------------------------------+
    |                                 User Interfaces                                         |
    |   [ Streamlit App (app.py) ]               [ React + Vite Dashboard (frontend/) ]       |
    +------------------------------+---------------------------+------------------------------+
                                   |                           |
                       Direct In-Process Python        HTTP / REST API (JSON)
                                   |                           |
                                   |               +-----------v------------+
                                   |               |    FastAPI Backend     |
                                   |               |  (backend/app/main.py) |
                                   |               +-----------+------------+
                                   |                           |
    +------------------------------v---------------------------v------------------------------+
    |                              Inference Service Layer                                    |
    |                 (SentimentService, SpamService, Text Preprocessing)                     |
    +----------------------------------------------+------------------------------------------+
                                                   |
    +----------------------------------------------v------------------------------------------+
    |                               Serialized Model Artifacts                                |
    |      sentiment_model.pkl, sentiment_vectorizer.pkl, spam_model.pkl, spam_vectorizer.pkl |
    +-----------------------------------------------------------------------------------------+
    ```
    """)

    st.subheader("Available REST Endpoints (FastAPI)")
    api_data = [
        {"Method": "GET", "Endpoint": "/health", "Description": "Liveness and system readiness probe"},
        {"Method": "GET", "Endpoint": "/api/metrics", "Description": "Returns JSON metrics and confusion matrices for all models"},
        {"Method": "POST", "Endpoint": "/api/sentiment/predict", "Description": "Predict sentiment with confidence scores"},
        {"Method": "POST", "Endpoint": "/api/spam/predict", "Description": "Detect spam in SMS/email text with class probabilities"},
        {"Method": "GET", "Endpoint": "/docs", "Description": "Interactive Swagger UI documentation"}
    ]
    st.table(pd.DataFrame(api_data))

    st.subheader("Quickstart Commands")
    st.code("""
# 1. Run this Streamlit App directly:
streamlit run app.py

# 2. Or run the FastAPI backend:
uvicorn backend.app.main:app --reload --port 8000

# 3. Or run the React Frontend:
cd frontend && npm run dev
    """, language="bash")


# ==========================================
# CLI BOOTSTRAPPER
# ==========================================
if __name__ == "__main__":
    # If run with 'python app.py' directly outside streamlit runtime, launch it
    try:
        from streamlit.web import cli as stcli
        # Only invoke cli if this script is the primary entry point
        if not any("streamlit" in arg for arg in sys.argv):
            sys.argv = ["streamlit", "run", str(Path(__file__).resolve())]
            sys.exit(stcli.main())
    except Exception:
        pass
