""" **** NOT USED ****
Module defining probability distribution of rating-interval thresholds for
response categories in an OrdinalItemResponseModel.

*** Main Class:
OrdinalItemScale --- defining response intervals for one item

Method:
In this version, response thresholds are indirectly determined by vector
w = non-normalized width parameters in the logistic-mapped domain.
The prior distribution of w is gamma,
and the posterior is approximated by a set of equally probable sample vectors.

2019-07-xx testing new version using width w directly as parameter
"""

import numpy as np
# from collections import Counter
# from scipy.optimize import line_search
from scipy.stats import norm
from .safe_logistic import logistic

from samppy import hamiltonian_sampler as ham
from samppy.sample_entropy import entropy_nn_approx as entropy

import logging
logger = logging.getLogger(__name__)

# logger.setLevel(logging.INFO)
logger.setLevel(logging.DEBUG)

ham.VECTOR_AXIS = 1  # just in case default has changed...

# ---------------------------- Module Default Constant:
INITIAL_WIDENING = 1.0  # 1.5
# scale expansion factor for interval bounds,
# after initial settings based on response frequencies,
# to account crudely for fixed logistic scale == 1.

#PRIOR_ETA_SCALE = 1.  # 3.
# scale of Gaussian prior distribution of eta parameters
# defining a diffuse prior

PRIOR_ALPHA = 1.01
# = shape parameter of prior gamma distribution of width parameters
PRIOR_ALPHAm1 = PRIOR_ALPHA - 1.  # only this is needed
PRIOR_BETA = 0.1
# = inverse-scale parameter of prior gamma distribution

PSEUDO_COUNT = 0.5
# = Jeffreys prior for Dirichlet distribution of probability vector,
# given response counts


