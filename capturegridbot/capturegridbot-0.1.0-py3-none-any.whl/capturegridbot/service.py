import os
import subprocess

SYSTEMD_SERVICE_TEMPLATE = """[Unit]
Description=Capture Grid Bot
After=snap.capturegrid4.node.service

[Service]
ExecStart="/usr/local/bin/capturegridbotd"
User=root
TimeoutSec=30
Restart=on-failure
RestartSec=30
StartLimitInterval=350
StartLimitBurst=10

[Install]
WantedBy=multi-user.target
"""

SYSTEMD_SERVICE_FILE = '/etc/systemd/system/capturegridbot.service'


def install_service():
    # ensure the service file is correct
    with open(SYSTEMD_SERVICE_FILE, 'w') as service_file:
        service_file.write(SYSTEMD_SERVICE_TEMPLATE)

    # remove the system
    cmd = ['systemctl', 'daemon-reload']
    subprocess.check_call(cmd)

    # start the bot service
    cmd = ['systemctl', 'start', 'capturegridbot']
    subprocess.check_call(cmd)

    # enable at boot
    cmd = ['systemctl', 'enable', 'capturegridbot']
    subprocess.check_call(cmd)


def uninstall_service():
    if os.path.exists(SYSTEMD_SERVICE_FILE):
        # stop the running service
        cmd = ['systemctl', 'stop', 'capturegridbot']
        subprocess.call(cmd)

        # remove the service
        os.remove(SYSTEMD_SERVICE_FILE)

        # remove the system
        cmd = ['systemctl', 'daemon-reload']
        subprocess.check_call(cmd)
