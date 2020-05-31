from __init__ import OGMSService

taskServer = OGMSService.CreateTaskServer('172.21.212.119', 8061)
dataExchangeServer = OGMSService.CreateDataExchangeServer("172.21.212.155", 8062)
task = taskServer.createTask("faa3fa6554e822154862800961a99e51", dataExchangeServer, "wangming")

if task != None:
    task.configInputData("RUNSTATE", "LOADDATASET", "E:\\DemoData\\FDS\\data11.fds")
    taskServer.subscribeTask(task)
    task.wait4Finish()
    print('Suc')
else:
    print('Error')