import numpy as np
import os
import ctypes as ct

#some ctypes
c_str = ct.c_char_p
c_bool = ct.c_bool
c_int = ct.c_int
c_float = ct.c_float
c_double = ct.c_double
c_int_ptr = np.ctypeslib.ndpointer(ct.c_int,flags="C_CONTIGUOUS")
c_float_ptr = np.ctypeslib.ndpointer(ct.c_float,flags="C_CONTIGUOUS")
c_double_ptr = np.ctypeslib.ndpointer(ct.c_double,flags="C_CONTIGUOUS")

#get the path of the library
libpath = os.path.dirname(__file__)+"/__data/libgcpm/"

#let's try and import the module
try:
	libgcpm = ct.CDLL(libpath+"libgcpm.so")
except:
	print('importing libgcpm.so failed, attempting to recompile')
	path = os.path.dirname(__file__)
	if '/usr/local/' in path:
		sudo = 'sudo '
	else:
		sudo = ''

	CWD = os.getcwd()
	os.chdir(libpath)
	os.system(sudo+'make clean')
	os.system(sudo+'make')
	os.chdir(CWD)	
	libgcpm = ct.CDLL(libpath+"libgcpm.so")



#define the functions and their arguments
#This is the model wrapper function
_Cgcpm = libgcpm.GCPM
_Cgcpm.restype = None
_Cgcpm.argtypes = [	c_float_ptr,	#x
					c_float_ptr,	#y
					c_float_ptr,	#z
					c_int_ptr,		#year
					c_int_ptr,		#day number
					c_float_ptr,	#ut in hours
					c_float_ptr,	#kp index
					c_int,			#number of positions to calculate density
					c_float_ptr,	#electron density
					c_float_ptr,	#proton density
					c_float_ptr,	#helium density
					c_float_ptr,	#oxygen density
					c_int]			#verbosity flag

#This will set the path of the model so it can find the data files
_Csetpath = libgcpm.setLibPath
_Csetpath.restype = None
_Csetpath.argtypes = [c_str]

_Csetpath(c_str(libpath.encode("utf-8")))
