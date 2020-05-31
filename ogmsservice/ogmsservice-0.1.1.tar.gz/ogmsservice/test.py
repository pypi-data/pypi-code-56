from __init__ import OGMSService


def main():
   server = OGMSService.CreateServer("127.0.0.1", "8060");
   status = server.connect()
   if status:
       access = server.getServiceAccess()
       list_ms = access.getModelServicesList()
       for index, item in enumerate(list_ms):
           print("ID : {0} - Name : {1} - Type : {2}".format(item.id, item.name, item.type))
       dataid = access.uploadDataByFile("touch_air", "E:\\DemoData\\input.xml")
       print("TouchAir - Input Data ID : {0}".format(dataid))
       touchair = access.getModelServiceByID('5c7e2ca448173f5618e12198')
       recordid = touchair.invoke([access.createDataConfigurationItem("aa00cced-60e7-48a5-90d2-f91ac08b624d", "InputData", dataid)])
       record = access.getModelServiceRunningRecordByID(recordid)
       record.wait4Finished(8000)
       print("TouchAir has been finished")
       record.refresh()
       for index, item in enumerate(record.outputs):
           dat = access.getDataByID(item.dataid)
           data_value = dat.value;
           ext = data_value[data_value.find('.') + 1:]
           dat.save("E:\\DemoData\\TouchAir\\" + item.eventname + '.' + ext)


    

if __name__ == '__main__':
    main()