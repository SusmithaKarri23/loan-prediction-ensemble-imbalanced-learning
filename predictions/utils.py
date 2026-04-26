import joblib
import numpy as np
import os
from django.conf import settings

def predict_loan_eligibility(data):
    """
    Predict loan eligibility based on input data
    Returns: probability score (0-100)
    """
    model_path = os.path.join(settings.BASE_DIR, 'ml_models', 'loan_model.pkl')
    
    try:
        # Load the trained model
        model = joblib.load(model_path)
        
        # Prepare features in correct order
        features = np.array([[
            data['annual_income'],
            data['loan_amount'],
            data['credit_score'],
            data['existing_debts'],
            data['loan_duration'],
        ]])
        
        # Get prediction probability
        prediction_proba = model.predict_proba(features)[0][1]  # Probability of approval
        return round(prediction_proba * 100, 2)
    except FileNotFoundError:
        # If model not found, return a simple rule-based score
        return calculate_simple_score(data)

def calculate_simple_score(data):
    """
    Simple rule-based scoring if ML model is not available
    """
    score = 50  # Base score
    
    # Income factor
    if data['annual_income'] > 100000:
        score += 15
    elif data['annual_income'] > 50000:
        score += 10
    
    # Credit score factor
    if data['credit_score'] >= 750:
        score += 20
    elif data['credit_score'] >= 650:
        score += 10
    elif data['credit_score'] < 550:
        score -= 20
    
    # Debt-to-income ratio
    debt_ratio = data['existing_debts'] / data['annual_income'] if data['annual_income'] > 0 else 1
    if debt_ratio < 0.2:
        score += 10
    elif debt_ratio > 0.5:
        score -= 15
    
    # Loan amount vs income
    loan_ratio = data['loan_amount'] / data['annual_income'] if data['annual_income'] > 0 else 10
    if loan_ratio < 2:
        score += 10
    elif loan_ratio > 5:
        score -= 15
    
    return max(0, min(100, score))
