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

from typing import TYPE_CHECKING, MutableMapping, Optional, Union

import numpy as np
from pytket.circuit import Circuit, OpType
from pytket.passes import BasePass, RebaseCustom

from .common import _QsharpSimBaseBackend, BackendResult
from pytket.utils.outcomearray import OutcomeArray

if TYPE_CHECKING:
    from qsharp.loader import QSharpCallable


def is_approx_0_mod_2(x, tol=1e-10):
    x %= 2  # --> [0,2)
    return min(x, 2 - x) < tol


def toffoli_from_tk1(a: float, b: float, c: float) -> Circuit:
    """ Only accept operations equivalent to I or X. """
    circ = Circuit(1)
    if is_approx_0_mod_2(b) and is_approx_0_mod_2(a + c):
        # identity
        pass
    elif is_approx_0_mod_2(b + 1) and is_approx_0_mod_2(a - c):
        # X
        circ.X()
    else:
        raise RuntimeError(
            "Cannot compile to Toffoli gate set: TK1({}, {}, {}) ∉ {{I, X}}".format(
                a, b, c
            )
        )
    return circ


class QsharpToffoliSimulatorBackend(_QsharpSimBaseBackend):
    """ Backend for simulating a Toffoli circuit using the QDK. """

    @property
    def default_compilation_pass(self) -> BasePass:
        return RebaseCustom(
            {OpType.CX, OpType.CCX, OpType.CnX, OpType.SWAP},  # multiqs
            Circuit(),  # cx_replacement (irrelevant)
            {OpType.X},  # singleqs
            toffoli_from_tk1,
        )  # tk1_replacement

    def _calculate_results(
        self, qscall: "QSharpCallable", n_shots: Optional[int] = None
    ) -> Union[BackendResult, "MutableMapping"]:
        if n_shots:
            shots = OutcomeArray.from_readouts(
                [qscall.toffoli_simulate() for _ in range(n_shots)]
            )
            return BackendResult(shots=shots)
        raise ValueError("Parameter n_shots is required")
