"""
Diabetes Risk & Lifestyle Advisor — Streamlit Dashboard
Chains: Neural Network → Fuzzy Logic → Rule-Based Engine
"""

import streamlit as st
import os
import sys

# Ensure project directory is on the path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from nn_model import predict_risk, train_model
from fuzzy_engine import categorize_risk
from rules_engine import get_recommendations, format_recommendations


# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Diabetes Risk & Lifestyle Advisor",
    page_icon="🩺",
    layout="wide",
)

# ── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .risk-low { background-color: #d4edda; color: #155724; padding: 15px; border-radius: 10px; text-align: center; font-size: 1.4em; font-weight: bold; }
    .risk-moderate { background-color: #fff3cd; color: #856404; padding: 15px; border-radius: 10px; text-align: center; font-size: 1.4em; font-weight: bold; }
    .risk-high { background-color: #f8d7da; color: #721c24; padding: 15px; border-radius: 10px; text-align: center; font-size: 1.4em; font-weight: bold; }
    .risk-severe { background-color: #d32f2f; color: white; padding: 15px; border-radius: 10px; text-align: center; font-size: 1.4em; font-weight: bold; }
    .metric-card { background-color: #f8f9fa; padding: 12px; border-radius: 8px; text-align: center; margin-bottom: 10px; }
    .disclaimer { background-color: #e3f2fd; color: #1a237e; padding: 12px; border-radius: 8px; border-left: 4px solid #1976d2; font-size: 0.9em; }
</style>
""", unsafe_allow_html=True)


# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.image("https://img.icons8.com/color/96/heart-with-pulse.png", width=64)
    st.title("ℹ️ About")
    st.markdown("""
    **Diabetes Risk & Lifestyle Advisor** uses three AI techniques in a pipeline:
    
    1. 🧠 **Neural Network** — predicts diabetes risk probability from health metrics
    2. 🌫️ **Fuzzy Logic** — categorizes risk considering BMI and activity level
    3. 📋 **Rule-Based Engine** — generates personalized lifestyle recommendations
    """)

    st.divider()
    st.subheader("📊 Dataset Info")
    st.markdown("""
    **Pima Indians Diabetes Dataset**
    - 768 patients, 8 health metrics
    - Source: NIDDK / UCI ML Repository
    - Population: Pima Native American women, age ≥ 21
    """)
    
    st.divider()
    st.subheader("⚠️ Limitations")
    st.markdown("""
    - Dataset contains only women of Pima heritage
    - Model may not generalize to other demographics
    - This is a **screening tool**, not a medical diagnosis
    """)

    st.divider()
    st.subheader("🛠️ Tech Stack")
    st.markdown("""
    - `scikit-learn` MLPClassifier
    - `scikit-fuzzy` inference engine
    - Python rule-based reasoning
    - `Streamlit` dashboard
    """)


# ── Main Title ───────────────────────────────────────────────────────────────
st.title("🩺 Diabetes Risk & Lifestyle Advisor")
st.markdown("Enter your health metrics below to receive a **personalized risk assessment** and **lifestyle recommendations**.")
st.divider()


# ── Input Form ───────────────────────────────────────────────────────────────
st.subheader("📝 Patient Health Metrics")

col1, col2, col3 = st.columns(3)

with col1:
    pregnancies = st.number_input(
        "Pregnancies",
        min_value=0, max_value=20, value=1, step=1,
        help="Number of times pregnant"
    )
    glucose = st.number_input(
        "Glucose (mg/dL)",
        min_value=0.0, max_value=300.0, value=120.0, step=1.0,
        help="Plasma glucose concentration (2-hour oral glucose tolerance test)"
    )
    blood_pressure = st.number_input(
        "Blood Pressure (mm Hg)",
        min_value=0.0, max_value=200.0, value=72.0, step=1.0,
        help="Diastolic blood pressure"
    )

with col2:
    skin_thickness = st.number_input(
        "Skin Thickness (mm)",
        min_value=0.0, max_value=100.0, value=29.0, step=1.0,
        help="Triceps skin fold thickness"
    )
    insulin = st.number_input(
        "Insulin (μU/mL)",
        min_value=0.0, max_value=900.0, value=125.0, step=1.0,
        help="2-Hour serum insulin"
    )
    bmi = st.number_input(
        "BMI (kg/m²)",
        min_value=0.0, max_value=70.0, value=28.0, step=0.1,
        help="Body Mass Index = weight(kg) / height(m)²"
    )

with col3:
    dpf = st.number_input(
        "Family History Score",
        min_value=0.0, max_value=2.5, value=0.3725, step=0.01,
        format="%.4f",
        help="Diabetes Pedigree Function — scores genetic predisposition (typical range 0.08–2.42, median ≈ 0.37)"
    )
    age = st.number_input(
        "Age (years)",
        min_value=1, max_value=120, value=33, step=1,
        help="Patient age in years"
    )
    activity_level = st.slider(
        "🏃 Activity Level",
        min_value=1, max_value=10, value=5,
        help="Self-reported: 1 = very sedentary, 10 = very active"
    )

st.divider()


# ── Predict Button ───────────────────────────────────────────────────────────
if st.button("🔍 Analyze Risk", type="primary", use_container_width=True):
    
    # Build patient data dict
    patient_data = {
        'Pregnancies': pregnancies,
        'Glucose': glucose,
        'BloodPressure': blood_pressure,
        'SkinThickness': skin_thickness,
        'Insulin': insulin,
        'BMI': bmi,
        'DiabetesPedigreeFunction': dpf,
        'Age': age,
        'activity_level': activity_level
    }
    
    # ── Stage 1: Neural Network ──────────────────────────────────────────
    with st.spinner("🧠 Running Neural Network prediction..."):
        try:
            risk_prob = predict_risk(patient_data)
        except Exception as e:
            st.error(f"Neural Network error: {e}")
            st.info("Training the model for the first time. Please click 'Analyze Risk' again.")
            try:
                train_model()
                risk_prob = predict_risk(patient_data)
            except Exception as e2:
                st.error(f"Failed to train model: {e2}")
                st.stop()
    
    # ── Stage 2: Fuzzy Logic ─────────────────────────────────────────────
    with st.spinner("🌫️ Running Fuzzy Logic categorization..."):
        fuzzy_result = categorize_risk(risk_prob, bmi, activity_level)
    
    # ── Stage 3: Rule-Based Recommendations ──────────────────────────────
    with st.spinner("📋 Generating recommendations..."):
        recommendations = get_recommendations(fuzzy_result['category'], patient_data)
    
    # ── Display Results ──────────────────────────────────────────────────
    st.divider()
    st.subheader("📊 Risk Assessment Results")
    
    # Pipeline visualization
    st.markdown("**Pipeline**: Neural Network ➜ Fuzzy Logic ➜ Rule-Based Engine")
    
    res_col1, res_col2, res_col3 = st.columns(3)
    
    with res_col1:
        st.markdown("##### 🧠 Neural Network Output")
        risk_pct = risk_prob * 100
        st.metric("Risk Probability", f"{risk_pct:.1f}%")
        # Color-coded progress bar
        st.progress(min(risk_prob, 1.0))
    
    with res_col2:
        st.markdown("##### 🌫️ Fuzzy Logic Output")
        category = fuzzy_result['category']
        score = fuzzy_result['score']
        css_class = f"risk-{category.lower()}"
        st.markdown(f'<div class="{css_class}">⬤ {category} Risk</div>', unsafe_allow_html=True)
        st.metric("Fuzzy Score", f"{score:.1f} / 100")
    
    with res_col3:
        st.markdown("##### 📋 Summary")
        st.metric("Recommendations Generated", len(recommendations) - 1)  # -1 for disclaimer
        st.metric("Activity Level", f"{activity_level}/10")
    
    # ── Recommendations ──────────────────────────────────────────────────
    st.divider()
    st.subheader("💡 Personalized Recommendations")
    
    # Separate disclaimer from recommendations
    disclaimer = recommendations[0] if recommendations else ""
    actual_recs = recommendations[1:] if len(recommendations) > 1 else []
    
    # Display recommendations
    for i, rec in enumerate(actual_recs, 1):
        # Choose icon based on content
        if any(word in rec.lower() for word in ['exercise', 'activity', 'walk', 'physical']):
            icon = "🏃"
        elif any(word in rec.lower() for word in ['diet', 'food', 'sugar', 'carbohydrate', 'caloric', 'sodium', 'glycemic', 'hydrated']):
            icon = "🥗"
        elif any(word in rec.lower() for word in ['doctor', 'physician', 'medical', 'consult', 'screening', 'check-up', 'counseling', 'medication']):
            icon = "🏥"
        elif any(word in rec.lower() for word in ['monitor', 'glucose level', 'blood pressure', 'weight', 'bmi']):
            icon = "📏"
        else:
            icon = "✅"
        st.markdown(f"{icon} **{i}.** {rec}")
    
    # Disclaimer at the bottom
    st.divider()
    st.markdown(f'<div class="disclaimer">{disclaimer}</div>', unsafe_allow_html=True)

    # ── Detailed Breakdown (Expander) ────────────────────────────────────
    with st.expander("🔎 View Detailed Pipeline Breakdown"):
        st.markdown("##### Stage 1: Neural Network")
        st.json({
            "input": {k: v for k, v in patient_data.items() if k != 'activity_level'},
            "output": {"risk_probability": round(risk_prob, 4)}
        })
        
        st.markdown("##### Stage 2: Fuzzy Logic")
        st.json({
            "input": {
                "risk_probability": round(risk_prob, 4),
                "bmi": bmi,
                "activity_level": activity_level
            },
            "output": fuzzy_result
        })
        
        st.markdown("##### Stage 3: Rule-Based Engine")
        st.json({
            "input": {
                "risk_category": fuzzy_result['category'],
                "patient_metrics_checked": list(patient_data.keys())
            },
            "output": {
                "recommendation_count": len(actual_recs),
                "recommendations": actual_recs
            }
        })


# ── Footer ───────────────────────────────────────────────────────────────────
st.divider()
st.caption(
    "🩺 **Diabetes Risk & Lifestyle Advisor** — "
    "Essentials of Artificial Intelligence Group Assignment  \n"
    "⚠️ This tool is for **educational and screening purposes only**. "
    "It is NOT a substitute for professional medical advice, diagnosis, or treatment. "
    "Always consult a qualified healthcare provider."
)
