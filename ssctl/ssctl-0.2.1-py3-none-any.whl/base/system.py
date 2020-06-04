# import platform
import subprocess


def check_root():
    import getpass
    if getpass.getuser() != "root":
        raise UserWarning("请使用 sudo 或 root 身份运行")


def check_command(command, check_string=None):
    if (subprocess.Popen(command,
                         shell=True,
                         stdout=subprocess.PIPE)
            .stdout.read().find(check_string)) < 0:
        raise OSError("命令检查错误：%s" % command)


def user_init():
    subprocess.check_call("groupadd -g 1234 shadowsocks", shell=True)
    subprocess.check_call(
        "useradd -u 1234 -m -g 1234 -s /sbin/nologin shadowsocks",
        shell=True)
    subprocess.call("mkdir -p /home/shadowsocks/etc/supervisor",
                    shell=True)
    subprocess.call("mkdir -p /home/shadowsocks/var/log",
                    shell=True)
    subprocess.call("chown -R shadowsocks:shadowsocks /home/shadowsocks",
                    shell=True)


def can_use_port(port):
    status_code = subprocess.call("lsof -i tcp:%d" % port, shell=True)
    return status_code != 0
