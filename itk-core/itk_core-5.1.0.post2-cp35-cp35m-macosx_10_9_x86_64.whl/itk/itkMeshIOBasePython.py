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
    from . import _itkMeshIOBasePython
else:
    import _itkMeshIOBasePython

try:
    import builtins as __builtin__
except ImportError:
    import __builtin__

_swig_new_instance_method = _itkMeshIOBasePython.SWIG_PyInstanceMethod_New
_swig_new_static_method = _itkMeshIOBasePython.SWIG_PyStaticMethod_New

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


import itk.ITKCommonBasePython
import itk.pyBasePython
class itkMeshIOBase(itk.ITKCommonBasePython.itkLightProcessObject):
    r"""


    Abstract superclass defines mesh IO interface.

    MeshIOBase is a class that reads and/or writes Mesh / QuadEdgeMesh
    data of a particular format (such as PNG or raw binary). The
    MeshIOBase encapsulates both the reading and writing of data. The
    MeshIOBase is used by the MeshFileReader class (to read data) and the
    MeshFileWriter (to write data) into a single file. Normally the user
    does not directly manipulate this class other than to instantiate it,
    set the FileName, and assign it to a MeshFileReader or MeshFileWriter.

    A Pluggable factory pattern is used this allows different kinds of
    readers to be registered (even at run time) without having to modify
    the code in this class.

    Wanlin Zhu. Uviversity of New South Wales, Australia.

    See:   MeshFileWriter

    See:   MeshFileReader

    C++ includes: itkMeshIOBase.h 
    """

    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined - class is abstract")
    __repr__ = _swig_repr
    SetFileName = _swig_new_instance_method(_itkMeshIOBasePython.itkMeshIOBase_SetFileName)
    GetFileName = _swig_new_instance_method(_itkMeshIOBasePython.itkMeshIOBase_GetFileName)
    SetPointPixelType = _swig_new_instance_method(_itkMeshIOBasePython.itkMeshIOBase_SetPointPixelType)
    GetPointPixelType = _swig_new_instance_method(_itkMeshIOBasePython.itkMeshIOBase_GetPointPixelType)
    SetCellPixelType = _swig_new_instance_method(_itkMeshIOBasePython.itkMeshIOBase_SetCellPixelType)
    GetCellPixelType = _swig_new_instance_method(_itkMeshIOBasePython.itkMeshIOBase_GetCellPixelType)
    SetPointComponentType = _swig_new_instance_method(_itkMeshIOBasePython.itkMeshIOBase_SetPointComponentType)
    GetPointComponentType = _swig_new_instance_method(_itkMeshIOBasePython.itkMeshIOBase_GetPointComponentType)
    SetCellComponentType = _swig_new_instance_method(_itkMeshIOBasePython.itkMeshIOBase_SetCellComponentType)
    GetCellComponentType = _swig_new_instance_method(_itkMeshIOBasePython.itkMeshIOBase_GetCellComponentType)
    SetPointPixelComponentType = _swig_new_instance_method(_itkMeshIOBasePython.itkMeshIOBase_SetPointPixelComponentType)
    GetPointPixelComponentType = _swig_new_instance_method(_itkMeshIOBasePython.itkMeshIOBase_GetPointPixelComponentType)
    SetCellPixelComponentType = _swig_new_instance_method(_itkMeshIOBasePython.itkMeshIOBase_SetCellPixelComponentType)
    GetCellPixelComponentType = _swig_new_instance_method(_itkMeshIOBasePython.itkMeshIOBase_GetCellPixelComponentType)
    SetNumberOfPointPixelComponents = _swig_new_instance_method(_itkMeshIOBasePython.itkMeshIOBase_SetNumberOfPointPixelComponents)
    GetNumberOfPointPixelComponents = _swig_new_instance_method(_itkMeshIOBasePython.itkMeshIOBase_GetNumberOfPointPixelComponents)
    SetNumberOfCellPixelComponents = _swig_new_instance_method(_itkMeshIOBasePython.itkMeshIOBase_SetNumberOfCellPixelComponents)
    GetNumberOfCellPixelComponents = _swig_new_instance_method(_itkMeshIOBasePython.itkMeshIOBase_GetNumberOfCellPixelComponents)
    SetPointDimension = _swig_new_instance_method(_itkMeshIOBasePython.itkMeshIOBase_SetPointDimension)
    GetPointDimension = _swig_new_instance_method(_itkMeshIOBasePython.itkMeshIOBase_GetPointDimension)
    SetNumberOfPoints = _swig_new_instance_method(_itkMeshIOBasePython.itkMeshIOBase_SetNumberOfPoints)
    GetNumberOfPoints = _swig_new_instance_method(_itkMeshIOBasePython.itkMeshIOBase_GetNumberOfPoints)
    SetNumberOfCells = _swig_new_instance_method(_itkMeshIOBasePython.itkMeshIOBase_SetNumberOfCells)
    GetNumberOfCells = _swig_new_instance_method(_itkMeshIOBasePython.itkMeshIOBase_GetNumberOfCells)
    SetNumberOfPointPixels = _swig_new_instance_method(_itkMeshIOBasePython.itkMeshIOBase_SetNumberOfPointPixels)
    GetNumberOfPointPixels = _swig_new_instance_method(_itkMeshIOBasePython.itkMeshIOBase_GetNumberOfPointPixels)
    SetNumberOfCellPixels = _swig_new_instance_method(_itkMeshIOBasePython.itkMeshIOBase_SetNumberOfCellPixels)
    GetNumberOfCellPixels = _swig_new_instance_method(_itkMeshIOBasePython.itkMeshIOBase_GetNumberOfCellPixels)
    SetCellBufferSize = _swig_new_instance_method(_itkMeshIOBasePython.itkMeshIOBase_SetCellBufferSize)
    GetCellBufferSize = _swig_new_instance_method(_itkMeshIOBasePython.itkMeshIOBase_GetCellBufferSize)
    SetUpdatePoints = _swig_new_instance_method(_itkMeshIOBasePython.itkMeshIOBase_SetUpdatePoints)
    GetUpdatePoints = _swig_new_instance_method(_itkMeshIOBasePython.itkMeshIOBase_GetUpdatePoints)
    SetUpdateCells = _swig_new_instance_method(_itkMeshIOBasePython.itkMeshIOBase_SetUpdateCells)
    GetUpdateCells = _swig_new_instance_method(_itkMeshIOBasePython.itkMeshIOBase_GetUpdateCells)
    SetUpdatePointData = _swig_new_instance_method(_itkMeshIOBasePython.itkMeshIOBase_SetUpdatePointData)
    GetUpdatePointData = _swig_new_instance_method(_itkMeshIOBasePython.itkMeshIOBase_GetUpdatePointData)
    SetUpdateCellData = _swig_new_instance_method(_itkMeshIOBasePython.itkMeshIOBase_SetUpdateCellData)
    GetUpdateCellData = _swig_new_instance_method(_itkMeshIOBasePython.itkMeshIOBase_GetUpdateCellData)
    GetComponentSize = _swig_new_instance_method(_itkMeshIOBasePython.itkMeshIOBase_GetComponentSize)
    GetComponentTypeAsString = _swig_new_instance_method(_itkMeshIOBasePython.itkMeshIOBase_GetComponentTypeAsString)
    GetPixelTypeAsString = _swig_new_instance_method(_itkMeshIOBasePython.itkMeshIOBase_GetPixelTypeAsString)
    SetFileType = _swig_new_instance_method(_itkMeshIOBasePython.itkMeshIOBase_SetFileType)
    GetFileType = _swig_new_instance_method(_itkMeshIOBasePython.itkMeshIOBase_GetFileType)
    SetFileTypeToASCII = _swig_new_instance_method(_itkMeshIOBasePython.itkMeshIOBase_SetFileTypeToASCII)
    SetFileTypeToBinary = _swig_new_instance_method(_itkMeshIOBasePython.itkMeshIOBase_SetFileTypeToBinary)
    SetByteOrder = _swig_new_instance_method(_itkMeshIOBasePython.itkMeshIOBase_SetByteOrder)
    GetByteOrder = _swig_new_instance_method(_itkMeshIOBasePython.itkMeshIOBase_GetByteOrder)
    SetByteOrderToBigEndian = _swig_new_instance_method(_itkMeshIOBasePython.itkMeshIOBase_SetByteOrderToBigEndian)
    SetByteOrderToLittleEndian = _swig_new_instance_method(_itkMeshIOBasePython.itkMeshIOBase_SetByteOrderToLittleEndian)
    SetUseCompression = _swig_new_instance_method(_itkMeshIOBasePython.itkMeshIOBase_SetUseCompression)
    GetUseCompression = _swig_new_instance_method(_itkMeshIOBasePython.itkMeshIOBase_GetUseCompression)
    UseCompressionOn = _swig_new_instance_method(_itkMeshIOBasePython.itkMeshIOBase_UseCompressionOn)
    UseCompressionOff = _swig_new_instance_method(_itkMeshIOBasePython.itkMeshIOBase_UseCompressionOff)
    GetFileTypeAsString = _swig_new_instance_method(_itkMeshIOBasePython.itkMeshIOBase_GetFileTypeAsString)
    GetByteOrderAsString = _swig_new_instance_method(_itkMeshIOBasePython.itkMeshIOBase_GetByteOrderAsString)
    CanReadFile = _swig_new_instance_method(_itkMeshIOBasePython.itkMeshIOBase_CanReadFile)
    ReadMeshInformation = _swig_new_instance_method(_itkMeshIOBasePython.itkMeshIOBase_ReadMeshInformation)
    ReadPoints = _swig_new_instance_method(_itkMeshIOBasePython.itkMeshIOBase_ReadPoints)
    ReadCells = _swig_new_instance_method(_itkMeshIOBasePython.itkMeshIOBase_ReadCells)
    ReadPointData = _swig_new_instance_method(_itkMeshIOBasePython.itkMeshIOBase_ReadPointData)
    ReadCellData = _swig_new_instance_method(_itkMeshIOBasePython.itkMeshIOBase_ReadCellData)
    CanWriteFile = _swig_new_instance_method(_itkMeshIOBasePython.itkMeshIOBase_CanWriteFile)
    WriteMeshInformation = _swig_new_instance_method(_itkMeshIOBasePython.itkMeshIOBase_WriteMeshInformation)
    WritePoints = _swig_new_instance_method(_itkMeshIOBasePython.itkMeshIOBase_WritePoints)
    WriteCells = _swig_new_instance_method(_itkMeshIOBasePython.itkMeshIOBase_WriteCells)
    WritePointData = _swig_new_instance_method(_itkMeshIOBasePython.itkMeshIOBase_WritePointData)
    WriteCellData = _swig_new_instance_method(_itkMeshIOBasePython.itkMeshIOBase_WriteCellData)
    Write = _swig_new_instance_method(_itkMeshIOBasePython.itkMeshIOBase_Write)
    GetSupportedReadExtensions = _swig_new_instance_method(_itkMeshIOBasePython.itkMeshIOBase_GetSupportedReadExtensions)
    GetSupportedWriteExtensions = _swig_new_instance_method(_itkMeshIOBasePython.itkMeshIOBase_GetSupportedWriteExtensions)
    __swig_destroy__ = _itkMeshIOBasePython.delete_itkMeshIOBase
    cast = _swig_new_static_method(_itkMeshIOBasePython.itkMeshIOBase_cast)

# Register itkMeshIOBase in _itkMeshIOBasePython:
_itkMeshIOBasePython.itkMeshIOBase_swigregister(itkMeshIOBase)
itkMeshIOBase_cast = _itkMeshIOBasePython.itkMeshIOBase_cast



