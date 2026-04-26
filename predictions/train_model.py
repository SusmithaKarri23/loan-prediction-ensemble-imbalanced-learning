import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os

def generate_training_data(n_samples=10000):
    """Generate synthetic loan application data"""
    np.random.seed(42)
    
    data = {
        'annual_income': np.random.normal(60000, 30000, n_samples).clip(20000, 200000),
        'loan_amount': np.random.normal(50000, 30000, n_samples).clip(5000, 150000),
        'credit_score': np.random.normal(650, 100, n_samples).clip(300, 850),
        'existing_debts': np.random.normal(20000, 15000, n_samples).clip(0, 100000),
        'loan_duration': np.random.choice([12, 24, 36, 48, 60, 84, 120], n_samples),
    }
    
    df = pd.DataFrame(data)
    
    # Generate target based on rules
    df['approved'] = 0
    
    # Approval logic
    df.loc[
        (df['credit_score'] >= 650) &
        (df['existing_debts'] / df['annual_income'] < 0.4) &
        (df['loan_amount'] / df['annual_income'] < 3),
        'approved'
    ] = 1
    
    # High credit score advantage
    df.loc[df['credit_score'] >= 750, 'approved'] = 1
    
    # Low credit score rejection
    df.loc[df['credit_score'] < 550, 'approved'] = 0
    
    # High debt ratio rejection
    df.loc[df['existing_debts'] / df['annual_income'] > 0.6, 'approved'] = 0
    
    return df

def train_loan_model():
    """Train and save the loan prediction model"""
    print("Generating training data...")
    df = generate_training_data(10000)
    
    # Save dataset
    df.to_csv('loan_dataset.csv', index=False)
    print(f"Dataset saved: {len(df)} samples")
    print(f"Approval rate: {df['approved'].mean() * 100:.2f}%")
    
    # Prepare features and target
    X = df[['annual_income', 'loan_amount', 'credit_score', 'existing_debts', 'loan_duration']]
    y = df['approved']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print("\nTraining Random Forest model...")
    model = RandomForestClassifier(n_estimators=100, random_state=42, max_depth=10)
    model.fit(X_train, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    print(f"\nModel Accuracy: {accuracy * 100:.2f}%")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=['Rejected', 'Approved']))
    
    # Feature importance
    feature_importance = pd.DataFrame({
        'feature': X.columns,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)
    print("\nFeature Importance:")
    print(feature_importance)
    
    # Save model
    os.makedirs('ml_models', exist_ok=True)
    joblib.dump(model, 'ml_models/loan_model.pkl')
    print("\nModel saved to ml_models/loan_model.pkl")
    
    return model, accuracy

if __name__ == '__main__':
    train_loan_model()
