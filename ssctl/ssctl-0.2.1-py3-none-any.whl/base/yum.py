import subprocess
import os
import platform

__USE_YUM__ = None
__YUM_CONFIG_PATH__ = "/etc/yum.repos.d/shadowsocks-libev.repo"


def is_use():
    global __USE_YUM__
    if __USE_YUM__ is not None:
        return __USE_YUM__
    with open(os.devnull, "w") as f:
        status_code = subprocess.call("yum version", stdout=f, stderr=f,
                                      shell=True)
        __USE_YUM__ = (status_code == 0)
    return __USE_YUM__


def install(pkg_list):
    cmd = "yum install -y " + " ".join(pkg_list)
    print(cmd)
    subprocess.call(cmd, stdout=os.sys.stdout,
                    stderr=os.sys.stdout,
                    shell=True)


def add_source(source_url):
    with open(__YUM_CONFIG_PATH__, "w") as _f:
        if platform.python_version()[0] == "2":
            import urllib2
            _u = urllib2.urlopen(source_url)
            _f.write(_u.read())
        elif platform.python_version()[0] == "3":
            import urllib.request
            with urllib.request.urlopen(source_url) as _u:
                _f.write(_u.read())

    subprocess.call("yum makecache", stdout=os.sys.stdout,
                    stderr=os.sys.stdout,
                    shell=True)
