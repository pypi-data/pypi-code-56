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
    from . import _itkQuadEdgeCellTraitsInfoPython
else:
    import _itkQuadEdgeCellTraitsInfoPython

try:
    import builtins as __builtin__
except ImportError:
    import __builtin__

_swig_new_instance_method = _itkQuadEdgeCellTraitsInfoPython.SWIG_PyInstanceMethod_New
_swig_new_static_method = _itkQuadEdgeCellTraitsInfoPython.SWIG_PyStaticMethod_New

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


import itk.itkQuadEdgeMeshPointPython
import itk.itkGeometricalQuadEdgePython
import itk.itkQuadEdgePython
import itk.pyBasePython
import itk.itkPointPython
import itk.itkVectorPython
import itk.itkFixedArrayPython
import itk.vnl_vector_refPython
import itk.stdcomplexPython
import itk.vnl_vectorPython
import itk.vnl_matrixPython
import itk.ITKCommonBasePython

def itkMapContainerULQEMPF2GQEULULBBT_New():
    return itkMapContainerULQEMPF2GQEULULBBT.New()

class itkMapContainerULQEMPF2GQEULULBBT(itk.ITKCommonBasePython.itkObject):
    r"""


    A wrapper of the STL "map" container.

    Define a front-end to the STL "map" container that conforms to the
    IndexedContainerInterface. This is a full-fleged Object, so there are
    events, modification time, debug, and reference count information.

    Parameters:
    -----------

    TElementIdentifier:  A type that shall be used to index the container.
    It must have a < operator defined for ordering.

    TElement:  The element type stored in the container.

    C++ includes: itkMapContainer.h 
    """

    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr

    def __init__(self, *args):
        r"""
        __init__(itkMapContainerULQEMPF2GQEULULBBT self) -> itkMapContainerULQEMPF2GQEULULBBT
        __init__(itkMapContainerULQEMPF2GQEULULBBT self, std::less< unsigned long > const & comp) -> itkMapContainerULQEMPF2GQEULULBBT


        A wrapper of the STL "map" container.

        Define a front-end to the STL "map" container that conforms to the
        IndexedContainerInterface. This is a full-fleged Object, so there are
        events, modification time, debug, and reference count information.

        Parameters:
        -----------

        TElementIdentifier:  A type that shall be used to index the container.
        It must have a < operator defined for ordering.

        TElement:  The element type stored in the container.

        C++ includes: itkMapContainer.h 
        """
        _itkQuadEdgeCellTraitsInfoPython.itkMapContainerULQEMPF2GQEULULBBT_swiginit(self, _itkQuadEdgeCellTraitsInfoPython.new_itkMapContainerULQEMPF2GQEULULBBT(*args))
    __New_orig__ = _swig_new_static_method(_itkQuadEdgeCellTraitsInfoPython.itkMapContainerULQEMPF2GQEULULBBT___New_orig__)
    Clone = _swig_new_instance_method(_itkQuadEdgeCellTraitsInfoPython.itkMapContainerULQEMPF2GQEULULBBT_Clone)
    CastToSTLContainer = _swig_new_instance_method(_itkQuadEdgeCellTraitsInfoPython.itkMapContainerULQEMPF2GQEULULBBT_CastToSTLContainer)
    CastToSTLConstContainer = _swig_new_instance_method(_itkQuadEdgeCellTraitsInfoPython.itkMapContainerULQEMPF2GQEULULBBT_CastToSTLConstContainer)
    ElementAt = _swig_new_instance_method(_itkQuadEdgeCellTraitsInfoPython.itkMapContainerULQEMPF2GQEULULBBT_ElementAt)
    CreateElementAt = _swig_new_instance_method(_itkQuadEdgeCellTraitsInfoPython.itkMapContainerULQEMPF2GQEULULBBT_CreateElementAt)
    GetElement = _swig_new_instance_method(_itkQuadEdgeCellTraitsInfoPython.itkMapContainerULQEMPF2GQEULULBBT_GetElement)
    SetElement = _swig_new_instance_method(_itkQuadEdgeCellTraitsInfoPython.itkMapContainerULQEMPF2GQEULULBBT_SetElement)
    InsertElement = _swig_new_instance_method(_itkQuadEdgeCellTraitsInfoPython.itkMapContainerULQEMPF2GQEULULBBT_InsertElement)
    IndexExists = _swig_new_instance_method(_itkQuadEdgeCellTraitsInfoPython.itkMapContainerULQEMPF2GQEULULBBT_IndexExists)
    GetElementIfIndexExists = _swig_new_instance_method(_itkQuadEdgeCellTraitsInfoPython.itkMapContainerULQEMPF2GQEULULBBT_GetElementIfIndexExists)
    CreateIndex = _swig_new_instance_method(_itkQuadEdgeCellTraitsInfoPython.itkMapContainerULQEMPF2GQEULULBBT_CreateIndex)
    DeleteIndex = _swig_new_instance_method(_itkQuadEdgeCellTraitsInfoPython.itkMapContainerULQEMPF2GQEULULBBT_DeleteIndex)
    Size = _swig_new_instance_method(_itkQuadEdgeCellTraitsInfoPython.itkMapContainerULQEMPF2GQEULULBBT_Size)
    Reserve = _swig_new_instance_method(_itkQuadEdgeCellTraitsInfoPython.itkMapContainerULQEMPF2GQEULULBBT_Reserve)
    Squeeze = _swig_new_instance_method(_itkQuadEdgeCellTraitsInfoPython.itkMapContainerULQEMPF2GQEULULBBT_Squeeze)
    Initialize = _swig_new_instance_method(_itkQuadEdgeCellTraitsInfoPython.itkMapContainerULQEMPF2GQEULULBBT_Initialize)
    __swig_destroy__ = _itkQuadEdgeCellTraitsInfoPython.delete_itkMapContainerULQEMPF2GQEULULBBT
    cast = _swig_new_static_method(_itkQuadEdgeCellTraitsInfoPython.itkMapContainerULQEMPF2GQEULULBBT_cast)

    def New(*args, **kargs):
        """New() -> itkMapContainerULQEMPF2GQEULULBBT

        Create a new object of the class itkMapContainerULQEMPF2GQEULULBBT and set the input and the parameters if some
        named or non-named arguments are passed to that method.

        New() tries to assign all the non named parameters to the input of the new objects - the
        first non named parameter in the first input, etc.

        The named parameters are used by calling the method with the same name prefixed by 'Set'.

        Ex:

          itkMapContainerULQEMPF2GQEULULBBT.New(reader, threshold=10)

        is (most of the time) equivalent to:

          obj = itkMapContainerULQEMPF2GQEULULBBT.New()
          obj.SetInput(0, reader.GetOutput())
          obj.SetThreshold(10)
        """
        obj = itkMapContainerULQEMPF2GQEULULBBT.__New_orig__()
        import itkTemplate
        itkTemplate.New(obj, *args, **kargs)
        return obj
    New = staticmethod(New)


