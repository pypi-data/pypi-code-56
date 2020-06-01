"""
Continuous Likelihood Models
=====
This module includes conjugate model classes for contimuous likelihood functions.
"""

import numpy as np
import scipy.stats as st
import logging

from romus._utils import check_fitted, check_input_gt_zero, check_input_state
from romus import _blueprint

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

################################################################################
################################################################################

class GammaExponential(_blueprint.ConjugateModel):
    """
    Gamma Exponential Model

    Prior: Gamma Distribution G(alpha, beta)
    Likelihood: Exponential Distribution E(lamba)
    Parameter of Interest: Rate of Events (lambda)

    Notes
    ----------
    Section 2.7 in  "A Compendium of Conjugate Priors" by Daniel Fink
    """

    def __init__(self, alpha=None, beta=None, *args, **kwargs):
        """
        Initialize the model object.

        Parameters
        ----------
        alpha : float, optional
            shape prior, must be specified in __init__() or fit(), must be > 0
        beta : float, optional
            rate prior, must be specified in __init__() or fit(), must be > 0
        random_state : np.random.RandomState, optional
            numpy object defining the random state to use for sampling, defaults
            to `np.random`

        Returns
        -------
        None
        """

        super(GammaExponential, self).__init__(*args, **kwargs)

        self.alpha = alpha
        self.beta = beta
        self.alpha_s = None
        self.beta_s = None

        check_input_gt_zero(self.alpha, "alpha")
        check_input_gt_zero(self.beta, "beta")

    def _validate_prior_parameters(self, alpha, beta):
        """utility to validate prior parameters"""

        self.alpha = check_input_state(alpha, self.alpha, "alpha")
        self.beta = check_input_state(beta, self.beta, "beta")

        check_input_gt_zero(self.alpha, "alpha")
        check_input_gt_zero(self.beta, "beta")

    def sample_prior(self, num_samples=1, alpha=None, beta=None):
        """
        Sample from the prior.

        Parameters
        ----------
        num_samples : int
            the number of desired samples from the posterior
        alpha : float, optional
            shape prior, must be specified in __init__() or fit(), must be > 0
        beta : float, optional
            rate prior, must be specified in __init__() or fit(), must be > 0

        Returns
        -------
        prior_samples : ndarray
            An array of samples from the prior
        """
        self._validate_prior_parameters(alpha=alpha, beta=beta)

        return self.random_state.gamma(shape=self.alpha, scale=1.0/self.beta,
                                       size=num_samples)

    def sample_prior_predictive(self, num_samples=1, alpha=None, beta=None):
        """
        Sample from the prior predictive.

        Parameters
        ----------
        num_samples : int
            the number of desired samples from the posterior
        alpha : float, optional
            shape prior, must be specified in __init__() or fit(), must be > 0
        beta : float, optional
            rate prior, must be specified in __init__() or fit(), must be > 0

        Returns
        -------
        prior_predictive_samples : ndarray
            An array of samples from the prior
        """
        self._validate_prior_parameters(alpha=alpha, beta=beta)

        # Gamma-Exponential distribution is equivalent to Lomax (Parento II)
        return st.lomax(c=self.alpha, scale=self.beta).rvs(size=num_samples)

    def fit(self, data=None, sum_stats=None, alpha=None, beta=None):
        """
        Fit the model using the prior and available data.

        Parameters
        ----------
        data: ndarray, optional
            nx1 array of the sample data, data OR sum_stats must be specified.
            Defaults to data if both are specified.
        sum_stats: tuple(int, int), optional
            Summary statistics, a tuple representing (num_events, sum_outcomes).
            num_events is the total number of events, must be > 0. sum_outcomes
            is the sum of values over events, must be > 0.
        alpha : float, optional
            shape prior, must be specified in __init__() or fit(), must be > 0
        beta : float, optional
            rate prior, must be specified in __init__() or fit(), must be > 0

        Returns
        -------

        """
        self._validate_prior_parameters(alpha=alpha, beta=beta)

        if data is not None:
            num_events, sum_outcomes = data.shape[0], data.sum()
        elif sum_stats is not None:
            num_events, sum_outcomes = sum_stats
        else:
            raise ValueError("Please specify either data or sum_stats input.")

        self.alpha_s = self.alpha + num_events
        self.beta_s = self.beta + sum_outcomes
        self.fitted = True

        return self.alpha_s, self.beta_s

    @check_fitted
    def sample_posterior(self, num_samples=1):
        """
        Sample from the posterior.

        Parameters
        ----------
        num_samples : int
            the number of desired samples from the posterior

        Returns
        -------
        posterior_samples : ndarray
            An array of samples from the fitted posterior
        """

        return self.random_state.gamma(shape=self.alpha_s,
                                       scale=1.0/self.beta_s, size=num_samples)

    @check_fitted
    def sample_posterior_predictive(self, num_samples=1):
        """
        Sample from the posterior predictive.

        Parameters
        ----------
        num_samples : int
            the number of desired samples from the posterior

        Returns
        -------
        posterior_predictive_samples : ndarray
            An array of samples from the fitted posterior
        """

        # posterior_samples = self.sample_posterior(num_samples=num_samples)
        # return self.random_state.exponential(scale=1.0/posterior_samples)

        # Gamma-Exponential distribution is equivalent to Lomax (Parento II)
        return st.lomax(c=self.alpha_s, scale=self.beta_s).rvs(size=num_samples)

################################################################################
################################################################################

