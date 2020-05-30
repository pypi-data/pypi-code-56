import numpy as np
import numpy.testing as npt
import pytest
from pytest import raises as assert_raises
from scipy.integrate import IntegrationWarning

from scipy import stats
from scipy.special import betainc
from. common_tests import (check_normalization, check_moment, check_mean_expect,
                           check_var_expect, check_skew_expect,
                           check_kurt_expect, check_entropy,
                           check_private_entropy, check_entropy_vect_scale,
                           check_edge_support, check_named_args,
                           check_random_state_property,
                           check_meth_dtype, check_ppf_dtype, check_cmplx_deriv,
                           check_pickling, check_rvs_broadcast, check_freezing)
from scipy.stats._distr_params import distcont

"""
Test all continuous distributions.

Parameters were chosen for those distributions that pass the
Kolmogorov-Smirnov test.  This provides safe parameters for each
distributions so that we can perform further testing of class methods.

These tests currently check only/mostly for serious errors and exceptions,
not for numerically exact results.
"""

# Note that you need to add new distributions you want tested
# to _distr_params

DECIMAL = 5  # specify the precision of the tests  # increased from 0 to 5

# Last three of these fail all around. Need to be checked
distcont_extra = [
    ['betaprime', (100, 86)],
    ['fatiguelife', (5,)],
    ['invweibull', (0.58847112119264788,)],
    # burr: sample mean test fails still for c<1
    ['burr', (0.94839838075366045, 4.3820284068855795)],
    # genextreme: sample mean test, sf-logsf test fail
    ['genextreme', (3.3184017469423535,)],
]


distslow = ['kstwo', 'ksone', 'kappa4', 'gausshyper', 'recipinvgauss',
            'genexpon', 'vonmises', 'vonmises_line', 'cosine', 'invweibull',
            'powerlognorm', 'johnsonsu', 'kstwobign']
# distslow are sorted by speed (very slow to slow)

# skip check_fit_args (test is slow)
skip_fit_test = ['exponpow', 'exponweib', 'gausshyper', 'genexpon',
                 'halfgennorm', 'gompertz', 'johnsonsb', 'johnsonsu',
                 'kappa4', 'ksone', 'kstwo', 'kstwobign', 'mielke', 'ncf', 'nct',
                 'powerlognorm', 'powernorm', 'recipinvgauss', 'trapz',
                 'vonmises', 'vonmises_line',
                 'levy_stable', 'rv_histogram_instance']

# skip check_fit_args_fix (test is slow)
skip_fit_fix_test = ['burr', 'exponpow', 'exponweib',
                     'gausshyper', 'genexpon', 'halfgennorm',
                     'gompertz', 'johnsonsb', 'johnsonsu', 'kappa4',
                     'ksone', 'kstwo', 'kstwobign', 'levy_stable', 'mielke', 'ncf',
                     'ncx2', 'powerlognorm', 'powernorm', 'rdist',
                     'recipinvgauss', 'trapz', 'vonmises', 'vonmises_line']

# These distributions fail the complex derivative test below.
# Here 'fail' mean produce wrong results and/or raise exceptions, depending
# on the implementation details of corresponding special functions.
# cf https://github.com/scipy/scipy/pull/4979 for a discussion.
fails_cmplx = set(['beta', 'betaprime', 'chi', 'chi2', 'dgamma', 'dweibull',
                   'erlang', 'f', 'gamma', 'gausshyper', 'gengamma',
                   'geninvgauss', 'gennorm', 'genpareto',
                   'halfgennorm', 'invgamma',
                   'ksone', 'kstwo', 'kstwobign', 'levy_l', 'loggamma', 'logistic',
                   'loguniform', 'maxwell', 'nakagami',
                   'ncf', 'nct', 'ncx2', 'norminvgauss', 'pearson3', 'rdist',
                   'reciprocal', 'rice', 'skewnorm', 't', 'tukeylambda',
                   'vonmises', 'vonmises_line', 'rv_histogram_instance'])

_h = np.histogram([1, 2, 2, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 5, 6,
                   6, 6, 6, 7, 7, 7, 8, 8, 9], bins=8)
histogram_test_instance = stats.rv_histogram(_h)


