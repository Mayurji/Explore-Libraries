from sklearn.datasets import make_regression
from sklearn.metrics import mean_squared_error
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

import mlflow
import mlflow.sklearn
from mlflow.models import infer_signature

mlflow.set_tracking_uri('http://localhost:8080')
mlflow.set_experiment('Exp-1')

with mlflow.start_run() as run:
    x, y = make_regression(n_features=4, n_informative=2, random_state=42, shuffle=False)
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)
    params = {'max_depth': 1, 'random_state': 42}
    model = RandomForestRegressor(**params)
    model.fit(x_train, y_train)

    y_pred = model.predict(x_test)
    signature = infer_signature(x_test, y_pred)
    
    mlflow.log_params(params)
    mlflow.log_metrics({'mse': mean_squared_error(y_test, y_pred)})

    mlflow.sklearn.log_model(
        sk_model=model,
        artifact_path='sklearn-model-2',
        signature=signature,
        registered_model_name='sklearn-random-forest-reg'
    )

