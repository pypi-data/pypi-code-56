from scipy.signal import butter, filtfilt


def butter_filter(x, lowfreq, highfreq, sf, btype='bandpass', order=4):
    """
    Apply the Butterworth lowpass or bandpass filter.

    Trick to remove/attenuate strongly the edge effects: append the signal in reverse in front of the actual signal before filtering, remove it after filtering.

    Parameters :

    - x : numpy.array - Continued time serie to filter.
    - lowcut : float - Highpass frequency in units of Hz.
    - highcut : float - Lowpass frequency in units of Hz.
    - sf : float - Sampling frequency in units of Hz.
    - btype : 'band' or 'lowpass' - For either bandpass or lowpass filtering.
    - order : int - Order of the filter. Default is 4.

    Returns :

    - y : numpy.array - Filtered data.

    """

    nyq = .5 * sf  # Nyqvist frequency

    if btype == 'bandpass':

        lowcut, highcut = lowfreq / nyq, highfreq / nyq
        b, a = butter(order, [lowcut, highcut], btype=btype)

    elif btype == 'lowpass':

        highcut = highfreq / nyq
        b, a = butter(order, [highcut], btype=btype)

    y = filtfilt(b, a, x)

    return y