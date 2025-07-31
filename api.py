from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split

app = FastAPI()

# --- Define expected input data model ---
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

# --- Columns order used for training and prediction ---
FEATURE_NAMES = ['Age', 'Weight', 'Height', 'Neck', 'Chest', 'Abdomen', 'Thigh', 'Ankle', 'Biceps', 'Forearm']

# --- Train model on startup ---
def train_and_evaluate_decision_tree(csv_path):
    dataset = pd.read_csv(csv_path)

    targets = dataset['BodyFat']
    features = dataset[FEATURE_NAMES]

    X_train, X_test, y_train, y_test = train_test_split(features, targets, test_size=0.2, random_state=42)

    model = DecisionTreeRegressor(random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    percentage_accuracies = 100 - abs((y_pred - y_test) / y_test) * 100
    print("Average Percentage Accuracy:", percentage_accuracies.mean())

    return model

model = train_and_evaluate_decision_tree("data/bf_clean.csv")

# --- Prepare input for prediction ---
def prepare_input(input_obj: BodyFatInput):
    df = pd.DataFrame([input_obj.dict()])
    df = df[FEATURE_NAMES]  # reorder columns exactly as during training
    return df

# --- Prediction endpoint ---
@app.post("/predict")
def predict_bodyfat(input_data: BodyFatInput):
    try:
        df = prepare_input(input_data)
        prediction = model.predict(df)[0]
        return {"predicted_bodyfat": round(prediction, 2)}
    except Exception as e:
        print("Error during prediction:", str(e))
        raise HTTPException(status_code=500, detail="Prediction failed.")