class GammaGamma(_blueprint.ConjugateModel):
    """
    Gamma Gamma Model

    Prior: Gamma Distribution G(alpha, beta)
    Likelihood: Gamma Distribution E(lamba)
    Parameter of Interest: Rate of Events (lambda)

    Equivalent to Gamma Inverse Gamma model if inputs x are transformed into
    1 / x.

    Assumption: Shape of likelihood (alpha) is known

    Notes
    ----------
    Section 2.8 in  "A Compendium of Conjugate Priors" by Daniel Fink
    Section 3.2 in  "A Compendium of Conjugate Priors" by Daniel Fink
    """

    def __init__(self, alpha=None, beta=None, alpha_lik=None, *args, **kwargs):
        """
        Initialize the model object.

        Parameters
        ----------
        alpha : float, optional
            shape prior, must be specified in __init__() or fit(), must be > 0
        beta : float, optional
            rate prior, must be specified in __init__() or fit(), must be > 0
        alpha_lik: float, optional
            known shape parameter of the likelihood distribution,
            must be specified in __init__() or fit(), must be > 0
        random_state : np.random.RandomState, optional
            numpy object defining the random state to use for sampling, defaults
            to `np.random`

        Returns
        -------
        None
        """

        super(GammaGamma, self).__init__(*args, **kwargs)

        self.alpha = alpha
        self.beta = beta
        self.alpha_lik = alpha_lik
        self.alpha_s = None
        self.beta_s = None

        check_input_gt_zero(self.alpha, "alpha")
        check_input_gt_zero(self.beta, "beta")
        check_input_gt_zero(self.alpha_lik, "alpha_lik")

    def _validate_prior_parameters(self, alpha, beta, alpha_lik):
        """utility to validate prior parameters"""

        self.alpha = check_input_state(alpha, self.alpha, "alpha")
        self.beta = check_input_state(beta, self.beta, "beta")
        self.alpha_lik = check_input_state(alpha_lik, self.alpha_lik, "alpha_lik")

        check_input_gt_zero(self.alpha, "alpha")
        check_input_gt_zero(self.beta, "beta")
        check_input_gt_zero(self.alpha_lik, "alpha_lik")

    def sample_prior(self, num_samples=1, alpha=None, beta=None, alpha_lik=None):
        """
        Sample from the prior.

        Parameters
        ----------
        num_samples : int
            the number of desired samples from the posterior
        alpha : float, optional
            shape prior, must be specified in __init__() or fit(), must be > 0
        beta : float, optional
            rate prior, must be specified in __init__() or fit(), must be > 0
        alpha_lik: float, optional
            known shape parameter of the likelihood distribution,
            must be specified in __init__() or fit(), must be > 0

        Returns
        -------
        prior_samples : ndarray
            An array of samples from the prior
        """
        self._validate_prior_parameters(alpha=alpha, beta=beta,
            alpha_lik=alpha_lik)

        return self.random_state.gamma(shape=self.alpha, scale=1.0/self.beta,
                                       size=num_samples)

    def sample_prior_predictive(self, num_samples=1, alpha=None, beta=None, alpha_lik=None):
        """
        Sample from the prior predictive.

        Parameters
        ----------
        num_samples : int
            the number of desired samples from the posterior
        alpha : float, optional
            shape prior, must be specified in __init__() or fit(), must be > 0
        beta : float, optional
            rate prior, must be specified in __init__() or fit(), must be > 0
        alpha_lik: float, optional
            known shape parameter of the likelihood distribution,
            must be specified in __init__() or fit(), must be > 0

        Returns
        -------
        prior_predictive_samples : ndarray
            An array of samples from the prior
        """
        self._validate_prior_parameters(alpha=alpha, beta=beta,
            alpha_lik=alpha_lik)

        prior_samples = self.sample_prior(num_samples=num_samples)
        return self.random_state.gamma(shape=self.alpha_lik,
            scale=1.0/prior_samples)

    def fit(self, data=None, sum_stats=None, alpha=None, beta=None, alpha_lik=None):
        """
        Fit the model using the prior and available data.

        Parameters
        ----------
        data: ndarray, optional
            nx1 array of the sample data, data OR sum_stats must be specified.
            Defaults to data if both are specified.
        sum_stats: tuple(int, int), optional
            Summary statistics, a tuple representing (num_events, sum_outcomes).
            num_events is the total number of events, must be > 0. sum_outcomes
            is the sum of values over events, must be > 0.
        alpha : float, optional
            shape prior, must be specified in __init__() or fit(), must be > 0
        beta : float, optional
            rate prior, must be specified in __init__() or fit(), must be > 0
        alpha_lik: float, optional
            known shape parameter of the likelihood distribution,
            must be specified in __init__() or fit(), must be > 0

        Returns
        -------

        """
        self._validate_prior_parameters(alpha=alpha, beta=beta,
            alpha_lik=alpha_lik)

        if data is not None:
            num_events, sum_outcomes = data.shape[0], data.sum()
        elif sum_stats is not None:
            num_events, sum_outcomes = sum_stats
        else:
            raise ValueError("Please specify either data or sum_stats input.")

        self.alpha_s = self.alpha + num_events * self.alpha_lik
        self.beta_s = self.beta + sum_outcomes
        self.fitted = True

        return self.alpha_s, self.beta_s

    @check_fitted
    def sample_posterior(self, num_samples=1):
        """
        Sample from the posterior.

        Parameters
        ----------
        num_samples : int
            the number of desired samples from the posterior

        Returns
        -------
        posterior_samples : ndarray
            An array of samples from the fitted posterior
        """

        return self.random_state.gamma(shape=self.alpha_s,
                                       scale=1.0/self.beta_s, size=num_samples)

    @check_fitted
    def sample_posterior_predictive(self, num_samples=1):
        """
        Sample from the posterior predictive.

        Parameters
        ----------
        num_samples : int
            the number of desired samples from the posterior

        Returns
        -------
        posterior_predictive_samples : ndarray
            An array of samples from the fitted posterior
        """

        posterior_samples = self.sample_posterior(num_samples=num_samples)
        return self.random_state.gamma(shape=self.alpha_lik,
            scale=1.0/posterior_samples)

################################################################################
################################################################################

