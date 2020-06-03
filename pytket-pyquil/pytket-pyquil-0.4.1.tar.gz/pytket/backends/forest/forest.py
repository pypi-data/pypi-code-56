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

from copy import copy
from typing import TYPE_CHECKING, Dict, Iterable, List, Optional, Tuple
from uuid import uuid4

import numpy as np
from pyquil import get_qc
from pyquil.api import QuantumComputer, WavefunctionSimulator
from pyquil.api._qam import QAM
from pyquil.gates import I
from pyquil.paulis import ID, PauliSum, PauliTerm
from pyquil.quilatom import Qubit as Qubit_

from pytket import Circuit, OpType, Qubit
from pytket.backends import (
    Backend,
    CircuitNotRunError,
    CircuitStatus,
    ResultHandle,
    StatusEnum,
)
from pytket.backends.backend import KwargTypes
from pytket.backends.backendresult import BackendResult
from pytket.backends.resulthandle import _ResultIdTuple
from pytket.device import Device
from pytket.passes import (
    BasePass,
    DecomposeSwapsToCXs,
    DelayMeasures,
    EulerAngleReduction,
    FullMappingPass,
    RebaseQuil,
    SequencePass,
    SynthesiseIBM,
)
from pytket.pauli import QubitPauliString
from pytket.predicates import (
    ConnectivityPredicate,
    GateSetPredicate,
    NoClassicalControlPredicate,
    NoFastFeedforwardPredicate,
    NoMidMeasurePredicate,
    Predicate,
)
from pytket.pyquil import process_device, tk_to_pyquil
from pytket.routing import NoiseAwarePlacement
from pytket.utils.operators import QubitPauliOperator
from pytket.utils.outcomearray import OutcomeArray

_STATUS_MAP = {
    "done": StatusEnum.COMPLETED,
    "running": StatusEnum.RUNNING,
    "loaded": StatusEnum.SUBMITTED,
    "connected": StatusEnum.SUBMITTED,
}


def _default_q_index(q: Qubit) -> int:
    if q.reg_name != "q" or len(q.index) != 1:
        raise ValueError("Non-default qubit register")
    return q.index[0]


class ForestBackend(Backend):
    _supports_shots = True
    _supports_counts = True
    _persistent_handles = True

    def __init__(self, qc_name: str, simulator: bool = True):
        """Backend for running circuits on a Rigetti QCS device or simulating with the QVM.

        :param qc_name: The name of the particular QuantumComputer to use. See the pyQuil docs for more details.
        :type qc_name: str
        :param simulator: Simulate the device with the QVM (True), or run on the QCS (False). Defaults to True.
        :type simulator: bool, optional
        """
        super().__init__()
        self._qc: QuantumComputer = get_qc(qc_name, as_qvm=simulator)
        self._device: Device = process_device(self._qc)

    @property
    def required_predicates(self) -> List[Predicate]:
        return [
            NoClassicalControlPredicate(),
            NoFastFeedforwardPredicate(),
            NoMidMeasurePredicate(),
            GateSetPredicate(
                {OpType.CZ, OpType.Rx, OpType.Rz, OpType.Measure, OpType.Barrier}
            ),
            ConnectivityPredicate(self._device),
        ]

    @property
    def default_compilation_pass(self) -> BasePass:
        passlist = [
            FullMappingPass(self._device, NoiseAwarePlacement(self._device)),
            DelayMeasures(),
            DecomposeSwapsToCXs(self._device),
            SynthesiseIBM(),
            RebaseQuil(),
            EulerAngleReduction(OpType.Rx, OpType.Rz),
        ]
        return SequencePass(passlist)

    @property
    def _result_id_type(self) -> _ResultIdTuple:
        return (int,)

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
        if not n_shots:
            raise ValueError("Parameter n_shots is required for ForestBackend")
        if valid_check:
            self._check_all_circuits(circuits)
        handle_list = []
        for circuit in circuits:
            p, bits = tk_to_pyquil(circuit, return_used_bits=True)
            p.wrap_in_numshots_loop(n_shots)
            ex = self._qc.compiler.native_quil_to_executable(p)
            qam = copy(self._qc.qam)
            qam.load(ex)
            qam.random_seed = kwargs.get("seed")
            qam.run()
            handle = ResultHandle(uuid4().int)
            self._cache[handle] = {"qam": qam, "c_bits": sorted(bits)}
            handle_list.append(handle)
        return handle_list

    def circuit_status(self, handle: ResultHandle) -> CircuitStatus:
        if handle in self._cache and "result" in self._cache[handle]:
            return CircuitStatus(StatusEnum.COMPLETED)
        if handle in self._cache:
            qamstatus = self._cache[handle]["qam"].status
            tkstat = _STATUS_MAP.get(qamstatus, StatusEnum.ERROR)
            return CircuitStatus(tkstat, qamstatus)
        raise CircuitNotRunError(handle)

    def get_result(self, handle: ResultHandle, **kwargs: KwargTypes) -> BackendResult:
        """
        See :py:meth:`pytket.backends.Backend.get_result`.
        Supported kwargs: none.
        """
        try:
            return super().get_result(handle)
        except CircuitNotRunError:
            if handle not in self._cache:
                raise CircuitNotRunError(handle)

            qam = self._cache[handle]["qam"]
            shots = qam.wait().read_memory(region_name="ro")
            shots = OutcomeArray.from_readouts(shots)
            res = BackendResult(shots=shots, c_bits=self._cache[handle]["c_bits"])
            self._cache[handle].update({"result": res})
            return res

    @property
    def device(self) -> Optional[Device]:
        return self._device


