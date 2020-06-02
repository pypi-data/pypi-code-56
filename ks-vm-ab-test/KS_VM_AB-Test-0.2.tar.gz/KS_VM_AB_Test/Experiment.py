import math
import matplotlib.pyplot as plt

class SetUp_Experiment():
    
    def __init__(self, power=0.8, sig=0.95):
    		
        """ Experiment Class - for set up and experiment analys
		
      Attributes:
			power (float) representing the power significence
			sig (float) representing the Statistical Significance
			"""
		
        self.power = power
        self.sig = sig
        self.n = 0

    def calculate_sample_size(self, p_base, p_effect):
    		
        """ Get the sample size of the

        Attributes:
            base probability (float) representing base
            effect probability (float) representing new expected probability
        """
        from scipy.stats import norm, zscore

        s = 1-self.sig
        z = norm.isf([s/2])
        zp = -1 * norm.isf([self.power])
        d = p_effect - p_base
        ss = 2 * ((p_effect + p_base)/2)*(1-((p_effect + p_base)/2))
        num = ss * ((zp + z)**2)/(d**2)
        self.n = int(round(num[0]))
        return self.n