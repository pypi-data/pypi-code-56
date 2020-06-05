import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from scipy import stats
from scipy import ndimage
from statsmodels import robust
from fBms import fBmnd
from scipy.stats import moment

from edges import *

import turbulence as tb 

plt.ion()

shape=(1024,256,256)
unit_length=1.

# field = fBmnd(3., shape)

ks = [np.fft.fftshift(np.fft.fftfreq(s, d=unit_length)) for s in shape]
kx, ky, kz = np.meshgrid(ks[1],ks[0],ks[2])
# kx = ellip * (kx * costheta - ky * sintheta)
# ky = kx * sintheta + ky * costheta
k = np.sqrt(kx**2 + ky**2 + kz**2)

rdm3D = np.random.normal(size=shape) 
phase = np.angle(np.fft.fftn(rdm3D))
power_k = np.where(k == 0, 0, np.sqrt(np.power(k, -2.)))
imfft = np.zeros(shape, dtype=complex)
imfft.real = power_k * np.cos(phase)
imfft.imag = power_k * np.sin(phase)
field3D = np.fft.ifftn(np.fft.ifftshift(imfft)).real

field2D = 1./1024*np.nansum(field3D,0)

sig3D = np.sqrt(moment(field3D.ravel(), moment=2, nan_policy='omit'))
sig2D = np.sqrt(moment(field2D.ravel(), moment=2, nan_policy='omit'))

R = sig2D**2. / sig3D**2.

print "R = ", R

stop

#mask WNM from Saury
#3D Open data                                                                                                                                                                                                                                                                                             
path_simu = '/data/amarchal/ROHSA_paper/data/Saury2014/'
hdu_list_T = fits.open(path_simu + 'T_016_subgrid_256.fits')
T_cube = hdu_list_T[0].data

idx_wnm = T_cube < 5000
fv = float(len(T_cube[idx_wnm])) / len(T_cube.ravel())

field3D_f = np.copy(field3D)
field3D_f[idx_wnm] = np.nan  
field2D_f = 1./1024*np.nansum(field3D_f,0)

sig3D_f = np.sqrt(moment(field3D_f.ravel(), moment=2, nan_policy='omit'))
sig2D_f = np.sqrt(moment(field2D_f.ravel(), moment=2, nan_policy='omit'))

R_f = sig2D_f**2. / sig3D_f**2.

print "R_f = ", R_f

stop

#######################################
stat = tb.PowerS(field2D_f)
sps1d = stat.sps1d()
ksps1d = stat.get_ks(unit_length=1)

slope, intercept, r_value, p_value, std_err = stats.linregress(np.log10(ksps1d[3:]),np.log10(sps1d[3:])) 
model = 10.**(slope * np.log10(k) + intercept)
# model = 10.**(-3. * np.log10(k))
model[shape[0]/2,shape[1]/2,shape[2]/2] = np.nan
R_theo = np.nansum(model[shape[0]/2]) / np.nansum(model)

field3Dnorm = field3D / np.mean(field3D)
field2Dnorm = field2D / np.mean(field2D)

sig3D = np.sqrt(moment(field3Dnorm.ravel(), moment=2, nan_policy='propagate'))
sig2D = np.sqrt(moment(field2Dnorm.ravel(), moment=2, nan_policy='propagate'))

R = sig2D**2. / sig3D**2.


