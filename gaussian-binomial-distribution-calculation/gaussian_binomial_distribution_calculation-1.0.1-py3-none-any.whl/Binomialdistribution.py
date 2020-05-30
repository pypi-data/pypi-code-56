import math
import matplotlib.pyplot as plt
from .Generaldistribution import Distribution

class Binomial(Distribution):
    """ Binomial distribution class for calculating and 
    visualizing a Binomial distribution.
    
    Attributes:
        mean (float) representing the mean value of the distribution
        stdev (float) representing the standard deviation of the distribution
        data_list (list of floats) a list of floats to be extracted from the data file
        p (float) representing the probability of an event occurring
        n (int) the total number of trials
            
    """
    
    def __init__(self, prob=.5, size=20):
        self.p = prob
        self.n = size 
        mu = self.calculate_mean()
        sigma = self.calculate_stdev()
        Distribution.__init__(self, mu, sigma)          
    
    def calculate_mean(self):
    
        """Function to calculate the mean from p and n
        
        Args: 
            None
        
        Returns: 
            float: mean of the data set
    
        """                
        self.mean = self.n * self.p
        return self.mean

    def calculate_stdev(self):

        """Function to calculate the standard deviation from p and n.
        
        Args: 
            None
        
        Returns: 
            float: standard deviation of the data set
    
        """
        self.stdev = math.sqrt(self.n * self.p * (1 - self.p))
        return self.stdev
           
    def replace_stats_with_data(self):
    
        """Function to calculate p and n from the data set
        
        Args: 
            None
        
        Returns: 
            float: the p value
            float: the n value
    
        """        
        self.mean = self.calculate_mean()
        self.stdev = self.calculate_stdev()
        self.n = len(self.data)
        self.p = self.mean / self.n
        return self.p, self.n
        
    def plot_bar(self):
        """Function to output a histogram of the instance variable data using 
        matplotlib pyplot library.
        
        Args:
            None
            
        Returns:
            None
        """
        plt.bar(x = ['0', '1'], height = [(1 - self.p) * self.n, self.p * self.n])
        plt.title('Barchart of data')
        plt.ylabel('Counts')
        plt.xlabel('Outcome')      
        
    def pdf(self, k):
        """Probability density function calculator for the gaussian distribution.
        
        Args:
            k (float): point for calculating the probability density function.
            
        
        Returns:
            float: probability density function output
        """

        pdf = math.factorial(self.n) / (math.factorial(k) * math.factorial(self.n - k)) \
                           * (self.p ** k) * ((1 - self.p) ** (self.n - k)) 
        return pdf

    def plot_bar_pdf(self):

        """Function to plot the pdf of the binomial distribution
        
        Args:
            None
        
        Returns:
            list: x values for the pdf plot
            list: y values for the pdf plot
            
        """
        x = []
        y = []

        for i in range(len(self.data) + 1):
            tmp = i
            x.append(tmp)
            y.append(self.pdf(tmp))

        plt.bar(x, y)
        plt.title('Binomial Distribution for \n probability density function')
        plt.ylabel('Density')
        plt.xlabel('Outcome')
        plt.show()
        
        return x, y
                
    def __add__(self, other):
        
        """Function to add together two Binomial distributions with equal p
        
        Args:
            other (Binomial): Binomial instance
            
        Returns:
            Binomial: Binomial distribution
            
        """
        
        try:
            assert self.p == other.p, 'p values are not equal'
        except AssertionError as error:
            raise

        result = Binomial()
        result.mean = self.mean + other.mean
        result.stdev = self.stdev + other.stdev
        result.p = self.p
        result.n = self.n + other.n

        return result
            
    def __repr__(self):
    
        """Function to output the characteristics of the Binomial instance
        
        Args:
            None
        
        Returns:
            string: characteristics of the Gaussian
        
        """
        return f"mean {self.mean}, standard deviation {self.stdev}, p {self.p}, n {self.n}"

