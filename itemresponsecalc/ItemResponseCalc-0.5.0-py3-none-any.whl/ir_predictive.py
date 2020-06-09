"""This module defines classes representing the predictive trait distributions
for an item_response_model.OrdinalItemResponseModel instance,
trained on subject responses.
"""
import numpy as np

RANDOM = np.random.default_rng()
# = module-global random generator, Numpy 1.17


class GaussianGivenParam:
    """Gaussian distribution of a vector-valued random variable
    with parameter vector mu and precision matrix tau,
    which may be either fixed numpy arrays or random variables.

    Used for PREDICTIVE multivariate distributions
    that may be an infinite mixture of Student-t distributions,
    which has no known exact form.

    Nevertheless,
    this class can draw random variates from the exact predictive distribution,
    and calculate a good approximation to its covariance.
    """
    def __init__(self, mu, tau):
        """
        :param mu: 1D array or random-variable instance for the mean
        :param tau: 2D array or random-variable instance for the precision matrix
        """
        self.mu = mu
        self.tau = tau

    def __repr__(self):
        return (self.__class__.__name__ + '('
                + '\n\t mu= ' + self.mu.__class__.__name__ + ','
                + '\n\t tau= ' + self.tau.__class__.__name__
                + ')')

    def cov(self):
        """Expected covariance matrix,
        averaged across parameter distributions
        """
        if isinstance(self.tau, np.ndarray):
            c = np.linalg.inv(self.tau)
        else:
            c = np.linalg.inv(self.tau.mean_inv)
        # c = expected conditional cov, given mu
        if isinstance(self.mu, np.ndarray):
            return c
        else:
            return self.mu.cov + c

    def rvs(self, size=1):
        """Random vectors drawn from self,
        based on random samples of parameters
        :param size: integer number of desired samples
        :return: 2D array x, with
            x[n, :] = n-th sample drawn from self

        Method: scipy.stats.multivariate_normal can only use 1D mean and 2D cov,
        so we must do it directly using eigen-analysis of the precision matrix
        """
        if isinstance(self.mu, np.ndarray):
            m = self.mu
        else:
            m = self.mu.rvs(size=size)
        if isinstance(self.tau, np.ndarray):
            (e_val, e_vec) = np.linalg.eigh(self.tau)
        else:
            (e_val, e_vec) = np.linalg.eigh(self.tau.rvs(size=size))
        # random deviations with zero mean:
        if np.isscalar(size):
            z_shape = (size, m.shape[-1])
        else:
            z_shape = (*size, m.shape[-1])
        z = RANDOM.standard_normal(size=z_shape)
        # = standard normal independent random numbers
        return m + np.einsum('...i, ...j, ...ji -> ...j',
                             z, 1. / np.sqrt(e_val), e_vec)


# -------------------------------------------------------- TEST:
if __name__ == '__main__':
    from scipy.stats import multivariate_normal as mnorm

    # Testing some module functions

    m = np.array([1.,2.,3., 4.])
    x = mnorm.rvs(mean=m, cov=np.eye(3))
    print('x.shape= ', x.shape)
    print('x=\n', x)