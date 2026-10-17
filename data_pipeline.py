"""
Data Pipeline  --  Multi-Dataset Harmonization Module
Loads, cleans, and harmonises diabetes datasets into a unified schema
for training the neural network and supporting the fuzzy/rules engines.

Unified feature schema (output):
    Sex_Code          : 0 = Female, 1 = Male, 2 = Other
    Age               : years
    BMI               : kg/m²
    Glucose           : blood glucose in mg/dL
    HbA1c             : glycated haemoglobin in %
    Hypertension      : 0 / 1
    HeartDisease       : 0 / 1
    SmokingEncoded    : 0 = never/no_info, 1 = former/not_current, 2 = ever/current
    Outcome           : 0 = non-diabetic, 1 = diabetic
"""

import os
import numpy as np
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------------------
# Smoking history encoding map
# ---------------------------------------------------------------------------
SMOKING_MAP = {
    'never': 0, 'no info': 0, 'not current': 1,
    'former': 1, 'ever': 2, 'current': 2,
}

FEATURE_COLUMNS = [
    'Sex_Code', 'Age', 'BMI', 'Glucose', 'HbA1c',
    'Hypertension', 'HeartDisease', 'SmokingEncoded',
]

TARGET_COLUMN = 'Outcome'


# ---------------------------------------------------------------------------
# Loaders for each dataset
# ---------------------------------------------------------------------------

def load_mustafa(filepath: str | None = None) -> pd.DataFrame:
    """
    Load the Comprehensive Diabetes Prediction Dataset (Mustafa 100k).
    Columns: gender, age, hypertension, heart_disease, smoking_history,
             bmi, HbA1c_level, blood_glucose_level, diabetes
    """
    if filepath is None:
        filepath = os.path.join(
            BASE_DIR, 'datasets', 'mustafa_100k',
            'diabetes_prediction_dataset.csv',
        )
    if not os.path.isfile(filepath):
        return pd.DataFrame()

    df = pd.read_csv(filepath)
    df.drop_duplicates(inplace=True)

    # Gender encoding
    gender_map = {'Female': 0, 'Male': 1, 'Other': 2}
    df['Sex_Code'] = df['gender'].map(gender_map).fillna(2).astype(int)

    # Smoking encoding
    df['SmokingEncoded'] = (
        df['smoking_history'].str.lower().str.strip()
        .map(SMOKING_MAP).fillna(0).astype(int)
    )

    # Rename to unified schema
    df = df.rename(columns={
        'age': 'Age',
        'bmi': 'BMI',
        'blood_glucose_level': 'Glucose',
        'HbA1c_level': 'HbA1c',
        'hypertension': 'Hypertension',
        'heart_disease': 'HeartDisease',
        'diabetes': 'Outcome',
    })

    return df[FEATURE_COLUMNS + [TARGET_COLUMN]]


def load_dtd(filepath: str | None = None) -> pd.DataFrame:
    """
    Load Multi-Type Diabetes Dataset (DTD  --  12,016 rows).
    Columns: Sex, NPregnancies, Age, BPressure, BMI, HbA1c,
             Insulin, FGlucose, PGlucose, Diagnosis, DiagnosisType
    """
    if filepath is None:
        filepath = os.path.join(
            BASE_DIR, 'datasets', 'dtd_multitype', 'diabetes.csv',
        )
    if not os.path.isfile(filepath):
        return pd.DataFrame()

    df = pd.read_csv(filepath)
    df.drop_duplicates(inplace=True)

    # Gender
    sex_map = {'Female': 0, 'female': 0, 'Male': 1, 'male': 1}
    df['Sex_Code'] = df['Sex'].map(sex_map).fillna(2).astype(int)

    df = df.rename(columns={
        'Age': 'Age', 'BMI': 'BMI',
        'FGlucose': 'Glucose', 'HbA1c': 'HbA1c',
    })

    # Ensure Glucose is mg/dL (convert mmol/L → mg/dL if max < 35)
    if df['Glucose'].max() < 35:
        df['Glucose'] = df['Glucose'] * 18.0182

    # Ensure HbA1c is in % (convert mmol/mol → % if max > 20)
    if df['HbA1c'].max() > 20:
        df['HbA1c'] = (0.09148 * df['HbA1c']) + 2.152

    # Binary outcome from Diagnosis column
    if 'Diagnosis' in df.columns:
        df['Outcome'] = df['Diagnosis'].astype(int)
    else:
        df['Outcome'] = 0

    # Fill missing comorbidity columns
    df['Hypertension'] = 0
    df['HeartDisease'] = 0
    df['SmokingEncoded'] = 0

    # Impute zeros
    for col in ['Glucose', 'BMI', 'HbA1c']:
        if col in df.columns:
            df[col] = df[col].replace(0, np.nan)
            df[col] = df[col].fillna(df[col].median())

    return df[FEATURE_COLUMNS + [TARGET_COLUMN]]


# ---------------------------------------------------------------------------
# Synthetic data generator (fallback when real data is unavailable)
# ---------------------------------------------------------------------------

