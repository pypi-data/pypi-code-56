import math
import time
import ctypes
import pyautogui
import win32gui
import win32ui
import win32con
from pywinauto import application
from ctypes import windll
from PIL import Image, ImageGrab
from ctypes import wintypes

class CameraControlError(Exception):
    '''
    When Camera control goes into an infinite loop of trials and errors
    '''
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class Flight(object):
    def __init__(self, location):
        # window
        self.location = location
        self.fpp_key = 0
        self.top_key = 0
        self.title = 'drone_simulator'
        self.app = application.Application(backend='win32')
        self.app.connect(title=self.title)[0]
        self.win = self.app.window(title_re=self.title)
        self.coords = (0, 0, 0)
        self.angles = (0, 0, 0)

    def screenshot(self):
        # this takes care of the DPI settings (https://stackoverflow.com/questions/51786794/using-imagegrab-with-bbox-from-pywin32s-getwindowrect)
        ctypes.windll.user32.SetProcessDPIAware()

        # get window handle and dimensions 
        hwnd = win32gui.FindWindow(None, str(self.title))
        dimensions = win32gui.GetWindowRect(hwnd)    

        # this gets the window size, comparing it to `dimensions` will show a difference
        winsize = win32gui.GetClientRect(hwnd)

        # this sets window to front if it is not already
        win32gui.SetWindowPos(hwnd, win32con.HWND_NOTOPMOST,0,0,0,0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
        win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST,0,0,0,0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
        win32gui.SetWindowPos(hwnd, win32con.HWND_NOTOPMOST,0,0,0,0, win32con.SWP_SHOWWINDOW | win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)

        # grab screen region set in `dimensions`
        image = ImageGrab.grab(dimensions)
        #image.show()

        # we're going to use this to get window attributes
        f=ctypes.windll.dwmapi.DwmGetWindowAttribute

        # `rect` is for the window coordinates
        rect = ctypes.wintypes.RECT()
        DWMWA_EXTENDED_FRAME_BOUNDS = 9

        # and then the coordinates of the window go into `rect`
        f(ctypes.wintypes.HWND(hwnd),
        ctypes.wintypes.DWORD(DWMWA_EXTENDED_FRAME_BOUNDS),
        ctypes.byref(rect),
        ctypes.sizeof(rect)
        )

        # if we want to work out the window size, for comparison this should be the same as `winsize`
        size = (rect.right - rect.left, rect.bottom - rect.top)        

        # put the window coordinates in a tuple like that returned earlier by GetWindowRect()
        dimensions = (rect.left, rect.top, rect.right, rect.bottom)

        # grab screen region set in the revised `dimensions`
        image = ImageGrab.grab(dimensions)
        return image

    def fpp_shot(self):
        # add changes to unity to denote which camera is currently open
        # Also save LOG file to its own directory 
        if self.fpp_key % 2 == 0:
            self.fpp_view()
        shot = self.screenshot()
        self.fpp_view()
        return shot

    def top_shot(self):
        # add changes to unity to denote which camera is currently open
        # Also save LOG file to its own directory 
        if self.top_key % 2 == 0:
            self.top_view()
        shot = self.screenshot()
        self.top_view()
        return shot

    def tpp_shot(self):
        # add changes to unity to denote which camera is currently open
        # Also save LOG file to its own directory 
        if self.fpp_key % 2 == 0 and self.top_key % 2 == 0:
            # alreaady in tpp
            pass
        elif self.fpp_key % 2 == 0 and self.top_key % 2 != 0:
            # in top view
            self.top_view()
        elif self.fpp_key % 2 != 0 and self.top_key % 2 == 0:
            # in fpp view
            self.fpp_view()
        else:
            # mixed up
            self.fpp_view()
            self.top_view()
            #raise CameraControlError('''Might have viewed FPP and then suddenly Top View (vice versa), before exiting into TPP View, i.e, pressed "1 and then 2" or "2 and then 1 again".
            #                            Had to press "1, then again 1 to exit, and then, press 2''')
        return self.screenshot()


    def turn_left(self):
        #win.send_keystrokes('{w}')
        #win.send_keystrokes('{a}')
        #win.send_keystrokes('{s}')
        #win.send_keystrokes('{d}')
        #win.send_keystrokes('{i}')
        
        self.win.send_keystrokes('{j}')
        #win.send_keystrokes('{j}')
        #win.send_keystrokes('{k}')
        #win.send_keystrokes('{l}')
        print('Turn Left')

    def turn_right(self):
        #win.send_keystrokes('{w}')
        #win.send_keystrokes('{a}')
        #win.send_keystrokes('{s}')
        #win.send_keystrokes('{d}')
        #win.send_keystrokes('{i}')
        #win.send_keystrokes('{j}')
        #win.send_keystrokes('{k}')
        #win.send_keystrokes('{l}')
        self.win.send_keystrokes('{l}')
        print('Turn Right')

    def up(self):
        #win.send_keystrokes('{w}')
        #win.send_keystrokes('{a}')
        #win.send_keystrokes('{s}')
        #win.send_keystrokes('{d}')
        
        self.win.send_keystrokes('{i}')
        ##
        #win.send_keystrokes('{j}')
        #win.send_keystrokes('{k}')
        #win.send_keystrokes('{l}')
        print('Move up')

    def down(self):
        #win.send_keystrokes('{w}')
        #win.send_keystrokes('{a}')
        #win.send_keystrokes('{s}')
        #win.send_keystrokes('{d}')
        #win.send_keystrokes('{i}')
        #win.send_keystrokes('{j}')
        
        self.win.send_keystrokes('{k}')
        ##
        #win.send_keystrokes('{l}')
        print('Move down')

    def forward(self):
        
        self.win.send_keystrokes('{w}')
        ##
        #win.send_keystrokes('{a}')
        #win.send_keystrokes('{s}')
        #win.send_keystrokes('{d}')
        #win.send_keystrokes('{i}')
        #win.send_keystrokes('{j}')
        #win.send_keystrokes('{k}')
        #win.send_keystrokes('{l}')
        print('Go Forward')

    def backward(self):
        #win.send_keystrokes('{w}')
        #win.send_keystrokes('{a}')
        
        self.win.send_keystrokes('{s}')
        #
        #win.send_keystrokes('{d}')
        #win.send_keystrokes('{i}')
        #win.send_keystrokes('{j}')
        #win.send_keystrokes('{k}')
        #win.send_keystrokes('{l}')
        print('Go Backward')

    def swerve_left(self):
        #win.send_keystrokes('{w}')
        
        self.win.send_keystrokes('{a}')
        ##
        #win.send_keystrokes('{s}')
        #win.send_keystrokes('{d}')
        #win.send_keystrokes('{i}')
        #win.send_keystrokes('{j}')
        #win.send_keystrokes('{k}')
        #win.send_keystrokes('{l}')
        print('swerve Left')

    def swerve_right(self):
        #win.send_keystrokes('{w}') 
        #win.send_keystrokes('{a}')
        #win.send_keystrokes('{s}')
        
        self.win.send_keystrokes('{d}')
        ##
        #win.send_keystrokes('{i}')
        #win.send_keystrokes('{j}')
        #win.send_keystrokes('{k}')
        #win.send_keystrokes('{l}')
        print('swerve Right')

    def top_view(self):
        #win.send_keystrokes('{1}')
        self.win.send_keystrokes('{1}')
        self.top_key += 1
        print('Top View')

    def fpp_view(self):
        #win.send_keystrokes('{2}')
        self.win.send_keystrokes('{2}')
        self.fpp_key += 1
        print('FPP View')

    def coords_xyz(self):
        try:
            f = open(self.location + '/LOG', 'r')
            f.seek(0)
            self.coords, _ = f.read().split('\n')
            self.coords = tuple(map(float, self.coords.split()))
            return self.coords
        except:
            return self.coords

    def angles_xyz(self):
        try:
            f = open(self.location + '/LOG', 'r')
            f.seek(0)
            _, self.angles = f.read().split('\n')
            self.angles = tuple(map(float, self.angles.split()))
            return self.angles
        except:
            return self.angles

    def goto(self, x2, z2):
        ## if at the start x1 > x2, doesn't work
        # Main Loop
        while(True):
            try:
                coordinates = self.coords_xyz()
                angles = self.angles_xyz()

                print('Coordinates : ', coordinates)

                x1 = coordinates[0]
                y1 = coordinates[1]
                z1 = coordinates[2]
                m_line = float((z2 - z1)/(x2 - x1))
                slope_angle = 90 - math.degrees(math.atan(m_line))
                print('Slope Angle : ', slope_angle)

                drone_angle = angles[1]
                drone_angle_relative = drone_angle
                if drone_angle > 180:
                    drone_angle_relative -= 360

                turn_angle = drone_angle_relative - slope_angle

                if x1 > x2:     # to add a vector kinda thingie
                    turn_angle += 180

                print('Drone Angle : ', drone_angle_relative)
                print('Turn Angle : ', turn_angle)

                if turn_angle < -10:     # 10 for thresholding
                    self.turn_right()
                elif turn_angle > 10:
                    self.turn_left()
                else:
                    self.forward()
                f.close()

                if x1 > x2 - 10 and x1 < x2 + 10 and z1 > z2 - 10 and z1 < z2 + 10:
                    print('reached')
                    break        

            except:
                pass
