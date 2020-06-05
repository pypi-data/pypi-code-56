import numpy as np
import healpy as hp
from galpy.potential import MWPotential2014 
from galpy.potential import vcirc

m_h = 1.6737236e-27 #kg                              

# def kinetic_T(sigma_obs, mach):
#     sigma_therm = sigma_obs / np.sqrt(1. + mach**2.)
#     return m_h * (sigma_therm*1.e3)**2 / const.k_B.value # K

def kinetic_T(sigma_obs, mach):
    return 121. * sigma_obs**2. / ((mach**2./4.2) + 1)

def PDF2mach(sigma,zeta,D):
    b = 1. + ((1./D) - 1.)*zeta
    return np.sqrt((np.exp(sigma**2.) - 1.) / b**2.)

# def v_r(r):
#     #Define constant in kpc and solar mass                                                                                                                                                                                                                                            
#     G  = 4.302e-6
#     a1 = 0.
#     b1 = 0.495
#     M1 = 2.05e10
#     a2 = 7.258
#     b2 = 0.520
#     M2 = 25.47e10

#     return r * np.sqrt((G*M1 / (r**2.+(a1+b1)**2.)**(3./2.))
#                        + (G*M2 / (r**2.+(a2+b2)**2.)**(3./2.)))

def fct_r(l, b, r0, d):
    return r0 * np.sqrt(np.cos(b)**2 * (d/r0)**2 - (2.*np.cos(b)*np.cos(l)*(d/r0)) + 1.)

# def fct_vlsr(r, r0, l, b):
#     return ( r0 * v_r(r) / r - v_r(r0) ) * np.sin(l) * np.cos(b)

def fct_vlsr(r, r0, v0, l, b):
    return (r0 * vcirc(MWPotential2014,r/r0,ro=r0,vo=v0) / r - vcirc(MWPotential2014,1,ro=r0,vo=v0)) * np.sin(l) * np.cos(b)

def vlimlsr_old(l, b):
    '''l in [0, 2pi] / b in [-pi/2, pi/2]'''
    # Define constant / unit kpc and km/s                                                                                                                                                                                                                                             
    r0 = 8.5
    v0 = 220.
    # Disk geometry                                                                                                                                                                                                                                                                   
    z1 = 1.
    z2 = 3.
    rmax = 26.

    d     = 0.
    z     = d * np.sin(b)
    zmax  = 1.
    r     = 0.
    save  = []
    count = 0
    test  = False

    while r < rmax :
        if np.abs(z) > zmax :
            test = True
        if test == True : break
        r = fct_r(l, b, r0, d)
        if r != 0. :
            vlsr = fct_vlsr(r, r0, v0, l, b)
            if count != 0 :
                save.append(vlsr)
            if r <= r0 :
                zmax = z1
            if r > r0 :
                zmax = z1 + (z2 - z1) * ( (r/r0 - 1.)**2 / 4. )
        d += 0.1
        z = d * np.sin(b)
        count += 1
    return np.min(save), np.max(save)

def vlimlsr(l,b):
    '''l in [0, 2pi] / b in [-pi/2, pi/2]
       unit : kpc and km/s'''
    # Cst for galpy
    r0 = 8.5
    v0 = 220.

    # Disk geometry                                                                                                                                                                                                     
    z1 = 1.
    z2 = 3.
    rmax = 26.

    dmax_disk = 2.*rmax
    
    d = np.arange(0.,dmax_disk,0.1)
    z = d * np.sin(b)
    r = fct_r(l, b, r0, d)
    zmax = np.where(r <= r0, z1, z1 + (z2 - z1) * ( (r/r0 - 1.)**2 / 4. ))
    
    vlsr = fct_vlsr(r, r0, v0, l, b)
    vlsr[np.abs(z) > zmax] = np.nan
    vlsr[r > rmax] = np.nan
    vlsr[r == 0] = np.nan

    return np.nanmin(vlsr,0), np.nanmax(vlsr,0)
    
if __name__ == '__main__':    
    # print(kinetic_T(8.,0.))
    # print(PDF2mach(0.40,0.2,3))    
    new = vlimlsr(180,0)
    old = vlimlsr_old(180,0)    
    print(new)
    print(old)

    # nside=64
    # l,b = hp.pix2ang(nside, np.arange(hp.nside2npix(nside)), lonlat=True)                                                                                                                                                                             

    # l = np.radians(l) 
    # b = np.radians(b)       

    # foo = np.zeros((2,len(l))) 
    # for i in np.arange(len(l)): 
    #     vmin, vmax = vlimlsr_old(l[i],b[i])      
    #     foo[0,i] = vmin 
    #     foo[1,i] = vmax 

    

    
