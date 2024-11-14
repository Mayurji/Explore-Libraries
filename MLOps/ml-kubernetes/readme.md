# [Develop ML Model with MLFlow and Deploy to kubernetes](https://mlflow.org/docs/latest/deployment/deploy-model-to-kubernetes/tutorial.html)


- Training a Linear Model with mlflow tracking
- Hyperparameter tuning to find the best model
- Packaging the model weights and dependenices as mlflow model
- Testing model serving locally with mlserver using mlflow model serve
- Deploy the model to kubernetes cluster using KServe with mlflow.

**KServe Installation(https://kserve.github.io/website/latest/get_started/)**

After installation, training and hyperparameter tuning is done.

Next deploying it as server, using mlserver.

Issue: pyenv.

- issue-1: https://stackoverflow.com/questions/75534090/mlflow-model-serve-cant-find-pyenv
- issue-2: https://github.com/mlflow/mlflow/issues/9174

Test locally by running the model using mlserver:

`mlflow models serve -m runs:/f00d42abb88a469fa2caea282072df93/model -p 1234 --enable-mlserver`

$ curl -X POST -H "Content-Type:application/json" --data '{"inputs": [[14.23, 1.71, 2.43, 15.6, 127.0, 2.8, 3.06, 0.28, 2.29, 5.64, 1.04, 3.92, 1065.0]]' http://127.0.0.1:1234/invocations


`#SERVICE_HOSTNAME=$(kubectl get inferenceservice wine-classifier -n mlflow-kserve-test -o jsonpath='{.status.url}' | cut -d "/" -f 3)`

`#curl -v -H "Host: ${SERVICE_HOSTNAME}" -H "Content-Type: application/json" -d @./test-input.json "http://localhost:8080/v2/models/mlflow-model/infer"`


`SERVICE_HOSTNAME=$(kubectl get inferenceservice mlflow-wine-classifier -n mlflow-kserve-test -o jsonpath='{.status.url}' | cut -d "/" -f 3)`

### Kubernetes Cluster Execution

`curl -v -H "Host: ${SERVICE_HOSTNAME}" -H "Content-Type: application/json" -d @./test-input.json "http://${INGRESS_HOST}:${INGRESS_PORT}/v2/models/mlflow-model/infer"`

### Local Execution mode:

***Modified the test-input.json as dtype and shape.***

`curl -v -H "Host: ${SERVICE_HOSTNAME}" -H "Content-Type: application/json" -d @./test-input.json "http://localhost:8080/v2/models/mlflow-model/infer"`