def cases_test_cont_basic():
    for distname, arg in distcont[:] + [(histogram_test_instance, tuple())]:
        if distname == 'levy_stable':
            continue
        elif distname in distslow:
            yield pytest.param(distname, arg, marks=pytest.mark.slow)
        else:
            yield distname, arg


@pytest.mark.parametrize('distname,arg', cases_test_cont_basic())
def test_cont_basic(distname, arg):
    # this test skips slow distributions

    if distname == 'truncnorm':
        pytest.xfail(reason=distname)

    try:
        distfn = getattr(stats, distname)
    except TypeError:
        distfn = distname
        distname = 'rv_histogram_instance'
    np.random.seed(765456)
    sn = 500
    with npt.suppress_warnings() as sup:
        # frechet_l and frechet_r are deprecated, so all their
        # methods generate DeprecationWarnings.
        sup.filter(category=DeprecationWarning, message=".*frechet_")
        rvs = distfn.rvs(size=sn, *arg)
        sm = rvs.mean()
        sv = rvs.var()
        m, v = distfn.stats(*arg)

        check_sample_meanvar_(distfn, arg, m, v, sm, sv, sn, distname + 'sample mean test')
        check_cdf_ppf(distfn, arg, distname)
        check_sf_isf(distfn, arg, distname)
        check_pdf(distfn, arg, distname)
        check_pdf_logpdf(distfn, arg, distname)
        check_pdf_logpdf_at_endpoints(distfn, arg, distname)
        check_cdf_logcdf(distfn, arg, distname)
        check_sf_logsf(distfn, arg, distname)
        check_ppf_broadcast(distfn, arg, distname)

        alpha = 0.01
        if distname == 'rv_histogram_instance':
            check_distribution_rvs(distfn.cdf, arg, alpha, rvs)
        elif distname != 'geninvgauss':
            # skip kstest for geninvgauss since cdf is too slow; see test for
            # rv generation in TestGenInvGauss in test_distributions.py
            check_distribution_rvs(distname, arg, alpha, rvs)

        locscale_defaults = (0, 1)
        meths = [distfn.pdf, distfn.logpdf, distfn.cdf, distfn.logcdf,
                 distfn.logsf]
        # make sure arguments are within support
        spec_x = {'frechet_l': -0.5, 'weibull_max': -0.5, 'levy_l': -0.5,
                  'pareto': 1.5, 'tukeylambda': 0.3,
                  'rv_histogram_instance': 5.0}
        x = spec_x.get(distname, 0.5)
        if distname == 'invweibull':
            arg = (1,)
        elif distname == 'ksone':
            arg = (3,)
        check_named_args(distfn, x, arg, locscale_defaults, meths)
        check_random_state_property(distfn, arg)
        check_pickling(distfn, arg)
        check_freezing(distfn, arg)

        # Entropy
        if distname not in ['kstwobign', 'kstwo']:
            check_entropy(distfn, arg, distname)

        if distfn.numargs == 0:
            check_vecentropy(distfn, arg)

        if (distfn.__class__._entropy != stats.rv_continuous._entropy
                and distname != 'vonmises'):
            check_private_entropy(distfn, arg, stats.rv_continuous)

        with npt.suppress_warnings() as sup:
            sup.filter(IntegrationWarning, "The occurrence of roundoff error")
            sup.filter(IntegrationWarning, "Extremely bad integrand")
            sup.filter(RuntimeWarning, "invalid value")
            check_entropy_vect_scale(distfn, arg)

        check_retrieving_support(distfn, arg)
        check_edge_support(distfn, arg)

        check_meth_dtype(distfn, arg, meths)
        check_ppf_dtype(distfn, arg)

        if distname not in fails_cmplx:
            check_cmplx_deriv(distfn, arg)

        if distname != 'truncnorm':
            check_ppf_private(distfn, arg, distname)

        if distname not in skip_fit_test:
            check_fit_args(distfn, arg, rvs[0:200])

        if distname not in skip_fit_fix_test:
            check_fit_args_fix(distfn, arg, rvs[0:200])


def test_levy_stable_random_state_property():
    # levy_stable only implements rvs(), so it is skipped in the
    # main loop in test_cont_basic(). Here we apply just the test
    # check_random_state_property to levy_stable.
    check_random_state_property(stats.levy_stable, (0.5, 0.1))


