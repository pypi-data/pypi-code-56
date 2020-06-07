import pandas as pd

def data_info(df):
    """
    Get info of the input dataframe
    """
    return df.describe()