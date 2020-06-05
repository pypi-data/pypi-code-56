from typing import Any, Dict

__virtualname__ = "vbox"


def absent(hub, ctx, name: str, *args, **kwargs) -> Dict[str, Any]:
    ret = {
        "name": name,
        "result": True,
        "changes": {"old": None, "new": None},
        "comment": "",
    }

    if not hub.exec.vbox.exists(name):
        ret["comment"] = f"Virtualbox machine {name} is already absent"
        return ret

    ret["changes"]["old"] = hub.exec.vbox.get(name)

    if ctx["test"]:
        return ret

    ret["result"] = hub.exec.vbox.delete(name, *args, **kwargs)
    ret["comment"] = f"Deleted virtualbox machine: {name}"

    return ret


def present(hub, ctx, name: str, *args, **kwargs) -> Dict[str, Any]:
    ret = {
        "name": name,
        "result": True,
        "changes": {"old": None, "new": None},
        "comment": "",
    }
    if hub.exec.vbox.exists(name):
        ret["changes"]["new"] = ret["changes"]["old"] = hub.exec.vbox.get(name)
        ret["comment"] = f"Virtualbox machine {name} is already present"
        return ret

    if ctx["test"]:
        return ret

    ret["changes"]["new"] = hub.exec.vbox.create(name, *args, **kwargs)
    ret["result"] = hub.exec.vbox.exists(name)
    ret["comment"] = f"Created virtualbox machine: {name}"

    return ret
