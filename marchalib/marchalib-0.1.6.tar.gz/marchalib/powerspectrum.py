import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from scipy import ndimage
from statsmodels import robust
from fBms import fBmnd
from fBms import Pkgen
# from edges import *

plt.ion()

class PowerS(object):
        def __init__(self, field, unit_length=1):
                super(PowerS, self).__init__()
                self.field = field
                self.shape = field.shape
                self.unit_length = unit_length

        def azimuthalAverage(self, image, unit_length=1., return_std=False):
                """
                Calculate the azimuthally averaged radial profile.
                
                image - The 2D image
                center - The [x,y] pixel coordinates used as the center. The default is 
                None, which then uses the center of the image (including 
                fracitonal pixels).
                
                """
                if self.shape[0] != self.shape[0]:
                        "Warning : Two dimensions are not the same / Be careful with the 2D Spatial Power Spectrum"
                        
                # Calculate the indices from the image
                y, x = np.indices(self.shape)
                
                center = np.array([(x.max()-x.min())/2.0, (x.max()-x.min())/2.0])
                
                r = np.hypot(x - center[0], y - center[1])

                # Get sorted radii
                ind = np.argsort(r.flat)
                r_sorted = r.flat[ind]
                i_sorted = image.flat[ind]
                
                # Get the integer part of the radii (bin size = 1)
                r_int = r_sorted.astype(int)
                deltar = r_int[1:] - r_int[:-1]  # Assumes all radii represented
                rind = np.where(deltar)[0]       # location of changed radius

                vals = [i_sorted[rind[i]+1:rind[i+1]+1] for i in np.arange(len(rind)-1)]
                azi_average = [np.median(val) for val in vals]
                std = [robust.mad(val) for val in vals]
                logstd = (np.array(std)) / np.array(azi_average) / np.log(10.)

                all_k = [np.fft.fftshift(np.fft.fftfreq(s, d=unit_length)) for s in self.shape[:-1]] + \
                        [np.fft.fftshift(np.fft.fftfreq(self.shape[-1], d=unit_length))]
                
                kgrid = [np.zeros(self.shape) for _ in range(len(self.shape))]
                
                for i, kg in enumerate(kgrid):
                        sl = [slice(None) if j == i
                              else None
                              for j in range(len(self.shape))
                        ]
                        kg[:] = all_k[i][sl]
                        
                k2 = np.sqrt(np.sum([k**2 for k in kgrid], axis=0))
                k2_sorted = k2.flat[ind]
                vals_k2 = [k2_sorted[rind[i]+1:rind[i+1]+1] for i in np.arange(len(rind)-1)]
                ks = [np.mean(val) for val in vals_k2]
                
                idx = np.where(np.array(ks) < 0.5)[0]                
                
                # if return_log == True:
                #         return np.log10(sps1d), np.log10(ks) #logstd
                # else:
                # print azi_average[:idx[-1]]
                if return_std == True:
                        return np.array(azi_average[:idx[-1]]), std[:idx[-1]]
                else:
                        return np.array(azi_average[:idx[-1]])

        def azimuthalAverage_nd(self, field, unit_length=1.):
                idx = np.indices(self.shape)                
                center = np.array(self.shape)/2
                distance = (idx.transpose() - center).transpose()
                r = np.sqrt(np.sum(distance**2,0))

                # Get sorted radii
                ind = np.argsort(r.flat)
                r_sorted = r.flat[ind]
                i_sorted = field.flat[ind]
                
                # Get the integer part of the radii (bin size = 1)
                r_int = r_sorted.astype(int)
                deltar = r_int[1:] - r_int[:-1]  # Assumes all radii represented
                rind = np.where(deltar)[0]       # location of changed radius

                vals = [i_sorted[rind[i]+1:rind[i+1]+1] for i in np.arange(len(rind)-1)]
                azi_average = [np.mean(val) for val in vals]
                std = [robust.mad(val) for val in vals]
                logstd = (np.array(std)) / np.array(azi_average) / np.log(10.)

                # Compute the k grid
                ks = [np.fft.fftshift(np.fft.fftfreq(s, d=unit_length)) for s in self.shape]
                
                if len(ks) == 3 : 
                        kgrid = np.meshgrid(ks[1],ks[0],ks[2])
                else:
                        kgrid = np.meshgrid(*ks)
                        
                knorm = np.sqrt(np.sum(np.power(kgrid,2), axis=0))
                        
                knorm_sorted = knorm.flat[ind]
                vals_knorm = [knorm_sorted[rind[i]+1:rind[i+1]+1] for i in np.arange(len(rind)-1)]
                kmean = [np.mean(val) for val in vals_knorm]

                kcut = np.where(np.array(kmean) < 0.5)[0]                                
                                
                return np.array(azi_average[:kcut[-1]])
                        

        def sps2d(self):
                # Return square modulus of complex number
                fftfield = np.fft.fft2(self.field)
                shiftfftfield = np.fft.fftshift(fftfield)
        
                return np.power(np.abs(shiftfftfield), 2) 

        def spsnd(self):
                # Return square modulus of complex number
                fftfield = np.fft.fftn(self.field)
                shiftfftfield = np.fft.fftshift(fftfield)
        
                return np.power(np.abs(shiftfftfield), 2) 


        # def sps1d(self, return_log=False):
        #         psnd = self.spsnd()
        #         sps1d = self.azimuthalAverage_nd(psnd)
        #         ks = self.get_ks()
                
        #         return sps1d

        def sps1d(self, return_log=False):
                ps2d = self.sps2d()
                sps1d, std = self.azimuthalAverage(ps2d, return_std=True)
                ks = self.get_ks()
                
                return sps1d, std
        

        # def get_ks(self, unit_length=1):                
        #         # Compute the k grid
        #         ks = [np.fft.fftshift(np.fft.fftfreq(s, d=unit_length)) for s in self.shape]
                
        #         if len(ks) == 3 : 
        #                 kgrid = np.meshgrid(ks[1],ks[0],ks[2])
        #         else:
        #                 kgrid = np.meshgrid(*ks)
                        
        #         knorm = np.sqrt(np.sum(np.power(kgrid,2), axis=0))

        #         k = self.azimuthalAverage_nd(knorm)
        #         return np.array(k)

        def get_ks(self, unit_length=1):                
                all_k = [np.fft.fftshift(np.fft.fftfreq(s, d=unit_length)) for s in self.shape[:-1]] + \
                        [np.fft.fftshift(np.fft.fftfreq(self.shape[-1], d=unit_length))]
                
                kgrid = [np.zeros(self.shape) for _ in range(len(self.shape))]
                
                for i, kg in enumerate(kgrid):
                        sl = [slice(None) if j == i
                              else None
                              for j in range(len(self.shape))
                        ]
                        kg[:] = all_k[i][sl]
                        
                k2 = np.sqrt(np.sum([k**2 for k in kgrid], axis=0))
                ks = self.azimuthalAverage(k2)
                return np.array(ks)

                
        
