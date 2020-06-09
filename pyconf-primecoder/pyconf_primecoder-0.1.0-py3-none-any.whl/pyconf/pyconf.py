"""
pyconf - Python Virtual Environment Configurator

Read configuration file and setup a virtual environment for the current shell session.

"""

import json
import os
import subprocess

PYCONF = "pyconf.json"


def isFileExist(path):
    expanded_path = os.path.expanduser(path)
    return os.path.isfile(expanded_path) or os.path.isdir(expanded_path)


def create_virt_env(virtual_name, virtual_manager):
    """
    Create a virtual environment with a given name.
    """
    print(f"pyconf> Creating virtual env: {virtual_name}")
    expanded_path = os.path.expanduser(virtual_name)
    complete_proc = subprocess.run(
        ["python", "-m", virtual_manager, expanded_path])
    if complete_proc.returncode == 0:
        print(f"pyconf> Done created virtual env: {expanded_path}")
    else:
        print(f"pyconf> ERROR creating virtual env: {expanded_path}")


def create_symlink(pyconf_activation_file):
    """
    Create a symlink file 'pyconf' which links to the activation file for the python env.
    This file can be used as:

    $ source pyconf

    """
    expanded_path = os.path.expanduser(pyconf_activation_file)
    completed_proc = subprocess.run(
        ["ln", "-sf", expanded_path, "activate"])
    if completed_proc.returncode == 0:
        print(f"pyconf> Symlink created")
    else:
        print(f"pyconf> ERROR creating symlink")


def update_py_conf(virtual_path, requirements):
    """
    Update all modules and packages for `virtual_path` using the specified `requirements` file.
    """
    print("pyconf> Upgrading packages in virtual env ...")
    # TODO: change var name - ssh var name is misleading and confusing.
    ssh = subprocess.Popen([f"/bin/bash"],
                           shell=True,
                           stdin=subprocess.PIPE,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE,
                           universal_newlines=True,
                           bufsize=0)

    expanded_path = os.path.expanduser(virtual_path)

    # Send ssh commands to stdin
    ssh.stdin.write(f"echo Activate virtual env: {virtual_path}\n")
    ssh.stdin.write(f"source {expanded_path}\n")

    ssh.stdin.write(f"echo Update pip\n")
    ssh.stdin.write(f"pip install --upgrade pip\n")

    ssh.stdin.write(f"echo Install requirements\n")
    ssh.stdin.write(f"pip install -qr {requirements}\n")

    ssh.stdin.write(f"echo Checking environment \n")
    ssh.stdin.write(f"ls -la activate\n")
    ssh.stdin.write(f"which python\n")
    ssh.stdin.write(f"which pip\n")

    ssh.stdin.close()

    # Fetch output
    for line in ssh.stdout:
        outstr = line.strip()
        print(f"pyconf> {outstr}")


def main():
    print("pyconf> Setup python virtual machine")
    try:
        with open(PYCONF, "r") as confFile:
            print(f"pyconf> reading configuration file: {PYCONF}")
            jsonConf = json.load(confFile)
            req_file = jsonConf["requirements"]
            virtual_manager = jsonConf["virtual_manager"]
            virtual_home = jsonConf["virtual_home"]
            virtual_name = jsonConf["virtual_name"]
            virtual_env = f"{virtual_home}/{virtual_name}"
            virtual_bin = f"{virtual_env}/bin/activate"

            if not isFileExist(req_file):
                raise FileNotFoundError(f"File not found: {req_file}")

            if not isFileExist(f"{virtual_env}"):
                print(f"pyconf> Virtual Env {virtual_env} not exist!")
                create_virt_env(virtual_env, virtual_manager)

            if isFileExist(virtual_bin):
                create_symlink(virtual_bin)
                update_py_conf(virtual_bin, req_file)
                print(
                    "pyconf> Done. Use the command below to activate"
                    "\npyconf>"
                    "\npyconf>\t$ source activate"
                    "\npyconf>")
            else:
                print(
                    f"ERROR> missing python virtual home directory: {virtual_env}")

    except FileNotFoundError as notFoundError:
        print(f"ERROR> {notFoundError}")

    except Exception as otherError:
        print(f"ERROR> other error: {otherError}")


if __name__ == "__main__":
    main()
