"""Module defining a Bayesian IRT model for the responses of a group of subjects
to a questionnaire with several items.
Each item response is assumed to be determined by the outcome of a
latent random variable with a subject-specific location.

Each uni-dimensional subject trait may determine responses to one or several items.

This model is implemented only for data with ORDINAL responses.

*** Main Classes:

ResponseGroup -- model for a group of subjects for which
    response data are available for each item for each subject.

GroupMeanTrait -- model for Gaussian distribution of mean trait vector for one group

Arne Leijon, 2019-07-08, first version
2019-07-23, cannot use SummaryResponseGroup!
2019-08-11, delete class SummaryResponseGroup
2019-08-11, use scales.trait_sel.mean as item_trait_weight
2019-08-15, new initialize method, incl. theta randomization
2019-08-17, single ResponseGroup class, generalized for tied or non-tied prec_among
2019-08-20, ResponseGroup.adapt returns self, to allow multi-processing
"""
import numpy as np
# from scipy.stats import multivariate_normal  # replaced by np.random.Generator

from samppy import hamiltonian_sampler as ham
from samppy.sample_entropy import entropy_nn_approx as entropy
from .ir_predictive import GaussianGivenParam

from .safe_logistic import logistic

import logging
logger = logging.getLogger(__name__)

logger.setLevel(logging.INFO)
# logger.setLevel(logging.DEBUG)

ham.VECTOR_AXIS = 1  # just in case default has changed...

multivariate_normal = np.random.default_rng().multivariate_normal
# = random generator for multivariate Gaussian vector

# ----------------------------------------------------------


# ---------------------------------------------- Respondent Group Model:

