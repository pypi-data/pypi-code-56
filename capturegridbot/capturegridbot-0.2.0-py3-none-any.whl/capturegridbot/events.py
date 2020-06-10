from queue import Queue
from typing import Optional


def send_drive_update(q: Optional[Queue], destination: str):
    if q is None:
        return

    q.put({
        'type': 'DriveUpdate',
        'destination': destination,
    })


def send_download_started(q: Optional[Queue], key: str):
    if q is None:
        return

    q.put({
        'type': 'DownloadStarted',
        'key': key,
    })


def send_download_complete(q: Optional[Queue], key: str, path: str):
    if q is None:
        return

    q.put({
        'type': 'DownloadComplete',
        'key': key,
        'path': path,
    })


def send_camera_update(q: Optional[Queue], key: str, status: str):
    if q is None:
        return

    q.put({
        'type': 'CameraUpdate',
        'key': key,
        'status': status,
    })