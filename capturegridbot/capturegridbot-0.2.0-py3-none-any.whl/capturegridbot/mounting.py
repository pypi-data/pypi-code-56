import logging
import os
import re
import subprocess
import threading
import time

LSBLK_PATTERN = re.compile(r'^(sd[a-z]+\d+)\s+exfat\s+(.+?)(?:\s+(/.+))?$')
NUM_DIRECTORY_ATTEMPTS = 256

logger = logging.getLogger('MountingSrv')


def _get_block_devices():
    devices = {}

    output = subprocess.check_output(['lsblk', '-fl']).decode().strip()
    for line in output.splitlines():
        match = LSBLK_PATTERN.match(line.strip())
        if match is not None:
            device, uuid, mount_point = match.groups()
            device = '/dev/{}'.format(device)  # make an actual device file

            devices[device] = {
                'uuid': uuid,
                'mount': mount_point,
            }

    return devices


def _monitor_devices():
    while True:
        # get the current devices
        devices = _get_block_devices()

        for device, info in devices.items():
            if info['mount'] is None:

                mount_success = False
                for index in range(NUM_DIRECTORY_ATTEMPTS):

                    # derive the mount path
                    mount_path = os.path.join('/media', info['uuid'])
                    if index > 0:
                        mount_path += '-{}'.format(index)

                    # make the folder if it doesn't already exists
                    if not os.path.exists(mount_path):
                        os.makedirs(mount_path)

                    # skip any already populated folders
                    if len(os.listdir(mount_path)) != 0:
                        continue  # try another index

                    # attempt to mount the drive
                    logger.info('Mounting: {} to {}'.format(device, mount_path))
                    cmd = ['mount', '-t', 'exfat', device, mount_path]
                    subprocess.check_call(cmd)

                    mount_success = True
                    break

                if not mount_success:
                    logger.error('Unable mount device: {}'.format(device))
                    continue

        time.sleep(1)


def start_mounting_service():
    if os.getuid() != 0:
        logger.warning('Automatic mounting service disable because service not running as root')
        return

    # start the monitor devices thread
    t = threading.Thread(target=_monitor_devices)
    t.daemon = True
    t.start()
