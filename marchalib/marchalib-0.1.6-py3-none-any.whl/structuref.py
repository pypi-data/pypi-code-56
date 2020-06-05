# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
from scipy import integrate
# from powerspectrum import PowerS
from fBms import fBmnd
from scipy import stats

plt.ion()
cm = plt.get_cmap('inferno')
cm.set_bad(color='black')
imkw = dict(origin='lower', interpolation='none', cmap=cm)

class StructF(object):
    def __init__(self, field, unit_length=1):
        super(StructF, self).__init__()
        self.field = field
        self.shape = field.shape
        self.unit_length = unit_length
        self.minval = 0.
        self.maxval = np.sqrt(self.shape[0]**2 + self.shape[1]**2)

        
    def shift_2D(self, data, dx, dy, constant=False):
        shifted_data = np.roll(data, dx, axis=1)
        if dx < 0:
            shifted_data[:, dx:] = constant
        elif dx > 0:
            shifted_data[:, 0:np.abs(dx)] = constant
            
        shifted_data = np.roll(shifted_data, dy, axis=0)
        if dy < 0:
            shifted_data[dy:, :] = constant
        elif dy > 0:
            shifted_data[0:np.abs(dy), :] = constant
        return shifted_data
    

    def shift_field(self, return_obj=False):
        if len(self.shape) == 2:
            self.dys = np.arange(0, self.shape[0], 1)
            self.dxs = np.arange(0, self.shape[1], 1)
            shifts = [[self.shift_2D(self.field, dy, dx, constant=np.nan) for dy in self.dys] for dx in self.dxs]
            
        else:
            print("Invalid shape encountered. Should be a 2D pr 3D array")

        self.shifts = shifts
        
        if return_obj:
            return shifts


    def mask_lag(self, l):
        lag_map = self.lag_map()
        return lag_map == l


    def shift_field_lag(self, l=None):
        mask = self.mask_lag(l)
        index = np.where(mask == True)
        return [self.shift_2D(self.field, index[0][i], index[1][i], constant=np.nan) for i in np.arange(len(index[0]))]            


    def diff_shift_field_lag(self, l=None):
        mask = self.mask_lag(l)
        index = np.where(mask == True)
        shifts = self.shift_field_lag(l)
        return [shift - self.field for shift in shifts]           

        
    def mean_diff_tab(self, shifts, order):
        self.dys = np.arange(0, self.shape[0], 1)
        self.dxs = np.arange(0, self.shape[1], 1)        
        mean_diff = [[np.nanmean(np.abs(shifts[i][j] - self.field)**order) for i in self.dys] for j in self.dxs]
        # mean_diff = [[np.nanmean((shifts[i][j] - self.field)**order) for i in self.dys] for j in self.dxs]
        return mean_diff
        

    def lag_map(self):
        return np.array([[np.sqrt(dy**2 + dx**2) for dy in np.arange(self.shape[0])] for dx in np.arange(self.shape[1])]).astype(int)


    def max_lag(self):
        lag_map = self.lag_map()
        return lag_map.max()
                

    def run(self, shifts=None, order=2, minval=None, maxval=None, bin_val=1, bin_type="logspace", nb_point=20):
        shifts = shifts or self.shift_field(return_obj=True)
        mean = self.mean_diff_tab(shifts=shifts, order=order)
        
        lag_map = [[np.sqrt(dy**2 + dx**2) for dy in np.arange(self.shape[0])] for dx in np.arange(self.shape[1])]

        # Get sorted radii
        flat_lag = np.array([item for sublist in lag_map for item in sublist])
        flat_mean = np.array([item for sublist in mean for item in sublist])
        
        ind = np.array(np.argsort(flat_lag))

        l_sorted = flat_lag[ind]
        mean_sorted = flat_mean[ind]

        # Get the integer part of the lag (bin size = 1)
        l_int = l_sorted.astype(int)
        deltal = l_int[1:] - l_int[:-1]  # Assumes all lag represented
        lind = np.where(deltal)[0]       # location of changed lag

        struct_f = [np.mean(mean_sorted[lind[i]+1:lind[i+1]+1]) for i in np.arange(len(lind)-1)]
        l = [np.mean(l_sorted[lind[i]+1:lind[i+1]+1]) for i in np.arange(len(lind)-1)]
        
        return struct_f, l

    def get_r_sf(self):
        lag_map = [[np.sqrt(dy**2 + dx**2) for dy in np.arange(self.shape[0])] for dx in np.arange(self.shape[1])]
        flat_lag = np.array([item for sublist in lag_map for item in sublist])        
        ind = np.array(np.argsort(flat_lag))
        l_sorted = flat_lag[ind]

        # Get the integer part of the lag (bin size = 1)
        l_int = l_sorted.astype(int)
        deltal = l_int[1:] - l_int[:-1]  # Assumes all lag represented
        lind = np.where(deltal)[0]       # location of changed lag

        l = [np.mean(l_sorted[lind[i]+1:lind[i+1]+1]) for i in np.arange(len(lind)-1)]

        return l 


    def integrand_SF_2(self, k, r, beta):
        return k**(-beta+1) * (1. - (np.sin(k*r) / (k*r)))

    def SF_2(self, r, beta):
        J = integrate.quad(self.integrand_SF_2, 0., np.inf, args=(r, beta))
        return 4. * np.pi * J[0]

    def sf2_from_gamma(self, rs, beta):
        return np.array([self.SF_2(r, np.abs(beta)) for r in rs])

    # def sf2_from_ps(self, unit_length=1):
    #     stat_ps = PowerS(self.field)
    #     sps1d, ks = stat_ps.sps1d(return_log=False)
    #     slope, intercept, r_value, p_value, std_err = stats.linregress(np.log10(ks),np.log10(sps1d))
    #     # rs = self.get_r_sf()
    #     rs = 1. / np.array(ks)
    #     SF2 = [self.SF_2(r, np.abs(slope)) for r in rs]
    #     return SF2, rs
        
