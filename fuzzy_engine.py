"""
Fuzzy Logic Module for the Diabetes Risk & Lifestyle Advisor.
Uses scikit-fuzzy to categorize diabetes risk based on neural network
output (risk_probability), BMI, and physical activity level.
"""

import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

_control_system = None

def _get_control_system() -> ctrl.ControlSystem:
    """
    Lazy initialization of the fuzzy logic control system (rules only).
    A fresh ControlSystemSimulation is created per call to avoid stale state.
    """
    global _control_system
    if _control_system is None:
        _control_system = setup_fuzzy_system()
    return _control_system

def setup_fuzzy_system() -> ctrl.ControlSystem:
    """
    Sets up the fuzzy logic control system with antecedents, consequents, and rules.
    Returns the ControlSystem (not a simulation).
    """
    # Define Antecedents
    risk_probability = ctrl.Antecedent(np.arange(0, 1.01, 0.01), 'risk_probability')
    bmi_var = ctrl.Antecedent(np.arange(0, 61, 1), 'bmi')
    activity_level = ctrl.Antecedent(np.arange(0, 11, 1), 'activity_level')
    
    # Define Consequent
    risk_category = ctrl.Consequent(np.arange(0, 101, 1), 'risk_category')
    
    # Membership functions for risk_probability
    risk_probability['low'] = fuzz.trapmf(risk_probability.universe, [0, 0, 0.2, 0.35])
    risk_probability['medium'] = fuzz.trimf(risk_probability.universe, [0.2, 0.45, 0.7])
    risk_probability['high'] = fuzz.trapmf(risk_probability.universe, [0.55, 0.75, 1.0, 1.0])
    
    # Membership functions for bmi
    bmi_var['underweight'] = fuzz.trapmf(bmi_var.universe, [0, 0, 16, 18.5])
    bmi_var['normal'] = fuzz.trimf(bmi_var.universe, [16, 22, 27])
    bmi_var['overweight'] = fuzz.trimf(bmi_var.universe, [25, 30, 35])
    bmi_var['obese'] = fuzz.trapmf(bmi_var.universe, [33, 38, 60, 60])
    
    # Membership functions for activity_level
    activity_level['sedentary'] = fuzz.trapmf(activity_level.universe, [0, 0, 2, 4])
    activity_level['moderate'] = fuzz.trimf(activity_level.universe, [3, 5, 7])
    activity_level['active'] = fuzz.trapmf(activity_level.universe, [6, 8, 10, 10])
    
    # Membership functions for risk_category
    risk_category['low'] = fuzz.trapmf(risk_category.universe, [0, 0, 15, 30])
    risk_category['moderate'] = fuzz.trimf(risk_category.universe, [20, 40, 60])
    risk_category['high'] = fuzz.trimf(risk_category.universe, [50, 70, 85])
    risk_category['severe'] = fuzz.trapmf(risk_category.universe, [75, 90, 100, 100])
    
    # Define Fuzzy Rules — comprehensive coverage of all combinations
    rules = [
        # High risk probability rules
        ctrl.Rule(risk_probability['high'] & bmi_var['obese'] & activity_level['sedentary'], risk_category['severe']),
        ctrl.Rule(risk_probability['high'] & bmi_var['obese'] & activity_level['moderate'], risk_category['severe']),
        ctrl.Rule(risk_probability['high'] & bmi_var['obese'] & activity_level['active'], risk_category['high']),
        ctrl.Rule(risk_probability['high'] & bmi_var['overweight'] & activity_level['sedentary'], risk_category['severe']),
        ctrl.Rule(risk_probability['high'] & bmi_var['overweight'] & activity_level['moderate'], risk_category['high']),
        ctrl.Rule(risk_probability['high'] & bmi_var['overweight'] & activity_level['active'], risk_category['high']),
        ctrl.Rule(risk_probability['high'] & bmi_var['normal'] & activity_level['sedentary'], risk_category['high']),
        ctrl.Rule(risk_probability['high'] & bmi_var['normal'] & activity_level['moderate'], risk_category['high']),
        ctrl.Rule(risk_probability['high'] & bmi_var['normal'] & activity_level['active'], risk_category['moderate']),
        ctrl.Rule(risk_probability['high'] & bmi_var['underweight'] & activity_level['sedentary'], risk_category['high']),
        ctrl.Rule(risk_probability['high'] & bmi_var['underweight'] & activity_level['moderate'], risk_category['moderate']),
        ctrl.Rule(risk_probability['high'] & bmi_var['underweight'] & activity_level['active'], risk_category['moderate']),
        
        # Medium risk probability rules
        ctrl.Rule(risk_probability['medium'] & bmi_var['obese'] & activity_level['sedentary'], risk_category['high']),
        ctrl.Rule(risk_probability['medium'] & bmi_var['obese'] & activity_level['moderate'], risk_category['high']),
        ctrl.Rule(risk_probability['medium'] & bmi_var['obese'] & activity_level['active'], risk_category['moderate']),
        ctrl.Rule(risk_probability['medium'] & bmi_var['overweight'] & activity_level['sedentary'], risk_category['high']),
        ctrl.Rule(risk_probability['medium'] & bmi_var['overweight'] & activity_level['moderate'], risk_category['moderate']),
        ctrl.Rule(risk_probability['medium'] & bmi_var['overweight'] & activity_level['active'], risk_category['moderate']),
        ctrl.Rule(risk_probability['medium'] & bmi_var['normal'] & activity_level['sedentary'], risk_category['moderate']),
        ctrl.Rule(risk_probability['medium'] & bmi_var['normal'] & activity_level['moderate'], risk_category['moderate']),
        ctrl.Rule(risk_probability['medium'] & bmi_var['normal'] & activity_level['active'], risk_category['low']),
        ctrl.Rule(risk_probability['medium'] & bmi_var['underweight'] & activity_level['sedentary'], risk_category['moderate']),
        ctrl.Rule(risk_probability['medium'] & bmi_var['underweight'] & activity_level['moderate'], risk_category['low']),
        ctrl.Rule(risk_probability['medium'] & bmi_var['underweight'] & activity_level['active'], risk_category['low']),
        
        # Low risk probability rules
        ctrl.Rule(risk_probability['low'] & bmi_var['obese'] & activity_level['sedentary'], risk_category['moderate']),
        ctrl.Rule(risk_probability['low'] & bmi_var['obese'] & activity_level['moderate'], risk_category['moderate']),
        ctrl.Rule(risk_probability['low'] & bmi_var['obese'] & activity_level['active'], risk_category['low']),
        ctrl.Rule(risk_probability['low'] & bmi_var['overweight'] & activity_level['sedentary'], risk_category['moderate']),
        ctrl.Rule(risk_probability['low'] & bmi_var['overweight'] & activity_level['moderate'], risk_category['low']),
        ctrl.Rule(risk_probability['low'] & bmi_var['overweight'] & activity_level['active'], risk_category['low']),
        ctrl.Rule(risk_probability['low'] & bmi_var['normal'] & activity_level['sedentary'], risk_category['low']),
        ctrl.Rule(risk_probability['low'] & bmi_var['normal'] & activity_level['moderate'], risk_category['low']),
        ctrl.Rule(risk_probability['low'] & bmi_var['normal'] & activity_level['active'], risk_category['low']),
        ctrl.Rule(risk_probability['low'] & bmi_var['underweight'] & activity_level['sedentary'], risk_category['low']),
        ctrl.Rule(risk_probability['low'] & bmi_var['underweight'] & activity_level['moderate'], risk_category['low']),
        ctrl.Rule(risk_probability['low'] & bmi_var['underweight'] & activity_level['active'], risk_category['low']),
    ]
    
    return ctrl.ControlSystem(rules)

