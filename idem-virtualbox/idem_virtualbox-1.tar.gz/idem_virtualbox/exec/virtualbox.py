# -*- coding: utf-8 -*-
"""
A salt cloud provider that lets you use virtualbox on your machine
and act as a cloud.

:depends: vboxapi

For now this will only clone existing VMs. It's best to create a template
from which we will clone.

Followed
https://docs.saltstack.com/en/latest/topics/cloud/cloud.html#non-libcloud-based-modules
to create this.
"""
import logging
import virtualbox
from typing import Any, Dict, List

log = logging.getLogger(__name__)
SaltCloudSystemExit = OSError

__virtualname__ = "vbox"
__func_alias__ = {
    "list_": "list",
}


def __virtual__(hub):
    # vbox-sdk is required to use this plugin
    return bool(virtualbox.import_vboxapi())


def __init__(hub):
    hub.exec.vbox.MANAGER = virtualbox.Manager()
    hub.exec.vbox.VBOX = hub.exec.vbox.MANAGER.get_virtualbox()


_is_builtin_type = lambda x: x.__class__.__module__ == "builtins"


def _node_to_dict(
    node: virtualbox.library_ext.IMachine, full: bool = False
) -> Dict[str, Any]:
    # Start with the values that are expected of every cloud node
    ret = {
        "id": node.id_p,
        "image": "",
        "size": int(node.memory_size),
        "state": str(node.state),
        "private_ips": (),
        "public_ips": (),
    }
    if full:
        # TODO ask for the correct attributes e.g state and private_ips
        for attr in dir(node):
            if not any(
                attr.startswith(x)
                for x in (
                    # Skip underscore attributes
                    "_",
                    # We already have these ones
                    "id_p",
                    "state",
                    "memory_size",
                    "name",
                    # These take far to long to load
                    "fault_",
                    "graphics_",
                    "accelerate",
                    "monitor",
                    "vram",
                )
            ):
                try:
                    value = getattr(node, attr)
                    if (
                        # Only call values that are builtin types, we aren't parsing custom objects
                        not callable(value)
                        and _is_builtin_type(value)
                        # If it's a list, make sure the things inside it aren't custom objects
                        and not (
                            hasattr(value, "__iter__")
                            and (len(value) >= 1)
                            and not _is_builtin_type(value[0])
                        )
                    ):
                        ret[attr] = value
                except Exception as e:
                    log.debug(
                        f"Error when collecting Machine {node.name} attribute {attr}: {e}"
                    )
    return ret


def _wait_progress(progress: virtualbox.lib.IProgress, timeout: int = -1) -> bool:
    progress.wait_for_completion(timeout=timeout)

    if progress.completed and progress.result_code:
        return False
    else:
        return True


def images(hub) -> Dict:
    r"""
    This function returns a list of images available for this cloud provider.


    CLI Example:

    .. code-block:: bash

        idem exec virtualbox.images

        # \[ virtualbox will always return an empty dict \]
    """
    return {}


def locations(hub) -> Dict:
    r"""
    This function returns a list of locations available.

    CLI Example:

    .. code-block:: bash

        idem exec virtualbox.locations

        # \[ virtualbox will always returns an empty dictionary \]
    """
    return {}


def sizes(hub) -> Dict:
    r"""
    This function returns a list of sizes available for this cloud provider.

    CLI Example:

    .. code-block:: bash

        idem exec virtualbox.sizes

        # \[ virtualbox will always returns an empty dictionary \]
    """
    return {}


def clone(
    hub,
    name: str,
    clone_from: str,
    timeout: int = -1,
    # These will be passed to `create_machine`
    os_type_id: str = "Other",
    groups: List[str] = None,
    settings_file: str = None,
    flags: Dict[str, str] = None,
    # These will be passed to `clone_to`
    mode: virtualbox.lib.CloneMode = 3,
    options: List[virtualbox.lib.CloneOptions] = None,
):
    log.info(f"Clone virtualbox machine {name} from {clone_from}")

    source_machine: virtualbox.library_ext.IMachine = hub.exec.vbox.VBOX.find_machine(
        clone_from
    )
    new_machine: virtualbox.library_ext.IMachine = hub.exec.vbox.VBOX.create_machine(
        name=name,
        os_type_id=os_type_id,
        groups=groups or [],
        settings_file=settings_file or "",
        flags=",".join(f"{key}={value}" for key, value in (flags or {}).items()),
    )

    progress: virtualbox.library_ext.IProgress = source_machine.clone_to(
        target=new_machine, mode=virtualbox.lib.CloneMode(mode), options=options or []
    )

    ret = _wait_progress(progress, timeout)
    if ret:
        log.error(
            f"Could not clone virtualbox machine '{name}' from '{clone_from}':\n{progress.error_info}"
        )
        return {}
    else:
        log.info(f"Finished cloning '{name}' from '{clone_from}'")
        hub.exec.vbox.VBOX.register_machine(new_machine)
        return _node_to_dict(new_machine)


