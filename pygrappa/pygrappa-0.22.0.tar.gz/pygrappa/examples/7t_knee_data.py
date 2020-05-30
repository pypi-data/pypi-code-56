'''Run GRAPPA on 7T knee data.'''

from time import time

import numpy as np
import matplotlib.pyplot as plt

from pygrappa import igrappa as grappa
from utils.find_acs import find_acs

def ifft2(x, ax=(0, 1)):
    return np.fft.fftshift(np.fft.ifft2(np.fft.ifftshift(x, axes=ax), axes=ax), axes=ax)

def sos(x, ax=-1):
    return np.sqrt(np.sum(np.abs(x)**2, axis=ax))

if __name__ == '__main__':

    # Load data
    print('Start loading data...')
    t0 = time()
    sl = np.load('/home/nicholas/Documents/pygrappa/data/slice.npy').astype('complex')
    print('Loading data took %g seconds' % (time() - t0))

    # Remove some coils
    sl = sl[..., ::2]

    t0 = time()
    calib = find_acs(sl)
    print('Took %g seconds to find calib' % (time() - t0))

    t0 = time()
    res = grappa(sl, calib, niter=10, silent=False)
    print('Took %g seconds to recon' % (time() - t0))

    plt.imshow(np.log(sos(res)))
    plt.show()

    plt.imshow(sos(ifft2(res)), cmap='gray')
    plt.show()
