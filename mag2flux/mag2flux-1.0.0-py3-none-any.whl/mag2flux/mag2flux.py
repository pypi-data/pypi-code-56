import numpy as np

def mag2flux(mag,emag,wave):
    flam = 10**(-0.4 * (mag + 2.406 + 5.*np.log10(wave)))
    eflam = flam * np.log(10.) * 0.4 * emag
    return flam,eflam
