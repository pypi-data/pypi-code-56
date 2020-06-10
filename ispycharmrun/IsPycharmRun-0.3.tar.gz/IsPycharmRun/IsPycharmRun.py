from functools import wraps
import os

class IsPycharmRun:
    def __init__(self, deviceUrl, logDir):
        self.deviceUrl = deviceUrl
        self.logDir = logDir

    def __call__(self, func):
        @wraps(func)
        def wrapped_function(baseDir):
            if self.isPycharmRun():
                print(func.__name__ + " was called")
                return func(basedir=baseDir, devices=self.deviceUrl, logdir=self.logDir)
            else:
                print("非pycharm环境，正常调试模式")
                return func(basedir=baseDir)
        return wrapped_function

    def isPycharmRun(self):
        isRunningInPyCharm = "PYCHARM_HOSTED" in os.environ
        return isRunningInPyCharm


if __name__ == "__main__":
    a = IsPycharmRun("MasterTable")