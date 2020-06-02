#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 20 10:31:44 2020

@author: quentinpeter
"""
from itertools import combinations

def get_constraints(Nb):
    """Get constraints such as C>0

    Parameters
    ----------
    Nb: int
        number of coefficients

    Returns
    -------
    constr_dict: dict
        dictionnary containing constraints
    """
    constr = []

    # Need C[i]>0
    for i in range(Nb):
        def cfun(C, i=i):
            return C[i]

        def cjac(C, i=i):
            ret = np.zeros_like(C)
            ret[i] = 1
            return ret

        constr.append({

            "type": "ineq",
            "fun": cfun,
            "jac": cjac

        })
    return constr

def get_zoom_indices(residual, indices, idx_min_mono, N, threshold):
    """Get the zoom indices"""
    zoom_mask = residual <= threshold

    zoom_x = (idx_min_mono - indices[..., 0])[zoom_mask]
    zoom_y = (indices[..., 1] - idx_min_mono)[zoom_mask]

    zoom_product = np.sqrt(zoom_x**2 * zoom_y**2)
    zoom_ratio = np.sqrt(zoom_x**2 / zoom_y**2)

    zoom_product = np.exp(np.linspace(
        np.log(np.min(zoom_product)),
        np.log(np.max(zoom_product)),
        101))[np.newaxis, :]
    zoom_ratio = np.tan(np.linspace(
        np.arctan(np.min(zoom_ratio)),
        np.arctan(np.max(zoom_ratio)),
        101))[:, np.newaxis]

    zoom_x = np.sqrt(zoom_product * zoom_ratio)
    zoom_y = np.sqrt(zoom_product / zoom_ratio)

    zoom_indices = np.asarray([idx_min_mono - zoom_x, zoom_y + idx_min_mono])
    zoom_indices = np.moveaxis(zoom_indices, 0, -1)

    zoom_valid = np.logical_and(zoom_indices > 0, zoom_indices < N - 1)
    zoom_valid = np.logical_and(zoom_valid[..., 0], zoom_valid[..., 1])
    zoom_indices = zoom_indices[zoom_valid]

    return zoom_indices, zoom_valid


def fit_2(profiles, Basis, phi, vary_offset=False):
    """Find the best monodisperse radius

    Parameters
    ----------
    M: 2d array
        The basis matrix. Mij = sum(basisi*basisj)
    b: 1d array
        bi = sum(profile*basisi)
    psquare: float
        psquare = sum(profiles*profile)
    phi:
        MUST BE SORTED
    Rs: 1d float
        The test radii [m]

    Returns
    -------
    radii: float
        The best radius fit
    """
    # Fit monodisperse to get mid point
    mono_fit = fit_monodisperse(profiles, Basis, phi, vary_offset)
    idx_min_mono = mono_fit.arg_x

    # Check shape Basis
    if len(Basis.shape) == 2:
        # add axis for pos
        Basis = Basis[:, np.newaxis]
        profiles = profiles[np.newaxis, :]
    # basis has phi. pos, pixel

    # Compute the matrices needed for res_interp_N
    sum_matrices = get_sum_matrices(profiles, Basis)
    Nb = np.shape(Basis)[0]

    # Get the distance from min_mono to the wall
    N = np.min([idx_min_mono, Nb - idx_min_mono])

    # Get indices for a diagonal
    indices = np.array(
        [np.arange(1, N), - np.arange(1, N)]) + idx_min_mono
    indices = np.moveaxis(indices, 0, -1)
    # Get valid indices
    valid = np.all(indices < np.shape(Basis)[0] - 1, axis=1)
    valid = np.logical_and(valid, np.all(indices > 0, axis=1))
    indices = indices[valid]
    # Compute diagonal
    res_diag = res_interp_N(indices, sum_matrices, vary_offset)

    # If best position is mopnodisperse, stop fit
    if np.nanmin(res_diag) > mono_fit.residual:
        warnings.warn("Monodisperse")
        fit = fit_monodisperse(profiles, Basis, phi, vary_offset)
        fit.dx = np.tile(fit.dx, 2)
        fit.x = np.tile(fit.x, 2)
        fit.interp_coeff = np.tile(fit.interp_coeff, 2)
        fit.x_distribution = np.array([1, 0])
        fit.x_range = [[x - dx, x + dx] for x, dx in zip(fit.x, fit.dx)]
        return fit

    # Get curve to look at (Cte XY)
    argmin_diag = np.nanargmin(res_diag) + 1
    XY = np.square(argmin_diag)
    factor = np.square(argmin_diag + 1) / XY * 2

    ratio = np.tan(
        np.linspace(0, np.pi / 2, 101)
    )[1:-1, np.newaxis]
    product = np.exp(np.linspace(np.log(XY / factor),
                                 np.log(XY * factor),
                                 101))[np.newaxis, :]
    x = np.sqrt(product * ratio)
    y = np.sqrt(product / ratio)

    indices = np.asarray([idx_min_mono - x, y + idx_min_mono])
    indices = np.moveaxis(indices, 0, -1)

    # only select valid values
    valid = np.logical_and(indices > 0, indices < Nb - 1)
    valid = np.logical_and(valid[..., 0], valid[..., 1])
    zoom_indices = indices[valid]

    # Get curve
    zoom_residual = res_interp_N(zoom_indices, sum_matrices, vary_offset)

    # Compute threshold
    minres = np.nanmin(zoom_residual[zoom_residual > 0])
    threshold = minres + 2 * np.sqrt(minres)

    # indices_range = [np.min(zoom_indices[zoom_residual < threshold], axis=0),
    #                  np.max(zoom_indices[zoom_residual < threshold], axis=0)]
    # phi_range = np.interp(indices_range, np.arange(len(phi)), phi)

    # Zoom twice
    for i in range(2):
        threshold = np.nanpercentile(zoom_residual, 0.1)
        zoom_indices, zoom_valid = get_zoom_indices(
            zoom_residual, zoom_indices, idx_min_mono, Nb, threshold)
        zoom_residual = residual_N_floating(
            zoom_indices, sum_matrices, vary_offset)[0]

    # Get best
    idx = np.unravel_index(np.argmin(zoom_residual), np.shape(zoom_residual))
    index = zoom_indices[idx]

    if np.min(index) == 0 or np.max(index) == Nb - 1:
        raise RuntimeError("Fit out of range")

    index = np.squeeze(index)
    return finalise(profiles, Basis, phi, index, sum_matrices, vary_offset)


def res_polydisperse(C, M, b, psquare):
    """Residus of the fitting

    Parameters
    ----------
    C: 1d array
        Coefficient for the basis function
    M: 2d array
        The basis matrix. Mij = sum(basisi*basisj)
    b: 1d array
        bi = sum(profile*basisi)
    psquare: float
        psquare = sum(profiles*profile)

    Returns
    -------
    Residus: float
        sum((d-p)^2)
    """
    return psquare + C@M@C - 2 * C@b


def jac_polydisperse(C, M, b, psquare):
    """Jacobian of the Residus function

    Parameters
    ----------
    C: 1d array
        Coefficient for the basis function
    M: 2d array
        The basis matrix. Mij = sum(basisi*basisj)
    b: 1d array
        bi = sum(profile*basisi)
    psquare: float
        psquare = sum(profiles*profile)

    Returns
    -------
    jacobian: 1d array
        The jacobian of res_polydisperse
    """
    return 2 * C@M - 2 * b


def hess_polydisperse(C, M, b, psquare):
    """Hessian matrix of the Residus function

    Parameters
    ----------
    C: 1d array
        Coefficient for the basis function
    M: 2d array
        The basis matrix. Mij = sum(basisi*basisj)
    b: 1d array
        bi = sum(profile*basisi)
    psquare: float
        psquare = sum(profiles*profile)

    Returns
    -------
    hess: 2d array
        The hessian matrix
    """
    return 2 * M


def fit_N(profiles, Basis, nspecies, phi):
    """Find the best N-disperse radius

    Parameters
    ----------
    M: 2d array
        The basis matrix. Mij = sum(basisi*basisj)
    b: 1d array
        bi = sum(profile*basisi)
    psquare: float
        psquare = sum(profiles*profile)
    nspecies: int
        Number of species to fit.

    Returns
    -------
    spectrum: 1d array
        The best radius fit spectrum
    """

    M, b, psquare = get_matrices(profiles, Basis)

    NRs = len(b)
    indices = np.asarray([i for i in combinations(range(NRs), nspecies)])
    res = np.empty(len(indices))
    C = np.empty((len(indices), nspecies))
    C0 = np.ones(nspecies) / nspecies
    best = psquare
    for i, idx in enumerate(indices):
        bi = b[idx]
        Mi = M[idx][:, idx]
        min_res = minimize(res_polydisperse, C0, args=(Mi, bi, psquare),
                           jac=jac_polydisperse, hess=hess_polydisperse,
                           constraints=get_constraints(nspecies))
        if min_res.fun < best:
            best = min_res.fun
#            print('New best: ', best)
        res[i] = min_res.fun
        C[i] = min_res.x

    bestidx = np.argmin(res)
    idx = indices[bestidx]
    spectrum = np.zeros(NRs)
    spectrum[idx] = C[bestidx]

    radius_error = np.zeros(nspecies)

    for rn, i in enumerate(idx):
        j = i + 1
        if j == NRs:
            j = NRs - 2
        error = (np.sqrt((phi[i] - phi[j])**2
                         / (M[i, i] + M[j, j] - M[i, j] - M[j, i])))
        radius_error[rn] = error

    fit = FitResult(x=phi[idx], dx=radius_error, x_distribution=C[bestidx],
                    basis_spectrum=spectrum, residual=np.min(res))
    fit.x_range = [[x - dx, x + dx] for x, dx in zip(fit.x, fit.dx)]

    phi_background_error = error_on_fit(
        profiles, Basis, phi, spectrum, idx)
    fit.phi_background_error = phi_background_error

    return fit


def fit_polydisperse(profiles, Basis, phi):
    """Find the best N-disperse radius

    Parameters
    ----------
    M: 2d array
        The basis matrix. Mij = sum(basisi*basisj)
    b: 1d array
        bi = sum(profile*basisi)
    psquare: float
        psquare = sum(profiles*profile)

    Returns
    -------
    spectrum: 1d array
        The best fit spectrum
    """

    M, b, psquare = get_matrices(profiles, Basis)

    Nb = len(b)
    C0 = np.zeros(Nb)
    C0[np.argmin(psquare + np.diag(M) - 2 * b)] = 1

    def fun2(C, M, b, psquare):
        return res_polydisperse(np.abs(C), M, b, psquare)

    def jac2(C, M, b, psquare):
        return jac_polydisperse(np.abs(C), M, b, psquare) * np.sign(C)

    res = basinhopping(fun2, C0, 100, disp=True,
                       minimizer_kwargs={'args': (M, b, psquare),
                                         'jac': jac2,
                                         })
    spectrum = np.abs(res.x)

    radius_error = np.zeros(Nb)

    for i in range(1, Nb):
        j = i - 1
        error = (np.sqrt((phi[i] - phi[j])**2
                         / (M[i, i] + M[j, j] - M[i, j] - M[j, i])))
        radius_error[i] = error
    radius_error[0] = radius_error[1]

    fit = FitResult(x=phi, dx=radius_error, x_distribution=spectrum,
                    basis_spectrum=spectrum, residual=res.fun)
    fit.x_range = [[x - dx, x + dx] for x, dx in zip(fit.x, fit.dx)]
    return fit