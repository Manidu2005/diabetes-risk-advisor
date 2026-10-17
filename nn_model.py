"""
Neural Network Module for the Diabetes Risk & Lifestyle Advisor.
Trains an MLPClassifier on the harmonised multi-gender dataset and
predicts diabetes risk probability for individual patients.

Feature vector (8 features):
    Sex_Code, Age, BMI, Glucose, HbA1c,
    Hypertension, HeartDisease, SmokingEncoded
"""

import os
import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score,
    f1_score, confusion_matrix,
)

from data_pipeline import load_training_data, FEATURE_COLUMNS, TARGET_COLUMN, SMOKING_MAP


def get_base_dir():
    return os.path.dirname(os.path.abspath(__file__))


def train_model():
    """
    Train the MLPClassifier on the harmonised multi-gender dataset
    and save model + scaler to disk.
    """
    df = load_training_data()

    feature_columns = list(FEATURE_COLUMNS)
    X = df[feature_columns]
    y = df[TARGET_COLUMN]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=42,
    )

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Compute sample weights to handle class imbalance
    from sklearn.utils.class_weight import compute_sample_weight
    sample_weights = compute_sample_weight('balanced', y_train)

    model = MLPClassifier(
        hidden_layer_sizes=(32, 16, 8),
        activation='relu',
        solver='adam',
        max_iter=500,
        random_state=42,
        early_stopping=True,
        validation_fraction=0.1,
    )

    # Manually balance: oversample minority class in training data
    from sklearn.utils import resample
    X_train_df = pd.DataFrame(X_train_scaled, columns=feature_columns)
    X_train_df['_y'] = y_train.values
    majority = X_train_df[X_train_df['_y'] == 0]
    minority = X_train_df[X_train_df['_y'] == 1]
    if len(minority) > 0 and len(minority) < len(majority):
        minority_upsampled = resample(
            minority, replace=True, n_samples=len(majority), random_state=42,
        )
        balanced = pd.concat([majority, minority_upsampled])
        X_train_balanced = balanced[feature_columns].values
        y_train_balanced = balanced['_y'].values
    else:
        X_train_balanced = X_train_scaled
        y_train_balanced = y_train

    model.fit(X_train_balanced, y_train_balanced)

    y_pred = model.predict(X_test_scaled)

    print("Model Evaluation:")
    print(f"  Accuracy:  {accuracy_score(y_test, y_pred):.4f}")
    print(f"  Precision: {precision_score(y_test, y_pred, zero_division=0):.4f}")
    print(f"  Recall:    {recall_score(y_test, y_pred, zero_division=0):.4f}")
    print(f"  F1 Score:  {f1_score(y_test, y_pred, zero_division=0):.4f}")
    print("  Confusion Matrix:")
    print(f"  {confusion_matrix(y_test, y_pred)}")

    base_dir = get_base_dir()
    joblib.dump(model, os.path.join(base_dir, 'model.pkl'))
    joblib.dump(scaler, os.path.join(base_dir, 'scaler.pkl'))

    return model, scaler, FEATURE_COLUMNS


def load_model():
    """
    Load the saved model and scaler from disk.
    """
    base_dir = get_base_dir()
    model = joblib.load(os.path.join(base_dir, 'model.pkl'))
    scaler = joblib.load(os.path.join(base_dir, 'scaler.pkl'))
    return model, scaler, FEATURE_COLUMNS


def _encode_patient(patient_data: dict) -> dict:
    """
    Convert a raw patient_data dict (from app.py) into the
    8-feature vector the model expects.
    """
    # --- Sex_Code ---
    sex_code = patient_data.get('Sex_Code')
    if sex_code is None:
        gender = str(patient_data.get('Gender', '')).strip().lower()
        sex_map = {'female': 0, 'male': 1, 'other': 2}
        sex_code = sex_map.get(gender, 2)

    # --- Smoking ---
    smoking_encoded = patient_data.get('SmokingEncoded')
    if smoking_encoded is None:
        sh = str(patient_data.get('SmokingHistory', 'never')).lower().strip()
        smoking_encoded = SMOKING_MAP.get(sh, 0)

    # --- Core clinical features ---
    glucose = patient_data.get('Glucose', patient_data.get('blood_glucose_level', 120.0))
    if glucose is None:
        glucose = 120.0

    hba1c = patient_data.get('HbA1c')
    if hba1c is None:
        hba1c = patient_data.get('HbA1c_level')
    if hba1c is None:
        # Clinically estimate HbA1c from blood glucose using the ADAG formula:
        # eAG (mg/dL) = 28.7 * HbA1c - 46.7  =>  HbA1c = (Glucose + 46.7) / 28.7
        est_hba1c = (float(glucose) + 46.7) / 28.7
        hba1c = float(np.clip(round(est_hba1c, 1), 4.0, 14.0))

    bmi = patient_data.get('BMI', 25.0)
    if bmi is None:
        bmi = 25.0

    age = patient_data.get('Age', 30)
    if age is None:
        age = 30

    hypertension = int(patient_data.get('Hypertension', 0) or 0)
    heart_disease = int(patient_data.get('HeartDisease', 0) or 0)

    return {
        'Sex_Code': sex_code,
        'Age': age,
        'BMI': bmi,
        'Glucose': glucose,
        'HbA1c': hba1c,
        'Hypertension': hypertension,
        'HeartDisease': heart_disease,
        'SmokingEncoded': smoking_encoded,
    }


def predict_risk(patient_data: dict) -> float:
    """
    Predict the diabetes risk probability for a single patient.

    Accepts the full patient_data dict from app.py and internally
    encodes it to the 8-feature vector the model expects.
    """
    base_dir = get_base_dir()
    model_path = os.path.join(base_dir, 'model.pkl')
    scaler_path = os.path.join(base_dir, 'scaler.pkl')

    if not (os.path.exists(model_path) and os.path.exists(scaler_path)):
        print("Model not found. Training model first...")
        train_model()

    model, scaler, feature_columns = load_model()

    encoded = _encode_patient(patient_data)
    df_patient = pd.DataFrame([encoded], columns=feature_columns)
    X_scaled = scaler.transform(df_patient)

    risk_proba = model.predict_proba(X_scaled)[0][1]
    return float(risk_proba)


if __name__ == '__main__':
    print("Training model on harmonised multi-gender dataset...")
    train_model()

    sample_patients = [
        {
            'label': 'Healthy young woman',
            'Gender': 'Female', 'Age': 25, 'BMI': 22.0,
            'Glucose': 85.0, 'HbA1c': 4.8,
            'Hypertension': 0, 'HeartDisease': 0,
            'SmokingHistory': 'never',
        },
        {
            'label': 'At-risk middle-aged man',
            'Gender': 'Male', 'Age': 50, 'BMI': 32.0,
            'Glucose': 160.0, 'HbA1c': 6.8,
            'Hypertension': 1, 'HeartDisease': 0,
            'SmokingHistory': 'current',
        },
        {
            'label': 'Non-binary young adult',
            'Gender': 'Other', 'Age': 28, 'BMI': 24.0,
            'Glucose': 95.0, 'HbA1c': 5.1,
            'Hypertension': 0, 'HeartDisease': 0,
            'SmokingHistory': 'never',
        },
    ]

    print("\nTesting predict_risk with sample patients:")
    for p in sample_patients:
        label = p.pop('label')
        risk = predict_risk(p)
        print(f"  {label}: {risk:.4f} ({risk*100:.1f}%)")