if __name__ == '__main__':    
    shape = (128, 128)
    beta = 2.6
    field = fBmnd(beta, shape)
    stat = StructF(field)

    stop

    stat_ps = PowerS(field)
    sps1d, ks = stat_ps.sps1d(return_log=False)
    slope, intercept, r_value, p_value, std_err = stats.linregress(np.log10(ks),np.log10(sps1d))

    rs = 1. / np.array(ks)
    
    F2_from_SPS, rs_from_SPS = stat.sf2_from_ps()
    SF2, l = stat.run(order=2)
    SF3, l = stat.run(order=3)
    stop
    beta1, intercept1, r_value1, p_value1, std_err1 = stats.linregress(np.log10(rs),np.log10(np.abs(F2_from_SPS)))
    beta2, intercept2, r_value2, p_value2, std_err2 = stats.linregress(np.log10(l)[10:30],np.log10(np.abs(SF2)[10:30]))
    
    print("True"), beta - 2.
    print("from SPS"), beta1
    print("from map"), beta2
    # print slope #FIXME

    #Test new ESS AM
    betas = np.arange(12)+2
    betas_K41 = [n/(n-1.) for n in betas[1:]]
    betas_ESS = [n/3. for n in betas]
    SF = [stat.run(order=b) for b in betas]

    slopes = []
    slopes_ESS = []
    for i in np.arange(len(betas)-1):
        slope, intercept, r_value, p_value, std_err = stats.linregress(np.log10(SF[i][0]),np.log10(SF[i+1][0]))
        slope_ESS, intercept, r_value, p_value, std_err = stats.linregress(np.log10(SF[1][0]),np.log10(SF[i][0]))
        slopes.append(slope)
        slopes_ESS.append(slope_ESS)

    er_K41 = (np.array(betas_K41[:11]) - np.array(slopes)) / np.array(betas_K41[:11]) * 100.
    er_ESS = (np.array(betas_ESS[:11]) - np.array(slopes_ESS)) / np.array(betas_ESS[:11]) * 100.
    
