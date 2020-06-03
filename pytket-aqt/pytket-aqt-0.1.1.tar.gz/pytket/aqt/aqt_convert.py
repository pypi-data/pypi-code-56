# Copyright 2020 Cambridge Quantum Computing
#
# Licensed under a Non-Commercial Use Software Licence (the "Licence");
# you may not use this file except in compliance with the Licence.
# You may obtain a copy of the Licence in the LICENCE file accompanying
# these documents or at:
#
#     https://cqcl.github.io/pytket/build/html/licence.html
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the Licence is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the Licence for the specific language governing permissions and
# limitations under the Licence, but note it is strictly for non-commercial use.

""" Conversion from :math:`\\mathrm{t|ket}\\rangle` to AQT
"""

from pytket.circuit import Circuit, OpType
from pytket.passes import (
    RebaseCustom,
    EulerAngleReduction,
    FlattenRegisters,
    RemoveRedundancies,
    SequencePass,
)
from typing import List

# CX replacement
c_cx = Circuit(2)
c_cx.Ry(0.5, 0)
c_cx.add_gate(OpType.XXPhase, 0.5, [0, 1])
c_cx.Ry(1.0, 0).Rx(-0.5, 0).Ry(0.5, 0)
c_cx.Rx(-0.5, 1)

# TK1 replacement
c_tk1 = lambda a, b, c: Circuit(1).Rx(-0.5, 0).Ry(a, 0).Rx(b, 0).Ry(c, 0).Rx(0.5, 0)

# Flatten registers, rebase to the AQT gate set, and remove redundancies
aqt_pass = SequencePass(
    [
        FlattenRegisters(),
        RebaseCustom({OpType.XXPhase}, c_cx, {OpType.Rx, OpType.Ry}, c_tk1),
        RemoveRedundancies(),
        EulerAngleReduction(OpType.Ry, OpType.Rx),
    ]
)


def translate_aqt(circ: Circuit) -> List[List]:
    """ Convert a circuit in the AQT gate set to AQT list representation """
    gates = []
    for cmd in circ.get_commands():
        op = cmd.op
        optype = op.type
        # https://www.aqt.eu/aqt-gate-definitions/
        if optype == OpType.Rx:
            gates.append(["X", op.params[0], [q.index[0] for q in cmd.args]])
        elif optype == OpType.Ry:
            gates.append(["Y", op.params[0], [q.index[0] for q in cmd.args]])
        elif optype == OpType.XXPhase:
            gates.append(["MS", op.params[0], [q.index[0] for q in cmd.args]])
        else:
            assert optype in {OpType.Measure, OpType.Barrier}
    return gates


def tk_to_aqt(circ: Circuit) -> List[List]:
    """ Convert a circuit to AQT list representation """
    c = circ.copy()
    aqt_pass.apply(c)
    return translate_aqt(c)
