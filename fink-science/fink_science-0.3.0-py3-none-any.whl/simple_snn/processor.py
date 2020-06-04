# Copyright 2019 AstroLab Software
# Author: Julien Peloton
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from pyspark.sql.functions import pandas_udf, PandasUDFType
from pyspark.sql.types import DoubleType, StringType, IntegerType

import pandas as pd
import numpy as np

import os

from fink_science.simple_snn.normaliser import compute_delta_time
from fink_science.simple_snn.normaliser import pivot_dataframe_single
from fink_science.simple_snn.normaliser import get_predictions

from fink_science.tester import spark_unit_tests

@pandas_udf(IntegerType(), PandasUDFType.SCALAR)
def snnscore(
        objectId, sntype, jd, fid, magpsf, sigmapsf, magnr,
        sigmagnr, magzpsci, isdiffpos, model=None) -> pd.Series:
    """ Return the probability of an alert to be a SNe Ia using a Bayesian
    Neural Network.

    Parameters
    ----------
    jd: Spark DataFrame Column
        JD times (float)
    fid: Spark DataFrame Column
        Filter IDs (int)
    magpsf, sigmapsf: Spark DataFrame Columns
        Magnitude from PSF-fit photometry, and 1-sigma error
    magnr, sigmagnr: Spark DataFrame Columns
        Magnitude of nearest source in reference image PSF-catalog
        within 30 arcsec and 1-sigma error
    magzpsci: Spark DataFrame Column
        Magnitude zero point for photometry estimates
    isdiffpos: Spark DataFrame Column
        t => candidate is from positive (sci minus ref) subtraction
        f => candidate is from negative (ref minus sci) subtraction
    model: Spark DataFrame Column, optional
        Path to the trained model. Default is None, in which case the default
        model `data/models/default-model.obj` is loaded.

    Returns
    ----------
    probabilities: 1D np.array of float
        Probability between 0 (non-Ia) and 1 (Ia).

    Examples
    ----------
    Examples
    ----------
    """
    # Convert filters
    filter_dic = {1: "g", 2: "r", 3: "i", 4: "z"}
    # Make a DataFrame from the columns
    # Note: MJD = JD − 2400000.5
    nalerts = len(jd)
    frame = {
        'SNID': np.concatenate([[objectId[i] for o in range(len(jd[i]))] for i in range(nalerts)]),
        'MJD': np.concatenate(jd),
        'FLUXCAL': np.concatenate(magpsf),
        'FLUXCALERR': np.concatenate(sigmapsf),
        'FLT': np.vectorize(filter_dic.get)(np.concatenate(fid)),
        'SNTYPE': np.concatenate([[sntype[i] for o in range(len(jd[i]))] for i in range(nalerts)])
    }

    # Stupidly assign PEAKMJD to be the first measurement
    peakmjd = np.concatenate(jd)
    frame['PEAKMJD'] = peakmjd

    df = pd.DataFrame(frame)
    # print(df)

    df_dt = compute_delta_time(df)
    # print(df_dt)
    df_piv = pivot_dataframe_single(df_dt, ["r", "g", "i", "z"])

    idea here: load data anais sent

    # print(df_piv.columns)
    df_pred = get_predictions(
        df_piv,
        model_dir='fullSNNsim_refactor_vanilla_000',
        pred_dir='pred_dir')
    print(df_pred[['all_class0', 'all_class1', 'target', 'SNID']])

    df_out = df_pred.groupby('SNID')['target'].apply(list)
    # print(df_out)
    return pd.Series([df_out.iloc[i][0] for i in range(len(df_out))])


if __name__ == "__main__":
    """ Execute the test suite """

    globs = globals()
    ztf_alert_sample = 'fink_science/data/alerts/alerts.parquet'
    globs["ztf_alert_sample"] = ztf_alert_sample

    model_path = 'fink_science/data/models/default-model.obj'
    globs["model_path"] = model_path

    # Run the test suite
    spark_unit_tests(globs)
