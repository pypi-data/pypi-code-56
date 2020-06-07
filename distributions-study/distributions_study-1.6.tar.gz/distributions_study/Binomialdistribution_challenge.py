import math
import matplotlib.pyplot as plt
from .Generaldistribution import Distribution


#     """ Binomial distribution class for calculating and 
#     visualizing a Binomial distribution.
    
#     Attributes:
#         mean (float) representing the mean value of the distribution
#         stdev (float) representing the standard deviation of the distribution
#         data_list (list of floats) a list of floats to be extracted from the data file
#         p (float) representing the probability of an event occurring
                
#     """
class Binomial(Distribution):
    
        
    def __init__(self, probability, distribution_size):
        self.p = probability
        self.n= distribution_size
    
        Distribution.__init__(self, self.calculate_mean(), self.calculate_stdev())
        
        

    def calculate_mean(self):
        
        """Function to calculate the mean from p and n
        
        Args: 
            None
        
        Returns: 
            float: mean of the data set
    
        """
        self.mean = 1.0*self.p*self.n
        return self.mean

    def calculate_stdev(self):
        
        """Function to calculate the standard deviation from p and n.
        
        Args: 
            None
        
        Returns: 
            float: standard deviation of the data set
    
        """
        self.stdev = math.sqrt(self.n*self.p*(1-self.p))
        return self.stdev
        
    
    def replace_stats_with_data(self):
#         self.read_data_file(self, file_name)
        self.n = len(self.data)
        self.p = self.data.count(1)/self.n
        self.mean = self.calculate_mean()
        self.stdev = self.calculate_stdev()
        return self.p, self.n
                                 
        
        """Function to calculate p and n from the data set. The function updates the p and n variables of the object.
        
        Args: 
            None
        
        Returns: 
            float: the p value
            float: the n value
    
        """
  
    def plot_bar(self):
        plt.bar(['0','1'], height= [self.data.count(0),self.data.count(1)])
        plt.xlabel('values')
        plt.ylabel('frequency')
        plt.title('Histogram for Binomial Distribution')
        plt.show()
        
        
        """Function to output a histogram of the instance variable data using 
        matplotlib pyplot library.
        
        Args:
            None
            
        Returns:
            None
        """
    
    def pdf(self, k):
        
        """Probability density function calculator for the binomial distribution.
        
        Args:
            k (float): point for calculating the probability density function
            
        
        Returns:
            float: probability density function output
        """
        a= 1.0 * math.factorial(self.n)/(math.factorial(k)*math.factorial(self.n - k))
        b= (self.p**k) * (1-self.p)**(self.n- k)
        return a*b
    
    def plot_bar_pdf(self):
        """Function to plot the pdf of the binomial distribution
        
        Args:
            None
        
        Returns:
            list: x values for the pdf plot
            list: y values for the pdf plot
            
        """
        x=[]
        y=[]
        
        for num in range(self.n+1):
            x.append(num)
            y.append(self.pdf(self, num))
        
        plt.bar(x, height= y)
        plt.xlabel('distribution size (trial numbers)')
        plt.ylabel('pdf')
        plt.title('PDF function Plot')
        plt.show()
        
        return x,y
                   
        
    
       
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
        additional = Binomial(0,1)
        additional.n = self.n + other.n
        additional.p= self.p
        additional.calculate_mean()
        additional.calculate_stdev()
        
        return additional
       
    def __repr__(self):
        
        """Function to output the characteristics of the Binomial instance
        
        Args:
            None
        
        Returns:
            string: characteristics of the Binomial object
        
        """
        return 'mean {}, standard deviation {}, p {}, n {}'.format(self.mean, self.stdev, self.p, self.n)
        
      
