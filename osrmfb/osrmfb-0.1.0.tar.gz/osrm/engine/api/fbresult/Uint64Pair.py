# automatically generated by the FlatBuffers compiler, do not modify

# namespace: fbresult

import flatbuffers
from flatbuffers.compat import import_numpy
np = import_numpy()

class Uint64Pair(object):
    __slots__ = ['_tab']

    # Uint64Pair
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # Uint64Pair
    def First(self): return self._tab.Get(flatbuffers.number_types.Uint64Flags, self._tab.Pos + flatbuffers.number_types.UOffsetTFlags.py_type(0))
    # Uint64Pair
    def Second(self): return self._tab.Get(flatbuffers.number_types.Uint64Flags, self._tab.Pos + flatbuffers.number_types.UOffsetTFlags.py_type(8))

def CreateUint64Pair(builder, first, second):
    builder.Prep(8, 16)
    builder.PrependUint64(second)
    builder.PrependUint64(first)
    return builder.Offset()
