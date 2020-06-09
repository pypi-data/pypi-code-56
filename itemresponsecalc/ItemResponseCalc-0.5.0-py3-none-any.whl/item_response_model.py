"""This module implements a Bayesian model of subjects' responses
to items in a questionnaire, using the Graded Response Model of Item Response Theory.

*** Main Classes:

OrdinalItemResponseModel, defining a complete Bayesian model with all parameters
    adapted to a data set with individual responses to each item in a questionnaire.
    obtained from subjects in one or more different groups.

*** Usage Example: see template script run_irt.py


*** Reference:
Leijon, Kramer et al.:
Analysis of Data from the International Outcome Inventory for Hearing Aids (IOI-HA)
using Bayesian Item Response Theory. 2019, Manuscript in preparation.

Arne Leijon, 2019-07-08, first functional version
2019-07-23, set Initial Trait Scale only here,
    for use by both item_scale and item_respondent initialization
2019-08-15, trying new initialization method, no boolean item_trait_map input
2019-08-16, max_hours limit for learn
2019-08-21, using Pool multi-processing for learn
"""
# **** allow string item_id ? *********************
# **** allow string trait_id ? *********************

import numpy as np
import datetime as dt

from collections import Counter

from .item_respondents import ResponseGroup
from .item_trait_selector import TraitProb
from .item_scale import make_scales
from .trait_precision import prior_precision_within, prior_precision_among
from .ir_predictive import GaussianGivenParam

from multiprocessing.pool import Pool
import os

import logging

logger = logging.getLogger(__name__)
# logger.setLevel(logging.INFO)
# logger.setLevel(logging.DEBUG)  # test

# ----------------------------------------------
__version__ = '2020-06-06'

INITIAL_TRAIT_SCALE = 3.  # larger? ***********
# = crude assumed initial scale of model trait values
# ----------------------------------------------


usePool = True
# usePool = False # for TEST


def _pool_size(n):
    """Estimate number of Pool sub-processes
    :param n: total number of independent jobs to share between processes
    :return: n_processes
    """
    # NOTE: cpu_count() returns n of LOGICAL cpu cores.
    return min(os.cpu_count(), n)


