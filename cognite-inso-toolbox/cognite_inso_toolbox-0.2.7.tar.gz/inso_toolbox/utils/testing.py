def any_nan_in_dataframe(df):
    return df.isna().values.any()
