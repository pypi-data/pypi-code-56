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
    from . import _itkGeometricalQuadEdgePython
else:
    import _itkGeometricalQuadEdgePython

try:
    import builtins as __builtin__
except ImportError:
    import __builtin__

_swig_new_instance_method = _itkGeometricalQuadEdgePython.SWIG_PyInstanceMethod_New
_swig_new_static_method = _itkGeometricalQuadEdgePython.SWIG_PyStaticMethod_New

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


import itk.itkQuadEdgePython
import itk.pyBasePython
class itkGeometricalQuadEdgeULULBBF(itk.itkQuadEdgePython.itkQuadEdge):
    r"""


    This class extends the QuadEdge by adding a reference to the Origin.

    The class is implemented in such a way that it can generate its own
    Dual. In a physical edge, there will be four GeometricalQuadEdge. Two
    of them will be Primal and two will be Dual. The Primal ones are
    parallel to the physical edge and their origins relate to the mesh
    points. The Dual ones are orthogonal to the physical edge and their
    origins relate to the faces at each side of the physical edge.

    The only purpose of the last parameter of the template is to guarantee
    that the two types GeometricalQuadEdge and GeometricalQuadEdge::Dual
    are always different (in the sense that their typeid() are different).
    If we only had the four first parameters and assume that
    GeometricalQuadEdge gets instantiated with types such that TVRef =
    TFRef and TPrimalData = TDualData then this instantiation
    GeometricalQuadEdge and GeometricalQuadEdge::Dual would be the same
    types (this is simply due to the very definition of
    GeometricalQuadEdge::Dual). This would in turn make the types QEType
    and QEDual of QuadEdgeMesh identical and would prevent any algorithm
    requiring to distinguish those types (e.g. by relying on a
    dynamic_cast<QEType*>) to be effective. This justifies the existence
    of last dummy template parameter and it's default value.

    Alexandre Gouaillard, Leonardo Florez-Valencia, Eric Boix  This
    implementation was contributed as a paper to the Insight
    Journalhttps://hdl.handle.net/1926/306

    See:   QuadEdge

    C++ includes: itkGeometricalQuadEdge.h 
    """

    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr
    BeginGeomOnext = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBF_BeginGeomOnext)
    EndGeomOnext = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBF_EndGeomOnext)
    BeginGeomSym = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBF_BeginGeomSym)
    EndGeomSym = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBF_EndGeomSym)
    BeginGeomLnext = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBF_BeginGeomLnext)
    EndGeomLnext = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBF_EndGeomLnext)
    BeginGeomRnext = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBF_BeginGeomRnext)
    EndGeomRnext = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBF_EndGeomRnext)
    BeginGeomDnext = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBF_BeginGeomDnext)
    EndGeomDnext = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBF_EndGeomDnext)
    BeginGeomOprev = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBF_BeginGeomOprev)
    EndGeomOprev = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBF_EndGeomOprev)
    BeginGeomLprev = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBF_BeginGeomLprev)
    EndGeomLprev = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBF_EndGeomLprev)
    BeginGeomRprev = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBF_BeginGeomRprev)
    EndGeomRprev = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBF_EndGeomRprev)
    BeginGeomDprev = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBF_BeginGeomDprev)
    EndGeomDprev = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBF_EndGeomDprev)
    BeginGeomInvOnext = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBF_BeginGeomInvOnext)
    EndGeomInvOnext = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBF_EndGeomInvOnext)
    BeginGeomInvLnext = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBF_BeginGeomInvLnext)
    EndGeomInvLnext = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBF_EndGeomInvLnext)
    BeginGeomInvRnext = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBF_BeginGeomInvRnext)
    EndGeomInvRnext = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBF_EndGeomInvRnext)
    BeginGeomInvDnext = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBF_BeginGeomInvDnext)
    EndGeomInvDnext = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBF_EndGeomInvDnext)
    GetOnext = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBF_GetOnext)
    GetRot = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBF_GetRot)
    GetSym = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBF_GetSym)
    GetLnext = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBF_GetLnext)
    GetRnext = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBF_GetRnext)
    GetDnext = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBF_GetDnext)
    GetOprev = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBF_GetOprev)
    GetLprev = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBF_GetLprev)
    GetRprev = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBF_GetRprev)
    GetDprev = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBF_GetDprev)
    GetInvRot = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBF_GetInvRot)
    GetInvOnext = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBF_GetInvOnext)
    GetInvLnext = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBF_GetInvLnext)
    GetInvRnext = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBF_GetInvRnext)
    GetInvDnext = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBF_GetInvDnext)

    def __init__(self, *args):
        r"""
        __init__(itkGeometricalQuadEdgeULULBBF self) -> itkGeometricalQuadEdgeULULBBF
        __init__(itkGeometricalQuadEdgeULULBBF self, itkGeometricalQuadEdgeULULBBF arg0) -> itkGeometricalQuadEdgeULULBBF


        This class extends the QuadEdge by adding a reference to the Origin.

        The class is implemented in such a way that it can generate its own
        Dual. In a physical edge, there will be four GeometricalQuadEdge. Two
        of them will be Primal and two will be Dual. The Primal ones are
        parallel to the physical edge and their origins relate to the mesh
        points. The Dual ones are orthogonal to the physical edge and their
        origins relate to the faces at each side of the physical edge.

        The only purpose of the last parameter of the template is to guarantee
        that the two types GeometricalQuadEdge and GeometricalQuadEdge::Dual
        are always different (in the sense that their typeid() are different).
        If we only had the four first parameters and assume that
        GeometricalQuadEdge gets instantiated with types such that TVRef =
        TFRef and TPrimalData = TDualData then this instantiation
        GeometricalQuadEdge and GeometricalQuadEdge::Dual would be the same
        types (this is simply due to the very definition of
        GeometricalQuadEdge::Dual). This would in turn make the types QEType
        and QEDual of QuadEdgeMesh identical and would prevent any algorithm
        requiring to distinguish those types (e.g. by relying on a
        dynamic_cast<QEType*>) to be effective. This justifies the existence
        of last dummy template parameter and it's default value.

        Alexandre Gouaillard, Leonardo Florez-Valencia, Eric Boix  This
        implementation was contributed as a paper to the Insight
        Journalhttps://hdl.handle.net/1926/306

        See:   QuadEdge

        C++ includes: itkGeometricalQuadEdge.h 
        """
        _itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBF_swiginit(self, _itkGeometricalQuadEdgePython.new_itkGeometricalQuadEdgeULULBBF(*args))
    __swig_destroy__ = _itkGeometricalQuadEdgePython.delete_itkGeometricalQuadEdgeULULBBF
    SetOrigin = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBF_SetOrigin)
    SetDestination = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBF_SetDestination)
    SetRight = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBF_SetRight)
    SetLeft = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBF_SetLeft)
    SetLnextRingWithSameLeftFace = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBF_SetLnextRingWithSameLeftFace)
    UnsetOrigin = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBF_UnsetOrigin)
    UnsetDestination = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBF_UnsetDestination)
    UnsetRight = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBF_UnsetRight)
    UnsetLeft = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBF_UnsetLeft)
    GetOrigin = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBF_GetOrigin)
    GetDestination = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBF_GetDestination)
    GetRight = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBF_GetRight)
    GetLeft = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBF_GetLeft)
    IsOriginSet = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBF_IsOriginSet)
    IsDestinationSet = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBF_IsDestinationSet)
    IsRightSet = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBF_IsRightSet)
    IsLeftSet = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBF_IsLeftSet)
    SetPrimalData = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBF_SetPrimalData)
    SetDualData = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBF_SetDualData)
    UnsetPrimalData = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBF_UnsetPrimalData)
    UnsetDualData = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBF_UnsetDualData)
    GetPrimalData = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBF_GetPrimalData)
    GetDualData = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBF_GetDualData)
    IsPrimalDataSet = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBF_IsPrimalDataSet)
    IsDualDataSet = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBF_IsDualDataSet)
    IsWire = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBF_IsWire)
    IsAtBorder = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBF_IsAtBorder)
    IsInternal = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBF_IsInternal)
    IsOriginInternal = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBF_IsOriginInternal)
    IsLnextSharingSameFace = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBF_IsLnextSharingSameFace)
    IsLnextOfTriangle = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBF_IsLnextOfTriangle)
    IsInOnextRing = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBF_IsInOnextRing)
    IsInLnextRing = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBF_IsInLnextRing)
    GetNextBorderEdgeWithUnsetLeft = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBF_GetNextBorderEdgeWithUnsetLeft)
    InsertAfterNextBorderEdgeWithUnsetLeft = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBF_InsertAfterNextBorderEdgeWithUnsetLeft)
    ReorderOnextRingBeforeAddFace = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBF_ReorderOnextRingBeforeAddFace)
    IsOriginDisconnected = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBF_IsOriginDisconnected)
    IsDestinationDisconnected = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBF_IsDestinationDisconnected)
    IsDisconnected = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBF_IsDisconnected)
    Disconnect = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBF_Disconnect)
    SetIdent = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBF_SetIdent)
    GetIdent = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBF_GetIdent)

