import matplotlib.pyplot as plt
from .BinomialDistribution import Binomial

class Bernoulli(Binomial):
    """ 
    Bernoulli distribution class for calculating and visualizing a Bernoulli distribution.
    A Bernoulli distribution is a special case of a Binomial distribution (n = 1)
    
    Attributes:
        mean (float) representing the mean value of the distribution
        stdev (float) representing the standard deviation of the distribution
        data_list (list of floats) a list of floats to be extracted from the data file
        p (float) representing the probability of an event occurring
    """
    
    
    def __init__(self, prob = .5):

        self.n = 1        
        self.p = prob
        
        Binomial.__init__(self, self.p, self.n)

    def read_data_file(self):
        pass
        
    def plot_bar_pmf(self):

        """
        Function to plot the pmf of the Bernoulli distribution
        
        Args:
            None
        
        Returns:
            list: x values for the pmf plot
            list: y values for the pmf plot
            
        """
        
        # make the plots
        plt.bar(x = ['0', '1'], height = [self.pmf(0), self.pmf(1)])
        plt.title('Distribution of Outcomes')
        plt.ylabel('Probability')
        plt.xlabel('Outcome')

        plt.show()

        return x, y

    def pmf(self, k):

        """
        Probability mass function calculator for the bernoulli distribution.
        
        Args:
            k (unsigned int): point for calculating the probability mass function. k is in support (the set{0, 1})
        
        Returns:
            float: probability density function output
        """
        
        try:
            assert k in range(2), 'k isn\'t in support'
        except AssertionError as error:
            raise
        
        return 1 - self.p if k == 0 else self.p
