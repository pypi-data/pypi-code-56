import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

class Error(Exception):
    pass
class CorrelationError(Error):
    pass

''' 
The data_preparation methods can be used without an instance of a class over a DataFrame
'''

def col_cast(
    df,
    columns=[],
    to_cast=None
):
    r'''
    Return a dataframe with a set of columns casted.

    Parameters
    ----------
    df : DataFrame
        It is the DataFrame with which want to work
    columns : list, default None
        A list of columns which want to cast
    to_cast : str, default None
        The type of cast as str, int, float, etc.

    :return: A DataFrame with columns casted
    :rtype: DataFrame

    Examples
    --------
    >>> import datup as dt
    >>> dt.col_cast(df, ["columns","to","cast"],"type of cast")
    ''' 

    try:
        for column in columns:
            df[column] = df[column].astype(to_cast)
    except IOError as error:
        print(error)
        raise
    return df

def featureselection_correlation(
    df,
    method="spearman",
    thresold=0.7
):
    r''' 
    Return a graph with correlation factors between features and a list of features to drop as a suggest

    Parameters
    ----------
    df : DataFrame
        It is the DataFrame with which want to work
    method : str, default 'spearman'
        Took it from Pandas corr methods description
        Method of correlation:
            pearson : standard correlation coefficient
            kendall : Kendall Tau correlation coefficient
            spearman : Spearman rank correlation
            callable: callable with input two 1d ndarrays 
                and returning a float. Note that the returned matrix from corr will have 1 along the diagonals
                and will be symmetric regardless of the callable’s behavior.
    threshold : float, default 0.7
        Is the threshold of correlation factor which goes from 0 to 1

    :return: A Graph with correlation factors between features
    :rtype: Graph
    :return: A list with features that doesn't contribute with additional information to drop
    :rtype: List

    Examples
    --------
    >>> import datup as dt
    >>> dt.featureselection_correlation(df)
    '''

    try:
        object_list = []
        for column in df.columns:
            if df[column].dtype == "object":
                object_list.append(column)

        if len(object_list) > 0:
            raise CorrelationError("Is necessary convert the nex columns to a numeric representation: {}".format(object_list))
        else:
            corr_dor = df.corr(method=method).abs()
            upper_corr = corr_dor.where(np.triu(np.ones(corr_dor.shape), k=1).astype(np.bool))
            v_return = [dim for dim in upper_corr.columns if any(upper_corr[dim] > thresold)]
            fig = plt.figure(figsize=(10, 7.5))
            plt.matshow(corr_dor, fignum=fig.number)
            plt.xticks(range(df.shape[1]), df.columns, fontsize=11, rotation=90)
            plt.yticks(range(df.shape[1]), df.columns, fontsize=11)
            cb = plt.colorbar()
            cb.ax.tick_params(labelsize=11)
            plt.show()
    except CorrelationError as error:
        print(f"Error: {error}")
        raise
    return v_return