from dataclasses import field, dataclass

from projects.utils.Singleton import Singleton


@dataclass
class LinearRegressionConfig(metaclass=Singleton):
    #: Whether to calculate the intercept for this model.
    #: If set to False, no intercept will be used in calculations
    #: (i.e. data is expected to be centered).
    fit_intercept: bool = field(default=True)

    #: The number of jobs to use for the computation.
    n_jobs: int = field(default=None)

    #: force cofficients to be positive
    positive: bool = field(default=False)

    def to_dict(self):
        return {
            'fit_intercept': self.fit_intercept,
            'n_jobs': self.n_jobs,
            'positive': self.positive
        }
