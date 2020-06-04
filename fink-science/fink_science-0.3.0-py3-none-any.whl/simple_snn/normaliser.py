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
import numpy as np
import pandas as pd
from natsort import natsorted
from collections import OrderedDict
import natsort
from itertools import combinations
import yaml
import torch
from pathlib import Path
import h5py

from fink_science.simple_snn.reader import HDF5Dataset

from constants import SNTYPES, LIST_FILTERS, OFFSETS, OFFSETS_STR, FILTER_DICT, MIN_DT


def compute_delta_time(df):
    """Compute the delta time between two consecutive observations

    Parameters
    ----------
    df: pandas.DataFrame
        dataframe holding lightcurve data.

    Returns
    ----------
    out: pandas.DataFrame
        Input DataFrame with delta_time features
    """
    df["delta_time"] = df["MJD"].diff()
    # Fill the first row with 0 to replace NaN
    df.delta_time = df.delta_time.fillna(0)
    try:
        IDs = df.SNID.values
    # Deal with the case where lightcrv_ID is the index
    except AttributeError:
        assert df.index.name == "SNID"
        IDs = df.index.values
    # Find idxs of rows where a new light curve start then zero delta_time
    idxs = np.where(IDs[:-1] != IDs[1:])[0] + 1
    arr_delta_time = df.delta_time.values
    arr_delta_time[idxs] = 0
    df["delta_time"] = arr_delta_time

    return df

def pivot_dataframe_single(df, list_filters, df_salt=None):
    """
    """
    arr_MJD = df.MJD.values
    arr_delta_time = df.delta_time.values
    # Loop over times to create grouped MJD:
    # if filters are acquired within less than 0.33 MJD (~8 hours) of each other
    # they get assigned the same time
    min_dt = MIN_DT
    time_last_change = 0
    arr_grouped_MJD = np.zeros_like(arr_MJD)
    for i in range(len(df)):
        time = arr_MJD[i]
        dt = arr_delta_time[i]
        # 2 possibilities to update the time
        # dt == 0 (it"s a new light curve)
        # time - time_last_change > min_dt
        if dt == 0 or (time - time_last_change) > min_dt:
            arr_grouped_MJD[i] = time
            time_last_change = time
        else:
            arr_grouped_MJD[i] = arr_grouped_MJD[i - 1]

    # Add grouped delta time to dataframe
    df["grouped_MJD"] = np.array(arr_grouped_MJD)

    # Some filters may appear multiple times with the same grouped MJD within same light curve
    # When this happens, we select the one with lowest FLUXCALERR
    df = df.sort_values("FLUXCALERR").groupby(["SNID", "grouped_MJD", "FLT"]).first()
    # We then reset the index
    df = df.reset_index()
    # Compute PEAKMJDNORM = PEAKMJD in days since the start of the light curve
    df["PEAKMJDNORM"] = df["PEAKMJD"] - df["MJD"]
    # The correct PEAKMJDNORM is the first one hence the use of first after groupby
    df_PEAKMJDNORM = df[["SNID", "PEAKMJDNORM"]].groupby("SNID").first().reset_index()
    # Remove PEAKMJDNORM
    df = df.drop("PEAKMJDNORM", 1)
    # Add PEAKMJDNORM back to df with a merge on SNID
    df = df.merge(df_PEAKMJDNORM, how="left", on="SNID")
    # drop columns that won"t be used onwards
    df = df.drop(["MJD", "delta_time"], 1)

    group_features_list = [
        "SNID",
        "grouped_MJD",
        "PEAKMJD",
        "PEAKMJDNORM",
        "SIM_REDSHIFT_CMB",
        "SNTYPE",
        "SIM_PEAKMAG_z",
        "SIM_PEAKMAG_g",
        "SIM_PEAKMAG_r",
        "SIM_PEAKMAG_i",
    ] + [k for k in df.keys() if "HOST" in k]

    # check if keys are in header
    group_features_list = [k for k in group_features_list if k in df.keys()]
    # Pivot so that for a given MJD, we have info on all available fluxes / error
    df = pd.pivot_table(df, index=group_features_list, columns=["FLT"])

    # Flatten columns
    df.columns = ["_".join(col).strip() for col in df.columns.values]
    # Reset index to get grouped_MJD and target as columns
    df.reset_index(df.index.names, inplace=True)
    # Rename grouped_MJD to MJD
    df.rename(columns={"grouped_MJD": "MJD"}, inplace=True)

    # New column to indicate which channel (r,g,z,i) is present
    # The column will read ``rg`` if r,g are present; ``rgz`` if r,g and z are present, etc.
    for flt in list_filters:
        df[flt] = np.where(df["FLUXCAL_%s" % flt].isnull(), "", flt)
    df["FLT"] = df[list_filters[0]]
    for flt in list_filters[1:]:
        df["FLT"] += df[flt]
    # Ensure combination is written in natural sorted order
    df["FLT"] = df.FLT.apply(lambda x: "".join(natsorted(list(x))))
    # Drop some irrelevant columns
    df = df.drop(list_filters, 1)
    # Finally replace NaN with 0
    df = df.fillna(0)
    # Add delta_time back. We removed all delta time columns above as they get
    # filled with NaN during pivot. It is clearer to recompute delta time once the pivot is complete
    df = compute_delta_time(df)

    # Cast columns to float32
    for c in df.columns:
        if df[c].dtype == np.float64:
            df[c] = df[c].astype(np.float32)

    if df_salt is not None:
        df_salt["salt"] = 1
        df = df.merge(df_salt[["SNID", "mB", "c", "x1", "salt"]], on="SNID", how="left")
        df["salt"] = df["salt"].fillna(0)
    else:
        df["salt"] = 0

    df.drop(columns="MJD", inplace=True)

    return df

