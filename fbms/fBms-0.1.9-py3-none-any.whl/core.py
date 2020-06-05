# -*- coding: utf-8 -*-
import numpy as np
import six

def fBmnd(shape, power_spectrum, unit_length=1, seed=None, statistic=np.random.normal, fft=np.fft, fft_args=dict()):
    """
    Generates a field given a stastitic and a power_spectrum.
    author: A. Marchal based on FieldGenerator (C. Cadiou) and MAMDLIB 

    Parameters
    ----------
    statistic: callable
        A function that takes returns a random array of a given signature,
        with signature (s) -> (B) with s == B.shape

    shape: tuple
        The shape of the output field

    unit_length: float
        How much physical length represent 1pixel. For example a value of 10
        mean that each pixel stands for 10 physical units. It has the
        dimension of a physical_unit/pixel.

    fft: a numpy-like fft API

    fft_args: array
        a dictionary of kwargs to pass to the FFT calls

    Returns:
    --------
    field: a real array of shape `shape` following the statistic
        with the given power_spectrum
    """

    if seed is not None: np.random.seed(seed)

    if not six.callable(statistic):
        raise Exception('`statistic` should be callable')

    # Draw a random sample
    normal = statistic(size=shape)

    # Compute the FFT of the field and take the phase
    phase = np.angle(fft.fftn(normal, **fft_args))

    try:
        fftfreq = fft.fftfreq
    except:
        # Fallback on numpy for the frequencies
        fftfreq = np.fft.fftfreq

    # Compute the k grid
    ks = [np.fft.fftshift(np.fft.fftfreq(s, d=unit_length)) for s in shape]

    if len(ks) == 3 : 
        kgrid = np.meshgrid(ks[1],ks[0],ks[2])
    else:
        kgrid = np.meshgrid(*ks)

    knorm = np.sqrt(np.sum(np.power(kgrid,2), axis=0))
    power_k = np.where(knorm == 0, 0, np.sqrt(power_spectrum(knorm)))

    imfft = np.zeros(shape, dtype=complex)
    imfft.real = power_k * np.cos(phase)
    imfft.imag = power_k * np.sin(phase)
    
    return fft.ifftn(np.fft.ifftshift(imfft)).real


def Pkgen(n, k0, k1):
    def Pk(k):
        return np.exp(-np.power(k0/k,2)) * np.power(k, -n) * np.exp(-np.power(k/k1,2))
    return Pk

def Pkgen_break(n1, n2, kcrit, k0, k1):
    def Pk(k):
        return np.where(k < kcrit, np.exp(-np.power(k0/k,2)) * np.power(k/kcrit, -n1) * np.exp(-np.power(k/k1,2)), np.exp(-np.power(k0/k,2)) * np.power(k/kcrit, -n2) * np.exp(-np.power(k/k1,2)))
    return Pk
        

if __name__ == '__main__':    
    shape = (512,512)

    field = fBmnd(shape, Pkgen(3,0.01,0.4), seed=31, unit_length=1)
    field_inj = fBmnd(shape, Pkgen_break(4, 3.6, 0.08, 0.0,np.inf), seed=31, unit_length=1)



