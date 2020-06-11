"""
viz.py
Written in Python3
author: C. Lockhart <chris@lockhartlab.org>
"""

from izzy.defaults import *

from IPython import get_ipython
from IPython.display import display, SVG
import os
import pandas as pd
import plotnine as p9
from tempfile import NamedTemporaryFile
from typelike import ArrayLike


# Plot
def plot(x, y=None, xlab='', ylab='', geom=('line', 'point'), output='auto', **kwargs):
    """
    https://matplotlib.org/tutorials/colors/colormaps.html
    https://github.com/rstudio/cheatsheets/blob/master/data-visualization-2.1.pdf
    Parameters
    ----------
    x
    y
    xlab
    ylab
    geom
    output
    kwargs

    Returns
    -------

    """

    output = str(output).lower()

    # If x is a DataFrame, x is the index and y are columns
    if isinstance(x, pd.DataFrame):
        df = x
        x = df.index.names
        y = df.columns

    # Otherwise, construct a DataFrame
    else:
        # y must be ArrayLike
        if not isinstance(y, ArrayLike):
            raise AttributeError('y must be ArrayLike')

        # Dump everything into a DataFrame
        df = pd.DataFrame({'x': x}).set_index('x')
        if not isinstance(y[0], ArrayLike):
            df['y'] = y
        else:
            for i, y_i in enumerate(y):
                df['y' + str(i)] = y_i

    # Name df.index.name as x for convenience
    x = df.index.name
    y = df.columns
    df = df.reset_index().melt(id_vars=x)

    # Make geom an array if it's not one already; convert all elements to lowercase
    if not isinstance(geom, ArrayLike):
        geom = [geom]
    for i, geom_i in enumerate(list(geom)):
        geom[i] = geom_i.lower()

    # Start building the figure
    fig = p9.ggplot(df, p9.aes(x=x, y='value', color='variable', group='variable'))
    if 'line' in geom:
        fig += p9.geom_line()
    if 'point' in geom:
        fig += p9.geom_point()
    fig += p9.labs(x=xlab, y=ylab)
    fig += p9.theme(axis_text_x=p9.element_text(rotation=45), legend_key=p9.element_blank())
    if len(y) > 1:
        fig += p9.scale_color_manual(name=' ', values=[p9.scale_color_cmap('Set1').palette(i) for i in range(len(y))])

    # Return
    if output in ['auto', 'ipython'] and get_ipython():
        with NamedTemporaryFile(delete=False) as tempfile:
            filename = str(tempfile.name) + '.svg'
        fig.save(filename=filename, verbose=False)
        display(SVG(filename))
        os.remove(filename)
    else:
        return fig