"""This module defines data structures and functions to display analysis results
given an OrdinalItemResponseModel instance,
learned from one or several data sets with ordinal responses to a questionnaire.

Results are shown as figures and tables.
Figures can be saved in pdf, eps, or other formats, as specified in ir_display_format.
Tables are saved in LaTeX tabular format OR in tab-delimited text files.
Thus, both figures and tables can be easily imported into a LaTeX document
or other word-processing document.

*** Main Class:

ItemResponseDisplaySet = a structured container for all display results
Each display element can be accessed and modified by the user, before saving.

*** Usage Example: see template script run_irt

*** Version History:
2020-06-04, first version for ItemResponseCalc standalone package
"""
# ********** figure comments table comments

import numpy as np
from collections import Counter
from pathlib import Path

import logging

from samppy.credibility import cred_diff

from . import ir_display_format as fmt

# -------- module-global variables, that may be changed by user:
FMT = {'percentiles': [5., 50., 95.],
       'credibility_levels': [.99, .95, .9, .8, .7],  # MAX 5 values
       'population': 'Population',
       'trait': 'Trait',
       'mean': 'Mean',
       'individual': 'Indiv.',
       'equivalent': 'Equivalent',
       'response': 'Response',
       'probability': 'Prob.',
       'rating': 'Rating',
       'global': 'Global',
       'correlation': 'Correlation',
       }
# = dict with format parameters that may be changed by user
# Any other parameters are handled by module ir_display_format

logger = logging.getLogger(__name__)
# logger.setLevel(logging.INFO)
# logger.setLevel(logging.DEBUG)  # test


# ------------------------------------------------------------
def set_format_param(**kwargs):
    """Set / modify format parameters for this module
    :param kwargs: dict with any formatting variables
    :return: None
    """
    other_fmt = dict()
    for (k, v) in kwargs.items():
        k = k.lower()
        if k in FMT:
            FMT[k] = v
        else:
            other_fmt[k] = v
    if len(FMT['credibility_levels']) > 5:
        FMT['credibility_levels'] = FMT['credibility_levels'][:5]
    fmt.set_format_param(**other_fmt)  # all remaining user-defined parameters


# ---------------------------------------------------------- Main Display Classes:
class ItemResponseDisplaySet:
    """Root container for all displays of predictive trait results
    and item properties,
    from one OrdinalItemResponseModel object.
    All display elements can be saved as files within a selected directory three.
    The complete instance can also be serialized and dumped to a single pickle file,
    then re-loaded and re-saved, if any display object needs to be edited.
    """
    def __init__(self,
                 log_likelihood,
                 instrument,
                 traits):
        """
        :param log_likelihood: fmt.FigureRef with log-likelihood plot
        :param instrument: ItemSetDisplay object, showing
            response thresholds, and response_prob plot for each item
        :param traits: TraitDisplay object with predicted trait distribution
            for population mean, and for random individual in population.
            Traits for individual respondents are NOT (yet) displayed.
        """
        self.log_likelihood = log_likelihood
        self.instrument = instrument
        self.traits = traits

    def __repr__(self):
        skip = '\n\t'
        return (self.__class__.__name__ + '(' + skip +
                (',' + skip).join(f'{key}={repr(v)}'
                                  for (key, v) in vars(self).items()) +
                skip + ')')

    def save(self, dir_top):
        """Save all displays in a directory tree
        :param dir_top: Path or string with top directory for all displays
        :return: None
        """
        dir_top = Path(dir_top)  # just in case
        self.log_likelihood.save(dir_top)
        if self.instrument is not None:
            self.instrument.save(dir_top)
        if self.traits is not None:
            self.traits.save(dir_top)

    @classmethod
    def show(cls, irm, mapping_item=-1, **kwargs):
        """Create displays for all results from an Item Response analysis model,
        and store all display elements in a single structured object.
        :param irm: a single learned OrdinalItemResponseModel instance
        :param mapping_item: index of irm.scales for item to be used for
            mapping non-linear mean rating, given scale trait
        :param: kwargs: (optional) any display formatting parameters
        :return: a single cls instance
        """
        set_format_param(**kwargs)
        logger.info(f'Creating displays for {len(irm.groups)} group(s): ' +
                    ', '.join(g.name for g in irm.groups))

        return cls(log_likelihood=fmt.fig_log_likelihood(irm.log_prob,
                                                         irm.n_subjects,
                                                         color='r',
                                                         name='LearnedLL'),
                   instrument=ItemSetDisplay.show(irm),
                   traits=TraitDisplay.show(irm, mapping_item))