# ---------------------------------------------- Main class:
class OrdinalItemResponseModel:
    """A Bayesian IRT model for discrete ORDINAL rating data,
    available as INDIVIDUAL results in a 2D array R with elements
    R[s, i] = ordinal integer-coded response by s-th subject to the i-th item.

    The number of response alternatives may differ among items.
    The i-th item has L_i ordinal integer response values.

    NOTE: In most modules of this package,
    the math notation assumes that R[s, i] is an integer in range(L_i),
    i.e., it can have integer values 0, 1,..., L_i-1.

    However, in the input data files,
    the recorded responses are usually coded as values 1, 2,..., L_i,
    with missing values encoded as zero.
    This response notation is used in module item_response_data.

    All model parameters are treated as random variables.
    The main parameter distributions are represented by equally probable samples.

    This package uses the Graded Response Model (Samejima, 1969, 1997):
    Each rating R_si is assumed to be determined by ONE latent random Trait variable
    Y_st = a real-valued random variable in the range (-inf, inf).
    There may be one or more separate trait variables,
    each determining the responses to one or more items.

    IF the i-th item is associated with the t-th trait,
    the latent variable Y_st is assumed to determine the response R_si as
    a_{i, l} < Y_st <= a_{i, l+1} => R_si = l,
    where the response thresholds are defined in
    an array (a_k0, ..., a_kL) with strictly increasing elements, and
    a_k0 = -inf; a_kL = +inf

    The latent random variable Y_st has a logistic distribution
    with location theta_st = a subject-specific TRAIT variable,
    for the t-th trait of the s-th subject.

    The trait (location) parameters represent
    the individual performance measures to be estimated.

    The response thresholds are represented by
    an item_scale.OrdinalItemScale object for each item,
    adapted to the distribution of responses from all subjects.

    Each item response is modelled as determined by ONE trait variable,
    identified by an item_trait_selector.TraitSelector object
    connected as a property of each item scale object.
    The association between traits and items is automatically
    estimated by the learning procedure.

    The scale of model parameters is arbitrary, assigned as follows:
    The scale of the latent variable is unity during model estimation.
    However, after learning, all model parameters may be re-scaled jointly,
    such that the predicted global variance is unity for all traits.

    The model is implemented by main properties
    groups = a list with one item_respondents.RespondentGroup instance for each group of subjects.
        Each group model includes all responses for each subject.
    scales = a list of item_scale.OrdinalItemScale objects,
        each defining rating intervals for the mapping
        from latent interval-scale values to ordinal ratings.
        Each scale object has its own item_trait_selector.TraitSelector object,
        defining the association between traits and the item.
    trait_prob = an item_trait_selector.TraitProb object,
        representing the overall probability for each trait to be used for each item.
    precision_within = a trait_precision.TraitPrecisionWithinGroup object, representing
        a Wishart distribution of the intra-group precision of trait vectors theta.
    precision_among = a trait_precision.TraitPrecisionAmongGroups object, representing
        a gamma distribution for the precision of mean trait vectors between groups.
    """
    @classmethod
    def initialize(cls, data_source,
                   n_traits=None,
                   n_scale_samples=1,
                   n_subject_samples=50,
                   trait_scale=INITIAL_TRAIT_SCALE):
        """Initialize a model crudely from given item response data.
        :param data_source: a single ItemResponseDataSet instance,
            including response data from one or more groups of subjects.
        :param n_traits: (optional) scalar integer max number of effective latent traits
        :param n_scale_samples: (optional) number of samples of scale parameters tau for each item
        :param n_subject_samples: (optional) number of samples of trait parameter theta for each subject
        :param trait_scale: (optional) scalar initially assumed scale of model trait values
        :return: a cls instance, crudely initialized for given data_source
            to be refined later, by method learn

        Method:
        1: Use item response counts to crudely initialize all item scales
        2.1: Initialize groups with individual response data for all items, using scales
        2.2: Use PCA or Factor Analysis (with varimax?) on these item-specific trait variables
        2.3: Transform all item-specific traits to a space with n_traits dimensions.
        3: Initialize precision_within, using data from these groups
        4: Initialize groups with only summary data
        5: Initialize precision_among using data from all groups
        """
        assert len(data_source.groups) > 0, 'Must have at least one group'

        item_response_count = data_source.item_response_count
        # item_response_count[i] = 1D array of response counts for i-th item
        n_items = len(item_response_count)
        if n_traits is None:
            n_traits = n_items

        # ----------------------------------------- initialize scales
        trait_prob = TraitProb.initialize(n_traits)
        logger.debug(f'Prior TraitProb.alpha = {np.array2string(trait_prob.alpha, precision=4)}')
        scales = make_scales(item_response_count,
                             trait_prob,
                             n_scale_samples,
                             trait_scale)
        logger.debug('\n' +
                     '\n'.join(f'Init scales[{i}] mean tau: '
                               + np.array2string(np.mean(sc.tau, axis=0), precision=3)
                               + '; trait_sel.mean= '
                               + np.array2string(sc.trait_sel.mean, precision=2)
                               for (i, sc) in enumerate(scales)))  # ******** do this in scales ********

        # ----------------------------------------- initialize groups with subjects
        groups = [ResponseGroup.initialize_by_item(subject_responses=g_responses,
                                                   scales=scales,
                                                   trait_scale=trait_scale,
                                                   n_samples=n_subject_samples,
                                                   name=g_name)
                  for (g_name, g_responses) in data_source.groups.items()]
        # = groups with individual response data for each item
        # g_responses = iterable yielding subject responses, coded as a 1D list with
        # g_responses[s][i] = integer index of response to i-th item
        trait_cov = np.sum(g.cov_all()
                           for g in groups)
        transform_matrix = _trait_rotation(trait_cov, n_traits)
        for g in groups:
            g.transform_traits(transform_matrix)

        # ----------------------------------------- initialize precision_within
        precision_within = prior_precision_within(n_traits)
        precision_within.adapt((g.mean_cov_theta for g in groups))

        # ----------------------------------------- initialize precision_among
        precision_among = prior_precision_among(n_traits)
        logger.debug(f'prior_precision_among.b= {np.mean(precision_among.b)}')

        return cls(data_source.questionnaire,
                   groups, scales, trait_prob,
                   precision_within, precision_among)

    # --------------------------------------------------------------------
    def __init__(self, questionnaire,
                 groups, scales, trait_prob,
                 precision_within, precision_among):
        """
        :param questionnaire: Questionnaire object with info about the items
        :param groups: list with ResponseGroup elements
        :param scales: list of OrdinalItemScale instances, one for each item
        :param trait_prob: single TraitProb object, prior for all scale.trait_sel objects
        :param precision_within: Wishart distribution object
            representing inter-individual precision matrix
            for subject trait vectors, assumed valid for all subject groups
        :param precision_among: gamma distribution object
            representing inter-group precision (inverse variance)
            for mean trait vectors across groups.
        """
        self.version = __version__
        self.questionnaire = questionnaire
        self.groups = groups
        self.scales = scales
        self.trait_prob = trait_prob
        # self.trait_item_map = trait_item_map
        self.precision_within = precision_within
        self.precision_among = precision_among
        # self.latent_scale = 1.  # scale parameter of logistic latent variable
        # may be changed after learning, by method standardize
        self.log_prob = []

    def __repr__(self):  # **********************************
        return (self.__class__.__name__ + '('
                + f'\n\t questionnaire= {self.questionnaire.__class__.__name__} '
                + f'object with {self.questionnaire.n_items} items,'
                + '\n\t groups= [\n\t\t'
                + ',\n\t\t'.join(f'{g.__class__.__name__}(name={repr(g.name)}, with {g.n_subjects} subjects)'
                                 for g in self.groups) + '],'
                + f'\n\t scales= [{len(self.scales)} item-scale objects],'
                + f'\n\t trait_prob = {self.trait_prob.__class__.__name__} object, '
                + f'mapping items to {self.n_traits} latent traits, '
                + f'\n\t precision_within= {self.precision_within.__class__.__name__} object,'
                + f'\n\t precision_among= {self.precision_among.__class__.__name__} object,'
                + f'\n\t version= {self.version}'
                + ')')

    @property
    def n_groups(self):
        return len(self.groups)

    @property
    def n_subjects(self):
        return sum(g.n_subjects for g in self.groups)

    @property
    def n_items(self):
        return len(self.scales)

    @property
    def n_traits(self):
        return len(self.trait_prob.mean)

    # ------------------------------------------ General VI learn algorithm:
    def learn(self,
              min_iter=10,
              min_step=0.01,
              max_iter=100,
              max_hours=10,
              callback=None):
        """Learn from all observed response data stored in self.groups,
        using Variational Inference (VI).

        This method adapts sampled distributions for all model parameters
        to maximize a lower bound to the total likelihood of the observed data.
        The resulting sequence of lower-bound values is theoretically guaranteed to be non-decreasing,
        but the sampling variability may cause small variations around the non-decreasing trend.
        :param min_iter: (optional) minimum number of learning iterations
        :param min_step: (optional) minimum data log-likelihood improvement,
                 over the latest min_iter iterations,
                 for learning iterations to continue.
        :param max_iter: (optional) maximum number of iterations, regardless of result.
        :param max_hours = (optional) maximal allowed running time, regardless of result.
        :param callback: (optional) function to be called after each iteration step.
            If callable, called as callback(self, log_prob)
            where log_prob == scalar last achieved value of VI lower bound
        :return: log_prob = list of log-likelihood values, one for each iteration.
        Result: updated properties of self
        """
        min_iter = np.max([min_iter, 1])
        end_time = dt.datetime.now() + dt.timedelta(hours=max_hours)
        # last allowed time to start new VI iteration
        log_prob = []
        while (len(log_prob) <= min_iter
               or (log_prob[-1] - log_prob[-1 - min_iter] > min_step
                   and (len(log_prob) < max_iter)
                   and (dt.datetime.now() < end_time))):
            log_prob.append(self.adapt())
            if callable(callback):
                callback(self, log_prob[-1])
            logger.info(f'Done {len(log_prob)} iterations. LL={log_prob[-1]:.1f}')
        self.log_prob = np.array(log_prob)
        return self.log_prob

    def adapt(self):
        """One adaptation step for all parameters
        using all response data stored in self.groups.
        :return: ll = scalar lower bound to data log-likelihood,
            incl. negative contributions for KLdiv re priors
        """
        ll = 0.
        ll += self._adapt_prec()
        ll += self._adapt_scales()
        ll += self._adapt_groups()
        # *** should be done in this order,
        # because prec are used in scales update
        # and prec and scales are used in groups update.
        # All KLdiv calculations must use SAME distributions
        # i.e., the current value AFTER adaptations  *********************** CHECK !!!
        return ll

    def _adapt_scales(self):
        """One adaptation step for all parameters
        using all response data stored in self.groups.
        :return: ll = scalar lower bound to data log-likelihood
        """
        _adapt_args = (self.groups, self.trait_prob)
        if usePool:
            n_pool = _pool_size(len(self.scales))
            ch_size = 1  # *** probably slightly faster than ch_size=2
            logger.debug(f'_adapt_scales Pool: n_pool= {n_pool}, ch_size= {ch_size}')
            with Pool(n_pool) as p:
                self.scales = list(p.imap(_adapt, ((sc, _adapt_args)
                                                   for sc in self.scales),
                                          chunksize=ch_size))
        else:
            self.scales = list(map(_adapt, ((sc, _adapt_args)
                                            for sc in self.scales)))

        for (i, sc) in enumerate(self.scales):
            logger.debug(f'scales[{i}] mean tau: '
                         + np.array2string(np.mean(sc.tau, axis=0),
                                           precision=2, suppress_small=True)
                         + ' trait_sel.mean= '
                         + np.array2string(sc.trait_sel.mean,
                                           precision=4, suppress_small=True))
        sum_r = sum(sc.trait_sel.mean
                    for sc in self.scales)
        logger.debug('TraitProb sum responsibility = '
                     + np.array2string(sum_r, precision=2, suppress_small=True))
        ll = self.trait_prob.adapt(sum_r)
        logger.debug(f'TraitProb.adapted: mean='
                     + np.array2string(self.trait_prob.mean, precision=3, suppress_small=True)
                     + f'; ll= -KLdiv = {ll}')
        # NOTE: scale.trait_sel kl_div must be calculated AFTER TraitProb update
        for sc in self.scales:
            ll -= sc.relative_entropy_re_prior(self.trait_prob)  # incl. both eta and trait_sel
        logger.debug(f'scales ll = {ll:.1f}')
        return ll

    def _adapt_groups(self):
        """One adaptation step for all parameters
        using all response data stored in self.groups.
        :return: ll = scalar lower bound to data log-likelihood
        """
        adapt_args = (self.scales, self.precision_within, self.precision_among)
        if usePool:
            n_pool = _pool_size(len(self.groups))
            ch_size = 1
            logger.debug(f'_adapt_groups Pool: n_pool= {n_pool}, ch_size= {ch_size}')
            with Pool(n_pool) as p:
                self.groups = list(p.imap(_adapt, ((g, adapt_args)
                                                   for g in self.groups),
                                          chunksize=ch_size))
        else:
            logger.debug(f'_adapt_groups map, NoPool')
            self.groups = list(map(_adapt, ((g, adapt_args)
                                            for g in self.groups)))

        for g in self.groups:
            logger.debug(f'group {repr(g.name)}: mu.loc= '
                         + np.array2string(g.mu.loc, precision=3, suppress_small=True)
                         + f'; ll={g.ll:.2f}')
        ll = sum(g.ll for g in self.groups)
        return ll

    def _adapt_prec(self):
        """One adaptation step for all parameters
        using all response data stored in self.groups.
        :return: ll = scalar lower bound to data log-likelihood
        """
        ll = self.precision_within.adapt((g.mean_cov_theta
                                          for g in self.groups))
        logger.debug('within-groups var= '
                     + np.array2string(np.diag(self.precision_within.mean_inv),
                                       precision=3))
        ll += self.precision_among.adapt([g.mu.mean2
                                          for g in self.groups])
        logger.debug('among-groups var= '
                     + np.array2string(self.precision_among.mean_inv,
                                       precision=3))
        logger.debug(f'prec ll = {ll:.1f}')
        return ll

    # ------------------------------------------------------- Result Display Functions:

    def item_trait_map(self):
        """Mapping with ONE trait corresponding to each item
        :return: itp = 2D boolean array
            itp[i, t] == True <=> i-th item responses were determined by t-th trait
        """
        return np.array([sc.trait_sel.mean > 0.5 for sc in self.scales])

    def prune(self):
        """Reduce model complexity by deleting any latent trait variables
        that did not correspond to any item
        :return: None
        Result: modified internal model properties
        """
        it_map = self.item_trait_map()
        keep = np.any(it_map, axis=0)
        self.trait_prob.prune(keep)
        self.precision_within.prune(keep)
        self.precision_among.prune(keep)
        for sc in self.scales:
            sc.prune(keep)
        for g in self.groups:
            g.prune(keep)

    def standardize(self):
        """Rescale all model parameters, after learning, such that
        predictive individual trait variance is unity for all traits
        :return: None
        """
        s = np.sqrt(self.predictive_individual_var())
        logger.info(f'Standardizing by factors '
                     + np.array2string(s, precision=3))
        for g in self.groups:
            g.standardize(s)
        self._adapt_prec()
        for sc in self.scales:
            sc.standardize(s)

    # ------------------------------------------------------ Raw Descriptive Data:
    def item_response_count(self):
        """Total frequency of responses at each ordinal level, for each item,
        by subjects in each included group.
        :return: dict with elements (group_key, g_count), where
            g_count is a list of collections.Counter objects,
            g_count[i][r] = number of responses == r for i-th item,
            with r==0 indicating missing response, and
            r = 1, ..., L_i are actual responses.
        """
        return {g.name: [Counter(sr_i)
                         for sr_i in g.subject_responses]
                for g in self.groups}

    # ------------------------------------------------------ Predictive Models:
    def predictive_individual_var(self):
        return np.diag(self.predictive_individual_cov())

    def predictive_individual_cov(self):
        """Covariance of the zero-mean Predictive distribution of IRT traits
        for a RANDOM INDIVIDUAL in any not yet seen future population,
        similar to the sub-populations represented by the included subject groups.
        :return: 2D array with covariance matrix

        Method: The exact predictive distribution is a continuous mixture
        of Student-t distributions.
        Samples from the exact distribution can be generated,
        but it may be sufficient to know the exact covariance
        derived from self.precision_within and self.precision_among
        """
        n_g = self.n_groups
        if n_g <= 1:
            logger.warning(f'Uncertain predictive distribution with only {n_g} groups')
        return (self.precision_within.mean_inv
                + self.precision_among.mean_inv * np.eye(self.n_traits))

    # def predictive_mean(self):
    #     """Predictive distribution of MEAN IRT traits
    #     in any not yet seen future population, similar to any of the sub-populations
    #     represented by the included groups of subjects.
    #     :return: PredictiveTrait instance
    #     """
    #     return GaussianGivenParam(mu=np.zeros(self.n_traits),
    #                               tau=self.precision_among)

    def predictive_individual(self):
        """Sampled Predictive distribution of IRT traits for a RANDOM INDIVIDUAL
        in ANY not yet seen future population, similar to any of the sub-populations
        represented by the included groups of subjects.
        :return: single ir_predictive.GaussianGivenParam object

        Method: the mean of the distribution is a zero-mean Gaussian random variable,
            with precision = estimated precision among groups.
        """
        return GaussianGivenParam(mu=GaussianGivenParam(mu=np.zeros(self.n_traits),
                                                        tau=self.precision_among),
                                  tau=self.precision_within)

    # ---------------------------------- Descriptive statistics:

    def mean_subject_ratings(self):
        """Mean raw ratings, across items, for each respondent in each group
        NOTE: Only informative: The raw ratings NOT on an interval scale!
        :return: dict with elements (group_key, mean_rating)
            mean_rating[s] = mean rating across items, by s-th subject
        """
        mr = dict()  # space for result
        for g in self.groups:
            try:
                mr[g.name] = g.mean_response()
            except AttributeError:
                pass  # no-name group, should not happen
        return mr

    def mean_scaled_subject_ratings(self):
        """Mean ratings, across items, for each respondent in each group,
        with raw ratings re-encoded on point-estimated interval scale.
        NOTE: Only informative, point-estimates are still discrete.
        :return: dict with elements (group_key, mean_rating)
            mean_rating[s] = mean rating across items, by s-th subject
        """
        s = [np.mean(sc.typical_trait(), axis=0)
             for sc in self.scales]
        # s = point-estimated scale values on common interval scale with mean == 0
        # s[i][r] = value for r-th response to i-th item
        return {g.name: np.mean(g.scaled_subject_responses(s), axis=0)
                for g in self.groups}

    def mean_subject_traits(self):
        """Mean latent trait variables in interval-scale domain, range (-inf, +inf),
        for each subject group,
        with equal weight for each item,
        i.e., higher weight if the trait is controlling responses to several items.
        This allows a fair comparison with mean_subject_rating,
        but the trait averaging presumes that separate traits (and items) represent
        measures that make sense to project onto a common uni-dimensional scale.
        :return: dict with elements (group_key, mean_trait), where
            mean_trait = 1D array with individual mean trait values
            mean_trait[s] = mean trait for s-th subject, weighted by item_trait_map
        """
        w = np.sum([sc.trait_sel.mean
                    for sc in self.scales], axis=0)
        w /= np.sum(w)
        # = normalized weight, for fair comparison to raw average rating across items
        return {g.name: np.mean(np.dot(g.theta, w), axis=0)
                for g in self.groups}

    def estim_var_mean_subject_traits(self):
        """Estimation-variance of mean_subject_traits() results,
        used to calculate scale error component of conditional variance given mean rating.
        :return: dict with elements (group_key, estim_var), where
            estim_var = scalar variance estimate for the group
        """
        w = np.sum([sc.trait_sel.mean
                    for sc in self.scales], axis=0)
        w /= np.sum(w)
        # = normalized weight, for fair comparison to raw average rating across items
        # for same weighting as in mean_subject_traits()
        # divide sample variance by n_samples to estimate variance of sample mean
        return {g.name: np.mean(np.var(np.dot(g.theta, w), axis=0)) / g.n_samples
                for g in self.groups}