def cases_test_moments():
    fail_normalization = set(['vonmises'])
    fail_higher = set(['vonmises', 'ncf'])

    for distname, arg in distcont[:] + [(histogram_test_instance, tuple())]:
        if distname == 'levy_stable':
            continue

        cond1 = distname not in fail_normalization
        cond2 = distname not in fail_higher

        yield distname, arg, cond1, cond2, False

        if not cond1 or not cond2:
            # Run the distributions that have issues twice, once skipping the
            # not_ok parts, once with the not_ok parts but marked as knownfail
            yield pytest.param(distname, arg, True, True, True,
                               marks=pytest.mark.xfail)


@pytest.mark.slow
@pytest.mark.parametrize('distname,arg,normalization_ok,higher_ok,is_xfailing',
                         cases_test_moments())
def test_moments(distname, arg, normalization_ok, higher_ok, is_xfailing):
    try:
        distfn = getattr(stats, distname)
    except TypeError:
        distfn = distname
        distname = 'rv_histogram_instance'

    with npt.suppress_warnings() as sup:
        sup.filter(IntegrationWarning,
                   "The integral is probably divergent, or slowly convergent.")
        sup.filter(category=DeprecationWarning, message=".*frechet_")
        if is_xfailing:
            sup.filter(IntegrationWarning)

        m, v, s, k = distfn.stats(*arg, moments='mvsk')

        if normalization_ok:
            check_normalization(distfn, arg, distname)

        if higher_ok:
            check_mean_expect(distfn, arg, m, distname)
            check_skew_expect(distfn, arg, m, v, s, distname)
            check_var_expect(distfn, arg, m, v, distname)
            check_kurt_expect(distfn, arg, m, v, k, distname)

        check_loc_scale(distfn, arg, m, v, distname)
        check_moment(distfn, arg, m, v, distname)


@pytest.mark.parametrize('dist,shape_args', distcont)
def test_rvs_broadcast(dist, shape_args):
    if dist in ['gausshyper', 'genexpon']:
        pytest.skip("too slow")

    # If shape_only is True, it means the _rvs method of the
    # distribution uses more than one random number to generate a random
    # variate.  That means the result of using rvs with broadcasting or
    # with a nontrivial size will not necessarily be the same as using the
    # numpy.vectorize'd version of rvs(), so we can only compare the shapes
    # of the results, not the values.
    # Whether or not a distribution is in the following list is an
    # implementation detail of the distribution, not a requirement.  If
    # the implementation the rvs() method of a distribution changes, this
    # test might also have to be changed.
    shape_only = dist in ['argus', 'betaprime', 'dgamma', 'dweibull',
                          'exponnorm', 'geninvgauss', 'levy_stable', 'nct',
                          'norminvgauss', 'rice', 'skewnorm', 'semicircular']

    distfunc = getattr(stats, dist)
    loc = np.zeros(2)
    scale = np.ones((3, 1))
    nargs = distfunc.numargs
    allargs = []
    bshape = [3, 2]
    # Generate shape parameter arguments...
    for k in range(nargs):
        shp = (k + 4,) + (1,)*(k + 2)
        allargs.append(shape_args[k]*np.ones(shp))
        bshape.insert(0, k + 4)
    allargs.extend([loc, scale])
    # bshape holds the expected shape when loc, scale, and the shape
    # parameters are all broadcast together.

    check_rvs_broadcast(distfunc, dist, allargs, bshape, shape_only, 'd')


