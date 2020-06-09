""" Module defining probability distribution of rating-interval thresholds for
response categories in an OrdinalItemResponseModel,
implementing the IRT Graded Response Model.

*** Main Class:
OrdinalItemScale --- defining response intervals for one item
    represented by IRT Graded Response Model.
    Response intervals are defined by a monotonically increasing
    sequence of response thresholds.

Method:
In this version, response thresholds are indirectly determined by vector
eta = logarithm of non-normalized width parameters in the logistic-mapped domain.
The prior distribution of eta is Gaussian,
and the posterior is approximated by a set of equally probable sample vectors,
or by a single MAP estimate.

To avoid numerical overflow during sampling,
the eta samples are also restricted between (wide) fixed bounds,
so the prior eta distribution is actually a (mildly) truncated Gaussian.

2019-07-08 first version
2019-07-14, used HamiltonianBoundedSampler for numerical safety
2019-07-23, fixed bug in scale.initialize, Initial Trait Scale set externally
2019-08-10, use a TraitSelector object for item-trait mapping
2019-08-16, try uniform TraitSelector initialization
2019-08-24, use np.random.Generator for sampling
2019-08-25, sample_trait and typical_trait assuming Gaussian inter-individual trait distribution
2020-02-06, adapt including initial MAP point estimate for faster(?) sampling
2020-02-13, allow n_samples == 1 in method relative_entropy_re_prior
"""
# **** after testing, include latent_scale as OrdinalItemScale property
# **** allow string item_id ? *********************

import numpy as np
from scipy.stats import norm
from scipy.optimize import minimize

from .safe_logistic import logistic

from samppy import hamiltonian_sampler as ham
from samppy.sample_entropy import entropy_nn_approx as entropy

from .item_trait_selector import TraitSelector

import logging
logger = logging.getLogger(__name__)

# logger.setLevel(logging.INFO)
# logger.setLevel(logging.DEBUG)

ham.VECTOR_AXIS = 1  # just in case default has changed...

# ---------------------------- Module Default Constants:

PRIOR_ETA_SCALE = 3.  # 1.  # 3. ??? *******
# scale of Gaussian prior distribution of eta parameters
# defining a sufficiently diffuse prior

PSEUDO_COUNT = 0.5
# = Jeffreys prior for Dirichlet distribution of probability vector,
# given response counts

RANDOM_G = np.random.default_rng()
# = module-global random generator, Numpy 1.17


# ------------------------------------------- main initialization function:
def make_scales(item_response_count, trait_prob, n_scale_samples, trait_scale):
    """Initialize all item scale objects, and corresponding trait mapping objects.
    :param item_response_count: 1D list of response-count lists
        item_response_count[i][l] = number of responses == l for i-th item
    :param trait_prob: prior TraitProb instance initialized by caller
    :param n_scale_samples: scalar integer number of samples in each scale object
    :param trait_scale: scalar initially assumed scale of model trait values
    :return: scales = list with one OrdinalItemScale object for each item
    """
    scales = [OrdinalItemScale.initialize(count_i,
                                          n_samples=n_scale_samples,
                                          trait_scale=trait_scale,
                                          trait_prob=trait_prob,
                                          item_index=i)
              for (i, count_i) in enumerate(item_response_count)]
    return scales