# Register itkGeometricalQuadEdgeULULBBF in _itkGeometricalQuadEdgePython:
_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBF_swigregister(itkGeometricalQuadEdgeULULBBF)

class itkGeometricalQuadEdgeULULBBT(itk.itkQuadEdgePython.itkQuadEdge):
    r"""


    This class extends the QuadEdge by adding a reference to the Origin.

    The class is implemented in such a way that it can generate its own
    Dual. In a physical edge, there will be four GeometricalQuadEdge. Two
    of them will be Primal and two will be Dual. The Primal ones are
    parallel to the physical edge and their origins relate to the mesh
    points. The Dual ones are orthogonal to the physical edge and their
    origins relate to the faces at each side of the physical edge.

    The only purpose of the last parameter of the template is to guarantee
    that the two types GeometricalQuadEdge and GeometricalQuadEdge::Dual
    are always different (in the sense that their typeid() are different).
    If we only had the four first parameters and assume that
    GeometricalQuadEdge gets instantiated with types such that TVRef =
    TFRef and TPrimalData = TDualData then this instantiation
    GeometricalQuadEdge and GeometricalQuadEdge::Dual would be the same
    types (this is simply due to the very definition of
    GeometricalQuadEdge::Dual). This would in turn make the types QEType
    and QEDual of QuadEdgeMesh identical and would prevent any algorithm
    requiring to distinguish those types (e.g. by relying on a
    dynamic_cast<QEType*>) to be effective. This justifies the existence
    of last dummy template parameter and it's default value.

    Alexandre Gouaillard, Leonardo Florez-Valencia, Eric Boix  This
    implementation was contributed as a paper to the Insight
    Journalhttps://hdl.handle.net/1926/306

    See:   QuadEdge

    C++ includes: itkGeometricalQuadEdge.h 
    """

    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr
    BeginGeomOnext = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBT_BeginGeomOnext)
    EndGeomOnext = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBT_EndGeomOnext)
    BeginGeomSym = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBT_BeginGeomSym)
    EndGeomSym = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBT_EndGeomSym)
    BeginGeomLnext = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBT_BeginGeomLnext)
    EndGeomLnext = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBT_EndGeomLnext)
    BeginGeomRnext = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBT_BeginGeomRnext)
    EndGeomRnext = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBT_EndGeomRnext)
    BeginGeomDnext = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBT_BeginGeomDnext)
    EndGeomDnext = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBT_EndGeomDnext)
    BeginGeomOprev = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBT_BeginGeomOprev)
    EndGeomOprev = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBT_EndGeomOprev)
    BeginGeomLprev = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBT_BeginGeomLprev)
    EndGeomLprev = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBT_EndGeomLprev)
    BeginGeomRprev = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBT_BeginGeomRprev)
    EndGeomRprev = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBT_EndGeomRprev)
    BeginGeomDprev = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBT_BeginGeomDprev)
    EndGeomDprev = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBT_EndGeomDprev)
    BeginGeomInvOnext = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBT_BeginGeomInvOnext)
    EndGeomInvOnext = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBT_EndGeomInvOnext)
    BeginGeomInvLnext = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBT_BeginGeomInvLnext)
    EndGeomInvLnext = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBT_EndGeomInvLnext)
    BeginGeomInvRnext = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBT_BeginGeomInvRnext)
    EndGeomInvRnext = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBT_EndGeomInvRnext)
    BeginGeomInvDnext = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBT_BeginGeomInvDnext)
    EndGeomInvDnext = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBT_EndGeomInvDnext)
    GetOnext = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBT_GetOnext)
    GetRot = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBT_GetRot)
    GetSym = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBT_GetSym)
    GetLnext = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBT_GetLnext)
    GetRnext = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBT_GetRnext)
    GetDnext = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBT_GetDnext)
    GetOprev = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBT_GetOprev)
    GetLprev = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBT_GetLprev)
    GetRprev = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBT_GetRprev)
    GetDprev = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBT_GetDprev)
    GetInvRot = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBT_GetInvRot)
    GetInvOnext = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBT_GetInvOnext)
    GetInvLnext = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBT_GetInvLnext)
    GetInvRnext = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBT_GetInvRnext)
    GetInvDnext = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBT_GetInvDnext)

    def __init__(self, *args):
        r"""
        __init__(itkGeometricalQuadEdgeULULBBT self) -> itkGeometricalQuadEdgeULULBBT
        __init__(itkGeometricalQuadEdgeULULBBT self, itkGeometricalQuadEdgeULULBBT arg0) -> itkGeometricalQuadEdgeULULBBT


        This class extends the QuadEdge by adding a reference to the Origin.

        The class is implemented in such a way that it can generate its own
        Dual. In a physical edge, there will be four GeometricalQuadEdge. Two
        of them will be Primal and two will be Dual. The Primal ones are
        parallel to the physical edge and their origins relate to the mesh
        points. The Dual ones are orthogonal to the physical edge and their
        origins relate to the faces at each side of the physical edge.

        The only purpose of the last parameter of the template is to guarantee
        that the two types GeometricalQuadEdge and GeometricalQuadEdge::Dual
        are always different (in the sense that their typeid() are different).
        If we only had the four first parameters and assume that
        GeometricalQuadEdge gets instantiated with types such that TVRef =
        TFRef and TPrimalData = TDualData then this instantiation
        GeometricalQuadEdge and GeometricalQuadEdge::Dual would be the same
        types (this is simply due to the very definition of
        GeometricalQuadEdge::Dual). This would in turn make the types QEType
        and QEDual of QuadEdgeMesh identical and would prevent any algorithm
        requiring to distinguish those types (e.g. by relying on a
        dynamic_cast<QEType*>) to be effective. This justifies the existence
        of last dummy template parameter and it's default value.

        Alexandre Gouaillard, Leonardo Florez-Valencia, Eric Boix  This
        implementation was contributed as a paper to the Insight
        Journalhttps://hdl.handle.net/1926/306

        See:   QuadEdge

        C++ includes: itkGeometricalQuadEdge.h 
        """
        _itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBT_swiginit(self, _itkGeometricalQuadEdgePython.new_itkGeometricalQuadEdgeULULBBT(*args))
    __swig_destroy__ = _itkGeometricalQuadEdgePython.delete_itkGeometricalQuadEdgeULULBBT
    SetOrigin = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBT_SetOrigin)
    SetDestination = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBT_SetDestination)
    SetRight = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBT_SetRight)
    SetLeft = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBT_SetLeft)
    SetLnextRingWithSameLeftFace = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBT_SetLnextRingWithSameLeftFace)
    UnsetOrigin = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBT_UnsetOrigin)
    UnsetDestination = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBT_UnsetDestination)
    UnsetRight = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBT_UnsetRight)
    UnsetLeft = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBT_UnsetLeft)
    GetOrigin = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBT_GetOrigin)
    GetDestination = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBT_GetDestination)
    GetRight = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBT_GetRight)
    GetLeft = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBT_GetLeft)
    IsOriginSet = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBT_IsOriginSet)
    IsDestinationSet = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBT_IsDestinationSet)
    IsRightSet = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBT_IsRightSet)
    IsLeftSet = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBT_IsLeftSet)
    SetPrimalData = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBT_SetPrimalData)
    SetDualData = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBT_SetDualData)
    UnsetPrimalData = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBT_UnsetPrimalData)
    UnsetDualData = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBT_UnsetDualData)
    GetPrimalData = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBT_GetPrimalData)
    GetDualData = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBT_GetDualData)
    IsPrimalDataSet = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBT_IsPrimalDataSet)
    IsDualDataSet = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBT_IsDualDataSet)
    IsWire = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBT_IsWire)
    IsAtBorder = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBT_IsAtBorder)
    IsInternal = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBT_IsInternal)
    IsOriginInternal = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBT_IsOriginInternal)
    IsLnextSharingSameFace = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBT_IsLnextSharingSameFace)
    IsLnextOfTriangle = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBT_IsLnextOfTriangle)
    IsInOnextRing = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBT_IsInOnextRing)
    IsInLnextRing = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBT_IsInLnextRing)
    GetNextBorderEdgeWithUnsetLeft = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBT_GetNextBorderEdgeWithUnsetLeft)
    InsertAfterNextBorderEdgeWithUnsetLeft = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBT_InsertAfterNextBorderEdgeWithUnsetLeft)
    ReorderOnextRingBeforeAddFace = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBT_ReorderOnextRingBeforeAddFace)
    IsOriginDisconnected = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBT_IsOriginDisconnected)
    IsDestinationDisconnected = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBT_IsDestinationDisconnected)
    IsDisconnected = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBT_IsDisconnected)
    Disconnect = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBT_Disconnect)
    SetIdent = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBT_SetIdent)
    GetIdent = _swig_new_instance_method(_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBT_GetIdent)

# Register itkGeometricalQuadEdgeULULBBT in _itkGeometricalQuadEdgePython:
_itkGeometricalQuadEdgePython.itkGeometricalQuadEdgeULULBBT_swigregister(itkGeometricalQuadEdgeULULBBT)



