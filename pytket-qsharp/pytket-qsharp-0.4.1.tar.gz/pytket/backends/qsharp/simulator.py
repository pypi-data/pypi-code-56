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

from .common import _QsharpSimBaseBackend, BackendResult
from pytket.utils.outcomearray import OutcomeArray

if TYPE_CHECKING:
    from qsharp.loader import QSharpCallable


class QsharpSimulatorBackend(_QsharpSimBaseBackend):
    """ Backend for simulating a circuit using the QDK. """

    _supports_shots = True
    _supports_counts = True

    def _calculate_results(
        self, qscall: "QSharpCallable", n_shots: Optional[int] = None
    ) -> BackendResult:
        if n_shots:
            shots = OutcomeArray.from_readouts(
                [qscall.simulate() for _ in range(n_shots)]
            )
            return BackendResult(shots=shots)
        raise ValueError("Parameter n_shots is required")
