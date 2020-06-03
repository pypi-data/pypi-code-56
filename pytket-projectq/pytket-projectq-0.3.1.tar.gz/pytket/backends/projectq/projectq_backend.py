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

"""Methods to allow t|ket> circuits to be ran on ProjectQ simulator
"""
from copy import copy
from typing import TYPE_CHECKING, Dict, Iterable, List, Optional, Tuple, Union
from uuid import uuid4

import numpy as np
import projectq
from projectq import MainEngine
from projectq.backends import Simulator
from projectq.cengines import ForwarderEngine
from projectq.ops import All, Measure
from pytket import Circuit, OpType
from pytket.circuit import BasisOrder, Qubit
from pytket.backends import (
    Backend,
    CircuitNotRunError,
    ResultHandle,
    CircuitStatus,
    StatusEnum,
)
from pytket.backends.resulthandle import _ResultIdTuple
from pytket.backends.backendresult import BackendResult
from pytket.passes import BasePass, RebaseProjectQ
from pytket.predicates import (
    GateSetPredicate,
    NoClassicalControlPredicate,
    NoFastFeedforwardPredicate,
    Predicate,
)
from pytket.projectq import tk_to_projectq
from pytket.utils.operators import QubitPauliOperator
from pytket.utils.results import KwargTypes

if TYPE_CHECKING:
    from pytket.device import Device


def _default_q_index(q: Qubit) -> int:
    if q.reg_name != "q" or len(q.index) != 1:
        raise ValueError("Non-default qubit register")
    return q.index[0]


class ProjectQBackend(Backend):
    """Backend for running statevector simulations on the ProjectQ simulator.
    """

    _supports_state = True
    _supports_expectation = True
    _expectation_allows_nonhermitian = False
    _persistent_handles = False

    @property
    def _result_id_type(self) -> _ResultIdTuple:
        return (str,)

    @property
    def device(self) -> "Optional[Device]":
        return None

    @property
    def required_predicates(self) -> List[Predicate]:
        return [
            NoClassicalControlPredicate(),
            NoFastFeedforwardPredicate(),
            GateSetPredicate(
                {
                    OpType.SWAP,
                    OpType.CRz,
                    OpType.CX,
                    OpType.CZ,
                    OpType.H,
                    OpType.X,
                    OpType.Y,
                    OpType.Z,
                    OpType.S,
                    OpType.T,
                    OpType.V,
                    OpType.Rx,
                    OpType.Ry,
                    OpType.Rz,
                    OpType.Measure,
                }
            ),
        ]

    @property
    def default_compilation_pass(self) -> BasePass:
        return RebaseProjectQ()

    def process_circuits(
        self,
        circuits: Iterable[Circuit],
        n_shots: Optional[int] = None,
        valid_check: bool = True,
        **kwargs: KwargTypes,
    ) -> List[ResultHandle]:
        """
        See :py:meth:`pytket.backends.Backend.process_circuits`.
        Supported kwargs: `seed`.
        """
        circuit_list = list(circuits)
        if valid_check:
            self._check_all_circuits(circuit_list)

        handle_list = []
        for circuit in circuit_list:
            measures = [-1] * len(circuit.bits)
            for com in circuit:
                if com.op.type == OpType.Measure:
                    measures[com.args[1].index[0]] = com.args[0].index[0]
            sim = Simulator(rnd_seed=kwargs.get("seed"))
            fwd = ForwarderEngine(sim)
            eng = MainEngine(backend=sim, engine_list=[fwd])
            qureg = eng.allocate_qureg(circuit.n_qubits)
            tk_to_projectq(eng, qureg, circuit, True)
            eng.flush()
            state = copy(
                eng.backend.cheat()[1]
            )  # `cheat()` returns tuple:(a dictionary of qubit indices, statevector)
            All(Measure) | qureg
            handle = ResultHandle(str(uuid4()))
            implicit_perm = circuit.implicit_qubit_permutation()
            # reverse qubits as projectq state is dlo
            res_qubits = [
                implicit_perm[qb] for qb in sorted(circuit.qubits, reverse=True)
            ]
            self._cache[handle] = {
                "result": BackendResult(
                    q_bits=res_qubits, state=np.array(state, dtype=np.complex)
                )
            }
            handle_list.append(handle)
        return handle_list

    def circuit_status(self, handle: ResultHandle) -> CircuitStatus:
        if handle in self._cache:
            return CircuitStatus(StatusEnum.COMPLETED)
        raise CircuitNotRunError(handle)

    def _expectation_value(
        self,
        circuit: Circuit,
        hamiltonian: projectq.ops.QubitOperator,
        valid_check: bool = True,
    ) -> complex:
        if valid_check and not self.valid_circuit(circuit):
            raise ValueError(
                "Circuits do not satisfy all required predicates for this backend"
            )
        sim = Simulator()
        fwd = ForwarderEngine(sim)
        eng = MainEngine(backend=sim, engine_list=[fwd])
        qureg = eng.allocate_qureg(circuit.n_qubits)
        tk_to_projectq(eng, qureg, circuit)
        eng.flush()
        energy = eng.backend.get_expectation_value(hamiltonian, qureg)
        All(Measure) | qureg
        return energy

    def get_pauli_expectation_value(
        self,
        state_circuit: Circuit,
        pauli: Iterable[Tuple[int, str]],
        valid_check: bool = True,
    ) -> complex:
        """Calculates the expectation value of the given circuit using the built-in ProjectQ functionality

        :param state_circuit: Circuit that generates the desired state :math:`\\left|\\psi\\right>`.
        :type state_circuit: Circuit
        :param pauli: Sparse Pauli operator :math:`P` [p1, p2, p3, ...] where each pi = (q, s) with qubit index q and Pauli s ("I", "X", "Y", "Z").
        :type pauli: Iterable[Tuple[int,str]]
        :param valid_check: Explicitly check that the circuit satisfies all required predicates to run on the backend. Defaults to True
        :type valid_check: bool, optional
        :return: :math:`\\left<\\psi | P | \\psi \\right>`
        :rtype: complex
        """
        return self._expectation_value(
            state_circuit, projectq.ops.QubitOperator(tuple(pauli)), valid_check
        )

    def get_operator_expectation_value(
        self,
        state_circuit: Circuit,
        operator: QubitPauliOperator,
        valid_check: bool = True,
    ) -> complex:
        """Calculates the expectation value of the given circuit with respect to the operator using the built-in ProjectQ functionality

        :param state_circuit: Circuit that generates the desired state :math:`\\left|\\psi\\right>`.
        :type state_circuit: Circuit
        :param operator: Operator :math:`H`. Must be Hermitian.
        :type operator: QubitPauliOperator
        :param valid_check: Explicitly check that the circuit satisfies all required predicates to run on the backend. Defaults to True
        :type valid_check: bool, optional
        :return: :math:`\\left<\\psi | H | \\psi \\right>`
        :rtype: complex
        """
        ham = projectq.ops.QubitOperator()
        for term, coeff in operator._dict.items():
            if type(coeff) is complex and abs(coeff.imag) > 1e-12:
                raise ValueError(
                    "Operator is not Hermitian and cannot be converted to `projectq.ops.QubitOperator`."
                )
            ham += projectq.ops.QubitOperator(
                tuple((_default_q_index(q), p.name) for q, p in term.map.items()),
                float(coeff),
            )
        return self._expectation_value(state_circuit, ham, valid_check)
