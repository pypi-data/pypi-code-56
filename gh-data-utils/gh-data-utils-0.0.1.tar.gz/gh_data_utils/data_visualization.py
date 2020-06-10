import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def get_overlapping_distributions(
        data, groups, data_col, order=None,
        x_label='', y_label='', title='',
        bins=20, tick_format = 'int'):

    """
    Generate overlapping distributions for 2 or more groups.
    Data should be a tidy pandas dataframe of records you want to compare
    (data_col), with a column identifying the groups you want compare by
    (groups). Visualization formatting is optional.
    """

    sns.set(rc={'figure.figsize':(9,5)})
    if order==None:
      order=data[groups].unique().tolist()

    for value in order:
      dist_data = data[data[groups]==value][data_col]
      ax = sns.distplot(dist_data,bins=bins)

    ax.legend(order)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_title(title,fontdict={'fontsize':16})
    xvals = ax.get_xticks()

    if tick_format == 'pct':
        ax.set_xticklabels(['{:,.0%}'.format(x) for x in xvals])

def get_barplot(
        data, groups, data_col, ci=95, order=None,
        hue=None, x_label='', y_label='', title='',
        palette=None, tick_format = 'int'):

    """
    Generate bar graphs for 2 or more groups.
    Data should be a tidy pandas dataframe of records you want to compare
    (data_col), with a column identifying the groups you want compare by
    (groups). Visualization formatting is optional.
    """

    sns.set(rc={'figure.figsize':(9,5)})
    ax = sns.barplot(
        x=groups, y=data_col, data=data, order=order,
        hue=hue, estimator=np.mean, ci=95,palette=palette)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_title(title,fontdict={'fontsize':16})
    yvals = ax.get_yticks()

    if tick_format == 'pct':
        ax.set_yticklabels(['{:,.0%}'.format(y) for y in yvals])
