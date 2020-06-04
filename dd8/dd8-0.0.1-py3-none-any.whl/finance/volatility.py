# -*- coding: utf-8 -*-
"""
Created on Sat Dec 29 18:00:46 2018

@author: LIM YUAN QING
"""

import multiprocessing as mp
import numpy as np
import pandas as pd
import scipy
from scipy import optimize
import datetime
import dateutil
import matplotlib.pyplot as plt

from dd8 import get_basic_logger, LOG_PRINT_LEVEL, LOG_WRITE_LEVEL

logger = get_basic_logger(__name__, LOG_PRINT_LEVEL, LOG_WRITE_LEVEL)

class VolatilityModel():
    def __init__(self):
        pass
    
    def __del__(self):
        pass
    
    def __str__(self):
        pass
    
    def __len__(self):
        pass
    
    def compute_vol(self):
        pass
    
    def compute_residuals(self):
        pass
    
    def calibrate(self):
        pass
    
    def get_vol(self):
        pass

class VolatilitySurface(object):
    def __init__(self, npa_strikes, npa_maturities, npa_data, 
                 dte_reference=None, enum_volatility_stickiness=None):
        self.strikes = npa_strikes
        self.maturities = npa_maturities
        self.surface = npa_data
        if dte_reference:
            self.reference_date = dte_reference
        else:
            self.reference_date = glob.TODAY
        
        if enum_volatility_stickiness:
            self.sticky = enum_volatility_stickiness
        else:
            self.sticky = enums.ENUM_VOLATILITY_STICKINESS.STRIKE
        
        self.max_strike = self.strikes.max()
        self.min_strike = self.strikes.min()
        self.max_maturity = self.maturities.max()
        self.min_maturity = self.maturities.min()
        
    def __call__(self, dte_maturity, dbl_strike):
        pass
    
    def get_volatility(self, dbl_strike, dte_maturity):
        if (dte_maturity<= self.min_maturity):
            return scipy.interpolate.CubicSpline(self.strikes, npa_data[:, 0])(dbl_strike)
        elif (dte_maturity>=self.max_maturity):
            return scipy.interpolate.CubicSpline(self.strikes, npa_data[:, -1])(dbl_strike)
        else:
            if dte_maturity in self.maturities:
                return scipy.interpolate.CubicSpline(self.strikes, 
                          npa_data[:, np.nonzero(self.maturities==dte_maturity)])(dbl_strike)
            else:
                mat_one = self.maturities[sef.maturities<dte_maturity][-1]
                mat_two = self.maturities[sef.maturities>dte_maturity][0]
                sigma_one = scipy.interpolate.CubicSpline(self.strikes, 
                                npa_data[:, np.nonzero(self.maturities==mat_one)])(dbl_strike)
                sigma_two = scipy.interpolate.CubicSpline(self.strikes, 
                                npa_data[:, np.nonzero(self.maturities==mat_two)])(dbl_strike)
                
                return math.sqrt((((sigma_one**2)*(mat_one-self.reference_date).days)+
                                  (((dte_maturity-mat_one)/(mat_two-mat_one))*
                                   (((sigma_two**2)*(mat_two-self.reference_date).days) - 
                                    ((sigma_one**2)*(mat_one-self.reference_date).days))))/
                                     (dte_maturity-self.reference_date))
    
    def from_csv(self):
        pass
    
