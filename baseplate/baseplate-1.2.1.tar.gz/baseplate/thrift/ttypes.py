#
# Autogenerated by Thrift Compiler (0.12.1)
#
# DO NOT EDIT UNLESS YOU ARE SURE THAT YOU KNOW WHAT YOU ARE DOING
#
#  options string: py:slots
#
import sys

from thrift.protocol.TProtocol import TProtocolException
from thrift.Thrift import TApplicationException
from thrift.Thrift import TException
from thrift.Thrift import TFrozenDict
from thrift.Thrift import TMessageType
from thrift.Thrift import TType
from thrift.transport import TTransport
from thrift.TRecursive import fix_spec

all_structs = []


class Loid(object):
    """
    The components of the Reddit LoID cookie that we want to propogate between
    services.

    This model is a component of the "Edge-Request" header.  You should not need to
    interact with this model directly, but rather through the EdgeRequestContext
    interface provided by baseplate.


    Attributes:
     - id: The ID of the LoID cookie.

     - created_ms: The time when the LoID cookie was created in epoch milliseconds.


    """

    __slots__ = ("id", "created_ms")

    def __init__(self, id=None, created_ms=None):
        self.id = id
        self.created_ms = created_ms

    def read(self, iprot):
        if (
            iprot._fast_decode is not None
            and isinstance(iprot.trans, TTransport.CReadableTransport)
            and self.thrift_spec is not None
        ):
            iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
            return
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 1:
                if ftype == TType.STRING:
                    self.id = (
                        iprot.readString().decode("utf-8")
                        if sys.version_info[0] == 2
                        else iprot.readString()
                    )
                else:
                    iprot.skip(ftype)
            elif fid == 2:
                if ftype == TType.I64:
                    self.created_ms = iprot.readI64()
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None and self.thrift_spec is not None:
            oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
            return
        oprot.writeStructBegin("Loid")
        if self.id is not None:
            oprot.writeFieldBegin("id", TType.STRING, 1)
            oprot.writeString(self.id.encode("utf-8") if sys.version_info[0] == 2 else self.id)
            oprot.writeFieldEnd()
        if self.created_ms is not None:
            oprot.writeFieldBegin("created_ms", TType.I64, 2)
            oprot.writeI64(self.created_ms)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        return

    def __repr__(self):
        L = ["%s=%r" % (key, getattr(self, key)) for key in self.__slots__]
        return "%s(%s)" % (self.__class__.__name__, ", ".join(L))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        for attr in self.__slots__:
            my_val = getattr(self, attr)
            other_val = getattr(other, attr)
            if my_val != other_val:
                return False
        return True

    def __ne__(self, other):
        return not (self == other)


class Session(object):
    """
    The components of the Reddit Session tracker cookie that we want to
    propogate between services.

    This model is a component of the "Edge-Request" header.  You should not need to
    interact with this model directly, but rather through the EdgeRequestContext
    interface provided by baseplate.


    Attributes:
     - id: The ID of the Session tracker cookie.


    """

    __slots__ = ("id",)

    def __init__(self, id=None):
        self.id = id

    def read(self, iprot):
        if (
            iprot._fast_decode is not None
            and isinstance(iprot.trans, TTransport.CReadableTransport)
            and self.thrift_spec is not None
        ):
            iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
            return
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 1:
                if ftype == TType.STRING:
                    self.id = (
                        iprot.readString().decode("utf-8")
                        if sys.version_info[0] == 2
                        else iprot.readString()
                    )
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None and self.thrift_spec is not None:
            oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
            return
        oprot.writeStructBegin("Session")
        if self.id is not None:
            oprot.writeFieldBegin("id", TType.STRING, 1)
            oprot.writeString(self.id.encode("utf-8") if sys.version_info[0] == 2 else self.id)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        return

    def __repr__(self):
        L = ["%s=%r" % (key, getattr(self, key)) for key in self.__slots__]
        return "%s(%s)" % (self.__class__.__name__, ", ".join(L))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        for attr in self.__slots__:
            my_val = getattr(self, attr)
            other_val = getattr(other, attr)
            if my_val != other_val:
                return False
        return True

    def __ne__(self, other):
        return not (self == other)


