import mlflow

# start the mlflow tracking server

#connecting to mlflow server
mlflow.set_tracking_uri(uri='http://localhost:5000')

mlflow.set_experiment('MLFlow Quickstart')

from mlflow.models import infer_signature
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

X, y = load_iris(return_X_y=True)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

params = {
    'solver': 'lbfgs',
    'max_iter': 1000,
    'multi_class': 'auto',
    'random_state': 8888
}

lr = LogisticRegression(**params)
lr.fit(X_train, y_train)

y_pred = lr.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)


with mlflow.start_run():
    mlflow.log_params(params=params)
    mlflow.log_metric('accuracy', accuracy)
    signature = infer_signature(X_train, lr.predict(X_train))

    model_info = mlflow.sklearn.log_model(
        sk_model=lr,
        name='iris_model',
        signature=signature,
        input_example=X_train,
        registered_model_name='tracking quickstart',
    )

    mlflow.set_logged_model_tags(
        model_info.model_id, {'training info': "Basic LR model on Iris Data"}
    )


#Loading the model
loaded_model = mlflow.pyfunc.load_model(model_info.model_uri)
predictions = loaded_model.predict(X_test)
iris_feature_names = load_iris().feature_names

result = pd.DataFrame(X_test, columns=iris_feature_names)
result['actual_class'] = y_test
result['predicted_class'] = predictions

result[:3]