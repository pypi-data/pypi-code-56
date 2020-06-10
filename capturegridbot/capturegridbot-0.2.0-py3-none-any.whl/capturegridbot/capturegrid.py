import logging
import threading
from queue import Queue
from typing import Optional, Tuple

import zmq

from .events import send_download_started, send_download_complete, send_camera_update


class Api:
    def __init__(self, event_queue: Optional[Queue] = None):
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

    def get_download_path(self, state: Optional[dict] = None) -> Optional[str]:
        state = self._ensure_state(state)
        if state is not None:
            state = state['OptionsInfo']['DownloadPath']
        return state

    def set_download_path(self, download_path: str) -> bool:
        success, _ = self._send_request('SetOptions', {
            'DownloadPath': download_path,
        })
        return success

    def get_fallback_path(self, state: Optional[dict] = None) -> Optional[str]:
        state = self._ensure_state(state)
        if state is not None:
            state = state['OptionsInfo']['FallbackPath']
        return state

    def set_fallback_path(self, download_path: str) -> bool:
        success, _ = self._send_request('SetOptions', {
            'FallbackPath': download_path,
        })
        return success

    def get_filename_expression(self, state: Optional[dict] = None) -> Optional[str]:
        state = self._ensure_state(state)
        if state is not None:
            state = state['OptionsInfo']['FilenameExpression']
        return state

    def set_filename_expression(self, filename_expression: str) -> bool:
        success, _ = self._send_request('SetOptions', {
            'FilenameExpression': filename_expression,
        })
        return success

    def get_auto_connect(self, state: Optional[dict] = None) -> Optional[bool]:
        state = self._ensure_state(state)
        if state is not None:
            state = state['OptionsInfo']['AutoConnect']
        return state

    def set_auto_connect(self, auto_connect: bool) -> bool:
        success, _ = self._send_request('SetOptions', {
            'AutoConnect': auto_connect,
        })
        return success

    def get_auto_synchronise_time(self, state: Optional[dict] = None) -> Optional[bool]:
        state = self._ensure_state(state)
        if state is not None:
            state = state['OptionsInfo']['AutoSynchroniseTime']
        return state

    def set_auto_synchronise_time(self, auto_synchronise_time: bool) -> bool:
        success, _ = self._send_request('SetOptions', {
            'AutoSynchroniseTime': auto_synchronise_time,
        })
        return success

    def trigger_all(self) -> bool:
        success, _ = self._send_request('Shoot', {
            'CameraSelection': 'All'
        })
        return success

    def _ensure_state(self, state: Optional[dict]) -> Optional[dict]:
        if state is not None:
            return state

        # attempt to lookup the state
        success, state = self.sync()
        if not success:
            return None

        return state

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
                camera_key = msg.get('CameraKey', '')
                camera_status = msg.get('CameraStatus', '')

                # suppress update events about camera focus updates etc.
                if camera_key != '' and camera_status != '':
                    send_camera_update(self._queue, camera_key, camera_status)
