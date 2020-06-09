import numpy as np
import pandas as pd
import ruptures as rpt


class ClippingDetector:
    """Detect data changepoints. Analyze the variance between regions. If variance is significantly
    reduced we have a clipped signal."""

    def __init__(self, threashold: int):
        self.threashold = threashold

    def __repr__(self):
        return "This is a Clipping Detection Model"

    def __call__(self, data: pd.DataFrame):
        self.model = rpt.Pelt(model="mahalanobis").fit(data.values)
        cps = self.model.predict(pen=50)
        cps.insert(0, 0)
        vars_ = []
        for pt in range(0, len(cps) - 1):
            left = cps[pt]
            right = cps[pt + 1]
            vars_.append(np.var(data.values[left:right]))
        pct_change = pd.Series(vars_).pct_change().values[1:]  # first value nan, throw it out
        data["shaved"] = 0
        for pt in range(0, len(pct_change)):
            left = cps[pt]
            right = cps[pt + 1]
            if pct_change[pt] * 100 > self.threashold:  # we have a shaved signal
                data.loc[left:right, "shaved"] = 1
        return data
