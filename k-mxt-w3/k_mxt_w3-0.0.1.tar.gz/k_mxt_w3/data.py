from abc import abstractmethod, ABC
import pandas as pd
import numpy as np
import logging


logger = logging.getLogger('k_mxt_w3.data_import')


class DataImport(ABC):
    @abstractmethod
    def __init__(self, df):
        self.df = df


class DataPropertyImportSpace(DataImport):
    def __init__(self, df):
        super().__init__(df)

    def get_data(self, name_latitude_cols='latitude', name_longitude_cols='longitude', features_list=None):
        x = self.df[name_latitude_cols].to_numpy(dtype=np.float)
        y = self.df[name_longitude_cols].to_numpy(dtype=np.float)
        return x.reshape(-1, 1), y.reshape(-1, 1), self.df[features_list].to_numpy(dtype=np.float)


class DataSave:
    @classmethod
    def arrays_to_csv(cls, source_filename, new_filename, **kwargs):
        df = pd.read_csv(source_filename)
        new_df = pd.DataFrame.from_dict(kwargs)
        res = pd.concat([df, new_df], axis=1)
        res.to_csv(new_filename)