def test_rvs_gh2069_regression():
    # Regression tests for gh-2069.  In scipy 0.17 and earlier,
    # these tests would fail.
    #
    # A typical example of the broken behavior:
    # >>> norm.rvs(loc=np.zeros(5), scale=np.ones(5))
    # array([-2.49613705, -2.49613705, -2.49613705, -2.49613705, -2.49613705])
    np.random.seed(123)
    vals = stats.norm.rvs(loc=np.zeros(5), scale=1)
    d = np.diff(vals)
    npt.assert_(np.all(d != 0), "All the values are equal, but they shouldn't be!")
    vals = stats.norm.rvs(loc=0, scale=np.ones(5))
    d = np.diff(vals)
    npt.assert_(np.all(d != 0), "All the values are equal, but they shouldn't be!")
    vals = stats.norm.rvs(loc=np.zeros(5), scale=np.ones(5))
    d = np.diff(vals)
    npt.assert_(np.all(d != 0), "All the values are equal, but they shouldn't be!")
    vals = stats.norm.rvs(loc=np.array([[0], [0]]), scale=np.ones(5))
    d = np.diff(vals.ravel())
    npt.assert_(np.all(d != 0), "All the values are equal, but they shouldn't be!")

    assert_raises(ValueError, stats.norm.rvs, [[0, 0], [0, 0]],
                  [[1, 1], [1, 1]], 1)
    assert_raises(ValueError, stats.gamma.rvs, [2, 3, 4, 5], 0, 1, (2, 2))
    assert_raises(ValueError, stats.gamma.rvs, [1, 1, 1, 1], [0, 0, 0, 0],
                     [[1], [2]], (4,))

def test_nomodify_gh9900_regression():
    # Regression test for gh-9990
    # Prior to gh-9990, calls to stats.truncnorm._cdf() use what ever was
    # set inside the stats.truncnorm instance during stats.truncnorm.cdf().
    # This could cause issues wth multi-threaded code.
    # Since then, the calls to cdf() are not permitted to modify the global
    # stats.truncnorm instance.
    tn = stats.truncnorm
    # Use the right-half truncated normal
    # Check that the cdf and _cdf return the same result.
    npt.assert_almost_equal(tn.cdf(1, 0, np.inf), 0.6826894921370859)
    npt.assert_almost_equal(tn._cdf(1, 0, np.inf), 0.6826894921370859)

    # Now use the left-half truncated normal
    npt.assert_almost_equal(tn.cdf(-1, -np.inf, 0), 0.31731050786291415)
    npt.assert_almost_equal(tn._cdf(-1, -np.inf, 0), 0.31731050786291415)

    # Check that the right-half truncated normal _cdf hasn't changed
    npt.assert_almost_equal(tn._cdf(1, 0, np.inf), 0.6826894921370859)  # NOT 1.6826894921370859
    npt.assert_almost_equal(tn.cdf(1, 0, np.inf), 0.6826894921370859)

    # Check that the left-half truncated normal _cdf hasn't changed
    npt.assert_almost_equal(tn._cdf(-1, -np.inf, 0), 0.31731050786291415)  # Not -0.6826894921370859
    npt.assert_almost_equal(tn.cdf(1, -np.inf, 0), 1)                     # Not 1.6826894921370859
    npt.assert_almost_equal(tn.cdf(-1, -np.inf, 0), 0.31731050786291415)  # Not -0.6826894921370859


def test_broadcast_gh9990_regression():
    # Regression test for gh-9990
    # The x-value 7 only lies within the support of 4 of the supplied
    # distributions.  Prior to 9990, one array passed to
    # stats.reciprocal._cdf would have 4 elements, but an array
    # previously stored by stats.reciprocal_argcheck() would have 6, leading
    # to a broadcast error.
    a = np.array([1, 2, 3, 4, 5, 6])
    b = np.array([8, 16, 1, 32, 1, 48])
    ans = [stats.reciprocal.cdf(7, _a, _b) for _a, _b in zip(a,b)]
    npt.assert_array_almost_equal(stats.reciprocal.cdf(7, a, b), ans)

    ans = [stats.reciprocal.cdf(1, _a, _b) for _a, _b in zip(a,b)]
    npt.assert_array_almost_equal(stats.reciprocal.cdf(1, a, b), ans)

    ans = [stats.reciprocal.cdf(_a, _a, _b) for _a, _b in zip(a,b)]
    npt.assert_array_almost_equal(stats.reciprocal.cdf(a, a, b), ans)

    ans = [stats.reciprocal.cdf(_b, _a, _b) for _a, _b in zip(a,b)]
    npt.assert_array_almost_equal(stats.reciprocal.cdf(b, a, b), ans)

def test_broadcast_gh7933_regression():
    # Check broadcast works
    stats.truncnorm.logpdf(
        np.array([3.0, 2.0, 1.0]),
        a=(1.5 - np.array([6.0, 5.0, 4.0])) / 3.0,
        b=np.inf,
        loc=np.array([6.0, 5.0, 4.0]),
        scale=3.0
    )

