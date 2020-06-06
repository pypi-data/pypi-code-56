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
        
    def plot_bar_pdf(self):

        """
        Function to plot the pdf of the Bernoulli distribution
        
        Args:
            None
        
        Returns:
            list: x values for the pdf plot
            list: y values for the pdf plot
            
        """
        
        # make the plots
        plt.bar(x = ['0', '1'], height = [self.pdf(0), self.pdf(1)])
        plt.title('Distribution of Outcomes')
        plt.ylabel('Probability')
        plt.xlabel('Outcome')

        plt.show()

        return x, y