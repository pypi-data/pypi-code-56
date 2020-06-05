import numpy as np
from astropy import units as u
from scipy.optimize import fsolve

class wolfire(object):
        def __init__(self, T=3000, n=0.5, phi=0.5, G0=1.7, Zd=1., zeta=1., Zg=1, fCII=1., Ac=1.4e-4, Ao=3.2e-4, Nw=1.e19):
                super(wolfire, self).__init__()
                self.T = T
                self.n = n
                self.phi = phi
                self.G0 = G0
                self.Zd = Zd
                self.Zg = Zg
                self.zeta = zeta
                self.fCII = fCII
                self.Ac = Ac #wolfire 03
                self.Ao = Ao #wolfire 03
                self.Nw = Nw

        def ne(self):
            # return 0.021 *u.cm**-3
            return 2.4e-3 * self.zeta**0.5 * (self.T/100.)**0.25 * (self.G0/1.7)**0.5 * self.Zd**-0.5 * self.phi**-1 *u.cm**-3
            # return 2.4e-3 * (self.T/100.)**0.25 * (self.G0 / 1.7)**0.5 / self.phi *u.cm**-3 #HERACLES

        def eff03(self):
            ne = self.ne().value
            return 4.9e-2 / (1. + 4.e-3*(self.G0*self.T**0.5/ne/self.phi)**0.73) 
            + ((3.7e-2*(self.T/1.e4)**0.7)/(1. + 2.0e-4*(self.G0*self.T**0.5/ne/self.phi)))

        def eff95(self):
            param = self.G0*self.T**0.5/self.ne().value
            return 4.9e-2 / (1. + (param/1925.)**0.73) 
            + ((3.7e-2*(self.T/1.e4)**0.7)/(1. + (param/5000.))) #HERACLES

        def effBT(self):
            param = self.G0*self.T**0.5/self.ne().value
            return 4.87e-2 / (1. + 4.e-3*(param)**0.73) 
            + ((3.65e-2*(self.T/1.e4)**0.7)/(1. + 2.e-4*param))

        def heat(self):
            # return 1.e-24 * self.n * self.eff95() * self.G0 * u.erg * u.cm**-3 * u.s**-1 #HERACLES
            return 1.3e-24 * self.n * self.eff03() * self.G0 * u.erg * u.s**-1 * u.cm**-3

        def cool_CII(self):
            ne = self.ne().value
            return 2.54e-14 * self.Ac * (2.8e-7 * ne / self.n * (self.T/100.)**-0.5 + 8.e-10) * np.exp(-92/self.T) * u.erg * u.cm**3 * u.s**-1
            # return (92. * 1.38e-16 * 2. * (2.8e-7* ((self.T/100.)**(-0.5))*ne/self.n + 8.e-10*((self.T/100.)**(0.07))) * 3.5e-4 * 0.4 * np.exp(-92./ self.T)) * u.erg * u.cm**3 * u.s**-1 #From HERACLES so from Karl Joulain thesis

        def Tn(self,n):
            return self.T/10.**n

        def Omega(self):
            return 1.80 + 0.484*self.Tn(4) + 4.01*self.Tn(4)**2 - 3.39*self.Tn(4)**3

        def cool_CII95(self):
            ne = self.ne().value
            gamma = 8.86e-10
            gamma_e = 2.1e-7 * self.Tn(2)**-0.5 * self.Omega()
            return 2.54e-14 * self.Ac * self.fCII * (gamma + gamma_e*(ne/self.n)) * np.exp(-92/self.T) * u.erg * u.cm**3 * u.s**-1

        def cool_OI(self):
            # O = 4.5e-4 #HERACLES
            return 1.e-26 * self.Ao * self.T**0.5 * (24. * np.exp(-228./self.T) + 7.*np.exp(-326./self.T)) * u.erg * u.cm**3 * u.s**-1
            # return 1.e-26 * O * self.T**0.5 * (24. * np.exp(-228./self.T) + 7.*np.exp(-326./self.T)) * u.erg * u.cm**3 * u.s**-1 #HERACLES

        def cool_Ly(self):
            ne = self.ne().value
            return 7.3e-19 * ne / self.n * np.exp(-118400./self.T) * u.erg * u.cm**3 * u.s**-1 #HERACLES

        def cool_rec03(self):
            ne = self.ne().value
            return 4.65e-30 * self.T**0.94 * (self.G0 * self.T**0.5 / ne / self.phi)**(0.74/self.T**0.068) * ne / self.n * self.phi * u.erg * u.cm**3 * u.s**-1

        def cool_rec95(self):
            ne = self.ne().value
            return 4.65e-30 * self.T**0.94 * (self.G0 * self.T**0.5 / ne)**(0.74/(self.T**0.068)) * ne / self.n * u.erg * u.cm**3 * u.s**-1

        def cool(self):
            return (self.n*u.cm**-3)**2 * (self.cool_CII95() + self.cool_OI() + self.cool_Ly() + self.cool_rec03())

        def fsix(self,p2):
            return 0.990 - (2.74e-3*p2) + (1.13e-3*p2**2)

        def heatXR(self):
            p1=np.log10(self.Nw/1.e18)
            p2=np.log10(self.ne().value/self.n)
            XR = self.fsix(p2)*(-26.5 -(0.920*p1) + (5.89e-2*p1**2)) + self.fsix(p2)*0.96*np.exp(-((p1-0.38)/0.87)**2)
            return self.n * 10.**XR * u.erg * u.cm**-3 * u.s**-1 #FIXME
            
        def loss(self):
            return self.heat() + self.heatXR() - self.cool()
            # return self.heat() - self.cool()

        # def PminJenkins(self):
        #         return 5730. * (Zd * 1.)  * (Zd / (1. + 2.08*(Zd * 1.)**0.365)) #FIXME I/I0

