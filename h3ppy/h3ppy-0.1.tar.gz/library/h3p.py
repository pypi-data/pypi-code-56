import os
import numpy as np
from functools import partial
import warnings



import matplotlib.pyplot as plt


class h3p_tools : 

    def __init__(self, line_list_file = '', **kwargs):
    
        self.parse_kwargs(kwargs)
    
        self.dtype = np.dtype('double')
        self.dtype = 'double'

#        self.wavelength = wave
        if (line_list_file == '') :
#            self.line_list_file = os.path.join(os.path(h3ppy.__file__), '../h3p_line_data/h3p_line_list_neale_1996_subset.txt')
            self.line_list_file = '../h3p_line_data/h3p_line_list_neale_1996_subset.txt'
        else : self.line_list_file = line_list_file
        
        
#        self.wl_shift = 0

        self.density = 1
        
        self.k = 1.380649e-23
        self.c = 299792458.0
        self.h = 6.62607015e-34

        self.bkg_consts    = self.get_iterable(0.0)
        self.offset_consts = self.get_iterable(0.0)
        self.sigma_consts  = self.get_iterable(0.0)
        self.nsigma        = 1
        self.noffset       = 1
        self.nbackground   = 1


        self.temperature = 500
        self.wavelength = np.array([-1])


        # Column density 
        self.column_density = 1        

        self._last_temperature = 0


        # Read the spectral information
        self.read_line_list()
        
        # This is the number of FWHM's before and after the line centre we'll
        # evaluate the intensity for. Purely for computational speedos. 
        self.sigma_limit = 2
        
        # When to stop iterating the fitting loop. This is defined as the ratio between
        # the first parameter delta over the current. 
        self.convergence_limit = 1e-5
              
        # The default set of variables
        self.vars = {}
        self.vars['temperature'] = 1000
        self.vars['density']     = 1.0e15
        self.vars['sigma']       = self.get_iterable(0.0)
        self.vars['offset']      = self.get_iterable(0.0)
        self.vars['background']  = self.get_iterable(0.0)
        warnings.warn('Wooooo')

    def read_line_list(self) : 
        # Read the line data into a structured array
        types = {'names' : ( 'Ju', 'wu', 'wl', 'EA', 'gw' ), 'formats' : ('f', 'f', 'f', 'f', 'f') }
        self.line_data = np.loadtxt(self.line_list_file, skiprows=1, dtype = types)


    # Evaluate an arbitraary polynomial function
    def poly_fn(self, consts) :

        ret = np.zeros(len(self.wavelength))
        for k, const in np.ndenumerate(consts) : 
            ret += const * np.power(self.wavelength, k[0])
        return ret

    # Calculate the derivative of an arbitrary polynomial function 
    def d_poly_fn(self, consts) : 
        if (type(consts) is float) : consts = [consts]
        return [np.power(consts[i] * float(i) * self.wavelength, i - 1) for i in range(len(consts))]


    def calculate_line_intensities(self) : 
        """
                  g*(2J'+1)*hcw*exp(-hcw'/kT)*A(if)
            E(w)= --------------------------------
                                 4Pi*Q

        """
        # Don't recalculate if we've just done it
        if (self._last_temperature == self.temperature) : 
            return self.line_intensity                

        Q = self.Q()

        self.line_intensity = np.zeros(len(self.line_data['gw']))
        for i in range(len(self.line_data['gw'])) : 
        
            if (1e4/self.line_data['wl'][i] > 0.9 * np.min(self.wavelength) and 1e4/self.line_data['wl'][i] < 1.1 * np.max(self.wavelength)) :

                exponent   = ( -1.0 * self.line_data['wu'][i] *  self.h *  self.c * 100 ) / ( self.k * self.temperature)

                intensity  = self.line_data['gw'][i] * (2.0 * self.line_data['Ju'][i] + 1) 
                intensity *=  self.h *  self.c * 100 * self.line_data['wl'][i] 
                intensity *= np.exp(exponent) * self.line_data['EA'][i]  / ( Q * 4.0 * np.pi )

                self.line_intensity[i] = intensity
    
        self._last_temperature = self.temperature
    
        return self.line_intensity                
        
    def model(self, **kwargs) :

        self.parse_kwargs(kwargs)

        line_intensity = self.calculate_line_intensities()

        self.background = self.poly_fn(self.bkg_consts)
        
        return self.render_spectrum(line_intensity) * self.density + self.background

    def render_spectrum(self, line_intensity, extra_fn_multiply = '', process_fn = '', **kwargs) : 
    
        self.parse_kwargs(kwargs)

        spectrum   = np.zeros(len(self.wavelength))

        self.sigma      = self.poly_fn(self.sigma_consts)
        self.offset     = self.poly_fn(self.offset_consts)
        self.background = self.poly_fn(self.bkg_consts)

        #print((np.max(self.sigma) * self.sigma_limit))

        relevant_range = np.max(self.sigma) * self.sigma_limit
        
        # Iterate over the H3+ spectral lines        
        for k in np.arange(len(self.line_data['wl'])) : 

            # Only calculate over the wavelength range appropriate for this line
            relevant_waves = np.argwhere(np.abs(self.wavelength - 1e4/self.line_data['wl'][k]) < relevant_range)

            for i in relevant_waves : 
                
                # Evaluate the spectral function for this line and this wavelength
                exponent     = -1.0 * np.power(self.wavelength[i] - ( 1e4/self.line_data['wl'][k] + self.offset[i]), 2) / (2.0 * np.power(self.sigma[i], 2))
                self.intensity_ik  = line_intensity[k] / ( self.sigma[i] * np.sqrt(2 * np.pi) ) * np.exp(exponent)

                # We can process the spectrum by adding additional terms, 
                # mainly for the derivaties of the spectral function.    
                if (process_fn == '') : spectrum[i] += self.intensity_ik
                else : spectrum[i] = getattr(self, process_fn)(i, k)
    
        return spectrum
        
    def render_spectrum_i(self, i) : 
        self.i = i
        relevant_range      = np.max(self.sigma) * self.sigma_limit
        exclude_transitions = np.argwhere(np.abs(self.wavelength[i] - 1e4/self.line_data['wl']) > relevant_range)
        line_intensities    = np.vectorize(self.render_spectrum_ik, excluded=exclude_waves)
        return np.sum(line_intensities)
        
    def render_spectrum_ik(self, k) : 
        i = self.i
        # Evaluate the spectral function for this line and this wavelength
        exponent     = -1.0 * np.power(self.wavelength[i] - ( 1e4/self.line_data['wl'][k] + self.offset[i]), 2) / (2.0 * np.power(self.sigma[i], 2))
        self.intensity_ik  = line_intensity[k] / ( self.sigma[i] * np.sqrt(2 * np.pi) ) * np.exp(exponent)

        return intensity_ik

        # We can process the spectrum by adding additional terms, 
        # mainly for the derivaties of the spectral function.    
        if (process_fn == '') : spectrum[i] += self.intensity_ik
        else : spectrum[i] += getattr(self, process_fn)(i, k)
        

    def fit_fn(self, wavelength, temperature) : 
        self.temperature = temperature