class ItemSetDisplay:
    """Container for all displays of item-related properties
    """
    def __init__(self,
                 response_freq,
                 items):
        """
        :param response_freq: FigureRef with relative response frequencies, all items
        :param items: dict with elements (item_id, item_display),
            item_display = ItemDisplay object
        """
        self.response_freq = response_freq
        self.items = items

    def save(self, top_path):
        """
        :param top_path:
        :return: None
        """
        items_path = top_path / 'items'
        if self.response_freq is not None:
            self.response_freq.save(items_path)
        for item in self.items.values():
            item.save(items_path)

    @classmethod
    def show(cls, irm):
        """
        :param irm: OrdinalItemResponseModel instance
        :return: a cls instance
        """
        t_min = min(np.min(s.tau) - 2. * s.latent_scale
                    for s in irm.scales)
        t_max = max(np.max(s.tau) + 2. * s.latent_scale
                    for s in irm.scales)
        t = np.linspace(t_min, t_max, 100)
        # same trait range across all items
        g_count = irm.item_response_count()
        # = dict with list of Counter objects, one for each item
        total_count = [sum((g_c[i] for g_c in g_count.values()), Counter())
                       for i in range(irm.n_items)]
        # *** use item_id instead of item_index ********************
        return cls(response_freq=fmt.fig_response_freq(total_count,
                                                       name='Response_freq'),
                   items={f'Q{scale.item_index + 1}': ItemDisplay.show(scale,
                                                                       count,
                                                                       trait=t)
                          for (scale, count) in zip(irm.scales,
                                                    total_count)})


class ItemDisplay:
    """Container for all displays related to ONE item
    """
    def __init__(self,
                 response_freq=None,
                 response_prob=None,
                 mean_response=None):
        """
        :param response_freq: FigureRef with empirical response freq
        :param response_prob: FigureRef with predicted response prob vs. trait
        :param mean_response: FigureRef with expected response vs. trait
            like "Item Characteristic Curves" in the Rasch tradition.
            (*** and ? empirical response range vs trait ? *****)
            NOTE: NOT valid, as ordinal responses are NOT on interval scale
            SKIPPING this display variant for now...
        """
        self.response_freq = response_freq
        self.response_prob = response_prob
        self.mean_response = mean_response

    def save(self, save_path):
        """
        :param save_path: path where sub-objects are saved
        :return:
        """
        if self.response_freq is not None:
            self.response_freq.save(save_path)
        if self.response_prob is not None:
            self.response_prob.save(save_path)
        if self.mean_response is not None:
            self.mean_response.save(save_path)

    @classmethod
    def show(cls, item_scale, response_count, trait):
        """Generate displays for given item
        :param item_scale: OrdinalItemScale object
        :param response_count: Counter object with response counts
        :param trait: 1D array with dense trait values for plot
        :return: a cls instance
        """
        item_id = f'Q{1+item_scale.item_index}'
        # ***** use item_scale.item_id instead *********************
        tau = np.mean(item_scale.tau, axis=0)
        ord_prob = item_scale.ordinal_prob(trait)
        r_mean = 1. + np.dot(ord_prob, np.arange(item_scale.n_response_levels))
        # response_freq=fmt.fig_response_freq(response_count),
        return cls(response_prob=fmt.fig_response_prob(trait, ord_prob,
                                                       name=item_id + '_prob',
                                                       tau=tau,
                                                       x_label=FMT['trait'],
                                                       y_label=' '.join([FMT['response'],
                                                                         FMT['probability']])
                                                       ))


