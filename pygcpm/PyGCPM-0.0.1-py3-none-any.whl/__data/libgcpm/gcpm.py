import numpy as np
import ctypes as ct
import DateTimeTools as TT

c_str = ct.c_char_p
c_bool = ct.c_bool
c_int = ct.c_int
c_float = ct.c_float
c_double = ct.c_double
c_int_ptr = np.ctypeslib.ndpointer(ct.c_int,flags="C_CONTIGUOUS")
c_float_ptr = np.ctypeslib.ndpointer(ct.c_float,flags="C_CONTIGUOUS")
c_double_ptr = np.ctypeslib.ndpointer(ct.c_double,flags="C_CONTIGUOUS")

lib = ct.CDLL('./libgcpm.so')
_Fgcpm = lib.gcpm_v24_
_Fgcpm.restype = None
_Fgcpm.argtypes = [	c_int_ptr,
					c_float_ptr,
					c_float_ptr,
					c_float_ptr,
					c_float_ptr,
					c_float_ptr]

_Csetpath = lib.setLibPath
_Csetpath.restype = None
_Csetpath.argtypes = [c_str]

def gcpm(x,y,z,Date,ut,kp=1.0):
	
	#set the path
	path = '/home/matt/gcpm/src/'
	c_path = ct.c_char_p(path.encode('utf-8'))
	_Csetpath(c_path)
	
	#convert date and time
	doy = TT.DayNo(Date)
	h,m,s = TT.DectoHHMM(ut,Split=True,ss=True)

	itime = np.array([(Date // 10000)*1000 + doy,1000*(h*3600 + m*60 + s)],dtype='int32')
	r = np.array([np.sqrt(x**2 + y**2 + z**2)],dtype='float32')
	rho = np.sqrt(x**2 + y**2)
	amlt = ((np.array([np.arctan2(-y,-x)*12/np.pi],dtype='float32') + 24.0) % 24.0)
	alatr = np.array([np.arcsin(z/rho)],dtype='float32')
	akp = np.array([kp],dtype='float32')
	
	out = np.zeros(4,dtype='float32')
	_Fgcpm(itime,r,amlt,alatr,akp,out)

	return out
