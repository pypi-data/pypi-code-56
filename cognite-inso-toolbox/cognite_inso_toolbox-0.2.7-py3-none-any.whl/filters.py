# ------------------
# Dependencies
# ------------------

from typing import Dict

import numpy as np
import pandas as pd
import pymc3 as pm
from cvxpy import ECOS, Minimize, Problem, Variable, pnorm, tv
from pykalman import KalmanFilter
from pymc3.distributions.timeseries import GaussianRandomWalk
from scipy import optimize, signal, sparse
from theano import shared


# ------------------
# Bases
# ------------------
class BaseSmoother:
    def __init__(self, window_size: int = 9):
        self.window_size = window_size


class BaseClassic:
    def __init__(self, filt: np.ndarray):
        self.filter_ = filt

    def __call__(self, data: pd.DataFrame):
        return pd.DataFrame(signal.sosfilt(self.filter_, data.values), columns=data.columns, index=data.index)


class BaseKalmanSmoother:
    def __init__(self):
        pass


# ------------------
# Callables
# ------------------


class GPSmooth:
    """
    Use:
        smoother = GPSmooth(0.9) # specify smoothing factor of 0;9
        results = smoother(ts) # pass univariate time series
        plt.plot(results) # plot the smoothed results
    """

    def __init__(self, smoothing_factor: float):
        self.smooth = smoothing_factor

    def __call__(self, data: np.ndarray):
        model = pm.Model()
        with model:
            smoothing_param = shared(0.9)
            mu = pm.Normal("mu", sigma=1e5)
            tau = pm.Exponential("tau", 1.0 / 1e5)
            z = GaussianRandomWalk("z", mu=mu, tau=tau / (1.0 - smoothing_param), shape=data.shape)
            obs = pm.Normal("obs", mu=z, tau=tau / smoothing_param, observed=data.values)  # noqa: F841
        with model:
            smoothing_param.set_value(self.smooth)
            res = pm.find_MAP(vars=[z], fmin=optimize.fmin_l_bfgs_b)
            return pd.DataFrame(res["z"], columns=data.columns, index=data.index)


class SGSmoother(BaseSmoother):
    def __init__(self, order: int, piecewise: bool = False, **kwargs):
        super().__init__(**kwargs)
        self.order = order
        self.piecewise = piecewise

    def __call__(self, data: pd.DataFrame):
        if not self.piecewise:
            return signal.savgol_filter(data.values.reshape(len(data)), self.window_size, self.order)
        else:
            df_reshape = data.values.reshape(len(data))
            return self.savitzky_golay_piecewise(df_reshape, order=self.order)

    def savitzky_golay_piecewise(self, data, kernel=11, order=4):
        xvals = np.arange(0, len(data))
        turnpoint = 0
        last = len(xvals)
        if xvals[1] > xvals[0]:  # x is increasing?
            for i in range(1, last):  # yes
                if xvals[i] < xvals[i - 1]:  # search where x starts to fall
                    turnpoint = i
                    break
        else:  # no, x is decreasing
            for i in range(1, last):  # search where it starts to rise
                if xvals[i] > xvals[i - 1]:
                    turnpoint = i
                    break
        if turnpoint == 0:  # no change in direction of x
            return signal.savgol_filter(data, kernel, order)
        else:
            # smooth the first piece
            firstpart = signal.savgol_filter(data[0:turnpoint], kernel, order)
            # recursively smooth the rest
            rest = self.savitzky_golay_piecewise(xvals[turnpoint:], data[turnpoint:], kernel, order)
            return np.concatenate((firstpart, rest))


class MovingAverage(BaseSmoother):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __call__(self, data: pd.DataFrame):
        kernel = np.ones(self.window_size) / self.window_size  # note name change! This is not a mask!
        return pd.DataFrame({col: np.convolve(data[col], kernel, "same") for col in data.columns}, index=data.index)


