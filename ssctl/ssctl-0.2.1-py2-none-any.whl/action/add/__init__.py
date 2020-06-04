from ssctl.base import supervisor, system


def main(port=0, encrypt=None, password=None):
    if not system.can_use_port(port):
        raise OSError("%d 端口已经被占用，请重新选择")
    supervisor.generate_config(port=port, password=password)
    supervisor.refresh()