class Device(object):
    """
    The components of the device making a request to our services that we want to
    propogate between services.

    This model is a component of the "Edge-Request" header.  You should not need to
    interact with this model directly, but rather through the EdgeRequestContext
    interface provided by baseplate.


    Attributes:
     - id: The ID of the device.


    """

    __slots__ = ("id",)

    def __init__(self, id=None):
        self.id = id

    def read(self, iprot):
        if (
            iprot._fast_decode is not None
            and isinstance(iprot.trans, TTransport.CReadableTransport)
            and self.thrift_spec is not None
        ):
            iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
            return
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 1:
                if ftype == TType.STRING:
                    self.id = (
                        iprot.readString().decode("utf-8")
                        if sys.version_info[0] == 2
                        else iprot.readString()
                    )
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None and self.thrift_spec is not None:
            oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
            return
        oprot.writeStructBegin("Device")
        if self.id is not None:
            oprot.writeFieldBegin("id", TType.STRING, 1)
            oprot.writeString(self.id.encode("utf-8") if sys.version_info[0] == 2 else self.id)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        return

    def __repr__(self):
        L = ["%s=%r" % (key, getattr(self, key)) for key in self.__slots__]
        return "%s(%s)" % (self.__class__.__name__, ", ".join(L))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        for attr in self.__slots__:
            my_val = getattr(self, attr)
            other_val = getattr(other, attr)
            if my_val != other_val:
                return False
        return True

    def __ne__(self, other):
        return not (self == other)


class Request(object):
    """
    Container model for the Edge-Request context header.

    Baseplate will automatically parse this from the "Edge-Request" header and
    provides an interface that wraps this Thrift model.  You should not need to
    interact with this model directly, but rather through the EdgeRequestContext
    interface provided by baseplate.


    Attributes:
     - loid
     - session
     - authentication_token
     - device

    """

    __slots__ = ("loid", "session", "authentication_token", "device")

    def __init__(self, loid=None, session=None, authentication_token=None, device=None):
        self.loid = loid
        self.session = session
        self.authentication_token = authentication_token
        self.device = device

    def read(self, iprot):
        if (
            iprot._fast_decode is not None
            and isinstance(iprot.trans, TTransport.CReadableTransport)
            and self.thrift_spec is not None
        ):
            iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
            return
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 1:
                if ftype == TType.STRUCT:
                    self.loid = Loid()
                    self.loid.read(iprot)
                else:
                    iprot.skip(ftype)
            elif fid == 2:
                if ftype == TType.STRUCT:
                    self.session = Session()
                    self.session.read(iprot)
                else:
                    iprot.skip(ftype)
            elif fid == 3:
                if ftype == TType.STRING:
                    self.authentication_token = (
                        iprot.readString().decode("utf-8")
                        if sys.version_info[0] == 2
                        else iprot.readString()
                    )
                else:
                    iprot.skip(ftype)
            elif fid == 4:
                if ftype == TType.STRUCT:
                    self.device = Device()
                    self.device.read(iprot)
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None and self.thrift_spec is not None:
            oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
            return
        oprot.writeStructBegin("Request")
        if self.loid is not None:
            oprot.writeFieldBegin("loid", TType.STRUCT, 1)
            self.loid.write(oprot)
            oprot.writeFieldEnd()
        if self.session is not None:
            oprot.writeFieldBegin("session", TType.STRUCT, 2)
            self.session.write(oprot)
            oprot.writeFieldEnd()
        if self.authentication_token is not None:
            oprot.writeFieldBegin("authentication_token", TType.STRING, 3)
            oprot.writeString(
                self.authentication_token.encode("utf-8")
                if sys.version_info[0] == 2
                else self.authentication_token
            )
            oprot.writeFieldEnd()
        if self.device is not None:
            oprot.writeFieldBegin("device", TType.STRUCT, 4)
            self.device.write(oprot)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        return

    def __repr__(self):
        L = ["%s=%r" % (key, getattr(self, key)) for key in self.__slots__]
        return "%s(%s)" % (self.__class__.__name__, ", ".join(L))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        for attr in self.__slots__:
            my_val = getattr(self, attr)
            other_val = getattr(other, attr)
            if my_val != other_val:
                return False
        return True

    def __ne__(self, other):
        return not (self == other)


all_structs.append(Loid)
Loid.thrift_spec = (
    None,  # 0
    (1, TType.STRING, "id", "UTF8", None),  # 1
    (2, TType.I64, "created_ms", None, None),  # 2
)
all_structs.append(Session)
Session.thrift_spec = (None, (1, TType.STRING, "id", "UTF8", None))  # 0  # 1
all_structs.append(Device)
Device.thrift_spec = (None, (1, TType.STRING, "id", "UTF8", None))  # 0  # 1
all_structs.append(Request)
Request.thrift_spec = (
    None,  # 0
    (1, TType.STRUCT, "loid", [Loid, None], None),  # 1
    (2, TType.STRUCT, "session", [Session, None], None),  # 2
    (3, TType.STRING, "authentication_token", "UTF8", None),  # 3
    (4, TType.STRUCT, "device", [Device, None], None),  # 4
)
fix_spec(all_structs)
del all_structs
