# -*- coding: utf-8 -*-
"""
RoboMentor_Client: Python library and framework for RoboMentor_Client.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
:copyright: (c) 2020 by RoboMentor.
:license: MIT, see LICENSE for more details.
"""

import os, fcntl
from . import v4l2
from multiprocessing import Process, Queue, Value
from ctypes import c_bool

virtual = lambda f: f

class Camera(Process):

    def __init__(self, video='/dev/video0', queue=False):
        Process.__init__(self)
        self.video = video
        self.video_dev = None
        self.running = Value(c_bool)
        self.queue = Queue(4) if queue else None

    def start(self):
        self.running.value = True

        if not os.path.exists(self.video):
            raise IOError('Device %s does not exist' % self.video)
        self.video_dev = open(self.video, 'wb')

        capability = v4l2.v4l2_capability()
        print('Get capabilities result: %s' % (fcntl.ioctl(self.video_dev, v4l2.VIDIOC_QUERYCAP, capability)))
        print('Capabilities: %s' % hex(capability.capabilities))
        print('V4l2 driver: %s' % capability.driver.decode())

        mat = v4l2.v4l2_format()
        mat.type = v4l2.V4L2_BUF_TYPE_VIDEO_OUTPUT
        mat.fmt.pix.field = v4l2.V4L2_FIELD_NONE
        mat.fmt.pix.pixelformat = v4l2.V4L2_PIX_FMT_YUYV
        mat.fmt.pix.width = 1280
        mat.fmt.pix.height = 720
        mat.fmt.pix.bytesperline = 1280 * 2
        mat.fmt.pix.sizeimage = 1280 * 720 * 2
        mat.fmt.pix.colorspace = v4l2.V4L2_COLORSPACE_SRGB
        mat('Set format result: %d' % fcntl.ioctl(self.video_dev, v4l2.VIDIOC_S_FMT, mat))

        while self.running.value:
            ok, src = self.video_dev.read()
            if not ok:
                continue

            if self.queue is not None and self.queue.qsize() <= self.queue.maxsize - 2:
                self.queue.put(src)
                print(src)

        self.release()

    def release(self):
        self.video_dev.close()
        print('cameras are closed')

    @virtual
    def transform(self, bgr_frame):
        return bgr_frame