# ------------------------------ module-internal help functions
def _trait_rotation(c, n_traits):
    """Transformation matrix for trait vectors to (sub-)space
    defined by eigenvectors of cov matrix
    :param c: 2D array with covariance matrix for all initial item-defined traits
        summed across all subjects in all groups
        c.shape == (n_items, n_items)
    :return: proj: 2D projection matrix with orthogonal COLUMN vectors
        proj[:, t] = unit direction vector for t-th trait
        proj.shape == (n_items, n_traits)
        where n_traits <= n_items
        The vectors are scaled such that transformation preserves trait variance
        in the new coordinate system,
        so the initial item scale thresholds should still be reasonably valid.
    """
    (e_val, e_vec) = np.linalg.eigh(c)
    mean_var = np.mean(np.diag(c))
    s = np.sign(e_vec[np.argmax(np.abs(e_vec), axis=0), np.arange(e_vec.shape[1])])
    e_vec *= s
    e_det = np.linalg.det(e_vec)
    proj = e_vec[:, ::-1][:, :n_traits]  # in decreasing e_val order
    new_var = e_val[::-1][:n_traits]  # in same order
    s = np.sqrt(mean_var / new_var)
    # = scale factor to preserve trait variance
    proj *= s
    c_proj = proj.T @ c @ proj  # *** for test, should be diagonal
    return proj
# ---------------------------------------------------------------------


# ------------------------------ help function for Pool multi-tasking:
# used by map or Pool().imap:
def _adapt(task):
    """dispatch call to given object.adapt(...)
    :param task: arguments defining the task:
        task[0] = object whose adapt method is called
        task[1] = positional arguments for adapt method
    :return: returned object from the called adapt method,
        i.e., an updated copy of object task[0]
    """
    # obj = task[0]
    # arg = task[1]
    # logger.debug(f'{obj}.adapt({arg})')
    return task[0].adapt(*task[1])


# ------------------------------ help functions for predictive calculations:
