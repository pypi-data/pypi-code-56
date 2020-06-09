"""This module defines classes for
intra-group and inter-group precision of trait parameters
in an OrdinalItemResponseModel.

The class instances are similar to frozen scipy.stats distribution objects,
but extend functionality by allowing the objects to adapt to observed data.

*** Main Classes:

TraitPrecisionWithinGroup -- Wishart distribution of full precision matrix,
    i.e., inverse of covariance matrix, of individual trait vectors.
    **** might be diagonal, if we require latent traits to be orthogonal ****
    **** but why should they have to be orthogonal ??? *******

TraitPrecisionAmongGroups -- gamma distribution of diagonal precision (inverse variance)
    for the group trait mean variations among groups.
"""
import numpy as np
from scipy.special import multigammaln, psi, gammaln
from scipy.stats import wishart

PRIOR_PRECISION_DELTA = 0.001
# Prior df of within-group Wishart distribution is
# df = D - 1 + PRIOR_PRECISION_DELTA, where
# df = approximate weight of prior precision re. one individual subject

PRIOR_SCALE_WITHIN = 1.
# = approximate scale of individual trait precision within groups

PRIOR_A_AMONG = 0.001
PRIOR_B_AMONG = 0.001
# = prior a, b parameters for prior_precision_among


# ---------------------------------------------- prior precision objects:
def prior_precision_among(n_traits):
    """
    :param n_traits: number of model traits
    :return: prior TraitPrecisionAmongGroups object
    """
    return TraitPrecisionAmongGroups(a=PRIOR_A_AMONG,
                                     b=np.ones(n_traits) * PRIOR_B_AMONG)


def prior_precision_within(n_traits):
    """
    :param n_traits: number of model traits
    :return: prior TraitPrecisionWithinGroup object
    """
    nu = n_traits - 1 + PRIOR_PRECISION_DELTA
    # = degrees-of-freedom to make the prior just barely proper
    # We need a PROPER prior to be able to calculate relative entropy
    # between posterior and prior models.
    return TraitPrecisionWithinGroup(df=nu,
                                     scale=np.eye(n_traits) * PRIOR_SCALE_WITHIN / nu)