class InverseGammaWeibull(_blueprint.ConjugateModel):
    """
    Inverse Gamma Weibull Model

    Prior: Inverse Gamma Distribution G(alpha, beta)
    Likelihood: Weibull Distribution W(k, theta)
    Parameter of Interest: Scale (theta)

    Assumption: the shape parameter of the likelihood is known

    Notes
    ----------
    Section 2.11.1 in  "A Compendium of Conjugate Priors" by Daniel Fink
    """

    def __init__(self, alpha=None, beta=None, k=None, *args, **kwargs):
        """
        Initialize the model object.

        Parameters
        ----------
        alpha : float, optional
            shape prior, must be specified in __init__() or fit(), must be > 0
        beta : float, optional
            rate prior, must be specified in __init__() or fit(), must be > 0
        k: float, optional
            known shape parameter of the likelihood distribution,
            must be specified in __init__() or fit(), must be > 0
        random_state : np.random.RandomState, optional
            numpy object defining the random state to use for sampling, defaults
            to `np.random`

        Returns
        -------
        None
        """

        super(InverseGammaWeibull, self).__init__(*args, **kwargs)

        self.alpha = alpha
        self.beta = beta
        self.k = k
        self.alpha_s = None
        self.beta_s = None

        check_input_gt_zero(self.alpha, "alpha")
        check_input_gt_zero(self.beta, "beta")
        check_input_gt_zero(self.k, "k")

    def _validate_prior_parameters(self, alpha, beta, k):
        """utility to validate prior parameters"""

        self.alpha = check_input_state(alpha, self.alpha, "alpha")
        self.beta = check_input_state(beta, self.beta, "beta")
        self.k = check_input_state(k, self.k, "k")

        check_input_gt_zero(self.alpha, "alpha")
        check_input_gt_zero(self.beta, "beta")
        check_input_gt_zero(self.k, "k")

    def sample_prior(self, num_samples=1, alpha=None, beta=None, k=None):
        """
        Sample from the prior.

        Parameters
        ----------
        num_samples : int
            the number of desired samples from the posterior
        alpha : float, optional
            shape prior, must be specified in __init__() or fit(), must be > 0
        beta : float, optional
            rate prior, must be specified in __init__() or fit(), must be > 0
        k: float, optional
            known shape parameter of the likelihood distribution,
            must be specified in __init__() or fit(), must be > 0

        Returns
        -------
        prior_samples : ndarray
            An array of samples from the prior
        """
        self._validate_prior_parameters(alpha=alpha, beta=beta, k=k)

        dist = st.invgamma(a=self.alpha, scale=self.beta)
        dist.random_state = self.random_state
        return np.power(dist.rvs(size=num_samples), 1.0/self.k)

    def sample_prior_predictive(self, num_samples=1, alpha=None, beta=None, k=None):
        """
        Sample from the prior predictive.

        Parameters
        ----------
        num_samples : int
            the number of desired samples from the posterior
        alpha : float, optional
            shape prior, must be specified in __init__() or fit(), must be > 0
        beta : float, optional
            rate prior, must be specified in __init__() or fit(), must be > 0
        k: float, optional
            known shape parameter of the likelihood distribution,
            must be specified in __init__() or fit(), must be > 0

        Returns
        -------
        prior_predictive_samples : ndarray
            An array of samples from the prior
        """
        self._validate_prior_parameters(alpha=alpha, beta=beta, k=k)

        prior_samples = self.sample_prior(num_samples=num_samples)
        return self.random_state.weibull(a=self.k, size=num_samples) * prior_samples

    def fit(self, data=None, sum_stats=None, alpha=None, beta=None, k=None):
        """
        Fit the model using the prior and available data.

        Parameters
        ----------
        data: ndarray, optional
            nx1 array of the sample data, data OR sum_stats must be specified.
            Defaults to data if both are specified.
        sum_stats: tuple(int, int), optional
            Summary statistics, a tuple representing (num_samples,
            exponentiated_sum_events). num_samples is the number of samples
            collected. exponentiated_sum_events is the sum of events after
            being raised to the k power. np.sum(data**k)
        alpha : float, optional
            shape prior, must be specified in __init__() or fit(), must be > 0
        beta : float, optional
            rate prior, must be specified in __init__() or fit(), must be > 0
        k: float, optional
            known shape parameter of the likelihood distribution,
            must be specified in __init__() or fit(), must be > 0

        Returns
        -------

        """
        self._validate_prior_parameters(alpha=alpha, beta=beta, k=k)

        if data is not None:
            num_samples, exponentiated_sum_events = data.shape[0], np.sum(data**self.k)
        elif sum_stats is not None:
            num_samples, exponentiated_sum_events = sum_stats
        else:
            raise ValueError("Please specify either data or sum_stats input.")

        self.alpha_s = self.alpha + num_samples
        self.beta_s = self.beta + exponentiated_sum_events
        self.fitted = True

        return self.alpha_s, self.beta_s

    @check_fitted
    def sample_posterior(self, num_samples=1):
        """
        Sample from the posterior.

        Parameters
        ----------
        num_samples : int
            the number of desired samples from the posterior

        Returns
        -------
        posterior_samples : ndarray
            An array of samples from the fitted posterior
        """

        dist = st.invgamma(a=self.alpha_s, scale=self.beta_s)
        dist.random_state = self.random_state
        return np.power(dist.rvs(size=num_samples), 1.0/self.k)

    @check_fitted
    def sample_posterior_predictive(self, num_samples=1):
        """
        Sample from the posterior predictive.

        Parameters
        ----------
        num_samples : int
            the number of desired samples from the posterior

        Returns
        -------
        posterior_predictive_samples : ndarray
            An array of samples from the fitted posterior
        """

        posterior_samples = self.sample_posterior(num_samples=num_samples)
        return self.random_state.weibull(a=self.k, size=num_samples) * posterior_samples

################################################################################
################################################################################

