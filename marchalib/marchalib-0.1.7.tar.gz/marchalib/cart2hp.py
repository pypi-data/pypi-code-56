import numpy as np
import matplotlib.pyplot as plt
import scipy.spatial as sp
import healpy as hp
from fBms import fBmnd
from astropy.io import fits

def appendSpherical_np(xyz):
    ptsnew = np.hstack((xyz, np.zeros(xyz.shape)))
    xy = xyz[:,0]**2 + xyz[:,1]**2
    ptsnew[:,3] = np.sqrt(xy + xyz[:,2]**2)
    ptsnew[:,4] = -(np.arctan2(np.sqrt(xy), xyz[:,2])-(np.pi/2.)) # for elevation angle defined from Z-axis down
    ptsnew[:,5] = np.arctan2(xyz[:,1], xyz[:,0])
    return ptsnew

def find_nearest(array, value):               
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx]

if __name__ == '__main__':
    path = "/data/amarchal/LUDOVIC/data/"
    hdu = fits.open(path+"stilism_GAIAdr2_mapJL.fits")
    hdr = hdu[0].header
    cube=hdu[0].data

    dim_max = np.max(cube.shape)

    center = np.array([cube.shape[0]/2,cube.shape[1]/2,cube.shape[2]/2])

    x = np.arange(cube.shape[0])
    y = np.arange(cube.shape[1])
    z = np.arange(cube.shape[2])

    X,Y,Z=np.meshgrid(x,y,z)

    data=np.vstack((X.ravel(),Y.ravel(),Z.ravel())).T

    diff=10
    bins = np.arange(1,dim_max,diff)
    # tree=sp.cKDTree(data)
    # mask=[tree.query_ball_point(center, shell) for shell in bins]
    # shells=[list(set(mask[int(i)])^set(mask[int(i-1)])) for i in np.linspace(1,len(mask)-1,len(mask)-1)]
    # convert=[appendSpherical_np(data[shell]-center) for shell in shells]

    convert=appendSpherical_np(data-center)
    r = convert[:,3]
    l = np.degrees(convert[:,5]+np.pi)
    b = np.degrees(convert[:,4])
    ext = cube.ravel()
    
    nside=64
    
    reso = np.degrees(hp.nside2resol(nside))

    lhp, bhp = hp.pix2ang(nside, np.arange(hp.nside2npix(nside)), lonlat=True)

    idxr = np.where((r > 55) & (r < 65))[0]

    idx =[np.where((l[idxr]>lhp[i]-reso/2.) & (l[idxr]<lhp[i]+reso/2.) & (b[idxr]>bhp[i]-reso/2.) & (b[idxr]<bhp[i]+reso/2.)) for i in np.arange(len(lhp))]

    hpmap = np.zeros(hp.nside2npix(nside), dtype=np.float)
    hpmap = [np.nanmean(ext[idx[i]]) for i in np.arange(len(lhp))]

    #Exemple shell
    idx = np.where((r > 0) & (r < diff))[0]
    npix = len(idx)
    nsides = 2 ** np.arange(12)
    nside = find_nearest(nsides,np.sqrt(npix/12))

    hpmap = np.zeros(hp.nside2npix(nside), dtype=np.float)
    indices = hp.ang2pix(nside, l[idx], b[idx], lonlat=True)
    hpmap[indices] += ext[indices]
    
    
    

    
