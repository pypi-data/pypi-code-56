import numpy as np
from ._CFunctions import _Cgcpm
import DateTimeTools as TT

def GCPM(x,y,z,Date,ut,Kp=1.0,Verbose=False):
	'''
	Calculates the Global Core Plasma Model at some given position(s)
	and time(s).
	
	Inputs
	======
	x : float
		scalar or array of x_SM (Solar Magnetic coordinates) component 
		of the position, where units are in R_E.
	y : float
		scalar or array of y_SM 
	z : float
		scalar or array of z_SM
	Date : int
		Date(s) in format yyyymmdd
	ut : float
		Time(s) in hours from beginning of day where 
		ut = hh + mm/60.0 + ss/3600.0
	Kp : float
		Kp index (or indices)
	Verbose : bool
		If True, model calculation progress will be displayed
		
	Returns
	=======
	ne : float32
		Array of electron densities in 1/cm^3
	nH : float32
		Array of proton densities in 1/cm^3
	nHe : float32
		Array of helium ion densities in 1/cm^3
	nO : float 32
		Array of Oxygen densities in 1/cm^3
	'''

	#reformat the positions
	_x = np.array([x]).flatten().astype('float32')
	_y = np.array([y]).flatten().astype('float32')
	_z = np.array([z]).flatten().astype('float32')
	_n = np.int32(_x.size)


	#sort out the dates
	dates = np.zeros(_n,dtype='int32') + Date
	_years = np.int32(dates//10000)
	_dayno = np.int32(TT.DayNo(dates))
	
	#times
	_ut = np.zeros(_n,dtype='float32') + ut
	
	#Kp indices
	_kp = np.zeros(_n,dtype='float32') + Kp
	
	#Verbose flag
	_verb = np.int32(Verbose)
	
	#output arrays
	ne = np.zeros(_n,dtype='float32')
	nH = np.zeros(_n,dtype='float32')
	nHe = np.zeros(_n,dtype='float32')
	nO = np.zeros(_n,dtype='float32')

	
	#call the C wrapper
	_Cgcpm(_x,_y,_z,_years,_dayno,_ut,_kp,_n,ne,nH,nHe,nO,_verb)
	
	return ne,nH,nHe,nO
	
