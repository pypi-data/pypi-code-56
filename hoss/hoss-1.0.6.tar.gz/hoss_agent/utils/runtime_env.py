import platform


def get_runtime_env():
    return {
        "arch": platform.machine(),
        "hostname": platform.node() or "unknown",
        "type": platform.system(),
        "platform:": platform.platform(),
        "version": platform.python_version(),
    }
