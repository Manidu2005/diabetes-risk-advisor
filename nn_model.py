import os
import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

def get_base_dir():
    return os.path.dirname(os.path.abspath(__file__))

def load_and_clean_data(filepath):
    """
    Load data from CSV and replace biologically impossible zeros with medians.
    """
    df = pd.read_csv(filepath)
    
    # Columns where zero is invalid
    zero_invalid_cols = ['Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI']
    
    for col in zero_invalid_cols:
        if col in df.columns:
            df[col] = df[col].replace(0, np.nan)
            df[col] = df[col].fillna(df[col].median())
        
    return df

def train_model(filepath='diabetes.csv'):
    """
    Train the MLPClassifier model and save it to disk along with the scaler.
    """
    base_dir = get_base_dir()
    full_path = os.path.join(base_dir, filepath)
    
    df = load_and_clean_data(full_path)
    
    feature_columns = ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age']
    X = df[feature_columns]
    y = df['Outcome']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)
    
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    model = MLPClassifier(hidden_layer_sizes=(16, 8), activation='relu', solver='adam', max_iter=500, random_state=42)
    model.fit(X_train_scaled, y_train)
    
    y_pred = model.predict(X_test_scaled)
    
    print("Model Evaluation:")
    print(f"Accuracy:  {accuracy_score(y_test, y_pred):.4f}")
    print(f"Precision: {precision_score(y_test, y_pred):.4f}")
    print(f"Recall:    {recall_score(y_test, y_pred):.4f}")
    print(f"F1 Score:  {f1_score(y_test, y_pred):.4f}")
    print("Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred))
    
    joblib.dump(model, os.path.join(base_dir, 'model.pkl'))
    joblib.dump(scaler, os.path.join(base_dir, 'scaler.pkl'))
    
    return model, scaler, feature_columns

def load_model():
    """
    Load the saved model and scaler from disk.
    """
    base_dir = get_base_dir()
    model = joblib.load(os.path.join(base_dir, 'model.pkl'))
    scaler = joblib.load(os.path.join(base_dir, 'scaler.pkl'))
    feature_columns = ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age']
    
    return model, scaler, feature_columns

def predict_risk(patient_data: dict) -> float:
    """
    Predict the diabetes risk probability for a single patient.
    """
    base_dir = get_base_dir()
    model_path = os.path.join(base_dir, 'model.pkl')
    scaler_path = os.path.join(base_dir, 'scaler.pkl')
    
    if not (os.path.exists(model_path) and os.path.exists(scaler_path)):
        print("Model not found. Training model first...")
        train_model()
        
    model, scaler, feature_columns = load_model()
    
    df_patient = pd.DataFrame([patient_data], columns=feature_columns)
    X_scaled = scaler.transform(df_patient)
    
    risk_proba = model.predict_proba(X_scaled)[0][1]
    return float(risk_proba)

if __name__ == '__main__':
    print("Training model...")
    train_model()
    
    sample_patient = {
        'Pregnancies': 2,
        'Glucose': 130.0,
        'BloodPressure': 70.0,
        'SkinThickness': 30.0,
        'Insulin': 100.0,
        'BMI': 28.5,
        'DiabetesPedigreeFunction': 0.5,
        'Age': 35
    }
    
    print("\nTesting predict_risk with sample patient data:")
    risk = predict_risk(sample_patient)
    print(f"Predicted Diabetes Risk: {risk:.4f} ({risk*100:.2f}%)")