# Register itkMapContainerULQEMPF2GQEULULBBT in _itkQuadEdgeCellTraitsInfoPython:
_itkQuadEdgeCellTraitsInfoPython.itkMapContainerULQEMPF2GQEULULBBT_swigregister(itkMapContainerULQEMPF2GQEULULBBT)
itkMapContainerULQEMPF2GQEULULBBT___New_orig__ = _itkQuadEdgeCellTraitsInfoPython.itkMapContainerULQEMPF2GQEULULBBT___New_orig__
itkMapContainerULQEMPF2GQEULULBBT_cast = _itkQuadEdgeCellTraitsInfoPython.itkMapContainerULQEMPF2GQEULULBBT_cast


def itkMapContainerULQEMPF3GQEULULBBT_New():
    return itkMapContainerULQEMPF3GQEULULBBT.New()

class itkMapContainerULQEMPF3GQEULULBBT(itk.ITKCommonBasePython.itkObject):
    r"""


    A wrapper of the STL "map" container.

    Define a front-end to the STL "map" container that conforms to the
    IndexedContainerInterface. This is a full-fleged Object, so there are
    events, modification time, debug, and reference count information.

    Parameters:
    -----------

    TElementIdentifier:  A type that shall be used to index the container.
    It must have a < operator defined for ordering.

    TElement:  The element type stored in the container.

    C++ includes: itkMapContainer.h 
    """

    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr

    def __init__(self, *args):
        r"""
        __init__(itkMapContainerULQEMPF3GQEULULBBT self) -> itkMapContainerULQEMPF3GQEULULBBT
        __init__(itkMapContainerULQEMPF3GQEULULBBT self, std::less< unsigned long > const & comp) -> itkMapContainerULQEMPF3GQEULULBBT


        A wrapper of the STL "map" container.

        Define a front-end to the STL "map" container that conforms to the
        IndexedContainerInterface. This is a full-fleged Object, so there are
        events, modification time, debug, and reference count information.

        Parameters:
        -----------

        TElementIdentifier:  A type that shall be used to index the container.
        It must have a < operator defined for ordering.

        TElement:  The element type stored in the container.

        C++ includes: itkMapContainer.h 
        """
        _itkQuadEdgeCellTraitsInfoPython.itkMapContainerULQEMPF3GQEULULBBT_swiginit(self, _itkQuadEdgeCellTraitsInfoPython.new_itkMapContainerULQEMPF3GQEULULBBT(*args))
    __New_orig__ = _swig_new_static_method(_itkQuadEdgeCellTraitsInfoPython.itkMapContainerULQEMPF3GQEULULBBT___New_orig__)
    Clone = _swig_new_instance_method(_itkQuadEdgeCellTraitsInfoPython.itkMapContainerULQEMPF3GQEULULBBT_Clone)
    CastToSTLContainer = _swig_new_instance_method(_itkQuadEdgeCellTraitsInfoPython.itkMapContainerULQEMPF3GQEULULBBT_CastToSTLContainer)
    CastToSTLConstContainer = _swig_new_instance_method(_itkQuadEdgeCellTraitsInfoPython.itkMapContainerULQEMPF3GQEULULBBT_CastToSTLConstContainer)
    ElementAt = _swig_new_instance_method(_itkQuadEdgeCellTraitsInfoPython.itkMapContainerULQEMPF3GQEULULBBT_ElementAt)
    CreateElementAt = _swig_new_instance_method(_itkQuadEdgeCellTraitsInfoPython.itkMapContainerULQEMPF3GQEULULBBT_CreateElementAt)
    GetElement = _swig_new_instance_method(_itkQuadEdgeCellTraitsInfoPython.itkMapContainerULQEMPF3GQEULULBBT_GetElement)
    SetElement = _swig_new_instance_method(_itkQuadEdgeCellTraitsInfoPython.itkMapContainerULQEMPF3GQEULULBBT_SetElement)
    InsertElement = _swig_new_instance_method(_itkQuadEdgeCellTraitsInfoPython.itkMapContainerULQEMPF3GQEULULBBT_InsertElement)
    IndexExists = _swig_new_instance_method(_itkQuadEdgeCellTraitsInfoPython.itkMapContainerULQEMPF3GQEULULBBT_IndexExists)
    GetElementIfIndexExists = _swig_new_instance_method(_itkQuadEdgeCellTraitsInfoPython.itkMapContainerULQEMPF3GQEULULBBT_GetElementIfIndexExists)
    CreateIndex = _swig_new_instance_method(_itkQuadEdgeCellTraitsInfoPython.itkMapContainerULQEMPF3GQEULULBBT_CreateIndex)
    DeleteIndex = _swig_new_instance_method(_itkQuadEdgeCellTraitsInfoPython.itkMapContainerULQEMPF3GQEULULBBT_DeleteIndex)
    Size = _swig_new_instance_method(_itkQuadEdgeCellTraitsInfoPython.itkMapContainerULQEMPF3GQEULULBBT_Size)
    Reserve = _swig_new_instance_method(_itkQuadEdgeCellTraitsInfoPython.itkMapContainerULQEMPF3GQEULULBBT_Reserve)
    Squeeze = _swig_new_instance_method(_itkQuadEdgeCellTraitsInfoPython.itkMapContainerULQEMPF3GQEULULBBT_Squeeze)
    Initialize = _swig_new_instance_method(_itkQuadEdgeCellTraitsInfoPython.itkMapContainerULQEMPF3GQEULULBBT_Initialize)
    __swig_destroy__ = _itkQuadEdgeCellTraitsInfoPython.delete_itkMapContainerULQEMPF3GQEULULBBT
    cast = _swig_new_static_method(_itkQuadEdgeCellTraitsInfoPython.itkMapContainerULQEMPF3GQEULULBBT_cast)

    def New(*args, **kargs):
        """New() -> itkMapContainerULQEMPF3GQEULULBBT

        Create a new object of the class itkMapContainerULQEMPF3GQEULULBBT and set the input and the parameters if some
        named or non-named arguments are passed to that method.

        New() tries to assign all the non named parameters to the input of the new objects - the
        first non named parameter in the first input, etc.

        The named parameters are used by calling the method with the same name prefixed by 'Set'.

        Ex:

          itkMapContainerULQEMPF3GQEULULBBT.New(reader, threshold=10)

        is (most of the time) equivalent to:

          obj = itkMapContainerULQEMPF3GQEULULBBT.New()
          obj.SetInput(0, reader.GetOutput())
          obj.SetThreshold(10)
        """
        obj = itkMapContainerULQEMPF3GQEULULBBT.__New_orig__()
        import itkTemplate
        itkTemplate.New(obj, *args, **kargs)
        return obj
    New = staticmethod(New)