# --------------------------------------------------------------------
class OrdinalItemScale:
    """Class defining response thresholds,
    and learning of scale parameters,
    for ONE item in an OrdinalItemResponseModel.

    Response interval widths in the logistic-transformed domain
    are proportional to 1D array w, which is represented as
    w = np.exp(eta)
    In each adapt step, the posterior distribution of eta
    is approximated by a set of sample vectors,
    or by a single MAP estimate.
    """
    @classmethod
    def initialize(cls, response_count, trait_scale, n_samples, trait_prob, item_index):
        """Initialize a scale object crudely to agree with given response counts.
        :param response_count: 1D array with total response counts
            response_count[l] = count of response == l
        :param trait_scale: scalar = initial scale of theta distribution
        :param n_samples: number of samples
        :param trait_prob: single prior TraitProb object for all scale.trait_sel objects
        :param item_index: scalar integer item identifier for this scale
        :return: a single cls object
        """
        f = np.cumsum(response_count + PSEUDO_COUNT)
        p_cum = f / f[-1]
        tau = norm.ppf(p_cum[:-1], scale=trait_scale)
        # tau[l] = upper limit of interval for response==l
        cum_w = np.concatenate(([0.], logistic.cdf(tau), [1.]))  # corrected 2019-07-23
        w = np.diff(cum_w)
        eta = np.log(w)
        # eta[l] = log width in transformed domain for l-th response interval
        eta = np.tile(eta, (n_samples, 1))
        return cls(eta, TraitSelector(trait_prob.mean), item_index)

    def __init__(self, eta, trait_sel, item_index):
        """
        :param eta: log interval width in logistic-transformed domain
            eta[n, l] = n-th sample of log-width for l-th response interval
        :param trait_sel: a TraitSelector object for this item
        :param item_index: scalar integer item identifier for this scale
        """
        self.item_index = item_index
        eta -= np.mean(eta, axis=1, keepdims=True)
        # forced to zero mean
        too_small = np.log(0.001)
        too_big = np.log(1000.)
        # => ratio about 1e6 between widest and smallest interval width
        b = [(too_small, too_big) for _ in range(eta.shape[-1])]
        # must restrict sample eta values to avoid numerical overflow
        self.sampler = ham.HamiltonianBoundedSampler(fun=neg_logprob,
                                                     jac=d_neg_logprob,
                                                     x=eta,
                                                     bounds=b,
                                                     epsilon=0.2,
                                                     n_leapfrog_steps=10)
        # sampler.args to be defined later
        # NOTE: eta is stored only as sampler.x
        self.trait_sel = trait_sel

    def __repr__(self):
        return (self.__class__.__name__ + f'(item_index= {self.item_index},'
                + f'\n\teta=\n\t{repr(self.eta)},'
                + f'\n\ttrait_sel= {repr(self.trait_sel)}'
                + ')')

    @property
    def eta(self):
        return self.sampler.x

    @property
    def n_samples(self):
        return self.sampler.x.shape[0]

    @property
    def n_response_levels(self):
        return self.sampler.x.shape[1]

    @property
    def tau(self):
        """Response-thresholds samples representing current distribution.
        :return: 2D array tau, with
            tau[m, l] = m-th sample of UPPER threshold for l-th interval,
            NOT including extreme values at -inf and +inf
            tau.shape[-1] == self.n_response_levels - 1
        """
        return _tau(np.exp(self.eta))

    def typical_trait(self, theta_scale=1.):
        """Point estimates of trait values, given any response,
        estimated at conditional mean within each response interval,
        assuming Gaussian traits with zero mean and scale = theta_scale,
        using current sampled distribution of scale thresholds.
        :param theta_scale: scalar = current (assumed) scale of theta distribution
        :return: theta = 2D array, with
            theta[m, l] = m-th sample of typical trait for response == l
            theta.shape[-1] == self.n_response_levels
        """
        # typ_median = _cond_median(self.tau, scale=theta_scale)
        typ_mean = _cond_mean(self.tau, scale=theta_scale)
        return typ_mean

    def sample_trait(self, r, n_samples, trait_scale=1.):
        """
        Generate samples of possible trait values, given subjects' responses
        :param r: 1D array with integer response indices, origin == 0
            r[s] = l in range(self.n_response_levels
            means s-th subject gave l-th response to this item
        :param n_samples: number of desired samples for each subject
        :param trait_scale: scalar = current (assumed) scale of theta distribution
        :return: th = 2D array of samples
            th[m, s] = m-th sample for s-th subject
        """
        def s_sample(r_s):
            """Sample in transformed (0, 1) range for ONE subject
            :param r_s: scalar integer response by this subject
            :return: 1D array th_s; len(th_s) == n_samples
            """
            if r_s < 0:
                return RANDOM_G.uniform(low=th_limits[0], high=th_limits[-1], size=n_samples)
            else:
                return RANDOM_G.uniform(low=th_limits[r_s], high=th_limits[r_s + 1], size=n_samples)
        # ----------------------------------------------------------------------
        th_limits = np.mean(self.tau, axis=0)
        th_limits = np.concatenate(([np.finfo(float).tiny],
                                    norm.cdf(th_limits, scale=trait_scale), [1.]))
        # tiny lowest limit, because RANDOM.uniform samples in [0, 1),
        # but we allow only samples in (0., 1)
        th = [s_sample(r_s) for r_s in r]
        return norm.ppf(np.array(th).T, scale=trait_scale)

    def ordinal_prob(self, theta):
        """Conditional probability of ordinal responses, given trait value,
        averaged across scale samples
        :param theta: array of trait values
        :return: pr = array of response probabilities
            pr[..., l] = P{response = l | theta[...]}
            = logistic.cdf(theta[...] - tau[l]) - logistic.cdf(theta[...] - tau[l-1])
            pr.shape == (*theta.shape, self.n_response_levels)
        """
        try:
            s = self.latent_scale
        except NameError:
            s = 1.
        t = self.tau - theta[..., np.newaxis, np.newaxis]
        t /= s
        cdf = np.mean(logistic.cdf(t), axis=-2)  # average across samples
        p = np.concatenate((np.zeros((*cdf.shape[:-1], 1)),
                            cdf,
                            np.ones((*cdf.shape[:-1], 1))),
                            axis=-1)
        p = np.diff(p, axis=-1)
        return p

    def mean_ordinal(self, theta):
        """Expected value of ordinal response level, given trait
        :param theta: array of trait values
        :return: r = expected "response" on continuous scale
            r[...] = sum_l l * P{response = l | theta[...]}

        NOTE: Since the ordinal responses are NOT on a linear interval scale,
        it is formally MEANINGLESS to take the mean of ordinal responses.
        Therefore, this result should be used only for illustration purpose,
        with caution about the scale non-linearity.

        Nevertheless, the expectation of ordinal responses
        is sometimes used without hesitation in the Rasch research tradition,
        Ref, e.g.: Wright and Masters (1982), Eq. 5.4.1.
        The expected rating plotted vs individual trait value
        is sometimes called Item Characteristic Curve (ICC).
        """
        return np.dot(self.ordinal_prob(theta), np.arange(self.n_response_levels))

    def rating_from_trait(self, theta):  # *** use mean_ordinal instead **********
        """Calculate mean equivalent continuous-valued "rating",
        in finite interval (- 0.5, n_rating_levels - 0.5)
        corresponding to given latent variable(s), such that
        th = tau[l] -> rating = l + 0.5
        with linear interpolation in the logistic-transformed (0, 1) range.
        :param theta: array-like 1D sequence of trait values in range (-inf, +inf)
        :return: z = rating-transformed values of y
            z.shape == y.shape
        """
        p_theta = logistic.cdf(theta)
        p_tau = logistic.cdf(np.mean(self.tau, axis=0))
        p_tau = np.concatenate(([0.], p_tau, [1.]))
        # = p corresponding to ratings [-0.5, 0.5, ..., n_rating_levels-0.5
        n_tau = len(p_tau)
        rp = np.linspace(-0.5, n_tau - 1.5, n_tau)
        return np.interp(p_theta, p_tau, rp) # + self.min_rating

    def adapt(self, groups, trait_prob):
        """One variational-inference update step of sample parameters eta.
        :param groups: list with ResponseGroup instances
            that can calculate log-likelihood values for given response thresholds.
        :param trait_prob: single TraitProb object, prior for self.trait_sel
        :return: self
            Must call relative_entropy_re_prior later !
        """
        logger.debug(self.__class__.__name__ + f'[{self.item_index}].adapt(...)')
        # ------ adapt trait selector first, with old tau:
        log_trait_resp = sum(np.mean(g.item_logprob_by_tau(self.tau, self.item_index),
                                     axis=0)
                             for g in groups)
        # log_trait_resp[t] = mean logprob given t-th trait
        self.trait_sel.adapt(log_trait_resp, trait_prob)

        # ------ adapt self.eta, to define new self.tau:
        self.sampler.args = (groups, self.item_index, self.trait_sel.mean)
        # ---------- first adjust by point estimate:
        eta_old = np.mean(self.sampler.x, axis=0)
        eta_new = self.adapt_point(eta_old)
        self.sampler.x += eta_new - eta_old
        logger.debug(f'scale[{self.item_index}] point adapted: diff= '
                     + np.array2string(eta_new - eta_old,
                                       precision=2,
                                       suppress_small=True))
        if self.n_samples == 1:
            logger.debug(self.__class__.__name__ + f'[{self.item_index}].adapt(...) MAP finished')
            return self
        # otherwise continue with sampling
        # --------------------------------
        max_steps = 20
        try:
            self.sampler.safe_sample(min_steps=5, max_steps=max_steps)
            if self.sampler.n_steps >= max_steps:
                logger.warning(f'Scale[{self.item_index}] Done {self.sampler.n_steps} = MAX allowed sampling steps')
            else:
                logger.debug(f'Scale[{self.item_index}] Done {self.sampler.n_steps} sampling steps')
            if self.sampler.accept_rate > 0.95:  # ****** do this in samppy.safe_sample ********
                self.sampler.epsilon *= 1.3
                logger.debug(f'Scale[{self.item_index}]: High sampler accept_rate; '
                             + 'increased epsilon = {self.sampler.epsilon}')
        except ham.AcceptanceError:
            logger.warning((f'Scale[{self.item_index}]: AcceptanceError: accept_rate= {self.sampler.accept_rate:.1%} '
                            + f'of {self.sampler.n_trajectories}; '
                            + f'epsilon reduced to {self.sampler.epsilon:.5f}'))
            # ****** keep going anyway ********
        else:
            logger.debug(f'Scale[{self.item_index}]: Sampler accept_rate = {self.sampler.accept_rate:.1%}')
            logger.debug(f'Scale[{self.item_index}]: Sampler epsilon = {self.sampler.epsilon:.5f}')
        self.sampler.x -= np.mean(self.sampler.x, axis=-1, keepdims=True)
        # adding a constant to all eta does not change any thresholds
        # --------------------------------- DONE distribution of eta
        if self.n_samples > 10:
            logger.debug(f'Scale[{self.item_index}]: tau percentiles=\n'
                         + np.array2string(np.percentile(self.tau, axis=0, q=[5, 50, 95]),
                                           precision=3, suppress_small=True))
        # # ------ adapt trait selector AFTER, with new traits:
        # log_trait_resp = sum(np.mean(g.item_logprob_by_tau(self.tau, item_index),
        #                              axis=0)
        #                      for g in groups.values())
        # # log_trait_resp[t] = mean logprob given t-th trait
        # self.trait_sel.adapt(log_trait_resp)
        # # **** self.trait_sel KL_div penalty must be calculated later, after TraitProb update ****
        logger.info(self.__class__.__name__ + f'[{self.item_index}].adapt(...) finished')
        return self

    def adapt_point(self, eta_0):
        """Find single MAP point estimate of eta,
        using same objective functions as sampler
        :param eta_0: 1D vector with start value
        :return: eta = 1D vector with new point estimate
            eta.shape == eta_0.shape == self.n_response_levels
        """
        def neg_logprob_1d(eta, *args):
            """Link to module-global function for 1D input
            :param eta: 1D vector with tentative parameter values
            :param args: tuple with additional arguments
            :return: nlp = scalar = - log p(data | eta)
            """
            return neg_logprob(eta[None, :], *args)[0]

        def d_neg_logprob_1d(eta, *args):
            """Gradient of neg_logprob_1d
            :param eta: 1D vector with tentative parameter values
            :param args: tuple with additional arguments
            :return: d_nlp = gradient vector
                d_nlp[i] = d neg_logprob_1d(eta,...) / d_eta[i]
                d_nlp.shape == eta.shape
            """
            return d_neg_logprob(eta[None, :], *args)[0]
        # --------------------------------------------------------
        res = minimize(neg_logprob_1d, eta_0,
                       jac=d_neg_logprob_1d,
                       args=self.sampler.args,
                       bounds=self.sampler.bounds,
                       tol=1e-4,
                       )
        if res.success:
            return res.x
        else:
            # ERROR exit
            logger.warning(res)  # ****
            return eta_0  # just let sampler do it anyway

    def relative_entropy_re_prior(self, trait_prob):
        """KL div(self || prior),
        estimated using current sampled approximation of self.eta
        AND KL div for current self.trait_sel
        :param trait_prob: single TraitProb object, prior for self.trait_sel
        :return: KL_div = scalar
        Method: E_{self}{ ln pdf(eta | self) / prior_pdf(eta)}
        """
        if self.n_samples == 1:
            h = 0.  # constant fix entropy
        else:
            h = entropy(self.eta)  # sample-estimated entropy
        return (self.trait_sel.relative_entropy_re_prior(trait_prob)
                - h - np.mean(prior_logprob(self.eta)))

    def prune(self, keep):
        """Prune away un-necessary trait dimensions
        :param keep: 1D boolean array indicating traits to keep
        :return: None
        Result: self.trait_sel pruned
        """
        self.trait_sel.prune(keep)

    def standardize(self, ss):
        """Standardize scale by down-scaling with given factor
        :param ss: 1D array with scale factors, one for each trait
        :return: None
        Method: all tau samples to be reduced by s toward zero
            logistic-transform to (0, 1) domain and adjust eta parameters there
        """
        s = np.dot(self.trait_sel.mean, ss)
        # = scalar factor for this item
        tau = self.tau / s
        n_samples = tau.shape[0]
        # tau[m, l] = m-th sample of new upper limit of l-th response interval
        p = logistic.cdf(tau)  # in (0, 1) domain
        p = np.concatenate((np.zeros((n_samples, 1)), p, np.ones((n_samples, 1))),
                           axis=1)
        w = np.diff(p, axis=1)
        # w[m, l] = width parameters in (0, 1) domain
        eta = np.log(w)
        self.latent_scale = 1. / s  # *********************
        # = new eta sample values defining rescaled tau values
        logger.debug(f'Scale[{self.item_index}]: Old mean tau = '
                     + np.array2string(np.mean(self.tau, axis=0),
                                       precision=3, suppress_small=True))
        self.sampler.x = eta
        # just to check for new values:
        logger.debug(f'Scale[{self.item_index}]: Rescaled mean tau = '
                     + np.array2string(np.mean(self.tau, axis=0),
                                       precision=3, suppress_small=True))


