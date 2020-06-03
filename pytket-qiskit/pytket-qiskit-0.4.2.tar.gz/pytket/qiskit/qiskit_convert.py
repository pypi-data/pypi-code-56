# Copyright 2019-2020 Cambridge Quantum Computing
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


"""Methods to allow conversion between Qiskit and pytket circuit classes
"""

from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit  # type: ignore
from qiskit.circuit import Instruction, Measure, Parameter, ParameterExpression, Barrier
import qiskit.circuit.library.standard_gates as qiskit_gates
from qiskit.extensions.unitary import UnitaryGate
from qiskit.providers import BaseBackend

from pytket.circuit import Circuit, OpType, Unitary2qBox, CircBox, UnitType, Node
from pytket.device import Device, GateError, GateErrorContainer
from pytket.routing import Architecture, FullyConnected
from pytket.utils.results import _reverse_bits_of_index
from math import pi
from typing import List, Dict, Union
import sympy

_known_qiskit_gate = {
    qiskit_gates.IGate: OpType.noop,
    qiskit_gates.XGate: OpType.X,
    qiskit_gates.YGate: OpType.Y,
    qiskit_gates.ZGate: OpType.Z,
    qiskit_gates.SGate: OpType.S,
    qiskit_gates.SdgGate: OpType.Sdg,
    qiskit_gates.TGate: OpType.T,
    qiskit_gates.TdgGate: OpType.Tdg,
    qiskit_gates.HGate: OpType.H,
    qiskit_gates.RXGate: OpType.Rx,
    qiskit_gates.RYGate: OpType.Ry,
    qiskit_gates.RZGate: OpType.Rz,
    qiskit_gates.U1Gate: OpType.U1,
    qiskit_gates.U2Gate: OpType.U2,
    qiskit_gates.U3Gate: OpType.U3,
    qiskit_gates.CXGate: OpType.CX,
    qiskit_gates.CYGate: OpType.CY,
    qiskit_gates.CZGate: OpType.CZ,
    qiskit_gates.CHGate: OpType.CH,
    qiskit_gates.SwapGate: OpType.SWAP,
    qiskit_gates.CCXGate: OpType.CCX,
    qiskit_gates.CSwapGate: OpType.CSWAP,
    qiskit_gates.CRZGate: OpType.CRz,
    qiskit_gates.CU1Gate: OpType.CU1,
    qiskit_gates.CU3Gate: OpType.CU3,
    Measure: OpType.Measure,
    UnitaryGate: OpType.Unitary2qBox,
    Barrier: OpType.Barrier,
    Instruction: OpType.CircBox,
}

_known_qiskit_gate_rev = {v: k for k, v in _known_qiskit_gate.items()}


class CircuitBuilder:
    def __init__(
        self, qregs: List[QuantumRegister], cregs: List[ClassicalRegister] = []
    ):
        self.qregs = qregs
        self.cregs = cregs
        self.tkc = Circuit()
        self.qregmap = {}
        for reg in qregs:
            tk_reg = self.tkc.add_q_register(reg.name, len(reg))
            self.qregmap.update({reg: tk_reg})
        self.cregmap = {}
        for reg in cregs:
            tk_reg = self.tkc.add_c_register(reg.name, len(reg))
            self.cregmap.update({reg: tk_reg})

    def circuit(self):
        return self.tkc

    def add_qiskit_data(self, data):
        for i, qargs, cargs in data:
            condition_kwargs = {}
            if i.condition is not None:
                cond_reg = self.cregmap[i.condition[0]]
                condition_kwargs = {
                    "condition_bits": [cond_reg[k] for k in range(len(cond_reg))],
                    "condition_value": _reverse_bits_of_index(
                        i.condition[1], len(cond_reg)
                    ),
                }
            optype = _known_qiskit_gate[type(i)]
            qubits = [self.qregmap[qbit.register][qbit.index] for qbit in qargs]
            bits = [self.cregmap[bit.register][bit.index] for bit in cargs]
            if optype == OpType.Unitary2qBox:
                u = i.to_matrix()
                ubox = Unitary2qBox(u)
                self.tkc.add_unitary2qbox(
                    ubox, qubits[0], qubits[1], **condition_kwargs
                )
            elif optype == OpType.Barrier:
                self.tkc.add_barrier(qubits)
            elif optype == OpType.CircBox:
                qregs = [QuantumRegister(i.num_qubits, "q")] if i.num_qubits > 0 else []
                cregs = (
                    [ClassicalRegister(i.num_clbits, "c")] if i.num_clbits > 0 else []
                )
                builder = CircuitBuilder(qregs, cregs)
                builder.add_qiskit_data(i.definition)
                cbox = CircBox(builder.circuit())
                self.tkc.add_circbox(cbox, qubits + bits, **condition_kwargs)
            else:
                params = [param_to_tk(p) for p in i.params]
                self.tkc.add_gate(optype, params, qubits + bits, **condition_kwargs)


