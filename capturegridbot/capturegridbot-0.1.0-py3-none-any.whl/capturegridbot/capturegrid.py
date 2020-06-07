import logging
import threading
from typing import Optional, Tuple
from queue import Queue

import zmq

from .events import send_download_started, send_download_complete, send_camera_update


class Api:
    def __init__(self, event_queue: Queue):
        self._queue = event_queue
        self._ctx = zmq.Context()
        self._req = self._ctx.socket(zmq.REQ)
        self._req.connect('tcp://127.0.0.1:54544')
        self._req_counter = 0
        self._sub = self._ctx.socket(zmq.SUB)
        self._sub.setsockopt(zmq.SUBSCRIBE, b"")
        self._sub.connect('tcp://127.0.0.1:54543')
        self._logger = logging.getLogger('CaptureGridApi')

        # create the event monitor thread
        self._event_monitor_thread = threading.Thread(target=self._event_monitor)
        self._event_monitor_thread.daemon = True
        self._event_monitor_thread.start()

    def sync(self) -> Tuple[bool, dict]:
        return self._send_request('Synchronise')

    def get_download_path(self) -> Optional[str]:
        success, state = self.sync()
        if not success:
            return None
        return state['OptionsInfo']['DownloadPath']

    def set_download_path(self, download_path: str) -> bool:
        success, _ = self._send_request('SetOptions', {
            'DownloadPath': download_path,
        })
        return success

    def get_fallback_path(self) -> Optional[str]:
        success, state = self.sync()
        if not success:
            return None
        return state['OptionsInfo']['FallbackPath']

    def set_fallback_path(self, download_path: str) -> bool:
        success, _ = self._send_request('SetOptions', {
            'FallbackPath': download_path,
        })
        return success

    def trigger_all(self) -> bool:
        success, _ = self._send_request('Shoot', {
            'CameraSelection': 'All'
        })
        return success

    def _send_request(self, endpoint, data: Optional[dict] = None) -> Tuple[bool, dict]:
        r = {
            'msg_type': 'Request',
            'msg_id': endpoint,
            'msg_seq_num': self._req_counter,
        }
        self._req_counter += 1

        # add the custom user data to the message
        if data is not None:
            r.update(data)

        # send the message
        self._req.send_json(r)

        # get the response
        resp = self._req.recv_json()

        success = resp.get('msg_result', False)
        if not success:
            self._logger.warning('Failed to send request to {} endpoint'.format(endpoint))
            print(resp)

        return success, resp

    def _event_monitor(self):
        while True:
            msg = self._sub.recv_json()

            if msg['msg_id'] == 'PhotoUpdated':
                photo_key = msg.get('PhotoKey')
                download_path = msg.get('PhotoFilename', '')
                if download_path == '':
                    send_download_started(self._queue, photo_key)
                else:
                    send_download_complete(self._queue, photo_key, download_path)
            elif msg['msg_id'] == 'CameraUpdated':
                send_camera_update(self._queue, msg.get('CameraKey', ''), msg.get('CameraStatus', ''))