class TraitDisplay:
    """Container for result displays of predicted trait values
    for all traits and groups,
    with layout depending on number of groups and traits.
    """
    def __init__(self, pop_mean, pop_ind,
                 corr_global=None, corr_within=None,
                 group_diff=None):
        """
        :param pop_mean: FigureRef of population predictive mean traits
        :param pop_ind: FigureRef of population predictive traits for random individual
        :param corr_global: (optional) TableRef with global predictive trait correlations
        :param corr_within: (optional) TableRef with predictive trait correlations
            within populations, i.e., excl. variance between populations.
        :param group_diff: (optional) GroupDiffDisplay object,
            iff we have more than one group (population)
       """
        self.pop_mean = pop_mean
        self.pop_ind = pop_ind
        self.corr_global = corr_global
        self.corr_within = corr_within
        self.group_diff = group_diff

    def save(self, path):
        if self.pop_mean is not None:
            self.pop_mean.save(path)
        if self.pop_ind is not None:
            self.pop_ind.save(path)
        if self.corr_global is not None:
            self.corr_global.save(path)
        if self.corr_within is not None:
            self.corr_within.save(path)
        if self.group_diff is not None:
            for (trait_id, trait_diff) in self.group_diff.items():
                trait_diff.save(path / 'group_diff', name=trait_id)

    @classmethod
    def show(cls, irm, mapping_item=-1):
        """
        :param irm: OrdinalItemResponseModel instance
        :param mapping_item: index of item to be used for non-linear scale mapping
        :return: a cls instance
        """
        def _fig_percentiles(perc, g_labels, t_labels, y_label):
            """Plot trait percentiles vs groups or traits,
            in style depending on n_groups and n_traits
            :param perc: 3D array with percentile trait values
                perc[g, p, t] = p-th percentile of t-th trait in g-th population
            :param g_labels: list of group label strings
                len(g_labels) == perc.shape[0]
            :param t_labels: list of trait label strings
                len[t_labels] == perc.shape[2]
            :param y_label: string with y-axis label
            :param mapping_item: index of irm.scales to be used for mapping
            :return: FigureRef instance
            """
            (n_groups, n_perc, n_traits) = perc.shape
            if n_traits > 1:  # plot perc vs traits, with populations as sub-cases
                f = fmt.fig_percentiles(perc,
                                        x_label=FMT['trait'],
                                        x_ticklabels=t_labels,
                                        case_labels=g_labels,
                                        y_label=y_label,
                                        x_offset=0.07)
            else:  # plot perc vs groups, with traits as sub-cases
                f = fmt.fig_percentiles(perc.transpose(2, 1, 0),
                                        x_label=FMT['population'],
                                        x_ticklabels=g_labels,
                                        case_labels=t_labels,
                                        y_label=y_label,
                                        x_offset=0.07)
            # ax = f.ax
            # make second corresponding scale with expected response ratings
            (y_min, y_max) = f.ax.get_ylim()
            y_min -= 0.1  # **** fix to make more space for legend
            f.ax.set_ylim(y_min, y_max)
            y = np.linspace(y_min, y_max, 100)
            # use mapping_item and its item_id
            y_mapped = 1. + irm.scales[mapping_item].mean_ordinal(y)
            item_id = f'Q{1+irm.scales[mapping_item].item_index}'
            # item_id = irm.scales[mapping_item].item_id
            f.mapped_y_axis(y, y_mapped,
                            y_label=(FMT['equivalent'] + ' ' +
                                     item_id + ' ' +
                                     FMT['rating'])
                            )
            return f
        # -----------------------------------------------------------
        item_trait_map = irm.item_trait_map()
        trait_sel = np.any(item_trait_map, axis=0)
        # = boolean trait index for display, just in case irm has NOT been pruned
        item_trait_map = item_trait_map[:, trait_sel]
        n_traits = np.sum(trait_sel)
        group_labels = [g.name for g in irm.groups]
        group_mean_samples = np.array([g.predictive_mean().rvs(size=10000)[:, trait_sel]
                                       for g in irm.groups])
        group_mean_perc = np.percentile(group_mean_samples,
                                        FMT['percentiles'],
                                        axis=1)
        # group_mean_perc[p, g, t] = p-th percentile for t-th trait in g-th population
        trait_labels = fmt._make_trait_labels(item_trait_map)  # **** done by model?
        pop_mean = _fig_percentiles(group_mean_perc.transpose(1, 0, 2),
                                    group_labels,
                                    trait_labels,
                                    y_label=' '.join([FMT['population'],
                                                      FMT['mean'],
                                                      FMT['trait']])
                                    )
        group_ind = [np.percentile(g.predictive_individual(irm.precision_within).rvs(size=10000)[:, trait_sel],
                                   FMT['percentiles'],
                                   axis=0)
                     for g in irm.groups]
        pop_ind = _fig_percentiles(np.array(group_ind),
                                   group_labels,
                                   trait_labels,
                                   y_label=' '.join([FMT['population'],
                                                     FMT['individual'],
                                                     FMT['trait']])
                                   )

        c_global = None
        c_within = None
        if n_traits > 1:
            if irm.n_groups > 1:
                c_global = fmt.tab_correlation_matrix(irm.predictive_individual_cov(),
                                                      item_trait_map,
                                                      name='_'.join((FMT['trait'],
                                                                     FMT['correlation'],
                                                                     FMT['global'])
                                                                    ))
            c_within = fmt.tab_correlation_matrix(irm.precision_within.mean_inv,
                                                  item_trait_map,
                                                  name='_'.join((FMT['trait'],
                                                                 FMT['correlation'],
                                                                 FMT['population'])
                                                                ))

        g_diff = None
        if irm.n_groups > 1:
            g_diff = {trait_id: GroupDiffDisplay.show(t_samples,
                                                      group_labels)
                      for (trait_id, t_samples) in zip(trait_labels,
                                                       group_mean_samples.transpose(2, 0, 1))
                      }
            if n_traits > 1:
                g_diff['Mean_Trait'] = GroupDiffDisplay.show(np.mean(group_mean_samples,
                                                                     axis=-1),
                                                             group_labels)

        return cls(pop_mean=pop_mean,
                   pop_ind=pop_ind,
                   corr_global=c_global,
                   corr_within=c_within,
                   group_diff=g_diff)


