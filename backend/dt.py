import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_absolute_error

def train_and_evaluate_decision_tree(csv_path):
    # Load your dataset
    dataset = pd.read_csv("/Users/dcg/Desktop/bodyfat_predictor_app/data/bf_clean.csv")

    # Split into features and target
    targets = dataset['BodyFat']
    features = dataset.drop(['BodyFat'], axis=1)

    # Add more columns to include in features (if necessary)
    additional_columns = ['Weight', 'Age', 'Height']
    features = pd.concat([features, dataset[additional_columns]], axis=1)

    # Split the dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(features, targets, test_size=0.2, random_state=42)

    # Initialize the Decision Tree regressor
    decision_tree = DecisionTreeRegressor(random_state=42)

    # Fit the model
    decision_tree.fit(X_train, y_train)

    # Make predictions
    y_pred = decision_tree.predict(X_test)

    # Calculate the percentage accuracy for each prediction
    percentage_accuracies = 100 - abs((y_pred - y_test) / y_test) * 100

    # Print the average percentage accuracy
    average_percentage_accuracy = percentage_accuracies.mean()
    print("Average Percentage Accuracy:", average_percentage_accuracy)

    # Return the trained model if you want to save or use it later
    return decision_tree