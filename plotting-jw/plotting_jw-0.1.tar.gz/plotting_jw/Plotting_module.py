import pandas
import math
import matplotlib.pyplot as plt


class Plotting:
    def __init__(self, xvalues, yvalues, rep='', xlabel='', ylabel='', title=''):
        
        """ Generic plotting class for plotting a dataset.

		Attributes:
			xvalues (list) representing the horizontal values of the plot
			yvalues (list) representing the vertical values of the plot
			rep (string) representation type of the plot
            xlabel (string) label for x values
            ylabel(string) label for y values
            title (string) title of the plot figure
			"""
        
        self.xvalues = xvalues
        self.yvalues = yvalues
        self.rep = rep
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.title = title
        
    def title_label(self):
        """ Generic function to give a title and label the exis
        """
        plt.title(self.title)
        plt.xlabel(self.xlabel)
        plt.ylabel(self.ylabel)
        return
    
    def plt_plot(self):
        """ Basic plot
        """
        plt.plot(self.xvalues, self.yvalues)
        self.title_label()
        plt.show()
        return
    
    def plt_bar(self):
        """ Bar plot
        """
        plt.bar(self.xvalues, self.yvalues)
        self.title_label()
        plt.show()
        return
    