class ParetoUniform(_blueprint.ConjugateModel):
    """
    Pareto Uniform Model

    Model with a Pareto prior and a Uniform likelihood.

    Prior: Pareto Distribution P(x_m, k)
    Likelihood: Uniform Distribution W(lb, ub)
    Parameter of Interest: Upper Bound (UB)

    Assumption: The lower bound (lb) of the likelihood is zero

    Notes
    ----------
    Section 2.5 in "A Compendium of Conjugate Priors" by Daniel Fink
    "Bayesian inference of a uniform distribution" by Thomas Minka
    """

    def __init__(self, x_m=None, k=None, *args, **kwargs):
        """
        Initialize the model object.

        Parameters
        ----------
        x_m : float, optional
            scale prior, must be specified in __init__() or fit(), must be > 0
        k : float, optional
            shape prior, must be specified in __init__() or fit(), must be > 0
        random_state : np.random.RandomState, optional
            numpy object defining the random state to use for sampling, defaults
            to `np.random`

        Returns
        -------
        None
        """

        super(ParetoUniform, self).__init__(*args, **kwargs)

        self.k = k
        self.x_m = x_m
        self.k_s = None
        self.x_m_s = None

        check_input_gt_zero(self.k, "k")
        check_input_gt_zero(self.x_m, "x_m")

    def _validate_prior_parameters(self, k, x_m):
        """utility to validate prior parameters"""

        self.k = check_input_state(k, self.k, "k")
        self.x_m = check_input_state(x_m, self.x_m, "x_m")

        check_input_gt_zero(self.k, "k")
        check_input_gt_zero(self.x_m, "x_m")

    def sample_prior(self, num_samples=1, x_m=None, k=None):
        """
        Sample from the prior.

        Parameters
        ----------
        num_samples : int
            the number of desired samples from the posterior
        x_m : float, optional
            scale prior, must be specified in __init__() or fit(), must be > 0
        k : float, optional
            shape prior, must be specified in __init__() or fit(), must be > 0

        Returns
        -------
        prior_samples : ndarray
            An array of samples from the prior
        """
        self._validate_prior_parameters(k=k, x_m=x_m)

        return self.random_state.pareto(a=self.k, size=num_samples) + self.x_m

    def sample_prior_predictive(self, num_samples=1, x_m=None, k=None):
        """
        Sample from the prior predictive.

        Parameters
        ----------
        num_samples : int
            the number of desired samples from the posterior
        x_m : float, optional
            scale prior, must be specified in __init__() or fit(), must be > 0
        k : float, optional
            shape prior, must be specified in __init__() or fit(), must be > 0

        Returns
        -------
        prior_predictive_samples : ndarray
            An array of samples from the prior
        """
        self._validate_prior_parameters(k=k, x_m=x_m)

        prior_samples = self.sample_prior(num_samples=num_samples)
        return self.random_state.uniform(low=0.0, high=prior_samples)

    def fit(self, data=None, sum_stats=None, x_m=None, k=None):
        """
        Fit the model using the prior and available data.

        Parameters
        ----------
        data: ndarray, optional
            nx1 array of the sample data, data OR sum_stats must be specified.
            Defaults to data if both are specified.
        sum_stats: tuple(int, int), optional
            Summary statistics, a tuple representing (num_samples,
            max_value). num_samples is the number of samples
            collected. max_value is the maximum value in the sample
        x_m : float, optional
            scale prior, must be specified in __init__() or fit(), must be > 0
        k : float, optional
            shape prior, must be specified in __init__() or fit(), must be > 0

        Returns
        -------
        k_s : float
            posterior shape parameter
        x_m_s : float
            posterior scale / minimum value parameter
        """
        self._validate_prior_parameters(k=k, x_m=x_m)

        if data is not None:
            num_samples, max_value = data.shape[0], data.max()
        elif sum_stats is not None:
            num_samples, max_value = sum_stats
        else:
            raise ValueError("Please specify either data or sum_stats input.")

        self.k_s = self.k + num_samples
        self.x_m_s = max_value
        self.fitted = True

        return self.x_m_s, self.k_s

    @check_fitted
    def sample_posterior(self, num_samples=1):
        """
        Sample from the posterior.

        Parameters
        ----------
        num_samples : int
            the number of desired samples from the posterior

        Returns
        -------
        posterior_samples : ndarray
            An array of samples from the fitted posterior
        """

        return self.random_state.pareto(a=self.k_s, size=num_samples) + self.x_m_s

    @check_fitted
    def sample_posterior_predictive(self, num_samples=1):
        """
        Sample from the posterior predictive.

        Parameters
        ----------
        num_samples : int
            the number of desired samples from the posterior

        Returns
        -------
        posterior_predictive_samples : ndarray
            An array of samples from the fitted posterior
        """

        posterior_samples = self.sample_posterior(num_samples=num_samples)
        return self.random_state.uniform(low=0.0, high=posterior_samples)

################################################################################
################################################################################

