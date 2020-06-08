import numpy
import os

import matplotlib.pyplot as plt
import errandpy.handy as handy
import errandpy.utility as Utility


def get_test_curve():
    x, y = [], []
    with open(os.path.dirname(__file__) + "/forcecurve.csv") as f:
        next(f)
        lines = f.readlines()
        for line in lines:
            x.append(float(line.split(",")[0]))
            y.append(float(line.split(",")[1]))
    return numpy.asarray(x), numpy.asarray(y)


def plot_test_curve():
    x, y = get_test_curve()
    plt.plot(x, y)
    plt.xlabel("z (angstorm)")
    plt.ylabel("Frequency shift (Hz)")
    plt.show()


def test_firststage(name="errandpy"):
    x, y = get_test_curve()
    return handy.tell_me_z0(x, y, name=name)


def test_secondstage(z0, name="errandpy"):
    x, y = get_test_curve()
    return handy.extract_short_range(x, y, z0, name=name)


def test_fitting():
    # Calculate z0 and extract short range
    z0, param = test_firststage()
    result_dict = test_secondstage(z0)
    # dict return the long-range parameter a, b, c, d, and normalize parameter min and delta, and z0, ze

    # then let's plot the result
    x, y = get_test_curve()
    min, delta = result_dict["min"], result_dict["delta"]
    Utility.draw_plt(x, y, Utility.real_a(result_dict["a"], delta, min), Utility.real_b(result_dict["b"], delta),
                     result_dict["c"], result_dict["d"], z0, "errandpy test result")
    plt.show()


if __name__ == '__main__':
    plot_test_curve()
    test_fitting()

