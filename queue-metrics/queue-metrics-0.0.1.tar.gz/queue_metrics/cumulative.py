import pandas as pd


def fill_rate(df_enter: pd.DataFrame, df_leave: pd.DataFrame):
    """
    Compute the cumulative fill rate over the entire dataset (this is not an average)
    Assuming a wide formatted frame with index date as some resolution (e.g. week).
    The columns of the frames will be used to calculate the fill rate (the fullfilment rate).
    :param df_enter: a dataframe indexed by date describing items/elements entering the queue
    :param df_leave: a dataframe indexed by date describing items/elements leaving the queue after service
    """
    return df_leave.cumsum()/df_enter.cumsum()
    

def service_rate(df_leave):
    """
    Estimate the cumulative average service rate along the columns of a date indexed dataframe. That is, compute
    the service rate of each column of df_leave over the index as a cumulative average.
    :param df_leave: a dataframe indexed by date describing items/elements leaving the queue after service
    """
    return df_leave.expanding().mean()


def length(df_enter, df_leave):
    """
    The average queue length (L_Q) over the indices of the provided dataframes by subtracting the cumulative
    elements leaving the queue after service from those entering (cumulatively)
    :param df_enter: a dataframe indexed by date describing items/elements entering the queue
    :param df_leave: a dataframe indexed by date describing items/elements leaving the queue after service
    """
    return (df_enter.cumsum() - df_leave.cumsum()).expanding().mean()


def arrival_rate(df_enter):
    """
    Estimate the average arrival rate over the date index of the provided dataframe describing when elements
    are entering the queue.
    :param df_enter: a dataframe indexed by date describing items/elements entering the queue
    """
    return df_enter.expanding().mean()


def waiting_time(df_waiting_days):
    """
    Compute the average number of days waiting in the queue for an element.
    :param df_waiting_days: a dataframe containing the number of days waiting over some time index
    """
    df_denominator = pd.concat([df_waiting_days.index.to_frame().expanding().count()]*len(df_waiting_days.columns), axis=1)
    df_denominator.columns = df_waiting_days.columns

    return df_waiting_days.expanding().sum()/df_denominator
