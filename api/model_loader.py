"""
Model loader utility for API
"""

import pickle
import pandas as pd
from pathlib import Path

class RiskModelLoader:
    """Handle model loading and prediction"""
    
    _instance = None
    
    def __new__(cls, model_path=None):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._load_model(model_path)
        return cls._instance
    
    def _load_model(self, model_path):
        """Load pickle model file"""
        if model_path is None:
            model_path = Path(__file__).parent.parent / "models" / "risk_model.pkl"
        
        if not model_path.exists():
            raise FileNotFoundError(f"Model not found at {model_path}")
        
        with open(model_path, 'rb') as f:
            self.model = pickle.load(f)
    
    def predict(self, features_dict):
        """Make prediction from feature dictionary"""
        df = pd.DataFrame([features_dict])
        prediction = self.model.predict(df)[0]
        probabilities = self.model.predict_proba(df)[0]
        
        risk_map = {0: "Low", 1: "Medium", 2: "High"}
        
        return {
            "risk_level": risk_map[prediction],
            "confidence": float(max(probabilities))
        }