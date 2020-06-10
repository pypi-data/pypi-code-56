
from typing import List
    
from sapsan.core.abstrctions.algorithm import Parameter, Artifact, Metric
from sapsan.core.abstrctions.experiment import Experiment
from sapsan.core.abstrctions.tracking import TrackingBackend
from sapsan.core.tracking.logger import LoggingBackend
from research.algorithm import ResearchEstimator
from research.dataset import ResearchDataset
    
    
class ResearchExperiment(Experiment):
    def __init__(self,
                 estimator: ResearchEstimator,
                 dataset: ResearchDataset,
                 tracking_backend: TrackingBackend = LoggingBackend()):
        super().__init__(tracking_backend)
        self.estimator = estimator
        self.dataset = dataset
    
    def run(self, **kwargs):
        data = self.dataset.load()
        return self.estimator.predict(data)
    
    def test(self, **kwargs):
        data = self.dataset.load()
        return self.estimator.predict(data)
    
    @property
    def parameters(self) -> List[Parameter]:
        return [
            Parameter("estimator", str(self.estimator)),
            Parameter("dataset", str(self.dataset))
        ]
    
    @property
    def metrics(self) -> List[Metric]:
        return []
    
    @property
    def artifacts(self) -> List[Artifact]:
        return []

