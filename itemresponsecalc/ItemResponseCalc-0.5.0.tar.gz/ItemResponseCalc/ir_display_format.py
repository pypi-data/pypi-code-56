"""Functions and classes to display results from an OrdinalItemResponseModel object.
"""
# ***** check special chars for latex and txt variants

import numpy as np
from itertools import cycle, product

import matplotlib.pyplot as plt
import logging

logger = logging.getLogger(__name__)

# --------------------------- Default format parameters:
FMT = {'table_format': 'latex',  # or 'tab' for tab-delimited tables
       'figure_format': 'pdf',   # or 'eps', or 'png', or 'pdf', for saved plots
       'colors': 'rbg',  # color cycle to separate results in plots
       'line_styles': ['solid', 'dashed', 'dashdot', 'dotted'],
       'markers': 'o^sDv',  # plot symbols, each repeated with each fillstyle
       'fillstyle': ['full', 'none'], # marker style
       'credibility': 'Credibility',  # heading in tables
       'correlation': 'Correlation',  # heading in tables
       }
# = module-global dict with default settings for display details
# that may be changed by user
# NOTE: Largest number of combinations of color, line_style, marker, fillstyle
# is obtained if the number of alternatives are NOT divisible by each other.

TABLE_FILE_SUFFIX = {'latex': '.tex', 'tab': '.txt'}
# = mapping table_format -> file suffix

# ------------------------- Matplotlib settings:
plt.rcParams.update({'figure.max_open_warning': 0})
# suppress warning for many open figures
pad_inches = plt.rcParams['savefig.pad_inches']
plt.rcParams['savefig.pad_inches'] = 0.
plt.rcParams['savefig.bbox'] = 'tight'
# *** allow user to set other plt.rcParams ? ***
# -----------------------------------------------


def set_format_param(**kwargs):
    """Set / modify module-global format parameters
    :param kwargs: dict with format variables
        to replace the default values in FMT
    :return: None
    """
    # *** allow user to set other plt.rcParams here ? ***
    for (k, v) in kwargs.items():
        k = k.lower()
        if k not in FMT:
            logger.warning(f'Format setting {k}={repr(v)} is not known, not used')
        FMT[k] = v


def _percent():
    """Percent sign for tables
    :return: str
    """
    return '\\%' if FMT['table_format'] == 'latex' else '%'


# ---------------------------- Main Result Classes
class FigureRef:
    """Reference to a single graph instance
    """
    def __init__(self, ax, name=None, path=None):
        """
        :param ax: Axes instance containing the graph
        :param path: Path to directory where figure has been saved
        :param name: (optional) updated name of figure file
        """
        self.ax = ax
        self.name = name
        self.path = path

    def __repr__(self):
        return (f'FigureRef(ax= {repr(self.ax)}, ' +
                f'name= {repr(self.name)}), path= {repr(self.path)}')

    @property
    def fig(self):
        return self.ax.figure

    def save(self, path, name=None):
        """Save figure to given path
        :param path: Path to directory where figure is saved
        :param name: (optional) updated name of figure file
        :return: None
        Result: updated properties path, name
        """
        if name is None:
            name = self.name
        name = _clean_file_name(name)
        path.mkdir(parents=True, exist_ok=True)
        f = (path / name).with_suffix('.' + FMT['figure_format'])
        self.fig.savefig(str(f))
        self.path = path
        self.name = f.name

    def mapped_y_axis(self, y, y_mapped, y_label='', fontsize=14):
        """Add a second y_axis to self.ax with ticks placed at
        y values corresponding to uniform steps in y_mapped values
        but labelled by the y_mapped values
        :param y: long sequence of y_values along original y axis
        :param y_mapped: corresponding transformed y_values for new y_ticks
            len(y_mapped) == len(y)
            y and y_mapped monotonically increasing
        :param y_label: label of second y-axis
        :param fontsize: (optional) fontsize of y_label
        :return: None
        """
        ax2 = self.ax.twinx()
        ax2.set_ylim(self.ax.get_ylim())
        ymap_ticks = _nice_ticks(np.amin(y_mapped), np.amax(y_mapped))
        # = uniform ticks in y_mapped scale
        ymap_ticklabels = [f'{tick:.1f}' for tick in ymap_ticks]
        y_ticks = np.interp(ymap_ticks, y_mapped, y)
        # = transformed to corresponding y scale positions
        ax2.set_yticks(y_ticks)
        ax2.set_yticklabels(ymap_ticklabels)
        ax2.set_ylabel(y_label, fontsize=fontsize)
        self.fig.tight_layout()


