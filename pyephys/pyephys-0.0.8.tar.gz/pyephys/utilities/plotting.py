import numpy as np
import matplotlib.pyplot as plt


def delete_empty_axes(fig, axes):
    """Delete the empty subplots in a figure."""

    for x in np.concatenate(axes):
        if len(x.get_lines()) == 0:
            fig.delaxes(x)


def simplify_axes(ax):
    """Remove the spines, the ticks and the tick labels in a subplot."""

    for side in ['left', 'right', 'top', 'bottom']:
        ax.spines[side].set_visible(False)
    ax.tick_params(left=False, right=False, top=False, bottom=False,
                   labelleft=False, labelright=False, labeltop=False,
                   labelbottom=False)


def scalebar(ax, xmin, xmax, ymin, ymax, c='k', lw=4):
    """Add a scale bar to a subplot."""

    ax.plot([xmin, xmax], [ymin, ymin], c, lw=lw)
    ax.plot([xmax, xmax], [ymin, ymax], c, lw=lw)


def format_func(value):
    """x axis with pi labels."""
    # find number of multiples of pi/2
    n = int(np.round(2 * value / np.pi))
    if n == 0:
        return "0"
    elif n == 1:
        return r"$\pi/2$"
    elif n == 2:
        return r"$\pi$"
    elif n == -1:
        return r"$-\pi/2$"
    elif n == -2:
        return r"$-\pi$"


def set_subplot_color(ax, color, title=None):
    """Change the color of the spines, the ticks, the tick labels, the axis labels and the title in a subplot."""

    if title is not None:
        ax.set_title(title, color=color)

    ax.tick_params(color=color, labelcolor=color)

    for spine in ax.spines.values():
        spine.set_edgecolor(color)

    ax.xaxis.label.set_color(color)
    ax.yaxis.label.set_color(color)


def create_subplots_layout(nplots, ncols=4, size=(3, 3)):
    nrows = int(np.ceil(nplots / ncols))
    fig, axarr = plt.subplots(nrows, ncols, figsize=np.array(size) * (ncols, nrows), sharex=True, sharey=True,
                              squeeze=False)

    return fig, axarr


def set_subplots_axis_labels(ax, xlabel, ylabel):
    for i_row in range(ax.shape[0]):
        ax[i_row, 0].set_ylabel(ylabel)

    if ax.shape[0] == 1:
        for ax_i in ax.flat:
            ax_i.set_xlabel(xlabel)
    else:
        for i_col in range(ax.shape[1]):
            last_row = np.where([bool(len(ax[i_row, i_col].get_lines())) for i_row in range(ax.shape[0])])[0][-1]
            ax[last_row, i_col].set_xlabel(xlabel)