def test_gh2002_regression():
    # Add a check that broadcast works in situations where only some
    # x-values are compatible with some of the shape arguments.
    x = np.r_[-2:2:101j]
    a = np.r_[-np.ones(50), np.ones(51)]
    expected = [stats.truncnorm.pdf(_x, _a, np.inf) for _x, _a in zip(x, a)]
    ans = stats.truncnorm.pdf(x, a, np.inf)
    npt.assert_array_almost_equal(ans, expected)

def test_gh1320_regression():
    # Check that the first example from gh-1320 now works.
    c = 2.62
    stats.genextreme.ppf(0.5, np.array([[c], [c + 0.5]]))
    # The other examples in gh-1320 appear to have stopped working
    # some time ago.
    # ans = stats.genextreme.moment(2, np.array([c, c + 0.5]))
    # expected = np.array([25.50105963, 115.11191437])
    # stats.genextreme.moment(5, np.array([[c], [c + 0.5]]))
    # stats.genextreme.moment(5, np.array([c, c + 0.5]))

def check_sample_meanvar_(distfn, arg, m, v, sm, sv, sn, msg):
    # this did not work, skipped silently by nose
    if np.isfinite(m):
        check_sample_mean(sm, sv, sn, m)
    if np.isfinite(v):
        check_sample_var(sv, sn, v)


def check_sample_mean(sm, v, n, popmean):
    # from stats.stats.ttest_1samp(a, popmean):
    # Calculates the t-obtained for the independent samples T-test on ONE group
    # of scores a, given a population mean.
    #
    # Returns: t-value, two-tailed prob
    df = n-1
    svar = ((n-1)*v) / float(df)    # looks redundant
    t = (sm-popmean) / np.sqrt(svar*(1.0/n))
    prob = betainc(0.5*df, 0.5, df/(df + t*t))

    # return t,prob
    npt.assert_(prob > 0.01, 'mean fail, t,prob = %f, %f, m, sm=%f,%f' %
                (t, prob, popmean, sm))


def check_sample_var(sv, n, popvar):
    # two-sided chisquare test for sample variance equal to
    # hypothesized variance
    df = n-1
    chi2 = (n-1)*popvar/float(popvar)
    pval = stats.distributions.chi2.sf(chi2, df) * 2
    npt.assert_(pval > 0.01, 'var fail, t, pval = %f, %f, v, sv=%f, %f' %
                (chi2, pval, popvar, sv))


def check_cdf_ppf(distfn, arg, msg):
    values = [0.001, 0.5, 0.999]
    npt.assert_almost_equal(distfn.cdf(distfn.ppf(values, *arg), *arg),
                            values, decimal=DECIMAL, err_msg=msg +
                            ' - cdf-ppf roundtrip')


def check_sf_isf(distfn, arg, msg):
    npt.assert_almost_equal(distfn.sf(distfn.isf([0.1, 0.5, 0.9], *arg), *arg),
                            [0.1, 0.5, 0.9], decimal=DECIMAL, err_msg=msg +
                            ' - sf-isf roundtrip')
    npt.assert_almost_equal(distfn.cdf([0.1, 0.9], *arg),
                            1.0 - distfn.sf([0.1, 0.9], *arg),
                            decimal=DECIMAL, err_msg=msg +
                            ' - cdf-sf relationship')


def check_pdf(distfn, arg, msg):
    # compares pdf at median with numerical derivative of cdf
    median = distfn.ppf(0.5, *arg)
    eps = 1e-6
    pdfv = distfn.pdf(median, *arg)
    if (pdfv < 1e-4) or (pdfv > 1e4):
        # avoid checking a case where pdf is close to zero or
        # huge (singularity)
        median = median + 0.1
        pdfv = distfn.pdf(median, *arg)
    cdfdiff = (distfn.cdf(median + eps, *arg) -
               distfn.cdf(median - eps, *arg))/eps/2.0
    # replace with better diff and better test (more points),
    # actually, this works pretty well
    msg += ' - cdf-pdf relationship'
    npt.assert_almost_equal(pdfv, cdfdiff, decimal=DECIMAL, err_msg=msg)