# ---------------------------------------------------------------------------
class TraitPrecisionWithinGroup:
    """Wishart distribution of a symmetric precision matrix Lambda of a Gaussian vector
    The probability density function is
    p(Lambda) = (1/C) |Lambda|**((nu - p - 1)/2) exp(- trace(inv(V) Lambda)/2), where
        V = symmetric scale matrix,
        p = length of corresponding Gaussian vector
        nu = degree of freedom parameter >= p,
        Lambda.shape == V.shape == (p, p)
        C = |V|**(nu/2) 2**(nu p / 2) Gamma_p(nu/2) is the normalization factor
    """
    def __init__(self, scale, df=None):
        """
        :param scale: array or array-like symmetric scale matrix V
        """
        self.scale = np.asarray(scale)
        n_traits = len(scale)
        if df is None:
            df = n_traits + PRIOR_PRECISION_DELTA
        self.df = df

    def __repr__(self):
        return self.__class__.__name__ + f'(df= {self.df}, scale= \n {self.scale})'

    @property
    def prior(self):
        return prior_precision_within(self.n_traits)

    @property
    def n_traits(self):
        return len(self.scale)

    @property
    def inv_scale(self):
        return np.linalg.inv(self.scale)

    @property
    def mean(self):
        """E{self}"""
        return self.df * self.scale

    @property
    def mean_inv(self):
        """E{ inv(self) }"""
        if self.df > self.n_traits + 1:
            return self.inv_scale / (self.df - self.n_traits - 1)
        else:
            # mean_inv is undefined
            return np.full_like(self.scale, np.nan)

    @property
    def mode_inv(self):
        """Mode of inv(self) = most probable corresponding covariance matrix
        """
        return self.inv_scale / (self.df + self.n_traits + 1)

    @property
    def mean_log_det(self):
        """E{ ln |self| }
        (self is positive definite, so sign of determinant is always = 1.)
        """
        (s, log_det_scale) = np.linalg.slogdet(self.scale)
        return multi_psi(self.df / 2, self.n_traits) + self.n_traits * np.log(2) + s * log_det_scale

    # def logpdf(self, x):
    #     """ln pdf(x | self), using scipy.stats.wishart
    #     :param x: 2D array or array-like list
    #     :return: lp = scalar lp = ln pdf(x | self)
    #
    #     NOTE: scipy.stats.wishart can do logprob for matrices staced along 3rd axis
    #     but we do not use it.
    #     """
    #     return wishart.logpdf(x, df=self.df, scale=self.scale)

    def rvs(self, size=1):
        """Samples from Wishart distribution
        :param size: scalar integer number of sample matrices
        :return: tau = 3D array
            tau[..., :, :] = ...-th random precision matrix
            tau.shape == (*size, *self.scale.shape)
        """
        return wishart.rvs(df=self.df, scale=self.scale, size=size)

    # ------------------------------------------- MAP learning:
    def adapt(self, group_cov):
        """Update distribution parameters using observed data and prior.
        :param group_cov: iterable of lists of covariance-matrix samples
            for vectors assumed to have precision matrix == self.
            group_cov[g][s] = 2D array of mean current estimated cov for s-th subject in g-th group
        :return: - KLdiv(self || self.prior)
        Result: updated internal parameters of self
        """
        prior = self.prior
        n_s = 0
        cov = np.zeros((self.n_traits, self.n_traits))
        for c in group_cov:
            n_s += len(c)
            cov += np.sum(c, axis=0)
        inv_scale = prior.inv_scale + cov
        self.scale = np.linalg.inv(inv_scale)
        self.df = prior.df + n_s
        return - self.relative_entropy(prior)

    def relative_entropy(self, othr):
        """Kullback-Leibler divergence between self and othr
        :param othr: single instance of same class as self
        :return: scalar KLdiv(q || p) = E_q{ln q(x) / p(x)}, where q = self and p = othr
        Method: Using notation D = self.n_traits, V = self.prec,
        KLdiv = (q.df - p.df) * E{log_det(self)} / 2
            - (q.df - p.df) * ln(2) * D / 2
            + (p.df * log_det(p.V) - q.df * log_det(q.V)) / 2
            + trace[(inv(p.V) - inv(q.V)) * E{self}] / 2
            + gammaln_D(p.df/2) - gammaln_D(q.df/2)
        where
            E{log_det(self)} = psi_D(q.df/2) + D * ln(2) + log_det(q.V)
            E{self} = q.df * q.V
        = (q.df - p.df) * psi_D(q.df/2) / 2
            + p.df * (log_det(p.V) - log_det(q.V)) / 2
            + trace[(inv(p.V) - inv(q.V)) q.V] * q.df / 2
            + gammaln_D(p.df/2) - gammaln_D(q.df/2)
        """
        d = self.n_traits
        Vpinv_Vq = np.dot(othr.inv_scale, self.scale)
        # ******* try linalg.solve instead   *********
        (s, log_det_VV) = np.linalg.slogdet(Vpinv_Vq)
        return (0.5 * ((self.df - othr.df) * multi_psi(self.df/2, d)
                       - othr.df * s * log_det_VV
                       + (np.trace(Vpinv_Vq) - d) * self.df
                       )
                + multigammaln(othr.df/2, d) - multigammaln(self.df/2, d)
                )

    def prune(self, keep):
        """Prune away un-necessary trait dimensions
        :param keep: 1D boolean array indicating traits to keep
        :return: None
        Result: self.scale reduced
        """
        self.scale = self.scale[keep, :][:, keep]

    def standardize(self, s):
        """Standardize for unity trait variance, as estimated externally
        :param s: 1D array with scale factors, one for each trait
        :return: None
        Method: covariance to be divided by s, so precision should be multiplied
        """
        self.scale = self.scale * s * s[:, None]