# -------------------------- internal module functions

def neg_logprob(eta, groups, item_index, trait_w):
    """Negative sum of log prob of observed data, given tentative samples.
    :param eta: 2D array with tentative sample values
        eta[n, l] = n-th sample of l-th log-width parameter
    :param groups: list with ref to all response groups
    :param item_index: integer index for this item
    :param trait_w: 1D weight vector
        trait_w[t] = weight for t-th trait
    :return: nlp = 1D array
        nlp[n] = negative log-prob for n-th tentative sample
        len(nlp) == eta.shape[0]
    """
    w = np.exp(eta)
    tau = _tau(w)
    lp = sum(g.item_logprob_by_tau(tau, item_index, trait_w)
             for g in groups)
    if np.any(np.isnan(lp)):
        logger.warning('Scale[{self.item_index}]: neg_logprob == nan. *** Should never happen!')
    return - lp - prior_logprob(eta)


def d_neg_logprob(eta, groups, item_index, trait_w):
    """Gradient of neg_logprob, given tentative samples.
    :param eta: 2D array with tentative sample values
        eta[n, l] = n-th sample of l-th log-width parameter
    :param groups: list with ref to all response groups
    :param item_index: integer index for this item
    :param trait_w: 1D weight vector
        trait_w[t] = weight for t-th trait
    :return: dnlp = 2D array
        dnlp[n, l] = d neg_logprob(eta[n]) / d eta[n, l]
        dnlp.shape == eta.shape
    """
    w = np.exp(eta)
    tau = _tau(w)
    if np.any(tau == -np.inf) or np.any(tau == np.inf):
        logger.warning('Scale[{self.item_index}]: Infinite tau. *** Should never happen!')
    d_lp_d_tau = sum(g.d_item_logprob_by_tau(tau, item_index, trait_w)
                     for g in groups)
    dlp = np.einsum('mk, mkl -> ml',
                    d_lp_d_tau, _d_tau_d_eta(w))
    return - dlp - d_prior_logprob(eta)