def check_pdf_logpdf(distfn, args, msg):
    # compares pdf at several points with the log of the pdf
    points = np.array([0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8])
    vals = distfn.ppf(points, *args)
    vals = vals[np.isfinite(vals)]
    pdf = distfn.pdf(vals, *args)
    logpdf = distfn.logpdf(vals, *args)
    pdf = pdf[(pdf != 0) & np.isfinite(pdf)]
    logpdf = logpdf[np.isfinite(logpdf)]
    msg += " - logpdf-log(pdf) relationship"
    npt.assert_almost_equal(np.log(pdf), logpdf, decimal=7, err_msg=msg)


def check_pdf_logpdf_at_endpoints(distfn, args, msg):
    # compares pdf with the log of the pdf at the (finite) end points
    points = np.array([0, 1])
    vals = distfn.ppf(points, *args)
    vals = vals[np.isfinite(vals)]
    with npt.suppress_warnings() as sup:
        # Several distributions incur divide by zero or encounter invalid values when computing
        # the pdf or logpdf at the endpoints.
        suppress_messsages = [
            "divide by zero encountered in true_divide",  # multiple distributions
            "divide by zero encountered in log",  # multiple distributions
            "divide by zero encountered in power",  # gengamma
            "invalid value encountered in add",  # genextreme
            "invalid value encountered in subtract",  # gengamma
            "invalid value encountered in multiply"  # recipinvgauss
            ]
        for msg in suppress_messsages:
            sup.filter(category=RuntimeWarning, message=msg)

        pdf = distfn.pdf(vals, *args)
        logpdf = distfn.logpdf(vals, *args)
        pdf = pdf[(pdf != 0) & np.isfinite(pdf)]
        logpdf = logpdf[np.isfinite(logpdf)]
        msg += " - logpdf-log(pdf) relationship"
        npt.assert_almost_equal(np.log(pdf), logpdf, decimal=7, err_msg=msg)


def check_sf_logsf(distfn, args, msg):
    # compares sf at several points with the log of the sf
    points = np.array([0.0, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 1.0])
    vals = distfn.ppf(points, *args)
    vals = vals[np.isfinite(vals)]
    sf = distfn.sf(vals, *args)
    logsf = distfn.logsf(vals, *args)
    sf = sf[sf != 0]
    logsf = logsf[np.isfinite(logsf)]
    msg += " - logsf-log(sf) relationship"
    npt.assert_almost_equal(np.log(sf), logsf, decimal=7, err_msg=msg)


def check_cdf_logcdf(distfn, args, msg):
    # compares cdf at several points with the log of the cdf
    points = np.array([0, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 1.0])
    vals = distfn.ppf(points, *args)
    vals = vals[np.isfinite(vals)]
    cdf = distfn.cdf(vals, *args)
    logcdf = distfn.logcdf(vals, *args)
    cdf = cdf[cdf != 0]
    logcdf = logcdf[np.isfinite(logcdf)]
    msg += " - logcdf-log(cdf) relationship"
    npt.assert_almost_equal(np.log(cdf), logcdf, decimal=7, err_msg=msg)


def check_ppf_broadcast(distfn, arg, msg):
    # compares ppf for multiple argsets.
    num_repeats = 5
    args = [] * num_repeats
    if arg:
        args = [np.array([_] * num_repeats) for _ in arg]

    median = distfn.ppf(0.5, *arg)
    medians = distfn.ppf(0.5, *args)
    msg += " - ppf multiple"
    npt.assert_almost_equal(medians, [median] * num_repeats, decimal=7, err_msg=msg)


def check_distribution_rvs(dist, args, alpha, rvs):
    # dist is either a cdf function or name of a distribution in scipy.stats.
    # args are the args for scipy.stats.dist(*args)
    # alpha is a significance level, ~0.01
    # rvs is array_like of random variables
    # test from scipy.stats.tests
    # this version reuses existing random variables
    D, pval = stats.kstest(rvs, dist, args=args, N=1000)
    if (pval < alpha):
        # The rvs passed in failed the K-S test, which _could_ happen
        # but is unlikely if alpha is small enough.
        # Repeat the the test with a new sample of rvs.
        # Generate 1000 rvs, perform a K-S test that the new sample of rvs
        # are distributed according to the distribution.
        D, pval = stats.kstest(dist, dist, args=args, N=1000)
        npt.assert_(pval > alpha, "D = " + str(D) + "; pval = " + str(pval) +
                    "; alpha = " + str(alpha) + "\nargs = " + str(args))


