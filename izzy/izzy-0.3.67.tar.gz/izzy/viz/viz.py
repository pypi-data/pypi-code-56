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
def plot(x, y=None, xlab='', ylab='', geom='line', output='auto', **kwargs):
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

    # If x is a DataFrame, split into columns
    if isinstance(x, pd.DataFrame):
        df = x
        x = df.index.values
        y = df.values

    # y must be ArrayLike
    if not isinstance(y, ArrayLike):
        raise AttributeError('y must be ArrayLike')

    # Dump everything into a DataFrame
    df = pd.DataFrame({'x': x})
    if not isinstance(y[0], ArrayLike):
        df['y'] = y
        y_labels = ['y']
    else:
        y_labels = []
        for i, y_i in enumerate(y):
            y_label = 'y' + str(i)
            df[y_label] = y_i
            y_labels.append(y_label)

    # Make geom an array if it's not one already; convert all elements to lowercase
    if not isinstance(geom, ArrayLike):
        geom = [geom]
    for i, geom_i in enumerate(geom):
        geom[i] = geom_i.lower()

    # Start building the figure
    fig = p9.ggplot(df)
    if 'line' in geom:
        for i, y_label in enumerate(y_labels):
            fig += p9.geom_line(p9.aes('x', y_label, group=1), color=p9.scale_color_cmap('Set1').palette(i))
    if 'point' in geom:
        for i, y_label in enumerate(y_labels):
            fig += p9.geom_point(p9.aes('x', y_label, group=1), color=p9.scale_color_cmap('Set1').palette(i))
    fig += p9.labs(x=xlab, y=ylab)
    fig += p9.theme(axis_text_x=p9.element_text(rotation=45))

    # Return
    if output in ['auto', 'ipython'] and get_ipython():
        with NamedTemporaryFile(delete=False) as tempfile:
            filename = str(tempfile.name) + '.svg'
        fig.save(filename=filename, verbose=False)
        display(SVG(filename))
        os.remove(filename)
    else:
        return fig