#        self.density = density / 1e15
        self.wavelength = np.array(wavelength)        
        return self.model()

    def fit(self, wave, spectrum) : 
        vars, pcov = curve_fit(self.fit_fn, wave, spectrum, bounds=([300, 1500]))
        print(vars)
        return self.fit_fn(wave, *vars)

    def Q_constants(self) : 
        """

            The partition functions from Miller et al. (2013)
            This is valid for temperatures 100 < T < 1800.
        
        """
        constants = [  -1.11391, 
                       +0.0581076, 
                       +0.000302967,
                       -0.000000283724,
                       +0.000000000231119,
                       -0.0000000000000715895,
                       +0.0000000000000000100150]

        return np.array(constants, dtype = self.dtype)

    def Q(self) :
        """
                     6              ^n
            log Q = SUM (a(n)(log T)
                    n=0
        """    
        pconst = self.Q_constants()    
    
        Q = 0.0
        for i, const in np.ndenumerate(pconst) : 
            Q += const * np.power(self.temperature, np.double(i))
            
        return Q;

    
    # The temperature derivative of the partivtion function.  
    def dQdT(self) : 

        vardQdT = 0.0
        for i, const in np.ndenumerate(self.Q_constants()) : 
            vardQdT += np.float(i[0]) * const * np.power(self.temperature, i[0] - 1)
        return vardQdT

    # The tempoerature derivative of the spectral function
    def dIdT(self) : 

        line_intensity = self.calculate_line_intensities()
        dIidT          = np.zeros(len(self.line_data['wl']))

        const1 =  self.h *  self.c * 100 / ( np.power(self.temperature, 2) *  self.k )
        Q      = self.Q()
        dQdT   = self.dQdT()

        # Iterate over the H3+ spectral lines
        for k in np.arange(len(self.line_data['wl'])) : 
