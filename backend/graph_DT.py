import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor

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

# Fit the KNN model
knn.fit(X_train, y_train)

# Make KNN predictions
y_pred_knn = knn.predict(X_test)

# Initialize the Decision Tree regressor
decision_tree = DecisionTreeRegressor(random_state=42)

# Fit the Decision Tree model
decision_tree.fit(X_train, y_train)

# Make Decision Tree predictions
y_pred_decision_tree = decision_tree.predict(X_test)

# Create a bar chart
plt.figure(figsize=(12, 6))
bar_width = 0.25

# Plot Actual
plt.bar(range(len(y_test)), y_test, width=bar_width, label='Actual', align='edge', alpha=0.7)

# Plot Predicted for KNN
plt.bar(range(len(y_test), len(y_test) * 2), y_pred_knn, width=-bar_width, label='KNN Predicted', align='edge', alpha=0.7)

# Plot Predicted for Decision Tree
plt.bar(range(len(y_test) * 2, len(y_test) * 3), y_pred_decision_tree, width=-bar_width,
        label='Decision Tree Predicted', align='edge', alpha=0.7)

# Add labels and title
plt.xlabel('Number of Test Entries')
plt.ylabel('Body Fat Percentage')
plt.title('Actual vs Predicted Body Fat Percentage (KNN and Decision Tree)')
plt.legend()
plt.show()
