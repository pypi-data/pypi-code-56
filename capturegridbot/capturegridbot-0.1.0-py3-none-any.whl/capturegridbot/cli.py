import argparse
import logging
import os
import re
import subprocess
import sys
import threading
import time
from logging.handlers import SysLogHandler
from queue import Queue, Empty

from .capturegrid import Api
from .config import Config
from .events import send_drive_update
from .mounting import start_mounting_service
from .service import install_service, uninstall_service

CONFIG_PATH = os.path.expanduser('~/.capturegridbot')


def scan_for_removable_drives():
    removable_drives = set()

    # Use the `df` command to look for all the removable drives that are on the system.
    output = subprocess.check_output(['df']).decode()
    for line in output.splitlines():
        match = re.match(r'^.*% (/.*)$', line)
        if match is not None:
            path = match.group(1)

            # we are only interested in the mounts that are in the media folder - this is a little bit of an assumption
            # but should be the case for the Pi version.
            if path.startswith('/media'):
                removable_drives.add(path)

    return removable_drives


def monitor_removable_drives(event_queue: Queue):
    logger = logging.getLogger('DriveMonitor')
    current_drives = set()  # set of drives from last poll
    selected_destination = ''  # the last selected photo destination

    while True:

        # work out what the next items on the system are
        next_drives = scan_for_removable_drives()

        # log all drive updates for the user
        for drive_path in next_drives - current_drives:
            logger.info('Detected new drive: {}'.format(drive_path))
        for drive_path in current_drives - next_drives:
            logger.info('Detected drive loss: {}'.format(drive_path))

        # detect changes to the device
        if len(next_drives) == 1:
            candidate_drive = list(next_drives)[0]
            if candidate_drive != selected_destination:
                selected_destination = candidate_drive
                logger.info('Switch to removable storage drive: {}'.format(selected_destination))
                send_drive_update(event_queue, selected_destination)

        else:

            # case where the previously selected drive is no longer present
            if selected_destination not in next_drives:
                if selected_destination == '':
                    logger.info('Waiting for removable storage drive')

                else:
                    logger.info('Lost in-use removable storage drive: {}'.format(selected_destination))
                    selected_destination = ''  # empty string signals the drive has been lost
                    send_drive_update(event_queue, selected_destination)

        # update the state
        current_drives = next_drives
        time.sleep(5)


def start_removable_drives_monitor(event_queue: Queue):
    t = threading.Thread(target=monitor_removable_drives, args=(event_queue,))
    t.daemon = True
    t.start()


def run():
    logger = logging.getLogger('Engine')
    cfg = Config(os.path.join(CONFIG_PATH, 'settings.toml'))
    event_queue = Queue()

    # start the internal services
    start_mounting_service()
    start_removable_drives_monitor(event_queue)

    api = Api(event_queue)
    download_path = cfg.override_destination or ''
    total_cameras = 0
    while True:

        # Step 1. Process any of the events that our program has been sent. Currently this is just updates for
        #         removable drives
        try:
            while True:
                event = event_queue.get(timeout=2)
                event_type = event.get('type')

                # process the drive update events
                if event_type == 'DriveUpdate' and cfg.override_destination is None:
                    download_path = event['destination']
                    if download_path != '':
                        download_path = os.path.join(download_path, cfg.output_folder_name)
                        os.makedirs(download_path, exist_ok=True)
                elif event_type == 'DownloadStarted':
                    logger.info('Download of "{}" started'.format(event['key']))
                elif event_type == 'DownloadComplete':
                    logger.info('Download of "{}" complete: {}'.format(event['key'], event['path']))
                elif event_type == 'CameraUpdate':
                    logger.info('Camera "{}" : {}'.format(event['key'], event['status']))

        except Empty:
            pass  # we don't mind!

        # Step 2. Ensure that capture grid is configured as we want it to

        # Download the status of the daemon
        success, status = api.sync()
        if success:

            # detect changes in the number of cameras
            next_total_cameras = len(status.get('CameraInfo', []))
            if next_total_cameras != total_cameras:
                logger.info('Total number of cameras: {}'.format(next_total_cameras))
                total_cameras = next_total_cameras

            # detect changes between the daemon download path and the bots download path
            if download_path != '':
                if download_path != status['OptionsInfo']['DownloadPath']:
                    logger.info('Updating download path to: {}'.format(download_path))
                    api.set_download_path(download_path)
                if download_path != status['OptionsInfo']['FallbackPath']:
                    logger.info('Updating fallback path to: {}'.format(download_path))
                    api.set_fallback_path(download_path)

        # Step 3. Control over shooting?
        # TBD


def parse_commandline():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--foreground', action='store_true', help='Run the application in the foreground')
    parser.add_argument('--install', action='store_true', help='Installs the bot as a service on your system')
    parser.add_argument('--uninstall', action='store_true', help='Uninstalls the bot as a service on your system')
    return parser.parse_args()


def configure_foreground_logging():
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                        datefmt='%m-%d %H:%M')


def configure_daemon_logging():
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    def add_handler(handler: logging.Handler):
        handler.setLevel(logging.DEBUG)
        root_logger.addHandler(handler)

    # create the syslog handler if running as root
    if os.getuid() == 0:
        slh = logging.handlers.SysLogHandler(
            facility=logging.handlers.SysLogHandler.LOG_DAEMON,
            address="/dev/log"
        )
        slh.setFormatter(logging.Formatter('%(name)s %(levelname)s %(message)s'))
        add_handler(slh)

    # create the local file handler
    logging_path = os.path.join(CONFIG_PATH, 'logs', 'capturegridbot.log')
    os.makedirs(os.path.dirname(logging_path), exist_ok=True)
    fh = logging.FileHandler(logging_path, mode='w')
    fh.setFormatter(logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s', datefmt='%m-%d %H:%M'))
    add_handler(fh)


def main():
    exit_code = 1

    # parse the command line
    args = parse_commandline()
    if args.foreground:
        configure_foreground_logging()
    else:
        configure_daemon_logging()

    # handle service install / uninstall
    if args.install:
        install_service()
        return

    elif args.uninstall:
        uninstall_service()
        return

    while True:
        try:
            run()
            exit_code = 0
        except KeyboardInterrupt:
            break  # stop the program if we ctrl + c
        except Exception:
            logging.exception('Internal error:')

        if args.foreground:
            break

    if exit_code != 0:
        sys.exit(exit_code)
