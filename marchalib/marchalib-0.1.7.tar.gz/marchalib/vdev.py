import numpy as np
import healpy as hp
import matplotlib.pyplot as plt
from galpy.potential import MWPotential2014
from galpy.potential import vcirc

def f_R(l, b, R0, d):
    return R0 * np.sqrt(np.cos(b)**2 * (d/R0)**2 - 
                        (2.*np.cos(b)*np.cos(l)*(d/R0)) + 1.)                                                                                                                

def f_vlsr(r, R0, v0, l, b):
    return (R0 * vcirc(MWPotential2014,r/R0,ro=R0,vo=v0) / 
            r - vcirc(MWPotential2014,1,ro=R0,vo=v0)) * np.sin(l) * np.cos(b)

def vlimlsr(l,b,R0,v0,z1,z2,rmax,dmin,dmax):
    #l in [0, 2pi] / b in [-pi/2, pi/2]                                                                                        
    #unit : kpc and km/s
    d = np.arange(dmin,dmax,0.1)
    z = d * np.sin(b)
    
    R = f_R(l, b, R0, d) 
    vlsr = f_vlsr(R, R0, v0, l, b)

    zmax = np.where(R <= R0, z1, z1 + (z2 - z1) * ( (R/R0 - 1.)**2 / 4. ))

    vlsr[np.abs(z) > zmax] = np.nan
    vlsr[R > rmax] = np.nan
    vlsr[R == 0] = np.nan

    return np.nanmin(vlsr), np.nanmax(vlsr)


