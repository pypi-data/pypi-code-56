"""Ucal Client implementation."""
from functools import wraps
import warnings

import grpc

# Make deprecation warnings silent
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    from google.protobuf import empty_pb2
    from ucal_client._internal_grpc import server_pb2
    from ucal_client._internal_grpc import server_pb2_grpc
    from ucal_client.base import UcalBlock, UcalState, \
        UcalConfig, UcalClientException, UcalTs

import numpy as np
import pandas as pd


_SERVER_DEFAULT_HOST = "192.168.241.1"
_SERVER_DEFAULT_PORT = "10003"
_SERVER_DEFAULT_TIMEOUT_SECONDS = 5


def grpc_reraise(method):
    """Wrap grpc error into UcalClientException."""
    @wraps(method)
    def reraised_method(*args, **kwargs):
        try:
            return method(*args, **kwargs)
        except grpc.RpcError as exc:
            exc_msg = None
            code = exc.code()  # pylint: disable=no-member
            details = exc.details()  # pylint: disable=no-member
            if code in (
                    grpc.StatusCode.UNAVAILABLE,
                    grpc.StatusCode.UNKNOWN,
                    grpc.StatusCode.DEADLINE_EXCEEDED
            ):
                exc_msg = "Failed to establish connection: {}".format(details)
            elif code == grpc.StatusCode.INVALID_ARGUMENT:
                exc_msg = "Got invalid input: {}".format(details)
            elif code == grpc.StatusCode.FAILED_PRECONDITION:
                exc_msg = "Action can't be performed: {}".format(details)
            if exc_msg:
                # No grpc traceback
                raise UcalClientException(exc_msg) from None
            else:
                # Show grpc traceback
                exc_msg = "Server bug, please report: {}".format(details)
                raise UcalClientException(exc_msg)
    return reraised_method


