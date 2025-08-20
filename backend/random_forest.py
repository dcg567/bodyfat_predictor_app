import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

FEATURE_NAMES = ['Age', 'Weight', 'Height', 'Neck', 'Chest', 'Abdomen', 'Thigh', 'Ankle', 'Biceps', 'Forearm']

def train_random_forest(csv_path):
    dataset = pd.read_csv(csv_path)
    targets = dataset['BodyFat']
    features = dataset[FEATURE_NAMES]

    X_train, X_test, y_train, y_test = train_test_split(features, targets, test_size=0.2, random_state=42)

    model = RandomForestRegressor(random_state=42, n_estimators=100)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    percentage_accuracies = 100 - abs((y_pred - y_test) / y_test) * 100
    print("Random Forest Average Percentage Accuracy:", percentage_accuracies.mean())
    
    return model

def prepare_input(input_dict):
    df = pd.DataFrame([input_dict], columns=FEATURE_NAMES)
    return df

def predict_bodyfat(input_dict, model):
    df = prepare_input(input_dict)
    prediction = model.predict(df)[0]
    return prediction


if __name__ == "__main__":
    csv_path = "data/bf_clean.csv"  # update with your actual path
    model = train_random_forest(csv_path)

    sample_input = {
        'Age': 25,
        'Weight': 180,
        'Height': 70,
        'Neck': 15,
        'Chest': 40,
        'Abdomen': 35,
        'Thigh': 22,
        'Ankle': 9,
        'Biceps': 13,
        'Forearm': 11
    }

    prediction = predict_bodyfat(sample_input, model)
    print("Predicted Body Fat (Random Forest):", prediction)
