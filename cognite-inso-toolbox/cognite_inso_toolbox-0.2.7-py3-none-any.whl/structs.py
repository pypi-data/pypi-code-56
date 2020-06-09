import warnings
from abc import ABC, abstractmethod
from typing import Any, Dict, List

import arrow
import pandas as pd
from cognite.client import CogniteClient

from inso_toolbox.imputer import BaseImputer
from inso_toolbox.utils.type_checks import is_int


class Loader(ABC):
    @abstractmethod
    def get(self, **kwargs) -> pd.DataFrame:
        pass

    @abstractmethod
    def known_ids(self) -> List[Any]:
        pass


class CDFTSLoader(Loader):
    """
    Metadata for time series that are to be pulled.
    Freq must be in seconds passed as an integer.
    """

    def __init__(
        self, start_date: arrow.Arrow, end_date: arrow.Arrow, ts_list: List[Any], client: CogniteClient,
    ):
        self._client = client
        self._start = start_date
        self._end = end_date
        self._ids = ts_list
        if all(isinstance(id, str) and is_int(id) for id in self._ids):
            warnings.warn(
                f"All 'ts' in given 'ts_list' are int-interpretable. Assuming they are external_ids", UserWarning,
            )

    def get(self, **kwargs):
        if all(isinstance(id, str) for id in self._ids):  # external ids are strings
            return self._client.datapoints.retrieve(
                external_id=self._ids,
                start=self._start.to("utc").datetime.replace(tzinfo=None),
                end=self._end.to("utc").datetime.replace(tzinfo=None),
                **kwargs,
            ).to_pandas()
        elif all(map(is_int, self._ids)):  # internal ids are numbers
            return self._client.datapoints.retrieve(
                id=list(map(int, self._ids)),
                start=self._start.to("utc").datetime.replace(tzinfo=None),
                end=self._end.to("utc").datetime.replace(tzinfo=None),
                **kwargs,
            ).to_pandas()
        else:
            raise ValueError(f"Only {int} and {str} types as ids supported by CDF...")

    def known_ids(self) -> List[Any]:
        return self._ids


class TSBunch:  # no event support in v1
    def __init__(self, loader: Loader, config: Dict, freq: str):
        self._loader = loader
        self._transforms = config
        self._index = None
        self._freq = freq

    def run(self, **kwargs):
        """
        We want to load new data directly from the dataloader
        """
        df = self._loader.get(**kwargs)

        # apply transforms -> loop through config keys
        time_series = []

        for ts in self._loader.known_ids():
            new = self.apply_transforms(ts=df[ts], transforms=self._transforms[ts], frequency=self._freq)
            time_series.append(pd.DataFrame(new, columns=[ts], index=self._index))
        return pd.concat(time_series, axis=1)

    def apply_transforms(self, ts: pd.DataFrame, transforms: Dict, frequency: str):
        imputed = self.apply_impute(pd.DataFrame(ts), transforms["imputation_type"], frequency)
        self._index = imputed.index
        filtered = self.apply_filter(imputed, transforms["filters"])
        return self.apply_smoother(filtered, transforms["smoothers"])

    @staticmethod
    def apply_impute(ts: pd.DataFrame, imputer: BaseImputer, frequency: str):
        return imputer(ts, frequency) if imputer is not None else ts

    @staticmethod
    def apply_filter(ts: pd.DataFrame, filter_type: List):
        if filter_type is not None:
            if len(filter_type) == 1:
                return filter_type[0](ts)
            else:
                for filt in filter_type:
                    ts = filt(ts)
                return ts
        else:
            return ts

    @staticmethod
    def apply_smoother(ts: pd.DataFrame, smoother_type: List):
        if smoother_type is not None:
            if len(smoother_type) == 1:
                return smoother_type[0](ts)
            else:
                for sm in smoother_type:
                    ts = sm(ts)
                return ts
        else:
            return ts