class GammaPareto(_blueprint.ConjugateModel):
    """
    Gamma Pareto Model

    Prior: Gamma Distribution G(alpha, beta)
    Likelihood: Pareto Distribution Pa(x_m, k)
    Parameter of Interest: Shape (k)

    Assumption: Known scale / minimum parameter (x_m)

    Notes
    ----------
    Section 2.6 in  "A Compendium of Conjugate Priors" by Daniel Fink
    """

    def __init__(self, alpha=None, beta=None, x_m=None, *args, **kwargs):
        """
        Initialize the model object.

        Parameters
        ----------
        alpha : float, optional
            shape prior, must be specified in __init__() or fit(), must be > 0
        beta : float, optional
            rate prior, must be specified in __init__() or fit(), must be > 0
        x_m : float, optional
            known scale / minimum parameter of pareto likelihood,
            must be specified in __init__() or fit(), must be > 0
        random_state : np.random.RandomState, optional
            numpy object defining the random state to use for sampling, defaults
            to `np.random`

        Returns
        -------
        None
        """

        super(GammaPareto, self).__init__(*args, **kwargs)

        self.alpha = alpha
        self.beta = beta
        self.x_m = x_m
        self.alpha_s = None
        self.beta_s = None

        check_input_gt_zero(self.alpha, "alpha")
        check_input_gt_zero(self.beta, "beta")
        check_input_gt_zero(self.x_m, "x_m")

    def _validate_prior_parameters(self, alpha, beta, x_m):
        """utility to validate prior parameters"""

        self.alpha = check_input_state(alpha, self.alpha, "alpha")
        self.beta = check_input_state(beta, self.beta, "beta")
        self.x_m = check_input_state(x_m, self.x_m, "x_m")

        check_input_gt_zero(self.alpha, "alpha")
        check_input_gt_zero(self.beta, "beta")
        check_input_gt_zero(self.x_m, "x_m")

    def sample_prior(self, num_samples=1, alpha=None, beta=None, x_m=None):
        """
        Sample from the prior.

        Parameters
        ----------
        num_samples : int
            the number of desired samples from the posterior
        alpha : float, optional
            shape prior, must be specified in __init__() or fit(), must be > 0
        beta : float, optional
            rate prior, must be specified in __init__() or fit(), must be > 0
        x_m : float, optional
            known scale / minimum parameter of pareto likelihood,
            must be specified in __init__() or fit(), must be > 0

        Returns
        -------
        prior_samples : ndarray
            An array of samples from the prior
        """
        self._validate_prior_parameters(alpha=alpha, beta=beta, x_m=x_m)

        return self.random_state.gamma(shape=self.alpha, scale=1.0/self.beta,
                                       size=num_samples)

    def sample_prior_predictive(self, num_samples=1, alpha=None, beta=None, x_m=None):
        """
        Sample from the prior predictive.

        Parameters
        ----------
        num_samples : int
            the number of desired samples from the posterior
        alpha : float, optional
            shape prior, must be specified in __init__() or fit(), must be > 0
        beta : float, optional
            rate prior, must be specified in __init__() or fit(), must be > 0
        x_m : float, optional
            known scale / minimum parameter of pareto likelihood,
            must be specified in __init__() or fit(), must be > 0

        Returns
        -------
        prior_predictive_samples : ndarray
            An array of samples from the prior
        """
        self._validate_prior_parameters(alpha=alpha, beta=beta, x_m=x_m)

        prior_samples = self.sample_prior(num_samples=num_samples)
        return self.random_state.pareto(a=prior_samples) + self.x_m

    def fit(self, data=None, sum_stats=None, alpha=None, beta=None, x_m=None):
        """
        Fit the model using the prior and available data.

        Parameters
        ----------
        data: ndarray, optional
            nx1 array of the sample data, data OR sum_stats must be specified.
            Defaults to data if both are specified.
        sum_stats: tuple(int, int), optional
            Summary statistics, a tuple representing (num_events, sum_log_ratio).
            num_events is the total number of events, must be > 0. sum_log_ratio
            is the sum of the log of the ratio of x_i / x_m.
        alpha : float, optional
            shape prior, must be specified in __init__() or fit(), must be > 0
        beta : float, optional
            rate prior, must be specified in __init__() or fit(), must be > 0
        x_m : float, optional
            known scale / minimum parameter of pareto likelihood,
            must be specified in __init__() or fit(), must be > 0

        Returns
        -------

        """
        self._validate_prior_parameters(alpha=alpha, beta=beta, x_m=x_m)

        if data is not None:
            num_events, sum_log_ratio = data.shape[0], np.log(data/self.x_m).sum()
        elif sum_stats is not None:
            num_events, sum_log_ratio = sum_stats
        else:
            raise ValueError("Please specify either data or sum_stats input.")

        self.alpha_s = self.alpha + num_events
        self.beta_s = self.beta + sum_log_ratio
        self.fitted = True

        return self.alpha_s, self.beta_s

    @check_fitted
    def sample_posterior(self, num_samples=1):
        """
        Sample from the posterior.

        Parameters
        ----------
        num_samples : int
            the number of desired samples from the posterior

        Returns
        -------
        posterior_samples : ndarray
            An array of samples from the prior
        """

        return self.random_state.gamma(shape=self.alpha_s, scale=1.0/self.beta_s,
                                       size=num_samples)

    @check_fitted
    def sample_posterior_predictive(self, num_samples=1):
        """
        Sample from the posterior predictive.

        Parameters
        ----------
        num_samples : int
            the number of desired samples from the posterior

        Returns
        -------
        posterior_predictive_samples : ndarray
            An array of samples from the prior
        """

        posterior_samples = self.sample_posterior(num_samples=num_samples)
        return self.random_state.pareto(a=posterior_samples) + self.x_m

################################################################################
################################################################################

