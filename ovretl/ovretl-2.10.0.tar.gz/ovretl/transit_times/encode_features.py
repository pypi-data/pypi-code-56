import pandas as pd
import numpy as np
from typing import List

from ovretl.transit_times.constants import DEFAULT_ENCODING


def encode_distance(train_df: pd.DataFrame, feature: str):
    train_df.loc[:, feature] = train_df[feature].apply(lambda x: int(x / 100) * 100 if not pd.isna(x) else np.nan)
    value_counts = train_df[feature].value_counts()
    mapping = {key: key if value >= 10 else DEFAULT_ENCODING for key, value in value_counts.items()}
    train_df.loc[:, feature] = train_df[feature].replace(mapping)


def encode_feature(train_df: pd.DataFrame, feature: str):
    value_counts = train_df[feature].value_counts()
    mapping = {key: key if value >= 10 else DEFAULT_ENCODING for key, value in value_counts.items()}
    train_df.loc[:, feature] = train_df[feature].replace(mapping)


def encode_features(train_df: pd.DataFrame, qualitative_features: List[str], distance_features: List[str]):
    train_df_copy = train_df.copy()
    for feature in qualitative_features:
        encode_feature(train_df_copy, feature)
    for feature in distance_features:
        encode_distance(train_df_copy, feature)
    return train_df_copy
