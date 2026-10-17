# Diabetes Risk & Lifestyle Advisor

An AI-based clinical decision-support system that predicts diabetes risk from patient health metrics and generates personalized lifestyle recommendations — combining three complementary AI techniques into an interpretable pipeline.

> ⚠️ **Medical Disclaimer**: This system is an educational and screening support tool. It is **NOT** a medical diagnostic instrument. Always consult a qualified healthcare provider for clinical evaluation.

---

## System Architecture

```
Patient Health Metrics (Required Core + Optional Clinical Tests)
                           ↓
Stage 1: Neural Network (MLPClassifier)
         ↳ Predicts continuous risk probability (0.0 – 1.0)
                           ↓
Stage 2: Fuzzy Logic Inference Engine (scikit-fuzzy)
         ↳ Resolves non-linear metric interactions (BMI, Activity, HbA1c)
         ↳ Produces a defuzzified risk score (0 – 100) and category:
           [ Low | Moderate | High | Severe ]
                           ↓
Stage 3: Rule-Based Expert System (Clinical Guidelines)
         ↳ Contextual, multi-tiered lifestyle & clinical recommendations
                           ↓
Interactive Dashboard (Streamlit Web Application)
```

Each stage feeds directly into the next: the Fuzzy Engine refines the Neural Network's statistical risk using lifestyle factors, and the Rule-Based Engine tailors recommendations based on the fuzzy tier and patient-specific biomarkers.

---

## Patient Input Metrics

The interface is streamlined to prevent user fatigue while accommodating clinical depth:

### 1. Core Inputs (Always Visible)
* **Biological Sex / Gender**: Female, Male, or Other (Pregnancies field auto-displays only for Female).
* **Blood Glucose (mg/dL)**: Plasma glucose level (fasting or random).
* **BMI (kg/m²)**: Body Mass Index.
* **Age (years)**: Patient age.
* **Hypertension**: Diagnosed high blood pressure (Yes / No).
* **Heart Disease**: Diagnosed cardiovascular condition (Yes / No).
* **Smoking History**: Never, Former, or Current smoker.
* **Physical Activity Level**: Self-reported lifestyle scale (1–10).

### 2. Optional Clinical Inputs (Collapsible Expander)
If patients have lab or family history reports, they can toggle these optional inputs to refine their assessment:
* **HbA1c (%)**: Glycated haemoglobin (if omitted, estimated from Glucose via the clinical ADAG formula).
* **Blood Pressure (mm Hg)**: Diastolic blood pressure.
* **Serum Insulin (μU/mL)**: 2-hour post-load or fasting insulin.
* **Family History Score (DPF)**: Diabetes Pedigree Function score.

*(Note: Redundant metrics such as Triceps Skin Thickness have been eliminated to keep inputs intuitive and accessible.)*

---

## AI Pipeline Details

### 1. Neural Network (`nn_model.py`)
* **Model**: Multi-Layer Perceptron Classifier (`MLPClassifier`) with 3 hidden layers: `(32, 16, 8)` neurons.
* **Input Feature Vector (8 features)**: `Sex_Code`, `Age`, `BMI`, `Glucose`, `HbA1c`, `Hypertension`, `HeartDisease`, `SmokingEncoded`.
* **Preprocessing & Scaling**: `StandardScaler` normalization; minority class oversampling to resolve clinical class imbalance.
* **Missing Value Imputation**: When HbA1c is not provided, the model clinically derives estimated HbA1c from blood glucose using the ADAG formula:
  $$\text{HbA1c} = \frac{\text{Glucose} + 46.7}{28.7}$$
* **Performance**: **~96.9% Accuracy**, **~97.2% Precision**, **~95.8% Recall**, and **~96.5% F1 Score** on held-out test data.

### 2. Fuzzy Logic Inference Engine (`fuzzy_engine.py`)
* **Antecedents**:
  * `risk_probability` (Trapezoidal / Triangular: Low, Medium, High)
  * `bmi` (Underweight, Normal, Overweight, Obese)
  * `activity_level` (Sedentary, Moderate, Active)
  * `hba1c` (Optional Antecedent: Normal, Prediabetic, Diabetic)
* **Consequent**: `risk_category` (0 – 100 score; Low, Moderate, High, Severe).
* **Adaptive Control System**:
  * **4-Variable Mode**: Evaluates 22 Mamdani fuzzy rules when HbA1c is supplied.
  * **3-Variable Fallback**: Seamlessly falls back to a 3-variable rule set when HbA1c is omitted.