#            print(k, len(self.line_data['wl']), len(self.line_data['wu']))
            dIidT[k]  = line_intensity[k] * const1 * self.line_data['wu'][k]
            dIidT[k] -= line_intensity[k] * dQdT     / Q

        return self.render_spectrum(dIidT) * self.density

    def dIdT_process(self, i, k) : 
    
        return self.intensity_ik * self.dIidT[k]
        

#        return self.render_spectrum(dIidT)


    # The wavelength polynomial constants derivative of the spectral function I
    def dIdo(self, index) :
    
        line_intensity = self.calculate_line_intensities()

        self.offset_index = index 
        return self.render_spectrum(line_intensity, process_fn = 'dIdo_process') * self.density

    # Alter the spectral function for dIdo()
    def dIdo_process(self, i, k) : 

        numerator_deriv = 2.0 * ( self.wavelength[i] - (1e4/self.line_data['wl'][k] + self.offset[i] ))
        dIdc            = np.power(self.wavelength[i], self.offset_index)

        return self.intensity_ik * numerator_deriv / (2.0 * np.power(self.sigma[i], 2)) * dIdc 
        
    # The line width derivative of the spectral function I 
    def dIds(self, index) : 
        line_intensity = self.calculate_line_intensities()

        self.sigma_index = index 
        return  self.render_spectrum(line_intensity, process_fn = 'dIds_process') * self.density
    
    # Alter the spectral function for dIds()
    def dIds_process(self, i, k) : 

        # The exponent in the spectral function
        exponent_numerator  = -1.0 * np.power(self.wavelength[i] - ( 1e4/self.line_data['wl'][k] + self.offset[i]), 2) 

        # The derivative of the exponent denominator
        dIds = -2.0 * exponent_numerator / (2.0 * np.power(self.sigma[i], 3)) 

        # The derivative of the sigma function polynmomial functions
        dsdc = np.power(self.wavelength[i], self.sigma_index) 

        return ( self.intensity_ik * dIds - 1.0 * self.intensity_ik / self.sigma[i]) * dsdc
    
    # The 
    def dIdb(self, index) : 
        return np.power(self.wavelength, index)

    def dIdN(self) :
        line_intensity = self.calculate_line_intensities()        
        return self.render_spectrum(line_intensity)

    def setno(self, temperature = -1.0, density = -1.0, sigma = -1.0, offset = 0.0, background = 0.0) : 
        if (temperature != -1) : self.temperature = temperature
        if (density != -1) : self.density = density
        if (sigma != -1) : self.sigma = np.array(sigma)
        self.offset = np.array(offset)
        self.background  = np.array(background)

    def set(self, **kwargs) : 
        self.parse_kwargs(kwargs) 
 
 
    def parse_kwargs(self, kwargs) :
        for key, value in kwargs.items() :
            if (key == 'wavelength') : self.wavelength = np.array(value)
            elif (key == 'data') : self.data = value
            elif (key == 'temperature') : self.temperature = float(value)
            elif (key == 'density') : self.density = float(value)
            elif (key == 'sigma') : self.sigma_consts = self.get_iterable(value)
            elif (key == 'offset') : self.offset_consts = self.get_iterable(value)
            elif (key == 'background') : self.bkg_consts = self.get_iterable(value)
            elif (key == 'nsigma') : self.nsigma = value
            elif (key == 'fwhm') : self.nsigma = value / 2.0 * np.sqrt(2.0 * np.alog(2.0))
            elif (key == 'noffset') : self.noffset = value
            elif (key == 'nbackground') : self.nbackground = value
            else : print('Unknown combo: ', key, value)

    def get_iterable(self, x):
        if (type(x) is float or int) : return np.array([float(x)])
        else : return np.array(float(x))

