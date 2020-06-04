import numpy as np


def chi_histogram(angle_min, angle_max, n_bins, x_values, y_values):

    if angle_max < angle_min:
        raise ValueError('Invalid value for min/max angles')

    if n_bins <= 0:
        raise ValueError('Invalid number of bins value')

    if len(x_values) != len(y_values):
        raise ValueError('Input values of different lengths')

    # Compute the bin length
    delta = (angle_max - angle_min)/n_bins

    hist = np.zeros((n_bins, n_bins), dtype=np.int)

    # Loop over the x and y value and fill the histogram
    for x, y in zip(x_values, y_values):

        bin_x = int((x - angle_min)/delta)
        if bin_x < 0 or bin_x >= n_bins:
            continue

        bin_y = int((y - angle_min)/delta)
        if bin_y < 0 or bin_y >= n_bins:
            continue

        hist[bin_x, bin_y] += 1

    return hist