class SABR(VolatilityModel):
    """
    Calibrate volatility surface under the SABR stochastic volatility model.
    
    The parameters of the SABR model are:
        α : initial variance
        v : volatility of variance
        β : exponent for the forward rate
        ρ : correlation between 2 Brownian motions (spot and volatility)
        
    Steps to estimate the SABR model:
        1. estimate β (currently assumed to be 1.0)
        2. calibrate model in one of two ways:
            a. estimate α, v, ρ directly, or
            b. estimate v and ρ by implying α from ATM volatility
            
    Here, model is calibrated for each option expiry and by estimating α, v, ρ 
    directly (2a).
    
    Parameters are estimated by minimising sum of squared errors between the 
    model and market volatilities.
    
    Parameters
    ----------
    dbl_spot : double
        current spot price of underlying
    lst_bloomberg_ticker : list
        option tickers given by [<underlying> <mm/dd/yy> <side> <strike> 
        <asset_class>]
    lst_forward_price : list
        forward prices of corresponding option tickers
    lst_implied_vol_mid : list
        implied volatilities (mid) of corresponding option tickers
    lst_implied_vol_bid : list
        implied volatilities (bid) of corresponding option tickers
    lst_implied_vol_ask : list
        implied volatilities (ask) of corresponding option tickers
    dbl_beta : double
        user-defined exponent for the forward rate
    
    References
    ----------
    [1] https://www.next-finance.net/IMG/pdf/pdf_SABR.pdf
    [2] https://quant.stackexchange.com/questions/21462/sabr-implied-volatility-and-option-prices
    [3] https://www.mathworks.com/help/fininst/calibrating-the-sabr-model.html  
    
    """
    def __init__(self, dbl_spot, 
                 lst_bloomberg_ticker,
                 lst_forward_price,
                 lst_implied_vol_mid,
                 lst_implied_vol_bid = None,
                 lst_implied_vol_ask = None,                 
                 dbl_beta = 1.0):
        
        self.__dbl_spot = dbl_spot
        self.__dbl_beta = dbl_beta
        
        lst_strikes = list(map(extract_strike, lst_bloomberg_ticker))
        lst_time_to_maturity = list(map(extract_time_to_maturity, 
                                        lst_bloomberg_ticker))        
        self.__npa_maturity_bucket_index = np.unique(lst_time_to_maturity, 
                                                     return_index=True)[1]
        
        self.__npa_bloomberg_ticker_buckets = np.split(lst_bloomberg_ticker, 
                                                self.__npa_maturity_bucket_index)
        self.__npa_time_to_maturity_buckets = np.split(lst_time_to_maturity, 
                                                self.__npa_maturity_bucket_index)
        self.__npa_strike_buckets = np.split(lst_strikes, 
                                        self.__npa_maturity_bucket_index)
        self.__npa_forward_price_buckets = np.split(lst_forward_price, 
                                            self.__npa_maturity_bucket_index)        
        self.__npa_implied_vol_mid_buckets = np.split(lst_implied_vol_mid, 
                                                  self.__npa_maturity_bucket_index)
        if lst_implied_vol_bid == None or lst_implied_vol_ask == None:
            npa_weights = np.ones(len(lst_implied_vol_mid))
        else:
            npa_weights = 1/np.abs(np.asarray(lst_implied_vol_ask) -
                                np.asarray(lst_implied_vol_bid))
            
        self.__npa_weights_buckets = np.split(npa_weights, 
                                              self.__npa_maturity_bucket_index)
        
        self.__lst_unique_strikes = list(set(lst_strikes))
        self.__dbl_atm_strike = self.compute_atm_strike()
                
    def __del__(self):
        pass
    
    def __str__(self):
        pass
    
    def compute_z(self, K, f, alpha, beta, volofvol):
        return (volofvol/alpha) * ((f*K)**((1-beta)/2)) * np.log(f/K)
    
    def compute_X(self, z, rho):
        return np.log(((1 - 2*rho*z + z*z)**0.5 + z - rho) / (1-rho))
        
    def compute_vol(self, K, f, T, alpha, beta, rho, volofvol):
        
        z = self.compute_z(K, f, alpha, beta, volofvol)
        X = self.compute_X(z, rho)
        
        sigma = (((alpha * (1 + T*(((((1 - beta)**2)/24) * ((alpha**2)/
                    ((f*K)**(1 - beta)))) + ((0.25 * rho * beta * volofvol * alpha) /
                    ((f * K)**((1 - beta)/2))) + ((2 - 3 * rho * rho * volofvol * 
                    volofvol)/24)))) / (((f * K)**((1 - beta)/2)) * 
                    (1 + ((((1 - beta)**2)/24) * (np.log(f/K)**2)) + 
                    ((((1 - beta)**4) / 1920) * (np.log(f / K)**4))))) * (z/X))
        
        return sigma

    def compute_residuals(self, parameters ,data, K, f, T, beta, weights):
        # parameters[0] - alpha
        # parameters[1] - rho
        # parameters[2] - volofvol
        #return np.asarray(data) - self.compute_vol(K, f, T, parameters[0], self.get_beta(), parameters[1], parameters[2])        
        return ((np.asarray(data) - 
                self.compute_vol(K, f, T, parameters[0], beta, parameters[1], 
                                 parameters[2]))*weights)

    def calibrate(self):
        # Loop through each set of time to maturity
