import asyncio
import datetime

class Client:
    def __init__(self):
        self.start_time = self.timeset()
    """
    업타임 세팅
    """
    def timeset(self):
        start_time = datetime.datetime.utcnow()
        return start_time
    """
    기존에 쓰던 코드
    """
    def uptime(self):
        return datetime.datetime.utcnow() - self.start_time
    """
    새로운 코드
    """
    def hours(self):
        uptime = str(datetime.datetime.utcnow() - self.start_time).split(":")
        hours = uptime[0]
        return hours

    def minitues(self):
        uptime = str(datetime.datetime.utcnow() - self.start_time).split(":")
        minitues = uptime[1]
        return minitues

    def seconds(self):
        uptime = str(datetime.datetime.utcnow() - self.start_time).split(":")
        seconds = uptime[2].split(".")[0]
        return seconds
