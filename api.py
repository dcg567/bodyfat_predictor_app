from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import joblib
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Input schema
class BodyFatInput(BaseModel):
    Age: float
    Weight: float
    Height: float
    Neck: float
    Chest: float
    Abdomen: float
    Thigh: float
    Ankle: float
    Biceps: float
    Forearm: float

# Feature order used during training
FEATURE_NAMES = ['Age', 'Weight', 'Height', 'Neck', 'Chest',
                 'Abdomen', 'Thigh', 'Ankle', 'Biceps', 'Forearm']

#Load trained model at startup
MODEL_PATH = "models/decision_tree_model.pkl"

if not os.path.exists(MODEL_PATH):
    raise RuntimeError(f"❌ Model not found at {MODEL_PATH}. Run train_model.py first.")

model = joblib.load(MODEL_PATH)
print("✅ Model loaded from", MODEL_PATH)

# Prepare input for prediction
def prepare_input(input_obj: BodyFatInput):
    df = pd.DataFrame([input_obj.dict()])
    return df[FEATURE_NAMES]

@app.get("/health")
def health_check():
    return {"status": "ok", "model_loaded": True}


# Prediction endpoint
@app.post("/predict")
def predict_bodyfat(input_data: BodyFatInput):
    try:
        df = prepare_input(input_data)
        prediction = model.predict(df)[0]
        return {"predicted_bodyfat": round(prediction, 2)}
    except Exception as e:
        print("Error during prediction:", str(e))
        raise HTTPException(status_code=500, detail="Prediction failed.")
