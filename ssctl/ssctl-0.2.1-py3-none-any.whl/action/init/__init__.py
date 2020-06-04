from ssctl.base import yum, system, supervisor


def main():
    system.check_root()
    if not yum.is_use():
        raise OSError("系统不支持 yum，需要在支持 yum 的系统上运行")
    yum.add_source("https://copr.fedorainfracloud.org/coprs/outman/"
                   "shadowsocks-libev/repo/epel-7/"
                   "outman-shadowsocks-libev-epel-7.repo")
    yum.install(("epel-release", "supervisor", "lsof"))
    yum.install(("libsodium", "shadowsocks-libev", "simple-obfs"))
    system.check_command("ss-server --help", check_string="shadowsocks-libev")
    supervisor.enable()
    system.user_init()
    print("已完成 shadowsocks 初始化工作")
