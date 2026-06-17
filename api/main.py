"""
FastAPI backend for Heat Wave Health Risk Prediction
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Literal
import uvicorn
import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))

from src.models.predict import RiskPredictor

# Initialize FastAPI
app = FastAPI(
    title="Heat Wave Health Risk Predictor API",
    description="Predicts health risk during heat waves for Sri Lanka",
    version="1.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model
try:
    predictor = RiskPredictor()
    print("Model loaded successfully")
except Exception as e:
    print(f"Failed to load model: {e}")
    predictor = None

from api.schemas import PatientData, PredictionResponse

# Endpoints
@app.get("/")
def root():
    return {
        "message": "Heat Wave Health Risk Predictor API",
        "status": "running",
        "endpoints": ["/health", "/predict"]
    }

@app.get("/health")
def health_check():
    if predictor is None:
        return {"status": "unhealthy", "error": "Model not loaded"}
    return {"status": "healthy"}

@app.post("/predict", response_model=PredictionResponse)
def predict(patient: PatientData):
    if predictor is None:
        raise HTTPException(status_code=503, detail="Model not available")
    
    try:
        # Convert to dict and calculate required features
        input_dict = patient.dict()
        
        # Calculate Heat_Index and Hypertension
        input_dict['Humidity_%'] = input_dict.pop('Humidity_percent')
        input_dict['Heat_Index'] = input_dict['Temperature_C'] + (0.12 * input_dict['Humidity_%'])
        input_dict['Hypertension'] = 1 if (input_dict['Systolic_BP'] >= 140 or input_dict['Diastolic_BP'] >= 90) else 0
        
        # Ensure correct column order
        feature_order = ['Age', 'Gender', 'Heart_Disease', 'Diabetes', 'Respiratory_Issue', 
                         'Outdoor_Worker', 'Systolic_BP', 'Diastolic_BP', 'Hydration_Level', 
                         'Temperature_C', 'Humidity_%', 'Rainfall_mm', 'Wind_Speed_kmh', 
                         'Hypertension', 'Heat_Index']
        input_dict = {k: input_dict[k] for k in feature_order}
        
        result = predictor.predict_single(input_dict)
        
        return {
            "risk_level": result["risk_level"],
            "confidence": result["confidence"]
        }
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)