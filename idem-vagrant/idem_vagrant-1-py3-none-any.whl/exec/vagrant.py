import logging
import os
import re
import subprocess
import shutil
from typing import Any, Dict, List

log = logging.getLogger(__name__)

# Credit to https://github.com/todddeluca/python-vagrant/blob/master/vagrant/__init__.py

__func_alias__ = {
    "list_": "list",
}


def __virtual__(hub):
    if not bool(shutil.which("vagrant")):
        return "Could not locate the 'vagrant' command"
    return True


def __init__(hub):
    hub.exec.vagrant.VAGRANT_EXE = shutil.which("vagrant")
    hub.exec.vagrant.VERSION = _version(hub)

    # TODO is this right? or am I waiting for vertical config loading to work?
    # TODO or does this belong in account profiles? idk
    # hub.pop.config.load(["idem", "idem_vagrant"], "idem")
    # hub.exec.vagrant.PATH = os.path.abspath(
    #    os.path.expanduser(hub.OPT.idem_vagrant.root)
    # )
    os.makedirs(hub.exec.vagrant.PATH, exist_ok=True)


def _run(
    hub, *args, subcommand: str = None, name: str = None, timeout: int = None
) -> str:
    """
    Execute a vagrant command in the given directory
    """
    cwd = None
    if name:
        cwd = os.path.join(hub.exec.vagrant.PATH, name)
        os.makedirs(cwd, exist_ok=True)

    cmd = [hub.exec.vagrant.VAGRANT_EXE]
    if subcommand:
        cmd.append(subcommand)
    if name:
        cmd.append(name)
    cmd.extend(args)

    log.debug("Running Vagrant command: " + " ".join(cmd))

    ret = subprocess.check_output(cmd, cwd=cwd, timeout=timeout,)
    return ret.decode()


def _version(hub) -> str:
    output = _run(hub, "--version", timeout=10)
    m = re.search(r"^Vagrant (?P<version>.+)$", output)
    if m is None:
        raise ValueError(
            "Failed to parse vagrant --version output. output={!r}".format(output)
        )
    return m.group("version")


def _node_to_dict(node: Dict[str, Any]) -> Dict[str, Any]:
    # TODO in salt, vbox get's this from the deployed node's grains, do we have grains on that node?
    ret = {
        "id": node.get("id"),
        "image": "",
        "size": node.get("size"),
        "state": node.get("state"),
        "private_ips": (),
        "public_ips": (),
    }

    return ret


def images(hub) -> Dict:
    r"""
    This function returns a list of images available for this cloud provider.


    CLI Example:

    .. code-block:: bash

        idem exec vagrant.images

        # \[ vagrant will return a list of profiles \]
    """
    # TODO salt gets the configured providers and returns a list of profiles
    return {}


def locations(hub) -> Dict:
    r"""
    This function returns a list of locations available.

    CLI Example:

    .. code-block:: bash

        idem exec vagrant.locations

        # \[ vagrant will always returns an empty dictionary \]
    """
    return {}


def sizes(hub) -> Dict:
    r"""
    This function returns a list of sizes available for this cloud provider.

    CLI Example:

    .. code-block:: bash

        idem exec vagrant.sizes

        # \[ vagrant will always returns an empty dictionary \]
    """
    return {}


def create(
    hub, name: str, box_url: str, provisioners: List[str] = None, timeout: int = None
):
    """
    Provision a single machine

    CLI Example:

    .. code-block:: bash

        idem exec vagrant.create exec-args ...
    """
    #  This initializes the current directory to be a Vagrant environment by
    #  creating an initial Vagrantfile if one doesn't already exist.
    # TODO allow the cwd to be configured and have a sane default
    ret = _run(hub, "init", name, box_url, timeout=timeout)

    args = []
    # Run the provisioners defined in the Vagrantfile.
    if provisioners:
        args.append("--provision-with")
        args.extend(provisioners)

    ret = _run(hub, "provision", name, *args, timeout=timeout)


def delete(hub, name: str, timeout: int = None):
    """
    Destroy a node.

    CLI Example:

    .. code-block:: bash

        idem exec vagrant.delete instance_name
    """
    ret = _run(hub, "destroy", name, "--force", timeout=timeout)


def list_(hub, full: bool = True) -> Dict[str, Dict[str, Any]]:
    """
    List the nodes, ask all 'vagrant' minions, return dict of grains (enhanced).

    CLI Example:

    .. code-block:: bash

        idem exec vagrant.list full+True
    """
    pass


def get(hub, name: str, timeout: int = None) -> Dict[str, Any]:
    """
    List the a single node, return dict of attributes.

    CLI Example:

    .. code-block:: bash

        idem exec vagrant.get instance_name
    """
    ret = _run(hub, "status", "--machine-readable", name, timeout=timeout)
    return ret


def start(
    hub,
    name: str,
    timeout: int = None,
    # These get passed to "launch_vm_process"
    type_p: str = "headless",
    environment: str = "",
) -> Dict[str, Any]:
    """
    Invoke `vagrant up` to start a box

    CLI Example:

    .. code-block:: bash

        idem exec vagrant.start instance_name
    """
    ret = _run(hub, "up", name, timeout=timeout)
    return ret


def stop(hub, name: str, force: bool = False, timeout: int = None) -> Dict[str, Any]:
    """
    Halt the Vagrant box.

    CLI Example:

    .. code-block:: bash

        idem exec vagrant.stop instance_name force=True
    """
    args = []
    if force:
        args.append("--force")
    ret = _run(hub, "halt", name, *args, timeout=timeout)

    return ret


# TODO add the snapshot functionality
