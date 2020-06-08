"""ansible-repo is a command which allowed ansible to download a git repository and run it as a playbook

Usage:
  ansible-repo <repo> <tag> [-e <env_vars>] [-vvv]
  ansible-repo <repo> <tag> -i <inventory> [-e <env_vars>] [-vvv]

Option:
  -v	verbose
  -i    inventory
  -e    Ansible environment variables
"""
import shutil
import uuid
import subprocess

from docopt import docopt


def main():
    try:
        main_fun()
    except KeyboardInterrupt:
        pass


def main_fun():
    args = docopt(__doc__)

    TAG = args['<tag>']
    REPO = args['<repo>']
    INVENTORY = args['<inventory>'] if args['<inventory>'] else False
    ENV_VARS = args['<env_vars>'] if args['<env_vars>'] else False
    VERBOSE = True if args['-v'] else False
    TMP_DIR = f'/tmp/ansible_repo.{uuid.uuid4()}'

    # git clone -b $2 $1 $tmp_dir
    GIT_CMD = f'git clone -b {TAG} {REPO} {TMP_DIR}'
    ANSIBLE_CMD = 'ansible-playbook -i {inv} {playbook}'.format(
        inv=INVENTORY if INVENTORY else f'{TMP_DIR}/inventory.yml',
        playbook=f'{TMP_DIR}/playbook.yml',
    )
    ANSIBLE_CMD_SPLITTED = ANSIBLE_CMD.split(' ')

    if ENV_VARS:
        ANSIBLE_CMD_SPLITTED.append('-e')
        ANSIBLE_CMD_SPLITTED.append(ENV_VARS)

    if VERBOSE:
        ANSIBLE_CMD_SPLITTED.append('-vvv')

    p = subprocess.run(
        GIT_CMD.split(' '),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    if p.returncode != 0:
        exit('Failed to clone the repository')

    p = subprocess.run(
        ANSIBLE_CMD_SPLITTED,
        # stdout=subprocess.DEVNULL,
        # stderr=subprocess.DEVNULL
    )
    if p.returncode != 0:
        shutil.rmtree(TMP_DIR)
        exit('Ansible command failed')

    # REMOVE TMP DIRECTORY
    shutil.rmtree(TMP_DIR)


if __name__ == '__main__':
    main()
