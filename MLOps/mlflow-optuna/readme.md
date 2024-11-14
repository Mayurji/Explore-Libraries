## MLFlow with Optuna

- To have production grade model, we need to tune the model to best of its parameters to acheive the best performance.
- But the number of parameters to tune are quite huge to tune it manually. Hence tools like Optuna come into picture.

### Why Optuna?

- Open Source Hyperparameter optimization framework.
- Efficient techniques for searching parameters.

### MLFlow child runs:

- MLFlow provides child runs concepts, 
    - where each iteration of hyperparameter tuning is recorded as one run, and all runs are placed under a parent.

## Scope of this Video:

- Data Preparation: We’ll start by loading and preprocessing our dataset.

- Model Definition: Defining a machine learning model that we aim to optimize.

- Optuna Study: Setting up an Optuna study to find the best hyperparameters for our model.

- MLflow Integration: Tracking each Optuna trial as a child run in MLflow.

- Analysis: Reviewing the tracked results in the MLflow UI.

### Installation

`pip install optuna`