* **Defuzzification**: Centroid method yielding a crisp composite score.

### 3. Rule-Based Expert System (`rules_engine.py`)
* **Baseline Tiers**: Recommendations tailored to Low, Moderate, High, or Severe classification.
* **Biomarker Thresholds**: Distinct triggers for elevated Glucose, severe obesity, hypertensive crisis, and insulin resistance.
* **Demographic Rules**: Gender-specific advice (e.g., gestational risk in multiparous women, age-specific screening for men over 45).
* **Comorbidity Modifiers**: Multi-factorial risk warnings when hypertension, heart disease, or active smoking co-occur.
* **Symptom Pattern Detection**: Rule sets calibrated with clinical symptom datasets (polyuria, polydipsia, unexplained weight loss).

---

## Datasets

All datasets are consolidated in the [`datasets/`](datasets/) directory and harmonized by [`data_pipeline.py`](data_pipeline.py):

| Dataset | Records | Demographics | Key Features |
|---|---|---|---|
| **Mustafa 100k** (`datasets/mustafa_100k/`) | 100,000 | Multi-gender (Female, Male, Other) | Glucose, HbA1c, Age, BMI, Hypertension, Heart Disease, Smoking |
| **DTD Multi-Type** (`datasets/dtd_multitype/`) | 70,000 | Multi-type (T1D, T2D, Gestational, MODY) | Glucose, Blood Pressure, BMI, Age, Smoking, Complications |
| **Pima Indians** (`datasets/pima_indians/`) | 768 | Adult females | Glucose, Insulin, BP, BMI, DPF, Age |
| **Sylhet Clinical Symptoms** (`datasets/sylhet_symptoms/`) | 520 | Early-stage clinical cohort | Polyuria, Polydipsia, Weight Loss, Weakness |

*Combined training pool: **157,115 deduplicated, clean records**.*

---

## Project Structure

```
├── app.py                  # Streamlit dashboard & user interface
├── nn_model.py             # Neural network architecture, training & inference
├── fuzzy_engine.py         # Fuzzy logic membership functions & inference rules
├── rules_engine.py         # Rule-based clinical recommendation expert system
├── data_pipeline.py        # Multi-dataset cleaning, mapping & harmonization pipeline
├── download_datasets.py    # Automated Kaggle dataset downloader
├── test_pipeline.py        # Comprehensive test harness with diverse patient profiles
├── model.pkl               # Serialized trained MLPClassifier model
├── scaler.pkl              # Serialized StandardScaler
├── requirements.txt        # Python library dependencies
└── datasets/               # Consolidated dataset repository
    ├── mustafa_100k/       # Mustafa 100k prediction dataset
    ├── dtd_multitype/      # Multi-type diabetes dataset
    ├── pima_indians/       # Pima Indians diabetes dataset
    └── sylhet_symptoms/    # Early-stage symptoms dataset
```

---

## Quickstart Guide

### 1. Clone & Install Dependencies
```bash
git clone https://github.com/Manidu2005/diabetes-risk-advisor.git
cd diabetes-risk-advisor
pip install -r requirements.txt
```

### 2. (Optional) Retrain Neural Network
```bash
python nn_model.py
```
*(Pre-trained weights `model.pkl` and `scaler.pkl` are included ready to use).*

### 3. Launch the Web Application
```bash
streamlit run app.py
```

### 4. Run Automated Test Suite
```bash
python test_pipeline.py
```
Validates individual modules and runs end-to-end evaluations across diverse patient profiles (Young, Elderly, Smoker, Non-Binary, and Minimal/Optional Inputs).

---

## Ethical & Clinical Considerations

* **Mitigation of Demographic Bias**: Earlier diabetes screening models often trained exclusively on the 1960s Pima Indians dataset (limited to adult females of one ethnic background). This system overcomes that limitation by harmonizing multiple diverse datasets with over 157,000 records across Female, Male, and Other categories.
* **Transparent Reasoning**: Unlike black-box predictors, combining Neural Networks with Fuzzy Logic and explicit Rules ensures that patients and clinicians can trace *why* a particular risk tier or recommendation was generated.
* **Safe Decision Support**: Missing laboratory values never cause system crashes or arbitrary estimates; clinically validated fallback equations (ADAG formula) and multi-variable logic guarantee consistent behavior.
