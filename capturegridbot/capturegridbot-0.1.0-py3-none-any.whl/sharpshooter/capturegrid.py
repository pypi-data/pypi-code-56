import logging
from typing import Optional, Tuple

import zmq


class Api:
    def __init__(self):
        self._ctx = zmq.Context()
        self._req = self._ctx.socket(zmq.REQ)
        self._req.connect('tcp://127.0.0.1:54544')
        self._req_counter = 0
        self._logger = logging.getLogger('CaptureGridApi')

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
