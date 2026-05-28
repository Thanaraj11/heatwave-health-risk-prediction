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
    print("✅ Model loaded successfully")
except Exception as e:
    print(f"❌ Failed to load model: {e}")
    predictor = None

# Request Schema
class PatientData(BaseModel):
    Age: int = Field(..., ge=0, le=120, description="Age in years")
    Systolic_BP: int = Field(..., ge=50, le=250, description="Systolic blood pressure")
    Diastolic_BP: int = Field(..., ge=30, le=150, description="Diastolic blood pressure")
    Heart_Disease: Literal[0, 1] = Field(..., description="0=No, 1=Yes")
    Diabetes: Literal[0, 1] = Field(..., description="0=No, 1=Yes")
    Respiratory_Issue: Literal[0, 1] = Field(..., description="0=No, 1=Yes")
    Outdoor_Worker: Literal[0, 1] = Field(..., description="0=No, 1=Yes")
    Temperature_C: float = Field(..., ge=20, le=50, description="Temperature in Celsius")
    Humidity_percent: float = Field(..., ge=0, le=100, description="Relative humidity %")
    Gender: Literal[0, 1] = Field(..., description="0=Female, 1=Male")
    Hydration_Level: Literal[0, 1, 2] = Field(..., description="0=Low, 1=Moderate, 2=Good")
    
    class Config:
        schema_extra = {
            "example": {
                "Age": 65,
                "Systolic_BP": 145,
                "Diastolic_BP": 92,
                "Heart_Disease": 1,
                "Diabetes": 0,
                "Respiratory_Issue": 1,
                "Outdoor_Worker": 1,
                "Temperature_C": 38.5,
                "Humidity_percent": 65,
                "Gender": 1,
                "Hydration_Level": 1
            }
        }

# Response Schema
class PredictionResponse(BaseModel):
    risk_level: Literal["Low", "Medium", "High"]
    confidence: float

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
        
        result = predictor.predict_single(input_dict)
        
        return {
            "risk_level": result["risk_level"],
            "confidence": result["confidence"]
        }
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)