#        if isinstance(x, Iterable): return np.array(x)
#        else: 

            
#            elif (key == 'data') : self.vars['data'] = np.array(value)
#            elif (key in self.defined_vars) : 
#                self.vars[key] = value
#            else : print('Unrecognized variable: ' + key) 

    def fit2(self, params_to_fit = '', **kwargs) : 

        self.parse_kwargs(kwargs)

        function_map = {'temperature' : 'dIdT()', 'density' : 'dIdN()', 'offset-n' : 'dIdo(n)', 'sigma-n' : 'dIds(n)', 'background-n' : 'dIdb(n)'}

        # The default set of params to fit
        #if (params_to_fit == '') :
        #    self.params_to_fit = ['temperature', 'density', 'sigma-0', 'offset-0', 'background-0']
        #else self.params_to_fit = params_to_fit

        params_to_fit = ['temperature', 'density', 'sigma-0', 'offset-0', 'background-0']


        self.noffset      = 1
#        self.offset_consts = np.array([0, 0])
        self.nsigma      = 1
        self.nbackground = 1

        niter = 8

        self.convergence_arrays = []
        
        
        
        iternbr = 0
        for i in range(niter) : 

            # The difference between the observation and the data
            diff = self.data - self.model()

            elements = {}
            for k, param in enumerate(params_to_fit) : 
                if '-' in param : 
                    p1, p2 = param.split('-')
                    fn = function_map[param.replace(p2, 'n')].replace('n', p2 )
                else : fn = function_map[param]
                elements[param] = eval('self.' + fn)     
        
            # Generate the Z and ABC matricies
            Z   = np.zeros([len(elements), len(elements)])
            ABC = np.zeros([len(elements), len(elements), len(elements)])
            for x, xparam in enumerate(params_to_fit) : 
                for y, yparam in enumerate(params_to_fit) : 
                    Z[y][x] = np.sum(elements[xparam] * elements[yparam])
                    for p, pparam in enumerate(params_to_fit) : 
                        if (y == p) : diffvar = diff
                        else : diffvar =  elements[yparam]
                        ABC[p][y][x] = np.sum(elements[xparam] * diffvar)

            diffs = []
            for p, param in enumerate(params_to_fit) : 
                diff = np.linalg.det(ABC[p]) / np.linalg.det(Z) 

               #if (np.isfinite(diff) == False) : print('Error: Fit cannot converge')

                diffs.append(diff)
        
                if (param == 'temperature') : 
                    self.temperature += diff
#                    fit[param] = self.temperature
                elif (param == 'density') : 
                    self.density += diff                
                for i in range(self.nsigma) : 
                    if (param == 'sigma-' + str(i)) :
                        self.sigma_consts[i] += diff
                for i in range(self.nbackground) : 
                    if (param == 'background-' + str(i)) :
                        self.bkg_consts[i] += diff
                for i in range(self.noffset) : 
                    if (param == 'offset-' + str(i)) :
                        self.offset_consts[i] += diff 
            #print(self.temperature)
                
                # Sanity check the retrieved variables 
                msg = ''
                if (np.isfinite(diff) == False) : '|D|/|Z| returned a NaN'
                if (self.temperature < 0) : msg = 'Temperature is less than zero'
                if (self.temperature > 5000) : msg = 'Temperature is larger than one might expect'
                if (self.density < 0) : msg = 'Density is less than zero'
                self.sigma = self.poly_fn(self.sigma_consts)
                if (np.mean(self.sigma) < 0) : msg = 'Line width is negative'
                if (msg != '') : 
                    print('Fit cannot converge: ' + msg)
                    return np.full(len(self.wavelength), -1)

            self.convergence_arrays.append(diffs)

            print(self.sigma_consts, self.temperature, self.density, self.offset_consts)


          
            
            converger = np.abs(np.min(diff / self.convergence_arrays[0]))
            print(converger)
            if (converger < self.convergence_limit) : break


        diff = self.data - self.model()
        mu = np.sqrt(np.sum(np.power(diff, 2)) / (len(self.data) - len(params_to_fit)))
        self.errors = {}
        for p, param in enumerate(params_to_fit) : 
            Zpp = np.delete(np.delete(Z, p, 0), p, 1)
            self.errors[param] = mu / np.sqrt(np.linalg.det(Z)  / np.linalg.det(Zpp) )
        
        
           
            # Calculate errors
