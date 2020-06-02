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
                
    """
    
    def __init__(self,prob=.5, size=20):
                
        self.n = size
        self.p = prob
        
        Distribution.__init__(self, self.calculate_mean(), self.calculate_stdev())
        
    
    def calculate_mean(self):
        """Function to calculate the mean from p and n
        
        Args: 
            None
        
        Returns: 
            float: mean of the data set
    
        """
        self.mean = self.p*self.n
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
        """Function to calculate p and n from the data set. The function updates the p and n variables of the object.
        
        Args: 
            None
        
        Returns: 
            float: the p value
            float: the n value
    
        """
        self.n = len(self.data)
        self.p = 1.0*sum(self.data)/self.n
        self.mean = self.calculate_mean()
        self.stdev = self.calculate_stdev()
        
        return self.p , self.n
    
    
    def plot_bar(self):
        """Function to output a histogram of the instance variable data using 
        matplotlib pyplot library.
        
        Args:
            None
            
        Returns:
            None
        """
        vals = ['1', '0']
        count = [self.data[self.data == 1],self.data[self.data != 1]]
        plt.bar(vals,count)
        plt.title('Histogram of the Instance variable')
        plt.xlabel('Instance variable')
        plt.ylabel('Count')
      
    
    def pdf(self, k):
        """Probability density function calculator for the binomial distribution.
        
        Args:
            k (float): point for calculating the probability density function
            
        
        Returns:
            float: probability density function output
        """
        tmp = math.factorial(self.n)/(math.factorial(k)*math.factorial(self.n - k))
        tmp1 = (self.p**k)*((1-self.p)**(self.n - k))
        return tmp*tmp1

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
        
        # calculate the x values to visualize
        for i in range(self.n + 1):
            x.append(i)
            y.append(self.pdf(i))

        # make the plots
        plt.bar(x, y)
        plt.title('Distribution of Outcomes')
        plt.ylabel('Probability')
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
            
        return_binomial = Binomial()
        return_binomial.p = self.p
        return_binomial.n = self.n + other.n
        
        return return_binomial
        
        
    def __repr__(self):
        """Function to output the characteristics of the Binomial instance
        
        Args:
            None
        
        Returns:
            string: characteristics of the Binomial object
        
        """
        return "mean {}, standard deviation {}, p {}, n {}".format(self.mean, self.stdev, self.p, self.n)
    