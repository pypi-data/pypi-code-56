def transform(df, df_len):
    pandas2ri.activate()
    r.data('df')
    pandas_df = df.head(df_len)

    col_name = pandas_df.columns.to_list()
    col_name.insert(0, "ID")
    Inputid = pandas_df.index
    pandas_df.reindex(columns=col_name)
    pandas_df["ID"] = Inputid
    pandas_df = pandas_df.reindex(columns=col_name)

    return pandas_df