class ForestStateBackend(Backend):
    _supports_state = True
    _supports_expectation = True
    _persistent_handles = False

    def __init__(self):
        """Backend for running simulations on the Rigetti QVM Wavefunction Simulator.
        """
        super().__init__()
        self._sim = WavefunctionSimulator()

    @property
    def required_predicates(self) -> List[Predicate]:
        return [
            NoClassicalControlPredicate(),
            NoFastFeedforwardPredicate(),
            GateSetPredicate(
                {
                    OpType.X,
                    OpType.Y,
                    OpType.Z,
                    OpType.H,
                    OpType.S,
                    OpType.T,
                    OpType.Rx,
                    OpType.Ry,
                    OpType.Rz,
                    OpType.CZ,
                    OpType.CX,
                    OpType.CCX,
                    OpType.CU1,
                    OpType.U1,
                    OpType.SWAP,
                }
            ),
        ]

    @property
    def default_compilation_pass(self) -> BasePass:
        return RebaseQuil()

    @property
    def _result_id_type(self) -> _ResultIdTuple:
        return (int,)

    def process_circuits(
        self,
        circuits: Iterable[Circuit],
        n_shots: Optional[int] = None,
        valid_check: bool = True,
        **kwargs: KwargTypes,
    ) -> List[ResultHandle]:
        handle_list = []
        if valid_check:
            self._check_all_circuits(circuits)
        for circuit in circuits:
            p = tk_to_pyquil(circuit)
            for qb in circuit.qubits:
                # Qubits with no gates will not be included in the Program
                # Add identities to ensure all qubits are present and dimension
                # is as expected
                p += I(Qubit_(qb.index[0]))
            handle = ResultHandle(uuid4().int)
            state = np.asarray(self._sim.wavefunction(p).amplitudes)
            implicit_perm = circuit.implicit_qubit_permutation()
            res_qubits = [
                implicit_perm[qb] for qb in sorted(circuit.qubits, reverse=True)
            ]
            res = BackendResult(q_bits=res_qubits, state=state)
            self._cache[handle] = {"result": res}
            handle_list.append(handle)
        return handle_list

    def circuit_status(self, handle: ResultHandle) -> CircuitStatus:
        if handle in self._cache:
            return CircuitStatus(StatusEnum.COMPLETED)
        raise CircuitNotRunError(handle)

    @property
    def device(self) -> Optional[Device]:
        return None

    def _gen_PauliTerm(self, term: QubitPauliString, coeff: complex = 1.0) -> PauliTerm:
        pauli_term = ID() * coeff
        for q, p in term.map.items():
            pauli_term *= PauliTerm(p.name, _default_q_index(q))
        return pauli_term

    def get_pauli_expectation_value(
        self, state_circuit: Circuit, pauli: QubitPauliString
    ) -> complex:
        """Calculates the expectation value of the given circuit using the built-in QVM functionality

        :param state_circuit: Circuit that generates the desired state :math:`\\left|\\psi\\right>`.
        :type state_circuit: Circuit
        :param pauli: Pauli operator
        :type pauli: QubitPauliString
        :return: :math:`\\left<\\psi | P | \\psi \\right>`
        :rtype: complex
        """
        prog = tk_to_pyquil(state_circuit)
        pauli_term = self._gen_PauliTerm(pauli)
        return self._sim.expectation(prog, [pauli_term])

    def get_operator_expectation_value(
        self, state_circuit: Circuit, operator: QubitPauliOperator
    ) -> complex:
        """Calculates the expectation value of the given circuit with respect to the operator using the built-in QVM functionality

        :param state_circuit: Circuit that generates the desired state :math:`\\left|\\psi\\right>`.
        :type state_circuit: Circuit
        :param operator: Operator :math:`H`.
        :type operator: QubitPauliOperator
        :return: :math:`\\left<\\psi | H | \\psi \\right>`
        :rtype: complex
        """
        prog = tk_to_pyquil(state_circuit)
        pauli_sum = PauliSum(
            [self._gen_PauliTerm(term, coeff) for term, coeff in operator._dict.items()]
        )
        return self._sim.expectation(prog, pauli_sum)
