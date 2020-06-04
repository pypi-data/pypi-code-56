#!/usr/bin/env python
# coding: utf-8
# In[10]:
from struct import *
import socket
import threading
import time
from subprocess import Popen, PIPE
class PyMod:
        global addr
        global xip
        global xport
        global sport
        global conn 
        global s    
        def _server(ip,port):
            PyMod._server.ip=ip
            PyMod._server.port=port
            PyMod._server.map=None
            PyMod._server.remoteaddress = None
            PyMod._server.response = []
            try:
                PyMod._connect(PyMod._server.ip,PyMod._server.port)
                PyMod._server.map=PyMod.srvmap()
                PyMod.close()
                return True
            except:
                return False
        def _connect(ip,port):
            global addr
            global xip
            global xport
            global sport
            global conn
            global s
            xip=ip
            xport=port
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((xip,xport))
            s.listen(1)
            conn, addr = s.accept()
            PyMod._server.remoteaddress = addr
            sport=addr[1]
            return True
        def packmod(bt):
                b = bytearray(bt.to_bytes(2, 'big',signed=True))
                return b
        def sendbyte(modbus_byte):
            global addr
            global conn 
            global s
            PyMod._connect(PyMod._server.ip,PyMod._server.port)
            def setbyte(modbus_byte):
                if len([i for i in modbus_byte if -256<i<256 ])==12 and len(modbus_byte)==12 and modbus_byte is not None:
                    return True
                else:
                    return False
            if setbyte(modbus_byte):
                zdh=modbus_byte
                rzh=bytes(zdh)
                t = threading.currentThread()
                while getattr(t, "run", True):
                    try:
                        data = conn.recv(1024)
                        if not data: 
                            return
                        else:
                            lnd = "%ib"%len(data)  
                            rs=unpack(lnd,data)
                            conn.send(rzh)
                            PyMod._server.response.append(rs)
                
                    except:
                        print("Error 001.")
                        pass
                PyMod.close()
            else:
                PyMod.close()
                return None
        def writeRG(ui,data_address,bt):
            global addr
            global conn 
            global s
            PyMod._connect(PyMod._server.ip,PyMod._server.port)
            def setparams(ui,data_address,bt):
                if (0<=data_address<256) and (0<=ui<256) and (-32768<bt<32768) and (data_address and ui and bt) is not None:
                    return True
                else:
                    return False
            if setparams(ui,data_address,bt):
                prt=PyMod.packmod(bt)
                zd=[0,data_address,0,0,0,6,ui,3,0,prt[0],prt[1],16] 
                rz=bytes(zd)
                try:
                    data = conn.recv(1024)
                    if not data: 
                        return False
                    else:
                        conn.send(rz)
                        PyMod.close()
                        return True
                except:
                    print("Error 001.")
                    pass
            else:
                PyMod.close()
                return None
        def readRG(modbus_type,data_address,ui):
            global conn 
            PyMod.readRG.val=[]
            PyMod._connect(PyMod._server.ip,PyMod._server.port)
            while True:
                *zd,=(0,0,0,0,0,6,0,0,0,0,0,0) 
                lnz = "%ib"%len(zd)  
                rz=pack(lnz,*zd)
                try:
                    data = conn.recv(1024)
                    if not data: break
                    lnd = "%ib"%len(data)  
                    nbyte=unpack(lnd,data)
                    np2=(data[7],data[9],data[6])
                    conn.send(rz)            
                    if np2==(modbus_type,data_address,ui):
                        PyMod.readRG.val.append(int.from_bytes([data[10],data[11]], byteorder='big', signed=True))
                        PyMod.close()
                        return PyMod.readRG.val
                        break
                except socket.error:
                    print("Error 002.")
                    PyMod.close()
                    break
        def forcecoil(ui,data_address,bt):
            mt=PyMod.getmodbustype('ic')
            srvaddr=PyMod.getsrvaddress(mt,data_address,ui)
            print(mt,ui,data_address,bt,srvaddr)
            if bt is True:
                dat=256
            else:
                dat=0
            if srvaddr is not None:
                PyMod.writeRG(ui,srvaddr,dat)
                return True
            else:
                return False
        def forceDI(ui,data_address,bt):# PUT ON/OFF DI function forceDI(unique id,data address, Boolean)
            mt=PyMod.getmodbustype('di')
            srvaddr=PyMod.getsrvaddress(mt,data_address,ui)
            if bt is True:
                dat=256
            else:
                dat=0
            if srvaddr is not None:
                PyMod.writeRG(ui,srvaddr,dat)
                return True
            else:
                return False
        def writeHR(ui,data_address,bt):
            mt=PyMod.getmodbustype('hri')
            srvaddr=PyMod.getsrvaddress(mt,data_address,ui)
            if srvaddr is not None:
                PyMod.writeRG(ui,srvaddr,bt)
                return True
            else:
                return False 
        def writeIR(ui,data_address,bt):#  Write Input Register function writeIR(unique id , Input Register address, data to send between -32768 and 32768) 
            mt=PyMod.getmodbustype('ir')
            srvaddr=PyMod.getsrvaddress(mt,data_address,ui)
            if srvaddr is not None:
                PyMod.writeRG(ui,srvaddr,bt)
                return True
            else:
                return False
        def readcoil(ui,data_address):
            mt=PyMod.getmodbustype('oc')
            srvaddr=PyMod.getsrvaddress(mt,data_address,ui)
            if srvaddr is not None:
                rc=PyMod.readRG(mt,data_address-1,ui)
                if rc[0]!=0: rc2=1
                else: rc2=0
                return rc2
            else:
                return None
        def readHR(ui,data_address):
            mt=PyMod.getmodbustype('hro')
            srvaddr=PyMod.getsrvaddress(mt,data_address,ui)
            if srvaddr is not None:
                hr=PyMod.readRG(mt,data_address-1,ui)
                #hr0=hr[0]
                #hro=int.from_bytes(hr0, byteorder='big', signed=True)
                return hr
            else:
                return None
        def close():
            global conn
            global s
            global xip
            global xport
            socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((xip,xport))
            conn.close()
            s.close()
        def killport(pt=None):
            if pt is not None:
                npt='-i:'+str(pt)
                p1=Popen(['lsof',npt],shell=False,stdout=PIPE)
                p2=Popen(['grep','LISTEN'],shell=False,stdin=p1.stdout, stdout=PIPE)
                p1.stdout.close()
                data = p2.communicate()[0]
                nwd=str(data)[2:len(str(data))-3]
                nwd2=nwd.replace('   ',' ')
                indx=nwd2.split(' ')
                if indx[0]=='python' or indx[0]=='python1' or indx[0]=='python2' or indx[0]=='python3':
                    Popen(['kill', '-9', indx[1]])
                    return True
                else:
                    return False
            else:
                return None
        def srvmap():        
            global conn 
            np1=[]
            for k in range(256):
                *zd,=(0,0,0,0,0,6,0,0,0,0,0,0) 
                lnz = "%ib"%len(zd)  
                rz=pack(lnz,*zd)
                try:
                    data = conn.recv(1024)
                    if not data: break
                    lnd = "%ib"%len(data)  
                    nbyte=unpack(lnd,data)
                    conn.send(rz)
                    if k==0 or PyMod.comparenb([ data[7],data[9],data[6]],np1): [np1.append([ data[7],data[9],data[6]])]
                except socket.error:
                    print("Error 003.")
                    break
            rse = [] 
            [rse.append(h) for h in np1 if h not in rse]
            return rse
        def comparenb(ax,xlist):
            if ax in xlist: 
                return False
            else:
                return True 
        def printmap():
            xp=[]
            rvs=PyMod._server.map
            for v in range(0,len(rvs)):
                mpd=rvs[v]
                xp.append('SERVER ADDRESS '+str(v)+'-> PLC ADDRESS: '+str(mpd[1]+1)+'| MODBUS TYPE:'+str(mpd[0])+'| PLC UID: '+str(mpd[2]))
            return xp
        def getsrvaddress(conn_type,data_address,uid):
            dt=PyMod._server.map
            rs = []
            data_address=data_address-1
            gd=([j for j in range(0,len(dt)) if dt[j]==[conn_type,data_address,uid]])
            if not gd: ng=None
            else: ng=gd[0]
            return ng
        def getmodbustype(mtype):
            if mtype==('hri' or 'HRI'):
                return int(3)
            elif mtype==('ir'or 'IR'):
                return int(4)
            elif mtype==('ic'or 'IC'):
                return int(1)
            elif mtype==('di'or 'DI'):
                return int(2)
            elif mtype==('hro' or 'HRO'):
                return int(6)
            elif mtype==('oc' or 'OC'):
                return int(5)
            else:
                return None