import os

import numpy as np
import cv2
import imageio

from skcvideo.utils import StoredImagesVideoCapture, BLACK, WHITE, RED


FONT = cv2.FONT_HERSHEY_PLAIN


TIMELINE_MIN = 585
TIMELINE_MAX = 1845
TIMELINE_LEN = TIMELINE_MAX - TIMELINE_MIN


GRAY_BAR = np.array([[189, 189, 190],
                     [193, 193, 194],
                     [196, 197, 198],
                     [200, 201, 202],
                     [204, 205, 206],
                     [208, 208, 209],
                     [212, 212, 213],
                     [215, 216, 217],
                     [219, 220, 221],
                     [235, 235, 236]])

BLUE_BAR = np.array([[224, 137, 44],
                     [218, 134, 43],
                     [213, 130, 42],
                     [207, 127, 41],
                     [204, 125, 40],
                     [204, 125, 40],
                     [204, 125, 40],
                     [204, 125, 40]])


def put_text(im, text, pos, color=WHITE, scale=1):
    cv2.putText(im, text, pos, FONT, scale, BLACK, scale + 1)
    cv2.putText(im, text, pos, FONT, scale, color, scale)


class Button(object):
    """
    Used to define a clickable button on the image executing a given callback
    when cliked. Some data specifying the button can be passed at the object
    creation. 

    Args:
        - hitbox: tuple (x1, y1, x2, y2) the bounding box of the clickable area. 
        - callback: a function taking x, y (the coordinates of the click) and
          optionnaly data as arguments.
        - data (optionnal): data of any shape that will be used by the callback.
    """
    def __init__(self, hitbox, callback, data=None):
        self.hitbox = hitbox
        self.data = data
        self.given_callback = callback

    def callback(self, *kwargs):
        if self.data is None:
            return self.given_callback(*kwargs)
        else:
            return self.given_callback(self.data, *kwargs)


