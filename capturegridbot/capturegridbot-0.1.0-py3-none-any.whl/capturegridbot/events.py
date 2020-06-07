from queue import Queue


def send_drive_update(q: Queue, destination: str):
    q.put({
        'type': 'DriveUpdate',
        'destination': destination,
    })


def send_download_started(q: Queue, key: str):
    q.put({
        'type': 'DownloadStarted',
        'key': key,
    })


def send_download_complete(q: Queue, key: str, path: str):
    q.put({
        'type': 'DownloadComplete',
        'key': key,
        'path': path,
    })


def send_camera_update(q: Queue, key: str, status: str):
    q.put({
        'type': 'CameraUpdate',
        'key': key,
        'status': status,
    })