def qiskit_to_tk(qcirc: QuantumCircuit) -> Circuit:
    """Convert a :py:class:`qiskit.QuantumCircuit` to a :py:class:`Circuit`.

    :param qcirc: A circuit to be converted
    :type qcirc: QuantumCircuit
    :return: The converted circuit
    :rtype: Circuit
    """
    builder = CircuitBuilder(qcirc.qregs, qcirc.cregs)
    builder.add_qiskit_data(qcirc.data)
    return builder.circuit()


def param_to_tk(p: Union[float, ParameterExpression]) -> sympy.Expr:
    if isinstance(p, float):
        return p / sympy.pi
    else:
        return p._symbol_expr / sympy.pi


def param_to_qiskit(
    p: sympy.Expr, symb_map: Dict[Parameter, sympy.Symbol]
) -> Union[float, ParameterExpression]:
    ppi = p * sympy.pi
    if len(ppi.free_symbols) == 0:
        return float(ppi.evalf())
    else:
        return ParameterExpression(symb_map, ppi)


def append_tk_command_to_qiskit(
    op, args, qcirc, qregmap, cregmap, symb_map
) -> Instruction:
    optype = op.type
    if optype == OpType.Measure:
        qubit = args[0]
        bit = args[1]
        qb = qregmap[qubit.reg_name][qubit.index[0]]
        b = cregmap[bit.reg_name][bit.index[0]]
        return qcirc.measure(qb, b)
    elif optype in [OpType.CircBox, OpType.ExpBox, OpType.PauliExpBox]:
        subcircuit = op.get_circuit()
        subqc = tk_to_qiskit(subcircuit)
        n_qb = subcircuit.n_qubits
        qargs = []
        cargs = []
        for a in args:
            if a.type == UnitType.qubit:
                qargs.append(qregmap[a.reg_name][a.index[0]])
            else:
                cargs.append(cregmap[a.reg_name][a.index[0]])
        return qcirc.append(subqc.to_instruction(), qargs, cargs)
    elif optype == OpType.Unitary2qBox:
        qargs = [qregmap[q.reg_name][q.index[0]] for q in args]
        u = op.get_matrix()
        g = UnitaryGate(u)
        return qcirc.append(g, qargs=qargs)
    elif optype == OpType.Barrier:
        qargs = [qregmap[q.reg_name][q.index[0]] for q in args]
        g = Barrier(len(args))
        return qcirc.append(g, qargs=qargs)
    elif optype == OpType.ConditionalGate:
        width = op.width
        regname = args[0].reg_name
        if len(cregmap[regname]) != width:
            raise NotImplementedError("OpenQASM conditions must be an entire register")
        for i, a in enumerate(args[:width]):
            if a.reg_name != regname:
                raise NotImplementedError(
                    "OpenQASM conditions can only use a single register"
                )
            if a.index != [i]:
                raise NotImplementedError(
                    "OpenQASM conditions must be an entire register in order"
                )
        instruction = append_tk_command_to_qiskit(
            op.op, args[width:], qcirc, qregmap, cregmap, symb_map
        )

        instruction.c_if(cregmap[regname], _reverse_bits_of_index(op.value, width))
    else:
        try:
            gatetype = _known_qiskit_gate_rev[optype]
        except KeyError as error:
            raise NotImplementedError(
                "Cannot convert tket Op to Qiskit gate: " + op.get_name()
            ) from error
        qargs = [qregmap[q.reg_name][q.index[0]] for q in args]
        params = [param_to_qiskit(p, symb_map) for p in op.params]
        g = gatetype(*params)
        return qcirc.append(g, qargs=qargs)


