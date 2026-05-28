"""
Make predictions using trained model
"""

import pandas as pd
import pickle
from pathlib import Path

class RiskPredictor:
    """Wrapper class for making risk predictions"""
    
    def __init__(self, model_path=None):
        if model_path is None:
            model_path = Path(__file__).parent.parent.parent / "models" / "risk_model.pkl"
        
        print(f"Loading model from: {model_path}")
        with open(model_path, 'rb') as f:
            self.model = pickle.load(f)
        print("Model loaded successfully")
    
    def predict_single(self, patient_data):
        """
        Predict risk for a single patient
        
        patient_data: dict with keys matching training features
        Returns: risk_level (0=Low, 1=Medium, 2=High) and confidence
        """
        input_df = pd.DataFrame([patient_data])
        risk = self.model.predict(input_df)[0]
        proba = self.model.predict_proba(input_df)[0]
        confidence = max(proba)
        
        risk_map = {0: "Low", 1: "Medium", 2: "High"}
        
        return {
            "risk_code": int(risk),
            "risk_level": risk_map[risk],
            "confidence": round(float(confidence), 3)
        }
    
    def predict_batch(self, patients_df):
        """Predict for multiple patients"""
        predictions = self.model.predict(patients_df)
        probabilities = self.model.predict_proba(patients_df)
        
        results = []
        for i, pred in enumerate(predictions):
            results.append({
                "risk_code": int(pred),
                "confidence": float(max(probabilities[i]))
            })
        
        return results

def main():
    # Example usage
    predictor = RiskPredictor()
    
    # Example patient data
    sample_patient = {
        'Age': 65,
        'Systolic_BP': 145,
        'Diastolic_BP': 92,
        'Heart_Disease': 1,
        'Diabetes': 0,
        'Respiratory_Issue': 1,
        'Outdoor_Worker': 1,
        'Temperature_C': 38.5,
        'Humidity_%': 65,
        'Gender': 1,
        'Hydration_Level': 1,
        'Hypertension': 1,
        'Heat_Index': 38.5 + (0.12 * 65)  # 46.3
    }
    
    result = predictor.predict_single(sample_patient)
    print(f"Prediction: {result}")

if __name__ == "__main__":
    main()