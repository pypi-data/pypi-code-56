import pandas as pd
import humanize


def _humanize(self, **kwds):
    return self.apply(humanize.naturalsize, **kwds)


pd.core.series.Series.humanize = _humanize