class GroupDiffDisplay:
    """Container for displays showing predictive credible differences
    between populations, for ONE selected trait.
    """
    def __init__(self, fig=None, tab=None):
        """
        :param fig: FigureRef object
        :param tab: TableRef object
        """
        self.fig = fig
        self.tab = tab

    def save(self, path, name):
        """
        :param path: path to directory for saved plots and tables
        :param name: string with file name
        :return: None
        """
        if self.fig is not None:
            self.fig.save(path, name=name)
        if self.tab is not None:
            self.tab.save(path, name=name)

    @classmethod
    def show(cls, group_samples, group_labels):
        """Display credible differences between groups,
        given samples of predictive distribution
        :param group_samples: 2D array with
            group_samples[g, n] = n-th sample of selected trait for g-th group
        :param group_labels: list of string-valued group labels
            len(group_labels) == group_samples.shape[0]
        :return: a cls instance
        """
        # **** Sort groups for decreasing median values *************
        s_ind = np.argsort(np.median(group_samples, axis=1))[::-1]
        g_samples = group_samples[s_ind, :]
        g_labels = [group_labels[i] for i in s_ind]
        diff = cred_diff(g_samples,
                         diff_axis=0, sample_axis=1,
                         p_lim=np.amin(FMT['credibility_levels']))

        fig = fmt.fig_credible_diff(diff,
                                    x_labels=g_labels,
                                    x_label=FMT['population'],
                                    cred_levels=FMT['credibility_levels'])
        tab = fmt.tab_credible_diff(diff,
                                    x_labels=g_labels,
                                    x_label=FMT['population'])
        return cls(fig, tab)