def check_vecentropy(distfn, args):
    npt.assert_equal(distfn.vecentropy(*args), distfn._entropy(*args))


def check_loc_scale(distfn, arg, m, v, msg):
    loc, scale = 10.0, 10.0
    mt, vt = distfn.stats(loc=loc, scale=scale, *arg)
    npt.assert_allclose(m*scale + loc, mt)
    npt.assert_allclose(v*scale*scale, vt)


def check_ppf_private(distfn, arg, msg):
    # fails by design for truncnorm self.nb not defined
    ppfs = distfn._ppf(np.array([0.1, 0.5, 0.9]), *arg)
    npt.assert_(not np.any(np.isnan(ppfs)), msg + 'ppf private is nan')


def check_retrieving_support(distfn, args):
    loc, scale = 1, 2
    supp = distfn.support(*args)
    supp_loc_scale = distfn.support(*args, loc=loc, scale=scale)
    npt.assert_almost_equal(np.array(supp)*scale + loc,
                            np.array(supp_loc_scale))


def check_fit_args(distfn, arg, rvs):
    with np.errstate(all='ignore'), npt.suppress_warnings() as sup:
        sup.filter(category=DeprecationWarning, message=".*frechet_")
        sup.filter(category=RuntimeWarning,
                   message="The shape parameter of the erlang")
        sup.filter(category=RuntimeWarning,
                   message="floating point number truncated")
        vals = distfn.fit(rvs)
        vals2 = distfn.fit(rvs, optimizer='powell')
    # Only check the length of the return
    # FIXME: should check the actual results to see if we are 'close'
    #   to what was created --- but what is 'close' enough
    npt.assert_(len(vals) == 2+len(arg))
    npt.assert_(len(vals2) == 2+len(arg))


def check_fit_args_fix(distfn, arg, rvs):
    with np.errstate(all='ignore'), npt.suppress_warnings() as sup:
        sup.filter(category=DeprecationWarning, message=".*frechet_")
        sup.filter(category=RuntimeWarning,
                   message="The shape parameter of the erlang")

        vals = distfn.fit(rvs, floc=0)
        vals2 = distfn.fit(rvs, fscale=1)
        npt.assert_(len(vals) == 2+len(arg))
        npt.assert_(vals[-2] == 0)
        npt.assert_(vals2[-1] == 1)
        npt.assert_(len(vals2) == 2+len(arg))
        if len(arg) > 0:
            vals3 = distfn.fit(rvs, f0=arg[0])
            npt.assert_(len(vals3) == 2+len(arg))
            npt.assert_(vals3[0] == arg[0])
        if len(arg) > 1:
            vals4 = distfn.fit(rvs, f1=arg[1])
            npt.assert_(len(vals4) == 2+len(arg))
            npt.assert_(vals4[1] == arg[1])
        if len(arg) > 2:
            vals5 = distfn.fit(rvs, f2=arg[2])
            npt.assert_(len(vals5) == 2+len(arg))
            npt.assert_(vals5[2] == arg[2])


@pytest.mark.parametrize('method', ['pdf', 'logpdf', 'cdf', 'logcdf',
                                    'sf', 'logsf', 'ppf', 'isf'])
@pytest.mark.parametrize('distname, args', distcont)
def test_methods_with_lists(method, distname, args):
    # Test that the continuous distributions can accept Python lists
    # as arguments.
    with npt.suppress_warnings() as sup:
        sup.filter(category=DeprecationWarning, message=".*frechet_")
        dist = getattr(stats, distname)
        f = getattr(dist, method)
        if distname == 'invweibull' and method.startswith('log'):
            x = [1.5, 2]
        else:
            x = [0.1, 0.2]
        shape2 = [[a]*2 for a in args]
        loc = [0, 0.1]
        scale = [1, 1.01]
        result = f(x, *shape2, loc=loc, scale=scale)
        npt.assert_allclose(result,
                            [f(*v) for v in zip(x, *shape2, loc, scale)],
                            rtol=1e-15, atol=1e-15)