#    if (p > 1) for (int i=0; i<p; i++) params_error[i] = mu/sqrt(det_Z/determinant(cofactor(Matrix.extract(0, p*p, 1), i, i)));
#    double mu = sqrt(total(pow(spectra-model, 2.0))/(n-p));


        {'value' : 0.0, 'error' : 0.0, 'unit' : ''}

        return self.model()

    def cofactor(self, x) : 
        m = np.linalg.det(x)
        c = np.zeros((len(x), len(x))) #[[i for i in range(3)] for j in range(3)]
        for i in len(x) :
            for j in len(x) :
                c[i][j] = (-1)*(i+j)*m
        return c.T
        
    def wavegen(self, wstart, wend, wnbr) : 
        res = (wend - wstart) / float(wnbr)
        return  np.arange(wstart, wend, res) 

    def total_emission(self, **kwargs) :    

        self.parse_kwargs(kwargs)
        
        if (self.temperature < 300) :
            coeffs = [-81.9599, 0.886768, -0.0264611, 0.000462693, -4.70108e-6, 2.84979e-8, 
                      -1.03090e-10, 2.13794e-13, -2.26029e-16, 8.66357e-20]
        if (self.temperature >= 300 and self.temperature < 800) : 
            coeffs = [-92.2048, 0.298920, 0.000962580, 1.82712e-6, -2.04420e-9, 1.24970e-12, -3.22212e-16]
        if (self.temperature >= 800 and self.temperature < 1800) : 
            coeffs = [-62.7016, 0.0526104, -7.22431e-5, 5.93118e-8, -2.83755e-11, 7.35415e-15, -8.01994e-19]
        if (self.temperature >= 1800 and self.temperature < 1800) : 
            coeffs = [-55.7672, 0.0162530, -7.68583e-6, 1.98412e-9, -2.68044e-13, 1.47026e-17]

        logE = 0.0
        for k, coeff in enumerate(coeffs) : 
            logE += coeff * np.power(self.temperature, k)

        return np.power(10, logE)        

    def get_parameters(self, verbose = True) : 
        nl = "\n"
        print(self.errors)
        txt  = '# h3ppy spectrum parameters:' + nl
        txt += '# Temperature    = {ds:0.1f} ± {ed:0.1f} [K]'.format(ds = self.temperature, ed=self.errors['temperature']) + nl
        txt += '# Column density = {ds:0.2E} ± {ed:0.2E} [m-2]'.format(ds = self.density, ed=self.errors['density']) + nl
#        txt += '# Sigma          = {ds:0.2f} ± {ed:0.2f} [μm]'.format(ds = self.sigma_consts[0], ed=self.errors['sigma-0']) + nl
        if (verbose == True) : print(txt)
#        print('Z')
#        print(Z)
#        print('ABC')        
#        print(ABC[0])
#        print('ABC')        
#        print(diffs)
        
#        print(elements)
        
#        for (int i=0; i<7; i++) {
#        logQ += a[i]*pow(log10(temperature), i);
#            dgx  += a[i]*i*pow(log10(temperature), i-1)/(temperature*log(10));
#        }
#        return log(10)*pow(10, logQ)*dgx;
#    }



        params = {}


#print(wave)
if False : 
    h3p = h3p_tools()

    wave = h3p.wavegen(3.94, 4.0, 500)
    h3p.set(wavelength = wave, temperature = 900, sigma=0.0005, offset=0, density = 1e15)

    m = h3p.model()

    ynoise = 0.05 * np.random.normal(size=m.size) * np.max(m)
    wave2 = wave

    m2 = m + ynoise
    h3p.set(wavelength = wave2) #, temperature = 1000, sigma=0.0006, offset=0, density = 5e15)
    #h3p.set(wavelength = wave, sigma=0.0011)

    ret = h3p.fit2(data = m2)
    h3p.get_parameters()
    #exit()
    #print(ret)

    #a = h3p.fit_fn(3.97, 1000, 1e15)

    #exit()
    #print(m)
    plt.plot(wave, m)
    plt.plot(wave, ret)
    plt.plot(wave, m2)
    #plt.plot(h3p.line_intensity)
    #plt.plot(wave, color='green')
    plt.xlabel('Wavelength (${\mu}m$)')
    plt.ylabel('Intensity ($Wm^{-2}sr^{-1}{\mu}m^{-1}$)')
    plt.show()

