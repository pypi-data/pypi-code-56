from ssctl.base import supervisor, system


def main(port=0):
    if system.can_use_port(port):
        raise OSError("%d 端口并未被使用，请重新选择")
    supervisor.remove(port)
