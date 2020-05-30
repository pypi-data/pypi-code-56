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
    from . import _itkBSplineBaseTransformPython
else:
    import _itkBSplineBaseTransformPython

try:
    import builtins as __builtin__
except ImportError:
    import __builtin__

_swig_new_instance_method = _itkBSplineBaseTransformPython.SWIG_PyInstanceMethod_New
_swig_new_static_method = _itkBSplineBaseTransformPython.SWIG_PyStaticMethod_New

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


import itk.itkArrayPython
import itk.vnl_vectorPython
import itk.stdcomplexPython
import itk.pyBasePython
import itk.vnl_matrixPython
import itk.itkArray2DPython
import itk.itkOptimizerParametersPython
import itk.ITKCommonBasePython
import itk.itkTransformBasePython
import itk.itkSymmetricSecondRankTensorPython
import itk.itkFixedArrayPython
import itk.itkMatrixPython
import itk.itkCovariantVectorPython
import itk.itkVectorPython
import itk.vnl_vector_refPython
import itk.vnl_matrix_fixedPython
import itk.itkPointPython
import itk.itkDiffusionTensor3DPython
import itk.itkVariableLengthVectorPython
import itk.itkBSplineInterpolationWeightFunctionPython
import itk.itkFunctionBasePython
import itk.itkRGBPixelPython
import itk.itkImagePython
import itk.itkIndexPython
import itk.itkOffsetPython
import itk.itkSizePython
import itk.itkImageRegionPython
import itk.itkRGBAPixelPython
import itk.itkContinuousIndexPython
class itkBSplineBaseTransformD23(itk.itkTransformBasePython.itkTransformD22):
    r"""


    A base class with common elements of BSplineTransform and
    BSplineDeformableTransform.

    C++ includes: itkBSplineBaseTransform.h 
    """

    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined - class is abstract")
    __repr__ = _swig_repr
    Clone = _swig_new_instance_method(_itkBSplineBaseTransformPython.itkBSplineBaseTransformD23_Clone)
    SetIdentity = _swig_new_instance_method(_itkBSplineBaseTransformPython.itkBSplineBaseTransformD23_SetIdentity)
    SetCoefficientImages = _swig_new_instance_method(_itkBSplineBaseTransformPython.itkBSplineBaseTransformD23_SetCoefficientImages)
    GetCoefficientImages = _swig_new_instance_method(_itkBSplineBaseTransformPython.itkBSplineBaseTransformD23_GetCoefficientImages)
    UpdateTransformParameters = _swig_new_instance_method(_itkBSplineBaseTransformPython.itkBSplineBaseTransformD23_UpdateTransformParameters)
    TransformPoint = _swig_new_instance_method(_itkBSplineBaseTransformPython.itkBSplineBaseTransformD23_TransformPoint)
    GetNumberOfWeights = _swig_new_instance_method(_itkBSplineBaseTransformPython.itkBSplineBaseTransformD23_GetNumberOfWeights)
    TransformVector = _swig_new_instance_method(_itkBSplineBaseTransformPython.itkBSplineBaseTransformD23_TransformVector)
    ComputeJacobianFromBSplineWeightsWithRespectToPosition = _swig_new_instance_method(_itkBSplineBaseTransformPython.itkBSplineBaseTransformD23_ComputeJacobianFromBSplineWeightsWithRespectToPosition)
    GetNumberOfParametersPerDimension = _swig_new_instance_method(_itkBSplineBaseTransformPython.itkBSplineBaseTransformD23_GetNumberOfParametersPerDimension)
    GetNumberOfAffectedWeights = _swig_new_instance_method(_itkBSplineBaseTransformPython.itkBSplineBaseTransformD23_GetNumberOfAffectedWeights)
    __swig_destroy__ = _itkBSplineBaseTransformPython.delete_itkBSplineBaseTransformD23
    cast = _swig_new_static_method(_itkBSplineBaseTransformPython.itkBSplineBaseTransformD23_cast)

# Register itkBSplineBaseTransformD23 in _itkBSplineBaseTransformPython:
_itkBSplineBaseTransformPython.itkBSplineBaseTransformD23_swigregister(itkBSplineBaseTransformD23)
itkBSplineBaseTransformD23_cast = _itkBSplineBaseTransformPython.itkBSplineBaseTransformD23_cast

class itkBSplineBaseTransformD33(itk.itkTransformBasePython.itkTransformD33):
    r"""


    A base class with common elements of BSplineTransform and
    BSplineDeformableTransform.

    C++ includes: itkBSplineBaseTransform.h 
    """

    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined - class is abstract")
    __repr__ = _swig_repr
    Clone = _swig_new_instance_method(_itkBSplineBaseTransformPython.itkBSplineBaseTransformD33_Clone)
    SetIdentity = _swig_new_instance_method(_itkBSplineBaseTransformPython.itkBSplineBaseTransformD33_SetIdentity)
    SetCoefficientImages = _swig_new_instance_method(_itkBSplineBaseTransformPython.itkBSplineBaseTransformD33_SetCoefficientImages)
    GetCoefficientImages = _swig_new_instance_method(_itkBSplineBaseTransformPython.itkBSplineBaseTransformD33_GetCoefficientImages)
    UpdateTransformParameters = _swig_new_instance_method(_itkBSplineBaseTransformPython.itkBSplineBaseTransformD33_UpdateTransformParameters)
    TransformPoint = _swig_new_instance_method(_itkBSplineBaseTransformPython.itkBSplineBaseTransformD33_TransformPoint)
    GetNumberOfWeights = _swig_new_instance_method(_itkBSplineBaseTransformPython.itkBSplineBaseTransformD33_GetNumberOfWeights)
    TransformVector = _swig_new_instance_method(_itkBSplineBaseTransformPython.itkBSplineBaseTransformD33_TransformVector)
    ComputeJacobianFromBSplineWeightsWithRespectToPosition = _swig_new_instance_method(_itkBSplineBaseTransformPython.itkBSplineBaseTransformD33_ComputeJacobianFromBSplineWeightsWithRespectToPosition)
    GetNumberOfParametersPerDimension = _swig_new_instance_method(_itkBSplineBaseTransformPython.itkBSplineBaseTransformD33_GetNumberOfParametersPerDimension)
    GetNumberOfAffectedWeights = _swig_new_instance_method(_itkBSplineBaseTransformPython.itkBSplineBaseTransformD33_GetNumberOfAffectedWeights)
    __swig_destroy__ = _itkBSplineBaseTransformPython.delete_itkBSplineBaseTransformD33
    cast = _swig_new_static_method(_itkBSplineBaseTransformPython.itkBSplineBaseTransformD33_cast)

# Register itkBSplineBaseTransformD33 in _itkBSplineBaseTransformPython:
_itkBSplineBaseTransformPython.itkBSplineBaseTransformD33_swigregister(itkBSplineBaseTransformD33)
itkBSplineBaseTransformD33_cast = _itkBSplineBaseTransformPython.itkBSplineBaseTransformD33_cast



