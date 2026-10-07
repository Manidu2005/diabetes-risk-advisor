"""
End-to-End Test Pipeline for the Diabetes Risk & Lifestyle Advisor.
Runs multiple test profiles through all three modules and the full pipeline,
printing a formatted results table.
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
                "Pregnancies": 0, "Glucose": 85.0, "BloodPressure": 66.0,
                "SkinThickness": 25.0, "Insulin": 80.0, "BMI": 21.5,
                "DiabetesPedigreeFunction": 0.15, "Age": 22,
                "activity_level": 8
            }
        },
        {
            "name": "Average Middle-Aged",
            "data": {
                "Pregnancies": 3, "Glucose": 110.0, "BloodPressure": 74.0,
                "SkinThickness": 30.0, "Insulin": 120.0, "BMI": 26.0,
                "DiabetesPedigreeFunction": 0.35, "Age": 40,
                "activity_level": 5
            }
        },
        {
            "name": "Overweight Sedentary",
            "data": {
                "Pregnancies": 5, "Glucose": 145.0, "BloodPressure": 82.0,
                "SkinThickness": 35.0, "Insulin": 175.0, "BMI": 33.0,
                "DiabetesPedigreeFunction": 0.55, "Age": 48,
                "activity_level": 2
            }
        },
        {
            "name": "High-Risk Elderly",
            "data": {
                "Pregnancies": 8, "Glucose": 190.0, "BloodPressure": 95.0,
                "SkinThickness": 40.0, "Insulin": 260.0, "BMI": 39.0,
                "DiabetesPedigreeFunction": 0.85, "Age": 62,
                "activity_level": 2
            }
        },
        {
            "name": "Borderline Case A",
            "data": {
                "Pregnancies": 2, "Glucose": 130.0, "BloodPressure": 78.0,
                "SkinThickness": 28.0, "Insulin": 140.0, "BMI": 27.5,
                "DiabetesPedigreeFunction": 0.45, "Age": 35,
                "activity_level": 5
            }
        },
        {
            "name": "Borderline Case B",
            "data": {
                "Pregnancies": 4, "Glucose": 140.0, "BloodPressure": 85.0,
                "SkinThickness": 32.0, "Insulin": 160.0, "BMI": 30.5,
                "DiabetesPedigreeFunction": 0.50, "Age": 44,
                "activity_level": 4
            }
        },
        {
            "name": "Very Active, Family History",
            "data": {
                "Pregnancies": 1, "Glucose": 100.0, "BloodPressure": 68.0,
                "SkinThickness": 22.0, "Insulin": 90.0, "BMI": 23.0,
                "DiabetesPedigreeFunction": 0.90, "Age": 30,
                "activity_level": 9
            }
        },
        {
            "name": "Extreme High Risk",
            "data": {
                "Pregnancies": 10, "Glucose": 200.0, "BloodPressure": 110.0,
                "SkinThickness": 45.0, "Insulin": 300.0, "BMI": 42.0,
                "DiabetesPedigreeFunction": 1.2, "Age": 55,
                "activity_level": 1
            }
        },
        {
            "name": "Young Underweight",
            "data": {
                "Pregnancies": 0, "Glucose": 75.0, "BloodPressure": 60.0,
                "SkinThickness": 15.0, "Insulin": 50.0, "BMI": 17.0,
                "DiabetesPedigreeFunction": 0.10, "Age": 20,
                "activity_level": 7
            }
        },
        {
            "name": "High BP, Normal Glucose",
            "data": {
                "Pregnancies": 6, "Glucose": 100.0, "BloodPressure": 105.0,
                "SkinThickness": 33.0, "Insulin": 130.0, "BMI": 29.0,
                "DiabetesPedigreeFunction": 0.40, "Age": 52,
                "activity_level": 4
            }
        },
    ]

    # Header
    print("=" * 100)
    print("DIABETES RISK & LIFESTYLE ADVISOR — FULL PIPELINE TEST")
    print("=" * 100)
    print()
    print(f"{'Profile':<28} {'NN Prob':>8} {'Fuzzy Score':>12} {'Category':>10} {'# Recs':>7}")
    print("-" * 100)

    for profile in test_profiles:
        name = profile["name"]
        data = profile["data"]

        # Strip activity_level for NN (it doesn't use it)
        nn_data = {k: v for k, v in data.items() if k != "activity_level"}

        # Stage 1: Neural Network
        risk_prob = predict_risk(nn_data)

        # Stage 2: Fuzzy Logic
        fuzzy_result = categorize_risk(risk_prob, data["BMI"], data["activity_level"])

        # Stage 3: Rule-Based Engine
        recommendations = get_recommendations(fuzzy_result["category"], data)
        num_recs = len(recommendations) - 1  # Exclude disclaimer

        # Print summary row
        print(f"{name:<28} {risk_prob:>7.4f} {fuzzy_result['score']:>11.2f} {fuzzy_result['category']:>10} {num_recs:>7}")

    print("-" * 100)
    print()

    # Detailed output for two key profiles
    print("=" * 100)
    print("DETAILED OUTPUT — Selected Profiles")
    print("=" * 100)

    for idx in [0, 3, 7]:  # Healthy, High-Risk Elderly, Extreme
        profile = test_profiles[idx]
        name = profile["name"]
        data = profile["data"]
        nn_data = {k: v for k, v in data.items() if k != "activity_level"}

        risk_prob = predict_risk(nn_data)
        fuzzy_result = categorize_risk(risk_prob, data["BMI"], data["activity_level"])
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
        "Pregnancies": 3, "Glucose": 148.0, "BloodPressure": 72.0,
        "SkinThickness": 35.0, "Insulin": 150.0, "BMI": 33.6,
        "DiabetesPedigreeFunction": 0.627, "Age": 50
    }
    prob = predict_risk(test_data)
    assert 0.0 <= prob <= 1.0, f"Risk probability out of range: {prob}"
    print(f"  [PASS] predict_risk() returned {prob:.4f} (valid range)")

    # Test Fuzzy module
    print("\n--- Fuzzy Logic Module ---")
    for rp, b, a in [(0.1, 22.0, 8.0), (0.5, 30.0, 5.0), (0.9, 40.0, 1.0)]:
        result = categorize_risk(rp, b, a)
        assert "category" in result, "Missing 'category' key"
        assert "score" in result, "Missing 'score' key"
        assert result["category"] in ["Low", "Moderate", "High", "Severe"], f"Invalid category: {result['category']}"
        print(f"  [PASS] categorize_risk({rp}, {b}, {a}) -> {result['category']} (score: {result['score']:.2f})")

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
