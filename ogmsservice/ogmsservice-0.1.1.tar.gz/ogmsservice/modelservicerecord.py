#Data : 2020-5-30
#Author : Fengyuan Zhang (Franklin)
#Email : franklinzhang@foxmail.com
#Description : Provide model service running record service

import time
from .utils import HttpHelper
from .base import Service
from .data import DataConfigrationItem
from .utils import CommonMethod

class ModelServiceRunningRecord(Service):
    def __init__(self, ip, port, id, msid, guid, status = 1, inputs = [], outputs = [], timespan = 0.0, standout = '', standerr = '', invokeerr = '', logs = []):
        Service.__init__(self, ip, port)
        self.id = id 
        self.msid = msid
        self.guid = guid
        self.status = status
        self.inputs = inputs
        self.outputs = outputs
        self.timespan = timespan
        self.standout = standout
        self.standerr = standerr
        self.invokeerr = invokeerr
        self.logs = logs

    def wait4Finished(self, timeout = 7200):
        currtime = time.time()
        endtime = currtime + timeout
        self.refresh()
        while self.status == 0 and currtime < endtime:
            time.sleep(2)
            self.refresh()
            currtime = time.time()
        if endtime >= currtime:
            # TODO more judgement
            return -1
        return 1

    def refresh(self):
        jsData = HttpHelper.Request_get_sync(self.ip, self.port, "/modelserrun/json/" + self.id)
        if jsData["result"] == "suc":
            msr = CommonMethod.getJsonValue(jsData, "data")
            self.status = int(CommonMethod.getJsonValue(msr, "msr_status"))
            self.timespan = float(CommonMethod.getJsonValue(msr, "msr_span"))
            self.standout = CommonMethod.getJsonValue(CommonMethod.getJsonValue(msr, "msr_runninginfo"), "StdErr")
            self.standerr = CommonMethod.getJsonValue(CommonMethod.getJsonValue(msr, "msr_runninginfo"), "StdOut")
            self.invokeerr = CommonMethod.getJsonValue(CommonMethod.getJsonValue(msr, "msr_runninginfo"), "InvokeErr")
            self.inputs = []
            for index, item in enumerate(CommonMethod.getJsonValue(msr, "msr_input")):
                self.inputs.append(DataConfigrationItem.MakeUpDataItem(item))
            self.outputs = []
            for index, item in enumerate(CommonMethod.getJsonValue(msr, "msr_output")):
                self.outputs.append(DataConfigrationItem.MakeUpDataItem(item))