def create(
    hub,
    name: str,
    clone_from: str,
    timeout: int = -1,
    # These will be passed to `create_machine`
    os_type_id: str = "Other",
    flags: Dict[str, str] = None,
    groups: List[str] = None,
    settings_file: str = None,
    # These will be passed to `clone_to`
    clone_mode: virtualbox.lib.CloneMode = 3,
    clone_options: List[virtualbox.lib.CloneOptions] = None,
) -> Dict[str, str]:
    """
    Provision a single machine

    CLI Example:

    .. code-block:: bash

        idem exec vbox.create instance_name clone_from=image
    """
    log.info(f"Creating virtualbox machine: {name}")
    ret = hub.exec.vbox.clone(
        name=name,
        clone_from=clone_from,
        timeout=timeout,
        os_type_id=os_type_id,
        groups=groups,
        settings_file=settings_file,
        flags=flags,
        mode=clone_mode,
        options=clone_options,
    )
    return ret


def delete(
    hub, name: str, cleanup_mode: virtualbox.lib.CleanupMode = 2, timeout: int = -1
) -> bool:
    """
    Destroy a node.

    CLI Example:

    .. code-block:: bash

        idem exec vbox.delete instance_name
    """
    if not hub.exec.vbox.exists(name):
        log.info(f"'{name}' doesn't exist and cannot be deleted")
        return True
    log.info(f"Destroying virtualbox machine: {name}")
    machine: virtualbox.library_ext.IMachine = hub.exec.vbox.VBOX.find_machine(name)
    files = machine.unregister(cleanup_mode=virtualbox.lib.CleanupMode(cleanup_mode))
    progress: virtualbox.library_ext.IProgress = machine.delete_config(files)

    ret = _wait_progress(progress, timeout)
    if ret:
        log.error(
            f"Could not delete virtualbox machine '{name}': {progress.error_info}"
        )
    else:
        log.info(f"Finished destroying virtualbox machine: {name}")

    return ret and _wait_progress(progress, timeout)


def exists(hub, name: str) -> bool:
    try:
        hub.exec.vbox.VBOX.find_machine(name)
        return True
    except Exception as e:
        log.error(f"Could not find machine {name}: {e}")
        return False


def list_(hub, full: bool = False) -> Dict[str, Dict[str, Any]]:
    """
    List the nodes.

    CLI Example:

    .. code-block:: bash

        idem exec vbox.list full=True
    """
    return {
        machine.name: _node_to_dict(machine, full=full)
        for machine in hub.exec.vbox.VBOX.machines
    }


def get(hub, name: str, full: bool = False) -> Dict[str, Any]:
    """
    List the a single node, return dict of attributes.

    CLI Example:

    .. code-block:: bash

        idem exec vbox.get instance_name full=True
    """
    ret = hub.pop.data.imap({"pid": 2, "retcode": 0, "stdout": "", "stderr": ""})
    # TODO use virtualbox.library_ext.virtual_system_description
    out = hub.exec.vbox.VBOX.find_machine(name)
    _node_to_dict(out, full=full)
    return ret


def start(
    hub,
    name: str,
    timeout: int = -1,
    # These get passed to "launch_vm_process"
    type_p: str = "headless",
    environment: str = "",
) -> Dict[str, Any]:
    """
    Start the virtual machine

    CLI Example:

    .. code-block:: bash

        idem exec vbox.start instance_name
    """
    machine: virtualbox.library_ext.IMachine = hub.exec.vbox.VBOX.find_machine(name)
    log.info(f"Starting machine '{name}' from state '{str(machine.state)}'")

    session: virtualbox.Session = hub.exec.vbox.MANAGER.get_session()
    progress: virtualbox.library_ext.IProgress = machine.launch_vm_process(
        session, type_p=type_p, environment=environment
    )
    ret = _wait_progress(progress, timeout)

    session.unlock_machine()

    if ret:
        log.error(
            f"Could not start virtualbox machine '{name}'':\n{progress.error_info.text}"
        )
    else:
        log.info(f"Started machine '{name}'")

    # TODO wait for IPs and such

    return _node_to_dict(machine)


def stop(hub, name: str, timeout: int = -1) -> Dict[str, Any]:
    """
    Halt the Vagrant box.

    CLI Example:

    .. code-block:: bash

        idem exec vbox.stop instance_name
    """
    machine: virtualbox.library_ext.IMachine = hub.exec.vbox.VBOX.find_machine(name)
    log.info(f"Stopping machine '{name}' from state '{str(machine.state)}'")

    session: virtualbox.Session = hub.exec.vbox.MANAGER.get_session()
    machine.lock_machine(session, virtualbox.lib.LockType(1))

    progress: virtualbox.library.IProgress = session.console.power_down()
    ret = _wait_progress(progress, timeout)

    if ret:
        log.error(
            f"Could not Stop virtualbox machine '{name}'':\n{progress.error_info.text}"
        )
    else:
        log.info(f"Stopped machine '{name}'")

    session.unlock_machine()
    return _node_to_dict(machine)