if __name__ == '__main__':
        
        T = np.logspace(np.log10(1), np.log10(10000), 100)
        n = np.logspace(np.log10(0.01), np.log10(1000), 100)
        
        core = wolfire(T=T,n=1)
        cooling = core.cool()
        heating = core.heat()
                
        Teq = np.array([fsolve(lambda x: wolfire(T=x, n=n[i], G0=1.7, phi=0.5, Nw=1.e19).loss(), 1)[0] for i in np.arange(len(n))])
        Teq_low = np.array([fsolve(lambda x: wolfire(T=x, n=n[i], G0=0.5*1.7, phi=0.5, Nw=1.e19).loss(), 1)[0] for i in np.arange(len(n))])
        Teq_high = np.array([fsolve(lambda x: wolfire(T=x, n=n[i], G0=2.*1.7, phi=0.5, Nw=1.e19).loss(), 1)[0] for i in np.arange(len(n))])

        heat =  wolfire(T=Teq,n=n, G0=1.7, phi=0.5, Nw=1.e19).heat() / n
        heatXR =  wolfire(T=Teq,n=n, G0=1.7, phi=0.5, Nw=1.e19).heatXR() / n 
        cool_CII95 =  wolfire(T=Teq,n=n, G0=1.7, phi=0.5, Nw=1.e19).cool_CII95() * n
        cool_Ly =  wolfire(T=Teq,n=n, G0=1.7, phi=0.5, Nw=1.e19).cool_Ly() * n
        cool_rec03 =  wolfire(T=Teq,n=n, G0=1.7, phi=0.5, Nw=1.e19).cool_rec03() * n
        cool_OI =  wolfire(T=Teq,n=n, G0=1.7, phi=0.5, Nw=1.e19).cool_OI() * n

        stop

        fig = plt.figure(figsize=(12, 8))
        ax = fig.add_subplot(111)
        ax.set_yscale('log')
        ax.set_xscale('log')
        ax.set_xlim([0.01,1000])
        ax.set_ylim([1.e1,1.e5])
        ax.plot(n,n*Teq_low, "--k", label=r"G$_0$=0.87", linewidth=2.)
        ax.plot(n,n*Teq, color="k", label=r"G$_0$=1.7", linewidth=2.)
        ax.plot(n,n*Teq_high, "-.k", label=r"G$_0$=3.4", linewidth=2.)
        ax.set_ylabel(r'$P/k_B$ (K.cm$^{-3}$)',  fontsize = 16)
        ax.set_xlabel(r'$n$ (cm$^{-3}$)', fontsize = 16)
        plt.legend(loc = 2, numpoints = 1)
        leg = plt.gca().get_legend()
        ltext  = leg.get_texts()
        plt.setp(ltext, fontsize = 'small')        
        plt.savefig('wolfire_solar.png', format='png', bbox_inches='tight', pad_inches=0.02)
        


        
    

