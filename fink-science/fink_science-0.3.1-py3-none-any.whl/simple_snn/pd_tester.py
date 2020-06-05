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
from pyspark.sql import SparkSession
import pyspark.sql.functions as F

from fink_science.random_forest_snia.classifier import concat_col

from fink_science.simple_snn.normaliser import compute_delta_time
from fink_science.simple_snn.normaliser import pivot_dataframe_single
from fink_science.simple_snn.normaliser import save_to_HDF5

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
import pickle
from astropy.table import Table

from constants import SNTYPES, LIST_FILTERS, OFFSETS, OFFSETS_STR, FILTER_DICT, MIN_DT

SPARK = False

def process_phot_file(file_path, list_filters):
    """
    """

    # Load the PHOT and HEAD files
    dat = Table.read(file_path, format="fits")
    header = Table.read(file_path.replace("PHOT", "HEAD"), format="fits")
    df = dat.to_pandas()
    df_header = header.to_pandas()

    # Keep only columns of interest
    keep_col = ["MJD", "FLUXCAL", "FLUXCALERR", "FLT"]
    df = df[keep_col].copy()

    keep_col_header = [
        "SNID",
        "PEAKMJD",
        "HOSTGAL_PHOTOZ",
        "HOSTGAL_PHOTOZ_ERR",
        "HOSTGAL_SPECZ",
        "HOSTGAL_SPECZ_ERR",
        "SIM_REDSHIFT_CMB",
        "SIM_PEAKMAG_z",
        "SIM_PEAKMAG_g",
        "SIM_PEAKMAG_r",
        "SIM_PEAKMAG_i",
        "SNTYPE",
    ]
    keep_col_header = [k for k in keep_col_header if k in df_header.keys()]
    df_header = df_header[keep_col_header].copy()
    df_header["SNID"] = df_header["SNID"].astype(np.int64)

    # New light curves are identified by MJD == -777.0
    # Last line may be a line with MJD = -777.
    # Remove it so that it does not interfere with arr_ID below
    if df.MJD.values[-1] == -777.0:
        df = df.drop(df.index[-1])

    arr_ID = np.zeros(len(df), dtype=np.int64)
    arr_idx = np.where(df["MJD"].values == -777.0)[0]
    arr_idx = np.hstack((np.array([0]), arr_idx, np.array([len(df)])))
    # Fill in arr_ID
    for counter in range(1, len(arr_idx)):
        start, end = arr_idx[counter - 1], arr_idx[counter]
        # index starts at zero
        arr_ID[start:end] = df_header.SNID.iloc[counter - 1]
    df["SNID"] = arr_ID

    df = df.set_index("SNID")
    df_header = df_header.set_index("SNID")
    # join df and header
    df = df.join(df_header).reset_index()

    #############################################
    # Miscellaneous data processing
    #############################################
    df = df[keep_col + keep_col_header].copy()
    # filters have a trailing white space which we remove
    df.FLT = df.FLT.apply(lambda x: x.rstrip()).values.astype(str)
    # keep only filters we are going to use for classification
    df = df[df["FLT"].isin(list_filters)]
    # Drop the delimiter lines
    df = df[df.MJD != -777.000]
    # Reset the index (it is no longer continuous after dropping lines)
    df.reset_index(inplace=True, drop=True)
    # Add delta time
    df = compute_delta_time(df)
    # Remove rows post large delta time in the same light curve(delta_time > 150)
    # df = data_utils.remove_data_post_large_delta_time(df)
    df.to_pickle(file_path.replace('.FITS', '_proc.pickle'))

    return df

if SPARK:
    sns.set_context('talk')

    spark = SparkSession.builder.getOrCreate()

    spark.sparkContext.setLogLevel('WARN')

    fn = '/Users/julien/Documents/workspace/myrepos/des2ztf/DESSMALL4'

    df = spark.read.parquet(fn)

    df = df.sample(fraction=0.01)

    # Required alert columns
    what = [
        'jd', 'fid', 'magpsf', 'sigmapsf',
        'magnr', 'sigmagnr', 'magzpsci', 'isdiffpos'
    ]

    # Use for creating temp name
    prefix = 'c'
    what_prefix = [prefix + i for i in what]

    # Append temp columns with historical + current measurements
    for colname in what:
        df = concat_col(df, colname, prefix=prefix)

    df_pd = df.toPandas()
    objectId = df_pd['objectId']
    jd = df_pd['cjd']
    magpsf = df_pd['cmagpsf']
    sigmapsf = df_pd['csigmapsf']
    fid = df_pd['cfid']
    sntype = df_pd['publisher']

    # Convert filters
    filter_dic = {1: "g", 2: "r", 3: "i", 4: "z"}
    # Make a DataFrame from the columns
    # Note: MJD = JD − 2400000.5
    nalerts = len(jd)
    idx = np.random.randint(0, 1e6, nalerts)
    frame = {
        'SNID': np.concatenate([[idx[i]] * len(jd[i]) for i in range(nalerts)]),
        'MJD': np.concatenate(jd),
        'FLUXCAL': np.concatenate(magpsf),
        'FLUXCALERR': np.concatenate(sigmapsf),
        'FLT': np.vectorize(filter_dic.get)(np.concatenate(fid)),
        'SNTYPE': np.concatenate([[sntype[i]] * len(jd[i]) for i in range(nalerts)])
    }

    # Stupidly assign PEAKMJD to be the first measurement
    peakmjd = np.concatenate([[jd[i][int(len(jd[i]) / 2)]] * len(jd[i]) for i in range(nalerts)])
    #np.concatenate(jd)
    frame['PEAKMJD'] = peakmjd

    df = pd.DataFrame(frame)
    # df['SNID'] = df['SNID'].map(lambda x: int(x.split('.')[0][-6:]))
    unique_types = df.SNTYPE.unique()
    class_map = {}
    for idx, unique_type in enumerate(unique_types):
        class_map[unique_type] = 101 if "Ia" in unique_type else 120
    df['SNTYPE'] = df['SNTYPE'].map(class_map)
    # df = df[df['SNTYPE'] == 101]
    print(len(df[df['SNTYPE'] == 101]), len(df[df['SNTYPE'] == 120]))

    # df['MJD'] = df['MJD'].map(lambda x: x - 2400000.5)

    df_dt = compute_delta_time(df)
    df_dt.to_pickle('spark_snnified.pickle')
    print(df_dt[['MJD', 'FLUXCAL', 'FLUXCALERR', 'delta_time']])
