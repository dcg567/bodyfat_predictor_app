import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsRegressor
import joblib
import os

# Path to save the trained model
MODEL_PATH = "/Users/dcg/Desktop/bodyfat_predictor_app/models/knn_model.pkl"
os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)

def train_and_evaluate_knn():
    # Load dataset
    dataset = pd.read_csv("/Users/dcg/Desktop/bodyfat_predictor_app/data/bf_clean.csv")

    # Split into features and target
    targets = dataset['BodyFat']
    features = dataset.drop(['BodyFat'], axis=1)

    # Add more columns to include in features
    additional_columns = ['Weight', 'Age', 'Height']
    features = pd.concat([features, dataset[additional_columns]], axis=1)

    # Split the dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(features, targets, test_size=0.2, random_state=42)

    # Initialize and train the KNN model
    knn = KNeighborsRegressor(n_neighbors=5)
    knn.fit(X_train, y_train)

    # Make predictions and calculate accuracy
    y_pred = knn.predict(X_test)
    percentage_accuracies = 100 - abs((y_pred - y_test) / y_test) * 100
    average_percentage_accuracy = percentage_accuracies.mean()
    print("Average Percentage Accuracy:", average_percentage_accuracy)

    # Save the trained model
    joblib.dump(knn, MODEL_PATH)
    print(f"KNN model saved at {MODEL_PATH}")

    # Return the trained model
    return knn

def load_knn():
    """Load the persisted KNN model if it exists."""
    try:
        return joblib.load(MODEL_PATH)
    except FileNotFoundError:
        print("KNN model not found. Please train it first.")
        return None

# Example usage
if __name__ == "__main__":
    train_and_evaluate_knn()
