import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter

def pdf_log(array, linewidth=2., color="c", label=None, xlabel=None, save=False, log=True, bins=None):
    if bins is None: bins = np.logspace(np.log10(np.nanmin(array)), np.log10(np.nanmax(array)), 200)  
    fig = plt.figure(0, figsize=(10, 10))
    ax = fig.add_subplot(111)
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.xaxis.set_major_formatter(ScalarFormatter())
    ax.yaxis.set_major_formatter(ScalarFormatter())
    ax.hist(array, bins=bins, log=log, histtype='step', color=color, normed=False, label=label, linewidth=linewidth)
    ax.set_xlim([np.min(array), np.max(array)])                                                                                                                                                                                                                                   
    if xlabel is not None: ax.set_xlabel(xlabel, fontsize = 16) 
    ax.set_ylabel(r'$PDF$', fontsize = 16)
    plt.legend(loc = 1, numpoints = 1)
    leg = plt.gca().get_legend()
    ltext  = leg.get_texts()
    plt.setp(ltext, fontsize = 'small')
    if save == True : plt.savefig(path_plot + 'PDF.png', format='png')   

if __name__ == '__main__':
    print("toto")
    xlabel = r'$NHI$'
    
    mu, sigma = 2, 0.1
    array = np.random.normal(mu, sigma, 1000)
    pdf_log(array)
