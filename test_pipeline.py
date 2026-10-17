"""
End-to-End Test Pipeline for the Diabetes Risk & Lifestyle Advisor.
Runs multiple test profiles through all three modules and the full pipeline,
printing a formatted results table covering diverse demographics (Male, Female, Other)
and clinical indicators (HbA1c, Hypertension, Heart Disease, Smoking History).
"""

import os
import sys

# Ensure project directory is on the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from nn_model import predict_risk, train_model
from fuzzy_engine import categorize_risk
from rules_engine import get_recommendations


def run_test_profiles():
    """Run a set of varied test profiles through the full pipeline."""

    # Ensure model is trained
    model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'model.pkl')
    if not os.path.exists(model_path):
        print("Model not found. Training first...\n")
        train_model()
        print()

    test_profiles = [
        {
            "name": "Healthy Young Woman",
            "data": {
                "Gender": "Female", "Sex_Code": 0, "Pregnancies": 0,
                "Glucose": 85.0, "BloodPressure": 66.0, "SkinThickness": 25.0,
                "Insulin": 80.0, "BMI": 21.5, "DiabetesPedigreeFunction": 0.15,
                "HbA1c": 4.8, "Age": 22, "Hypertension": 0, "HeartDisease": 0,
                "SmokingHistory": "never", "activity_level": 8
            }
        },
        {
            "name": "Healthy Young Man",
            "data": {
                "Gender": "Male", "Sex_Code": 1, "Pregnancies": 0,
                "Glucose": 90.0, "BloodPressure": 70.0, "SkinThickness": 20.0,
                "Insulin": 75.0, "BMI": 23.0, "DiabetesPedigreeFunction": 0.18,
                "HbA1c": 5.0, "Age": 25, "Hypertension": 0, "HeartDisease": 0,
                "SmokingHistory": "never", "activity_level": 9
            }
        },
        {
            "name": "Non-Binary Young Adult",
            "data": {
                "Gender": "Other", "Sex_Code": 2, "Pregnancies": 0,
                "Glucose": 95.0, "BloodPressure": 68.0, "SkinThickness": 22.0,
                "Insulin": 85.0, "BMI": 24.0, "DiabetesPedigreeFunction": 0.20,
                "HbA1c": 5.1, "Age": 28, "Hypertension": 0, "HeartDisease": 0,
                "SmokingHistory": "never", "activity_level": 7
            }
        },
        {
            "name": "Middle-Aged Woman (Moderate Risk)",
            "data": {
                "Gender": "Female", "Sex_Code": 0, "Pregnancies": 3,
                "Glucose": 130.0, "BloodPressure": 78.0, "SkinThickness": 30.0,
                "Insulin": 140.0, "BMI": 28.5, "DiabetesPedigreeFunction": 0.45,
                "HbA1c": 5.9, "Age": 42, "Hypertension": 0, "HeartDisease": 0,
                "SmokingHistory": "former", "activity_level": 5
            }
        },
        {
            "name": "Middle-Aged Man (Moderate Risk)",
            "data": {
                "Gender": "Male", "Sex_Code": 1, "Pregnancies": 0,
                "Glucose": 140.0, "BloodPressure": 82.0, "SkinThickness": 28.0,
                "Insulin": 155.0, "BMI": 30.0, "DiabetesPedigreeFunction": 0.50,
                "HbA1c": 6.0, "Age": 48, "Hypertension": 1, "HeartDisease": 0,
                "SmokingHistory": "current", "activity_level": 3
            }
        },
        {
            "name": "High-Risk Elderly Woman",
            "data": {
                "Gender": "Female", "Sex_Code": 0, "Pregnancies": 6,
                "Glucose": 190.0, "BloodPressure": 95.0, "SkinThickness": 38.0,
                "Insulin": 260.0, "BMI": 37.0, "DiabetesPedigreeFunction": 0.85,
                "HbA1c": 7.8, "Age": 62, "Hypertension": 1, "HeartDisease": 1,
                "SmokingHistory": "former", "activity_level": 2
            }
        },
        {
            "name": "High-Risk Man (Smoker)",
            "data": {
                "Gender": "Male", "Sex_Code": 1, "Pregnancies": 0,
                "Glucose": 185.0, "BloodPressure": 92.0, "SkinThickness": 32.0,
                "Insulin": 220.0, "BMI": 35.0, "DiabetesPedigreeFunction": 0.70,
                "HbA1c": 7.2, "Age": 55, "Hypertension": 1, "HeartDisease": 0,
                "SmokingHistory": "current", "activity_level": 2
            }
        },
        {
            "name": "Extreme Risk (Severe)",
            "data": {
                "Gender": "Male", "Sex_Code": 1, "Pregnancies": 0,
                "Glucose": 210.0, "BloodPressure": 110.0, "SkinThickness": 45.0,
                "Insulin": 300.0, "BMI": 42.0, "DiabetesPedigreeFunction": 1.2,
                "HbA1c": 9.5, "Age": 58, "Hypertension": 1, "HeartDisease": 1,
                "SmokingHistory": "current", "activity_level": 1
            }
        },
        {
            "name": "Prediabetic Non-Binary",
            "data": {
                "Gender": "Other", "Sex_Code": 2, "Pregnancies": 0,
                "Glucose": 115.0, "BloodPressure": 75.0, "SkinThickness": 26.0,
                "Insulin": 110.0, "BMI": 27.0, "DiabetesPedigreeFunction": 0.35,
                "HbA1c": 6.2, "Age": 35, "Hypertension": 0, "HeartDisease": 0,
                "SmokingHistory": "never", "activity_level": 6
            }
        },
        {
            "name": "Active Man, Family History",
            "data": {
                "Gender": "Male", "Sex_Code": 1, "Pregnancies": 0,
                "Glucose": 100.0, "BloodPressure": 68.0,
                "Insulin": 90.0, "BMI": 23.0, "DiabetesPedigreeFunction": 0.90,
                "HbA1c": 5.3, "Age": 30, "Hypertension": 0, "HeartDisease": 0,
                "SmokingHistory": "never", "activity_level": 9
            }
        },
        {
            "name": "Minimal Inputs (No Optionals)",
            "data": {
                "Gender": "Female", "Sex_Code": 0, "Pregnancies": 0,
                "Glucose": 125.0, "BloodPressure": None,
                "Insulin": None, "BMI": 27.5, "DiabetesPedigreeFunction": None,
                "HbA1c": None, "Age": 35, "Hypertension": 0, "HeartDisease": 0,
                "SmokingHistory": "never", "activity_level": 5
            }
        },
    ]

    # Header
    print("=" * 100)
    print("DIABETES RISK & LIFESTYLE ADVISOR  --  FULL PIPELINE TEST")
    print("=" * 100)
    print()
    print(f"{'Profile':<28} {'Gender':>7} {'NN Prob':>8} {'Fuzzy Score':>12} {'Category':>10} {'# Recs':>7}")
    print("-" * 100)

    for profile in test_profiles:
        name = profile["name"]
        data = profile["data"]
        gender = data.get("Gender", "Unknown")

        # Stage 1: Neural Network
        risk_prob = predict_risk(data)

        # Stage 2: Fuzzy Logic
        fuzzy_result = categorize_risk(risk_prob, data["BMI"], data["activity_level"], data.get("HbA1c"))

        # Stage 3: Rule-Based Engine
        recommendations = get_recommendations(fuzzy_result["category"], data)
        num_recs = len(recommendations) - 1  # Exclude disclaimer

        # Print summary row
        print(f"{name:<28} {gender:>7} {risk_prob:>8.4f} {fuzzy_result['score']:>12.2f} {fuzzy_result['category']:>10} {num_recs:>7}")

    print("-" * 100)
    print()

    # Detailed output for selected profiles
    print("=" * 100)
    print("DETAILED OUTPUT  --  Selected Profiles")
    print("=" * 100)

    for idx in [0, 5, 7]:  # Healthy Young Woman, High-Risk Elderly Woman, Extreme Risk
        profile = test_profiles[idx]
        name = profile["name"]
        data = profile["data"]

        risk_prob = predict_risk(data)
        fuzzy_result = categorize_risk(risk_prob, data["BMI"], data["activity_level"], data.get("HbA1c"))
        recommendations = get_recommendations(fuzzy_result["category"], data)

        print(f"\n--- {name} ---")
        print(f"  Input: {data}")
        print(f"  NN Risk Probability: {risk_prob:.4f} ({risk_prob*100:.1f}%)")
        print(f"  Fuzzy Category: {fuzzy_result['category']} (score: {fuzzy_result['score']:.2f})")
        print(f"  Recommendations ({len(recommendations)-1}):")
        for i, rec in enumerate(recommendations[1:], 1):
            print(f"    {i}. {rec}")
        print()


