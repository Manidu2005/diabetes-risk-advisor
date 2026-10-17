"""
Diabetes Risk & Lifestyle Advisor  --  Streamlit Dashboard
Chains: Neural Network → Fuzzy Logic → Rule-Based Engine
Supports Male, Female, and Other patient demographics.
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



# ── Main Title ───────────────────────────────────────────────────────────────
st.title("🩺 Diabetes Risk & Lifestyle Advisor")
st.markdown("Enter your health metrics below to receive a **personalized risk assessment** and **lifestyle recommendations**.")
st.divider()


# ── Input Form ───────────────────────────────────────────────────────────────
st.subheader("📝 Patient Health Metrics")

col1, col2, col3 = st.columns(3)

with col1:
    gender = st.selectbox(
        "Gender / Sex",
        options=["Female", "Male", "Other"],
        index=0,
        help="Biological sex  --  affects risk factors and recommendations"
    )

    # Map gender to Sex_Code
    sex_code = {"Female": 0, "Male": 1, "Other": 2}[gender]

    # Pregnancies  --  only show for Female
    if gender == "Female":
        pregnancies = st.number_input(
            "Pregnancies",
            min_value=0, max_value=20, value=1, step=1,
            help="Number of times pregnant"
        )
    else:
        pregnancies = 0
        st.markdown(
            '<div style="padding: 4px 0; color: #888; font-size: 0.85em;">'
            '💡 Pregnancies auto-set to 0 for Male / Other</div>',
            unsafe_allow_html=True,
        )

    glucose = st.number_input(
        "Glucose (mg/dL)",
        min_value=0.0, max_value=300.0, value=120.0, step=1.0,
        help="Plasma glucose concentration (fasting or 2-hour OGTT)"
    )
with col2:
    bmi = st.number_input(
        "BMI (kg/m²)",
        min_value=0.0, max_value=70.0, value=28.0, step=0.1,
        help="Body Mass Index = weight(kg) / height(m)²"
    )
    age = st.number_input(
        "Age (years)",
        min_value=1, max_value=120, value=33, step=1,
        help="Patient age in years"
    )
    hypertension = st.checkbox("🫀 Hypertension", value=False, help="Has been diagnosed with hypertension")
    heart_disease = st.checkbox("❤️‍🩹 Heart Disease", value=False, help="Has been diagnosed with heart disease")

with col3:
    smoking_history = st.selectbox(
        "🚬 Smoking History",
        options=["Never", "Former", "Current"],
        index=0,
        help="Smoking status"
    )
    activity_level = st.slider(
        "🏃 Activity Level",
        min_value=1, max_value=10, value=5,
        help="Self-reported: 1 = very sedentary, 10 = very active"
    )

# ── Optional Inputs (improve accuracy when provided) ─────────────────────
with st.expander("🔬 Optional Inputs (provide for more accurate analysis)", expanded=False):
    st.caption(
        "These fields are optional. When provided, they improve the accuracy "
        "of the risk assessment and enable additional personalised recommendations."
    )

    opt_col1, opt_col2 = st.columns(2)

    with opt_col1:
        provide_hba1c = st.checkbox("I know my HbA1c (%)", value=False)
        if provide_hba1c:
            hba1c = st.number_input(
                "HbA1c (%)",
                min_value=0.0, max_value=15.0, value=5.5, step=0.1,
                help="Glycated haemoglobin  --  Normal: <5.7%, Prediabetes: 5.7-6.4%, Diabetes: >=6.5%"
            )
        else:
            hba1c = None

        provide_bp = st.checkbox("I know my Blood Pressure", value=False)
        if provide_bp:
            blood_pressure = st.number_input(
                "Blood Pressure (mm Hg)",
                min_value=0.0, max_value=200.0, value=72.0, step=1.0,
                help="Diastolic blood pressure"
            )
        else:
            blood_pressure = None

    with opt_col2:
        provide_insulin = st.checkbox("I know my Insulin level", value=False)
        if provide_insulin:
            insulin = st.number_input(
                "Insulin (μU/mL)",
                min_value=0.0, max_value=900.0, value=125.0, step=1.0,
                help="2-Hour serum insulin"
            )
        else:
            insulin = None

        provide_dpf = st.checkbox("I know my Family History Score", value=False)
        if provide_dpf:
            dpf = st.number_input(
                "Family History Score",
                min_value=0.0, max_value=2.5, value=0.3725, step=0.01,
                format="%.4f",
                help="Diabetes Pedigree Function  --  scores genetic predisposition "
                     "(typical range 0.08-2.42, median ≈ 0.37)"
            )
        else:
            dpf = None

st.divider()


# ── Predict Button ───────────────────────────────────────────────────────────
if st.button("🔍 Analyze Risk", type="primary", use_container_width=True):
    
    # Build patient data dict
    patient_data = {
        'Gender': gender,
        'Sex_Code': sex_code,
        'Pregnancies': pregnancies,
        'Glucose': glucose,
        'BloodPressure': blood_pressure,
        'Insulin': insulin,
        'BMI': bmi,
        'DiabetesPedigreeFunction': dpf,
        'HbA1c': hba1c,
        'Age': age,
        'Hypertension': int(hypertension),
        'HeartDisease': int(heart_disease),
        'SmokingHistory': smoking_history.lower(),
        'activity_level': activity_level,
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
        fuzzy_result = categorize_risk(risk_prob, bmi, activity_level, hba1c)
    
    # ── Stage 3: Rule-Based Recommendations ──────────────────────────────
    with st.spinner("📋 Generating recommendations..."):
        recommendations = get_recommendations(fuzzy_result['category'], patient_data)
    
    # ── Display Results ──────────────────────────────────────────────────
    st.divider()
    st.subheader("📊 Risk Assessment Results")
    
    # Patient info banner
    hba1c_str = f"HbA1c {hba1c}%" if hba1c is not None else "HbA1c: Not provided"
    bp_str = f" · BP {blood_pressure:.0f} mmHg" if blood_pressure is not None else ""
    st.markdown(
        f"**Patient**: {gender}, Age {age} · BMI {bmi} · {hba1c_str}{bp_str} · "
        f"Glucose {glucose} mg/dL · "
        f"{'Hypertensive' if hypertension else 'Normotensive'} · "
        f"Smoking: {smoking_history}"
    )
    
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
        elif any(word in rec.lower() for word in ['doctor', 'physician', 'medical', 'consult', 'screening', 'check-up', 'counseling', 'medication', 'ob-gyn', 'cardiologist']):
            icon = "🏥"
        elif any(word in rec.lower() for word in ['monitor', 'glucose level', 'blood pressure', 'weight', 'bmi', 'hba1c']):
            icon = "📏"
        elif any(word in rec.lower() for word in ['smoking', 'tobacco', 'cessation']):
            icon = "🚭"
        elif any(word in rec.lower() for word in ['symptom', 'polyuria', 'polydipsia', 'triad']):
            icon = "🔬"
        else:
            icon = "✅"
        st.markdown(f"{icon} **{i}.** {rec}")
    
    # Disclaimer at the bottom
    st.divider()
    st.markdown(f'<div class="disclaimer">{disclaimer}</div>', unsafe_allow_html=True)


# ── Footer ───────────────────────────────────────────────────────────────────
st.divider()
st.caption(
    "🩺 **Diabetes Risk & Lifestyle Advisor**  --  "
    "Essentials of Artificial Intelligence Group Assignment  \n"
    "⚠️ This tool is for **educational and screening purposes only**. "
    "It is NOT a substitute for professional medical advice, diagnosis, or treatment. "
    "Always consult a qualified healthcare provider."
)