def categorize_risk(risk_prob: float, bmi: float, activity_level: float) -> dict:
    """
    Categorizes the risk based on fuzzy logic inference.
    
    Args:
        risk_prob (float): Probability output from neural network (0.0 to 1.0).
        bmi (float): Patient's BMI.
        activity_level (float): Patient's physical activity level (0 to 10).
        
    Returns:
        dict: A dictionary containing 'category', 'score', and 'membership'.
    """
    # Clamp inputs to valid ranges to avoid skfuzzy edge issues
    clamped_risk = max(0.01, min(0.99, float(risk_prob)))
    clamped_bmi = max(1.0, min(59.0, float(bmi)))
    clamped_activity = max(1.0, min(9.0, float(activity_level)))
    
    control_system = _get_control_system()
    sim = ctrl.ControlSystemSimulation(control_system)
    
    try:
        # Feed inputs
        sim.input['risk_probability'] = clamped_risk
        sim.input['bmi'] = clamped_bmi
        sim.input['activity_level'] = clamped_activity
        
        # Compute fuzzy inference
        sim.compute()
        
        # Get defuzzified output score
        score = sim.output['risk_category']
        
        # Map to category string
        if score <= 25:
            category = 'Low'
        elif score <= 50:
            category = 'Moderate'
        elif score <= 75:
            category = 'High'
        else:
            category = 'Severe'
            
        # Normalize membership (0-1) based on score (0-100)
        membership = score / 100.0
        
        return {
            'category': category,
            'score': float(score),
            'membership': float(membership)
        }
        
    except (ValueError, KeyError):
        # Fallback in case no rules fire
        score = clamped_risk * 100.0
        if score <= 25:
            category = 'Low'
        elif score <= 50:
            category = 'Moderate'
        elif score <= 75:
            category = 'High'
        else:
            category = 'Severe'
            
        return {
            'category': category,
            'score': float(score),
            'membership': float(clamped_risk)
        }

if __name__ == '__main__':
    # Test cases
    test_cases = [
        ("Low risk", 0.15, 22.0, 7.0),
        ("Medium risk", 0.5, 30.0, 4.0),
        ("High risk", 0.85, 38.0, 2.0),
        ("Borderline", 0.45, 27.0, 5.0)
    ]
    
    print("Testing Fuzzy Logic Engine...")
    print("-" * 50)
    for name, rp, b, al in test_cases:
        res = categorize_risk(rp, b, al)
        print(f"Case: {name}")
        print(f"  Inputs: Risk Prob={rp}, BMI={b}, Activity={al}")
        print(f"  Result: Category={res['category']}, Score={res['score']:.2f}, Membership={res['membership']:.2f}")
        print("-" * 50)