class UcalClient:
    """
    The main object that can be used to manage Ucal Server.
    Client (and Server) supports next actions:

    - get_state to get current state of server, see UcalState;
    - set/get_config to save global settings, see UcalConfig;
    - set/get_plan to set execution program, see UcalBlock;
    - get_data to download from server data as a pandas.DataFrame;
    - run_next/stop to start and stop program execution.
    """
    def __init__(
            self,
            host=_SERVER_DEFAULT_HOST,
            port=_SERVER_DEFAULT_PORT,
            timeout_s=_SERVER_DEFAULT_TIMEOUT_SECONDS
    ):
        """
        Set host to 'localhost' when server is run locally.
        :param host: IP addrress where server is running
        :param port: port where server is running
        :param timeout_s: how much time in seconds should
            client wait for response from server
        """
        self.host = host
        self.port = port
        self.timeout_s = timeout_s

        self._channel = grpc.insecure_channel(
            "{}:{}".format(self.host, self.port)
        )
        self.stub = server_pb2_grpc.ServerStub(self._channel)

    def is_server_available(self, timeout_s=2):
        """
        Checks if server is currently available.
        :param timeout_s: how much time in seconds should
            client wait for response from server
        """
        try:
            grpc.channel_ready_future(self._channel).result(
                timeout=timeout_s
            )
            return True
        except grpc.FutureTimeoutError:
            return False

    @grpc_reraise
    def get_state(self):
        """
        Return UcalState of the server.
        Possible results: *NoPlan*, *HavePlan*, *Executing*, *Error*.
        State defines, which actions can or can not be executed by server now.
        """
        return UcalState(
            self.stub.GetState(empty_pb2.Empty(), timeout=self.timeout_s).name
        )

    @grpc_reraise
    def get_config(self):
        """
        Return current server configuration as a UcalConfig.
        Valid action at any state.
        """
        return UcalConfig.from_message(
            self.stub.GetConfig(empty_pb2.Empty(), timeout=self.timeout_s).json
        )

    @grpc_reraise
    def set_config(self, config):
        """
        Apply new config(UcalConfig) to the server.
        Valid action at *NoPlan* state only.

        :param config: UcalConfig, Str, None or Dict with
            valid UcalConfig key-values
        """
        if isinstance(config, dict):
            config = UcalConfig(**config)
        if isinstance(config, UcalConfig):
            self.stub.SetConfig(
                server_pb2.JsonMsg(json=config.to_message()), timeout=self.timeout_s
            )
            return
        if config is None:
            config = "{}"
        if isinstance(config, str):
            self.stub.SetConfig(
                server_pb2.JsonMsg(json=config), timeout=self.timeout_s
            )
            return
        msg = "set_config accepts dict, UcalConfig or str, got {}".format(
            type(config)
        )
        raise UcalClientException(msg)

    @grpc_reraise
    def get_plan(self):
        """
        Return plan (List[UcalBlock]) that server is executing or
        going to execute.
        Valid action at *NoPlan*, *HavePlan* and *Executing* states.
        """
        grpc_blocks = list(
            b for b in self.stub.GetPlan(empty_pb2.Empty())
        )
        replace = lambda v: v if len(v) else None
        return list(
            UcalBlock(
                read_step_tu=b.read_step_tu,
                write_step_tu=b.write_step_tu,
                block_len_tu=b.block_len_tu,
                voltage_0=replace(b.voltage_0),
                voltage_1=replace(b.voltage_1)
            ) for b in grpc_blocks
        )

    @grpc_reraise
    def set_plan(self, plan):
        """
        Set a new plan for server.
        Valid action at *NoPlan* and *HavePlan* states.

        :param plan: List[UcalBlock], starting point for returned data.
            Set empty list([]) to move to *NoPlan* state.
        """
        if not (
                isinstance(plan, list) and
                all(isinstance(b, UcalBlock) for b in plan)
        ):
            msg = "Plan must have type List[UcalBlock]"
            raise UcalClientException(msg)
        self.stub.SetPlan(
            (server_pb2.BlockMsg(
                read_step_tu=b.read_step_tu,
                write_step_tu=b.write_step_tu,
                block_len_tu=b.block_len_tu,
                voltage_0=b.voltage_0,
                voltage_1=b.voltage_1
            ) for b in plan),
            timeout=self.timeout_s
        )

    @grpc_reraise
    def get_data(self, start_ts=None, merge=True):
        """
        Return List[pd.DataFrame] from Server.
        If merge=True, DataFrames are concatenated.
        DataFrames contain info about voltage and time moments from
        the execution start.

        :param start_ts: UcalTs, starting point for returned data.
        :param merge: bool, whether to concat frames into single df.
        """
        EXPECTED_DATA_KEYS = ['Uaux', 'Uhtr', 'Umod', 'Uref', 'Utpl']
        ADDITIONAL_KEYS = ['step', 'count']
        TIME_KEY = ['Time']

        if start_ts is None:
            start_ts = UcalTs(0, 0)
        assert isinstance(start_ts, UcalTs)

        def parse_frame_msg(msg):
            """Turn server_pb2.FrameMsg into pd.DataFrame."""
            data = dict(msg.data)
            if len(data.keys()) and (sorted(data.keys()) != EXPECTED_DATA_KEYS):
                msg = "Server interface has changed! "
                msg += "Expected data keys '{}' but got '{}'".format(
                    EXPECTED_DATA_KEYS, list(data.keys())
                )
                raise UcalClientException(msg)
            step = np.zeros(msg.size) + msg.ts.step
            count = np.arange(msg.ts.count, msg.ts.count + msg.size)
            return np.stack(
                [step, count] +
                [np.array(data[k].data) for k in EXPECTED_DATA_KEYS],
                axis=-1
            )
        raw_data = list(self.stub.GetData(
            server_pb2.TimeStampMsg(step=start_ts.step, count=start_ts.count),
            timeout=self.timeout_s
        ))
        message_arrays = list(parse_frame_msg(r) for r in raw_data)
        if merge:
            if not len(message_arrays):
                return pd.DataFrame(columns=TIME_KEY + EXPECTED_DATA_KEYS)
            total = np.vstack(message_arrays)
            df = pd.DataFrame(total, columns=ADDITIONAL_KEYS + EXPECTED_DATA_KEYS)
            df['Time'] = df['step'].cumsum()
            df = df.drop(columns=['count', 'step'])
            return df.set_index('Time')
        else:
            if not len(message_arrays):
                return []
            return [
                pd.DataFrame(x, columns=ADDITIONAL_KEYS + EXPECTED_DATA_KEYS)
                for x in message_arrays
            ]

    @grpc_reraise
    def _deprecated_get_data(self, start_ts=None, merge=True):
        """
        Return List[pd.DataFrame] from Server.
        If merge=True, DataFrames are concatenated.
        DataFrames contain info about voltage and time moments from
        the execution start.

        :param start_ts: UcalTs, starting point for returned data.
        :param merge: bool, whether to concat frames into single df.
        """
        # TODO: delete this method as deprecated
        if start_ts is None:
            start_ts = UcalTs(0, 0)
        assert isinstance(start_ts, UcalTs)

        def parse_frame_msg(msg):
            """Turn server_pb2.FrameMsg into pd.DataFrame."""
            df = pd.DataFrame()
            for col in msg.data.keys():
                df[col] = msg.data[col].data
            df['step'] = msg.ts.step
            # TimeStamp in frame is related to the last point
            df['count'] = list(
                x for x in range(msg.ts.count, msg.ts.count + len(df))
            )
            return df
        raw_data = (self.stub.GetData(
            server_pb2.TimeStampMsg(step=start_ts.step, count=start_ts.count),
            timeout=self.timeout_s
        ))

        separate_dfs = list(parse_frame_msg(r) for r in raw_data)
        if merge:
            if not len(separate_dfs):
                return pd.DataFrame()
            df = pd.concat(separate_dfs).reset_index(drop=True)
            df['Time'] = df['step'].cumsum()
            df = df.drop(columns=['count', 'step'])
            return df.set_index('Time')
        else:
            return separate_dfs

    @grpc_reraise
    def run_next(self):
        """
        Start next block execution.
        Valid action at *HavePlan*, *Executing* states.
        If server is at *HavePlan* state, execution is started.
        If server is at *Executing* state, current UcalBlock execution is
        stopped and next UcalBlock in plan is started.
        If there is no more UcalBlock in plan, execution is finished and
        *HavePlan* state is set.
        """
        return self.stub.RunNext(empty_pb2.Empty(), timeout=self.timeout_s)

    @grpc_reraise
    def stop(self):
        """
        Stop blocks execution. All measured data is available.
        Valid action at *Executing* state.
        """
        return self.stub.Stop(empty_pb2.Empty(), timeout=self.timeout_s)

    @grpc_reraise
    def get_logs(self):
        """Return current server logs."""
        return str(self.stub.GetLogs(empty_pb2.Empty(), timeout=self.timeout_s).row)

    @grpc_reraise
    def drop_logs(self):
        """Drop current server logs."""
        self.stub.DropLogs(empty_pb2.Empty(), timeout=self.timeout_s)
