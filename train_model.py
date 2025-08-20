import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
import joblib
import os

# --- File paths ---
DATA_PATH = "data/bf_clean.csv"
MODEL_PATH = "models/decision_tree_model.pkl"

# --- Feature columns (same order as in api.py) ---
FEATURE_NAMES = ['Age', 'Weight', 'Height', 'Neck', 'Chest',
                 'Abdomen', 'Thigh', 'Ankle', 'Biceps', 'Forearm']

def train_and_save_model():
    # Load dataset
    dataset = pd.read_csv(DATA_PATH)

    # Split into features and target
    X = dataset[FEATURE_NAMES]
    y = dataset['BodyFat']

    # Split dataset
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Train model
    model = DecisionTreeRegressor(random_state=42)
    model.fit(X_train, y_train)

    # Evaluate quickly
    y_pred = model.predict(X_test)
    accuracy = 100 - abs((y_pred - y_test) / y_test) * 100
    print("Average Percentage Accuracy:", accuracy.mean())

    # Ensure models/ dir exists
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)

    # Save model
    joblib.dump(model, MODEL_PATH)
    print(f"✅ Model saved to {MODEL_PATH}")

if __name__ == "__main__":
    train_and_save_model()