# -------------------------------------------------------------------------
class TraitPrecisionAmongGroups:
    """Array of independent gamma distributions for model parameter psi,
    representing diagonal prior precision matrix of the group mean trait
    among different ItemResponseGroup instances
    """
    def __init__(self, a=1., b=1.):
        self.a = a
        self.b = np.array(b).reshape((-1,))
        # a is scalar, b must be 1D array

    def __repr__(self):
        return self.__class__.__name__ + f'(a={self.a}, b={self.b})'

    @property
    def prior(self):
        return prior_precision_among(len(self.b))

    @property
    def scale(self):
        return 1. / self.b

    @property
    def inv_scale(self):
        return self.b

    @property
    def mean(self):
        return self.a / self.b

    @property
    def mean_inv(self):
        if self.a > 1:
            return self.b / (self.a - 1)
        else:
            return np.full(self.b.shape, np.nan)

    # @property
    # def var(self):
    #     return self.a / self.b**2

    @property
    def mean_log(self):
        """E{ log( self ) }"""
        return psi(self.a) - np.log(self.b)

    def relative_entropy(self, prior):
        """Kullback-Leibler divergence between GammaRV q and p,
        :param prior: prior with same class and structure
        :return: KLdiv( self || prior ) = E{ ln pdf(x | self) / pdf(x | prior) }_self
        Method:
        pdf(x) = prod_d C(a, b_d) x^{a-1} exp(-b_d x_d)
        C(a, b_d) = b_d^a / Gamma(a)
        """
        pq_b_ratio = prior.b / self.b
        return np.sum(gammaln(prior.a) - gammaln(self.a)
                      - prior.a * np.log(pq_b_ratio)
                      + (self.a - prior.a) * psi(self.a)
                      - self.a * (1 - pq_b_ratio)
                      )

    # ------------------------------------------- MAP learning:
    def adapt(self, mean2_mu):
        """Adapt to given data
        :param mean2_mu: 2D array-like nested list of mean square group property mu
            mean2_mu[g][d] =  E{mu_gd^2} for d-th trait of g-th group
            len(mean2_mu[g]) == n_traits == len(self.b) == number of groups
        :return: ll = KLdiv(self || prior) after adjustment
        2019-08-18, changed for NON-tied self
        """
        prior = self.prior
        mean2 = np.array(mean2_mu)
        (n_groups, n_traits) = mean2.shape
        # self.a = prior.a + n_traits * n_groups / 2
        self.a = prior.a + n_groups / 2
        self.b = prior.b + np.sum(mean2, axis=0) / 2  # sum across g and d
        return - self.relative_entropy(prior)

    def prune(self, keep):
        """Prune away un-necessary trait dimensions
        :param keep: 1D boolean array indicating traits to keep
        :return: None
        Result: self.b reduced
        """
        self.b = self.b[keep]

    def standardize(self, s):
        """Standardize for unity trait variance, as estimated externally
        :param s: 1D array with scale factors, one for each trait
        :return: None
        Method: covariance to be divided by mean(s**2)
        """
        self.b = self.b / np.mean(s**2)


# ---------------------------------------- module help functions:

def multi_psi(a, d):
    """Multivariate psi function
    = first derivative of scipy.special.multigammaln(a, d) w.r.t a
    = sum( psi( a + (1-j)/2) for j = 1,...,d ) (Wikipedia)
    = sum( psi( a - (j-1)/2) for j = 1,...,d )
    = sum( psi( a - j/2) for j = 0,...,d-1 )
    """
    return np.sum(psi(a - np.arange(d) / 2))


# ------------------------------------------------------------- Module TEST:

if __name__ == '__main__':
    from scipy.stats import norm

    # --------------------------- simulated trait data:
    n_groups = 2
    n_samples = 10
    n_subjects = 20
    n_traits = 3

    theta = norm.rvs(size=(n_groups, n_samples, n_subjects, n_traits))

    print('*** Testing TraitPrecisionAmongGroups:\n')

    prec_among = prior_precision_among(n_traits)
    print(prec_among)
    print(f'mean= {prec_among.mean}')
    print(f'relative_entropy(prior)=', prec_among.relative_entropy(prec_among.prior))

    mean2_mu = np.mean(theta**2, axis=(1,2))  # mean across samples and subjects
    print('mean2_mu=', mean2_mu)

    ll=prec_among.adapt(mean2_mu=mean2_mu)
    print('adapted: ', prec_among)
    print('ll= ',ll)
    print(f'mean= {prec_among.mean}')
    print(f'relative_entropy(prior)=', prec_among.relative_entropy(prec_among.prior))

    print('\n*** Testing TraitPrecisionWithinGroup:\n')

    prec_within = prior_precision_within(n_traits)
    print(prec_within)
    print(f'mean=\n{prec_within.mean}')
    print(f'mean_inv=\n{prec_within.mean_inv}')
    print(f'mode_inv=\n{prec_within.mode_inv}')
    print(f'relative_entropy(prior)=', prec_within.relative_entropy(prec_within.prior))

    group_cov = np.einsum('gnsi, gnsj -> gsij',
                          theta, theta) / n_samples

    print('adapting to group_cov')
    print('mean empirical group_cov=\n', np.mean(group_cov, axis=(0, 1)))
    print('')

    ll = prec_within.adapt(group_cov)
    print('adapted: ', prec_within)
    print('ll= ', ll)
    print(f'mean=\n{prec_within.mean}')
    print(f'mean_inv=\n{prec_within.mean_inv}')
    print(f'mode_inv=\n{prec_within.mode_inv}')
    print(f'mean_log_det={prec_within.mean_log_det}')
    print(f'relative_entropy(prior)=', prec_within.relative_entropy(prec_within.prior))

