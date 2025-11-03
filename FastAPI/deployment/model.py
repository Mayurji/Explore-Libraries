#pip install fastapi uvicorn "pydantic[email]" scikit-learn

from sklearn.linear_model import LogisticRegression
from sklearn.datasets import load_iris
import pickle

iris = load_iris()
X, y = iris.data, iris.target

model = LogisticRegression(max_iter=200)
model.fit(X, y)

with open('iris_model.pkl', 'wb') as file:
    pickle.dump(model, file)

print('Model is saved as iris_model.pkl')

