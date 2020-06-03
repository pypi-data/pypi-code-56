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
"""Pytket Backend for Honeywell devices."""

from ast import literal_eval
import json
from http import HTTPStatus
from typing import Dict, Iterable, List, Optional, TYPE_CHECKING

import numpy as np
import requests
from pytket.backends import Backend, ResultHandle, CircuitStatus, StatusEnum
from pytket.backends.backend import KwargTypes
from pytket.backends.resulthandle import _ResultIdTuple
from pytket.backends.backendresult import BackendResult
from pytket.backends.backend_exceptions import CircuitNotRunError
from pytket.circuit import Circuit, OpType, Bit
from pytket.device import Device
from pytket.honeywell.honeywell_convert import honeywell_pass, translate_honeywell
from pytket.passes import BasePass, SequencePass, SynthesiseIBM
from pytket.predicates import GateSetPredicate, MaxNQubitsPredicate, Predicate
from pytket.routing import FullyConnected
from pytket.utils.outcomearray import OutcomeArray
from .api_wrappers import retrieve_job

if TYPE_CHECKING:
    from pytket.device import Device

_DEBUG_HANDLE_PREFIX = "_MACHINE_DEBUG_"


HONEYWELL_URL_PREFIX = "https://qapi.honeywell.com/v1/"

HONEYWELL_DEVICE_QC = "HQS-LT-1.0"
HONEYWELL_DEVICE_APIVAL = "HQS-LT-1.0-APIVAL"

# Hard-coded for now as there is no API to retrieve these.
# All devices are fully connected.
_DEVICE_INFO = {
    HONEYWELL_DEVICE_QC: {"max_n_qubits": 4},
    HONEYWELL_DEVICE_APIVAL: {"max_n_qubits": 10},
}

_STATUS_MAP = {
    "queued": StatusEnum.QUEUED,
    "running": StatusEnum.RUNNING,
    "completed": StatusEnum.COMPLETED,
    "failed": StatusEnum.ERROR,
    "canceling": StatusEnum.ERROR,
    "canceled": StatusEnum.ERROR,
}


