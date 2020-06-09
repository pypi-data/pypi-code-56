# -*- coding: utf-8 -*-
"""
RoboMentor_Client: Python library and framework for RoboMentor_Client.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
:copyright: (c) 2020 by RoboMentor.
:license: MIT, see LICENSE for more details.
"""

import cv2,os,fcntl,v4l2
from .filters import bgr2yuyv
from multiprocessing import Process,Queue,Value
from ctypes import c_bool

virtual = lambda f: f

class Camera(Process):

    def __init__(self, in_dev_name='/dev/video0', out_dev_name='/dev/video1', flip=False, queue=False):
        Process.__init__(self)
        self.in_dev = None
        self.out_dev = None
        self.in_dev_name = in_dev_name
        self.out_dev_name = out_dev_name
        self.flip = flip
        self.running = Value(c_bool)
        self.queue = Queue(4) if queue else None

    def setup(self):

        self.in_dev = cv2.VideoCapture(self.in_dev_name)
        ok, im = self.in_dev.read()
        if not ok:
            raise IOError('Unable to read frames from device %s' % self.in_dev_name)

        height, width, _ = im.shape
        channels = 2

        if not os.path.exists(self.out_dev_name):
            raise IOError('Device %s does not exist' % self.out_dev_name)
        self.out_dev = open(self.out_dev_name, 'wb')

        capability = v4l2.v4l2_capability()
        print('Get capabilities result: %s' % (fcntl.ioctl(self.out_dev, v4l2.VIDIOC_QUERYCAP, capability)))
        print('Capabilities: %s' % hex(capability.capabilities))
        print('V4l2 driver: %s' % capability.driver.decode())

        fmt = v4l2.v4l2_format()
        fmt.type = v4l2.V4L2_BUF_TYPE_VIDEO_OUTPUT
        fmt.fmt.pix.field = v4l2.V4L2_FIELD_NONE
        fmt.fmt.pix.pixelformat = v4l2.V4L2_PIX_FMT_YUYV
        fmt.fmt.pix.width = width
        fmt.fmt.pix.height = height
        fmt.fmt.pix.bytesperline = width * channels
        fmt.fmt.pix.sizeimage = width * height * channels
        fmt.fmt.pix.colorspace = v4l2.V4L2_COLORSPACE_SRGB
        print('Set format result: %d' % fcntl.ioctl(self.out_dev, v4l2.VIDIOC_S_FMT, fmt))

    def start(self):

        self.running.value = True
        self.setup()

        while self.running.value:
            ok, src = self.in_dev.read()
            if not ok:
                continue

            tr = self.transform(src)
            if self.flip:
                tr = cv2.flip(tr, 1)

            tgt = bgr2yuyv(tr)

            self.out_dev.write(tgt)
            if self.queue is not None and self.queue.qsize() <= self.queue.maxsize - 2:
                self.queue.put(src)
                self.queue.put(tr)

        self.release()

    def release(self):
        self.in_dev.release()
        self.out_dev.close()
        print('cameras are closed')

    def stop(self):
        self.running.value = False

    def __del__(self):
        del self

    @virtual
    def transform(self, bgr_frame):
        return bgr_frame