class ResponseGroup:
    """Model representing subjects' latent traits in an OrdinalItemResponseModel,
    learned by adaptation to individual item responses for each subject.
    The trait distribution is represented by sampling.
    """
    @classmethod
    def initialize_by_item(cls, subject_responses, scales, trait_scale,
                           name,
                           n_samples=20):
        """Initialize trait values by sampling, on trait for each item
        :param subject_responses: iterable yielding subject responses as a list with
            g_subjects[s][i] = integer index of response to i-th item,
            coded with origin==1 for the first response alternative,
            and missing response encoded as 0.
            Recoded later to python origin 0 for internal use.
        :param scales: list of ItemScale instances, one for each item
        :param trait_scale: scalar initially assumed scale of trait values
        :param n_samples: number of samples of the intra-subject distribution of trait values
        :param name: string identifying this group
        :return: single cls instance
        """
        # collect all response data in one array
        s_responses = np.array([s_r for s_r in subject_responses]).T
        # s_responses[i, s] = response-level index for i-th item by s-th subject
        # still with origin == 1, missing response == 0
        # n_items = len(s_responses)
        th = np.array([sc_i.sample_trait(r_i - 1, n_samples, trait_scale=trait_scale)
                       for (sc_i, r_i) in zip(scales, s_responses)])
        # th[i, m, s] = m-th sample for i-th item and s-th subject
        th = th.transpose((1, 2, 0))
        # th[m, s, i] = m-th sample of i-th item for s-th subject
        mu = GroupMeanTrait(loc=np.mean(th, axis=(0, 1)))
        logger.info(f'Initializing {repr(name)}'
                    + f' with {s_responses.shape[-1]} subjects')
        logger.debug('Initial item mu.loc= ' + np.array2string(mu.loc, precision=3))
        return cls(subject_responses=s_responses,
                   theta=th,
                   mu=mu,
                   name=name)

    def __init__(self, subject_responses, theta, mu, name):
        """
        :param subject_responses: 2D array-like list with response data
            response[i, s] = integer ordinal response index for i-th item by s-th subject
            coded with origin==1 for the first response alternative,
        :param theta: 3D array with initial subject latent trait samples
            theta[n, s, t] = n-th sample of t-th trait for s-th subject
        :param mu: GroupMeanTrait instance representing current distribution of mean
        :param name: string with arbitrary label for this object
        NOTE: Internal property
        _response = 2D array of individual response indices, with
            response[i, s] = integer index of response to i-th item,
            encoded with origin==0, and missing response encoded as -1.
        The corresponding external property is
        subject_responses = _response + 1,
        with origin == 1 and missing response == 0, for external presentation.
        """
        assert theta.ndim == 3, 'theta must be 3-dim numpy array'
        self._response = np.array(subject_responses) - 1
        (n_samples, self.n_subjects, self.n_traits) = theta.shape
        self.sampler = ham.HamiltonianSampler(fun=self.neg_logprob,
                                              jac=self.d_neg_logprob,
                                              x=theta.reshape(n_samples, -1),
                                              epsilon=0.3,
                                              n_leapfrog_steps=10)
        # NOTE: theta is stored only as sampler.x
        # args for neg_logprob and d_neg_logprob are defined later, before each call
        self.mu = mu
        self.name = name
        self.ll = None  # log likelihood saved here by adapt step

    def __repr__(self):
        return (self.__class__.__name__ + f'(name= {repr(self.name)},'
                + f'\n\t subject_responses= array with {len(self._response)} responses'
                + f' by {self.n_subjects} subjects,'
                + f'\n\t theta= array with shape= {self.theta.shape},'
                + '\n\t mu= ' + self.mu.__repr__()
                + ')')

    def cov_all(self):
        """Covariance matrix across all samples, all subjects,
        used only for initial rotation of trait dimensions
        as determined externally
        :return: c = 2D array covariance matrix
        """
        # m = np.mean(self.theta, axis=(0,1))
        logger.debug('Initial cov without mean subtraction')
        x = self.theta.reshape((-1, self.theta.shape[-1]))  # ***** - m
        c = np.cov(x, rowvar=False)
        # (e_val, e_vec) = np.linalg.eigh(c)  # **** only for test
        return c

    def transform_traits(self, proj):
        """Transform initial item-traits to (sub-)space defined by external PCA
        :param proj: 2D projection matrix with orthonormal COLUMN vectors
            proj[:, t] = unit vector for t-th trait
        :return: None
        self.theta and self.mu transformed to proj coordinate system
        """
        th = np.dot(self.theta, proj)
        self.n_traits = th.shape[-1]
        self.theta = th
        self.mu = GroupMeanTrait(loc=np.mean(th, axis=(0, 1)))
        logger.info(f'Transformed group {repr(self.name)} self.mu.loc= '
                    + np.array2string(self.mu.loc, precision=3, suppress_small=True))

    @property
    def subject_responses(self):
        """Subject responses as obtained from input files
        using the external encoding {1,..., L_i},
        with missing response == 0
        :return: r = 2D array with responses,
            r[s, i] = response by s-th subject to i-th item
        """
        return self._response + 1

    @property
    def n_samples(self):
        return self.sampler.x.shape[0]

    @property
    def theta(self):
        """Sample representation of current distribution of trait values
        for all subjects in this group
        :return: theta = 3D array of samples
            theta[n, s, t] = n-th sample of t-th trait for s-th subject
        """
        return self.sampler.x.reshape((self.n_samples, self.n_subjects, self.n_traits))

    @theta.setter
    def theta(self, th):
        """Store theta values in 2D array sampler.x
        :param th: 3D theta matrix
            th[n, s, t] = n-th sample of t-th trait for s-th subject
        :return: None
        """
        self.sampler.x = th.reshape((self.n_samples, -1))

    @property
    def mean_cov_theta(self):
        """Mean cov of current theta distribution for each subject
        averaged across samples.
        :return: c = 3D array with
        c[s] = mean covariance matrix for s-th subject =
        = E{ theta_s - mu)^T (theta_s - mu) }
        = E{ theta_s - mu.loc)^T (theta_s - mu.loc) } + mu.cov
        """
        th_diff = self.theta - self.mu.loc
        c = np.einsum('nsi, nsj -> sij',
                      th_diff, th_diff) / th_diff.shape[0]
        return c + self.mu.cov

    @property
    def entropy_theta(self):
        """Entropy of current theta distribution,
        estimated from samples by nearest-neighbor method
        :return: h_sum = scalar entropy, sum across all subjects
        """
        th = self.theta
        # h = entropy(self.sampler.x)
        # h = single estimate using all subjects in one operation.
        # But we know distributions are independent among subjects,
        # and Singh et al. (2016) showed convergence is slower with increasing dimension,
        # so an average across all subjects, at low dimension for each subject,
        # is most probably closer to the true value.
        h_sum = sum(entropy(th[:, s, :]) for s in range(th.shape[1]))
        return h_sum

    def adapt(self, scales, precision_within, precision_among):
        """One learning step for distribution of group theta values,
        and group mu property,
        using responses data and current distribution of item scale parameters.
        :param scales: list of ItemScale objects, one for each item
        :param precision_within: TraitPrecisionWithinGroup object defining
            current distribution of inter-individual precision matrix within every group
        :param precision_among: TraitPrecisionAmongGroups object defining
            current distribution of psi = scalar precision among group means
        :return: self updated, to allow multi-processing
        """
        _id = repr(self.name)  # used for logger output
        logger.debug(self.__class__.__name__ + f'[{_id}].adapt(...)')
        # ---------------------------------- adapt self.theta by Hamilton sampling
        tau = [sc.tau for sc in scales]
        weight = [sc.trait_sel.mean for sc in scales]
        # response thresholds, fixed during theta learning
        if np.any([np.any(np.isinf(tau_i)) for tau_i in tau]):
            logger.warning(f'{_id}: Infinite tau. Should not happen!')
        mean_precision_within = precision_within.mean
        mean_log_det_prec_within = precision_within.mean_log_det
        # = external parameters, constant during re-sampling of theta
        # but change between calls
        self.sampler.args = (tau, weight, mean_precision_within, mean_log_det_prec_within)
        max_steps=20
        # logger.debug(f'test sampler._rng.std_normal: {self.sampler._rng.standard_normal()}')
        try:
            self.sampler.safe_sample(min_steps=5, max_steps=max_steps)
            if self.sampler.n_steps >= max_steps:
                logger.warning(f'{_id}: Done {self.sampler.n_steps} = MAX allowed sampling steps')
            else:
                logger.debug(f'{_id}: Done {self.sampler.n_steps} sampling steps')
        #     if self.sampler.accept_rate > 0.95:  # ****** do this in samppy.safe_sample ??? ********
        #         self.sampler.epsilon *= 1.3
        #         logger.debug(f'{_id}: High sampler accept_rate; increased epsilon = {self.sampler.epsilon}')
        except ham.AcceptanceError:  # raised by sampler, even after reducing epsilon
            # logger.debug(f'* AcceptanceError {self}.adapt()')
            # self.sampler.epsilon *= (0.7 + 0.2 * uniform.rvs())  # ************** SKIP
            logger.warning((f'{_id}: AcceptanceError: accept_rate= {self.sampler.accept_rate:.2f} ' +
                            f'of {self.sampler.n_trajectories}; ' +
                            f'epsilon reduced to {self.sampler.epsilon:.5f}'))
            # ****** keep going anyway ********
        else:
            logger.debug(f'{_id}: Sampler accept_rate = {self.sampler.accept_rate:.1%}')
            logger.debug(f'{_id}: Sampler epsilon = {self.sampler.epsilon}')
        # --------------------------------- DONE distribution of theta
        LL = - np.mean(self.sampler.U)
        LL += self.mu.adapt(np.mean(self.theta, axis=0),
                            mean_precision_within,
                            precision_among)
        h = self.entropy_theta
        logger.debug(f'{_id}: LL={LL:.1f}, + entropy={h:.1f}')
        self.ll = LL + h
        logger.debug(self.__class__.__name__ + f'[{_id}].adapt(...) finished')
        return self

    def neg_logprob(self, x, tau, weight, mean_prec, mean_log_det_prec):
        """Negative log-likelihood for any sample subject trait vector
        :param x: 2D array of trait values as stored in self.sampler.x
            x[n, st] = n-th sample of (s,t)-th subject,trait value
        :param tau: list of 2D arrays with UPPER item response thresholds
            tau[i][m, l] = m-th sample of UPPER threshold for l-th response interval of i-th item
            EXCEPT the extreme at +inf
            tau[i].shape[-1] == L_i - 1; L_i = n ordinal response levels
        :param weight: list of 1D arrays of item trait weights
            weight[i][t] = i-th item weight for t-th trait
        :param mean_prec: 2D symmetric intra-group mean precision matrix
        :param mean_log_det_prec: scalar log det(precision matrix)
        :return: nlp = 1D vector of negative log-likelihood values
            nlp.shape == (x.shape[0],) == (self.n_samples,)
        """
        th = x.reshape((self.n_samples, self.n_subjects, self.n_traits))
        return (- self.logprob_by_theta(th, tau, weight)
                - self.prior_logprob(th, mean_prec, mean_log_det_prec))

    def d_neg_logprob(self, x, tau, weight, mean_prec, mean_log_det_prec):
        """Gradient of logprob for any sample subject trait vector
        :param x: 2D array of trait values as stored in self.sampler.x
            x[n, st] = n-th sample of (s,t)-th subject,trait value
        :param tau: list of 2D arrays with UPPER item response thresholds
            tau[i][m, l] = m-th sample of UPPER threshold for l-th response interval of i-th item
            EXCEPT the extreme at +inf
            tau[i].shape[-1] == L_i - 1; L_i = n ordinal response levels
        :param weight: list of 1D arrays of item trait weights
            weight[i][t] = i-th item weight for t-th trait
        :param mean_prec: 2D symmetric intra-group mean precision matrix
        :param mean_log_det_prec: scalar log det(precision matrix)
            NOT NEEDED to calculate gradient w.r.t. theta
        :return: dlp = 2D array of gradient row vectors, one for each sample
            dlp.shape == x.shape
        """
        th = x.reshape((self.n_samples, self.n_subjects, self.n_traits))
        dnlp = (- self.d_logprob_by_theta(th, tau, weight)
                - self.d_prior_logprob(th, mean_prec))
        return dnlp.reshape((self.n_samples, -1))

    def prior_logprob(self, theta, mean_prec, mean_log_det_prec):
        """Prior log-probability of theta, given current group mu
        :param theta: 3D reshaped array of traits
            theta[n, s, t] = n-th sample of t-th trait for s-th subject
        :param mean_prec: 2D array = mean precision matrix within this group
            externally calculated
        :param mean_log_det_prec: 2D mean log det precision matrix
            externally calculated
        :return: lp = 1D array, with lp[n] = n-th sample
        Method: prior theta_s is Gaussian with location self.loc and external prec matrix
        for each subject.
        """
        # th_diff = theta.reshape(self.n_samples, self.n_subjects, -1) - self.mu.loc  # ********
        th_diff = theta - self.mu.loc
        return 0.5 *(self.n_subjects * mean_log_det_prec
                     - np.einsum('nsi, ij, nsj -> n',
                                 th_diff, mean_prec, th_diff))

    def d_prior_logprob(self, theta, mean_prec):
        """Gradient of prior_log-probability of theta, given current group mu
        :param theta: 3D reshaped array of traits
            theta[n, s, t] = n-th sample of t-th trait for s-th subject
        :param mean_prec: 2D mean precision matrix within this group
        :return: dlp = 2D array with gradient sample vectors
            dlp.shape == theta.shape
        """
        # th_diff = theta.reshape(self.n_samples, self.n_subjects, -1) - self.mu.loc   # ******** again
        th_diff = theta - self.mu.loc
        # th_diff[n, s, t] = n-th sample, s-th subject, t-th trait
        # dlp_old = - np.einsum('nsi, ij -> nsj',
        #                       th_diff, mean_prec).reshape(theta.shape)
        dlp = - np.dot(th_diff, mean_prec)  # .reshape(theta.shape)
        return dlp

    def logprob_by_theta(self, theta, tau, weight):
        """log-likelihood of observed responses for any sample subject trait vector
        summed across all responses, averaged across threshold samples
        :param theta: 3D reshaped array of traits
            theta[n, s, t] = n-th sample of t-th trait for s-th subject
        :param tau: list of 2D arrays of response thresholds, EXCEPT extremes
            tau[i][m, l] =  m-th sample of UPPER interval limit for l-th response to i-th item
            tau[i].shape[-1] == L_i - 1; L_i = number of ordinal response levels
        :param weight: list of 1D arrays of item trait weights
            weight[i][t] = i-th item weight for t-th trait
        :return: lp = 1D vector of log-likelihood values
            lp.shape == (self.n_samples,)
        """
        # th = theta.reshape((self.n_samples, self.n_subjects, self.n_traits))  # **** already done !
        lp = [item_logprob_by_theta(theta, tau_i, w_i, r_i)
              for (tau_i, w_i, r_i) in zip(tau,
                                           weight,
                                           self._response)]
        # lp[i, n] = logprob for n-th theta sample for i-th item
        # lp = np.dot(self.trait_item_map, lp)
        return np.sum(lp, axis=0)

    def d_logprob_by_theta(self, theta, tau, weight):
        """Gradient of logprob w.r.t theta, for any given sample subject trait vector
        :param theta: 3D reshaped array of traits
            theta[n, s, t] = n-th sample of t-th trait for s-th subject
        :param tau: list of 2D arrays of response thresholds, EXCEPT extremes
            tau[i][m, l] =  m-th sample of UPPER interval limit for l-th response to i-th item
            tau[i].shape[-1] == L_i - 1; L_i = number of ordinal response levels
        :param weight: list of 1D arrays of item trait weights
            weight[i][t] = i-th item weight for t-th trait
        :return: dlp = 3D array of gradients, one for each sample
            dlp[n, s, t] = n-th sample gradient for t-th trait of s-th subject
            dlp[n, s, t] = d logprob(theta[n]) / d theta[n, s, t]
            dlp.shape == theta.shape
        """
        # th = theta.reshape((self.n_samples, self.n_subjects, self.n_traits))  # **** already done !
        dlp = [d_item_logprob_by_theta(theta, tau_i, w_i, r_i)
               for (tau_i, w_i, r_i) in zip(tau,
                                            weight,
                                            self._response)]
        # dlp[i, n, s, t] = n-th sample of grad logprob w.r.t theta for i-th item, s-th subject
        # dlp = np.einsum('ti, ins -> nst',
        #                 self.trait_item_map, dlp)
        dlp = np.sum(dlp, axis=0)
        # dlp[n, s, t] = n-th d_logprob_by_theta sample for t-th trait, s-th subject
        return dlp  # .reshape(dlp.shape[0], -1)  # shape == theta.shape

    def item_logprob_by_tau(self, tau_i, i, w_i=None):
        """log prob of observed responses for ONE item,
        summed across subjects, averaged across theta samples
        using current theta distribution.
        :param tau_i: tau_i[m, l] = m-th sample of UPPER interval limit for l-th response
            tau_i.shape[-1] == L_i - 1
        :param i: index of selected item
        :param w_i: (optional) 1D array with trait weights for this item
        :return: lp = 2D array, with lp[m, t] = m-th sample for t-th trait
        """
        r_i = self._response[i]
        # theta_i = self.theta[..., self.item_trait_index[i]]
        # theta_i[n, s] = n-th trait sample for s-th subject for this item
        (tau_low, tau_high) = response_interval(tau_i, r_i)
        # tau_low[m, s] and tau_high[m, s] are (low, high) interval limits
        th = self.theta[:, None, :, :]  # to allow broadcast
        # th[n, 0, s, t] = n-th sample of t-trait for s-th subject
        lp = log_prob_range(tau_low[..., None] - th, tau_high[..., None] - th)
        # lp[n, m, s, t] = n-th theta sample, m-th tau sample for s-th subject
        lp = np.sum(lp, axis=-2)
        lp = np.mean(lp, axis=0)
        # lp[m, t] = m-th tau sample, for t-th trait
        if w_i is None:
            return lp
        else:
            return np.dot(lp, w_i)

    def d_item_logprob_by_tau(self, tau_i, i, w_i):
        """Gradient of item_logprob_by_tau w.r.t. tau_i,
        summed across subjects, averaged across theta samples
        :param tau_i: tau_i[m, l] = m-th sample of UPPER interval limit for l-th response
            tau_i.shape[-1] == L_i - 1
        :param i: index of selected item
        :param w_i: (optional) 1D array with trait weights for this item
        :return: dlp = 3D array, with
            dlp[m, l, t] = d logprob(tau_i[m, :] / d tau_i[m, l], given t-th trait
            dlp.shape == (*tau_i.shape, self.n_traits)
        """
        r_i = self._response[i]
        # theta_i = self.theta[..., self.item_trait_index[i]]
        (tau_low, tau_high) = response_interval(tau_i, r_i)
        # tau_low[m, s] and tau_high[m, s] are (low, high) interval limits
        th = self.theta[:, None, :, :]  # to allow broadcast
        (da, db) = d_log_prob_range_dab(tau_low[..., None] - th, tau_high[..., None] - th)
        # da[n, m, s, t] = n-th theta sample, m-th tau sample for t-th trait of s-th subject
        # of derivative w.r.t. tau_low
        # db similar for tau_high
        da = np.dot(np.mean(da, axis=0), w_i)
        db = np.dot(np.mean(db, axis=0), w_i)
        # da[n, m, s] = n-th theta sample, m-th tau sample of s-th subject, same for db
        n_response_levels = tau_i.shape[-1] + 1
        r_bool = np.array([r_i == l
                           for l in range(n_response_levels)]).T
        dlp = np.dot(da, r_bool[:, 1:]) + np.dot(db, r_bool[:, :-1])
        # dlp[m, l] = derivative w.r.t tau_i[m, l], sum across all responses
        # when tau[m, l] is LOWER limit PLUS when it is UPPER limit
        return dlp

    # -------------------------------------- Predictive Models for result displays:
    def predictive_individual_cov(self, precision_within):
        """Covariance of the Predictive distribution of IRT traits
        for a RANDOM INDIVIDUAL
        in the sub-population represented by this subject group.
        :param precision_within: TraitPrecisionWithinGroup object defining
            current distribution of inter-individual precision matrix within every group
        :return: 2D array with covariance matrix

        Method: The exact predictive distribution is a continuous mixture
        of Student-t distributions.
        Samples from the exact distribution can be generated,
        but it may be sufficient to know the exact covariance
        derived from self.precision_within and self.precision_among
        The predictive location is simply = self.mu.loc
        """
        return precision_within.mean_inv + self.mu.cov

    def prune(self, keep):
        """Prune away un-necessary trait dimensions
        :param keep: 1D boolean array indicating traits to keep
        :return: None
        Result: self.theta and self.mu pruned
        """
        th = self.theta[..., keep]
        self.n_traits = np.sum(keep)
        self.theta = th
        self.mu.prune(keep)

    def standardize(self, s):
        """Standardize for unity trait variance, as estimated externally
        :param s: 1D array with scale factors, one for each trait
            s.shape[-1] == self.theta.shape[-1]
        :return: None
        Method: All trait samples down-scaled by s
        """
        self.theta = self.theta / s
        self.mu.standardize(s)

    def mean_response(self):
        """Mean rating across all items, disregarding any missing data
        used mainly to illustrate deviation re. corresponding mean trait
        :return: mean_r = 1D array
        """
        r = self.subject_responses
        # r[i, s] = integer ordinal response to i-th item by s-th subject
        # with origin 1, missing response = 0
        mean_r = np.sum(r, axis=0) / np.sum(r > 0, axis=0)
        return mean_r

    def scaled_subject_responses(self, item_scale_values):
        """Recoded subject responses on common interval scale
        :param item_scale_values: nested list with point-estimated scale values
            item_scale_values[i][r] = value for r-th response to i-th item
            assuming scale mean = 0, to be used for missing responses
        :return: sc_r = 2D array
            sc_r[i, s] = recoded response value for i-th item by s-th subject
            with missing responses recoded as zero
        """
        r = self._response
        # r[i, s] integer-encoded with origin=0, missing response == -1
        sc_r = np.array([v_i[np.maximum(0, r_i)]
                         for (v_i, r_i) in zip(item_scale_values, r)])
        sc_r[r < 0] = 0.
        return sc_r

    def predictive_mean(self):
        """Predictive distribution of MEAN IRT traits
        in the sub-population for which the subject data in self are representative.
        :return: GroupMeanTrait distribution object
        """
        return self.mu

    def predictive_individual(self, precision_within):
        """Predictive distribution of IRT traits for a RANDOM INDIVIDUAL
        in the sub-population for which the subject data in self are representative.
        :param precision_within: distribution instance for trait precision, given mean
        :return: PredictiveTrait object
        """
        return GaussianGivenParam(mu=self.mu, tau=precision_within)


