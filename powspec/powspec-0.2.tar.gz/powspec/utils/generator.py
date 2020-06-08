import numpy as np

__all__ = ["Pk", "gen_pkfield"]


def Pk(k, alpha=-11.0 / 3, fknee=1):
    """Simple power law formula"""
    return (k / fknee) ** alpha


def gen_pkfield(npix=32, alpha=-11.0 / 3, fknee=1, res=1):
    """Generate a 2D square map with P(k) field"""

    ufreq = np.fft.fftfreq(npix, d=res)
    kfreq = np.sqrt(ufreq[:, np.newaxis] ** 2 + ufreq ** 2)

    with np.errstate(divide="ignore"):
        psd = 2 * Pk(kfreq, alpha=alpha, fknee=fknee)
    psd[0, 0] = 0

    pha = np.random.uniform(low=-np.pi, high=np.pi, size=(npix, npix))

    fft_img = np.sqrt(psd) * (np.cos(pha) + 1j * np.sin(pha))
    return np.real(np.fft.ifft2(fft_img)) * npix / res ** 2