#        for i in range(len(tk_samples)):
#            sol = scipy.optimize.least_squares(self.compute_errors,[0.1,1.25,-0.1],
#        args=(tk_samples[i],),max_nfev=2000)
#        print(sol.x)
        self.__lst_solution = []
        for i in range(1, len(self.__npa_time_to_maturity_buckets)):
            self.__lst_solution.append(
                    scipy.optimize.least_squares(self.compute_residuals, [0.5, 0.0, 0.5],
                                                 args=(self.__npa_implied_vol_mid_buckets[i],
                                                       self.__npa_strike_buckets[i],
                                                       self.__npa_forward_price_buckets[i],
                                                       self.__npa_time_to_maturity_buckets[i],
                                                       self.get_beta(),
                                                       self.__npa_weights_buckets[i]),
                                                 bounds=([0.0, -1.0, 0.0], [np.inf, 1.0, np.inf])
                                                 ).x
                                        )        
        return self.__lst_solution
    
    def gen_surface(self):
        lst_surface = []
        for i in range(1, len(self.__npa_time_to_maturity_buckets)):
            vol_surf = self.compute_vol(self.__npa_strike_buckets[i],
                                        self.__npa_forward_price_buckets[i],
                                        self.__npa_time_to_maturity_buckets[i],
                                        self.__lst_solution[i-1][0],
                                        self.get_beta(),
                                        self.__lst_solution[i-1][1],
                                        self.__lst_solution[i-1][2])
            lst_surface.append(vol_surf)
            result = np.column_stack((self.__npa_strike_buckets[i], vol_surf))
            result = result[result[:,0].argsort()]
            
            original = np.column_stack((self.__npa_strike_buckets[i], 
                                        self.__npa_implied_vol_mid_buckets[i]))
            original = original[original[:,0].argsort()]
            
            plt.plot(result[:,0], result[:,1], label=i)
            plt.scatter(original[:,0], original[:,1])
            plt.legend()
            plt.show()
                        
            #plt.plot(self.__npa_strike_buckets[i], vol_surf, label=i)
            #plt.scatter(self.__npa_strike_buckets[i], self.__npa_implied_vol_buckets[i])
            #plt.legend()
            
        return lst_surface                       
    
    def visualize(self):
        pass
    
    def compute_atm_strike(self):
        return self.__lst_unique_strikes[np.abs(np.asarray(self.__lst_unique_strikes) - 
                                                self.__dbl_spot).argmin()]
            
    def set_beta(self, dbl_beta):
        self.__dbl_beta = dbl_beta
        
    def set_spot(self, dbl_spot):
        self.__dbl_spot = dbl_spot
        
    def get_beta(self):
        return self.__dbl_beta
    
    def get_spot(self):
        return self.__dbl_spot
    
    def get_time_to_maturity(self):
        return self.__df_time_to_maturity
    
    def get_strikes(self):
        return self.__df_strikes
    
    def get_atm_strike(self):
        return self.__dbl_atm_strike
    
    def get_solution(self):
        return self.__lst_solution

def process_bloomberg_opt_ticker(str_bloomberg_ticker):
    pass

def extract_strike(str_bloomberg_ticker):
    return float(str_bloomberg_ticker.split(' ')[3][1:])

def extract_time_to_maturity(str_bloomberg_ticker, year_basis = 360.0):
    expiry_date = dateutil.parser.parse(str_bloomberg_ticker.split(' ')[2])    
    return float((expiry_date - datetime.datetime.today()).days) / year_basis

