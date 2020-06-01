"""
Discrete Likelihood Models
=====
This module includes conjugate model classes for discrete likelihood functions.
"""

import numpy as np
# import scipy.stats as st
import logging

from romus._utils import check_fitted, check_input_gt_zero, check_input_state
from romus import _blueprint

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

################################################################################
################################################################################

class BetaBinomial(_blueprint.ConjugateModel):
    """
    Beta Binomial Model (Equivalent to Bernoulli Beta Model)

    Prior: Beta Distribution B(alpha, Beta)
    Likelihood: Binomial Distribution Bi(N, p)
    Parameter of Interest: Probability of Success (p)

    Notes
    ----------
    Section 2.3 in  "A Compendium of Conjugate Priors" by Daniel Fink
    """

    def __init__(self, alpha=None, beta=None, *args, **kwargs):
        """
        Initialize the model object.

        Parameters
        ----------
        alpha : float, optional
            shape prior (number of successes),
            must be specified in __init__() or fit(), must be > 0
        beta : float, optional
            scale prior (number of failures),
            must be specified in __init__() or fit(), must be > 0
        random_state : np.random.RandomState, optional
            numpy object defining the random state to use for sampling, defaults
            to `np.random`

        Returns
        -------
        None
        """

        super(BetaBinomial, self).__init__(*args, **kwargs)

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
            shape prior (number of successes),
            must be specified in __init__() or fit(), must be > 0
        beta : float, optional
            scale prior (number of failures),
            must be specified in __init__() or fit(), must be > 0

        Returns
        -------
        prior_samples : ndarray
            An array of samples from the prior
        """
        self._validate_prior_parameters(alpha=alpha, beta=beta)

        return self.random_state.beta(a=self.alpha, b=self.beta,
                                      size=num_samples)

    def sample_prior_predictive(self, num_samples=1, alpha=None, beta=None, N=1):
        """
        Sample from the prior predictive.

        Parameters
        ----------
        num_samples : int
            the number of desired samples from the posterior
        alpha : float, optional
            shape prior (number of successes),
            must be specified in __init__() or fit(), must be > 0
        beta : float, optional
            scale prior (number of failures),
            must be specified in __init__() or fit(), must be > 0
        N : int
            The number of observations for each sample from the binomial
            distribution, must be greater than 0

        Returns
        -------
        prior_predictive_samples : ndarray
            An array of samples from the prior
        """
        self._validate_prior_parameters(alpha=alpha, beta=beta)

        if not isinstance(N, int):
            raise ValueError("Paramter N must be an integer.")
        if N <= 0:
            raise ValueError("Paramter N must be greater than 0.")

        prior_samples = self.sample_prior(num_samples=num_samples)
        return self.random_state.binomial(n=N, p=prior_samples)

    def fit(self, data=None, sum_stats=None, alpha=None, beta=None):
        """
        Fit the model using the prior and available data.

        Parameters
        ----------
        data: ndarray, optional
            nx1 array of the sample data, data OR sum_stats must be specified.
            Defaults to data if both are specified.
        sum_stats: tuple(int, int), optional
            Summary statistics, a tuple representing (num_trials, num_successes).
            num_trials is the total number of trials (denominator of rate), must
            be >= 0. num_successes is the number of successful trials (numerator
            of rate), must be >= 0.
        alpha : float, optional
            shape prior (number of successes),
            must be specified in __init__() or fit(), must be > 0
        beta : float, optional
            scale prior (number of failures),
            must be specified in __init__() or fit(), must be > 0

        Returns
        -------

        """
        self._validate_prior_parameters(alpha=alpha, beta=beta)

        if data is not None:
            num_trials, num_successes = data.shape[0], data.sum()
        elif sum_stats is not None:
            num_trials, num_successes = sum_stats
        else:
            raise ValueError("Please specify either data or sum_stats input.")

        # posterior_successes = prior_successes + observed_successes
        self.alpha_s = self.alpha + num_successes
        # posterior_failures = prior_failures + observed_failures
        self.beta_s = self.beta + num_trials - num_successes
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

        return self.random_state.beta(a=self.alpha_s, b=self.beta_s,
                                      size=num_samples)

    @check_fitted
    def sample_posterior_predictive(self, num_samples=1, N=1):
        """
        Sample from the posterior predictive.

        Parameters
        ----------
        num_samples : int
            the number of desired samples from the posterior
        N : int
            The number of observations for each sample from the binomial
            distribution, must be greater than 0

        Returns
        -------
        posterior_predictive_samples : ndarray
            An array of samples from the fitted posterior
        """

        if not isinstance(N, int):
            raise ValueError("Paramter N must be an integer.")
        if N <= 0:
            raise ValueError("Paramter N must be greater than 0.")

        posterior_samples =  self.sample_posterior(num_samples=num_samples)
        return self.random_state.binomial(n=N, p=posterior_samples)

BetaBernoulli = BetaBinomial

################################################################################
################################################################################

class GammaPoisson(_blueprint.ConjugateModel):
    """
    Gamma Poisson Model

    Prior: Gamma Distribution G(alpha, beta)
    Likelihood: Poisson Distribution P(lambda)
    Parameter of Interest: Rate of Events (lambda)

    Notes
    ----------
    Section 2.2 in  "A Compendium of Conjugate Priors" by Daniel Fink
    """

    def __init__(self, k=None, theta=None, *args, **kwargs):
        """
        Initialize the model object.

        Parameters
        ----------
        k : float, optional
            shape prior (count of events),
            must be specified in __init__() or fit(), must be > 0
        theta : float, optional
            scale prior (interval over which events were counted),
            must be specified in __init__() or fit(), must be > 0
        random_state : np.random.RandomState, optional
            numpy object defining the random state to use for sampling, defaults
            to `np.random`

        Returns
        -------
        None
        """

        super(GammaPoisson, self).__init__(*args, **kwargs)

        self.k = k
        self.theta = theta
        self.k_s = None
        self.theta_s = None

        check_input_gt_zero(self.k, "k")
        check_input_gt_zero(self.theta, "theta")

    def _validate_prior_parameters(self, k, theta):
        """utility to validate prior parameters"""

        self.k = check_input_state(k, self.k, "k")
        self.theta = check_input_state(theta, self.theta, "theta")

        check_input_gt_zero(self.k, "k")
        check_input_gt_zero(self.theta, "theta")

    def sample_prior(self, num_samples=1, k=None, theta=None):
        """
        Sample from the prior.

        Parameters
        ----------
        num_samples : int
            the number of desired samples from the posterior
        k : float, optional
            shape prior (count of events),
            must be specified in __init__() or fit(), must be > 0
        theta : float, optional
            scale prior (interval over which events were counted),
            must be specified in __init__() or fit(), must be > 0

        Returns
        -------
        prior_samples : ndarray
            An array of samples from the prior
        """
        self._validate_prior_parameters(k=k, theta=theta)

        return self.random_state.gamma(shape=self.k, scale=self.theta,
                                       size=num_samples)

    def sample_prior_predictive(self, num_samples=1, k=None, theta=None):
        """
        Sample from the prior predictive.

        Parameters
        ----------
        num_samples : int
            the number of desired samples from the posterior
        k : float, optional
            shape prior (count of events),
            must be specified in __init__() or fit(), must be > 0
        theta : float, optional
            scale prior (interval over which events were counted),
            must be specified in __init__() or fit(), must be > 0

        Returns
        -------
        prior_samples : ndarray
            An array of samples from the prior
        """
        self._validate_prior_parameters(k=k, theta=theta)

        prior_samples = self.sample_prior(num_samples=num_samples)
        return self.random_state.poisson(lam=prior_samples)

    def fit(self, data=None, sum_stats=None, k=None, theta=None):
        """
        Fit the model using the prior and available data.

        Parameters
        ----------
        data: ndarray, optional
            nx1 array of the sample data, data OR sum_stats must be specified.
            Defaults to data if both are specified.
        sum_stats: tuple(int, int), optional
            Summary statistics, a tuple representing (num_samples, num_events).
            num_samples is the total number of samples (denominator of rate),
            must be >= 0. num_events is the number of events (numerator of rate),
            must be >= 0.
        k : float, optional
            shape prior (count of events),
            must be specified in __init__() or fit(), must be > 0
        theta : float, optional
            scale prior (interval over which events were counted),
            must be specified in __init__() or fit(), must be > 0

        Returns
        -------

        """
        self._validate_prior_parameters(k=k, theta=theta)

        if data is not None:
            num_samples, num_events = data.shape[0], data.sum()
        elif sum_stats is not None:
            num_trials, num_successes = sum_stats
        else:
            raise ValueError("Please specify either data or sum_stats input.")

        self.k_s = self.k + num_events
        self.theta_s = self.theta / (num_samples * self.theta + 1.0)
        self.fitted = True

        return self.k_s, self.theta_s

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

        return self.random_state.gamma(shape=self.k_s, scale=self.theta_s,
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
            An array of samples from the fitted posterior
        """

        # Gamma-Poisson distribution is equivalent to Negative Binomial
        # b = 1.0 / self.theta_s
        # return self.random_state.negative_binomial(n=self.k_s, p=b/(b+1),
        #     size=num_samples)

        posterior_samples = self.sample_posterior(num_samples=num_samples)
        return self.random_state.poisson(lam=posterior_samples)

