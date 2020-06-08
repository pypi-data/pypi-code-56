import logging
import os
import re
import subprocess
import time

LSBLK_PATTERN = re.compile(r'^(sd[a-z]+\d+)\s+exfat\s+(.+?)(?:\s+(/.+))?$')

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
                mount_path = os.path.join('/media', info['uuid'])
                if not os.path.exists(mount_path):
                    os.makedirs(mount_path)

                if not os.path.isdir(mount_path):
                    logger.warning('Unable mount to {} (it is not a directory)')
                    continue

                logger.info('Mounting: {} to {}'.format(device, mount_path))
                cmd = ['mount', '-t', 'exfat', device, mount_path]
                subprocess.check_call(cmd)

        time.sleep(1)


def start_mounting_service():
    if os.getuid() != 0:
        logger.warning('Automatic mounting service disable because service not running as root')
        return

    _monitor_devices()