class NormalNormal(_blueprint.ConjugateModel):
    """
    Normal Normal Model

    Prior: Normal Distribution N(mu, tau)
    Likelihood: Normal Distribution N(mu, tau)
    Parameter of Interest: Mean (mu)

    Assumption: precision parameter (tau) is known

    Notes
    ----------
    Section 2.9.1 in  "A Compendium of Conjugate Priors" by Daniel Fink
    """

    def __init__(self, mu=None, tau=None, tau_lik=None, *args, **kwargs):
        """
        Initialize the model object.

        Parameters
        ----------
        mu : float, optional
            mean prior, must be specified in __init__() or fit()
        tau: float, optional
            precision prior,
            must be specified in __init__() or fit(), must be > 0
        tau_lik: float, optional
            known precision of the likelihood,
            must be specified in __init__() or fit(), must be > 0
        random_state : np.random.RandomState, optional
            numpy object defining the random state to use for sampling, defaults
            to `np.random`

        Returns
        -------
        None
        """

        super(NormalNormal, self).__init__(*args, **kwargs)

        self.mu = mu
        self.tau = tau
        self.tau_lik = tau_lik
        self.mu_s = None
        self.tau_s = None

        check_input_gt_zero(self.tau, "tau")
        check_input_gt_zero(self.tau_lik, "tau_lik")

    def _validate_prior_parameters(self, mu, tau, tau_lik):
        """utility to validate prior parameters"""

        self.mu = check_input_state(mu, self.mu, "mu")
        self.tau = check_input_state(tau, self.tau, "tau")
        self.tau_lik = check_input_state(tau_lik, self.tau_lik, "tau_lik")

        check_input_gt_zero(self.tau, "tau")
        check_input_gt_zero(self.tau_lik, "tau_lik")

    def sample_prior(self, num_samples=1, mu=None, tau=None, tau_lik=None):
        """
        Sample from the prior.

        Parameters
        ----------
        num_samples : int
            the number of desired samples from the posterior
        mu : float, optional
            mean prior, must be specified in __init__() or fit()
        tau: float, optional
            precision prior,
            must be specified in __init__() or fit(), must be > 0
        tau_lik: float, optional
            known precision of the likelihood,
            must be specified in __init__() or fit(), must be > 0

        Returns
        -------
        prior_samples : ndarray
            An array of samples from the prior
        """
        self._validate_prior_parameters(mu=mu, tau=tau, tau_lik=tau_lik)

        return self.random_state.normal(loc=self.mu, scale=np.sqrt(1.0/self.tau),
            size=num_samples)

    def sample_prior_predictive(self, num_samples=1, mu=None, tau=None, tau_lik=None):
        """
        Sample from the prior predictive.

        Parameters
        ----------
        num_samples : int
            the number of desired samples from the posterior
        mu : float, optional
            mean prior, must be specified in __init__() or fit()
        tau: float, optional
            precision prior,
            must be specified in __init__() or fit(), must be > 0
        tau_lik: float, optional
            known precision of the likelihood,
            must be specified in __init__() or fit(), must be > 0

        Returns
        -------
        prior_predictive_samples : ndarray
            An array of samples from the prior
        """
        self._validate_prior_parameters(mu=mu, tau=tau, tau_lik=tau_lik)

        prior_samples = self.sample_prior(num_samples=num_samples)
        return self.random_state.normal(loc=prior_samples, scale=np.sqrt(1.0/self.tau_lik))

    def fit(self, data=None, sum_stats=None, mu=None, tau=None, tau_lik=None):
        """
        Fit the model using the prior and available data.

        Parameters
        ----------
        data: ndarray, optional
            nx1 array of the sample data, data OR sum_stats must be specified.
            Defaults to data if both are specified.
        sum_stats: tuple(int, int), optional
            Summary statistics, a tuple representing (num_events, sum_events).
            num_events is the total number of events, must be > 0. sum_events is the
            sum of the data points.
        mu : float, optional
            mean prior, must be specified in __init__() or fit()
        tau: float, optional
            precision prior,
            must be specified in __init__() or fit(), must be > 0
        tau_lik: float, optional
            known precision of the likelihood,
            must be specified in __init__() or fit(), must be > 0

        Returns
        -------

        """
        self._validate_prior_parameters(mu=mu, tau=tau, tau_lik=tau_lik)

        if data is not None:
            num_events, sum_events = data.shape[0], data.sum()
        elif sum_stats is not None:
            num_events, sum_events = sum_stats
        else:
            raise ValueError("Please specify either data or sum_stats input.")

        # weighted sum of priors and data
        mu_numerator = self.mu * self.tau + self.tau_lik * sum_events
        # weighted sum of prior and data
        mu_demoninator = self.tau + num_events * self.tau_lik
        self.mu_s = mu_numerator / mu_demoninator
        self.tau_s = mu_demoninator
        self.fitted = True

        return self.mu_s, self.tau_s

    @check_fitted
    def sample_posterior(self, num_samples=1):
        """
        Sample from the posterior.

        Parameters
        ----------
        num_samples : int
            the number of desired samples from the posterior

        Returns
        -------
        posterior_samples : ndarray
            An array of samples from the prior
        """

        return self.random_state.normal(loc=self.mu_s, scale=np.sqrt(1.0/self.tau_s),
            size=num_samples)

    @check_fitted
    def sample_posterior_predictive(self, num_samples=1):
        """
        Sample from the posterior predictive.

        Parameters
        ----------
        num_samples : int
            the number of desired samples from the posterior

        Returns
        -------
        posterior_predictive_samples : ndarray
            An array of samples from the prior
        """

        # posterior_samples = self.sample_posterior(num_samples=num_samples)
        # return self.random_state.normal(loc=posterior_samples,
        #     scale=np.sqrt(1.0/self.tau_lik))

        return self.random_state.normal(loc=self.mu_s,
            scale=np.sqrt(1.0/self.tau+1.0/self.tau_lik), size=num_samples)

################################################################################
################################################################################

