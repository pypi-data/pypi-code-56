import numpy as np
from astropy import wcs


def mean2vel(CRVAL, CDELT, CRPIX, mean):
    vel = [(CRVAL + CDELT * (mean[i] - CRPIX)) for i in range(len(mean))]
    return vel

def vel2mean(CRVAL, CDELT, CRPIX, vel):
    mean = [(vel[i] - CRVAL)/CDELT + CRPIX for i in range(len(vel))]
    return mean

def wcs2D(hdr):
    w = wcs.WCS(naxis=2)
    w.wcs.crpix = [hdr['CRPIX1'], hdr['CRPIX2']]
    w.wcs.cdelt = np.array([hdr['CDELT1'], hdr['CDELT2']])
    w.wcs.crval = [hdr['CRVAL1'], hdr['CRVAL2']]
    w.wcs.ctype = [hdr['CTYPE1'], hdr['CTYPE2']]
    return w

def set_wcs(patch_size, projx, projy, cdelt, GLON, GLAT):
    w           = wcs.WCS(naxis=2)
    w.wcs.crpix = [patch_size/2, patch_size/2]
    w.wcs.crval = [GLON, GLAT]
    w.wcs.cdelt = np.array([-cdelt,cdelt])
    w.wcs.ctype = [projx, projy]
    return w


def lsr2gsr(cube, hdr):
    center_y = int(cube.shape[2]/2)
    center_x = int(cube.shape[1]/2)  
    
    large = np.zeros((2*cube.shape[0],cube.shape[1],cube.shape[2]))
    large_shift = np.zeros((2*cube.shape[0],cube.shape[1],cube.shape[2]))
    
    for i in np.arange(cube.shape[0]):
        large[int(cube.shape[0]/2)+i] = cube[i]
        
    vlsr=c
        
    target_wcs=ml.wcs2D(hdr)
    target_header = target_wcs.to_header()
    
    l,b = hp.pix2ang(1024, np.arange(hp.nside2npix(1024)), lonlat=True) 
    proj_l, foo = reproject_from_healpix((l,'g'), target_header, shape_out=(cube.shape[2],cube.shape[1]), nested=False)
    proj_b, foo = reproject_from_healpix((b,'g'), target_header, shape_out=(cube.shape[2],cube.shape[1]), nested=False)
    
    vgsr_cube = np.array([np.full((cube.shape[2],cube.shape[1]),vlsr[i]) 
                          + (220. * np.sin(np.radians(proj_l)) * np.cos(np.radians(proj_b))) for i in np.arange(len(vlsr))])
    
    shift = np.zeros((cube.shape[2],cube.shape[1]))
    shift_v = np.zeros((cube.shape[2],cube.shape[1]))
    for i in np.arange(cube.shape[2]):
        for j in np.arange(cube.shape[1]):
            shift_v[i,j] = (vgsr_cube[:,center_y,center_x] - vgsr_cube[:,i,j])[0]
            shift[i,j] = (vgsr_cube[:,center_y,center_x] - vgsr_cube[:,i,j])[0] / np.abs((hdr["CDELT3"]*1.e-3))
            large_shift[:,i,j] = np.roll(large[:,i,j], - int(shift[i,j]))

    CRPIX = int(cube.shape[0]/2)
    CRVAL = vgsr_cube[0,center_y,center_x]
    CDELT = hdr["CDELT3"] *1.e-3
    
    vgsr = mean2vel(CRVAL, CDELT, CRPIX, np.arange(large.shape[0]))

    hdr0 = fits.Header()
    hdr0["CRPIX1"] = target_header["CRPIX1"]
    hdr0["CRVAL1"] = target_header["CRVAL1"]
    hdr0["CDELT1"] = target_header["CDELT1"]
    hdr0["CTYPE1"] = target_header["CTYPE1"]
    
    hdr0["CRPIX2"] = target_header["CRPIX2"]
    hdr0["CRVAL2"] = target_header["CRVAL2"]
    hdr0["CDELT2"] = target_header["CDELT2"]
    hdr0["CTYPE2"] = target_header["CTYPE2"]
    
    hdr0["CRPIX3"] = CRPIX
    hdr0["CRVAL3"] = CRVAL * 1.e3
    hdr0["CDELT3"] = CDELT * 1.e3
    hdr0["CTYPE3"] = "m/s"

    return large_shift, hdr0

    
    
    
