# -*- coding: utf-8 -*-
"""
Created on Mon Feb 24 10:22:19 2020

@author: yuanq
"""

from abc import ABC, abstractmethod

from dd8 import get_basic_logger, LOG_PRINT_LEVEL, LOG_WRITE_LEVEL
from dd8.finance.enums import ENUM_CALL_PUT, ENUM_OPTION_TYPE

logger = get_basic_logger(__name__, LOG_PRINT_LEVEL, LOG_WRITE_LEVEL)

class VanillaOption(object):
    """
    Each instance represents a vanilla option. Does not assume any asset class
    but instead takes parameters that have asset-class specific properties or 
    behaviour (e.g. `cost_of_carry` can take a equity.Dividend object).
    
    Attributes
    ----------
    dbl_initial : double
        initial price of underlying
    dbl_strike : double
        strike price of option
    dbl_time_to_maturity : double
        number of days between trade date and expiry date divided by 365
    rates : rates.DiscountCurve
        discount curve object for discounting of payoff
    volatility : volatility.VolatilitySurface
        volatility surface object to obtain pricing volatility
    cost_of_carry : quant.Schedule
        schedule object or any other inherited object (e.g. equity.Dividend)
    bln_is_put : boolean, optional
        indicates if option is a put or call option (default is True, which
        implies option is a put option)
    bln_is_european : boolean, optional
        indicates if option is a European or American option (default is True,
        which implies option is a European option)
    underlying: quant.Underlying, optional
        underlying object or any other inherited object (e.g. equity.Security)
        (default is None, which implies a generic vanilla option)    
    """
    def __init__(self,
                 dbl_initial_price,
                 dbl_strike_price,
                 dbl_time_to_maturity,
                 rates,
                 volatility,
                 cost_of_carry,
                 bln_is_put=True,
                 bln_is_european=True,
                 underlying=None):
        self.__initial_price = dbl_initial_price
        self.__strike_price = dbl_strike_price
        self.__time_to_maturity = dbl_time_to_maturity
        self.__rates = rates
        self.__volatility = volatility
        self.__cost_of_carry = cost_of_carry
        self.__is_put = bln_is_put
        self.__is_european = bln_is_european
        self.__underlying = underlying
        
        if self.__is_put:
            self.__call_put = ENUM_CALL_PUT.PUT
        else:
            self.__call_put = ENUM_CALL_PUT.CALL

    def price(self):
        pass
    
    @property
    def initial_price(self):
        return self.__initial_price
    
    @initial_price.setter
    def initial_price(self, dbl_initial_price):        
        self.__initial_price = dbl_initial_price
    
    @property
    def strike_price(self):
        return self.__strike_price
    
    @strike_price.setter
    def strike_price(self, dbl_strike_price):
        self.__strike_price = dbl_strike_price
    
    @property
    def rates(self):
        return self.__rates
    
    @rates.setter
    def rates(self, rates):
        self.__rates = rates
        
    @property
    def volatility(self):
        return self.__volatility
    
    @volatility.setter
    def volatility(self, volatility):
        self.__volatility = volatility
        
    @property
    def cost_of_carry(self):
        return self.__cost_of_carry
    
    @cost_of_carry.setter
    def cost_of_carry(self, cost_of_carry):
        self.__cost_of_carry = cost_of_carry
        
    @property
    def is_put(self):
        return self.__is_put
    
    @is_put.setter
    def is_put(self, bln_is_put):
        self.__is_put = bln_is_put
        if self.__is_put:
            self.__call_put = ENUM_CALL_PUT.PUT
        else:
            self.__call_put = ENUM_CALL_PUT.CALL
        
    @property
    def is_european(self):
        return self.__is_european
    
    @is_european.setter
    def is_european(self, bln_is_european):
        self.__is_european = bln_is_european
        
    @property
    def underlying(self):
        return self.__underlying
    
    @underlying.setter
    def underlying(self, underlying):
        self.__underlying = underlying


