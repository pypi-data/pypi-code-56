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

from abc import abstractmethod
from typing import (
    TYPE_CHECKING,
    Dict,
    Iterable,
    List,
    MutableMapping,
    Optional,
    Tuple,
    Union,
)
from uuid import uuid4

import numpy as np
from qsharp import compile as qscompile
from pytket.backends import (
    Backend,
    CircuitNotRunError,
    CircuitStatus,
    ResultHandle,
    StatusEnum,
)
from pytket.backends.backend import KwargTypes
from pytket.backends.resulthandle import _ResultIdTuple
from pytket.backends.backendresult import BackendResult
from pytket.circuit import BasisOrder, Circuit, OpType
from pytket.passes import BasePass, RebaseCustom
from pytket.predicates import (
    GateSetPredicate,
    NoClassicalControlPredicate,
    NoFastFeedforwardPredicate,
    Predicate,
)
from pytket.qsharp import tk_to_qsharp
from pytket.utils.results import counts_from_shot_table

if TYPE_CHECKING:
    from qsharp.loader import QSharpCallable
    from pytket.device import Device


def _from_tk1(a: float, b: float, c: float) -> Circuit:
    circ = Circuit(1)
    circ.Rz(c, 0)
    circ.Rx(b, 0)
    circ.Rz(a, 0)
    return circ


def qs_predicates() -> List[Predicate]:
    return [
        NoClassicalControlPredicate(),
        NoFastFeedforwardPredicate(),
        GateSetPredicate(
            {
                OpType.CCX,
                OpType.CX,
                OpType.PauliExpBox,
                OpType.H,
                OpType.noop,
                OpType.Rx,
                OpType.Ry,
                OpType.Rz,
                OpType.S,
                OpType.SWAP,
                OpType.T,
                OpType.X,
                OpType.Y,
                OpType.Z,
                OpType.CnX,
            }
        ),
    ]


def qs_compilation_pass() -> BasePass:
    return RebaseCustom(
        {OpType.CX, OpType.CCX, OpType.PauliExpBox, OpType.SWAP, OpType.CnX},  # multiqs
        Circuit(),  # cx_replacement (irrelevant)
        {
            OpType.H,
            OpType.Rx,
            OpType.Ry,
            OpType.Rz,
            OpType.S,
            OpType.T,
            OpType.X,
            OpType.Y,
            OpType.Z,
        },  # singleqs
        _from_tk1,
    )  # tk1_replacement


class _QsharpBaseBackend(Backend):
    """Shared base backend for Qsharp backends."""

    _persistent_handles = False

    @property
    def required_predicates(self) -> List[Predicate]:
        return qs_predicates()

    @property
    def default_compilation_pass(self) -> BasePass:
        return qs_compilation_pass()

    @property
    def _result_id_type(self) -> _ResultIdTuple:
        return (str,)

    @property
    def device(self) -> Optional["Device"]:
        return None

    def circuit_status(self, handle: ResultHandle) -> CircuitStatus:
        if handle in self._cache:
            return CircuitStatus(StatusEnum.COMPLETED)
        raise CircuitNotRunError(handle)

    @abstractmethod
    def _calculate_results(
        self, qscall: "QSharpCallable", n_shots: Optional[int] = None
    ) -> Union[BackendResult, "MutableMapping"]:
        raise NotImplementedError()

    def process_circuits(
        self,
        circuits: Iterable[Circuit],
        n_shots: Optional[int] = None,
        valid_check: bool = True,
        **kwargs: KwargTypes,
    ) -> List[ResultHandle]:
        """
        See :py:meth:`pytket.backends.Backend.process_circuits`.
        Supported kwargs: none.
        """
        if valid_check:
            self._check_all_circuits(circuits)
        handles = []
        for c in circuits:
            qs = tk_to_qsharp(c)
            qc = qscompile(qs)
            results = self._calculate_results(qc, n_shots)
            handle = ResultHandle(str(uuid4()))
            key = "result" if isinstance(results, BackendResult) else "resource"
            self._cache.update({handle: {key: results}})
            handles.append(handle)
        return handles


class _QsharpSimBaseBackend(_QsharpBaseBackend):
    _supports_shots = True
    _supports_counts = True
