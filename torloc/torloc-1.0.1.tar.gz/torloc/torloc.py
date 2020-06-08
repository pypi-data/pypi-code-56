#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import os
import sys
import time
import zipfile
import threading
import subprocess
import pkg_resources
from tempfile import TemporaryDirectory, TemporaryFile

import requests


temp_dir_obj = TemporaryDirectory()
TEMP_DIR = temp_dir_obj.name


class TorProcess:
    def __init__(self, port):
        print("Starting", port)
        self.port = port
        self.ip = ''

        self.process = None
        self.stdout = TemporaryFile(mode='w', encoding='utf-8', prefix=f'stdout_{self.port}', dir=TEMP_DIR)
        self.stderr = TemporaryFile(mode='w', encoding='utf-8', prefix=f'stderr_{self.port}', dir=TEMP_DIR)

        self._start()

    def stop(self):
        self.process.kill()

    def _get_ip(self):
        proxies = {'http': f'socks5://localhost:{self.port}', 'https': f'socks5://localhost:{self.port}'}
        while not self.ip:
            try:
                self.ip = requests.get('http://icanhazip.com', proxies=proxies).text.strip()
                print("Ready", self.port)
            except requests.exceptions.ConnectionError:
                time.sleep(1)

    def _start(self):
        if sys.platform == 'win32':
            self.process = subprocess.Popen([
                f'{TEMP_DIR}/Tor/tor.exe',
                '-SOCKSPort', str(self.port),
                '-DataDirectory', f'{TEMP_DIR}/Data_{self.port}'
            ], stdout=self.stdout, stderr=self.stderr)
        else:
            self.process = subprocess.Popen([
                'tor',
                '-SOCKSPort', str(self.port),
                '-DataDirectory', f'{TEMP_DIR}/Data_{self.port}'
            ], stdout=self.stdout, stderr=self.stderr)

        get_ip_process = threading.Thread(target=self._get_ip)
        get_ip_process.start()


class CreateMany:
    def __init__(self, number_of_ports, threads=8):
        self.threads = threads
        self.number_of_ports = number_of_ports
        self.ports = {}

        self.ready = False

        self._create()

        readiness_check_process = threading.Thread(target=self._readiness_check)
        readiness_check_process.start()

    def stop(self, port):
        self.ports[port].stop()

    def stop_all(self):
        for process in self.ports.values():
            process.stop()

    def _readiness_check(self):
        while not self.ready:
            if '' not in [process.ip for process in self.ports.values()]:
                self.ready = True
            else:
                time.sleep(1)

    def _create(self):
        for port in range(49152, 49152 + self.number_of_ports):
            while [process.ip for process in self.ports.values()].count('') == self.threads:
                pass
                time.sleep(1)
            self.ports[port] = TorProcess(port)


def _download_win_32():
    download_page = requests.get('https://www.torproject.org/download/tor/')

    tor_url = 'https://www.torproject.org'
    tor_url += re.findall(r'"/dist/torbrowser/.*/tor-win32-.*.zip"', download_page.text)[0][1:-1]

    tor_zip = requests.get(tor_url)

    zip_path = pkg_resources.resource_filename('torloc', 'tor_win32.zip')
    zip_file = open(zip_path, 'wb')
    zip_file.write(tor_zip.content)


def init():
    if sys.platform == 'win32':
        if not os.path.exists(pkg_resources.resource_filename('torloc', 'tor_win32.zip')):
            _download_win_32()
        zip_file = zipfile.ZipFile(pkg_resources.resource_filename('torloc', f'tor_win32.zip'), 'r')
        zip_file.extractall(TEMP_DIR)

    else:
        if not os.path.exists('/usr/local/bin/tor') and not os.path.exists('/usr/bin/tor'):
            sys.stderr.write("Please install tor package via package manager")
            sys.exit(1)


if __name__ == '__main__':
    init()