class PricingModel(ABC):
    """
    Abstract Base Class for vanilla pricing models. `PricingModel` objects 
    should always be initiated with model parameters and not with the instrument
    to be priced, for consistent implementation. The instrument is then passed
    to the `PricingModel` object via the `price()` method.
    """
    def __init__(self):
        pass
    
    # for del method
    def __del__(self):
        pass
    
    def __repr__(self):
        pass
    
    # for print()
    def __str__(self):
        pass
    
    # for len()
    def __len__(self):
        pass
    
    @abstractmethod
    def price(self):
        pass
    
    def gen_greeks_basic(self):
        pass
    
    def gen_greeks_full(self):
        pass

class BlackScholesMertonModel(PricingModel):
    """
    Implements the generalized Black-Scholes-Merton model for pricing of European
    options.
    
    Attributes
    ----------
    option : vanilla.VanillaOption
        vanilla European option object    
    """
    def __init__(self):
        self.__option = None
        self.__dbl_d1 = None
        self.__dbl_d2 = None
        self.__dbl_price = None
        
        
    @property
    def option(self):
        return self.__option
    
    @option.setter
    def option(self, option):
        if option:
            if not option.type == ENUM_OPTION_TYPE.EUROPEAN:
                raise ValueError("""Black-Scholes-Merton model can only be used 
                                 to price European options.""")
            
    def price(self, option):
        """
        Price the vanilla option.
        
        Parameters
        ----------
        
        Return
        ------
        """
        self.option = option
        if self.option.is_put:
            self.__dbl_price = ((self.__dbl_strike_price * 
                                 self.__dbl_riskfree_discount *
                                 (1.0-self.__dbl_cdf_d2)) -
                                (self.__dbl_initial_price * 
                                 self.__dbl_dividend_discount *
                                 (1.0-self.__dbl_cdf_d1)))
        else:
            self.__dbl_price = ((self.__dbl_initial_price * 
                                 self.__dbl_dividend_discount *
                                 self.__dbl_cdf_d1) -
                                (self.__dbl_strike_price * 
                                 self.__dbl_riskfree_discount *
                                 self.__dbl_cdf_d2))
        
        

