import os
import subprocess

__CONF_TEMP__ = """[program:ss_port_{port}]
command      = /usr/bin/ss-server -p {port} -k {password} -m {encrypt} -v
process_name = %(program_name)s
directory    = /home/shadowsocks
user         = shadowsocks
group        = shadowsocks
startsecs    = 3
stopsignal   = TERM
stopasgroup  = true
killasgroup  = true
stopwaitsecs = 3
startretries = 3
autostart    = true
autorestart  = unexpected
redirect_stderr         = true
stdout_logfile_maxbytes = 50MB
stdout_logfile_backups  = 100
stdout_logfile          = /home/shadowsocks/var/log/%(program_name)s.log
stderr_logfile          = /home/shadowsocks/var/log/%(program_name)s.error.log
stderr_logfile_maxbytes = 10MB
stderr_logfile_backups  = 10
"""


def enable():
    subprocess.check_call("systemctl enable supervisord.service", shell=True)
    subprocess.check_call("systemctl start supervisord.service", shell=True)
    with open("/etc/supervisord.d/utf-8.ini", "w") as _f:
        _f.write('[supervisord]\n'
                 'environment=LC_ALL="en_US.UTF-8",LANG="en_US.UTF-8"\n')
    subprocess.check_call("systemctl restart supervisord.service", shell=True)


def generate_config(port=0, password=None, encrypt="aes-256-gcm"):
    print(port)
    print(password)
    print(encrypt)
    assert port != 0
    assert password is not None and len(password) > 6
    config_str = __CONF_TEMP__.format(port=port,
                                      password=password,
                                      encrypt=encrypt)
    config_path = "/home/shadowsocks/etc/supervisor/ss_port_%d.ini" % port
    if os.path.isfile(config_path):
        raise Warning("已存在 %d 端口的配置文件" % port)
    with open(config_path, "w") as _f:
        _f.write(config_str)
    subprocess.check_call(
        "ln -s %s /etc/supervisord.d/ss_port_%d.ini" % (config_path, port),
        shell=True)


def refresh():
    subprocess.call("supervisorctl reread", shell=True)
    subprocess.call("supervisorctl update", shell=True)


def remove(port):
    config_path = "/home/shadowsocks/etc/supervisor/ss_port_%d.ini" % port
    config_link = "/etc/supervisord.d/ss_port_%d.ini" % port
    os.remove(config_path)
    os.remove(config_link)
    refresh()