# -------------------------------------------------------------------------
class GroupMeanTrait:
    """Gaussian distribution of group mean trait vector mu,
    defined by properties
    loc = location, learned from sampled trait vectors theta of ONE group of subjects,
    prec = precision matrix, learned externally by data from all groups
    """
    def __init__(self, loc, prec=None):
        self.loc = np.asarray(loc)
        if prec is None:
            self.prec = np.eye(len(loc))
        else:
            self.prec = np.asarray(prec)

    @property
    def n_traits(self):
        return len(self.loc)

    @property
    def mean2(self):
        """Mean square elements E{ mu_d^2 | self }
        used externally for learning precision_among_groups property
        for case with NON-tied precision_among_groups
        :return: mean2 = 1D array
        """
        return self.loc**2 + np.diag(self.cov)

    @property
    def cov(self):
        return np.linalg.inv(self.prec)

    def adapt(self, mean_theta, mean_prec_within, prec_among):
        """Adapt self to observed samples
        :param mean_theta: 2D array of mean observed samples of subject traits
            mean_theta[s, d] = current mean of d-th trait for s-th subject in this group
        :param mean_prec_within: mean precision matrix within this group
        :param prec_among: TraitPrecisionAmongGroups object
        :return: LL = log-likelihood after adaptation
        """
        (n_subjects, n_traits) = mean_theta.shape
        psi_among = np.eye(n_traits) * prec_among.mean  # ** works also for NON-tied prec_among
        self.prec = n_subjects * mean_prec_within + psi_among
        sum_theta = np.sum(mean_theta, axis=0)
        self.loc = np.linalg.solve(self.prec,
                                   np.dot(mean_prec_within, sum_theta))
        # = inv(self.prec) @ mean_prec_within @ sum_theta
        kl_div = self.relative_entropy(prec_among)
        # kl_div_tied = self.relative_entropy_tied(prec_among)  # ******** only for test
        # logger.info(f'group.mu.kl_div_tied= {kl_div_tied:.3f}; kl_div= {kl_div:.3f}')
        return - kl_div

    def relative_entropy(self, prior_prec):
        """Mean KLdiv( self || prior), where
        prior is zero-mean Gaussian vector with precision defined by given prior_prec,
        with either TIED or NON-TIED diagonal prec elements
        :param prior_prec: TraitPrecisionAmongGroups object defined externally
        :return: E{ ln pdf(mu | self) / pdf(mu | prior_prec) }_{self, prior_prec}

        Method:
        pdf(mu | prior) = prod_d sqrt(psi_d / 2 pi) exp(-mu_d^2 psi_d / 2), where
        psi is precision diagonal defined by prior_prec, either scalar or vector-valued
        pdf(mu | self) = ( |Psi|^{1/2} / (2 pi)^{D/2} ) exp(-(mu - m)^T Psi (mu - m) / 2
        where Psi = self.prec; m = self.loc

        KLdiv = ( ln(|Psi|) - sum_d(E{ln(psi_d)}) )/2 - D/2 + sum_d( E{ mu_d^2 } * E{psi_d}) /2
        """
        # d = self.n_traits
        (s, log_det_prec) = np.linalg.slogdet(self.prec)
        return 0.5 * (s * log_det_prec
                      + np.sum(self.mean2 * prior_prec.mean - prior_prec.mean_log - 1)
                      )

    def rvs(self, size):
        """Generate random samples
        :param size: scalar number of samples
        :return: 2D array with
            mu[n, t] = n-th sample of t-th trait
        """
        return multivariate_normal(mean=self.loc, cov=self.cov, size=size)

    def prune(self, keep):
        """Prune away un-necessary trait dimensions
        :param keep: 1D boolean array indicating traits to keep
        :return: None
        Result: self.prec and self.loc pruned
        """
        self.loc = self.loc[keep]
        self.prec = self.prec[keep, :][:, keep]

    def standardize(self, s):
        """Standardize by scaling for unity trait variance, as estimated externally
        :param s: 1D array with down-scale factors, one for each trait
        :return: None
        Method: All trait samples to be divided by s
            loc down-scaled, prec up-scaled, i.e., cov downscaled
        """
        self.loc = self.loc / s
        self.prec = self.prec * s * s[:, None]


