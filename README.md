# Diabetes Risk & Lifestyle Advisor

An AI-based decision-support system that predicts a person's diabetes risk from basic health metrics and provides personalized lifestyle recommendations — combining three real AI techniques into one working pipeline.

> ⚠️ **Disclaimer**: This is a screening tool for educational purposes only. It is NOT a medical diagnosis. Always consult a qualified healthcare professional.

## System Architecture

```
Patient health data (glucose, BMI, age, blood pressure, etc.)
        ↓
Neural Network   →  risk probability (0.0–1.0)
        ↓
Fuzzy Logic      →  risk category (Low / Moderate / High / Severe)
        ↓
Rule-Based Engine →  personalized recommendations
        ↓
Dashboard (Streamlit app)
```

Each stage feeds into the next — the fuzzy engine needs the NN's output, and the rule engine needs the fuzzy engine's category.

## Setup

### 1. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 2. Train the Neural Network model

```bash
python nn_model.py
```

This cleans the dataset, trains the MLPClassifier, prints evaluation metrics, and saves `model.pkl` + `scaler.pkl`.

### 3. Run the Streamlit Dashboard

```bash
streamlit run app.py
```

## Project Structure

| File | Description |
|---|---|
| `nn_model.py` | Neural network — data cleaning, training, prediction |
| `fuzzy_engine.py` | Fuzzy logic — membership functions, inference rules |
| `rules_engine.py` | Rule-based engine — personalized recommendations |
| `app.py` | Streamlit dashboard — UI integrating all three modules |
| `test_pipeline.py` | End-to-end test suite with 10 test profiles |
| `diabetes.csv` | Pima Indians Diabetes Dataset (768 records) |
| `requirements.txt` | Python dependencies |

## Dataset

**Pima Indians Diabetes Dataset** (NIDDK / UCI ML Repository)
- 768 records, 8 predictors, binary outcome
- Columns: Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age, Outcome
- Known limitation: data is entirely from adult women of Pima Native American heritage

## AI Techniques

### 1. Neural Network (scikit-learn MLPClassifier)
- 2 hidden layers (16, 8 neurons), ReLU activation, Adam optimizer
- Data cleaning: biologically impossible zeros imputed with column medians
- Preprocessing: StandardScaler normalization, 80/20 stratified split
- Output: diabetes risk probability (0.0–1.0)

### 2. Fuzzy Logic (scikit-fuzzy)
- 3 input variables: risk probability, BMI, activity level
- 1 output variable: risk category score (0–100)
- 17 fuzzy rules mapping input combinations to risk levels
- Output: risk category (Low / Moderate / High / Severe) with confidence score

### 3. Rule-Based Engine (plain Python if/elif)
- 4 risk tiers with tier-specific recommendations
- Metric-specific modifiers (glucose, BMI, blood pressure, age, family history, activity)
- ~25–30 distinct recommendations, contextually selected
- Always includes a medical disclaimer

## Running Tests

```bash
python test_pipeline.py
```

This runs:
- Individual module tests (NN, Fuzzy, Rules) with assertions
- 10 full-pipeline test profiles with a formatted results table
- Detailed output for selected profiles

## Tech Stack

- **Python** 3.8+
- **scikit-learn** — MLPClassifier neural network
- **scikit-fuzzy** — fuzzy inference engine
- **Streamlit** — interactive web dashboard
- **pandas / numpy** — data processing
- **joblib** — model persistence

## Ethical Considerations

- **Dataset Bias**: The Pima Indians dataset represents only adult women of Pima Native American heritage from a 1960s study — the model may not generalize to men, other ethnicities, or younger populations
- **Framing**: This is explicitly a screening/decision-support tool, never a diagnosis
- **Privacy**: Uses only public, anonymized data — no real patient data is collected
- **Error Costs**: False negatives (missed risk) and false positives (unnecessary alarm) carry different real-world consequences