class Reader(StoredImagesVideoCapture):
    """
    A video displayer that allows interaction with the image by using buttons
    or keyboard.

    The main advantage of this displayer is that it allows to read the video
    backward while keeping relatively fast. 

    The best way to use this displayer is to make your own class inheriting
    from this one and overridding its methods. 
    """
    def __init__(self, video_path, **kwargs):
        self.resize_window = kwargs.pop('resize_window', True)
        self.vlc_timeline = kwargs.pop('vlc_timeline', False)
        super(Reader, self).__init__(video_path, colormap='bgr', **kwargs)

        self.to_exit = False

        # The key/function mapping
        self.keydict = {'k': self.next,
                        'j': self.previous,
                        'q': self.exit}

        # The clickable buttons
        self.buttons = []

        if self.vlc_timeline:
            self.buttons.append(Button((79, 966, 1771, 976), self.jump_event))
        else:
            self.n_timelines = (self.max_frame - self.min_frame) / TIMELINE_LEN + 1
            hitbox = (TIMELINE_MIN, 730, TIMELINE_MAX, 730 + self.n_timelines * 30)
            self.buttons.append(Button(hitbox, self.jump_event))
        self.background = self._create_background()

        self.init(video_path, **kwargs)

        self._refresh()

        # Resizes the display panel, set it to False if you want to work with
        # the undistorted image. 
        if self.resize_window:
            cv2.namedWindow("image", cv2.WINDOW_NORMAL)
            cv2.resizeWindow("image", 1280, 720)
        else:
            cv2.namedWindow("image")
        cv2.setMouseCallback("image", self.click_event)

    def init(self, video_path, **kwargs):
        pass

    @property
    def image_to_disp(self):
        """
        This property specifies the image to be displayed. You would override
        it at your convenience e.g. to only display a subpart of the global
        image.
        """
        return self.big_image

    def next(self):
        super(Reader, self).next()
        self._refresh()

    def previous(self):
        super(Reader, self).previous()
        self._refresh()

    def exit(self):
        self.to_exit = True

    def _create_background(self):
        """
        Here you define the elements of the image that don't change throughout
        the video or manipulations. 
        """
        if self.vlc_timeline:
            im = np.zeros((980, 1855, 3), dtype=np.uint8)
            im[-18:] = np.array([240, 241, 242])[np.newaxis, np.newaxis, :]
            im[-14:-4, 79:1771] = GRAY_BAR[:, np.newaxis, :]
        else:
            def draw_timeline_box(im, i):
                y_min = 740 + i * 30
                y_max = y_min + 10
                if i == self.n_timelines - 1:
                    frame_max = (self.max_frame - self.min_frame) % TIMELINE_LEN
                    timeline_max = TIMELINE_MIN + frame_max
                else:
                    timeline_max = TIMELINE_MAX
                cv2.rectangle(im, (TIMELINE_MIN, y_min), (timeline_max, y_max),
                    color=WHITE, thickness=1)

            im = np.zeros((740 + self.n_timelines * 30, 1855, 3), dtype=np.uint8)
            for i in range(self.n_timelines - 1):
                draw_timeline_box(im, i)

            i = self.n_timelines - 1
            draw_timeline_box(im, i)
            self.draw_timeline_data(im)
        im = self.draw_background(im)
        return im

    def draw_background(self, im):
        return im

    def draw_timeline_data(self, im):
        """
        Draws information on the timeline. Useful to have a global view of
        your data or to have a reference for jumping in the video. 
        """
        for frame in range(self.min_frame, self.max_frame):
            color = self.timeline_color(frame)
            if color != (0, 0, 0):
                timer = frame - self.min_frame
                timer_x = timer % TIMELINE_LEN
                timer_y = timer / TIMELINE_LEN
                cv2.line(im, (TIMELINE_MIN + timer_x, timer_y * 30 + 741),
                    (TIMELINE_MIN + timer_x, timer_y * 30 + 749), color=color)

    def timeline_color(self, frame):
        """
        Here you define the color of the timeline with repect to the frame.
        """
        return (0, 0, 0)

    def jump_event(self, x, y, *kwargs):
        """
        Allows to click on the timeline to jump to another moment in the video.
        """
        if self.vlc_timeline:
            frames_length = float(self.max_frame - self.min_frame)
            pixels_length = 1771.0 - 79.0
            frame = (float(x) - 79.0) / pixels_length * frames_length + self.min_frame
            frame = int(np.round(frame))
        else:
            x = x - TIMELINE_MIN
            y = (y - 730) / 30
            frame = x + y * TIMELINE_LEN + self.min_frame
        self.jump(frame)

    def click_event(self, event, x, y, flags, param):
        """
        Part of the core engine that manages the buttons.

        /!\ Should not be overridden without knowing what you do. 
        """
        if event == cv2.EVENT_LBUTTONUP:
            if hasattr(self, 'buttons'):
                for button in self.buttons:
                    x1, y1, x2, y2 = button.hitbox
                    if x1 < x < x2 and y1 < y < y2:
                        button.callback(x, y)
            self._refresh()

    def _refresh(self):
        """
        Here you define the appearance of the image to be displayed with
        respect to structural elements such as the frame index. 

        It is called each time the user is interacting with the image
        (clicks, keys, previous, next, ...) to allow updating it with new
        information. 
        """
        self.big_image = self.background.copy()
        put_text(self.big_image, 'Frame {}'.format(self.frame), (20, 30), WHITE)
        self.draw_timer()
        self.refresh()
        image = self.image.copy()
        image = self.refresh_image(image)
        self.big_image[:720, 575:575+1280, :] = image

    def refresh(self):
        pass

    def refresh_image(self, image):
        return image

    def draw_timer(self):
        """
        Draws the timer mark to known where you are in the video. 
        """
        if self.vlc_timeline:
            i = (float(self.frame - self.min_frame)
               / float(self.max_frame - self.min_frame) * (1771.0 - 79.0) + 79.0)
            i = int(np.round(i))
            self.big_image[-13:-5, 79:i] = BLUE_BAR[:, np.newaxis, :]
        else:
            timer = self.frame - self.min_frame
            timer_x = timer % TIMELINE_LEN
            timer_y = timer / TIMELINE_LEN
            cv2.line(self.big_image, (TIMELINE_MIN + timer_x, timer_y * 30 + 730),
                (TIMELINE_MIN + timer_x, timer_y * 30 + 760), color=RED)

    def start(self):
        """
        Part of the core engine that manages the display of the image and the
        keys.

        /!\ Should not be overridden without knowing what you do. 
        """
        while not self.to_exit:
            cv2.imshow("image", self.image_to_disp)
            key = cv2.waitKey(1) & 0xFF
            for k, fun in self.keydict.items():
                if key == ord(k):
                    fun()

    def create_video(self, video_path='video.mp4'):
        if os.path.exists(video_path):
            print 'video_path already exists, overwite (y/n)?'
            answer = raw_input()
            if answer.lower() != 'y':
                return
        video = imageio.get_writer(video_path, 'ffmpeg', fps=10, quality=5.5)
        print 'Creating video...'
        for frame in range(self.min_frame, self.max_frame):
            sys.stdout.write('\r{}/{}'.format(frame - self.min_frame, self.max_frame - self.min_frame - 1))
            sys.stdout.flush()
            self.seek(frame)
            self._refresh()
            video.append_data(cv2.cvtColor(self.big_image, cv2.COLOR_BGR2RGB))
        sys.stdout.write('\n')
        sys.stdout.flush()
        print 'Done'
        video.close()


if __name__ == '__main__':
    import sys
    video_path = sys.argv[1]
    reader = Reader(video_path, fps=10, vlc_timeline=True, resize_window=True, min_frame=0, max_frame=1000)
    reader.create_video()
