"""
Fuzzy Logic Module for the Diabetes Risk & Lifestyle Advisor.
Uses scikit-fuzzy to categorize diabetes risk based on neural network
output (risk_probability), BMI, physical activity level, and HbA1c.
"""

import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

_control_system = None
_control_system_3var = None

def _get_control_system(has_hba1c: bool = True) -> ctrl.ControlSystem:
    """
    Lazy initialization of the fuzzy logic control system (rules only).
    A fresh ControlSystemSimulation is created per call to avoid stale state.
    """
    global _control_system, _control_system_3var
    if has_hba1c:
        if _control_system is None:
            _control_system = setup_fuzzy_system(include_hba1c=True)
        return _control_system
    else:
        if _control_system_3var is None:
            _control_system_3var = setup_fuzzy_system(include_hba1c=False)
        return _control_system_3var

def setup_fuzzy_system(include_hba1c: bool = True) -> ctrl.ControlSystem:
    """
    Sets up the fuzzy logic control system with antecedents, consequents, and rules.
    Returns the ControlSystem (not a simulation).
    """
    # Define Antecedents
    risk_probability = ctrl.Antecedent(np.arange(0, 1.01, 0.01), 'risk_probability')
    bmi_var = ctrl.Antecedent(np.arange(0, 61, 1), 'bmi')
    activity_level = ctrl.Antecedent(np.arange(0, 11, 1), 'activity_level')
    if include_hba1c:
        hba1c_var = ctrl.Antecedent(np.arange(0, 15.1, 0.1), 'hba1c')
    
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
    
    # Membership functions for hba1c
    if include_hba1c:
        hba1c_var['normal'] = fuzz.trapmf(hba1c_var.universe, [0, 0, 5.0, 5.7])
        hba1c_var['prediabetic'] = fuzz.trimf(hba1c_var.universe, [5.4, 6.0, 6.5])
        hba1c_var['diabetic'] = fuzz.trapmf(hba1c_var.universe, [6.2, 7.0, 15.0, 15.0])
    
    # Membership functions for risk_category
    risk_category['low'] = fuzz.trapmf(risk_category.universe, [0, 0, 15, 30])
    risk_category['moderate'] = fuzz.trimf(risk_category.universe, [20, 40, 60])
    risk_category['high'] = fuzz.trimf(risk_category.universe, [50, 70, 85])
    risk_category['severe'] = fuzz.trapmf(risk_category.universe, [75, 90, 100, 100])
    
    # Define Fuzzy Rules  --  comprehensive coverage of all combinations
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
    
    # HbA1c modifier rules (boost risk when HbA1c is elevated regardless of other inputs)
    if include_hba1c:
        rules.extend([
            ctrl.Rule(hba1c_var['diabetic'] & bmi_var['obese'], risk_category['severe']),
            ctrl.Rule(hba1c_var['diabetic'] & bmi_var['overweight'], risk_category['severe']),
            ctrl.Rule(hba1c_var['diabetic'] & bmi_var['normal'], risk_category['high']),
            ctrl.Rule(hba1c_var['diabetic'] & bmi_var['underweight'], risk_category['high']),
            ctrl.Rule(hba1c_var['prediabetic'] & bmi_var['obese'], risk_category['high']),
            ctrl.Rule(hba1c_var['prediabetic'] & bmi_var['overweight'], risk_category['moderate']),
            ctrl.Rule(hba1c_var['prediabetic'] & bmi_var['normal'], risk_category['moderate']),
            ctrl.Rule(hba1c_var['prediabetic'] & bmi_var['underweight'], risk_category['low']),
            ctrl.Rule(hba1c_var['prediabetic'] & activity_level['sedentary'], risk_category['high']),
            ctrl.Rule(hba1c_var['diabetic'] & activity_level['sedentary'], risk_category['severe']),
        ])
    
    return ctrl.ControlSystem(rules)

def categorize_risk(risk_prob: float, bmi: float, activity_level: float, hba1c: float = None) -> dict:
    """
    Categorizes the risk based on fuzzy logic inference.
    
    Args:
        risk_prob (float): Probability output from neural network (0.0 to 1.0).
        bmi (float): Patient's BMI.
        activity_level (float): Patient's physical activity level (0 to 10).
        hba1c (float, optional): Patient's HbA1c level in % (e.g. 4.0 to 15.0).
        
    Returns:
        dict: A dictionary containing 'category', 'score', and 'membership'.
    """
    # Clamp inputs to valid ranges to avoid skfuzzy edge issues
    clamped_risk = max(0.01, min(0.99, float(risk_prob)))
    clamped_bmi = max(1.0, min(59.0, float(bmi)))
    clamped_activity = max(1.0, min(9.0, float(activity_level)))
    clamped_hba1c = max(0.1, min(14.9, float(hba1c))) if hba1c is not None else None
    
    control_system = _get_control_system(has_hba1c=(clamped_hba1c is not None))
    sim = ctrl.ControlSystemSimulation(control_system)
    
    try:
        # Feed inputs
        sim.input['risk_probability'] = clamped_risk
        sim.input['bmi'] = clamped_bmi
        sim.input['activity_level'] = clamped_activity
        if clamped_hba1c is not None:
            sim.input['hba1c'] = clamped_hba1c
        
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
        ("Low risk", 0.15, 22.0, 7.0, 5.0),
        ("Medium risk", 0.5, 30.0, 4.0, 6.0),
        ("High risk", 0.85, 38.0, 2.0, 7.5),
        ("Borderline", 0.45, 27.0, 5.0, 5.8),
        ("Prediabetic HbA1c", 0.3, 25.0, 6.0, 6.2),
    ]
    
    print("Testing Fuzzy Logic Engine...")
    print("-" * 50)
    for name, rp, b, al, hba1c in test_cases:
        res = categorize_risk(rp, b, al, hba1c)
        print(f"Case: {name}")
        print(f"  Inputs: Risk Prob={rp}, BMI={b}, Activity={al}, HbA1c={hba1c}")
        print(f"  Result: Category={res['category']}, Score={res['score']:.2f}, Membership={res['membership']:.2f}")
        print("-" * 50)