# ---------------------------------------- module help functions

def item_logprob_by_theta(theta, tau_i, w_i, r_i):
    """sum log prob of observed data for ONE item,
    averaged across tau samples
    :param theta: theta[n, s, t] = n-th sample of t-th trait by s-th subject
    :param tau_i: tau_i[m, l] = m-th sample of UPPER interval limit for l-th response
        tau_i.shape[-1] == L_i - 1
    :param w_i: 1D array with w_i[t] = i-th item weight for t-th trait
    :param r_i: r_i[s] = response index for s-th subject to i-th item
    :return: lp = 1D array, with lp[n] = n-th sample
    """
    (tau_low, tau_high) = response_interval(tau_i, r_i)
    # tau_low[m, s] and tau_high[m, s] are (low, high) interval limits
    th = theta[:, None, :, :]  # to allow broadcast
    # th[n, 0, s, t] = n-th sample of t-th trait for s-th subject
    lp = log_prob_range(tau_low[..., None] - th, tau_high[..., None] - th)
    # lp[n, m, s, t] = n-th sample of t-th trait for s-th subject, with m-th tau sample
    lp = np.sum(lp, axis=-2)  # across subjects
    # lp[n, m, t]
    lp = np.mean(lp, axis=-2)
    # lp[n, t]
    lp = np.dot(lp, w_i)  # ***** let caller do this ???
    # lp[n]
    return lp


