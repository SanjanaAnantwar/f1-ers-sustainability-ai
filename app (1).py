from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np
import os

app = FastAPI(title="F1 ERS Green AI API")

# Load model
model = joblib.load(os.path.join("model", "efficiency_model.pkl"))

class EngineInput(BaseModel):
    engine_type: str  # "V8" or "Hybrid"

@app.get("/")
def home():
    return {"message": "F1 ERS Green AI API running 🚀"}

@app.post("/predict")
def predict(data: EngineInput):
    if data.engine_type == "V8":
        fuel = np.random.uniform(140, 160)
        ers = 0
    else:
        fuel = np.random.uniform(85, 105)
        ers = np.random.uniform(1.5, 4.0)

    efficiency = model.predict([[fuel, ers]])[0]

    return {
        "engine": data.engine_type,
        "fuel_used_kg": round(fuel, 2),
        "ers_energy_mj": round(ers, 2),
        "efficiency_score": round(efficiency, 4)
    }
