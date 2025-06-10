from metaflow import FlowSpec, step, Parameter

class KFoldFlow(FlowSpec):
    
    k = Parameter('k', default=5)

    @step
    def start(self):
        from sklearn.datasets import load_wine
        data = load_wine()
        self.x = data['data']
        self.y = data['target']
        self.next(self.make_splits)
        
    @step
    def make_splits(self):
        from sklearn.model_selection import KFold
        kfold = KFold(n_splits=self.k)
        self.split = []
        for train_id, valid_id in kfold.split(self.x):
            self.split.append((train_id, valid_id))
        self.next(self.fit_and_score_model, 
                  foreach="split") 

    @step
    def fit_and_score_model(self):
        from sklearn.tree import ExtraTreeClassifier
        from sklearn.metrics import accuracy_score
        self.model = ExtraTreeClassifier()
        train_x = self.x[self.input[0]]
        valid_x = self.x[self.input[1]]
        train_y = self.y[self.input[0]]
        valid_y = self.y[self.input[1]]
        self.model.fit(train_x, train_y)
        self.score = accuracy_score(
            valid_y, 
            self.model.predict(valid_x)
        )
        self.next(self.average_scores)
        
    @step
    def average_scores(self, models):
        import numpy as np
        self.mean_score = np.mean([model.score 
                                   for model in models])
        self.next(self.end)
    
    @step
    def end(self):
        pass


if __name__ == "__main__":
    KFoldFlow()