def prior_logprob(eta):
    """Prior log pdf of tentative eta array,
    disregarding the normalization constant,
    because the scale parameters are fixed.
    :param eta: 2D array of log interval-width parameters
        eta[n, l] = n-th sample of l-th log-width
    :return: lp = 1D array,
        lp[n] = log pdf(eta[n, :])
    """
    return - 0.5 * np.sum((eta / PRIOR_ETA_SCALE)**2, axis=-1)


def d_prior_logprob(eta):
    """Gradient of prior_logprob for tentative eta array,
    :param eta: 2D array of log interval-width parameters
        eta[n, l] = n-th sample of l-th log-width
    :return: dlp = 2D array,
        dlp[n, l] = d prior_logprob(eta[n,:] / d eta[n, l]
        dlp.shape == eta.shape
    """
    return - eta / PRIOR_ETA_SCALE**2


def _tau(w):
    """Response-interval internal limits, NOT including extremes at -+ inf
    :param w: 2D array of non-normalized interval-width parameters = np.exp(eta)
        w[n, l] = n-th sample of l-th interval non-normalized width in logistic-transformed domain
    :return: t = 2D array with corresponding bounds in the (-inf, inf) range,
        t.shape == (w.shape[0], w.shape[1] - 1)
    """
    cc = np.cumsum(w, axis=1)
    return logistic.ppf(cc[:, :-1] / cc[:, -1:])


