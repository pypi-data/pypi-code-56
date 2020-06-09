"""Classes to handle mapping between questionnaire items and subjective traits

*** Main Classes:
TraitSelector: Probability distribution of a one-of-D boolean switch array
TraitProb: Distribution of prior probability mass vector for any TraitSelector object
"""
import numpy as np
from scipy.special import gammaln, psi

# ----------------------------------------------------------
PRIOR_TRAIT_CONCENTRATION = 0.001
# = prior concentration parameters for TraitProb Dirichlet distribution


# ----------------------------------------------------------
class TraitSelector:
    """Probability distribution of a one-of-D boolean switch array
    z = (z_1, ..., z_D) with only ONE element z_d == True,
    used as property trait_sel of ONE OrdinalItemScale object
    indicating that responses to this object
    are determined by the the d-th trait.
    """
    def __init__(self, weight):
        """
        :param weight: 1D array with un-normalized probability mass elements
        """
        weight = np.array(weight)
        self.prob = weight / np.sum(weight)

    @property
    def mean(self):  # ******* mean_responsibility!
        return self.prob

    def adapt(self, log_responsibility, prior):
        """Adapt self.prob for given trait responsibility
        :param log_responsibility: 1D array with sum logprob(responses) given each trait
        :param prior: single TraitProb object
        :return: None
        """
        log_r = log_responsibility + prior.mean_log
        log_r -= np.amax(log_r)
        r = np.exp(log_r)
        self.prob = r / np.sum(r)

    def relative_entropy_re_prior(self, prior):
        """KL div = E{ log q(z) / p(z | w) }_{z, w}
        :param prior: single TraitProb object
        :return: scalar KL-div
        Method:
        q(z) = prod_t r_t^{z_t}; p(z | w) = prod_t w_t^{z_t}
        where r = self.prob; w = prior
        """
        eps = np.finfo(float).tiny  # just to prevent log(0.)
        return np.dot(self.prob, np.log(self.prob + eps) - prior.mean_log)

    def prune(self, keep):
        """Prune away un-necessary trait dimensions
        :param keep: 1D boolean array indicating traits to keep
        :return: None
        Result: self.prob reduced, and still normalized
        """
        w = self.prob[keep]
        self.prob = w / np.sum(w)


# ---------------------------------------------------------------------------
class TraitProb:
    """Distribution of hierarchical prior probability mass for all TraitSelector objects,
    modeled as a single Dirichlet distribution.
    """
    @classmethod
    def initialize(cls, n_traits):
        """Create prior trait distribution
        :param n_traits: scalar integer number of traits
        :return: single initialized TraitProb object
        """
        alpha = PRIOR_TRAIT_CONCENTRATION * np.ones(n_traits)
        # ****** decreasing alpha by trait index ???
        return cls(alpha)

    def __init__(self, alpha):
        self.alpha=np.array(alpha)

    def __repr__(self):
        return (self.__class__.__name__
                + '(' + f'alpha= ' + repr(self.alpha) + ')')

    @property
    def mean(self):
        return self.alpha / np.sum(self.alpha)

    @property
    def mean_log(self):
        """E{ log W } where W is random vector represented by self"""
        return psi(self.alpha) - psi(np.sum(self.alpha))

    def adapt(self, sum_resp):
        """adapt from given trait-responsibility sum
        :param sum_resp: sum of trait responsibilities across items
        :return: - kl_div
        """
        self.alpha = sum_resp + self.initialize(len(self.alpha)).alpha
        return - self.relative_entropy_re_prior()

    def relative_entropy_re_prior(self):
        """KL_div = E{ log q(w) / p(w) }_{q(w}), where
        q(w) = self distribution; p(w) = self.initialize
        :return: scalar KL_div
        Method:
        q(w) = C(q_alpha) prod_t w_t^{q_alpha - 1}
        p(w) = C(p_alpha) prod_t w_t^{p_alpha - 1}
        C(alpha) = log(gamma(sum alpha)) - sum log(gamma(alpha))
        """
        p = self.initialize(len(self.alpha))
        # = prior
        kl_div = (np.dot(self.alpha - p.alpha, self.mean_log)
                  + gammaln(np.sum(self.alpha)) - gammaln(np.sum(p.alpha))
                  + np.sum(gammaln(p.alpha) - gammaln(self.alpha)))
        return kl_div

    def prune(self, keep):
        """Prune away un-necessary trait dimensions
        :param keep: 1D boolean array indicating traits to keep
        :return: None
        Result: self.trait_sel pruned
        """
        self.alpha = self.alpha[keep]