def d_item_logprob_by_theta(theta, tau_i, w_i, r_i):
    """d_logprob_by_theta of response data for each item
    :param theta: theta[n, s, t] = n-th sample of t-th trait by s-th subject
    :param tau_i: tau_i[m, l] = m-th sample of UPPER interval limit for l-th response
        tau_i.shape[-1] == L_i - 1
    :param w_i: 1D array with w_i[t] = i-th item weight for t-th trait
    :param r_i: list with r_i[s] = response index for s-th subject to i-th item
    :return: generator yielding dlp = 2D array, with
        dlp[n, s] = n-th sample of gradient for s-th subject theta value
    """
    (tau_low, tau_high) = response_interval(tau_i, r_i)
    # tau_low[m, s] and tau_high[m, s] are (low, high) interval limits
    th = theta[:, None, :, :]  # to allow broadcast
    # th[n, 0, s, t] = n-th sample of t-th trait for s-th subject
    dlp = d_log_prob_range_dm(tau_low[..., None] - th, tau_high[..., None] - th)
    # dlp[n, m, s, t] = n-th theta sample, m-th tau sample for s-th subject
    dlp = np.mean(dlp, axis=1)
    # dlp[n, s, t] = n-th sample of t-th trait for s-th subject
    return dlp * w_i    # ***** let caller do the weighting ???