def _d_tau_dw(w):
    """Jacobian of _tau(w)
    :param w: 2D array of non-normalized interval-width parameters = np.exp(eta)
        w[n, l] = proportional to n-th sample of l-th interval width
        in logistic-transformed domain
    :return: 3D array dt_dw, with
        dt_dw[n, l, j] = d _tau[n, l] / dw[n, j]
        dt_dw.shape == (w.shape[0], w.shape[1]-1, w.shape[1])
    Method:
    t_l = log(w_0 +...+ w_l) - log(w_{l+1} +...+ w_{L-1}); l = 0,..., L-2, any n
    dt_nlj / d w_nj =
        = +1 / (w_0 +...+ w_l); j <= l
        = -1 / (w_{l+1}+...+w_{L-1}); j > l
    2019-07-04 seems OK
    """
    nw = w.shape[1]
    cc = np.cumsum(w, axis=1)
    cc_plus = cc[:, :-1]
    cc_minus = cc[:, -1:] - cc_plus
    mask = np.ones((nw-1, nw))
    dt_dw = (1. / cc_plus[:, :, None] * np.tril(mask, k=0)
             - 1. / cc_minus[:, :, None] * np.triu(mask, k=1))
    return dt_dw


def _d_tau_d_eta(w):
    """Jacobian of _tau(w) w.r.t log(w)
    :param w: 2D array of non-normalized interval-width parameters = np.exp(eta)
        w[n, l] = proportional to n-th sample of l-th interval width
        in logistic-transformed domain
    :return: 3D array dt_d_eta with
        dt_d_eta[n, l, j] = d _tau[n, l] / d_eta[n, j]
        dt_d_eta.shape == (w.shape[0], w.shape[1]-1, w.shape[1])
    2019-07-04, sum(_d_tau_d_eta(w), axis=-1) == 0. as it should
    """
    return _d_tau_dw(w) * w[:, None, :]


