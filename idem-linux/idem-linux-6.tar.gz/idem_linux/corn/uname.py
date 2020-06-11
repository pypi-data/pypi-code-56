import os


async def load_uname(hub):
    """
    Verify that idem-linux is running on linux
    """
    (
        hub.corn.CORN.kernel,
        hub.corn.CORN.nodename,
        hub.corn.CORN.kernelrelease,
        hub.corn.CORN.kernelversion,
        hub.corn.CORN.cpuarch,
    ) = os.uname()

    assert (
        hub.corn.CORN.kernel == "Linux"
    ), "idem-Linux is only intended for Linux systems"


async def load_ps(hub):
    """
    Let anyone else try to set this grain first, then fallback to a default
    """
    if not await hub.corn.init.wait_for("ps"):
        hub.log.info("Using default Linux 'ps' grain")
        hub.corn.CORN.ps = "ps -efHww"
