from metaflow import FlowSpec, step, Parameter

class GradientBoostedTreesFlow(FlowSpec):

    random_state = Parameter("seed", default=12)
    n_estimators = Parameter("n-est", default=10)
    eval_metric = Parameter("eval-metric", default='mlogloss')
    k_fold = Parameter("k", default=5)
    
    @step
    def start(self):
        from sklearn import datasets
        self.iris = datasets.load_iris()
        self.X = self.iris['data']
        self.y = self.iris['target']
        self.next(self.train_xgb)

    @step
    def train_xgb(self):
        from xgboost import XGBClassifier
        from sklearn.model_selection import cross_val_score
        self.clf = XGBClassifier(
            n_estimators=self.n_estimators,
            random_state=self.random_state,
            eval_metric=self.eval_metric,
            use_label_encoder=False)
        self.scores = cross_val_score(
            self.clf, self.X, self.y, cv=self.k_fold)
        self.next(self.end)
        
    @step
    def end(self):
        import numpy as np
        msg = "Gradient Boosted Trees Model Accuracy: {} \u00B1 {}%"
        self.mean = round(100*np.mean(self.scores), 3)
        self.std = round(100*np.std(self.scores), 3)
        print(msg.format(self.mean, self.std))

if __name__ == "__main__":
    GradientBoostedTreesFlow()