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

import json
import time
from ast import literal_eval
from typing import Iterable, List, Optional, Tuple

import numpy as np
from requests import put
from pytket.aqt.aqt_convert import aqt_pass, translate_aqt
from pytket.backends import Backend, CircuitStatus, ResultHandle, StatusEnum
from pytket.backends.backend import KwargTypes
from pytket.backends.backendresult import BackendResult
from pytket.backends.resulthandle import _ResultIdTuple
from pytket.backends.backend_exceptions import CircuitNotRunError
from pytket.circuit import Circuit, OpType
from pytket.device import Device
from pytket.passes import BasePass, SequencePass, SynthesiseIBM
from pytket.predicates import (
    DefaultRegisterPredicate,
    GateSetPredicate,
    MaxNQubitsPredicate,
    NoClassicalControlPredicate,
    NoFastFeedforwardPredicate,
    Predicate,
)
from pytket.routing import FullyConnected
from pytket.utils.outcomearray import OutcomeArray

AQT_URL_PREFIX = "https://gateway.aqt.eu/marmot/"

AQT_DEVICE_QC = "lint"
AQT_DEVICE_SIM = "sim"
AQT_DEVICE_NOISY_SIM = "sim/noise-model-1"

_DEBUG_HANDLE_PREFIX = "_MACHINE_DEBUG_"

# Hard-coded for now as there is no API to retrieve these.
# All devices are fully connected.
device_info = {
    AQT_DEVICE_QC: {"max_n_qubits": 4},
    AQT_DEVICE_SIM: {"max_n_qubits": 10},
    AQT_DEVICE_NOISY_SIM: {"max_n_qubits": 10},
}


AQTResult = Tuple[int, List[int]]  # (n_qubits, list of readouts)

# TODO add more
_STATUS_MAP = {
    "finished": StatusEnum.COMPLETED,
    "error": StatusEnum.ERROR,
    "queued": StatusEnum.QUEUED,
}


class AQTBackend(Backend):
    """
    Interface to an AQT device or simulator.
    """

    _supports_shots = True
    _supports_counts = True
    _persistent_handles = True

    def __init__(
        self, access_token: str, device_name: str = AQT_DEVICE_SIM, label: str = ""
    ):
        """
        Construct a new AQT backend.

        :param      access_token: AQT access token
        :type       access_token: string
        :param      device_name:  device name (suffix of URL, e.g. "sim/noise-model-1")
        :type       device_name:  string
        :param      label:        label to apply to submitted jobs
        :type       label:        string
        """
        super().__init__()
        self._url = AQT_URL_PREFIX + device_name
        self._label = label
        self._header = {"Ocp-Apim-Subscription-Key": access_token, "SDK": "pytket"}
        self._max_n_qubits = (
            device_info[device_name]["max_n_qubits"]
            if device_name in device_info
            else None
        )
        self._device = (
            Device(FullyConnected(self._max_n_qubits)) if self._max_n_qubits else None
        )
        self._MACHINE_DEBUG = False

    @property
    def device(self) -> Optional[Device]:
        return self._device

    @property
    def required_predicates(self) -> List[Predicate]:
        preds = [
            DefaultRegisterPredicate(),
            NoClassicalControlPredicate(),
            NoFastFeedforwardPredicate(),
            GateSetPredicate(
                {OpType.Rx, OpType.Ry, OpType.XXPhase, OpType.Measure, OpType.Barrier}
            ),
        ]
        if self._max_n_qubits is not None:
            preds.append(MaxNQubitsPredicate(self._max_n_qubits))
        return preds

    @property
    def default_compilation_pass(self) -> BasePass:
        return SequencePass([SynthesiseIBM(), aqt_pass])

    @property
    def _result_id_type(self) -> _ResultIdTuple:
        return (str,)

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
        if not n_shots:
            raise ValueError("Parameter n_shots is required")

        if valid_check:
            self._check_all_circuits(circuits)
        handles = []
        for c in circuits:
            aqt_circ = translate_aqt(c)
            if self._MACHINE_DEBUG:
                handles.append(
                    ResultHandle(_DEBUG_HANDLE_PREFIX + str((c.n_qubits, n_shots)))
                )
            else:
                resp = put(
                    self._url,
                    data={
                        "data": json.dumps(aqt_circ),
                        "repetitions": n_shots,
                        "no_qubits": c.n_qubits,
                        "label": self._label,
                    },
                    headers=self._header,
                ).json()
                if "status" not in resp:
                    raise RuntimeError(resp["message"])
                if resp["status"] == "error":
                    raise RuntimeError(resp["ERROR"])
                handles.append(ResultHandle(resp["id"]))
        for handle in handles:
            self._cache[handle] = dict()
        return handles

    def circuit_status(self, handle: ResultHandle) -> CircuitStatus:
        self._check_handle_type(handle)
        jobid = handle[0]
        message = ""
        if self._MACHINE_DEBUG:
            n_qubits, n_shots = literal_eval(jobid[len(_DEBUG_HANDLE_PREFIX) :])
            empty_ar = OutcomeArray.from_ints([0] * n_shots, n_qubits, big_endian=True)
            self._cache[handle].update({"result": BackendResult(shots=empty_ar)})
            statenum = StatusEnum.COMPLETED
        else:
            data = put(self._url, data={"id": jobid}, headers=self._header).json()
            status = data["status"]
            if "ERROR" in data:
                message = data["ERROR"]
            statenum = _STATUS_MAP.get(status, StatusEnum.ERROR)
            if statenum is StatusEnum.COMPLETED:
                shots = OutcomeArray.from_ints(
                    data["samples"], data["no_qubits"], big_endian=True
                )
                self._cache[handle].update({"result": BackendResult(shots=shots)})
        return CircuitStatus(statenum, message)

    def get_result(self, handle: ResultHandle, **kwargs: KwargTypes) -> BackendResult:
        """
        See :py:meth:`pytket.backends.Backend.get_result`.
        Supported kwargs: `timeout`, `wait`.
        """
        try:
            return super().get_result(handle)
        except CircuitNotRunError:
            timeout = kwargs.get("timeout")
            wait = kwargs.get("wait", 1.0)
            # Wait for job to finish; result will then be in the cache.
            end_time = (time.time() + timeout) if (timeout is not None) else None
            while (end_time is None) or (time.time() < end_time):
                circuit_status = self.circuit_status(handle)
                if circuit_status.status is StatusEnum.COMPLETED:
                    return self._cache[handle]["result"]
                if circuit_status.status is StatusEnum.ERROR:
                    raise RuntimeError(circuit_status.message)
                time.sleep(wait)
            raise RuntimeError(f"Timed out: no results after {timeout} seconds.")
