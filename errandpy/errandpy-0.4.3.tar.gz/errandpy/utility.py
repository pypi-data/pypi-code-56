import matplotlib.pyplot as plt
import numpy

import errandpy
"""
    logファイルのFitting Parameter: a,b,c,dを返します
    normalized_paramの時正規化したパラメーターを返します
    
"""


def real_a(a, delta, min):
    return (a + 1) * delta + min


def real_b(b, delta):
    return b * delta


def get_z0FromLogFile(path, isLegacy=False):
    with open(path, 'r') as f:
        lines = f.readlines()
        length = len(lines)
        if isLegacy:
            s = lines[length - 4].split(" ")
            # print(path, lines[length - 4], int(s[13]))
        else:
            s = lines[length - 3].split(" ")

        return int(s[13])


def legacy_get_logFileParamater(path, normalized_param=True, normMode=1) -> []:
    with open(path, 'r') as f:
        lines = f.readlines()
        length = len(lines)
        s = lines[length - 2].split(" ")
        print(s)
        if len(s) == 10:
            result = [float(s[3]), float(s[5]), float(s[7]), float(s[9])]
        else:
            result = [0,0,0,0]
            print(" Warning: Log File Error!!! " + path)
        if normalized_param is False:
            min =  float(lines[0].split(" ")[1][normMode:-2])
            delta = float(lines[1].split(" ")[1][normMode:-2])

            result[0] = real_a(result[0], delta, min)
            result[1] = real_b(result[1], delta)

    return result


def get_logFileParamater(path, normalized_param=True, normMode=1) -> []:
    with open(path, 'r') as f:
        lines = f.readlines()
        length = len(lines)
        s = lines[length - 1].split(" ")
        # print(s)
        if len(s) == 12 or len(s) == 14:
            result = [float(s[3]), float(s[5]), float(s[7]), float(s[9])]
        else:
            result = [0,0,0,0]
            print(" Warning: Log File Error!!! " + path)
        if normalized_param is False:
            min =  float(lines[0].split(" ")[1][normMode:-2])
            delta = float(lines[1].split(" ")[1][normMode:-2])
            result[0] = real_a(result[0], delta, min)
            result[1] = real_b(result[1], delta)
    print(result)
    return result


def _f_long(x, a, b, c, d):
    if errandpy.useLegacyModel:
        y = a - b / (1 + c * x) ** d
    else:
        y = a - b / (c + x) ** d
    return y


def clamp(minValue, maxValue, value):
    return max(min(value, maxValue), minValue)


def clamp01(value):
    return clamp(0, 1, value)


def mean_r(x, y, a, b, c, d):
    ss_res = numpy.dot((y - _f_long(x, a, b, c, d)), (y - _f_long(x, a, b, c, d)))
    ymean = numpy.mean(y)
    ss_tot = numpy.dot((y - ymean), (y - ymean))

    return 1 - ss_res / ss_tot


def normalized(array, max=1, bias=0):
    minValue = array.min(keepdims=True)
    maxValue = array.max(keepdims=True)
    result = (array - minValue) / (maxValue - minValue) * max + bias
    return result, minValue, maxValue - minValue


def draw_plt(x, y, a, b, c, d, bound, name, ze=None):
    y_b = y[bound:]
    plt.clf()
    plt.scatter(x, y, color='red', label='Original data', alpha=0.5)

    _x = x[bound:]

    plt.title(name + " (Mean R: " + str(mean_r(_x, y_b, a, b, c, d)) + ")")
    plt.axhline(0, color='green', linestyle='dashdot')
    plt.axvline(x[bound], color='green', linestyle='dashdot')
    if ze is not None:
        plt.axvline(x[ze], color='blue', linestyle='dashdot')
    plt.plot(x, _f_long(x, a, b, c, d), color='blue', label='Fitted line')
    plt.plot(x, y - _f_long(x, a, b, c, d), color='black', label='force curve')