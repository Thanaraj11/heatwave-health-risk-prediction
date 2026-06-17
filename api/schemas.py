"""
Pydantic schemas for request/response validation
"""

from pydantic import BaseModel, Field
from typing import Literal, Optional

class PatientData(BaseModel):
    """Input validation for prediction endpoint"""
    Age: int = Field(..., ge=0, le=120, description="Age in years")
    Systolic_BP: int = Field(..., ge=50, le=250, description="Systolic blood pressure")
    Diastolic_BP: int = Field(..., ge=30, le=150, description="Diastolic blood pressure")
    Heart_Disease: Literal[0, 1] = Field(..., description="0=No, 1=Yes")
    Diabetes: Literal[0, 1] = Field(..., description="0=No, 1=Yes")
    Respiratory_Issue: Literal[0, 1] = Field(..., description="0=No, 1=Yes")
    Outdoor_Worker: Literal[0, 1] = Field(..., description="0=No, 1=Yes")
    Temperature_C: float = Field(..., ge=20, le=50, description="Temperature in Celsius")
    Humidity_percent: float = Field(..., ge=0, le=100, description="Relative humidity %")
    Rainfall_mm: float = Field(..., ge=0, le=500, description="Rainfall in mm")
    Wind_Speed_kmh: float = Field(..., ge=0, le=200, description="Wind speed in km/h")
    Gender: Literal[0, 1] = Field(..., description="0=Female, 1=Male")
    Hydration_Level: Literal[0, 1, 2] = Field(..., description="0=Low, 1=Moderate, 2=Good")
    
    class Config:
        json_schema_extra = {
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
                "Rainfall_mm": 0.0,
                "Wind_Speed_kmh": 15.0,
                "Gender": 1,
                "Hydration_Level": 1
            }
        }

class PredictionResponse(BaseModel):
    """Output format for prediction"""
    risk_level: Literal["Low", "Medium", "High"]
    confidence: float = Field(..., ge=0, le=1, description="Model confidence score")