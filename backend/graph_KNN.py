import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsRegressor

# Load your dataset
dataset = pd.read_csv("/Users/dcg/Desktop/bodyfat_predictor_app/data/bf_clean.csv")

# Split into features and target
targets = dataset['BodyFat']
features = dataset.drop(['BodyFat'], axis=1)

# Add more columns to include in features
additional_columns = ['Weight', 'Age', 'Height']
features = pd.concat([features, dataset[additional_columns]], axis=1)

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(features, targets, test_size=0.2, random_state=42)

# Initialize the KNN regressor
knn = KNeighborsRegressor(n_neighbors=5)

# Fit the model
knn.fit(X_train, y_train)

# Make predictions
y_pred = knn.predict(X_test)

# Create a bar chart
plt.figure(figsize=(10, 6))
plt.bar(range(len(y_test)), y_test, width=0.4, label='Actual', align='edge')
plt.bar(range(len(y_pred)), y_pred, width=-0.4, label='Predicted', align='edge')

# Add labels and title
plt.xlabel('Number of Test Samples')
plt.ylabel('Body Fat Percentage')
plt.title('Actual vs Predicted Body Fat Percentage')
plt.legend()
plt.show()