class BlackScholesModel(PricingModel):
    int_option_count = 0
    def __init__(self,                
                 enum_call_put,
                 dbl_initial_price,
                 dbl_strike_price,
                 dbl_time_to_maturity,
                 dbl_riskfree_rate,
                 dbl_volatility,
                 dbl_dividend_yield):
        
        self.__enum_call_put = enum_call_put
        self.__dbl_initial_price = float(dbl_initial_price)
        self.__dbl_strike_price = float(dbl_strike_price)
        self.__dbl_time_to_maturity = float(dbl_time_to_maturity)
        self.__dbl_riskfree_rate = float(dbl_riskfree_rate)
        self.__dbl_volatility = float(dbl_volatility)
        self.__dbl_dividend_yield = float(dbl_dividend_yield)
                
        self.update_riskfree_discount()
        self.update_dividend_discount()        
        self.update_cost_of_carry()        
        
        BlackScholesModel.int_option_count += 1
    
    def __del__(self):
        BlackScholesModel.int_option_count -= 1
        
    def __repr__(self):
        return (self.__class__.__name__ + '(' +
                str(self.__enum_call_put) + ',"' +
                str(self.__dbl_initial_price) + '",' +
                str(self.__dbl_strike_price) + ',' +
                str(self.__dbl_time_to_maturity) + ',' +
                str(self.__dbl_riskfree_rate) + ',' +
                str(self.__dbl_volatility) + ',' +
                str(self.__dbl_dividend_yield) + ')')
    
    def __len__(self):
        pass
   
    def __str__(self):
        return '''
        Option #{int_option_count} \n
        
        Type: {enum_call_put} \n
        Spot: {dbl_initial_price} \n
        Strike: {dbl_strike_price} \n
        Time To Maturity: {dbl_time_to_maturity} \n
        Riskfree Rate: {dbl_riskfree_rate} \n
        Volatility: {dbl_volatility} \n
        Dividend Yield: {dbl_dividend_yield} \n    
        '''.format(int_option_count = BlackScholesModel.int_option_count,
                    enum_call_put = self.__enum_call_put,
                    dbl_initial_price = self.__dbl_initial_price,
                    dbl_strike_price = self.__dbl_strike_price,
                    dbl_time_to_maturity = self.__dbl_time_to_maturity,
                    dbl_riskfree_rate = self.__dbl_riskfree_rate,
                    dbl_volatility = self.__dbl_volatility,
                    dbl_dividend_yield = self.__dbl_dividend_yield)

    def update_cost_of_carry(self):
        self.__dbl_cost_of_carry = self.__dbl_riskfree_rate - self.__dbl_dividend_yield 
        self.update_d1()
        return self.__dbl_cost_of_carry

    def update_d1(self):
        self.__dbl_d1 = (
                (math.log(self.__dbl_initial_price/self.__dbl_strike_price) +
                 (self.__dbl_cost_of_carry + (self.__dbl_volatility**2.0)/2.0) * self.__dbl_time_to_maturity) /
                 (self.__dbl_volatility * (self.__dbl_time_to_maturity ** 0.5))  
                 )
        self.update_d2()
        return self.__dbl_d1        
                
    def update_d2(self):
        self.__dbl_d2 = self.__dbl_d1 - (self.__dbl_volatility * (self.__dbl_time_to_maturity ** 0.5))
        self.update_densities()
        self.price()
        return self.__dbl_d2
    
    def update_densities(self):
        self.__dbl_pdf_d1 = scipy.stats.norm.pdf(self.__dbl_d1)
        self.__dbl_pdf_d2 = scipy.stats.norm.pdf(self.__dbl_d2)
        self.__dbl_cdf_d1 = scipy.stats.norm.cdf(self.__dbl_d1,0.0,1.0)
        self.__dbl_cdf_d2 = scipy.stats.norm.cdf(self.__dbl_d2,0.0,1.0)
        return (self.__dbl_pdf_d1, self.__dbl_cdf_d1, self.__dbl_pdf_d2, self.__dbl_cdf_d2)        
    
    def update_dividend_discount(self):
        self.__dbl_dividend_discount = math.exp(- self.__dbl_dividend_yield *self.__dbl_time_to_maturity)
        return self.__dbl_dividend_discount
    
    def update_riskfree_discount(self):
        self.__dbl_riskfree_discount = math.exp(-self.__dbl_riskfree_rate * self.__dbl_time_to_maturity)
        return self.__dbl_riskfree_discount

    def price(self):
        if self.__enum_call_put == enums.ENUM_CALL_PUT.PUT:
            self.__dbl_price = ((self.__dbl_strike_price * 
                                 self.__dbl_riskfree_discount *
                                 (1.0-self.__dbl_cdf_d2)) -
                                (self.__dbl_initial_price * 
                                 self.__dbl_dividend_discount *
                                 (1.0-self.__dbl_cdf_d1)))
        elif self.__enum_call_put == enums.ENUM_CALL_PUT.CALL:
            self.__dbl_price = ((self.__dbl_initial_price * 
                                 self.__dbl_dividend_discount *
                                 self.__dbl_cdf_d1) -
                                (self.__dbl_strike_price * 
                                 self.__dbl_riskfree_discount *
                                 self.__dbl_cdf_d2))
        return self.__dbl_price
    
    def gen_greeks_basic(self):
        self.__dic_greeks = dict()
        self.__dic_greeks['SPOT_DELTA'] = self.gen_spot_delta()
        
        return self.__dic_greeks

    def gen_greeks_full(self):
        self.__dic_greeks = dict()
        self.__dic_greeks['SPOT_DELTA'] = self.gen_spot_delta()
        self.__dic_greeks['VANNA'] = self.gen_vanna()
        self.__dic_greeks['CHARM'] = self.gen_charm()
        self.__dic_greeks['GAMMA'] = self.gen_gamma()
        self.__dic_greeks['GAMMA_PERC'] = self.gen_gamma_perc()
        self.__dic_greeks['ZOMMA'] = self.gen_zomma()
        self.__dic_greeks['ZOMMA_PERC'] = self.gen_zomma_perc()
        self.__dic_greeks['SPEED'] = self.gen_speed()
        self.__dic_greeks['SPEED_PERC'] = self.gen_speed_perc()
        self.__dic_greeks['COLOUR'] = self.gen_colour()
        self.__dic_greeks['COLOUR_PERC'] = self.gen_colour_perc()
        self.__dic_greeks['VEGA'] = self.gen_vega()        
        self.__dic_greeks['VEGA_PERC'] = self.gen_vega()        
        self.__dic_greeks['VOMMA'] = self.gen_vomma()
        self.__dic_greeks['VOMMA_PERC'] = self.gen_vomma_perc()
        self.__dic_greeks['ULTIMA'] = self.gen_ultima()
        self.__dic_greeks['VEGA_BLEED'] = self.gen_vega_bleed()
        self.__dic_greeks['THETA'] = self.gen_theta()
        self.__dic_greeks['THETA_THEORETICAL'] = self.gen_theta(True)
        self.__dic_greeks['RHO'] = self.gen_rho()
        return self.__dic_greeks

    def gen_spot_delta(self):
        if self.__enum_call_put == enums.ENUM_CALL_PUT.PUT:
            return (self.__dbl_dividend_discount*(self.__dbl_cdf_d1 - 1.0))            
        elif self.__enum_call_put == enums.ENUM_CALL_PUT.CALL:
            return (self.__dbl_dividend_discount*self.__dbl_cdf_d1)

    def gen_vanna(self, variance_form = False):
        vanna = ((-self.__dbl_dividend_discount * self.__dbl_d2 * self.__dbl_pdf_d1)/
                self.__dbl_volatility)
        if variance_form:
            return vanna * (self.__dbl_initial_price/(2.0*self.__dbl_volatility))
        else:
            return vanna
           
    def gen_charm(self):
        if self.__enum_call_put == enums.ENUM_CALL_PUT.PUT:
            return (-self.__dbl_dividend_discount * ( 
                    (self.__dbl_pdf_d1 * ((self.__dbl_cost_of_carry/
                        (self.__dbl_volatility * self.__dbl_time_to_maturity**0.5))-
                        (self.__dbl_d2 / (2.0*self.__dbl_time_to_maturity)))) -
                    ((self.__dbl_cost_of_carry-self.__dbl_riskfree_rate)*(1.0-self.__dbl_cdf_d1))
                        )
                    )
        elif self.__enum_call_put == enums.ENUM_CALL_PUT.CALL:
            return (-self.__dbl_dividend_discount * ( 
                    (self.__dbl_pdf_d1 * ((self.__dbl_cost_of_carry/
                        (self.__dbl_volatility * self.__dbl_time_to_maturity**0.5))-
                        (self.__dbl_d2 / (2.0*self.__dbl_time_to_maturity)))) +
                    ((self.__dbl_cost_of_carry-self.__dbl_riskfree_rate)*(self.__dbl_cdf_d1))
                        )
                    )

    def gen_gamma(self):
        return ((self.__dbl_pdf_d1 * self.__dbl_dividend_discount) /
                 (self.__dbl_initial_price * self.__dbl_volatility * 
                  (self.__dbl_time_to_maturity**0.5)))
    
    def gen_gamma_perc(self):
        return (self.gen_gamma() * self.__dbl_initial_price) / 100.0
    
    def gen_zomma(self):
        return self.gen_gamma() * ((self.__dbl_d1 * self.__dbl_d2 - 1.0)/self.__dbl_volatility)
    
    def gen_zomma_perc(self):
        return self.gen_gamma_perc() * ((self.__dbl_d1 * self.__dbl_d2 - 1.0)/self.__dbl_volatility)
    
    # d(gamma)/d(spot)
    def gen_speed(self):
        return (-self.gen_gamma()*(1.0 + (self.__dbl_d1/(self.__dbl_volatility * self.__dbl_time_to_maturity**0.5))))/self.__dbl_initial_price
    
    def gen_speed_perc(self):
        return (-self.gen_gamma()*self.__dbl_d1) / (100.0 * self.__dbl_volatility * self.__dbl_time_to_maturity**0.5)
    
    def gen_colour(self):
        return (self.gen_gamma() * (self.__dbl_riskfree_rate - self.__dbl_cost_of_carry + 
                              ((self.__dbl_cost_of_carry * self.__dbl_d1)/(self.__dbl_volatility*self.__dbl_time_to_maturity**0.5)) + 
                              ((1.0 - self.__dbl_d1 * self.__dbl_d2)/(2.0*self.__dbl_time_to_maturity))))
                
    def gen_colour_perc(self):
        return (self.gen_gamma_perc() * (self.__dbl_riskfree_rate - self.__dbl_cost_of_carry + 
                              ((self.__dbl_cost_of_carry * self.__dbl_d1)/(self.__dbl_volatility*self.__dbl_time_to_maturity**0.5)) + 
                              ((1.0 - self.__dbl_d1 * self.__dbl_d2)/(2.0*self.__dbl_time_to_maturity))))
    
    def gen_vega(self, variance_form = False):
        vega = (self.__dbl_initial_price * self.__dbl_dividend_discount *
                self.__dbl_pdf_d1 * (self.__dbl_time_to_maturity ** 0.5))
        if variance_form:
            return vega / (2.0*self.__dbl_volatility)
        else:
            return vega
        
    def gen_vega_perc(self):
        return (self.__dbl_volatility/10.0) * self.gen_vega()
    
    def gen_vomma(self, variance_form = False):
        if variance_form:
            return ((self.gen_vega(True) / (2.0 * self.__dbl_volatility**2.0)) * 
                    (self.__dbl_d1*self.__dbl_d2 - 1.0))
        else:
            return self.gen_vega() * ((self.__dbl_d1*self.__dbl_d2)/self.__dbl_volatility) 
    
    def gen_vomma_perc(self):
        return self.gen_vega_perc() * ((self.__dbl_d1*self.__dbl_d2)/self.__dbl_volatility)
    
    def gen_ultima(self):
        return (self.gen_vomma() * (1.0/self.__dbl_volatility) * 
                (self.__dbl_d1 * self.__dbl_d2 - 
                 self.__dbl_d1 / self.__dbl_d2 - 
                 self.__dbl_d2 / self.__dbl_d1 - 1.0)
                )
                
    def gen_vega_bleed(self):
        return self.gen_vega() * (self.__dbl_riskfree_rate - self.__dbl_cost_of_carry +
                            ((self.__dbl_cost_of_carry * self.__dbl_d1) / (self.__dbl_volatility * self.__dbl_time_to_maturity**0.5)) - 
                            ((1.0 + self.__dbl_d1 * self.__dbl_d2) / (2.0 * self.__dbl_time_to_maturity)))
    
    def gen_theta(self, bln_theoratical = False):
        if bln_theoratical:
            if self.__enum_call_put == enums.ENUM_CALL_PUT.PUT:
                return (
                        ((-self.__dbl_initial_price * self.__dbl_dividend_discount * self.__dbl_pdf_d1 * self.__dbl_volatility)/(2.0*self.__dbl_time_to_maturity**0.5)) +        
                            ((self.__dbl_cost_of_carry-self.__dbl_riskfree_rate) * self.__dbl_initial_price * self.__dbl_dividend_discount * (1.0 - self.__dbl_cdf_d1)) + 
                            ((self.__dbl_riskfree_rate*self.__dbl_strike_price*self.__dbl_riskfree_discount*(1.0-self.__dbl_cdf_d2)))
                            )        
            elif self.__enum_call_put == enums.ENUM_CALL_PUT.CALL:
                return (
                        ((-self.__dbl_initial_price * self.__dbl_dividend_discount * self.__dbl_pdf_d1 * self.__dbl_volatility)/(2.0*self.__dbl_time_to_maturity**0.5)) -     
                            ((self.__dbl_cost_of_carry-self.__dbl_riskfree_rate) * self.__dbl_initial_price * self.__dbl_dividend_discount * self.__dbl_cdf_d1) -
                            ((self.__dbl_riskfree_rate*self.__dbl_strike_price*self.__dbl_riskfree_discount*self.__dbl_cdf_d2))
                            )
        else:
            dbl_time_to_maturity_old = self.get_time_to_maturity()
            dbl_price_old = self.price()
            self.set_time_to_maturity(dbl_time_to_maturity_old - 1.0/360.0)
            theta = self.price() - dbl_price_old
            self.set_time_to_maturity(dbl_time_to_maturity_old)
            self.price()
            return theta
        
    def gen_rho(self):
        if self.__enum_call_put == enums.ENUM_CALL_PUT.PUT:
            return (-self.__dbl_time_to_maturity * self.__dbl_strike_price * 
                    math.exp(-self.__dbl_riskfree_rate*self.__dbl_time_to_maturity) * 
                    (1.0-self.__dbl_cdf_d2))
        elif self.__enum_call_put == enums.ENUM_CALL_PUT.CALL:
            return (self.__dbl_time_to_maturity * self.__dbl_strike_price * 
                    math.exp(-self.__dbl_riskfree_rate*self.__dbl_time_to_maturity) * 
                    self.__dbl_cdf_d2)
    ## Getters

    def get_initial_price(self):
        return self.__dbl_initial_price
    
    def get_strike_price(self):
        return self.__dbl_strike_price
    
    def get_time_to_maturity(self):
        return self.__dbl_time_to_maturity
    
    def get_riskfree_rate(self):
        return self.__dbl_riskfree_rate
    
    def get_volatility(self):
        return self.__dbl_volatility
    
    def get_dividend_yield(self):
        return self.__dbl_dividend_yield
    
    
    ## Setters
    
    def set_initial_price(self, dbl_initial_price):
        self.__dbl_initial_price = dbl_initial_price
        self.update_d1()        
        return self.__dbl_initial_price
    
    def set_strike_price(self, dbl_strike_price):
        self.__dbl_strike_price = dbl_strike_price
        self.update_d1()        
        return self.__dbl_strike_price
    
    def set_time_to_maturity(self, dbl_time_to_maturity):
        self.__dbl_time_to_maturity = dbl_time_to_maturity
        self.update_d1()        
        return self.__dbl_time_to_maturity
    
    def set_riskfree_rate(self, dbl_riskfree_rate):
        self.__dbl_riskfree_rate = dbl_riskfree_rate
        self.update_riskfree_discount()
        self.update_cost_of_carry()
        return self.__dbl_riskfree_rate
    
    def set_volatility(self, dbl_volatility):
        self.__dbl_volatility = dbl_volatility
        self.update_d1()        
        return self.__dbl_volatility
    
    def set_dividend_yield(self, dbl_dividend_yield):
        self.__dbl_dividend_yield = dbl_dividend_yield
        self.update_dividend_discount()
        self.update_cost_of_carry()
        return self.__dbl_dividend_yield

    

    