def response_interval(tau_i, r_i):
    """Get response interval for given thresholds and responses for ONE item
    :param tau_i: 2D array with threshold samples, as
        tau_i[m, l] = m-th sample of UPPER limit of l-th response interval,
            EXCEPT extreme limits -infty, +infty
        tau_i.shape[-1] == L - 1, with L = highest response value
    :param r_i: 1D array of response indices, with missing response = -1
        r_i[s] = response index for s-th subject in range(L)
        except r_[s] = -1 in case of missing response 
    :return: tuple (tau_low, tau_high) with
        tau_low[m, s] = m-th sample of lower interval limit for r_i[s]
        tau_high[m, s] = m-th sample of upper interval limit for r_i[s]
        tau_low.shape == tau_high.shape
    """
    r_i = np.asarray(r_i)
    max_l = tau_i.shape[-1] - 1
    # r_i may be -1 for missing response, or = max_l +1 for highest interval
    tau_low = tau_i[:, np.maximum(0, r_i - 1)]
    tau_low[:, r_i <= 0] = -np.inf  # lowest interval OR missing response value
    tau_high = tau_i[:, np.minimum(max_l, r_i)]
    tau_high[:, r_i > max_l] = np.inf  # highest interval
    tau_high[:, r_i < 0] = np.inf  # missing response value
    return tau_low, tau_high