class SimpleKalmanSmoother(BaseKalmanSmoother):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __call__(self, data: pd.DataFrame):
        kf = KalmanFilter(
            transition_matrices=[1],
            observation_matrices=[1],
            initial_state_mean=56,
            initial_state_covariance=1,
            observation_covariance=1,
            transition_covariance=0.01,
        )
        state_means, _ = kf.filter(data.values)
        return pd.DataFrame(state_means.flatten(), index=data.index, columns=data.columns)


class ESSmoother(BaseSmoother):
    def __init__(
        self,
        mean: bool = True,
        trend: bool = True,
        seasonal: bool = True,
        approx_season_cosntant: bool = None,
        seas_const: int = 100,
    ):
        super().__init__()
        self.base_model = ESModels(mean_bool=mean, trend_bool=trend, seasonal_bool=seasonal)
        if seasonal:
            self.base_model.add_seasonality(seas_const)

    def __call__(self, data: pd.DataFrame):
        model = RobustES(data, ESMod=self.base_model, window_dict={"R": 131 * 2, "L": 131 * 2})
        model.fit(lambda_noise=0.05, lambda_anchor=5)
        model.x_DF.index = data.index
        res = model.x_DF.Yfilter
        return pd.DataFrame(res, columns=data.columns, index=data.index)


class Butter(BaseClassic):
    """
    N:int
    The order of the filter.

    Wn: array_like
    The critical frequency or frequencies. For lowpass and highpass filters,
    Wn is a scalar; for bandpass and bandstop
    filters, Wn is a length-2 sequence.

    For a Butterworth filter, this is the point at which the gain drops to
    1/sqrt(2) that of the passband
    (the “-3 dB point”).

    For digital filters, Wn are in the same units as fs. By default, fs is
    2 half-cycles/sample, so these are normalized
    from 0 to 1, where 1 is the Nyquist frequency. (Wn is thus in
    half-cycles / sample.)

    For analog filters, Wn is an angular frequency (e.g. rad/s).

    btype{‘lowpass’, ‘highpass’, ‘bandpass’, ‘bandstop’}, optional
    The type of filter. Default is ‘lowpass’.

    analogbool, optional
    When True, return an analog filter, otherwise a digital filter is returned.

    output{‘ba’, ‘zpk’, ‘sos’}, optional
    Type of output: numerator/denominator (‘ba’), pole-zero (‘zpk’), or
    second-order sections (‘sos’). Default is ‘ba’
    for backwards compatibility, but ‘sos’ should be used for
    general-purpose filtering.

    fsfloat, optional # this is probably really good to include
    The sampling frequency of the digital system.
    """

    def __init__(self, **kwargs):
        super().__init__(signal.butter(**kwargs, output="sos"))


class Cheby(BaseClassic):
    """
    N:int
    The order of the filter.

    rp: float
    The maximum ripple allowed below unity gain in the passband. Specified in
    decibels, as a positive number.

    Wn: array_like
    A scalar or length-2 sequence giving the critical frequencies. For Type I
    filters, this is the point in the
    transition band at which the gain first drops below -rp.

    For digital filters, Wn are in the same units as fs. By default, fs is 2
    half-cycles/sample, so these are normalized
    from 0 to 1, where 1 is the Nyquist frequency. (Wn is thus in
    half-cycles / sample.)

    For analog filters, Wn is an angular frequency (e.g. rad/s).

    btype{‘lowpass’, ‘highpass’, ‘bandpass’, ‘bandstop’}, optional
    The type of filter. Default is ‘lowpass’.

    analogbool, optional
    When True, return an analog filter, otherwise a digital filter is returned.

    output{‘ba’, ‘zpk’, ‘sos’}, optional
    Type of output: numerator/denominator (‘ba’), pole-zero (‘zpk’), or
    second-order sections (‘sos’). Default is ‘ba’
    for backwards compatibility, but ‘sos’ should be used for
    general-purpose filtering.

    fsfloat, optional # this is probably really good to include
    The sampling frequency of the digital system.
    """

    def __init__(self, **kwargs):
        super().__init__(signal.cheby1(**kwargs, output="sos"))


