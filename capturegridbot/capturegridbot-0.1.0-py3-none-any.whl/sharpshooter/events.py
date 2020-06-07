from queue import Queue


def send_drive_update(q: Queue, destination: str):
    q.put({
        'type': 'DriveUpdate',
        'destination': destination,
    })