class GammaNormal(_blueprint.ConjugateModel):
    """
    Gamma Normal Model

    Prior: Gamma Distribution G(alpha, beta)
    Likelihood: Normal Distribution N(mu, tau)
    Parameter of Interest: Precision (tau)

    Assumption: likelihood mean (mu) is known

    Notes
    ----------
    Section 2.9.2 in  "A Compendium of Conjugate Priors" by Daniel Fink
    """

    def __init__(self, alpha=None, beta=None, mu_lik=None, *args, **kwargs):
        """
        Initialize the model object.

        Parameters
        ----------
        alpha : float, optional
            shape prior, must be specified in __init__() or fit(), must be > 0.
        beta : float, optional
            scale prior, must be specified in __init__() or fit(), must be > 0.
        mu_lik : int, optional
            The known mean of the likelihood.
        random_state : np.random.RandomState, optional
            numpy object defining the random state to use for sampling, defaults
            to `np.random`

        Returns
        -------
        None
        """

        super(GammaNormal, self).__init__(*args, **kwargs)

        self.alpha = alpha
        self.beta = beta
        self.mu_lik = mu_lik
        self.alpha_s = None
        self.beta_s = None

        check_input_gt_zero(self.alpha, "alpha")
        check_input_gt_zero(self.beta, "beta")

    def _validate_prior_parameters(self, alpha, beta, mu_lik):
        """utility to validate prior parameters"""

        self.alpha = check_input_state(alpha, self.alpha, "alpha")
        self.beta = check_input_state(beta, self.beta, "beta")
        self.mu_lik = check_input_state(mu_lik, self.mu_lik, "mu_lik")

        check_input_gt_zero(self.alpha, "alpha")
        check_input_gt_zero(self.beta, "beta")

    def sample_prior(self, num_samples=1, alpha=None, beta=None, mu_lik=None):
        """
        Sample from the prior.

        Parameters
        ----------
        num_samples : int
            the number of desired samples from the posterior
        alpha : float, optional
            shape prior, must be specified in __init__() or fit(), must be > 0.
        beta : float, optional
            scale prior, must be specified in __init__() or fit(), must be > 0.
        mu_lik : int, optional
            The known mean of the likelihood.

        Returns
        -------
        prior_samples : ndarray
            An array of samples from the prior
        """
        self._validate_prior_parameters(alpha=alpha, beta=beta, mu_lik=mu_lik)

        return self.random_state.gamma(shape=self.alpha, scale=1.0/self.beta,
            size=num_samples)

    def sample_prior_predictive(self, num_samples=1, alpha=None, beta=None, mu_lik=None):
        """
        Sample from the prior predictive.

        Parameters
        ----------
        num_samples : int
            the number of desired samples from the posterior
        alpha : float, optional
            shape prior, must be specified in __init__() or fit(), must be > 0.
        beta : float, optional
            scale prior, must be specified in __init__() or fit(), must be > 0.
        mu_lik : int, optional
            The known mean of the likelihood.

        Returns
        -------
        prior_predictive_samples : ndarray
            An array of samples from the prior
        """
        self._validate_prior_parameters(alpha=alpha, beta=beta, mu_lik=mu_lik)

        prior_samples = self.sample_prior(num_samples=num_samples)
        prior_samples = np.sqrt(1.0/prior_samples)
        return self.random_state.normal(loc=self.mu_lik, scale=prior_samples)

    def fit(self, data=None, sum_stats=None, alpha=None, beta=None, mu_lik=None):
        """
        Fit the model using the prior and available data.

        Parameters
        ----------
        data: ndarray, optional
            nx1 array of the sample data, data OR sum_stats must be specified.
            Defaults to data if both are specified.
        sum_stats: tuple(int, int), optional
            Summary statistics, a tuple representing (num_events, sum_sq_diff).
            num_events is the total number of events, must be > 0. sum_sq_diff is
            the sum of squared differences between each data point and the known
            likelihood mean.
        alpha : float, optional
            shape prior, must be specified in __init__() or fit(), must be > 0.
        beta : float, optional
            scale prior, must be specified in __init__() or fit(), must be > 0.
        mu_lik : int, optional
            The known mean of the likelihood.

        Returns
        -------

        """
        self._validate_prior_parameters(alpha=alpha, beta=beta, mu_lik=mu_lik)

        if data is not None:
            num_events, sum_sq_diff = data.shape[0], np.sum((data - self.mu_lik)**2.0)
        elif sum_stats is not None:
            num_events, sum_sq_diff = sum_stats
        else:
            raise ValueError("Please specify either data or sum_stats input.")

        self.alpha_s = self.alpha + num_events / 2.0
        self.beta_s = self.beta + sum_sq_diff / 2.0
        self.fitted = True

        return self.alpha_s, self.beta_s

    @check_fitted
    def sample_posterior(self, num_samples=1):
        """
        Sample from the posterior.

        Parameters
        ----------
        num_samples : int
            the number of desired samples from the posterior

        Returns
        -------
        posterior_samples : ndarray
            An array of samples from the prior
        """

        return self.random_state.gamma(shape=self.alpha_s, scale=1.0/self.beta_s,
            size=num_samples)

    @check_fitted
    def sample_posterior_predictive(self, num_samples=1):
        """
        Sample from the posterior predictive.

        Parameters
        ----------
        num_samples : int
            the number of desired samples from the posterior

        Returns
        -------
        posterior_predictive_samples : ndarray
            An array of samples from the prior
        """

        # posterior_samples = self.sample_posterior(num_samples=num_samples)
        # posterior_samples = np.sqrt(1.0/posterior_samples)
        # return self.random_state.normal(loc=self.mu_lik, scale=posterior_samples)

        dist = st.t(loc=self.mu_lik, scale=np.sqrt(self.beta_s/self.alpha_s), df=2*self.alpha_s)
        dist.random_state = self.random_state
        return dist.rvs(size=num_samples)

################################################################################
################################################################################

