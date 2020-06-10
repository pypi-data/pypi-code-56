import numpy as np
import sympy as sp
from matplotlib import pyplot as plt
from typing import Tuple, Union, List
from control2020 import core


def plot_root_locus(g: sp.Expr, k: sp.Expr = sp.var("K"), h: sp.Expr = 1,
                    ki: float = 0, kf: float = 5e3, points: int = 500, k_space: str = "lin",
                    print_critical: bool = False, critical_tolerance: float = 0.1) -> plt.Line2D:
    """
    Plot a medium fidelity Root Locus of your G, K and H transfer functions
    :param g: Your plant transfer function
    :param k: Your gain (or compensator) transfer function
    :param h: Your feedback transfer function
    :param ki: Gain range start (default: 0)
    :param kf: Gain range end (default: 5000)
    :param points: Fine Grain or measured points of your Gain range (default: 500)
    :param k_space: Your kind of space generated for your Gain range
    :param print_critical: If you want to print Critical Gain (pass for imag axis)
    :param critical_tolerance: The minimal threshold distance to imag axis
    :return: A Plot Line2D object, ready to show
    """
    plt.title(f"Root locus of $G={sp.latex(g)}$", fontsize='x-large')
    plt.xlabel("$Real\\ Axis\\ [s^{-1}]$")
    plt.ylabel("$Imaginary\\ Axis\\ [s^{-1}]$")

    eq = core.extract_characteristic_equation(k, g, h)
    eq = eq.n(chop=True)

    s = sp.var("s")

    poles_points = {}
    if k_space == "lin":
        range_space = np.linspace(ki, kf, points)
    elif k_space == "log":
        range_space = np.logspace(ki, kf, points)
    else:
        raise BaseException("invalid space, use \"lin\" o \"log\"")

    for current_gain in range_space:
        p = sp.Poly(sp.expand(eq.subs(sp.var("K"), current_gain)), s)
        all_coeffs = list(p.all_coeffs())
        num_polynomial = np.poly1d(all_coeffs)
        points = list(np.roots(num_polynomial))
        for i, point in enumerate(points):
            if print_critical and abs(point.real) < critical_tolerance:
                print("Critical gain K = %.3f at %.3f + %.3fi" % (current_gain, point.real, point.imag))
            if i not in poles_points:
                poles_points[i] = []
            poles_points[i].append(point)

    plt.axvline(0, color='k')
    plt.axhline(0, color='k')
    plt.grid()

    for pole in poles_points.keys():
        plt.plot(np.real(poles_points[pole]), np.imag(poles_points[pole]))

    p = sp.Poly(sp.expand(eq.subs(sp.var("K"), 0)), s)
    num_polynomial = np.poly1d(p.all_coeffs())
    k0_poles = list(np.roots(num_polynomial))

    return plt.plot(np.real(k0_poles), np.imag(k0_poles), "kX")


def find_points_in_root_locus(g: sp.Expr, find: Union[List[float], List[complex]], k: sp.Expr = sp.var("K"),
                              h: sp.Expr = 1,
                              tolerance: float = 0.01, ki: float = 0, kf: float = 50, points: int = int(1e3),
                              print_founds: bool = False) -> List[Tuple[float, complex]]:
    """
    Find points near a some path of your root locus space
    :param g: Your plant transfer function
    :param find: Your point or list of points to search
    :param k: Your gain (or compensator) transfer function
    :param h: Your feedback transfer function
    :param tolerance: The minimal threshold distance to your searched points
    :param ki: Gain range start (default: 0)
    :param kf: Gain range end (default: 5000)
    :param points: Fine Grain or measured points of your Gain range (default: 500)
    :param print_founds: If you want to print your founded points
    :return: a list of pairs (Gain, point)
    """
    if find is None:
        find = []
    eq = core.extract_characteristic_equation(k, g, h)
    s = sp.var("s")

    founds: List[Tuple[float, complex]] = []

    for current_gain in np.linspace(ki, kf, points):
        p = sp.Poly(sp.expand(eq.subs(sp.var("K"), current_gain)), s)
        all_coeffs = list(p.all_coeffs())
        num_polynomial = np.poly1d(all_coeffs)
        points = list(np.roots(num_polynomial))
        for i, point in enumerate(points):
            for to_find in find:
                real_error = np.abs(to_find.real - point.real)
                imag_error = np.abs(to_find.imag - point.imag)
                if real_error < tolerance and imag_error < tolerance:
                    if print_founds:
                        e = float(np.mean([real_error, imag_error]))
                        print("K = %.3f at %.3f + %.3fi | e = %.3f" % (current_gain, point.real, point.imag, e))
                    founds.append((current_gain, point))
    return founds
