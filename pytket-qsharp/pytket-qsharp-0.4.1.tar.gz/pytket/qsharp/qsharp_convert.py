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

"""Methods to allow conversion from :math:`\\mathrm{t|ket}\\rangle` to Q#
"""

from pytket.circuit import Circuit, OpType
from pytket.pauli import Pauli
from typing import List
from math import pi

qs_pauli = {Pauli.I: "PauliI", Pauli.X: "PauliX", Pauli.Y: "PauliY", Pauli.Z: "PauliZ"}


def cmd_body(op, qbs):
    optype = op.type

    if optype == OpType.CCX:
        return "CCNOT(q[{}], q[{}], q[{}])".format(*qbs)
    elif optype == OpType.CX:
        return "CNOT(q[{}], q[{}])".format(*qbs)
    elif optype == OpType.PauliExpBox:
        paulis = op.get_paulis()
        theta = (-2 / pi) * op.get_phase()
        return "Exp([{}], {}, [{}])".format(
            ", ".join([qs_pauli[p] for p in paulis]),
            theta,
            ", ".join(["q[{}]".format(i) for i in qbs]),
        )
    elif optype == OpType.H:
        return "H(q[{}])".format(*qbs)
    elif optype == OpType.noop:
        pass
    elif optype == OpType.Rx:
        return "Rx({}, q[{}])".format(pi * op.params[0], qbs[0])
    elif optype == OpType.Ry:
        return "Ry({}, q[{}])".format(pi * op.params[0], qbs[0])
    elif optype == OpType.Rz:
        return "Rz({}, q[{}])".format(pi * op.params[0], qbs[0])
    elif optype == OpType.S:
        return "S(q[{}])".format(*qbs)
    elif optype == OpType.SWAP:
        return "SWAP(q[{}], q[{}])".format(*qbs)
    elif optype == OpType.T:
        return "T(q[{}])".format(*qbs)
    elif optype == OpType.X:
        return "X(q[{}])".format(*qbs)
    elif optype == OpType.Y:
        return "Y(q[{}])".format(*qbs)
    elif optype == OpType.Z:
        return "Z(q[{}])".format(*qbs)
    elif optype == OpType.CnX:
        return (
            "ApplyMultiControlledC("
            + ", ".join(
                [
                    "ApplyToFirstTwoQubitsCA(CNOT, _)",
                    "CCNOTop(CCNOT)",
                    "[{}]".format(", ".join(["q[{}]".format(i) for i in qbs[:-1]])),
                    "[{}]".format("q[{}]".format(qbs[-1])),
                ]
            )
            + ")"
        )
    else:
        raise RuntimeError("Unsupported operation {}".format(optype))


def main_body(c: Circuit) -> List[str]:
    lines = []
    for cmd in c:
        qbs = [qb.index[0] for qb in cmd.args]
        lines.append("        " + cmd_body(cmd.op, qbs) + ";")
    return lines


def operation_body(c: Circuit) -> List[str]:
    lines = []
    n_q = c.n_qubits
    lines.append("    mutable r = [" + ", ".join(["Zero"] * n_q) + "];")
    lines.append("    using (q = Qubit[{}]) {{".format(n_q))
    lines.append("        ResetAll(q);")
    lines.extend(main_body(c))
    lines.append("        set r = MultiM(q);")
    lines.append("        ResetAll(q);")
    lines.append("    }")
    lines.append("    return r;")
    return lines


def tk_to_qsharp(tkcirc: Circuit) -> str:
    """Convert a :math:`\\mathrm{t|ket}\\rangle` :py:class:`Circuit` to a Q# program.

    :param tkcirc: Circuit to be converted

    :return: Converted circuit
    """
    if tkcirc.is_symbolic():
        raise RuntimeError("Cannot convert symbolic circuit to Q#")

    lines = []
    lines.append("open Microsoft.Quantum.Intrinsic;")
    lines.append("open Microsoft.Quantum.Measurement;")
    lines.append("open Microsoft.Quantum.Canon;")
    lines.append("operation Circuit() : Result[] {")
    lines.extend(operation_body(tkcirc))
    lines.append("}")
    return "\n".join(lines)