class NormalGammaNormal(_blueprint.ConjugateModel):
    """
    Normal Gamma Normal Model

    Prior: Normal Gamma Distribution N(mu, tau)G(alpha, beta)
    Likelihood: Normal Distribution N(mu, tau)
    Parameter of Interest: Mean (mu) and Precision (tau)

    Notes
    ----------
    Section 2.9.1 in  "A Compendium of Conjugate Priors" by Daniel Fink
    Section 2.9.2 in  "A Compendium of Conjugate Priors" by Daniel Fink
    Section 6 in "Conjugate Bayesian analysis of the Gaussian distribution" by Kevin Murphy
    Section 3 in "The Conjugate Prior for the Normal Distribution" by Michael Jordan
    """

    def __init__(self, alpha=None, beta=None, mu=None, nu=None, *args, **kwargs):
        """
        Initialize the model object.

        Parameters
        ----------
        alpha : float, optional
            shape prior, must be specified in __init__() or fit(), must be > 0.
        beta : float, optional
            rate prior, must be specified in __init__() or fit(), must be > 0.
        mu: float, optional
            mean prior, must be specified in __init__() or fit().
        nu: float, optional
            mean prior strength,
            must be specified in __init__() or fit(), must be > 0.
        random_state : np.random.RandomState, optional
            numpy object defining the random state to use for sampling, defaults
            to `np.random`

        Returns
        -------
        None
        """

        super(NormalGammaNormal, self).__init__(*args, **kwargs)

        self.alpha = alpha
        self.beta = beta
        self.mu = mu
        self.nu = nu
        self.alpha_s = None
        self.beta_s = None
        self.mu_s = None
        self.nu_s = None

        check_input_gt_zero(self.alpha, "alpha")
        check_input_gt_zero(self.beta, "beta")
        check_input_gt_zero(self.nu, "nu")

    def _validate_prior_parameters(self, alpha, beta, mu, nu):
        """utility to validate prior parameters"""

        self.alpha = check_input_state(alpha, self.alpha, "alpha")
        self.beta = check_input_state(beta, self.beta, "beta")
        self.mu = check_input_state(mu, self.mu, "mu")
        self.nu = check_input_state(nu, self.nu, "nu")

        check_input_gt_zero(self.alpha, "alpha")
        check_input_gt_zero(self.beta, "beta")
        check_input_gt_zero(self.nu, "nu")

    def sample_prior(self, num_samples=1, alpha=None, beta=None, mu=None, nu=None):
        """
        Sample from the prior.

        Parameters
        ----------
        num_samples : int
            the number of desired samples from the posterior
        alpha : float, optional
            shape prior, must be specified in __init__() or fit(), must be > 0.
        beta : float, optional
            rate prior, must be specified in __init__() or fit(), must be > 0.
        mu: float, optional
            mean prior, must be specified in __init__() or fit().
        nu: float, optional
            mean prior strength,
            must be specified in __init__() or fit(), must be > 0.

        Returns
        -------
        mu_prior_samples : ndarray
            An array of samples from the prior for mu
        tau_prior_samples : ndarray
            An array of samples from the prior for tau
        """
        self._validate_prior_parameters(alpha=alpha, beta=beta, mu=mu, nu=nu)

        precision_prior = self.random_state.gamma(shape=self.alpha,
            scale=1.0/self.beta, size=num_samples)
        mean_prior = self.random_state.normal(loc=self.mu,
            scale=np.sqrt(1.0/(precision_prior*self.nu)))
        return mean_prior, precision_prior

    def sample_prior_predictive(self, num_samples=1, alpha=None, beta=None, mu=None, nu=None):
        """
        Sample from the prior predictive.

        Parameters
        ----------
        num_samples : int
            the number of desired samples from the posterior
        alpha : float, optional
            shape prior, must be specified in __init__() or fit(), must be > 0.
        beta : float, optional
            rate prior, must be specified in __init__() or fit(), must be > 0.
        mu: float, optional
            mean prior, must be specified in __init__() or fit().
        nu: float, optional
            mean prior strength,
            must be specified in __init__() or fit(), must be > 0.

        Returns
        -------
        prior_predictive_samples : ndarray
            An array of samples from the prior
        """
        self._validate_prior_parameters(alpha=alpha, beta=beta, mu=mu, nu=nu)

        mean_prior, precision_prior = self.sample_prior(num_samples=num_samples)
        return self.random_state.normal(loc=mean_prior,
            scale=np.sqrt(1.0/precision_prior))

    def fit(self, data=None, sum_stats=None, alpha=None, beta=None, mu=None, nu=None):
        """
        Fit the model using the prior and available data.

        Parameters
        ----------
        data: ndarray, optional
            nx1 array of the sample data, data OR sum_stats must be specified.
            Defaults to data if both are specified.
        sum_stats: tuple(int, float, float), optional
            Summary statistics, a tuple representing (num_events, sample_mean,
            sum_sq_diff). num_events is the total number of events, must be > 0.
            sample_mean is the mean of the data sample. sum_sq_diff is the sum
            of squared differences between each data point and the sample mean.
        alpha : float, optional
            shape prior, must be specified in __init__() or fit(), must be > 0.
        beta : float, optional
            rate prior, must be specified in __init__() or fit(), must be > 0.
        mu: float, optional
            mean prior, must be specified in __init__() or fit().
        nu: float, optional
            mean prior strength,
            must be specified in __init__() or fit(), must be > 0.

        Returns
        -------

        """
        self._validate_prior_parameters(alpha=alpha, beta=beta, mu=mu, nu=nu)

        if data is not None:
            num_events, sample_mean, sum_sq_diff = data.shape[0], data.mean(), \
                np.sum((data - data.mean())**2.0)
        elif sum_stats is not None:
            num_events, sample_mean, sum_sq_diff = sum_stats
        else:
            raise ValueError("Please specify either data or sum_stats input.")

        self.nu_s = self.nu + num_events
        self.mu_s = (self.nu*self.mu + num_events*sample_mean) / self.nu_s
        self.alpha_s = self.alpha + num_events / 2.0
        self.beta_s = self.beta + 0.5 * sum_sq_diff + \
            (num_events*self.nu) / self.nu_s * \
            (sample_mean - self.mu)**2 / 2.0

        self.fitted = True

        return self.alpha_s, self.beta_s, self.mu_s, self.nu_s

    @check_fitted
    def sample_posterior(self, num_samples=1):
        """
        Sample from the posterior.

        Parameters
        ----------
        num_samples : int
            the number of desired samples from the posterior

        Returns
        -------
        mu_posterior_samples : ndarray
            An array of samples from the prior for mu
        tau_posterior_samples : ndarray
            An array of samples from the prior for tau
        """
        precision_posterior = self.random_state.gamma(shape=self.alpha_s,
            scale=1.0/self.beta_s, size=num_samples)
        mean_posterior = self.random_state.normal(loc=self.mu_s,
            scale=np.sqrt(1.0/(precision_posterior*self.nu_s)))
        return mean_posterior, precision_posterior

    @check_fitted
    def sample_posterior_predictive(self, num_samples=1):
        """
        Sample from the posterior predictive.

        Parameters
        ----------
        num_samples : int
            the number of desired samples from the posterior

        Returns
        -------
        posterior_predictive_samples : ndarray
            An array of samples from the prior
        """

        mean_posterior, precision_posterior = self.sample_posterior(num_samples=num_samples)
        return self.random_state.normal(loc=mean_posterior,
            scale=np.sqrt(1.0/precision_posterior))

################################################################################
################################################################################
