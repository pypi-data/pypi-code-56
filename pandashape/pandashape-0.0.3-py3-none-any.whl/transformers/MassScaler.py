import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from .GenericTransformer import GenericTransformer
from pandashape.enums.Scaling import Scaling


class MassScaler(GenericTransformer):
    def __init__(self, scaling=Scaling.MinMax, skewness_breakpoint=None, inplace=False, suffix='_scaled'):
        self.scaling = scaling
        self.skewness_breakpoint = skewness_breakpoint
        self.suffix = suffix

    def transform(self, df):
        # this feels unnecessarily ugly
        for column in df.iteritems():
            if (self.skewness_breakpoint is not None):
                skewness = abs(1 - column[1].skew())
                if (self.skewness_breakpoint is not None and skewness < self.skewness_breakpoint):
                    pass

            if self.scaling == Scaling.Log:
                print("transforming", column[0], self.scaling)
                df[f"{column[0]}{self.suffix}"] = np.log(column[1])
            elif self.scaling == Scaling.MinMax:
                scaler = MinMaxScaler()
                scaler.fit_transform(column)
            elif self.scaling == Scaling.Standard:
                scaler = StandardScaler()
                scaler.fit_transform(column)

        return df