class TableRef:
    """Reference to a single table instance,
    formatted in LaTeX OR plain tabulated txt versions
    """
    def __init__(self, text=None, name=None, path=None):
        """
        :param text: single string with all table text incl. newline, tab chars.
        :param path: (optional) Path to directory where tables are saved
        :param name: (optional) updated file name, with or without suffix
            suffix is determined by FMT['table_format'] anyway
        """
        # store table parts instead *****???
        self.text = text
        self.name = name
        self.path = path

    def __repr__(self):
        return (f'TableRef(text= text, ' +    # fmt= {repr(self.fmt)}, ' +
                f'name= {repr(self.name)}), path= {repr(self.path)}')

    def save(self, path, name=None):
        """Save table to file.
        :param path: Path to directory where tables are saved
        :param name: (optional) updated file name, with or without suffix
            suffix is determined by FMT['table_format'] anyway
        :return: None
        Result: updated properties path, name
        """
        if name is None:
            name = self.name
        name = _clean_file_name(name)
        path.mkdir(parents=True, exist_ok=True)   # just in case
        f = (path / name).with_suffix(TABLE_FILE_SUFFIX[FMT['table_format']])
        if self.text is not None and len(self.text) > 0:
            f.write_text(self.text, encoding='utf-8')
        self.path = path
        self.name = f.name


# ------------------------------------------------ plot routines

def fig_log_likelihood(learned_ll, n_users,
                       title='',
                       # label=None,
                       fontsize=14,
                       name=None,
                       **kwargs):
    """plot VI learning result
    :param learned_ll = list log-likelihood values from a learned ItemResponseModel
    :param n_users = scalar number of users included in the total log-likelihood
    :param title = (optional) figure title
    :param name = (optional) figure name for file
    :param fontsize = (optional) font size for axis labels
    :param kwargs = (optional) dict with any additional arguments for plot function
    :return: None
    """
    f_logprob, ax = plt.subplots()
    t1 = 1
    # for ll in learned_ll:
    t = [t1 + n for n in range(len(learned_ll))]
    # n_train = ham.n_training_users
    ax.plot(t, np.array(learned_ll) / n_users, **kwargs)
    # t1 = t[-1] + 1
    ax.set_xlim(0, t[-1]+1)
    ax.set_xlabel('Learning Iterations', fontsize=fontsize)
    ax.set_ylabel('Log-likelihood / N', fontsize=fontsize)
    if 0 < len(title):
        ax.set_title(title)
    return FigureRef(ax, name=name)


def fig_response_freq(count, name=None, fontsize=14):
    """Generate a plot with relative frequencies of response counts for all items
    :param count: list of Counter objects  *** dict ?
        count[i][0] = number of missing responses for i-th item
        count[i][l] = number of responses in l-th ordinal level for i-th item
    :param fontsize = (optional) font size for axis labels
    :return: figure object *** FigureRef object ???
    """
    fig, ax = plt.subplots()
    for (i, (c, col, (m, fill_style))) in enumerate(zip(count,  # total_count,
                                                        cycle(FMT['colors']),
                                                        cycle(product(FMT['markers'],
                                                                      FMT['fillstyle'])))):
        x_i = np.arange(1 + max(*c.keys()))  # key = 0 means missing data
        y_i = np.array([c[r] for r in x_i])
        y_i = y_i / np.sum(y_i)
        y_i *= 100  # in percent
        ax.plot(x_i, y_i, label = f'Q{i+1}', color=col,
                marker=m, fillstyle=fill_style)
    ax.set_xticks(np.arange(0, 6))
    ax.set_xticklabels(['Missing'] + [f'R={i+1}' for i in range(5)])
    ax.set_xlabel('Item Response', fontsize=fontsize)
    ax.set_ylabel('Rel. Frequency (%)', fontsize=fontsize)
    ax.legend(loc='best')
    return FigureRef(ax, name=name)


