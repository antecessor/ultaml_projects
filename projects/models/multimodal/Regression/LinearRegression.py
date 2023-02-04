from sklearn.linear_model import LinearRegression as _LinearRegression

from LinearRegressionConfig import LinearRegressionConfig


class LinearRegression:
    def __init__(self, config: LinearRegressionConfig) -> None:
        super().__init__()
        self.config = config
        self.model = _LinearRegression(**self.config.to_dict())

    def fit(self, X, y):
        self.model = self.model.fit(X, y)

    def predict(self, X):
        return self.model.predict(X)

    def score(self, X, y):
        return self.model.score(X, y)
