import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from dotenv import load_dotenv
import os
from feature import engineer_features
from sqlalchemy import create_engine
from xgboost import XGBClassifier
from sklearn.metrics import classification_report, confusion_matrix , accuracy_score ,precision_score, recall_score, f1_score
import mlflow

load_dotenv()

mlflow.set_experiment("Transaction-Anomaly-Detection")

# Connect to the database
DB_URL= f'postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}'
engine = create_engine(DB_URL)

# Load data from the database
df = pd.read_sql('SELECT * FROM Transactions',engine)

# Feature Engineering imported from feature.py
df = engineer_features(df)

# Create Target : Is_anomaly
df['is_anomaly'] = (df['deviation'].abs()>2).astype(int)

# Create features and target variable
X = df[['deviation', 'user_avg_amount', 'user_std_amount', 'user_txn_count', 'hour_of_day', 'day_of_week']]

y = df['is_anomaly']

# Split the data into training and testing sets
X_train , X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42,stratify=y)

# set scale_pos_weight to handle class imbalance
scale_pos_weight = y_train.value_counts()[0] / y_train.value_counts()[1]
print(y_train.value_counts())

with mlflow.start_run():
    mlflow.log_param("scale_pos_weight", scale_pos_weight)
    mlflow.log_param("test_size", 0.2)
    mlflow.log_param("random_state", 42)
    
    # Train the model
    model = XGBClassifier(scale_pos_weight=scale_pos_weight, random_state=42)
    model.fit(X_train, y_train)

    # Predict on the test set
    y_pred =model.predict(X_test)

    # Evaluate the model
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test , y_pred)
    recall = recall_score(y_test, y_pred)
    confusion = confusion_matrix(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    classification_rep = classification_report(y_test, y_pred)
    
    print('confusion matrix:\n', confusion)
    print('Classification Report:\n', classification_rep)
    
    mlflow.log_metrics({
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1_score": f1,
    })
    
    mlflow.xgboost.log_model(model,name = "xgboost_model")
    print(f"Run ID: {mlflow.active_run().info.run_id}")