def generate_synthetic_mustafa(n: int = 100_000, seed: int = 42) -> pd.DataFrame:
    """
    Generate realistic synthetic data matching the Mustafa 100k schema.
    Distributions are calibrated to published summary statistics.
    """
    rng = np.random.default_rng(seed)

    # Gender distribution: ~58% Female, ~38% Male, ~4% Other
    sex_code = rng.choice([0, 1, 2], size=n, p=[0.58, 0.38, 0.04])

    age = rng.normal(42, 15, n).clip(1, 80).astype(int)
    bmi = rng.normal(27.3, 6.5, n).clip(10, 60).round(1)
    hypertension = rng.binomial(1, 0.075, n)
    heart_disease = rng.binomial(1, 0.04, n)
    smoking = rng.choice([0, 1, 2], size=n, p=[0.65, 0.20, 0.15])

    # HbA1c  --  bimodal: most people normal, some elevated
    hba1c_base = rng.normal(5.5, 0.6, n).clip(3.5, 6.5)
    elevated_mask = rng.random(n) < 0.15
    hba1c_base[elevated_mask] = rng.normal(7.5, 1.2, elevated_mask.sum()).clip(6.0, 9.5)
    hba1c = hba1c_base.round(1)

    # Blood glucose  --  correlated with HbA1c
    glucose = (hba1c * 20 + rng.normal(10, 15, n)).clip(60, 300).round(0)

    # Outcome  --  logistic model based on clinical risk factors
    logit = (
        -3.5
        + 0.02 * age
        + 0.04 * bmi
        + 0.8 * hypertension
        + 0.7 * heart_disease
        + 1.2 * (hba1c - 5.7)
        + 0.008 * (glucose - 100)
        + 0.2 * smoking
    )
    prob = 1.0 / (1.0 + np.exp(-logit))
    outcome = (rng.random(n) < prob).astype(int)

    df = pd.DataFrame({
        'Sex_Code': sex_code,
        'Age': age,
        'BMI': bmi,
        'Glucose': glucose,
        'HbA1c': hba1c,
        'Hypertension': hypertension,
        'HeartDisease': heart_disease,
        'SmokingEncoded': smoking,
        'Outcome': outcome,
    })

    return df


# ---------------------------------------------------------------------------
# Main loader  --  combines available datasets or falls back to synthetic
# ---------------------------------------------------------------------------

def load_training_data() -> pd.DataFrame:
    """
    Load and harmonise all available datasets.
    Falls back to synthetic data if no real datasets are found.
    """
    frames = []

    # Try Mustafa 100k
    df_m = load_mustafa()
    if not df_m.empty:
        print(f"[data_pipeline] Loaded Mustafa 100k: {len(df_m):,} rows")
        frames.append(df_m)

    # Try DTD multi-type
    df_d = load_dtd()
    if not df_d.empty:
        print(f"[data_pipeline] Loaded DTD multi-type: {len(df_d):,} rows")
        frames.append(df_d)

    if frames:
        combined = pd.concat(frames, ignore_index=True)
        combined.drop_duplicates(inplace=True)
        print(f"[data_pipeline] Combined dataset: {len(combined):,} rows")
        return combined

    # Fallback: generate synthetic data
    print("[data_pipeline] No real datasets found  --  generating synthetic data (100k rows)...")
    print("[data_pipeline] To use real data, download the Mustafa dataset from Kaggle:")
    print("[data_pipeline]   kaggle datasets download -d iammustafatz/diabetes-prediction-dataset --unzip")
    print(f"[data_pipeline]   Place CSV in: datasets/mustafa_100k/diabetes_prediction_dataset.csv")
    df_synth = generate_synthetic_mustafa()
    return df_synth


# ---------------------------------------------------------------------------
# Sylhet symptom data loader (for rules_engine validation)
# ---------------------------------------------------------------------------

def load_sylhet_symptoms(filepath: str | None = None) -> pd.DataFrame:
    """
    Load the Early-Stage Diabetes Risk Prediction Dataset (Sylhet 520).
    Used to validate/expand symptom-based rules in rules_engine.py.
    """
    if filepath is None:
        filepath = os.path.join(
            BASE_DIR, 'datasets', 'sylhet_symptoms',
            'diabetes_risk_prediction.csv',
        )
    if not os.path.isfile(filepath):
        return pd.DataFrame()

    df = pd.read_csv(filepath)
    # Standardise gender
    gender_map = {'Male': 1, 'Female': 0}
    df['Sex_Code'] = df['gender'].map(gender_map).fillna(2).astype(int)
    # Binary encode Yes/No symptom columns
    yn_cols = [c for c in df.columns if c not in ('age', 'gender', 'class', 'Sex_Code')]
    for col in yn_cols:
        df[col] = df[col].map({'Yes': 1, 'No': 0, 'Positive': 1, 'Negative': 0}).fillna(0).astype(int)
    df['Outcome'] = df['class'].map({'Positive': 1, 'Negative': 0}).fillna(0).astype(int)

    return df


# ---------------------------------------------------------------------------

if __name__ == '__main__':
    df = load_training_data()
    print(f"\nTraining data shape: {df.shape}")
    print(f"Columns: {list(df.columns)}")
    print(f"Outcome distribution:\n{df['Outcome'].value_counts()}")
    print(f"\nSex_Code distribution:\n{df['Sex_Code'].value_counts()}")
    print(f"\nSample rows:\n{df.head()}")

    df_s = load_sylhet_symptoms()
    if not df_s.empty:
        print(f"\nSylhet symptoms shape: {df_s.shape}")
        print(f"Columns: {list(df_s.columns)}")