def fig_response_prob(t, p,
                      tau=None,
                      name=None,
                      x_label='',
                      y_label='',
                      fontsize=14
                      ):
    """figure with response prob vs. trait
    :param t: 1D array with trait values
    :param p: 2D array with response probabilities
        p[n, l] = P{l-th response | t[n]}
    :param tau: (optional) 1D array with trait thresholds
    :param name: (optional) string for plot file name
    :param x_label: string for x-axis label
    :param y_label: string for y-axis label
    :param fontsize: (optional) fontsize for x_ and y_label
    :return: FigureRef object
    """
    fig, ax = plt.subplots()
    for (l, (p_l, c, ls)) in enumerate(zip(p.T,
                                           cycle(FMT['colors']),
                                           cycle(FMT['line_styles']))):
        ax.plot(t, p_l, color=c, linestyle=ls, label=f'R={1+l}')
    if tau is not None:
        # plot ticks at thresholds
        x = [tau, tau]
        y = [np.zeros(len(tau)), 0.1 * np.ones(len(tau))]
        ax.plot(x, y, color='k', linewidth=1., linestyle='solid')
    ax.set_ylim(0., 1.)
    ax.set_xlabel(x_label, fontsize=fontsize)
    ax.set_ylabel(y_label, fontsize=fontsize)
    ax.legend(loc='best')
    return FigureRef(ax, name=name)


def fig_percentiles(perc,
                    y_label,
                    x_ticklabels,
                    case_labels=None,
                    x_label=None,
                    x_offset=0.1,
                    x_space=0.5,
                    fontsize=14,
                    name=None,
                    **kwargs):
    """create a figure with trait percentile results
    :param perc: 3D (or 2D) array with trait percentiles
        perc[c, p, t] = p-th percentile of t-th variable for c-th case
        percentiles plotted vertically vs t-variables horizontally,
    :param y_label: string for y axis label
    :param x_label: string for x-axis label
    :param x_ticklabels: list of strings with labels for x_ticks,
        one for each value in rows perc[..., :]
        len(x_ticklabels) == perc.shape[-1] == number of traits
    :param case_labels: list of strings with labels for cases, if more than one
        len(case_labels) == perc.shape[0] if perc.ndim == 3
    :param x_offset: (optional) horizontal space between case plots for each x_tick
    :param x_space: (optional) min space outside min and max x_tick values
    :param fontsize: (optional) fontsize for x and theta labels
    :param kwargs: (optional) dict with any additional keyword arguments for plot commands.
    :return: None  # fig object with single plot axis with all results
    """
    fig, ax = plt.subplots()
    if perc.ndim == 2:
        perc = perc[np.newaxis,...]
        case_labels = [None]
    (n_cases, n_perc, n_xticks) = perc.shape
    x = np.arange(0., n_xticks) - x_offset * (n_cases - 1) / 2
    for (c_key, c_y, c, (m, fs)) in zip(case_labels, perc,
                                      cycle(FMT['colors']),
                                      cycle(product(FMT['markers'],
                                                    FMT['fillstyle']))):
        ax.plot(np.tile(x, (2, 1)), c_y[[0, 2], :],
                linestyle='solid', color=c, **kwargs)
        ax.plot(x, c_y[1, :], linestyle='', color=c,
                marker=m, fillstyle=fs,  # markeredgecolor=c,  # markerfacecolor='w',
                label=c_key, **kwargs)
        x += x_offset
    (x_min, x_max) = ax.get_xlim()
    x_min = min(x_min, -x_space)
    x_max = max(x_max, n_xticks - 1 + x_space)
    ax.set_xlim(x_min, x_max)
    ax.set_xticks(np.arange(n_xticks))
    ax.set_xticklabels(x_ticklabels)
    ax.set_ylabel(y_label, fontsize=fontsize)  # + ' (' + y_unit + ')')
    ax.set_xlabel(x_label, fontsize=fontsize)
    if n_cases > 1:
        # make space for legend
        (x_min, x_max) = ax.get_xlim()
        ax.set_xlim(x_min, x_max + 0.6)
        ax.legend(loc='best')
    if name is None:
        name = _clean_file_name(y_label)
    return FigureRef(ax, name=name)


