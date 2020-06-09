import pandas as pd

''' 
The utils methods can be used without an instance of a class over a DataFrame
'''
def filter_by_list(
    df,
    dim=None,
    list_to_filter=None
):
    r'''
    Return a dataframe filtered by a list passed as argument.

    Parameters
    ----------
    df : DataFrame
        It is the DataFrame with which want to work
    dim : str, default None
        Is the feature with which want to work
    list_to_filter : list, default None
        The attributes which want to filter into a list

    :return: A DataFrame filtered by the attributes in a list
    :rtype: DataFrame

    Examples
    --------
    >>> import datup as dt
    >>> dt.filter_by_list(df, "COLUMN",["list","of","attributes"])
    ''' 

    try:
        df_res = df[df[dim].isin(list_to_filter)]
    except IOError as error:
        print(error)
        raise 
    return df_res    

def antifilter_by_list(
    df,
    dim=None,
    list_to_filter=None
):
    r'''
    Return a dataframe filtered with a different attributes listed as argument.

    Parameters
    ----------
    df : DataFrame
        It is the DataFrame with which want to work
    dim : str, default None
        Is the feature with which want to work
    list_to_filter : list, default None
        The attributes which want to not filter into a list

    :return: A DataFrame filtered by the differents attributes in a list
    :rtype: DataFrame

    Examples
    --------
    >>> import datup as dt
    >>> dt.antifilter_by_list(df, "COLUMN",["list","of","attributes"])
    ''' 
    try:        
        df_res = df[~df[dim].isin(list_to_filter)]
    except IOError as error:
        print(error)
        raise 
    return df_res