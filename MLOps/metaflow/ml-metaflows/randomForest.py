from metaflow import FlowSpec, step, Parameter

class RandomForestFlow(FlowSpec):

    max_depth = Parameter("max_depth", default=None)
    random_state = Parameter("seed", default=11)
    n_estimators = Parameter("n-est", default=10)
    min_samples_split = Parameter("min-samples", default=2)
    k_fold = Parameter("k", default=5)

    @step
    def start(self):
        from sklearn import datasets
        self.iris = datasets.load_iris()
        self.X = self.iris['data']
        self.y = self.iris['target']
        self.next(self.train_rf)

    @step
    def train_rf(self):
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.model_selection import cross_val_score
        self.clf = RandomForestClassifier(
            n_estimators=self.n_estimators, 
            max_depth=self.max_depth,
            min_samples_split=self.min_samples_split, 
            random_state=self.random_state)
        self.scores = cross_val_score(
            self.clf, self.X, self.y, cv=self.k_fold)
        self.next(self.end)

    @step
    def end(self):
        import numpy as np
        msg = "Random Forest Accuracy: {} \u00B1 {}%"
        self.mean = round(100*np.mean(self.scores), 3)
        self.std = round(100*np.std(self.scores), 3)
        print(msg.format(self.mean, self.std))

if __name__ == "__main__":
    RandomForestFlow()