def fig_credible_diff(c_diff,
                      x_labels,
                      x_label=None,
                      title=None,
                      cred_levels=None,
                      fontsize=10
                      ):
    """Nice color plot to show jointly credible differences
    :param c_diff: list of tuples ((i, j), p), indicating that
        x_labels[i] > x-labels[j] with joint credibility p
    :param x_labels: list of labels of compared categories
    :param x_label: (optional) axis label
    :param title: (optional) string with plot title
    :param cred_levels: (optional) list of joint-credibility values, in DECREASING order
    :param fontsize: (optional) fontsize for x_labels in plot
    :return:
    """
    if cred_levels is None:
        cred_levels = [.99, .95, .9, .8, .7]
    marker_sizes = [15, 12, 9, 6, 3]

    cred_levels = np.asarray(cred_levels)
    symbol_size = None  # use previous size to detect change

    # ------------------------------------------------
    def select_symbol(p, prev_size):
        """Determine symbol size and legend text
        """
        i_size = np.nonzero(cred_levels < p)[0][0]
        size = marker_sizes[i_size]
        if size != prev_size:
            return size, f'> {cred_levels[i_size]:.0%}'
        else:
            return size, None
    # ------------------------------------------------

    fig, ax = plt.subplots()
    for ((i, j), p) in c_diff:
        symbol_size, label = select_symbol(p, symbol_size)
        if symbol_size > 0:
            s, = ax.plot(i, len(x_labels) - 1 - j, 'sr', markersize=symbol_size)
            if label is not None:
                s.set_label(label)
    ax.set_xlim([-0.5, len(x_labels) - 0.5])
    ax.set_ylim([-0.5, len(x_labels) - 0.5])
    ax.set_xticks(np.arange(len(x_labels)))
    ax.set_yticks(np.arange(len(x_labels)))
    ax.set_xticklabels(x_labels,
                       fontsize=fontsize,
                       **_x_tick_style(x_labels) )
    ax.set_yticklabels(x_labels[::-1],  # reversed order
                       fontsize=fontsize,
                       rotation='horizontal',
                       horizontalalignment='right'
                       )
    if x_label is not None:
        ax.set_xlabel(x_label, fontsize=fontsize + 4)
        ax.set_ylabel(x_label, fontsize=fontsize + 4)
    ax.set_title(title)
    if len(c_diff) > 0:
        ax.legend(loc='best')
    fig.tight_layout()
    return FigureRef(ax)


# --------------------------------------- Table formatting functions
def tab_correlation_matrix(cov, item_trait_map, name=None):
    """Normalized correlation matrix between IRT traits corresponding to items.
    :param cov: estimated, possibly un-normalized, covariance matrix,
        possibly including traits that have NO item correspondence
    :param item_trait_map: 2D boolean array mapping trait to item
        item_trait_map[i, t] == True <=> t-th trait determines i-th item response
    :param name: (optional) string file name of table
    :return: string with tabulated correlation values by trait = IOI-HA item
    """
    if name is None:
        name = 'Corr'
    trait_sel = np.any(item_trait_map, axis=0)
    c = cov[:, trait_sel][trait_sel, :]
    std = np.sqrt(np.diag(c))
    # Normalize covariance matrix
    c /= std
    c /= std[:, None]
    n_traits = c.shape[0]
    trait_labels = _make_trait_labels(item_trait_map)
    # *** use externally defined trait labels? ******
    align = 'r | ' + (n_traits-1) * 'r '
    header = ['Trait'] + trait_labels[1:]
    rows = []
    for i in range(n_traits-1):
        rows += [[trait_labels[i]] + i * [' '] + [f'{c[i, j]:.3f}'
                                                  for j in range(i+1, n_traits)]]
    return TableRef(_make_table(header, rows, align), name=name)


