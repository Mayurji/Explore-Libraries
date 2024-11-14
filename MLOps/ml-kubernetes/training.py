import mlflow

import numpy as np
from sklearn import datasets, metrics
from sklearn.linear_model import ElasticNet
from sklearn.model_selection import train_test_split


def eval_metrics(pred, actual):
    rmse = np.sqrt(metrics.mean_squared_error(actual, pred))
    mae = metrics.mean_absolute_error(actual, pred)
    r2 = metrics.r2_score(actual, pred)
    return rmse, mae, r2


# Set th experiment 
mlflow.set_tracking_uri('http://localhost:5000')
mlflow.set_experiment("Wine-Quality-II")

# Enable auto-logging to MLflow
mlflow.sklearn.autolog()

# Load wine quality dataset
X, y = datasets.load_wine(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25)

# Start a run and train a model
with mlflow.start_run(run_name="default-params"):
    lr = ElasticNet()
    lr.fit(X_train, y_train)

    y_pred = lr.predict(X_test)
    metrics = eval_metrics(y_pred, y_test)
