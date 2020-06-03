import libABCD
from pathlib import Path
import signal
import os
import sys
import time
import glob

waitchild=True
filebase=".watchdog.{}"

def watchfile(pid):
    return filebase.format(pid)

def check():
    Path(watchfile(os.getpid())).touch()

def sigchild(a,b):
    global waitchild
    libABCD.logger.warning("Process {} died. Watchdog will restart it".format(sys.argv[0]))
    waitchild=False

def start():
    global waitchild
    libABCD.logger.info("Starting watchdog on process {}".format(sys.argv[0]))
    signal.signal(signal.SIGCHLD,sigchild)
    pid=os.fork()
    if pid!=0:
        # in parent
        try:
            while waitchild:
                time.sleep(10)
                # clean watchfiles older than a minute
                try:
                    for fname in glob.glob(filebase.format("*")):
                        mtime=os.path.getmtime(fname)
                        if time.time()-mtime>60:
                            os.unlink(fname)
                except Exception as e:
                    # don't want to mess because of cleanup
                    pass
                # check that file has been modified within 30 sec, else reset app
                try:
                    mtime=os.path.getmtime(watchfile(pid))
                    if time.time()-mtime>30:
                        # need to kill child and that should be it
                        try:
                            libABCD.logger.warning("Watchfile not updated in 30 sec. Killing process {}".format(sys.argv[0]))
                            os.kill(pid,signal.SIGKILL)
                        except Exception as e:
                            try:
                                os.unlink(watchfile(pid))
                            except:
                                pass
                            libABCD.logger.critical("Watchdog couldn't kill rogue child")
                            libABCD.die()
                except Exception as e:
                    try:
                        os.unlink(watchfile(pid))
                    except:
                        pass
                    libABCD.logger.critical("Watchdog couldn't find watchfile")
                    libABCD.die()
            waitchild=True
            start()
        except: # here catching also Interrupt and kill
            try:
                os.unlink(watchfile(pid))
            except:
                pass
            libABCD.logger.critical("Watchdog couldn't keep process running")
            libABCD.die()
