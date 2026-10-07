def get_recommendations(risk_category: str, patient_data: dict) -> list[str]:
    """
    Generate lifestyle and medical recommendations based on risk category and patient data.
    
    Args:
        risk_category (str): One of 'Low', 'Moderate', 'High', 'Severe'
        patient_data (dict): Dictionary containing patient metrics
        
    Returns:
        list[str]: A list of recommendation strings
    """
    recommendations = []
    
    # Universal recommendation
    recommendations.append(
        "⚕️ DISCLAIMER: This is a screening tool for educational purposes only. "
        "It is NOT a medical diagnosis. Please consult a qualified healthcare professional for proper evaluation and advice."
    )
    
    # Risk-category-based recommendations
    category = risk_category.strip().upper()
    if category == 'LOW':
        recommendations.extend([
            "Maintain your current healthy lifestyle.",
            "Schedule an annual routine health checkup.",
            "Stay adequately hydrated.",
            "Continue eating a balanced diet."
        ])
    elif category == 'MODERATE':
        recommendations.extend([
            "Schedule a fasting blood glucose test with your doctor.",
            "Aim to increase physical activity to at least 150 minutes per week.",
            "Reduce your intake of refined sugars and processed foods.",
            "Monitor your weight and BMI on a monthly basis."
        ])
    elif category == 'HIGH':
        recommendations.extend([
            "Schedule an appointment with your doctor within the next 2 weeks.",
            "Consider starting daily blood glucose monitoring.",
            "Follow a structured low-glycemic index dietary plan.",
            "Aim for 30 minutes of daily physical exercise.",
            "Implement stress reduction techniques (e.g., meditation, yoga)."
        ])
    elif category == 'SEVERE':
        recommendations.extend([
            "Seek medical consultation immediately for proper evaluation.",
            "Daily blood glucose monitoring is mandatory.",
            "A strict dietary plan prescribed by a dietitian is needed.",
            "Medication or insulin therapy may be required based on doctor's assessment.",
            "Ensure regular medical follow-ups every 2 weeks or as directed."
        ])
        
    # Metric-specific modifiers
    glucose = patient_data.get('Glucose')
    if glucose is not None:
        if glucose > 180:
            recommendations.append("Your glucose level is significantly elevated. Seek medical attention promptly.")
        elif glucose > 140:
            recommendations.append("Your glucose level is elevated. Reduce intake of refined carbohydrates and sugary beverages.")
            
    bmi = patient_data.get('BMI')
    if bmi is not None:
        if bmi > 35:
            recommendations.append("Your BMI indicates severe obesity. Weight management is critical — consult a dietitian and physician.")
        elif bmi > 30:
            recommendations.append("Your BMI indicates obesity. Consider a structured weight management program with professional guidance.")
        elif 0 < bmi < 18.5:
            recommendations.append("Your BMI indicates underweight. Ensure adequate caloric intake and consult a nutritionist.")
            
    bp = patient_data.get('BloodPressure')
    if bp is not None:
        if bp > 100:
            recommendations.append("Your blood pressure is high. Consult a physician — antihypertensive evaluation may be needed.")
        elif bp > 90:
            recommendations.append("Your blood pressure is elevated. Reduce sodium intake, manage stress, and monitor BP regularly.")
            
    insulin = patient_data.get('Insulin')
    if insulin is not None:
        if insulin > 200:
            recommendations.append("Your insulin levels are elevated, suggesting possible insulin resistance. Discuss with your doctor.")
            
    age = patient_data.get('Age')
    if age is not None:
        if age > 60:
            recommendations.append("At your age, regular comprehensive health check-ups (every 6 months) are strongly recommended.")
        elif age > 45:
            recommendations.append("Being over 45 increases diabetes risk. Ensure annual screening and proactive lifestyle management.")
            
    dpf = patient_data.get('DiabetesPedigreeFunction')
    if dpf is not None:
        if dpf > 0.8:
            recommendations.append("Strong family history of diabetes detected. Genetic counseling may be beneficial.")
        elif dpf > 0.5:
            recommendations.append("Your family history score suggests genetic predisposition. Earlier and more frequent screening is advised.")
            
    activity_level = patient_data.get('activity_level')
    if activity_level is not None:
        if activity_level >= 8:
            recommendations.append("Great job maintaining an active lifestyle! Keep it up — regular exercise significantly reduces diabetes risk.")
        elif activity_level < 3:
            recommendations.append("Your activity level is low. Start with short daily walks and gradually increase to 150 minutes of moderate exercise per week.")
            
    return recommendations

def format_recommendations(recommendations: list[str]) -> str:
    """
    Format the list of recommendations into a readable numbered string.
    
    Args:
        recommendations (list[str]): List of recommendation strings
        
    Returns:
        str: Formatted string
    """
    if not recommendations:
        return "No recommendations available."
        
    formatted_lines = []
    for i, rec in enumerate(recommendations, 1):
        formatted_lines.append(f"{i}. {rec}")
        
    return "\n".join(formatted_lines)

if __name__ == '__main__':
    profiles = [
        {
            'name': 'Healthy young person',
            'risk_category': 'Low',
            'data': {'Glucose': 90, 'BMI': 22, 'BloodPressure': 70, 'Age': 25, 'Insulin': 80, 'DiabetesPedigreeFunction': 0.2, 'activity_level': 8}
        },
        {
            'name': 'At-risk middle-aged',
            'risk_category': 'Moderate',
            'data': {'Glucose': 155, 'BMI': 32, 'BloodPressure': 88, 'Age': 50, 'Insulin': 180, 'DiabetesPedigreeFunction': 0.6, 'activity_level': 3}
        },
        {
            'name': 'High-risk elderly',
            'risk_category': 'Severe',
            'data': {'Glucose': 195, 'BMI': 38, 'BloodPressure': 105, 'Age': 65, 'Insulin': 250, 'DiabetesPedigreeFunction': 0.9, 'activity_level': 2}
        }
    ]
    
    for profile in profiles:
        print(f"--- Profile: {profile['name']} ({profile['risk_category']} Risk) ---")
        recs = get_recommendations(profile['risk_category'], profile['data'])
        print(format_recommendations(recs))
        print("\n")