def _cond_mean(tau, scale=1.):
    """Conditional means of trait values for each ordinal rating,
    for each rating-interval limits on the latent scale,
    assuming traits are normal-distributed with given scale
    :param tau: 2D array with upper interval limits for rating
        tau[m, l] = m-th sample of upper interval limit for rating == l
        lower limit is - inf for l == 0
        upper limit is + inf for l == n_rating_levels-1
        tau.shape[-1] == n_rating_levels - 1
    :return: theta = 2D array with mean traits
        theta[m, l] = m-th sample of conditional mean trait, given rating=l
        theta.shape == (tau.shape[0], n_rating_levels)
    """
    n_samples = tau.shape[0]
    n_rating_levels = tau.shape[1] + 1
    tau = np.concatenate((np.full((n_samples,1), - np.inf),
                          tau,
                          np.full((n_samples,1), np.inf)), axis=1)
    return np.array([[norm.expect(scale=scale, lb=tau_m[l], ub=tau_m[l+1],
                                  conditional=True)
                      for l in range(n_rating_levels)]
                     for tau_m in tau])


def _cond_median(tau, scale=1.):  # **** not used, but much faster than _cond_mean
    """Conditional medians of trait values for each ordinal rating,
    for each rating-interval limits on the latent scale,
    assuming traits are normal-distributed with given scale
    :param tau: 2D array with upper interval limits for rating
        tau[m, l] = m-th sample of upper interval limit for rating == l
        lower limit is - inf for l == 0
        upper limit is + inf for l == n_rating_levels-1
        tau.shape[-1] == n_rating_levels - 1
    :return: theta = 2D array with median trait values
        theta[m, l] = m-th sample of conditional median trait, given rating = l
        theta.shape == (tau.shape[0], n_rating_levels)
    """
    n_samples = tau.shape[0]
    p = norm.cdf(tau, scale=scale)
    p = np.concatenate((np.zeros((n_samples, 1)),
                        p,
                        np.ones((n_samples, 1))), axis=1)
    p_mid = (p[:, :-1] + p[:, 1:]) / 2
    return norm.ppf(p_mid, scale=scale)


