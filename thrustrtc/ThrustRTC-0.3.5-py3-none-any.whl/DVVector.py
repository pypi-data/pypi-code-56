from .Native import ffi, native
import numpy as np
from .DeviceViewable import DeviceViewable
from .utils import *
import ctypes

class DVVectorLike(DeviceViewable):
	def name_elem_cls(self):
		return ffi.string(native.n_dvvectorlike_name_elem_cls(self.m_cptr)).decode('utf-8')

	def size(self):
		return native.n_dvvectorlike_size(self.m_cptr)

	def range(self, begin = 0, end = -1):
		return DVRange(self, begin, end)

class DVRange(DVVectorLike):
	def __init__(self, src, begin = 0, end = -1):
		self.m_src = src
		self.m_cptr = native.n_dvrange_create(src.m_cptr, ctypes.c_ulonglong(begin).value, ctypes.c_ulonglong(end).value)

class DVVector(DVVectorLike):
	def __init__(self, cptr):
		self.m_cptr = cptr

	def to_host(self, begin = 0, end = -1):
		elem_cls = self.name_elem_cls()
		if elem_cls=='int8_t':
			nptype = np.int8
		elif elem_cls=='uint8_t':
			nptype = np.uint8
		elif elem_cls=='int16_t':
			nptype = np.int16
		elif elem_cls=='uint16_t':
			nptype = np.uint16
		elif elem_cls=='int32_t':
			nptype = np.int32
		elif elem_cls=='uint32_t':
			nptype = np.uint32
		elif elem_cls=='int64_t':
			nptype = np.int64
		elif elem_cls=='uint64_t':
			nptype = np.uint64
		elif elem_cls=='float':
			nptype = np.float32
		elif elem_cls=='double':
			nptype = np.float64
		elif elem_cls=='bool':
			nptype = np.bool
		if end == -1:
			end = self.size()
		ret = np.empty(end - begin, dtype=nptype)
		native.n_dvvector_to_host(self.m_cptr, ffi.cast("void *", ret.__array_interface__['data'][0]), begin, end)
		return ret

def device_vector(elem_cls, size, ptr_host_data=None):
	ffiptr = ffi.NULL
	if ptr_host_data!=None:
		ffiptr = ffi.cast("void *", ptr_host_data)
	return DVVector(native.n_dvvector_create(elem_cls.encode('utf-8'), size, ffiptr))

def device_vector_from_numpy(nparr):
	if nparr.dtype == np.int8:
		elem_cls = 'int8_t'
	elif nparr.dtype == np.uint8:
		elem_cls = 'uint8_t'
	elif nparr.dtype == np.int16:
		elem_cls = 'int16_t'
	elif nparr.dtype == np.uint16:
		elem_cls = 'uint16_t'
	elif nparr.dtype == np.int32:
		elem_cls = 'int32_t'
	elif nparr.dtype == np.uint32:
		elem_cls = 'uint32_t'		
	elif nparr.dtype == np.int64:
		elem_cls = 'int64_t'
	elif nparr.dtype == np.uint64:
		elem_cls = 'uint64_t'	
	elif nparr.dtype == np.int64:
		elem_cls = 'int64_t'
	elif nparr.dtype == np.uint64:
		elem_cls = 'uint64_t'	
	elif nparr.dtype == np.float32:
		elem_cls = 'float'
	elif nparr.dtype == np.float64:
		elem_cls = 'double'
	elif nparr.dtype == np.bool:
		elem_cls = 'bool'
	size = len(nparr)
	ptr_host_data = nparr.__array_interface__['data'][0]
	return device_vector(elem_cls, size, ptr_host_data)

def device_vector_from_list(lst, elem_cls):
	if elem_cls=='int8_t':
		nptype = np.int8
	elif elem_cls=='uint8_t':
		nptype = np.uint8
	elif elem_cls=='int16_t':
		nptype = np.int16
	elif elem_cls=='uint16_t':
		nptype = np.uint16
	elif elem_cls=='int32_t':
		nptype = np.int32
	elif elem_cls=='uint32_t':
		nptype = np.uint32
	elif elem_cls=='int64_t':
		nptype = np.int64
	elif elem_cls=='uint64_t':
		nptype = np.uint64
	elif elem_cls=='float':
		nptype = np.float32
	elif elem_cls=='double':
		nptype = np.float64
	elif elem_cls=='bool':
		nptype = np.bool
	nparr = np.array(lst, dtype=nptype)
	size = len(lst)
	ptr_host_data = nparr.__array_interface__['data'][0]
	return device_vector(elem_cls, size, ptr_host_data)

def device_vector_from_dvs(lst_dv):
	dvarr = ObjArray(lst_dv)
	return DVVector(native.n_dvvector_from_dvs(dvarr.m_cptr))

class DVNumbaVector(DVVectorLike):
	def __init__(self, nbarr):
		self.nbarr = nbarr
		if nbarr.dtype == np.int8:
			elem_cls = 'int8_t'
		elif nbarr.dtype == np.uint8:
			elem_cls = 'uint8_t'
		elif nbarr.dtype == np.int16:
			elem_cls = 'int16_t'
		elif nbarr.dtype == np.uint16:
			elem_cls = 'uint16_t'
		elif nbarr.dtype == np.int32:
			elem_cls = 'int32_t'
		elif nbarr.dtype == np.uint32:
			elem_cls = 'uint32_t'		
		elif nbarr.dtype == np.int64:
			elem_cls = 'int64_t'
		elif nbarr.dtype == np.uint64:
			elem_cls = 'uint64_t'	
		elif nbarr.dtype == np.int64:
			elem_cls = 'int64_t'
		elif nbarr.dtype == np.uint64:
			elem_cls = 'uint64_t'	
		elif nbarr.dtype == np.float32:
			elem_cls = 'float'
		elif nbarr.dtype == np.float64:
			elem_cls = 'double'
		elif nbarr.dtype == np.bool:
			elem_cls = 'bool'
		size = nbarr.size
		ptr_device_data = nbarr.device_ctypes_pointer.value
		self.m_cptr = native.n_dvvectoradaptor_create(elem_cls.encode('utf-8'), size, ffi.cast("void *", ptr_device_data))

