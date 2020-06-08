import os
import sys
from threading import RLock

from py4j.java_gateway import GatewayParameters
from py4j.java_gateway import JavaGateway
from py4j.java_gateway import launch_gateway

from .config import g_config
from .utils import has_pyflink

_gateway = None
_lock = RLock()


def set_java_gateway(gateway):
    global _gateway
    global _lock
    with _lock:
        _gateway = gateway


def get_java_gateway():
    global _gateway
    global _lock
    with _lock:
        if _gateway is None:
            _gateway = LocalJvmBridge.inst().gateway
    return _gateway


def get_java_class(name):
    return _gateway.jvm.__getattr__(name)


def list_all_jars():
    alink_deps_dir = g_config["alink_deps_dir"]
    flink_home = g_config["flink_home"]

    ret = []
    ret += [os.path.join(alink_deps_dir, x) for x in
            os.listdir(alink_deps_dir) if x.endswith('.jar')]
    ret += [os.path.join(flink_home, 'lib', x) for x in
            os.listdir(os.path.join(flink_home, 'lib'))
            if x.endswith('.jar')]

    if has_pyflink():
        ret += [os.path.join(flink_home, 'opt', x) for x in
                os.listdir(os.path.join(flink_home, 'opt'))
                if x.endswith('.jar') and x.startswith("flink-python")]
    return ret


class LocalJvmBridge(object):
    _bridge = None

    def __init__(self):
        self.process = None
        self.gateway = None
        self.app = None
        self.port = 0
        pass

    @classmethod
    def inst(cls):
        if cls._bridge is None:
            cls._bridge = LocalJvmBridge()
            cls._bridge.init()
        return cls._bridge

    def init(self):
        debug_mode = g_config["debug_mode"]
        redirect_stdout = sys.stdout if debug_mode else None
        redirect_stderr = sys.stderr if debug_mode else None
        self.port = launch_gateway(
            port=0, javaopts=[], die_on_exit=True, daemonize_redirect=True,
            redirect_stderr=redirect_stdout, redirect_stdout=redirect_stderr,
            classpath=os.pathsep.join(list_all_jars())
        )
        print('JVM listening on 127.0.0.1:{}'.format(self.port))
        self.gateway = JavaGateway(
            gateway_parameters=GatewayParameters(port=self.port, auto_field=True),
            start_callback_server=False)

    def close(self):
        self.gateway.close()
        self.gateway.shutdown()