def log_prob_range(a, b):
    """log prob{ a < R <= b },
    for standard logistic random variable R, i.e.,
    = log(logistic.cdf(b) - logistic.cdf(a))
    :param a: array of lower interval limits
    :param b: array of upper interval limits, such that
        a.shape == b.shape
        -inf <= a < b <= +inf
    :return: lP = array of logprob values
        lP.shape == a.shape
    """
    # Reformulated, numerically safer than use of cdf functions:
    return (np.log1p(-np.exp(a - b))
            - np.log1p(np.exp(-b))
            - np.log1p(np.exp(a))
            )


def d_log_prob_range_dm(am, bm):
    """Gradient d log_prob_range(am, bm) / dm, where
    am = a - m, and bm = b - m
    :param am: array with lower limits
    :param bm: array with upper limits
        am.shape == bm.shape
        -inf <= am  < bm <= +inf
    :return: d_dm = array of gradient elements
        d_dm.shape == am.shape == bm.shape

    Method:
    log_prob_range = log-prob( a < Z <= b),
    for a logistic-distributed Z with location = m and scale=1,
    = logprob(a-m < Y <= b-m) for standardized Y with location = 0.
    = ln(1 - e^(am-bm)) - ln(1 + e^(-bm)) - ln(1 + e^(am))
    am - bm = a - b is independent of m.
    Thus,
    d_dm = - e^{-bm) / (1+ e^{-bm} ) + e^am / (1 + e^am)
    """
    return logistic.cdf(am) - logistic.cdf(-bm)


def d_log_prob_range_dab(am, bm):
    """Gradient d log_prob_range(am, bm) w.r.t. interval limits (a, b), where
    am = a - m, and bm = b - m
    :param am: array with lower limits
    :param bm: array with upper limits
        am.shape == bm.shape
        -infty <= am  < bm <= +infty
    :return: tuple (d_da, d_db), where
        d_da = d logprob(am, bm) w.r.t lower limit a
        d_db = d logprob(am, bm) w.r.t upper limet b
        d_da.shape == d_db.shape == am.shape == bm.shape

    Method:
    log_prob_range = log-prob( a < Z <= b),
    for a logistic-distributed Z with location = m and scale=1,
    = logprob(a-m < Y <= b-m) for standardized Y with location = 0.
    = ln(1 - e^(am-bm)) - ln(1 + e^(-bm)) - ln(1 + e^(am))

    d_da = -1 / (e^{bm - am} - 1 ) - e^am / (1 + e^am)
    d_db = +1 / (e^{bm - am} - 1 ) + e^bm / (1 + e^bm)
    """

    c = 1 / np.expm1(bm - am)
    if np.any(np.logical_not(np.isfinite(c))):
        logger.warning('Invalid tau, zero interval width')
    return - c - logistic.cdf(am), c + logistic.cdf(-bm)


