import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
import sys

from .utilities.math_functions import expfunc, expfuncinv


def membrane_test(sig, cmd, sf, fit_region=(0.8, 0.1), whole_cell=True):
    """
    The membrane test protocol must be such that the command pulse occupies the first part of the trace.

    The calculation are performed as follows:
    1) The input resistance Rinput is derived from the input voltage step and output command step: Rinput=Vstep/Istep
    2) The membrane time constant tau is derived from an exponential fit to the capacitive transient
    3) The charge of the membrane Q is calculated by integrating the capacitive transient
    4) The access resistance is derived as Ra = tau * Vstep / Q
    5) The membrane resistance is derived as Rm = Rinput - Ra
    6) The membrane capacitance is derived as Cm tau * Rinput / (Ra * Rm)
    7) The holding current is the current at baseline level

    Parameters :

        - sig : numpy array - Output signal in units of pA.
        - cmd : numpy array - Input signal in units of mV.
        - sf : float - Sampling frequency of the signal in units of Hz.
        - fit_region : tuple of float -  Default is (0.8, 0.1).
        - whole_cell : boolean - If False, only Rinput and the holding level are calculated (in bath and seal
        configuration). Default is True.
        - positive_peak : boolean - If True, the calculation is performed based on the upward capacitive transient.
        If False, on the downward capacitive transient. Default is True.

    Returns :

        - Rinput : float - Input resistance in units of MOhm.
        - Ra : float - Access resistance in units of MOhm.
        - Rm : float - Membrane resistance in units of MOhm.
        - Cm : float - Membrane capacitance in units of pF.
        - tau : float - Membrane time constant in units of µs.
        - holding : float - Holding current in units of pA.

    Example :

    Rinput, Ra, Rm, Cm, tau, holding = membrane_test(sig, cmd, sf, fit_region = (0.8, 0.1),
                                                     whole_cell = True, positive_peak = True)

    See also : scipy.optimize.curve_fit

    """

    results = pd.Series(data=[np.nan] * 6, index=['Rinput', 'Ra', 'Rm', 'Cm', 'tau', 'holding'])

    t = np.arange(0.0, sig.size / sf, 1 / sf)  # s

    threshold = 100  # mV/ms
    diff = np.diff(cmd) * sf * pow(10, -3)  # mV/ms
    a, b = np.where(diff > threshold)[0][0], np.where(diff < -threshold)[0][0]

    nmargin = int(0.001 * sf)  # 1 ms
    a += nmargin
    b -= nmargin

    nsamples_baseline = int(0.005 * sf)  # 5 ms

    v1 = np.mean(cmd[- nsamples_baseline:])
    v2 = np.mean(cmd[b - nsamples_baseline:b])

    i1 = np.mean(sig[- nsamples_baseline:])
    i2 = np.mean(sig[b - nsamples_baseline:b])

    holding = i1

    Istep = i2 - i1  # pA
    Vstep = v2 - v1  # mV

    Rinput = Vstep / Istep * pow(10, 3)  # MOhm

    if whole_cell:

        imax = np.argmax(sig[:b])
        peak = sig[imax] - i2  # pA
        start = imax + np.where(sig[imax:] - i2 < fit_region[0] * peak)[0][0]
        stop = imax + np.where(sig[imax:] - i2 < fit_region[1] * peak)[0][0]

        try:

            (param1, param2, param3), cov = curve_fit(expfunc, t[start:stop] - t[start], sig[start:stop] - i2)
            tau = pow(10, 6) / param2  # ms
            Q = np.sum(sig[imax:imax + b] - expfuncinv(t[:b], i2 - i1, param2, i1)) / sf  # pC
            Ra = tau * Vstep / Q * pow(10, -3)  # MOhm

            Rm = Rinput - Ra  # MOhm

            Cm = tau * Rinput / (Ra * Rm)  # pF

            results[['Rinput', 'Ra', 'Rm', 'Cm', 'tau', 'holding']] = np.around(Rinput), np.around(Ra), np.around(
                Rm), np.around(Cm), np.around(
                tau), np.around(holding)

        except:

            sys.stdout.write('\nFailed curve fitting\n')

    else:

        results[['Rinput', 'holding']] = np.around(Rinput, 1), np.around(holding)

    return results