def tab_credible_diff(diff,
                      x_labels,
                      x_label='Population'):
    """create table with credible trait differences between populations
    represented by included group data sets
    :param diff: list of tuples ((i, j), p), indicating that
        x_labels[i] > x-labels[j] with joint credibility p, meaning
        prob{ x_labels[i] > s_labels[j] } AND all previous pairs } == p
    :param x_labels: list of category labels of compared data
    :param x_label: label of category for the difference
    :return: TableRef object with header lines + one line for each credible difference,
    """
    if len(diff) == 0:
        return None
    align = 'l l c l r'
    h = ['', x_label, '$>$', x_label, FMT['credibility']]
    rows = []
    col_0 = ''
    # ((i,j), p) = diff[0]  # separate format for first line
    for ((i, j), p) in diff:
        rows.append([col_0, x_labels[i], '$>$', x_labels[j], f'{100*p:.1f}\%'])
        col_0 = 'AND' # for all except first row
    return TableRef(_make_table(h, rows, align))


# ------------------------------------------ internal help functions:
def _nice_ticks(y_min, y_max):
    """Make nice sequence of equally spaced ticks
    with at most one decimal
    :param y_min: scalar axis min
    :param y_max: scalar axis max
    :return: t = array with tick values
        all(y_min <= t <= y_max
    """
    d = y_max - y_min
    if d < 1.:
        step = 0.1
    elif d < 2.:
        step = 0.2
    elif d < 5.:
        step = 0.5
    else:
        step = 1.
    return np.arange(np.ceil(y_min / step), np.floor(y_max / step) + 1) * step


def _x_tick_style(labels):
    """Select xtick properties to avoid tick-label clutter
    :param labels: list of tick label strings
    :return: dict with keyword arguments for set_xticklabels
    """
    maxL = max(len(l) for l in labels)
    rotate_x_label = maxL * len(labels) > 60
    if rotate_x_label:
         style = dict(rotation=25, horizontalalignment='right')
    else:
        style = dict(rotation='horizontal', horizontalalignment='center')
    # if len(labels) > 20:
    #     style['fontsize'] = 8
    # else:
    #     style['fontsize'] = 10
    return style


table_begin = {'latex': lambda align: '\\begin{tabular}{' + align + '}\n',
               'tab': lambda align: ''}
table_head_sep = {'latex':'\hline\n',
                  'tab':''}
table_cell_sep = {'latex': ' & ',
                  'tab':' \t '}
table_row_sep = {'latex': '\\\\ \n',
                 'tab': '\n'}
table_end = {'latex':'\hline\n\end{tabular}',
             'tab': ''}


def _make_table(header, rows, col_alignment):
    """Generate a string with table text.
    :param header: list with one string for each table column
    :param rows: list of rows, where
        each row is a list of string objects for each column in this row
    :param col_alignment: list of alignment symbols, l, r, or c
        len(col_alignment) == len(header) == len(row), for every row in rows
    :return: single string with complete table
    """
    def make_row(cells, fmt):
        return table_cell_sep[fmt].join(f'{c}' for c in cells) + table_row_sep[fmt]
    # ------------------------------------------------------------------------

    fmt = FMT['table_format']  # module global constant
    t = table_begin[fmt](col_alignment)
    t += table_head_sep[fmt]
    t += make_row(header, fmt)
    t += table_head_sep[fmt]
    t += ''.join((make_row(r, fmt) for r in rows))
    t += table_end[fmt]
    return t


def _make_trait_labels(item_trait_map):
    """Prepare trait labels for plots and tables
    :param item_trait_map: 2D boolean array mapping trait for each item
    :return: list of strings
    """
    # *** should be done externally ? ***
    trait_sel = np.any(item_trait_map, axis=0)
    item_trait_map = item_trait_map[:, trait_sel]
    n_items = len(item_trait_map)
    t_items = [np.arange(1, n_items + 1, dtype=int)[t_i]
               for t_i in item_trait_map.T]
    return ['Q(' + ','.join(f'{i}' for i in t_i) + ')'
            for t_i in t_items]


def _clean_file_name(s):
    """Make a string that can be used as file name
    :param s: string
    :return: clean_s,
        with whitespace replaced by _,
        and not-allowed chars removed
    """
    clean_s = s.replace(' ', '_')
    return clean_s.translate({ord(c): None for c in '(),.'})


# ------------------------------------------------------
if __name__ == '__main__':
    print(_clean_file_name('asd asdf. (asdf), asdf'))