class BloombergVolatilitySurface():
    def __init__(self, lst_bval_csv_paths, 
                 str_delimiter='|',
                 lst_skiprows=[0],
                 dtype=str,
                 bln_dup_bid_ask=False,
                 bln_by_moneyness=True,
                 bln_by_tenor=True):
        if type(lst_bval_csv_paths) is str:
            lst_bval_csv_paths = [lst_bval_csv_paths]
        
        self.__df_data = pd.concat([pd.read_csv(file,
                                         skiprows=lst_skiprows,
                                         delimiter=str_delimiter,
                                         dtype=dtype) for file in lst_bval_csv_paths])
        
        self.__df_data.columns = [col.strip().upper() for col in self.__df_data.columns]
        self.__df_data['TICKER'] = self.__df_data['TICKER'].str.replace(' Equity', '', regex=False)
        self.__df_data = self.__df_data[self.__df_data['TICKER']!='END-OF-DATA VOLA']
        self.__df_data.dropna(how='all', inplace=True)
        
        if bln_by_moneyness:
            if bln_by_tenor:
                self.__df_data.set_index(['TICKER', 'TENOR', 'MONEYNESS'], inplace=True)
            else:
                self.__df_data.set_index(['TICKER', 'EXPIRY', 'MONEYNESS'], inplace=True)
        else:
            if bln_by_tenor:
                self.__df_data.set_index(['TICKER', 'TENOR', 'STRIKE'], inplace=True)
            else:
                self.__df_data.set_index(['TICKER', 'EXPIRY', 'STRIKE'], inplace=True)
                
        if bln_dup_bid_ask:
            self.__df_data['BID'] = self.__df_data['MID']
            self.__df_data['ASK'] = self.__df_data['MID']
        
    def __repr__(self):
        pass
    
    def __len__(self):
        pass
    
    def get_surface(self, lst_tickers=None):
        if lst_tickers:
            if type(lst_tickers) is list:
                return self.__df_data.loc[lst_tickers]
            elif type(lst_tickers) is str:
                return self.__df_data.loc[[lst_tickers]]
            else:
                logger.debug('Please pass string or list to `lst_tickers`.')
        else:
            return self.__df_data
                
    def stack_surface(self):
        pass
    
    def diff_surface(self, df_bloomberg_volatility_surface,
                     str_col_to_compare='MID'):
        self.__df_data = self.get_surface().merge(df_bloomberg_volatility_surface,
                                         left_index=True, right_index=True)
        self.__df_data['DIFF'] = (self.__df_data[str_col_to_compare + '_x'].astype(np.float64) - 
                                  self.__df_data[str_col_to_compare + '_y'].astype(np.float64))
        self.__df_data.rename(columns={str_col_to_compare+'_x':str_col_to_compare+'_LEFT', str_col_to_compare+'_y':str_col_to_compare+'_RIGHT'}, inplace=True)
        lst_cols_to_drop = [col for col in self.__df_data.columns if '_y' in col]
        self.__df_data.drop(columns=lst_cols_to_drop, inplace=True)
        self.__df_data.columns = [col.replace('_x','') for col in self.__df_data.columns]
        return self.__df_data        

if __name__ == '__main__':
    
    # Obtaining data from Bloomberg API
    # (Enhance modBloomberg3 to factor in NULL returns)
    
    import modBloomberg3 as bbg
    from itertools import zip_longest
    
    str_ticker = '700 HK Equity'
    opt_chain = bbg.bloomberg_bds(str_ticker, 'OPT_CHAIN')[0][0]
    implied_vol = bbg.bloomberg_bdp(opt_chain, ['IVOL_MID', 'IVOL_BID', 'IVOL_ASK'])
    forward_price = bbg.bloomberg_bdp(opt_chain, ['IMPLIED_FORWARD_PRICE'])
    spot = bbg.bloomberg_bdp(str_ticker, 'PX_LAST')[0][0]
    
    implied_vol = list(zip_longest(*implied_vol))
    
    implied_vol = [[ele if ele!='' else '0' for ele in list(tup)]
                        for tup in implied_vol]
            
    SABR_model = SABR(float(spot), opt_chain,
                      list(map(float, *zip_longest(*forward_price))),
                      list(map(float,implied_vol[0])),
                      list(map(float,implied_vol[1])),
                      list(map(float,implied_vol[2]))
                      )
    solution = SABR_model.calibrate()
    SABR_model.gen_surface()
    
    
    
    
    
    
    # Obtaining data from GeneralPricer
    
    str_folder_path = r"//nas05/nas05_apps/gm_gms/T_Equities/Equity Warehousing/5. Personal Folders/3. Lim Yuan Qing/Projects/97. Exotic Options (WIP)/1. Volatility Surfaces/1. SABR/3. Data/"
    str_todate = datetime.datetime.now().strftime('%Y%m%d')
    str_ticker = '700 HK'
    df_data = pd.read_csv(str_folder_path + str_ticker + '_' + str_todate + '.csv').dropna(how='any')
    print(df_data['VOL_MID'])
    
    df_bloomberg_ticker = df_data.loc[:, ['OPT_CHAIN']]
    df_forward_price = df_data.loc[:,['FORWARD_PRICE']]
    df_implied_vol_mid = df_data.loc[:,['VOL_MID']]
    df_implied_vol_bid = df_data.loc[:,['VOL_BID']].fillna(0.0)
    df_implied_vol_ask = df_data.loc[:,['VOL_ASK']].fillna(0.0)
    
    del df_data
        
    SABR_model = SABR(343.80, df_bloomberg_ticker.iloc[:,0].tolist(),
                      df_forward_price.iloc[:,0].tolist(),
                      (df_implied_vol_mid.iloc[:,0]/100).tolist(),
                      (df_implied_vol_bid.iloc[:,0]/100).tolist(),
                      (df_implied_vol_ask.iloc[:,0]/100).tolist()
                      )
    solution = SABR_model.calibrate()
    SABR_model.gen_surface()