from metaflow import FlowSpec, step

class ParamGridFlow(FlowSpec):
    
    @step
    def start(self):
        from sklearn.datasets import load_iris
        data = load_iris()
        self.X, self.y = data['data'], data['target']
        self.next(self.make_grid)
        
    @step
    def make_grid(self):
        from sklearn.model_selection import ParameterGrid
        param_values = {'max_depth': [2, 4, 8, 16], 
                        'criterion': ['entropy', 'gini']}
        self.grid_points = list(
            ParameterGrid(param_values)
        )
        # evaluate each in cross product of ParameterGrid.
        self.next(self.evaluate_model, 
                  foreach='grid_points')
        
    @step
    def evaluate_model(self):
        from sklearn.tree import ExtraTreeClassifier
        from sklearn.model_selection import cross_val_score
        self.clf = ExtraTreeClassifier(**self.input)
        self.scores = cross_val_score(self.clf, self.X, 
                                      self.y, cv=5)
        self.next(self.join)
        
    @step
    def join(self, inputs):
        import numpy as np
        self.mean_scores = [np.mean(model.scores) 
                            for model in inputs]
        self.next(self.end)
        
    @step
    def end(self):
        pass
    
if __name__ == "__main__":
    ParamGridFlow()