class ESModels(object):
    def __init__(self, mean_bool: bool = True, trend_bool: bool = True, seasonal_bool: bool = True):

        """
        :param mean_bool: Boolean, Additive ES with Level
        :param trend_bool: Boolean, Additive ES with Trend
        :param seasonal_bool: Bolean, Additive ES with Seasonality
        """
        # Configure Component of the Additive ES model
        self.mean = mean_bool
        self.trend = trend_bool
        if self.mean and not self.trend:
            raise ValueError("ES with Trend but without Mean is impossible")

        self.seasonal_bool = seasonal_bool
        self.number_seasonality = 0
        # if self.seasonal_bool:
        self.seas: Dict
        self.seas = {}

        # Store number of components
        self.components_list: Dict
        self.components_list = {}
        self.number_components = 0
        self.number_components += 1 if mean_bool else self.number_components
        self.number_components += 1 if trend_bool else self.number_components

        self.number_components_tot = int(self.number_components)

        return

    def add_seasonality(self, period):

        """
        :param period: Integer, Periodicity of the seasonality
        :return: None
        """
        name = "S" + str(self.number_seasonality + 1)

        if self.seasonal_bool:
            if name not in self.seas.keys():
                self.seas[name] = period
                self.number_seasonality = len(self.seas.keys())
                self.number_components += 1
                self.number_components_tot += period

            else:
                print("Seasonality name already exists : ", name)

        else:
            raise ValueError(
                "You have to activate seasonality to \
                              add a new seasonality"
            )

        return

    def _create_gmat(self):

        """
        :return: Vector, g (See paper)
        """
        start_ind = 0
        gmat_list = []

        if self.mean:
            mean_row = np.zeros(self.number_components).tolist()
            mean_row[start_ind] = 1
            start_ind += 1
            gmat_list.append(sparse.lil_matrix([mean_row]))

        if self.trend:
            trend_row = np.zeros(self.number_components).tolist()
            trend_row[start_ind] = 1
            start_ind += 1
            gmat_list.append(sparse.lil_matrix([trend_row]))

        if self.seasonal_bool:
            for season in self.seas.keys():
                seasonality_row = np.zeros(self.number_components).tolist()
                seasonality_row[start_ind] = 1
                seasonality_row_zeros = sparse.lil_matrix(np.zeros((self.seas[season] - 1, self.number_components)))
                gmat_list.append(sparse.lil_matrix([seasonality_row]))
                gmat_list.append(sparse.lil_matrix(seasonality_row_zeros))
                start_ind += 1

        return sparse.vstack(gmat_list)

    def _create_A_matrix(self):
        """
        :return: Matrix, A (see Paper)
        """

        def vecmi(m, i):
            vecmi = np.zeros(m).tolist()
            vecmi[i - 1] = 1
            return vecmi

        # Get A mean / trend
        Al = None
        if self.mean and self.trend:
            Al = sparse.lil_matrix([[1, 1], [0, 1]])
        elif self.mean and not self.trend:
            Al = sparse.lil_matrix([[1]])

        # Block of seasonal patterns
        list_Am = []
        for season in sorted(self.seas.keys()):
            mi = self.seas[season]
            Ami = [vecmi(mi, mi)] + [vecmi(mi, i) for i in range(1, mi)]
            Ami = sparse.lil_matrix(Ami)
            list_Am.append(Ami)

        if len(self.seas) > 0:
            Aseasonal = sparse.block_diag(tuple(list_Am))

            # Combine Amean/trend with Aseasonal
            A = Aseasonal if Al is None else sparse.block_diag((Al, Aseasonal))

            return A
        else:
            return Al

    def _create_w_vector(self):
        """
        :return: vector, w (see Paper)
        """
        w_vector = sparse.lil_matrix(np.zeros(self.number_components_tot))

        if self.mean:
            w_vector[0, 0] = 1
        if self.trend:
            w_vector[0, 1] = 1

        current_m = 0
        for season in self.seas.keys():
            m = self.seas[season]
            current_m += m
            w_vector[0, current_m + 1] = 1

        return w_vector

    def get_components(self):

        """
        :return: Dictionary, components of the model associated with their
        nicknames (L for mean, B for trend etc...)
        """
        if self.mean:
            self.components_list["mean"] = "L"
        if self.trend:
            self.components_list["trend"] = "B"
        for season in self.seas:
            self.components_list[season] = season
        return self.components_list

    def _create_model(self):

        """
        :return: None
        """
        self.g_names = []

        if self.seasonal_bool:
            if len(self.seas.keys()) == 0:
                print(
                    "Error, there should be at least one seasonal \
                       pattern if seasonal bool is activated!"
                )

        # Map names of g components into g_names
        if self.mean:
            self.g_names.append(("L", "alpha"))
            if self.trend:
                self.g_names.append(("B", "beta"))

        if len(self.seas) > 0:
            for ind, key in enumerate(sorted(self.seas.keys())):
                self.g_names.append(("S" + str(int(ind + 1)), "gamma_" + str(int(ind + 1))))

        self.gmat = self._create_gmat()
        self.A_matrix = self._create_A_matrix()
        self.w_vector = self._create_w_vector()


