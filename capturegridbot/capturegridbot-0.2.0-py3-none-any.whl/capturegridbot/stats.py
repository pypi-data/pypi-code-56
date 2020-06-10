import os
from typing import Optional

ACTIVE_CAMERA_STATES = ('Ready', 'Busy')


class CameraStats:
    def __init__(self, status: Optional[dict] = None):
        self.total_cameras = 0
        self.active_cameras = 0

        # parse the status response
        if status is not None:
            all_camera_states = list(map(
                lambda x: x.get('CameraStatus', ''),
                status.get('CameraInfo', []),
            ))

            self.total_cameras = len(all_camera_states)
            self.active_cameras = len(list(filter(lambda x: x in ACTIVE_CAMERA_STATES, all_camera_states)))

    def __eq__(self, other: 'CameraStats'):
        return self._as_tuple() == other._as_tuple()

    def __ne__(self, other):
        return not self.__eq__(other)

    def _as_tuple(self):
        return self.total_cameras, self.active_cameras


class PhotoStats:
    def __init__(self, status: Optional[dict] = None):
        self.total_photos = 0

        if status is not None:
            photos = status.get('PhotoInfo', [])

            for photo in photos:
                if photo.get('PhotoLocation', '') == 'Local Disk':
                    photo_path = photo.get('PhotoFilename', '')
                    if photo_path.startswith('/media') and os.path.isfile(photo_path):
                        self.total_photos += 1

    def __eq__(self, other: 'PhotoStats'):
        return self._as_tuple() == other._as_tuple()

    def __ne__(self, other: 'PhotoStats'):
        return not self.__eq__(other)

    def _as_tuple(self):
        return (self.total_photos,)