else:
    # with open('DES_Ia-0001_PHOT.pickle', 'rb') as f:
    #     dfia = pickle.load(f)
    # with open('DES_NONIa-0001_PHOT.pickle', 'rb') as f:
    #     dfnonia = pickle.load(f)
    # print('LEN', len(dfia.SNID.unique()), len(dfnonia.SNID.unique()))
    # df_dt = pd.concat([dfia, dfnonia])
    # print(df_dt[['MJD', 'FLUXCAL', 'FLUXCALERR', 'delta_time']])
    df_ia = process_phot_file('DES_Ia-0001_PHOT.FITS', LIST_FILTERS)
    df_nia = process_phot_file('DES_NONIa-0001_PHOT.FITS', LIST_FILTERS)
    df_dt = pd.concat([df_ia, df_nia])
    print(len(df_dt[df_dt['SNTYPE'] == 101]), len(df_dt[df_dt['SNTYPE'] != 101]))

# with open('DES_Ia-0001_PHOT.pickle', 'rb') as f:
#     dfia = pickle.load(f)
# with open('DES_NONIa-0001_PHOT.pickle', 'rb') as f:
#     dfnonia = pickle.load(f)
# print('LEN', len(dfia.SNID.unique()), len(dfnonia.SNID.unique()))
# df_dt2 = pd.concat([dfia, dfnonia])
# # unique_types = df_dt.SNTYPE.unique()
# # print(unique_types)
# # class_map = {}
# # for unique_type in unique_types:
# #     class_map[unique_type] = 'Ia' if unique_type == 101 else 'Ic'
# # df_dt['SNTYPE'] = df_dt['SNTYPE'].map(class_map)
# print(df_dt2[['MJD', 'FLUXCAL', 'FLUXCALERR', 'delta_time']])
# import matplotlib.pyplot as plt
#
# plt.plot(range(1000), df_dt['FLUXCAL'].values[:1000], label='Emille sims')
# plt.plot(range(1000), df_dt2['FLUXCAL'].values[:1000], label='Anais sims')
# plt.legend()
# plt.show()
df_piv = pivot_dataframe_single(df_dt, LIST_FILTERS)

# save to hdf5
save_to_HDF5(df_piv, 'totos.h5', LIST_FILTERS, OFFSETS, OFFSETS_STR, FILTER_DICT)

# print(len(df_piv))
# df_pred = get_predictions(
#     'toto.h5',
#     model_dir='fullSNNsim_refactor_vanilla_000',
#     pred_dir='pred_dir')
# print(df_pred.columns)
# print(df_pred[['all_class0', 'all_class1', 'target', 'SNID']])
# print(df_pred[['all_class0', 'all_class1', 'target', 'target_median', 'target_std']])
# print(len(df_pred))
#
# g_pred = df_pred.groupby("SNID").median()
# preds = g_pred[[f"all_class{i}" for i in range(2)]].values
# # print(preds)
# preds = np.argmax(preds, axis=1)
# mask = g_pred.target.values == 0
# acc = (preds[mask] == g_pred.target.values[mask]).sum() / len(g_pred[mask])
# print('ACC = ', acc)
#
# # df_out = df_pred.groupby('SNID').first()
# # print(df_out.columns)
# # # out = df_out['target'].values
# # # out_nonia = sum(np.array(out) == 1)
# # # print('{} misclassified'.format(out_nonia))
#
# # df_out = df_pred.groupby('SNID')['target'].apply(list)
# # targets = pd.Series([df_out.iloc[i][0] for i in range(len(df_out))])
# # print(len(targets))
# # df_pd['target'] = targets
# # # print(df_pd[['publisher', 'target']])
# # #
# # targets = df_pd['target'].values
# # inputs = df_pd['publisher'].values
# #
# # inputs = np.array([0 if 'Ia' in i else 1 for i in inputs])
# # print('input length', len(inputs))
# # print('acc', sum(np.array(targets) == np.array(inputs)) / len(inputs))
# # mask0 = np.where(inputs == 0)[0]
# # print('acc - 0', sum(np.array([targets[i] for i in mask0]) == np.array([inputs[i] for i in mask0])) / len(mask0))
# # mask1 = np.where(inputs == 1)[0]
# # print('acc - 1', sum(np.array([targets[i] for i in mask1]) == np.array([inputs[i] for i in mask1])) / len(mask1))