# --------------------------------------------------------------------
class OrdinalItemScale:
    """Class defining response thresholds,
    and learning of defining parameters,
    for ONE item in an OrdinalItemResponseModel.

    Response interval widths in the logistic-transformed domain
    are proportional to 1D array w with only positive values.
    In each adapt step, the posterior distribution of eta
    is approximated by a set of sample vectors, bounded to be positive
    """

    @classmethod
    def initialize(cls, response_count, n_samples=100):
        """Initialize a scale object crudely to agree with given response counts.
        :param response_count: 1D array with total response counts
            response_count[l] = count of response == l
        :param n_samples: (optional) number of samples
        :return: a single cls object
        """
        f = np.cumsum(response_count + PSEUDO_COUNT)
        p_cum = f / f[-1]
        tau = norm.ppf(p_cum[:-1], scale=INITIAL_WIDENING)
        # tau[l] = upper limit of interval for response==l
        cum_w = np.concatenate(([0.], norm.cdf(tau), [1.]))
        w = np.diff(cum_w)
        # eta = np.log(w)
        # # eta[l] = log width in transformed domain for l-th response interval
        # eta = np.tile(eta, (n_samples, 1))

        return cls(np.tile(w, (n_samples, 1)))

    def __init__(self, w):
        """
        :param w: 2D array with interval widths in logistic-transformed domain
            w[n, l] = n-th sample of width for l-th response interval
        """
        # eta -= np.mean(eta, axis=1, keepdims=True)
        # forced to zero mean
        b = [(0., None) for _ in range(w.shape[-1])]
        # restrict all sample values to be positive
        self.sampler = ham.HamiltonianBoundedSampler(fun=neg_logprob,
                                                     jac=d_neg_logprob,
                                                     x=w,
                                                     bounds=b,
                                                     epsilon=0.2,
                                                     n_leapfrog_steps=10)
        # sampler.args to be defined later
        # NOTE: w is stored only as sampler.x

    def __repr__(self):
        return self.__class__.__name__ + f'(w=\n{repr(self.w)})'

    @property
    def w(self):
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
        return _tau(self.w)

    @property
    def typical_trait(self):
        """Crude point estimate of trait parameter, given response,
        estimated at MEDIAN of conditional distribution, given response,
        using current sampled distribution of scale thresholds.
        :return: theta = 2D array, with
            theta[m, l] = m-th sample of typical trait for response == l
            theta.shape[-1] == self.n_response_levels
        """
        cum_w = np.cumsum(self.w, axis=1)
        p = np.concatenate((np.zeros((self.n_samples, 1)), cum_w / cum_w[:, -1:]), axis=1)
        p_mid = (p[:, :-1] + p[:, 1:]) / 2
        return logistic.ppf(p_mid)

    def adapt(self, groups, item_index):
        """One variational-inference update step of sample parameters eta.
        :param groups: dict with elements (group_id, group_model)
            where group_model is a subclass of RespondentGroup object
            that can calculate log-likelihood values for given response thresholds.
        :param item_index: integer index of item with scale defined by self.
        :return: LL = scalar contribution to lower bound to data log-likelihood
        """
        self.sampler.args = (groups, item_index)
        max_steps=20
        try:
            self.sampler.safe_sample(min_steps=5, max_steps=max_steps)
            if self.sampler.n_steps >= max_steps:
                logger.warning(f'Done {self.sampler.n_steps} = MAX allowed sampling steps')
            else:
                logger.debug(f'Done {self.sampler.n_steps} sampling steps')
            if self.sampler.accept_rate > 0.95:  # ****** do this in samppy.safe_sample ********
                self.sampler.epsilon *= 1.3
                logger.debug(f'High sampler accept_rate; increased epsilon = {self.sampler.epsilon}')
        except ham.AcceptanceError:
            logger.warning((f'* AcceptanceError: accept_rate= {self.sampler.accept_rate:.1%} '
                            + f'of {self.sampler.n_trajectories}; '
                            + f'epsilon reduced to {self.sampler.epsilon:.5f}'))
            # ****** keep going anyway ********
        else:
            logger.debug(f'Sampler accept_rate = {self.sampler.accept_rate:.1%}')
            logger.debug(f'Sampler epsilon = {self.sampler.epsilon:.5f}')
        # --------------------------------- DONE distribution of eta
        logger.debug(f'scales[{item_index}] tau percentiles:\n'
                     + np.array2string(np.percentile(self.tau, axis=0, q=[5, 50, 95]),
                                       precision=3))

        # lp = - np.mean(self.sampler.U)
        # the lp part will be included bh RespondentGroup.adapt()
        # so here we contribute only the relative_entropy part
        kl_div = self.relative_entropy_re_prior()
        logger.debug(f'scale[{item_index}]: kl_div={kl_div:.3f}')
        return - kl_div

    def relative_entropy_re_prior(self):
        """KL div(self || prior),
        estimated using current sampled approximation of self.eta
        :return: KL_div = scalar
        Method: E_{self}{ pdf(eta | self) / prior_pdf(eta)}
        """
        return - entropy(self.w) - np.mean(prior_logprob(self.w))


# -------------------------- internal module functions

def neg_logprob(w, groups, item_index):
    """Negative sum of log prob of observed data, given tentative samples.
    :param w: 2D array with tentative sample values
        w[n, l] = n-th sample of l-th width parameter
    :param groups: dict with ref to all response groups
    :param item_index: integer index for this item
    :return: nlp = 1D array
        nlp[n] = negative log-prob for n-th tentative sample
        len(nlp) == w.shape[0]
    """
    # w = np.exp(eta)
    tau = _tau(w)
    lp = sum(g.item_logprob_by_tau(tau, item_index) for g in groups.values())
    if np.any(np.isnan(lp)):
        logger.warning('neg_logprob == nan')
    return - lp - prior_logprob(w)


def d_neg_logprob(w, groups, item_index):
    """Gradient of neg_logprob, given tentative samples.
    :param w: 2D array with tentative sample values
        w[n, l] = n-th sample of l-th width parameter
    :param groups: dict with ref to all response groups
    :param item_index: integer index for this item
    :return: dnlp = 2D array
        dnlp[n, l] = d neg_logprob(w[n]) / d w[n, l]
        dnlp.shape == w.shape
    """
    # w = np.exp(eta)
    tau = _tau(w)
    if np.any(tau == -np.inf) or np.any(tau == np.inf):
        logger.warning('Infinite tau. Should never happen!')
    d_lp_d_tau = sum(g.d_item_logprob_by_tau(tau, item_index) for g in groups.values())
    dlp = np.einsum('mk, mkl -> ml',
                    d_lp_d_tau, _d_tau_dw(w))
    return - dlp - d_prior_logprob(w)


