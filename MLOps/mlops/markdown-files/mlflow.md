## **Setting Up MLFLow**

- Create a virtual environment
- On the terminal
  - ***sudo apt-get install python3-venv***
  - ***python3 -m venv env-name***
  - ***source env-name/bin/activate***
- To install mlflow
  - ***pip install mlflow***
  - Check if mlflow is installed
    - ***pip list***
- To run mlflow:
  - ***mlflow server --host 127.0.0.1 --port 8080***

- Create a ml model using randomforest with mlflow tracker.
  - Important parameters to set
    - mlflow.set_tracking_uri('http://localhost:8080')
    - mlflow.set_experiment('exp-1')

## MLFlow Model Serving

### using Flask

- curl https://pyenv.run | bash
- python3 -m  pip install virtualenv
- export PATH="$HOME/.pyenv/bin:$PATH"

Issue: https://github.com/mlflow/mlflow/issues/9174, which resolved running mlflow models serve.

```sudo apt-get install zlib1g-dev libssl-dev libbz2-dev libncursesw5-dev libffi-dev libreadline-dev libsqlite3-dev tk-dev liblzma-dev```

Running: ```mlflow models serve -m runs:/5a4cf70f31a94f5abe2b52e1bc167f85/sklearn-model-2 -p 5000```

Request:

```curl http://127.0.0.1:5000/invocations -H 'Content-Type:application/json' --data '{"inputs": [[1, 2, 3, 6]]}'```

### ML Server

```
import os

[experiment_file_path] = !ls -td ./mlruns/0/* | head -1
model_path = os.path.join(experiment_file_path, "artifacts", "model")
print(model_path)
```

export MLSERVER_HOST=0.0.0.0 MLSERVER_HTTP_PORT=9001

![](https://mlserver.readthedocs.io/en/latest/_images/urlv2.png)
