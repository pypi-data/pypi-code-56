import numpy as np
import matplotlib.pyplot as plt
from pynverse import inversefunc

def g(z):
    '''------------------------------------------------------------------------                                                                                                   
    --- g : The gravitational acceleration is taken from Wolfire et al                                                                                                                                                                                            
    (1995) and Spergel (1994)                                                                                                                                                                                                                                      
    
    Parameters : z [pc]                                                                                                                                                                                                                                             
    Return     : g [cm.s-2]                                                                                                                                                                                                                                           
    ---------------------------------------------------------------------------'''
    return 9.5e-9 * np.tanh(z/400)

def nWIM(z):
    l_wim = 1000.
    n0_wim = 0.025
    nz_wim = n0_wim * np.exp(-z/l_wim)

    return nz_wim

def nHIM(z):
    l_him = 3000.    
    n0_him = 0.0015
    nz_him = n0_him * np.exp(-z/l_him)
    return nz_him

def P_k(z):
    '''------------------------------------------------------------------------                                                                                                                                                                                
    --- P_k : For T=10^6K / see Wolfire (1995)                                                                                                                                                                                                                              

    
    Parameters : z    [kpc] !Warning                                                                                                                                                                                                                             
    Return     : P_k  [K.cm-3]                                                                                                                                                                                                                                      
    ---------------------------------------------------------------------------'''

    return 2250. * (1. + (z**2 / 19.6))**(-1.35)

def nHI(z):
    '''------------------------------------------------------------------------                                                                                                                                                                                        
    --- nHI : The "Reynolds layer" plus the mean H I density of Dickey &                                                                                                                                                                                               
    Lockman (1990)                                                                                                                                                                                                                                                  
    
    Parameters : z   [pc]                                                                                                                                                                                                                                       
    Return     : nHI [cm-3]                                                                                                                                                                                                                                         
    ---------------------------------------------------------------------------'''
    l_wnm = 530.
    l_cnm = 212.
    l_exp = 403.
    
    sig_wnm = l_wnm/2.355
    sig_cnm = l_cnm/2.355
    
    n0_wnm = 0.107
    n0_cnm = 0.395
    n0_exp = 0.064
        
    nz_wnm = n0_wnm * np.exp(-z**2./(2.*sig_wnm**2.))
    nz_cnm = n0_cnm * np.exp(-z**2./(2.*sig_cnm**2.))
    nz_exp = n0_exp * np.exp(-z/l_exp)
   
    nz_tot = nz_wnm+nz_cnm+nz_exp

    return nz_tot


def ntot(z):
    '''------------------------------------------------------------------------                                                                                                                                                                        
    --- ntot : The sum of the three componant of the diferent mean density                                                                                                                                                                                                   
                                                                                                                                                                                                                                                                       
    Parameters : z    [pc]                                                                                                                                                                                                                                     
    Return     : ntot [cm-3]                                                                                                                                                                                                                                       
    ---------------------------------------------------------------------------'''
    return nWIM(z) + nHIM(z) + nHI(z)

def vt(z, NHI, Cd):
    '''------------------------------------------------------------------------                                                                                                                                                                                      
    --- vt : The terminal velocity from Benjamin & Danly                                                                                                                                                          
                                                                                                                                                                                                                                                                          
    Parameters : z [pc]                                                                                                                                                                                                                                         
    NHI [cm-2]                                                                                                                                                                                                                                       
    
    Return     : vt [cm.s-1]                                                                                                                                                                                                                                         
    ---------------------------------------------------------------------------'''
    return np.sqrt(2.*g(z) * NHI / Cd / ntot(z)) #* np.sin(b)


if __name__ == '__main__':    
    z   = np.linspace(100, 100000, 1000)
    WIM = nWIM(z)
    HIM = nHIM(z)
    HI  = nHI(z)
    TOT = ntot(z)
    
    fig = plt.figure(figsize=(14,9))
    ax  = fig.add_subplot(1, 1, 1)
    ax.set_ylim([1.e-6, 1])
    ax.set_xlim([100, 100000])
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.plot(z, WIM, color = 'g', linewidth=2., label='WIM (fixme ref)')
    ax.plot(z, HIM, color = 'r', linewidth=2., label='HIM (fixme ref)')
    ax.plot(z, HI,  color = 'b', linewidth=2., label='HI  (Dickey & Lockman 1990)')
    ax.plot(z, TOT, color='k', linewidth=2.5, label='WIM + HIM + HI')
    legend = ax.legend(loc=1, shadow=True)
    frame = legend.get_frame()
    frame.set_facecolor('0.90')
    for label in legend.get_texts():
        label.set_fontsize('large')
    for label in legend.get_lines():
        label.set_linewidth(1.5)
    # for i in range(len(TOT)):                                                                                                   
    #     ax.plot(inversefunc(BD.ntot, y_values=TOT[i]), np.log10(TOT[i]), marker='.')                                              
        
    ax.set_xlabel(r'z (pc)', fontsize=18)
    ax.set_ylabel(r'n$_h$(z) (cm$^{-3}$)', fontsize=18)
    # fig.savefig('../plot/ntot.pdf', format='pdf')

    # stop
    # # '''________________________________________________________________________________________'''
    # b        = [np.pi/6, np.pi/4, np.pi/3, np.pi/2]
    # log10NHI = [18., 18.5, 19, 19.5, 20.]
    
    # fig = plt.figure(figsize=(12,10))
    # ax  = fig.add_subplot(1, 1, 1)
    # plt.locator_params(nbins=4)
    # for j in range(len(b)):
    #     plt.tight_layout()
    #     plt.subplot(2, 2, j+1)
    #     plt.ylim(0, 400)
    #     for _ in log10NHI:
    #         invVr = inversefunc((lambda x: np.sin(np.abs(b[j])) * np.sqrt(2.*g(x)*10**(_) / ntot(x))))
    #         z     = np.linspace(100, 50000, 2000)
    #         inv   = invVr(Vr(z, 10**(_), b[j], 1.))
    #         plt.plot(z, Vr(z, 10**(_), b[j], 1.)*1.e-5, label='$log_{10} NHI = $' + str(_))
    #     plt.xscale('log')
    #     plt.xlabel('$z [pc]$')
    #     plt.ylabel('$V_T [km/s]$')
    #     if j == 0:
    #         plt.legend(loc=2)
    #         leg = plt.gca().get_legend()
    #         ltext  = leg.get_texts()
    #         plt.setp(ltext, fontsize='small')
    #     plt.title('b = ' + str(b[j])[:4] + ' rad', fontsize=10)
    # # plt.savefig('../plot/Vtz.pdf', format='pdf')




