def extract(dir, cdf = "hgu133plus2cdf"):
    affy = importr('affy')
    annotation = importr(cdf)
    print("Annotation is using {}".format(ann))

    os.chdir(dir)
    datapath = os.getcwd()
    datalist = [i for i in os.listdir(datapath) if i.endswith(".CEL")]
    print("Catch CEL data {}".format(datalist))

    cdatalist = robjects.r['as.character'](datalist)
    rawdata = affy.ReadAffy(filenames=cdatalist)
    rmdata = affy.rma(rawdata)

    data = robjects.r['exprs'](rmdata)
    df = robjects.r['data.frame'](data)

    rID_list = robjects.r['rownames'](df)
    df_len = len(rID_list)
    print("This Platform have {} probes".format(df_len))

    return df, df_len

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
