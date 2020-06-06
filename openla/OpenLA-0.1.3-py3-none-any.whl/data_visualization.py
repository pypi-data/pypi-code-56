import matplotlib.dates as mdates
from matplotlib import pyplot as plt
from matplotlib import ticker as tick
from pandas.plotting import register_matplotlib_converters

from .data_extraction import *
from .check import _is_str, _is_str_list
from .data_classes.event_stream import EventStream
from .data_classes.operation_count import OperationCount
from .data_classes.time_range_aggregation import TimeRangeAggregation
from .data_classes.pagewise_aggregation import PageWiseAggregation, PageTransition


def _set_ax(ax, figsize):
    """
    Create new axes if it is None.

    :param ax: The axes to plot the figure on. If None, new axes is created
    :type ax: matplotlib.axes.Axes

    :param figsize: Figure size
    :type figsize: tuple(float, float)

    :return: The axes to plot the figure on
    """
    if ax is None:
        _, ax = plt.subplots(1, 1, figsize=figsize)

    return ax


def visualize_time_series_graph(event_stream, column, graph_type='line', time_format='%Y/%m/%d %H:%M:%S', xlabel=None, ylabel=None,
                               start_time=None, end_time=None, ax=None, figsize=None, save_file=None):
    """
    Draw a time series graph of indicated “column”. If the “save_file” is indicated, the graph is saved.

    :param event_stream: EventStream instance
    :type event_stream: EventStream

    :param column: Column to make Y-axis of time series graph
    :type colmn: str

    :param graph_type: The graph type selected from 'line', 'step', 'plot', or 'bar'
    :type graph_type: str

    :param start_time: The start time of time series
    :type start_time: pandas.Timestamp or datetime.datetime or None

    :param end_time: The end time of time series
    :type end_time: pandas.Timestamp or datetime.datetime or NOne

    :param ax: The axes to plot the figure on. If None, new axes is created
    :type ax: matplotlib.axes.Axes or None

    :param figsize: Figure size
    :type figsize: tuple(float, float) or None

    :param format: The time format in x axis.
                   For example, default format '%Y/%m/%d %H:%M:%S' converts "December 10, 2019 at 10:30 p.m." to "2019/12/10 22:30:00".
                   The meaning of directive such as '%Y' is in https://docs.python.org/3/library/time.html.
    :type format: str

    :param save_file: The file path for saving the graph
    :type save_file: str or None

    :return: The time series graph of selected type
    :rtype: matplotlib.axes.Axes
    """
    df = event_stream.df
    df["eventtime"] = pd.to_datetime(df["eventtime"])

    # time range
    if (start_time is None) and (end_time is None):
        df = df
    elif start_time is None:
        df = df[df["eventtime"] < end_time]
    elif end_time is None:
        df = df[start_time <= df["eventtime"]]
    else:
        df = df[(start_time <= df["eventtime"]) and (df["eventtime"] < end_time)]

    ax = _set_ax(ax, figsize)
    register_matplotlib_converters()
    # graph type
    if graph_type == "line":
        ax.plot(df["eventtime"], df[column])
    elif graph_type == "step":
        ax.step(df["eventtime"], df[column])
    elif graph_type == "plot":
        ax.plot(df["eventtime"], df[column], marker="s", linestyle='None')
    elif graph_type == "bar":
        ax.bar(df["eventtime"], df[column], linestyle='None')

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.xaxis.set_major_formatter(mdates.DateFormatter(time_format))
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.grid(True)
    if save_file is not None:
        plt.savefig(save_file)
    return ax


def visualize_operation_count_bar(operation_count, user_id, contents_id, operation_name=None,
                                  xlabel=None, ylabel=None, ax=None, figsize=None, save_file=None):
    """
    Draw a bar graph which represents each operation used by a specific learner.
    If the “save_file” is indicated, the scatter graph is saved.

    :param operation_count: OperationCount instance
    :type operation_count: OperationCount

    :param user_id: The user id to make graph
    :type user_id: str

    :param contents_id: The contents id to make graph
    :type contents_id: str

    :param operation_name: The operation name to count
    :type operation_name: str

    :param ax: The axes to plot the figure on. If None, new axes is created
    :type ax: matplotlib.axes.Axes or None

    :param figsize: Figure size
    :type figsize: tuple(float, float) or None

    :param save_file: The file path for saving the graph
    :type save_file: str or None

    :return: The bar graph
    :rtype: matplotlib.axes.Axes
    """
    assert not _is_str_list(user_id), "The list of user ids is not available. Please input a user id"
    assert not _is_str_list(contents_id), "The list of contents ids is not available. Please input a contents id"

    operation_count = select_user(operation_count, user_id)
    operation_count = select_contents(operation_count, contents_id)
    #
    count_df = operation_count.df
    count_df = count_df.drop(['userid', 'contentsid', 'lecture'], axis=1)

    ax = _set_ax(ax, figsize)
    register_matplotlib_converters()
    if operation_name is not None:
        count_df = count_df.loc[:, operation_name]

    if _is_str(operation_name):
        ax.bar(operation_name, count_df.values)
    else:
        ax.bar(count_df.columns, count_df.iloc[0].values)
    plt.xticks(rotation=90)
    plt.tight_layout()
    if xlabel is not None:
        ax.set_xlabel(xlabel)
    if ylabel is not None:
        ax.set_ylabel(ylabel)

    # plt.gca().xaxis.set_minor_locator(tick.MultipleLocator(1))

    if save_file is not None:
        plt.savefig(save_file)
    return ax