def prior_logprob(w):
    """Prior log pdf of tentative eta array,
    disregarding the normalization constant,
    because the scale parameters are fixed.
    :param w: 2D array of interval-width parameters
        w[n, l] = n-th sample of l-th width
    :return: lp = 1D array,
        lp[n] = log pdf(w[n, :])
        using independent gamma distribution for all elements
    """
    return np.sum(PRIOR_ALPHAm1 * np.log(w) - PRIOR_BETA * w,
                  axis=-1)


def d_prior_logprob(eta):
    """Gradient of prior_logprob for tentative eta array,
    :param eta: 2D array of log interval-width parameters
        eta[n, l] = n-th sample of l-th log-width
    :return: dlp = 2D array,
        dlp[n, l] = d prior_logprob(eta[n,:] / d eta[n, l]
        dlp.shape == eta.shape
    """
    return PRIOR_ALPHAm1 / w - PRIOR_BETA


def _tau(w):
    """Response-interval internal limits, NOT including extremes at -+ inf
    :param w: 2D array of non-normalized interval-width parameters = np.exp(eta)
        w[n, l] = n-th sample of l-th interval non-normalized width in logistic-transformed domain
    :return: t = 2D array with corresponding bounds in the (-inf, inf) range,
        t.shape == (w.shape[0], w.shape[1] - 1)
    """
    # cc = np.cumsum(np.abs(w), axis=1)   # ********** Why abs?
    cc = np.cumsum(w, axis=1)
    return logistic.ppf(cc[:, :-1] / cc[:, -1:])


def _d_tau_dw(w):
    """Jacobian of _tau(w)
    :param w: 2D array of non-normalized interval-width parameters
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


# def _d_tau_d_eta(w):
#     """Jacobian of _tau(w) w.r.t log(w)
#     :param w: 2D array of non-normalized interval-width parameters = np.exp(eta)
#         w[n, l] = proportional to n-th sample of l-th interval width
#         in logistic-transformed domain
#     :return: 3D array dt_d_eta with
#         dt_d_eta[n, l, j] = d _tau[n, l] / d_eta[n, j]
#         dt_d_eta.shape == (w.shape[0], w.shape[1]-1, w.shape[1])
#     2019-07-04, sum(_d_tau_d_eta(w), axis=-1) == 0. as it should
#     """
#     return _d_tau_dw(w) * w[:, None, :]
#

# --------------------------------------------------- TEST:

if __name__ == '__main__':
    # from scipy.optimize import check_grad, approx_fprime
    from scipy.stats import gamma

    g = gamma(a=PRIOR_ALPHA, scale=1. / PRIOR_BETA)
    print(f'prior width range: {g.ppf(0.01):.3f} ... {g.ppf(0.99):.3f}')
    prior_width_ratio = g.ppf(0.99) / g.ppf(0.01)
    print(f'prior gamma width ratio = {prior_width_ratio:.2f}')

    w = np.array([[1., 2., 3., 4., 5.]])
    w = np.concatenate((w, 2*w), axis=0)
    # 2 samples, 5 levels
    print('_d_tau_dw(w)= ', _d_tau_dw(w))

    # dt_d_eta = _d_tau_d_eta(w)
    # print('_d_tau_d_eta(w)= ', dt_d_eta)
    # print('sum dt_d_eta= ', np.sum(dt_d_eta, axis=-1))

    item_sc = OrdinalItemScale.initialize(10 * w[0], n_samples=3)
    print('item_sc= ', item_sc)
    print('item_sc.n_samples=', item_sc.n_samples)
    print('item_sc.n_response_levels=', item_sc.n_response_levels)
    print('item_sc.w=\n', item_sc.w)
    print('item_sc.tau=\n', item_sc.tau)
    print('item_sc.typical_trait=\n', item_sc.typical_trait)

    # ------- neg_loprob gradient tested in test_item_scale