def save_to_HDF5(df, hdf5_file, list_filters, offsets, offsets_str, filter_dict):
    """Saved processed dataframe to HDF5

    Args:
        settings (ExperimentSettings): controls experiment hyperparameters
        df (pandas.DataFrame): dataframe holding processed data

    """

    # Compute how many unique nights of data taking existed around PEAKMJD
    df["time"] = df[["SNID", "delta_time"]].groupby("SNID").cumsum()
    list_df_night = []
    for offset, suffix in zip(offsets, offsets_str):
        new_column = f"PEAKMJD{suffix}_unique_nights"
        df_night = (
            df[df["time"] < df["PEAKMJDNORM"] + offset][["PEAKMJDNORM", "SNID"]]
            .groupby("SNID")
            .count()
            .rename(columns={f"PEAKMJDNORM": new_column})
            .reset_index()
        )
        list_df_night.append(df_night)

    # Compute how many occurences of a specific filter around PEAKMJD
    list_df_flt = []
    for flt in list_filters:
        # Check presence / absence of the filter at all time steps
        df[f"has_{flt}"] = df.FLT.str.contains(flt).astype(int)
        for offset, suffix in zip(offsets, offsets_str):
            new_column = f"PEAKMJD{suffix}_num_{flt}"
            df_flt = (
                df[df["time"] < df["PEAKMJDNORM"] + offset][[f"has_{flt}", "SNID"]]
                .groupby("SNID")
                .sum()
                .astype(int)
                .rename(columns={f"has_{flt}": new_column})
                .reset_index()
            )
            list_df_flt.append(df_flt)

        df.drop(columns=f"has_{flt}", inplace=True)

    list_training_features = [f"FLUXCAL_{f}" for f in list_filters]
    list_training_features += [f"FLUXCALERR_{f}" for f in list_filters]
    list_training_features += ["delta_time"]

    list_metadata_features = [
        "SNID",
        "SNTYPE",
        "mB",
        "c",
        "x1",
        "SIM_REDSHIFT_CMB",
        "SIM_PEAKMAG_z",
        "SIM_PEAKMAG_g",
        "SIM_PEAKMAG_r",
        "SIM_PEAKMAG_i",
        "salt",
    ]
    list_metadata_features += [f for f in df.columns.values if "PEAKMJD" in f]
    list_metadata_features += [f for f in df.columns.values if "HOSTGAL" in f]
    list_metadata_features = [k for k in list_metadata_features if k in df.keys()]

    # Get the list of lightcurve IDs
    ID = df.SNID.values
    # Find out when ID changes => find start and end idx of each lightcurve
    idx_change = np.where(ID[1:] != ID[:-1])[0] + 1
    idx_change = np.hstack(([0], idx_change, [len(df)]))
    list_start_end = [(s, e) for s, e in zip(idx_change[:-1], idx_change[1:])]
    # N.B. We could use df.loc[SNID], more elegant but much slower

    # Shuffle
    np.random.shuffle(list_start_end)

    # Drop features we no longer need
    df.drop(columns=["time"], inplace=True)

    # Save hdf5 file
    with h5py.File(hdf5_file, "w") as hf:

        n_samples = len(list_start_end)

        # Fill metadata
        start_idxs = [i[0] for i in list_start_end]

        df_meta = df[list_metadata_features].iloc[start_idxs]
        df = df.drop(columns=list_metadata_features)

        for df_tmp in list_df_flt + list_df_night:
            df_meta = df_meta.merge(df_tmp, how="left", on="SNID")

        list_metadata_features = df_meta.columns.tolist()
        arr_meta = df_meta.values.astype(np.float32)
        hf.create_dataset("metadata", data=arr_meta)
        hf["metadata"].attrs["columns"] = np.array(
            list_metadata_features, dtype=h5py.special_dtype(vlen=str)
        )

        ####################################
        # Save the rest of the data to hdf5
        ####################################
        data_type = h5py.special_dtype(vlen=np.dtype("float32"))
        hf.create_dataset("data", (n_samples,), dtype=data_type)

        # Add normalizations
        flux_features = [f"FLUXCAL_{f}" for f in list_filters]
        fluxerr_features = [f"FLUXCALERR_{f}" for f in list_filters]

        hf["data"].attrs["flux_norm"] = log_standardization(df[flux_features].values)
        hf["data"].attrs["fluxerr_norm"] = log_standardization(
            df[fluxerr_features].values
        )
        hf["data"].attrs["delta_time_norm"] = log_standardization(
            df["delta_time"].values
        )

        df["FLT"] = df["FLT"].map(filter_dict).astype(np.float32)

        list_training_features += ["FLT"]
        hf["data"].attrs["columns"] = np.array(
            list_training_features, dtype=h5py.special_dtype(vlen=str)
        )
        hf["data"].attrs["n_features"] = len(list_training_features)

        # Save training features to hdf5
        # logging_utils.print_green("Save data features to HDF5")
        arr_feat = df[list_training_features].values
        for idx, idx_pair in enumerate(list_start_end):
            arr = arr_feat[idx_pair[0] : idx_pair[1]]
            hf["data"][idx] = np.ravel(arr)

def log_standardization(arr):
    """Normalization strategy for the fluxes and fluxes error

    - Log transform the data
    - Mean and std dev normalization

    Args:
        arr (np.array): data to normalize

    Returns:
        (LogStandardized) namedtuple holding normalization data
    """

    arr_min = -100
    arr_log = np.log(-arr_min + np.clip(arr, a_min=arr_min, a_max=np.inf) + 1e-5)
    arr_mean = arr_log.mean()
    arr_std = arr_log.std()

    return [arr_min, arr_mean, arr_std]