def window_func(L, R, x):

    """
    :param L: Float, Left window size
    :param R: Float, Right window size
    :param x: Float, Get window weight at x
    :return: Float, values of weighted window at x
    """

    if L < 0 or R < 0:
        raise ValueError("Window dimension should be positive")

    if x >= 0:
        y = (-1.0 / R) * x + 1
        return y if y >= 0 else 0

    elif x < 0:
        y = (1.0 / L) * x + 1
        return y if y >= 0 else 0


class RobustES(object):
    def _load_regularizer_init(self):

        """
        :return: None
        """

        # Store regularizer
        self.regularizer_dict = {}
        regul_ind = 0
        if self.ESMod.mean:
            self.regularizer_dict["mean"] = (regul_ind, regul_ind)
            regul_ind += 1
            if self.ESMod.trend:
                self.regularizer_dict["trend"] = (regul_ind, regul_ind)
                regul_ind += 1

        for season in sorted(self.ESMod.seas.keys()):
            season_value = self.ESMod.seas[season]
            self.regularizer_dict[season] = (regul_ind, regul_ind + season_value)
            regul_ind += season_value

        self.x_take_index = [tuple_dict[0] for tuple_dict in sorted(list(self.regularizer_dict.values()))]  # noqa: E128

        return

    def _load_ESmatrix_init(self):

        """
        :return: None
        """

        # Store main matrices to execute the algorithm
        self.D_matrix = self._set_D_matrix()
        self.A_matrix = self.ESMod.A_matrix
        shapeA = self.A_matrix.shape
        if shapeA[0] != shapeA[1]:
            raise ValueError("A should be a square matrix!")

        self.w_vector = self.ESMod.w_vector
        self.H = self.ESMod.gmat

        # Store complete set of matrices needed to compute algorithm
        self.dim_A = shapeA[0]
        self.A_dict = {0: sparse.identity(self.dim_A)}
        self.a_dict = {0: self.w_vector}

        for i in range(len(self.Y)):
            self.A_dict[i + 1] = self.A_dict[i] * self.A_matrix
            self.a_dict[i + 1] = self.w_vector * self.A_dict[i + 1]

        self.A_BIG = sparse.vstack(list(self.a_dict.values())[:-1])
        self.A_BIG = self.A_BIG.tocsc()

        return

    def _load_ESModel_init(self, ESMod):

        """
        :param ESMod: Object, Additive ES Model
        :return: None
        """

        # Store ESModel
        self.ESMod = ESMod
        self.ESMod._create_model()
        # Store model parameters
        self.components_list = self.ESMod.get_components()
        self.nb_components = len(self.components_list.keys())

        return

    def _load_Yts_init(self, Y):

        """
        :param Y: Numpy array, Time series under study
        :return: None
        """

        L, R = self.window_dict["L"], self.window_dict["R"]

        self.Y_old = Y
        self.N_old = len(self.Y_old)

        # Add invisible window
        self.Y = np.append(np.NaN * np.zeros(L), Y)
        self.Y = np.append(self.Y, np.NaN * np.zeros(R))
        self.N = len(self.Y)

        return

    def _load_window_init(self, window_dict):

        """
        :param window_dict: Dictionary, Window characteristics
        :return: None
        """

        # Store Window of ES cell
        self.window_dict = window_dict
        self.eta_matrix = [
            window_func(self.window_dict["L"], self.window_dict["R"], i)
            for i in range(-self.window_dict["L"], self.window_dict["R"] + 1)
        ]

        return

    def __init__(self, Y, ESMod, window_dict):

        """
        :param Y: Numpy Array, original time series to be fitted and forecasted
        :param ESMod: ESModels Object, containing the Additive ES model
                      that will fit the time series
        :param window_dict: Dictionnary, containing the single
                            ES Cell properties.
        """

        # Load window
        self._load_window_init(window_dict)

        # Load time series
        self.N = len(Y)
        self._load_Yts_init(Y)

        # Load ES Model
        self._load_ESModel_init(ESMod)
        # Load ES matrices
        self._load_ESmatrix_init()
        self._load_regularizer_init()

        # Load forecasting tools
        # self._load_forecasting_init()

        return

    def _set_D_matrix(self):

        """
        :return: D matrix for algorithm, taking into account possible missing
                 values
        """

        D_matrix = np.ones(self.N)
        index_missing = pd.isnull(pd.Series(self.Y))
        index_missing = index_missing[index_missing].index

        # Change NaN value into 0 to prevent optimizer from failing.
        # 0*np.NaN = np.NaN
        self.Y = pd.Series(self.Y).fillna(0).values

        for missing in index_missing:
            D_matrix[missing] = 0

        return D_matrix

    def _load_seasonalities_m(self):

        """
        :return: Integer, List : Total seasonality components, List of
                 individual seasonality components
        """

        m = 0
        m_list = []

        for season in sorted(self.ESMod.seas.keys()):

            season_value = self.ESMod.seas[season]
            m_list.append(season_value)
            m += season_value

        return m, m_list

    def _update_opt_func(self, t):

        """
        :param t: Float, Time to apply the single ES cell model
        :return: None
        """

        L, R = self.window_dict["L"], self.window_dict["R"]

        Y_VEC = np.matrix(self.Y[0 + t : L + R + t + 1]).T  # noqa: E203
        D_ETA_VEC = self.D_matrix[0 + t : L + R + t + 1] * self.eta_matrix  # noqa: E203

        D_ETA_VEC = self.D_matrix[0 + t : L + R + t + 1] * self.eta_matrix  # noqa: E203
        D_ETA_VEC = sparse.diags(D_ETA_VEC)
        A_VEC = self.A_BIG[0 : L + R + 1, :]  # noqa: E203

        self.opt_func += pnorm(D_ETA_VEC * (Y_VEC - A_VEC * self.xt_list[t]), 1)

    def _update_opt_regularizer(self, t, lambda_noise):

        """
        :param t: Float, Time to apply the single ES cell model
        :param lambda_noise: Float, regularization factor (Denoising ES cell)
        :return: None
        """

        # Regularization R1
        for season in sorted(self.ESMod.seas.keys()):
            season_reg_ind = self.regularizer_dict[season]
            self.regularizer_func += lambda_noise * tv(
                self.xt_list[t][season_reg_ind[0] : season_reg_ind[1]]  # noqa: E203
            )  # noqa: E203

    def _update_opt_anchor(self, t, lambda_anchor):

        """
        :param t: Time to link two consecutive ES cells
        :param lambda_anchor: Float, regularization factor (Linking
                              the ES cells)
        :return: None
        """

        # Create anchor
        L, _ = self.window_dict["L"], self.window_dict["R"]
        self.anchor_func += float(lambda_anchor) * pnorm(
            self.A_dict[L + 1] * self.xt_list[t] - self.A_dict[L] * self.xt_list[t + 1], 1
        )

        return

    def _load_x_g(self):

        """
        :return: None
        """

        # DF to store output of model : x, s and gt
        self.x_names, self.g_names = zip(*self.ESMod.g_names)
        self.x_DF = pd.DataFrame(columns=list(self.x_names))
        self.g_DF = pd.DataFrame(columns=list(self.g_names))
        self.geps_DF = pd.DataFrame(columns=list(self.g_names))

        return

    def _build_optimization(self, lambda_anchor, lambda_noise):

        """
        :param lambda_anchor: Float, regularization factor
                              (Linking the ES cells)
        :param lambda_noise: Float, regularization factor (Denoising)
        :return: cvxpy object, Convex objective function to optimize
        """

        m, _ = self._load_seasonalities_m()
        self.xt_list = [Variable((m + 2, 1)) for _ in range(self.N_old)]

        # Building Single ES Cells
        self.opt_func = 0
        for i in range(self.N_old):
            self._update_opt_func(t=i)

        # Building Dynamic ES Cells model
        self.anchor_func = 0
        for i in range(self.N_old - 1):
            self._update_opt_anchor(t=i, lambda_anchor=lambda_anchor)

        # Building Regularizers
        self.regularizer_func = 0
        for i in range(self.N_old):
            self._update_opt_regularizer(t=i, lambda_noise=lambda_noise)

        print("Building Objective")
        objective = self.opt_func + self.anchor_func + self.regularizer_func

        return objective

    def _solve_optimization(self, lambda_noise, lambda_anchor, status_opt=False):

        """
        :param lambda_noise: Float, regularization factor (Denoising)
        :param lambda_anchor: Float, regularization factor
                              (Linking the ES cells)
        :param status_opt: Boolean, Enable to print optimization details
        :return: None
        """
        objective = self._build_optimization(lambda_noise=lambda_noise, lambda_anchor=lambda_anchor)

        # Optimization problem
        print("Optimizing")
        objective = Minimize(objective)
        prob = Problem(objective)
        prob.solve(solver=ECOS)

        if status_opt:
            print("Point in time: Initialization")
            print("status:", prob.status)
            print("optimal value:", prob.value)

        return

    def _collecting_results(self):

        """
        :return: None
        """
        L, _ = self.window_dict["L"], self.window_dict["R"]
        print("Collecting Results")
        # Saving x_DF
        # Add component of x
        for ind, x in enumerate(self.xt_list):
            # Need to multiply by A^L to get the estimate t
            # hat we are interested in
            estimate_x = self.A_dict[L] * x.value
            values_key = np.array(estimate_x.T)[0]
            self.x_DF.loc[ind] = np.take(values_key, self.x_take_index)

        # Add residual
        self.x_DF["Yfilter"] = self.x_DF.sum(axis=1)
        self.x_DF["Y"] = self.Y_old

        # Saving geps_DF
        # Add component of g
        self.geps_DF.loc[0] = np.zeros(self.nb_components)
        self.g_DF.loc[0] = np.zeros(self.nb_components)

        for ind, x in enumerate(self.xt_list):

            if ind > 0:
                geps = (
                    self.A_dict[L] * self.xt_list[ind].value - self.A_dict[L + 1] * self.xt_list[ind - 1].value
                )  # noqa
                self.geps_DF.loc[ind] = np.array(geps.T)[0][: self.nb_components]  # noqa: E501

        return

    def fit(self, lambda_anchor, lambda_noise, status_opt=False):

        """
        :param lambda_noise: Float, regularization factor (Denoising)
        :param lambda_anchor: Float, regularization factor
                            (Linking the ES cells)
        :param status_opt: Boolean, Detail about optimization
        :return: None
        """

        self._load_x_g()
        self._solve_optimization(lambda_anchor=lambda_anchor, lambda_noise=lambda_noise, status_opt=status_opt)
        self._collecting_results()

        return