# Register itkMapContainerULQEMPF3GQEULULBBT in _itkQuadEdgeCellTraitsInfoPython:
_itkQuadEdgeCellTraitsInfoPython.itkMapContainerULQEMPF3GQEULULBBT_swigregister(itkMapContainerULQEMPF3GQEULULBBT)
itkMapContainerULQEMPF3GQEULULBBT___New_orig__ = _itkQuadEdgeCellTraitsInfoPython.itkMapContainerULQEMPF3GQEULULBBT___New_orig__
itkMapContainerULQEMPF3GQEULULBBT_cast = _itkQuadEdgeCellTraitsInfoPython.itkMapContainerULQEMPF3GQEULULBBT_cast

class itkQuadEdgeMeshCellTraitsInfo2FFULULUCQEMPGQEULQEMPF2GQEULULBBTGQE(object):
    r"""Proxy of C++ itkQuadEdgeMeshCellTraitsInfo2FFULULUCQEMPGQEULQEMPF2GQEULULBBTGQE class."""

    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr

    def __init__(self, *args):
        r"""
        __init__(itkQuadEdgeMeshCellTraitsInfo2FFULULUCQEMPGQEULQEMPF2GQEULULBBTGQE self) -> itkQuadEdgeMeshCellTraitsInfo2FFULULUCQEMPGQEULQEMPF2GQEULULBBTGQE
        __init__(itkQuadEdgeMeshCellTraitsInfo2FFULULUCQEMPGQEULQEMPF2GQEULULBBTGQE self, itkQuadEdgeMeshCellTraitsInfo2FFULULUCQEMPGQEULQEMPF2GQEULULBBTGQE arg0) -> itkQuadEdgeMeshCellTraitsInfo2FFULULUCQEMPGQEULQEMPF2GQEULULBBTGQE
        """
        _itkQuadEdgeCellTraitsInfoPython.itkQuadEdgeMeshCellTraitsInfo2FFULULUCQEMPGQEULQEMPF2GQEULULBBTGQE_swiginit(self, _itkQuadEdgeCellTraitsInfoPython.new_itkQuadEdgeMeshCellTraitsInfo2FFULULUCQEMPGQEULQEMPF2GQEULULBBTGQE(*args))
    __swig_destroy__ = _itkQuadEdgeCellTraitsInfoPython.delete_itkQuadEdgeMeshCellTraitsInfo2FFULULUCQEMPGQEULQEMPF2GQEULULBBTGQE