################################################################################
################################################################################

class BetaNegativeBinomial(_blueprint.ConjugateModel):
    """
    Beta Negative Binomial Model

    Prior: Beta Distribution B(alpha, Beta)
    Likelihood: Negative Binomial Distribution Bi(r, p)
    Parameter of Interest: Probability of Success (p)

    Assumption: r is known

    Notes
    ----------
    Section 2.3 in  "A Compendium of Conjugate Priors" by Daniel Fink
    """

    def __init__(self, alpha=None, beta=None, r=None, *args, **kwargs):
        """
        Initialize the model object.

        Parameters
        ----------
        alpha : float, optional
            shape prior (number of successes),
            must be specified in __init__() or fit(), must be > 0
        beta : float, optional
            scale prior (number of failures),
            must be specified in __init__() or fit(), must be > 0
        r : float
            dispersion parameter, number of failures until the experiment is
            stopped, must be specified in __init__() or fit(), must be > 0
        random_state : np.random.RandomState, optional
            numpy object defining the random state to use for sampling, defaults
            to `np.random`

        Returns
        -------
        None
        """

        super(BetaNegativeBinomial, self).__init__(*args, **kwargs)

        self.alpha = alpha
        self.beta = beta
        self.r = r
        self.alpha_s = None
        self.beta_s = None

        check_input_gt_zero(self.alpha, "alpha")
        check_input_gt_zero(self.beta, "beta")
        check_input_gt_zero(self.r, "r")

    def _validate_prior_parameters(self, alpha, beta, r):
        """utility to validate prior parameters"""

        self.alpha = check_input_state(alpha, self.alpha, "alpha")
        self.beta = check_input_state(beta, self.beta, "beta")
        self.r = check_input_state(alpha, self.r, "r")

        check_input_gt_zero(self.alpha, "alpha")
        check_input_gt_zero(self.beta, "beta")
        check_input_gt_zero(self.r, "r")

    def sample_prior(self, num_samples=1, alpha=None, beta=None, r=None):
        """
        Sample from the prior.

        Parameters
        ----------
        num_samples : int
            the number of desired samples from the posterior
        alpha : float, optional
            shape prior (number of successes),
            must be specified in __init__() or fit(), must be > 0
        beta : float, optional
            scale prior (number of failures),
            must be specified in __init__() or fit(), must be > 0
        r : float
            dispersion parameter, number of failures until the experiment is
            stopped, must be specified in __init__() or fit(), must be > 0

        Returns
        -------
        prior_samples : ndarray
            An array of samples from the prior
        """
        self._validate_prior_parameters(alpha=alpha, beta=beta, r=r)

        return self.random_state.beta(a=self.alpha, b=self.beta,
                                      size=num_samples)

    def sample_prior_predictive(self, num_samples=1,
        alpha=None, beta=None, r=None):
        """
        Sample from the prior preditive.

        Parameters
        ----------
        num_samples : int
            the number of desired samples from the posterior
        alpha : float, optional
            shape prior (number of successes),
            must be specified in __init__() or fit(), must be > 0
        beta : float, optional
            scale prior (number of failures),
            must be specified in __init__() or fit(), must be > 0
        r : float
            dispersion parameter, number of failures until the experiment is
            stopped, must be specified in __init__() or fit(), must be > 0

        Returns
        -------
        prior_samples : ndarray
            An array of samples from the prior
        """
        self._validate_prior_parameters(alpha=alpha, beta=beta, r=r)

        prior_samples = self.sample_prior(num_samples=num_samples)
        return self.random_state.negative_binomial(n=self.r, p=prior_samples)

    def fit(self, data=None, sum_stats=None, alpha=None, beta=None, r=None):
        """
        Fit the model using the prior and available data.

        Parameters
        ----------
        data: ndarray, optional
            nx1 array of the sample data, data OR sum_stats must be specified.
            Defaults to data if both are specified.
        sum_stats: tuple(int, int), optional
            Summary statistics, a tuple representing (num_samples, num_events).
            num_trials is the total number of trials (denominator of rate), must
            be >= 0. num_successes is the number of successful trials (numerator
            of rate), must be >= 0.
        alpha : float, optional
            shape prior (number of successes),
            must be specified in __init__() or fit(), must be > 0
        beta : float, optional
            scale prior (number of failures),
            must be specified in __init__() or fit(), must be > 0
        r : float
            dispersion parameter, number of failures until the experiment is
            stopped, must be specified in __init__() or fit(), must be > 0

        Returns
        -------

        """
        self._validate_prior_parameters(alpha=alpha, beta=beta, r=r)

        if data is not None:
            num_trials, num_successes = data.shape[0], data.sum()
        elif sum_stats is not None:
            num_trials, num_successes = sum_stats
        else:
            raise ValueError("Please specify either data or sum_stats input.")

        self.alpha_s = self.alpha + self.r * num_trials
        self.beta_s = self.beta + num_successes
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

        return self.random_state.beta(a=self.alpha_s, b=self.beta_s,
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
        posterior_samples : ndarray
            An array of samples from the fitted posterior
        """

        posterior_samples = self.sample_posterior(num_samples=num_samples)
        return self.random_state.negative_binomial(n=self.r,
            p=posterior_samples)

################################################################################
################################################################################

class DirichletMultinomial(_blueprint.ConjugateModel):
    """
    Dirichlet Multinomial Model (Equivalent to Categorical Dirichlet Model)

    Prior: Dirichlet Distribution D(alpha)
    Likelihood: Multinomial Distribution Bi(n, p)
    Parameter of Interest: Probability Class K=k (p)

    Assumption: Number of classes (K) is known

    Notes
    ----------
    Section 5.1 in  "A Compendium of Conjugate Priors" by Daniel Fink
    """

    def __init__(self, alpha=None,  *args, **kwargs):
        """
        Initialize the model object.

        Parameters
        ----------
        alpha : np.array, optional
            an n dimensional vector parametrizing the dirichlet prior, all
            values in vector must be must be > 0,
            must be specified in __init__() or fit()
        random_state : np.random.RandomState, optional
            numpy object defining the random state to use for sampling, defaults
            to `np.random`

        Returns
        -------
        None
        """

        super(DirichletMultinomial, self).__init__(*args, **kwargs)

        self.alpha = np.asarray(alpha).reshape(-1) if alpha is not None else None
        self.alpha_s = None

        if self.alpha is not None and not np.all(self.alpha > 0):
            raise ValueError("Elements of input alpha must be greater than 0.")

    def _validate_prior_parameters(self, alpha):
        """utility to validate prior parameters"""

        alpha = np.asarray(alpha).reshape(-1) if alpha is not None else None
        self.alpha = check_input_state(alpha, self.alpha, "alpha")

        if self.alpha is not None and not np.all(self.alpha > 0):
            raise ValueError("Elements of input alpha must be greater than 0.")

    def sample_prior(self, num_samples=1, alpha=None):
        """
        Sample from the prior.

        Parameters
        ----------
        num_samples : int
            the number of desired samples from the posterior
        alpha : np.array, optional
            an n dimensional vector parametrizing the dirichlet prior, all
            values in vector must be must be > 0,
            must be specified in __init__() or fit()

        Returns
        -------
        prior_samples : ndarray
            An array of samples from the prior
        """
        self._validate_prior_parameters(alpha=alpha)

        return self.random_state.dirichlet(alpha=self.alpha, size=num_samples)

    def sample_prior_predictive(self, num_samples=1, alpha=None, N=1):
        """
        Sample from the prior predictive.

        Parameters
        ----------
        num_samples : int
            the number of desired samples from the posterior
        alpha : np.array, optional
            an n dimensional vector parametrizing the dirichlet prior, all
            values in vector must be must be > 0,
            must be specified in __init__() or fit()
        N : int
            The number of observations for each sample from the multinomial
            distribution, must be greater than 0

        Returns
        -------
        prior_samples : ndarray
            An array of samples from the prior
        """
        self._validate_prior_parameters(alpha=alpha)

        if not isinstance(N, int):
            raise ValueError("Paramter N must be an integer.")
        if N <= 0:
            raise ValueError("Paramter N must be greater than 0.")

        prior_samples =  self.sample_prior(num_samples=num_samples)
        return np.asarray([
            self.random_state.multinomial(n=N, pvals=p)
            for p in prior_samples
        ])

    def fit(self, data=None, sum_stats=None, alpha=None):
        """
        Fit the model using the prior and available data.

        Parameters
        ----------
        data: ndarray, optional
            nxk array of the sample data, data OR sum_stats must be specified.
            Defaults to data if both are specified. k = number of categories.
        sum_stats: ndarray, optional
            Summary statistics, a 1xk dimensional vector representing the count
            of overservations across all categories.
        alpha : np.array, optional
            an n dimensional vector parametrizing the dirichlet prior, all
            values in vector must be must be > 0,
            must be specified in __init__() or fit()

        Returns
        -------

        """
        self._validate_prior_parameters(alpha=alpha)

        if data is not None:
            counts = np.asarray(data).sum(axis=0)
        elif sum_stats is not None:
            counts = np.asarray(sum_stats).reshape(-1)
        else:
            raise ValueError("Please specify either data or sum_stats input.")

        if self.alpha.shape != counts.shape:
            raise ValueError("Prior and counts dimensions fo not match: "
                "{} vs {}".format(self.alpha.shape, counts.shape))

        self.alpha_s = self.alpha + counts
        self.fitted = True

        return self.alpha_s

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

        return self.random_state.dirichlet(alpha=self.alpha_s, size=num_samples)

    @check_fitted
    def sample_posterior_predictive(self, num_samples=1, N=1):
        """
        Sample from the posterior predictive.

        Parameters
        ----------
        num_samples : int
            the number of desired samples from the posterior
        N : int
            The number of observations for each sample from the multinomial
            distribution, must be greater than 0

        Returns
        -------
        posterior_samples : ndarray
            An array of samples from the fitted posterior
        """

        if not isinstance(N, int):
            raise ValueError("Paramter N must be an integer.")
        if N <= 0:
            raise ValueError("Paramter N must be greater than 0.")

        posterior_samples = self.sample_posterior(num_samples=num_samples)
        return np.asarray([
            self.random_state.multinomial(n=N, pvals=p)
            for p in posterior_samples
        ])

DirichletCategorical = DirichletMultinomial

################################################################################
################################################################################

class BetaBinomialHyperGeometeric(_blueprint.ConjugateModel):
    """
    Beta-Binomial HyperGeometeric Model

    Prior: Beta-Binomial Distribution Bi(N, p=B(alpha, beta))
    Likelihood: HyperGeometeric Distribution HG(N, K, n)
    Parameter of Interest: Number of Unobserved Successes (M)

    Notes
    ----------
    Section 2.4 in  "A Compendium of Conjugate Priors" by Daniel Fink
    """

    def __init__(self, alpha=None, beta=None, N=None, *args, **kwargs):
        """
        Initialize the model object.

        Parameters
        ----------
        alpha : float, optional
            shape prior (number of successes),
            must be specified in __init__() or fit(), must be > 0
        beta : float, optional
            scale prior (number of failures),
            must be specified in __init__() or fit(), must be > 0
        N : int, optional
            the total size of the population being sampled without replacement,
            must be specified in __init__() or fit(), must be > 0
        random_state : np.random.RandomState, optional
            numpy object defining the random state to use for sampling, defaults
            to `np.random`

        Returns
        -------
        None
        """

        super(BetaBinomialHyperGeometeric, self).__init__(*args, **kwargs)

        self.alpha = alpha
        self.beta = beta
        self.N = N
        self.alpha_s = None
        self.beta_s = None
        self.N_s = N

        check_input_gt_zero(self.alpha, "alpha")
        check_input_gt_zero(self.beta, "beta")
        check_input_gt_zero(self.N, "N")

    def _validate_prior_parameters(self, alpha, beta, N):
        """utility to validate prior parameters"""

        self.alpha = check_input_state(alpha, self.alpha, "alpha")
        self.beta = check_input_state(beta, self.beta, "beta")
        self.N = check_input_state(N, self.N, "N")

        check_input_gt_zero(self.alpha, "alpha")
        check_input_gt_zero(self.beta, "beta")
        check_input_gt_zero(self.N, "N")

    def sample_prior(self, num_samples=1, alpha=None, beta=None, N=None):
        """
        Sample from the prior.

        Parameters
        ----------
        num_samples : int
            the number of desired samples from the posterior
        alpha : float, optional
            shape prior (number of successes),
            must be specified in __init__() or fit(), must be > 0
        beta : float, optional
            scale prior (number of failures),
            must be specified in __init__() or fit(), must be > 0
        N : int, optional
            the total size of the population being sampled without replacement,
            must be specified in __init__() or fit(), must be > 0

        Returns
        -------
        prior_samples : ndarray
            An array of samples from the prior
        """
        self._validate_prior_parameters(alpha=alpha, beta=beta, N=N)

        p = np.random.beta(a=self.alpha, b=self.beta, size=num_samples)
        return np.random.binomial(n=self.N, p=p)

    def sample_prior_predictive(self, *args, **kwargs):
        """
        sample_prior_predictive is not avilable for this model.
        """
        super().sample_prior_predictive()

    def fit(self, data=None, sum_stats=None, alpha=None, beta=None, N=None):
        """
        Fit the model using the prior and available data.

        Parameters
        ----------
        data: ndarray, optional
            nx1 array of the sample data, data OR sum_stats must be specified.
            Defaults to data if both are specified.
        sum_stats: tuple(int, int), optional
            Summary statistics, a tuple representing (n, successes). n is the
            number of samples drawn without replacement (maximum sample is
            n = N). successes is the number of successes out of n samples.
        alpha : float, optional
            shape prior (number of successes),
            must be specified in __init__() or fit(), must be > 0
        beta : float, optional
            scale prior (number of failures),
            must be specified in __init__() or fit(), must be > 0
        N : int, optional
            the total size of the population being sampled without replacement,
            must be specified in __init__() or fit(), must be > 0

        Returns
        -------
        alpha_s : float
            posterior shape
        beta_s : float
            posterior scale
        N_s : int
            since N is assumed to be known, this is simply N - n (the total
            population minus the sample size)
        """
        self._validate_prior_parameters(alpha=alpha, beta=beta, N=N)

        if data is not None:
            n, successes = data.shape[0], data.sum()
        elif sum_stats is not None:
            n, successes = sum_stats
        else:
            raise ValueError("Please specify either data or sum_stats input.")

        if n >= self.N:
            raise ValueError("Sample size n cannot exceed total population size N.")
        if successes > n:
            raise ValueError("Sample size n cannot be fewer than the number of successes.")

        self.alpha_s = self.alpha + successes
        self.beta_s = self.beta + n - successes
        self.N_s = self.N - n
        self.fitted = True

        return self.alpha_s, self.beta_s, self.N_s

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

        p = np.random.beta(a=self.alpha_s, b=self.beta_s, size=num_samples)
        return np.random.binomial(n=self.N_s, p=p)

    @check_fitted
    def sample_posterior_predictive(self, *args, **kwargs):
        """
        sample_posterior_predictive is not avilable for this model.
        """
        super().sample_posterior_predictive()

################################################################################
################################################################################

class BetaGeometric(_blueprint.ConjugateModel):
    """
    Beta Geometric Model

    Prior: Beta Distribution B(alpha, beta)
    Likelihood: Geometeric Distribution Geo(p)
    Parameter of Interest: Probability of Success (p)

    Notes
    ----------
    TODO: add derivation of conjugate model
    """

    def __init__(self, alpha=None, beta=None, *args, **kwargs):
        """
        Initialize the model object.

        Parameters
        ----------
        alpha : float, optional
            shape prior (number of successes),
            must be specified in __init__() or fit(), must be > 0
        beta : float, optional
            scale prior (number of failures),
            must be specified in __init__() or fit(), must be > 0
        random_state : np.random.RandomState, optional
            numpy object defining the random state to use for sampling, defaults
            to `np.random`

        Returns
        -------
        None
        """

        super(BetaGeometric, self).__init__(*args, **kwargs)

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
            shape prior (number of successes),
            must be specified in __init__() or fit(), must be > 0
        beta : float, optional
            scale prior (number of failures),
            must be specified in __init__() or fit(), must be > 0

        Returns
        -------
        prior_samples : ndarray
            An array of samples from the prior
        """
        self._validate_prior_parameters(alpha=alpha, beta=beta)

        return self.random_state.beta(a=self.alpha, b=self.beta,
                                      size=num_samples)

    def sample_prior_predictive(self, num_samples=1, alpha=None, beta=None):
        """
        Sample from the prior.

        Parameters
        ----------
        num_samples : int
            the number of desired samples from the posterior
        alpha : float, optional
            shape prior (number of successes),
            must be specified in __init__() or fit(), must be > 0
        beta : float, optional
            scale prior (number of failures),
            must be specified in __init__() or fit(), must be > 0

        Returns
        -------
        prior_samples : ndarray
            An array of samples from the prior
        """
        self._validate_prior_parameters(alpha=alpha, beta=beta)

        prior_samples = self.sample_prior(num_samples=num_samples)
        return self.random_state.geometric(p=prior_samples)

    def fit(self, data=None, sum_stats=None, alpha=None, beta=None):
        """
        Fit the model using the prior and available data.

        Parameters
        ----------
        data: ndarray, optional
            nx1 array of the sample data, data OR sum_stats must be specified.
            Defaults to data if both are specified.
        sum_stats: tuple(int, int), optional
            Summary statistics, a tuple representing (num_trials, num_successes).
            num_trials is the total number of trials (denominator of rate),
            must be >= 0. num_successes is the number of successful trials
            (numerator of rate), must be >= 0.
        alpha : float, optional
            shape prior (number of successes),
            must be specified in __init__() or fit(), must be > 0
        beta : float, optional
            scale prior (number of failures),
            must be specified in __init__() or fit(), must be > 0

        Returns
        -------

        """
        self._validate_prior_parameters(alpha=alpha, beta=beta)

        if data is not None:
            num_trials, num_successes = data.shape[0], data.sum()
        elif sum_stats is not None:
            num_trials, num_successes = sum_stats
        else:
            raise ValueError("Please specify either data or sum_stats input.")

        self.alpha_s = self.alpha + num_trials
        self.beta_s = self.beta + num_successes - num_trials
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

        return self.random_state.beta(a=self.alpha_s, b=self.beta_s,
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
        posterior_samples : ndarray
            An array of samples from the fitted posterior
        """

        posterior_samples = self.sample_posterior(num_samples=num_samples)
        return self.random_state.geometric(p=posterior_samples)

################################################################################
################################################################################