def visualize_operation_count_in_pages(course_info, pagewise_aggregation, user_id, contents_id, operation_name,
                                        xlabel=None, ylabel=None, ax=None, figsize=None, save_file=None):
    """
    Draw a bar graph which represents page-wise counting result of each operation used by a specific learner.
    If the “save_file” is indicated, the scatter graph is saved.

    :param course_info: CourseInformation instance
                       (See course_information module to know about class CourseInformation)
    :type course_info: CourseInformation

    :param pagewise_aggregation: PageWiseAggregation instance
    :type pagewise_aggregation: PageWiseAggregation

    :param user_id: The user id to make graph
    :type user_id: str

    :param contents_id: The contents id to make graph
    :type contents_id: str

    :param operation_name: The operation name to count
    :type operation_name: str

    :param ax: The axes to plot the figure on. If None, new axes is created
    :type ax: matplotlib.axes.Axes or None

    :param figsize: Figure size
    :type figsize: tuple(float, float) or None

    :param save_file: The file path for saving the graph
    :type save_file: str or None

    :return: The bar graph
    :rtype: matplotlib.axes.Axes
    """
    assert not _is_str_list(user_id), "The list of user ids is not available. Please input a user id"
    assert not _is_str_list(contents_id), "The list of contents ids is not available. Please input a contents id"
    assert not _is_str_list(operation_name), "The list of operation names is not available. Please input a operation name"

    pagewise_aggregation = select_user(pagewise_aggregation, user_id)
    pagewise_aggregation = select_contents(pagewise_aggregation, contents_id)

    num_pages = course_info.contents_id_to_num_pages(contents_id=contents_id)
    pagewise_df = pagewise_aggregation.df

    ax = _set_ax(ax, figsize)
    register_matplotlib_converters()

    ax.bar(x=pagewise_df['pageno'], height=pagewise_df[operation_name])
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

    plt.xticks(ticks=range(1, num_pages, 5), labels=range(1, num_pages, 5))
    plt.gca().xaxis.set_minor_locator(tick.MultipleLocator(1))

    if save_file is not None:
        plt.savefig(save_file)
    return ax


def visualize_pages_in_time_range(time_range_aggregation, user_id, lecture_week,
                                  xlabel=None, ylabel=None, ax=None, figsize=None, save_file=None):
    """

    :param time_range_aggregation: TImeRangeAggregation instance
    :type time_range_aggregation: TimeRangeAggregation

    :param user_id: The user id to make graph
    :type user_id: str

    :param lecture_week: The lecture week to make graph
    :type lecture_week: str

    :param xlabel: The label name of x-axis
    :type xlabel: str

    :param ylabel: The label name of y-axis
    :type ylabel: str

    :param ax: The axes to plot the figure on. If None, new axes is created
    :type ax: matplotlib.axes.Axes or None

    :param figsize: Figure size
    :type figsize: tuple(float, float) or None

    :param save_file: The file path for saving the graph
    :type save_file: str or None

    :return: The line graph which shows the page tracking
    :rtype: matplotlib.axes.Axes
    """

    ax = _set_ax(ax, figsize)
    register_matplotlib_converters()

    if isinstance(user_id, str):
        user_id = [user_id]

    max_time = 0
    max_page = 0
    for user in user_id:
        user_time_range = select_user(time_range_aggregation, user)
        user_time_range = select_lecture(user_time_range, lecture_week)
        time_range_df = user_time_range.df
        if time_range_df.empty:
            continue

        for column in ['elapsed_seconds', 'elapsed_minutes', 'elapsed_hours']:
            if column in time_range_df.columns:
                break
        ax.plot(time_range_df[column], time_range_df['pageno'])
        max_time = max(max_time, max(time_range_df[column]))
        max_page = max(max_page, max(time_range_df['pageno']))

    plt.gca().xaxis.set_minor_locator(tick.MultipleLocator(1))
    plt.gca().yaxis.set_minor_locator(tick.MultipleLocator(1))

    if xlabel is None:
        xlabel = column
    if ylabel is None:
        ylabel = "page"
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    if save_file is not None:
        plt.savefig(save_file)
    return ax