# Register itkQuadEdgeMeshCellTraitsInfo2FFULULUCQEMPGQEULQEMPF2GQEULULBBTGQE in _itkQuadEdgeCellTraitsInfoPython:
_itkQuadEdgeCellTraitsInfoPython.itkQuadEdgeMeshCellTraitsInfo2FFULULUCQEMPGQEULQEMPF2GQEULULBBTGQE_swigregister(itkQuadEdgeMeshCellTraitsInfo2FFULULUCQEMPGQEULQEMPF2GQEULULBBTGQE)

class itkQuadEdgeMeshCellTraitsInfo3FFULULUCQEMPGQEULQEMPF3GQEULULBBTGQE(object):
    r"""Proxy of C++ itkQuadEdgeMeshCellTraitsInfo3FFULULUCQEMPGQEULQEMPF3GQEULULBBTGQE class."""

    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr

    def __init__(self, *args):
        r"""
        __init__(itkQuadEdgeMeshCellTraitsInfo3FFULULUCQEMPGQEULQEMPF3GQEULULBBTGQE self) -> itkQuadEdgeMeshCellTraitsInfo3FFULULUCQEMPGQEULQEMPF3GQEULULBBTGQE
        __init__(itkQuadEdgeMeshCellTraitsInfo3FFULULUCQEMPGQEULQEMPF3GQEULULBBTGQE self, itkQuadEdgeMeshCellTraitsInfo3FFULULUCQEMPGQEULQEMPF3GQEULULBBTGQE arg0) -> itkQuadEdgeMeshCellTraitsInfo3FFULULUCQEMPGQEULQEMPF3GQEULULBBTGQE
        """
        _itkQuadEdgeCellTraitsInfoPython.itkQuadEdgeMeshCellTraitsInfo3FFULULUCQEMPGQEULQEMPF3GQEULULBBTGQE_swiginit(self, _itkQuadEdgeCellTraitsInfoPython.new_itkQuadEdgeMeshCellTraitsInfo3FFULULUCQEMPGQEULQEMPF3GQEULULBBTGQE(*args))
    __swig_destroy__ = _itkQuadEdgeCellTraitsInfoPython.delete_itkQuadEdgeMeshCellTraitsInfo3FFULULUCQEMPGQEULQEMPF3GQEULULBBTGQE

# Register itkQuadEdgeMeshCellTraitsInfo3FFULULUCQEMPGQEULQEMPF3GQEULULBBTGQE in _itkQuadEdgeCellTraitsInfoPython:
_itkQuadEdgeCellTraitsInfoPython.itkQuadEdgeMeshCellTraitsInfo3FFULULUCQEMPGQEULQEMPF3GQEULULBBTGQE_swigregister(itkQuadEdgeMeshCellTraitsInfo3FFULULUCQEMPGQEULQEMPF3GQEULULBBTGQE)