if __name__ == '__main__':
        shape = (256,256)
        field = fBmnd(shape, Pkgen(3,0.01,0.45), seed=31, unit_length=1)

        stat = PowerS(field)
        sps1d, std = stat.sps1d()
        ks = stat.get_ks(unit_length=1)
        
        slope, intercept, r_value, p_value, std_err = stats.linregress(np.log10(ks[3:]),np.log10(sps1d[3:]))
        
        print("Beta = " + str(slope))

        stop
                
        fig = plt.figure(0)
        ax = fig.add_subplot(111)
        ax.set_yscale('log')
        ax.set_xscale('log')
        ax.plot(ks, sps1d, '.k', markersize=2)

        # ax.plot(np.log10(np.arange(len(logsps1d))+1), logsps1d, '.k', markersize=2, label='TOT')
        # ax.fill_between(np.log10(np.arange(len(logsps1d))+1), logsps1d-logstd, logsps1d+logstd,
        #                                  alpha=0.2, edgecolor='k', facecolor='k', linewidth=0)

        # fig = plt.figure()
        # ax = fig.add_subplot(111)
        # ax.errorbar(np.log10(np.arange(len(sps1d))+1), np.log10(sps1d), yerr=err, fmt=".k")
        # ax.set_yscale('log', nonposy="clip")
        # ax.set_xscale('log', nonposx="clip")
        # ax.errorbar(np.arange(len(sps1d)), sps1d, yerr=np.array(stdp)/2., fmt=".")
