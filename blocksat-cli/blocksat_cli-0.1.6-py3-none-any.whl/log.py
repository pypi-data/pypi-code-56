"""Handling of Logs"""
import os, time


class Logfile():
    def __init__(self, cfg_dir, module):
        """Setup directory and file for logs"""
        log_dir = os.path.join(cfg_dir, "logs")
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        name = module + "-" + time.strftime("%Y%m%d-%H%M%S") + ".log"
        self.logfile = os.path.join(log_dir, name)

    def append(self, line):
        with open(self.logfile, "a") as fd:
            fd.write(line + "\n")