def test_individual_modules():
    """Test each module independently."""
    print("\n" + "=" * 100)
    print("INDIVIDUAL MODULE TESTS")
    print("=" * 100)

    # Test NN module
    print("\n--- Neural Network Module ---")
    test_data = {
        "Gender": "Female", "Sex_Code": 0, "Pregnancies": 3,
        "Glucose": 148.0, "BloodPressure": 72.0,
        "Insulin": 150.0, "BMI": 33.6, "DiabetesPedigreeFunction": 0.627,
        "HbA1c": 6.5, "Age": 50, "Hypertension": 1, "HeartDisease": 0,
        "SmokingHistory": "former", "activity_level": 4
    }
    prob = predict_risk(test_data)
    assert 0.0 <= prob <= 1.0, f"Risk probability out of range: {prob}"
    print(f"  [PASS] predict_risk() returned {prob:.4f} (valid range)")

    # Test Fuzzy module
    print("\n--- Fuzzy Logic Module ---")
    fuzzy_test_cases = [
        (0.1, 22.0, 8.0, 4.8),
        (0.5, 30.0, 5.0, 6.0),
        (0.9, 40.0, 1.0, 8.5),
        (0.4, 26.0, 6.0, None),  # Test without HbA1c
    ]
    for rp, b, a, h in fuzzy_test_cases:
        result = categorize_risk(rp, b, a, h)
        assert "category" in result, "Missing 'category' key"
        assert "score" in result, "Missing 'score' key"
        assert result["category"] in ["Low", "Moderate", "High", "Severe"], f"Invalid category: {result['category']}"
        h_str = f"hba1c={h}" if h is not None else "hba1c=None (optional)"
        print(f"  [PASS] categorize_risk({rp}, {b}, {a}, {h_str}) -> {result['category']} (score: {result['score']:.2f})")

    # Test Rules module
    print("\n--- Rule-Based Engine Module ---")
    for cat in ["Low", "Moderate", "High", "Severe"]:
        recs = get_recommendations(cat, test_data)
        assert isinstance(recs, list), "Recommendations should be a list"
        assert len(recs) >= 2, f"Too few recommendations for {cat}"
        assert "DISCLAIMER" in recs[0], "First recommendation should be the disclaimer"
        print(f"  [PASS] get_recommendations('{cat}', ...) -> {len(recs)} recommendations")

    print("\n[PASS] All individual module tests passed!")


if __name__ == "__main__":
    test_individual_modules()
    print()
    run_test_profiles()