# --------------------------------------------------- TEST:

if __name__ == '__main__':
    from .item_trait_selector import TraitProb

    # from scipy.optimize import check_grad, approx_fprime

    w = np.array([[1., 2.,3.,4.,5.]])
    w = np.concatenate((w, 2*w), axis=0)
    # 2 samples, 5 levels
    print('w =\n', w)
    tau = _tau(w)
    print('tau(w) = \n', tau)
    scale = 1.
    print(f'_cond_mean(tau, scale={scale}) = \n', _cond_mean(tau, scale=scale))
    print(f'_cond_median(tau, scale={scale}) = \n', _cond_median(tau, scale=scale))

    print('_d_tau_dw(w)= ', _d_tau_dw(w))

    dt_d_eta = _d_tau_d_eta(w)
    print('_d_tau_d_eta(w)= ', dt_d_eta)
    print('sum dt_d_eta= ', np.sum(dt_d_eta, axis=-1))

    trait_prob = TraitProb.initialize(5)
    item_sc = OrdinalItemScale.initialize(10 * w[0], n_samples=3, trait_scale=3.,
                                          trait_prob=trait_prob,
                                          item_index=0)
    print('item_sc= ', item_sc)
    print('item_sc.n_samples=', item_sc.n_samples)
    print('item_sc.n_response_levels=', item_sc.n_response_levels)
    print('item_sc.eta=\n', item_sc.eta)
    print('item_sc.tau=\n', item_sc.tau)
    # print('item_sc.typical_trait=\n', item_sc.typical_trait())
    r = [-1, 0, 1, 2, 3, 4]
    print('item_sc.sample_trait=\n', item_sc.sample_trait(r, 5))

    # ------- neg_loprob gradient tested in test_item_scale
