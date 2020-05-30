# This file was automatically generated by SWIG (http://www.swig.org).
# Version 4.0.1
#
# Do not make changes to this file unless you know what you are doing--modify
# the SWIG interface file instead.

from sys import version_info as _swig_python_version_info
if _swig_python_version_info < (2, 7, 0):
    raise RuntimeError("Python 2.7 or later required")

# Import the low-level C/C++ module
if __package__ or "." in __name__:
    from . import _itkKernelFunctionBasePython
else:
    import _itkKernelFunctionBasePython

try:
    import builtins as __builtin__
except ImportError:
    import __builtin__

_swig_new_instance_method = _itkKernelFunctionBasePython.SWIG_PyInstanceMethod_New
_swig_new_static_method = _itkKernelFunctionBasePython.SWIG_PyStaticMethod_New

def _swig_repr(self):
    try:
        strthis = "proxy of " + self.this.__repr__()
    except __builtin__.Exception:
        strthis = ""
    return "<%s.%s; %s >" % (self.__class__.__module__, self.__class__.__name__, strthis,)


def _swig_setattr_nondynamic_instance_variable(set):
    def set_instance_attr(self, name, value):
        if name == "thisown":
            self.this.own(value)
        elif name == "this":
            set(self, name, value)
        elif hasattr(self, name) and isinstance(getattr(type(self), name), property):
            set(self, name, value)
        else:
            raise AttributeError("You cannot add instance attributes to %s" % self)
    return set_instance_attr


def _swig_setattr_nondynamic_class_variable(set):
    def set_class_attr(cls, name, value):
        if hasattr(cls, name) and not isinstance(getattr(cls, name), property):
            set(cls, name, value)
        else:
            raise AttributeError("You cannot add class attributes to %s" % cls)
    return set_class_attr


def _swig_add_metaclass(metaclass):
    """Class decorator for adding a metaclass to a SWIG wrapped class - a slimmed down version of six.add_metaclass"""
    def wrapper(cls):
        return metaclass(cls.__name__, cls.__bases__, cls.__dict__.copy())
    return wrapper


class _SwigNonDynamicMeta(type):
    """Meta class to enforce nondynamic attributes (no new attributes) for a class"""
    __setattr__ = _swig_setattr_nondynamic_class_variable(type.__setattr__)


import itk.itkFunctionBasePython
import itk.itkRGBPixelPython
import itk.itkFixedArrayPython
import itk.pyBasePython
import itk.itkCovariantVectorPython
import itk.itkVectorPython
import itk.vnl_vector_refPython
import itk.stdcomplexPython
import itk.vnl_vectorPython
import itk.vnl_matrixPython
import itk.itkArrayPython
import itk.itkImagePython
import itk.itkSymmetricSecondRankTensorPython
import itk.itkMatrixPython
import itk.vnl_matrix_fixedPython
import itk.itkPointPython
import itk.itkIndexPython
import itk.itkOffsetPython
import itk.itkSizePython
import itk.itkImageRegionPython
import itk.ITKCommonBasePython
import itk.itkRGBAPixelPython
import itk.itkContinuousIndexPython
class itkKernelFunctionBaseD(itk.itkFunctionBasePython.itkFunctionBaseDD):
    r"""


    Kernel used for density estimation and nonparametric regression.

    This class encapsulates the smoothing kernel used for statistical
    density estimation and nonparametric regression. The basic idea of the
    kernel approach is to weight observations by a smooth function (the
    kernel) to created a smoothed approximation.

    Reference: Silverman, B. W. (1986) Density Estimation. London: Chapman
    and Hall.

    C++ includes: itkKernelFunctionBase.h 
    """

    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined - class is abstract")
    __repr__ = _swig_repr
    TRealValueTypeIsFloatingPointCheck = _itkKernelFunctionBasePython.itkKernelFunctionBaseD_TRealValueTypeIsFloatingPointCheck
    
    __swig_destroy__ = _itkKernelFunctionBasePython.delete_itkKernelFunctionBaseD
    cast = _swig_new_static_method(_itkKernelFunctionBasePython.itkKernelFunctionBaseD_cast)

# Register itkKernelFunctionBaseD in _itkKernelFunctionBasePython:
_itkKernelFunctionBasePython.itkKernelFunctionBaseD_swigregister(itkKernelFunctionBaseD)
itkKernelFunctionBaseD_cast = _itkKernelFunctionBasePython.itkKernelFunctionBaseD_cast

class itkKernelFunctionBaseF(itk.itkFunctionBasePython.itkFunctionBaseFF):
    r"""


    Kernel used for density estimation and nonparametric regression.

    This class encapsulates the smoothing kernel used for statistical
    density estimation and nonparametric regression. The basic idea of the
    kernel approach is to weight observations by a smooth function (the
    kernel) to created a smoothed approximation.

    Reference: Silverman, B. W. (1986) Density Estimation. London: Chapman
    and Hall.

    C++ includes: itkKernelFunctionBase.h 
    """

    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined - class is abstract")
    __repr__ = _swig_repr
    TRealValueTypeIsFloatingPointCheck = _itkKernelFunctionBasePython.itkKernelFunctionBaseF_TRealValueTypeIsFloatingPointCheck
    
    __swig_destroy__ = _itkKernelFunctionBasePython.delete_itkKernelFunctionBaseF
    cast = _swig_new_static_method(_itkKernelFunctionBasePython.itkKernelFunctionBaseF_cast)

# Register itkKernelFunctionBaseF in _itkKernelFunctionBasePython:
_itkKernelFunctionBasePython.itkKernelFunctionBaseF_swigregister(itkKernelFunctionBaseF)
itkKernelFunctionBaseF_cast = _itkKernelFunctionBasePython.itkKernelFunctionBaseF_cast



