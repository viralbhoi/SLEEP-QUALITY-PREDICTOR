from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import joblib
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Sleep Quality Prediction API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # allow all for dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model = joblib.load("../model/pipeline.pkl")

class UserInput(BaseModel):
    Age: int
    Gender: str
    Occupation: str
    Sleep_Duration: float
    Physical_Activity_Level: int
    Stress_Level: int
    BMI_Category: str
    Heart_Rate: int
    Daily_Steps: int
    BP_sys: int
    BP_dia: int

@app.get("/")
def root():
    return {"message": "Sleep Quality Prediction API Running"}

@app.post("/predict")

def predict(data: UserInput):
    df = pd.DataFrame([data.dict()])
    prediction = model.predict(df)[0]
    
    score = round(float(prediction), 2)
    if score >= 8:
        status = "Excellent Sleep"
    elif score >= 6:
        status = "Moderate Sleep"
    else:
        status = "Poor Sleep"

    return {
        "predicted_sleep_quality": score,
        "sleep_status": status
    }