def tk_to_qiskit(tkcirc: Circuit) -> QuantumCircuit:
    """Convert back

    :param tkcirc: A circuit to be converted
    :type tkcirc: Circuit
    :return: The converted circuit
    :rtype: QuantumCircuit
    """
    tkc = tkcirc
    qcirc = QuantumCircuit()
    qreg_sizes: Dict[str, int] = {}
    for qb in tkc.qubits:
        if len(qb.index) != 1:
            raise NotImplementedError("Qiskit registers must use a single index")
        if (qb.reg_name not in qreg_sizes) or (qb.index[0] >= qreg_sizes[qb.reg_name]):
            qreg_sizes.update({qb.reg_name: qb.index[0] + 1})
    creg_sizes: Dict[str, int] = {}
    for b in tkc.bits:
        if len(b.index) != 1:
            raise NotImplementedError("Qiskit registers must use a single index")
        if (b.reg_name not in creg_sizes) or (b.index[0] >= creg_sizes[b.reg_name]):
            creg_sizes.update({b.reg_name: b.index[0] + 1})
    qregmap = {}
    for reg_name, size in qreg_sizes.items():
        qis_reg = QuantumRegister(size, reg_name)
        qregmap.update({reg_name: qis_reg})
        qcirc.add_register(qis_reg)
    cregmap = {}
    for reg_name, size in creg_sizes.items():
        qis_reg = ClassicalRegister(size, reg_name)
        cregmap.update({reg_name: qis_reg})
        qcirc.add_register(qis_reg)
    symb_map = {Parameter(str(s)): s for s in tkc.free_symbols()}
    for command in tkc:
        append_tk_command_to_qiskit(
            command.op, command.args, qcirc, qregmap, cregmap, symb_map
        )
    return qcirc


def process_device(backend: BaseBackend) -> Device:
    """Convert a :py:class:`qiskit.BaseBackend` to a :py:class:`Device`.

    :param backend: A backend to be converted
    :type backend: BaseBackend
    :return: A :py:class:`Device` containing device information
    :rtype: Device
    """
    properties = backend.properties()
    gate_str_2_optype = {
        "u1": OpType.U1,
        "u2": OpType.U2,
        "u3": OpType.U3,
        "cx": OpType.CX,
        "id": OpType.noop,
    }

    def return_value_if_found(iterator, name):
        try:
            first_found = next(filter(lambda item: item.name == name, iterator))
        except StopIteration:
            return None
        if hasattr(first_found, "value"):
            return first_found.value
        return None

    config = backend.configuration()
    coupling_map = config.coupling_map
    n_qubits = config.n_qubits
    if coupling_map is None:
        # Assume full connectivity
        arc = FullyConnected(n_qubits)
        link_ers_dict = {}
    else:
        arc = Architecture(coupling_map)
        link_ers_dict = {
            tuple(pair): GateErrorContainer({OpType.CX}) for pair in coupling_map
        }

    node_ers_dict = {}
    supported_single_optypes = {OpType.U1, OpType.U2, OpType.U3, OpType.noop}

    if properties is not None:
        for index, qubit_info in enumerate(properties.qubits):
            error_cont = GateErrorContainer(supported_single_optypes)
            error_cont.add_readout(return_value_if_found(qubit_info, "readout_error"))
            error_cont.add_t1_time(return_value_if_found(qubit_info, "T1"))
            error_cont.add_t2_time(return_value_if_found(qubit_info, "T2"))
            error_cont.add_frequency(return_value_if_found(qubit_info, "frequency"))
            node_ers_dict[index] = error_cont

        for gate in properties.gates:
            name = gate.gate
            if name in gate_str_2_optype:
                optype = gate_str_2_optype[name]
                qubits = gate.qubits
                gate_error = return_value_if_found(gate.parameters, "gate_error")
                gate_error = gate_error if gate_error else 0.0
                gate_length = return_value_if_found(gate.parameters, "gate_length")
                gate_length = gate_length if gate_length else 0.0
                # add gate fidelities to their relevant lists
                if len(qubits) == 1:
                    node_ers_dict[qubits[0]].add_error(
                        (optype, GateError(gate_error, gate_length))
                    )
                elif len(qubits) == 2:
                    link_ers_dict[tuple(qubits)].add_error(
                        (optype, GateError(gate_error, gate_length))
                    )
                    opposite_link = tuple(qubits[::-1])
                    if opposite_link not in coupling_map:
                        # to simulate a worse reverse direction square the fidelity
                        link_ers_dict[opposite_link] = GateErrorContainer({OpType.CX})
                        link_ers_dict[opposite_link].add_error(
                            (optype, GateError(2 * gate_error, gate_length))
                        )

    # convert qubits to architecture Nodes
    node_ers_dict = {Node(q_index): ers for q_index, ers in node_ers_dict.items()}
    link_ers_dict = {
        (Node(q_indices[0]), Node(q_indices[1])): ers
        for q_indices, ers in link_ers_dict.items()
    }

    device = Device(node_ers_dict, link_ers_dict, arc)
    return device
