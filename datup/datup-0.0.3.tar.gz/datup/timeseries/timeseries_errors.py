import numpy as np

''' 
The timeseries_errors methods can be used without an instance of a class over a timeseries
'''

def compute_rmse(
    timeseries,
    forecast
):
    r'''
    Return the root mean square error (RMSE) between actual and forecast points.
    
    Parameters
    ----------
    timeseries : DataFrame, Serie
        It is the DataFrame with which want to work
    forecast : DataFrame, Serie
        It is the forecasted DataFrame which want to compare the points
    
    :return: A RMSE error
    :rtype: float

    Examples
    --------
    >>> import datup as dt
    >>> dt.compute_rmse(timeseries, forecast)
    '''
    try:
        e = timeseries.iloc[:,0]-forecast.iloc[:,0]
        rmse = np.sqrt((e**2).mean())
    except IOError as error:
        #logger.exception('Exception found')
        print(f'Exception found: {error}')
        raise
    return rmse

def compute_mae(
    timeseries,
    forecast
):
    r'''
    Return the mean average error (MAE) between actual and forecast points.
    
    Parameters
    ----------
    timeseries : DataFrame, Serie
        It is the DataFrame with which want to work
    forecast : DataFrame, Serie
        It is the forecasted DataFrame which want to compare the points
    
    :return: A MAE error
    :rtype: float

    Examples
    --------
    >>> import datup as dt
    >>> dt.compute_mae(timeseries, forecast)
    '''
    try:
        e = timeseries.iloc[:,0]-forecast.iloc[:,0]
        mae = np.mean(abs(e))
    except IOError as error:
        #logger.exception('Exception found')
        print(f'Exception found: {error}')
        raise
    return mae

def compute_maep(timeseries, forecast):
    r'''
    Return the mean average error (MAEP) between actual and forecast points.
    
    Parameters
    ----------
    timeseries : DataFrame, Serie
        It is the DataFrame with which want to work
    forecast : DataFrame, Serie
        It is the forecasted DataFrame which want to compare the points
    
    :return: A MAEP error
    :rtype: float

    Examples
    --------
    >>> import datup as dt
    >>> dt.compute_maep(timeseries, forecast)
    '''    
    try:
        e = timeseries.iloc[:,0]-forecast.iloc[:,0]
        maep = 100*np.mean(abs(e))/np.mean(timeseries.iloc[:,0])
    except IOError as error:
        #logger.exception('Exception found')
        print(f'Exception found: {error}')
        raise
    return maep

def compute_mape(timeseries, forecast):
    r'''
    Return the mean average percentage error (MAPE) between actual and forecast points.
    
    Parameters
    ----------
    timeseries : DataFrame, Serie
        It is the DataFrame with which want to work
    forecast : DataFrame, Serie
        It is the forecasted DataFrame which want to compare the points
    
    :return: A MAPE error
    :rtype: float

    Examples
    --------
    >>> import datup as dt
    >>> dt.compute_mape(timeseries, forecast)
    '''
    try:
        e = (timeseries.iloc[:,0]-forecast.iloc[:,0])/timeseries.iloc[:,0]
        mape = 100*np.mean(abs(e))
    except IOError as error:
        #logger.exception('Exception found')
        print(f'Exception found: {error}')
        raise
    return mape

def compute_mase(timeseries, forecast):
    r'''
    Return mean absolute scaled error (MASE) between actual and forecast points.
    
    Parameters
    ----------
    timeseries : DataFrame, Serie
        It is the DataFrame with which want to work
    forecast : DataFrame, Serie
        It is the forecasted DataFrame which want to compare the points
    
    :return: A MASE error
    :rtype: float

    Examples
    --------
    >>> import datup as dt
    >>> dt.compute_mape(timeseries, forecast)
    '''
    try:
        ts_values = timeseries.iloc[:,0]
        e = (ts_values - forecast.iloc[:,0])
        denominator = (1/len(ts_values)-1)*sum(abs((ts_values-ts_values.shift(1)).fillna(0)))
        mase = np.mean(abs(e/denominator))        
    except IOError as error:
        #logger.exception('Exception found')
        print(f'Exception found: {error}')
        raise
    return mase