class HoneywellBackend(Backend):
    """
    Interface to a Honeywell device.
    """

    _supports_shots = True
    _supports_counts = True
    _persistent_handles = True

    def __init__(
        self,
        api_key: str,
        device_name: Optional[str] = HONEYWELL_DEVICE_APIVAL,
        label: Optional[str] = "job",
    ):
        """
        Construct a new Honeywell backend.

        :param      api_key: Honeywell API key
        :type       api_key: string
        :param      device_name:  device name (suffix of URL, e.g. "HQS-LT-1.0")
        :type       device_name:  string
        :param      label:        label to apply to submitted jobs
        :type       label:        string
        """
        super().__init__()
        self._device_name = device_name
        self._label = label
        self._header = {"x-api-key": api_key}
        self._max_n_qubits = (
            _DEVICE_INFO[device_name]["max_n_qubits"]
            if device_name in _DEVICE_INFO
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
            GateSetPredicate(
                {
                    OpType.Rz,
                    OpType.PhasedX,
                    OpType.ZZMax,
                    OpType.Reset,
                    OpType.Measure,
                    OpType.Barrier,
                }
            )
        ]
        if self._max_n_qubits is not None:
            preds.append(MaxNQubitsPredicate(self._max_n_qubits))
        return preds

    @property
    def default_compilation_pass(self) -> BasePass:
        return SequencePass([SynthesiseIBM(), honeywell_pass])

    @property
    def _result_id_type(self) -> _ResultIdTuple:
        return tuple((str,))

    @property
    def device(self) -> Optional["Device"]:
        return None

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
        basebody = {
            "machine": self._device_name,
            "name": self._label,
            "language": "OPENQASM 2.0",
            "priority": "normal",
            "count": n_shots,
            "options": None,
        }
        handle_list = []
        for circ in circuits:
            honeywell_circ = translate_honeywell(circ)
            body = basebody.copy()
            body["program"] = honeywell_circ
            if self._MACHINE_DEBUG:
                handle_list.append(
                    ResultHandle(_DEBUG_HANDLE_PREFIX + str((circ.n_qubits, n_shots)))
                )
            else:
                try:
                    # send job request
                    res = requests.post(
                        HONEYWELL_URL_PREFIX + "job",
                        json.dumps(body),
                        headers=self._header,
                    )
                    jobdict = res.json()
                    if res.status_code != HTTPStatus.OK:
                        print(jobdict)
                        raise RuntimeError(
                            f'HTTP error while submitting job, {jobdict["error"]["text"]}'
                        )
                except ConnectionError:
                    raise ConnectionError(
                        "{} Connection Error: Error during submit...".format(
                            self._label
                        )
                    )

                # extract job ID from response
                handle = ResultHandle(jobdict["job"])
                handle_list.append(handle)
                self._cache[handle] = dict()

        return handle_list

    def _retrieve_job(self, jobid: str, timeout=None) -> Dict:
        return retrieve_job(
            self._header["x-api-key"], jobid, HONEYWELL_URL_PREFIX, timeout=timeout
        )

    def _update_cache_result(self, handle: ResultHandle, res: BackendResult):
        rescache = {"result": res}

        if handle in self._cache:
            self._cache[handle].update(rescache)
        else:
            self._cache[handle] = rescache

    def circuit_status(self, handle: ResultHandle) -> CircuitStatus:
        if self._MACHINE_DEBUG or handle[0].startswith(_DEBUG_HANDLE_PREFIX):
            return CircuitStatus(StatusEnum.COMPLETED)
        res = requests.get(
            HONEYWELL_URL_PREFIX + "job/" + handle[0] + "?websocket=true",
            headers=self._header,
        )
        response = res.json()
        circ_status = _parse_status(response)
        if circ_status.status is StatusEnum.COMPLETED:
            if "results" in response:
                self._update_cache_result(handle, _convert_result(response["results"]))
        return circ_status

    def get_result(self, handle: ResultHandle, **kwargs: KwargTypes) -> BackendResult:
        """
        See :py:meth:`pytket.backends.Backend.get_result`.
        Supported kwargs: `timeout`.
        """
        try:
            return super().get_result(handle)
        except CircuitNotRunError:
            if self._MACHINE_DEBUG or handle[0].startswith(_DEBUG_HANDLE_PREFIX):
                debug_handle_info = handle[0][len(_DEBUG_HANDLE_PREFIX) :]
                n_qubits, shots = literal_eval(debug_handle_info)
                return _convert_result({"c": (["0" * n_qubits] * shots)})
            jobid = handle[0]
            # TODO exception handling when jobid not found on backend
            job_retrieve = self._retrieve_job(jobid, kwargs.get("timeout"))
            circ_status = _parse_status(job_retrieve)
            if circ_status.status is not StatusEnum.COMPLETED:
                raise RuntimeError(
                    f"Cannot retrieve results, job status is {circ_status.message}"
                )
            try:
                res = job_retrieve["results"]
            except KeyError:
                raise RuntimeError("Results missing.")

            backres = _convert_result(res)
            self._update_cache_result(handle, backres)
            return backres


def _convert_result(resultdict: Dict[str, List[str]]) -> BackendResult:
    array_dict = {
        creg: np.array([list(a) for a in reslist]).astype(np.uint8)
        for creg, reslist in resultdict.items()
    }
    reversed_creg_names = sorted(array_dict.keys(), reverse=True)
    c_bits = [
        Bit(name, ind)
        for name in reversed_creg_names
        for ind in range(array_dict[name].shape[-1] - 1, -1, -1)
    ]

    stacked_array = np.hstack([array_dict[name] for name in reversed_creg_names])
    return BackendResult(c_bits=c_bits, shots=OutcomeArray.from_readouts(stacked_array))


def _parse_status(response: Dict) -> CircuitStatus:
    h_status = response["status"]
    message = response["error"]["text"] if h_status == "failed" else h_status
    return CircuitStatus(_STATUS_MAP[h_status], message)
