import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Slider
from sympy import *
from scipy.integrate import simps


class Model:
    PRECISION_HIGH = 0.001
    PRECISION_MEDIUM = 0.01
    PRECISION_LOW = 0.1

    plot_x_start = 0.01
    x_step = 0.01
    plot_x_end = 0.99

    plot_lam_start = 0.01
    lam_step = 0.01
    plot_lam_end = 0.09

    def __init__(self, precision=None):
        if precision in [self.PRECISION_HIGH, self.PRECISION_MEDIUM, self.PRECISION_LOW]:
            self.x_step = precision
            self.lam_step = precision

    def sail_shape(self, x, eta):
        return -((2 * x - 0.5) * np.arcsin(2 * x - 1) + (2 * x + 1) * np.sqrt(x - x * x) - np.pi * 0.25 * (
                    2 * x + 1) - 0.5 * np.pi * x * eta / (eta + 1))

    def symbolic_sail_shape(self, lam=1.0, eta=0.0):
        x = Symbol('x')
        return x, -lam * ((2 * x - 0.5) * asin(2 * x - 1) + (2 * x + 1) * sqrt(x - x * x) - pi * 0.25 * (
                    2 * x + 1) - 0.5 * pi * x * eta / (eta + 1))

    def sail_end(self, lam=1., eta=0.0):
        x, shape = self.symbolic_sail_shape(lam=lam, eta=eta)
        shape_prime = lambdify(x, shape.diff(x), 'numpy')
        x_axis = np.arange(self.plot_x_start, self.plot_x_end + self.x_step, self.x_step)
        i = simps(shape_prime(x_axis), x=x_axis)
        return 1 - lam * lam * 0.5 * i


    def plot_interactive(self):
        fig, (ax1, ax2) = plt.subplots(1, 2)
        fig.tight_layout()
        plt.subplots_adjust(left=0.10, bottom=0.25)


        x_axis = np.arange(self.plot_x_start, self.plot_x_end + self.x_step, self.x_step)
        f_axis = [self.sail_shape(x, 0) for x in x_axis]
        f, = ax1.plot(x_axis, f_axis)
        ax1.set(xlabel=r'$\frac{x}{c}$', ylabel=r'$\frac{F}{\lambda c sin(2\alpha)}$')

        ax1.set_xlim([0, 1.2])
        ax1.set_ylim([0, 1.75])

        lam_axis = np.arange(self.plot_lam_start, self.plot_lam_end + self.lam_step, self.lam_step)
        c_axis = [self.sail_end(l, 0) for l in lam_axis]
        c, = ax2.plot(lam_axis, c_axis)
        ax2.set(xlabel=r'$\lambda$', ylabel=r'c*/c')
        ax2.set_xlim([0, 0.11])
        ax2.set_ylim([0.9995, 1.001])


        etavalue = plt.axes([0.25, 0.1, 0.65, 0.03], facecolor='lightgoldenrodyellow')
        seta = Slider(etavalue, r'$\eta$', 0.0, 5.0, valinit=0)

        def update(val):
            eta = seta.val

            f.set_ydata([self.sail_shape(x, eta) for x in x_axis])
            c.set_ydata([self.sail_end(l, eta) for l in lam_axis])

        seta.on_changed(update)


        plt.show()

    def plot_shape(self, eta):
        fig, ax = plt.subplots()
        fig.tight_layout()
        plt.subplots_adjust(left=0.10, bottom=0.25)

        x_axis = np.arange(self.plot_x_start, self.plot_x_end + self.x_step, self.x_step)

        ax.set(xlabel=r'$\frac{x}{c}$', ylabel=r'$\frac{F}{\lambda c sin(2\alpha)}$')
        ax.set_xlim([0, 1.2])
        ax.set_ylim([0, 1.75])

        for value in eta:
            f_axis = [self.sail_shape(x, value) for x in x_axis]
            ax.plot(x_axis, f_axis, label=r'$\eta$ = {}'.format(value))
            ax.legend()

        plt.show()

    def plot_knot_position(self, eta):
        fig, ax = plt.subplots()
        fig.tight_layout()
        plt.subplots_adjust(left=0.10, bottom=0.25)

        lam_axis = np.arange(self.plot_lam_start, self.plot_lam_end + self.lam_step, self.lam_step)

        ax.set(xlabel=r'$\lambda$', ylabel=r'c*/c')
        ax.set_xlim([0, 0.11])
        ax.set_ylim([0.9995, 1.001])

        for value in eta:
            c_axis = [self.sail_end(l, value) for l in lam_axis]
            ax.plot(lam_axis, c_axis, label=r'$\eta$ = {}'.format(value))
            ax.legend()

        plt.show()