# -------------------------------------------------------- TEST:
if __name__ == '__main__':
    # Testing some module functions

    from scipy.optimize import check_grad, approx_fprime

    print('\n*** Check logprob_range gradients: ')
    a = np.array([5.])
    b = a + 2.

    def test_logprob_range_m(y):
        return log_prob_range(a- y, b- y)

    def test_d_logprob_range_dm(y):
        return d_log_prob_range_dm(a- y, b- y)

    # ------------------------------------
    def test_logprob_range_a(y):
        return log_prob_range(a + y, b)

    def test_d_logprob_range_da(y):
        return d_log_prob_range_dab(a + y, b)[0]

    # ----------------------------------------
    def test_logprob_range_b(y):
        return log_prob_range(a, b + y)

    def test_d_logprob_range_db(y):
        return d_log_prob_range_dab(a, b + y)[1]

    test_y = np.array([0.])
    print(f'test_logprob_range_m(test_y) = {test_logprob_range_m(test_y)}')

    err = check_grad(test_logprob_range_m, test_d_logprob_range_dm, test_y)
    print('d_logprob_range_dm =', test_d_logprob_range_dm(test_y))
    print('approx_grad = ', approx_fprime(test_y,
                                          test_logprob_range_m,
                                          epsilon=1e-6))
    print('check_grad err = ', err)

    print(f'test_logprob_range_a(test_y) = {test_logprob_range_a(test_y)}')
    err = check_grad(test_logprob_range_a, test_d_logprob_range_da, test_y)
    print('d_logprob_range_da =', test_d_logprob_range_da(test_y))
    print('approx_grad = ', approx_fprime(test_y,
                                          test_logprob_range_a,
                                          epsilon=1e-6))
    print('check_grad err = ', err)

    print(f'test_logprob_range_b(test_y) = {test_logprob_range_b(test_y)}')
    err = check_grad(test_logprob_range_b, test_d_logprob_range_db, test_y)
    print('d_logprob_range_db =', test_d_logprob_range_db(test_y))
    print('approx_grad = ', approx_fprime(test_y,
                                          test_logprob_range_b,
                                          epsilon=1e-6))
    print('check_grad err = ', err)

    # ---------------------------------------------------------------
    print('\n*** Testing ResponseGroup ***\n')
    n_samples = 1
    n_subjects = 2
    n_traits = 3
    n_items = 3

    theta = np.array([[1., 2., 3.], [0., -1., -2.]])  # 2 subjects, 3 traits
    theta = np.tile(theta, (n_samples, 1, 1))

    s_response = np.array([[1, 2], [3, 4],[0, 4]]) + 1  # 3 items, 5 response levels
    # encoded as 1,...,5
    trait_item_map = np.eye(n_traits, dtype=bool)
    mu = GroupMeanTrait(loc=np.zeros(n_traits))

    g_ind = ResponseGroup(s_response,
                          theta=theta,
                          mu=mu,
                          name='TEST')
    # NOTE: response encoded with origin == 1 here!  **********************
    print('g_ind=', g_ind)
    print('g_ind.theta=\n', g_ind.theta)
    print('g_ind._response=\n', g_ind._response)
    print('g_ind.subject_responses=\n', g_ind.subject_responses)

    n_tau_samples = 3
    tau = [np.array([[-2., -1., +2., +4]
                     for _ in range(n_tau_samples)])
           for _ in range(3)]  # 3 items, 5 response levels
    print('tau= ', tau)
    r_i = np.arange(-1, 5, dtype=int)
    (a, b) = response_interval(tau[0], r_i)
    for (l, a_l, b_l) in zip(r_i, a[0], b[0]):
        print(f'\tresponse_interval a,b({l})= {a_l, b_l}')

    #  *** th = theta.reshape((n_samples, -1))
    print('sampler theta= ', theta)
    weight = np.eye(n_traits)  # ********** item_i <=> trait_i
    # weight = np.ones((n_items,n_traits))  # ********** item_i <=> trait_i

    lp = g_ind.logprob_by_theta(theta, tau, weight)
    print('logprob_by_theta(theta, tau, weight)= ', lp)

    mean_prec_within = np.eye(n_traits)
    mean_log_det_prec = 1.
    lp = g_ind.prior_logprob(theta, mean_prec_within, mean_log_det_prec)
    print('prior_lp(theta, tau)= ', lp)

    th = theta.reshape((n_samples, -1))
    lp = g_ind.neg_logprob(th, tau, weight, mean_prec_within, mean_log_det_prec)
    print('neg_logprob(th, tau)= ', lp)

    # -----------------------------------------------
    def test_neg_logprob(y):
        return g_ind.neg_logprob(y.reshape(1,-1), tau, weight, mean_prec_within, mean_log_det_prec)[0]

    def test_grad_neg_logprob(y):
         return g_ind.d_neg_logprob(y.reshape(1,-1), tau, weight, mean_prec_within, mean_log_det_prec)[0]
    # -------------------------------------------------
    print('test_neg_logprob(th)= ', test_neg_logprob(th))

    y = th[0]  # must be 1D vector for test
    err = check_grad(test_neg_logprob, test_grad_neg_logprob, y)
    print('grad_test =', test_grad_neg_logprob(y))
    print('approx_grad = ', approx_fprime(y,
                                          test_neg_logprob,
                                          epsilon=1e-6))
    print('check_grad err = ', err)

    print('\nTesting item_logprob_by_tau\n')

    item_ind = 0
    w_i = weight[item_ind]

    # ----------------------------------------
    def test_logprob_mean_theta(y):
        tau = y[None, :]
        return g_ind.item_logprob_by_tau(tau, item_ind, w_i)[0]

    def test_d_logprob_mean_theta(y):
        tau = y[None, :]
        return g_ind.d_item_logprob_by_tau(tau, item_ind, w_i)[0]

    test_tau = np.array(tau)[0,0,:]  # must be vector for test
    print('test_tau= ', test_tau)
    print('test_logprob_mean_theta(test_tau, item_ind)= ', test_logprob_mean_theta(test_tau))

    err = check_grad(test_logprob_mean_theta, test_d_logprob_mean_theta, test_tau)
    print('grad_test =', test_d_logprob_mean_theta(test_tau))
    print('approx_grad = ', approx_fprime(test_tau,
                                          test_logprob_mean_theta,
                                          epsilon=1e-6))
    print('check_grad err = ', err)

    test_tau = np.array(tau)[0, 0, :]  # must be vector for test
    print('test_tau= ', test_tau)
    print('test_logprob_mean_theta(test_tau, item_ind)= ', test_logprob_mean_theta(test_tau))

    err = check_grad(test_logprob_mean_theta, test_d_logprob_mean_theta, test_tau)
    print('grad_test =', test_d_logprob_mean_theta(test_tau))
    print('approx_grad = ', approx_fprime(test_tau,
                                          test_logprob_mean_theta,
                                          epsilon=1e-6))
    print('check_grad err = ', err)
