import libABCD
import socket
import selectors
import time
import random
import json

def connect(name="Unknown"):
    if not libABCD.network_info["isconnected"]:
        libABCD.network_info["name"]=name
        mysel=libABCD.network_info["selector"]
        server_address=(libABCD.network_info["host"],libABCD.network_info["port"])
        libABCD.logger.info('connecting to {} port {}'.format(*server_address))
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect(server_address)
            sock.setblocking(False)
            mysel.register(
                sock,
                selectors.EVENT_READ | selectors.EVENT_WRITE,
            )
            libABCD.network_info["socket"]=sock
            libABCD.network_info["isconnected"]=True
            msg='{"cmd":"_init","name":"'+name+'"}'
            libABCD.addmessage(msg)
        except Exception as e:
            libABCD.logger.error("error connecting to server")

def addmessage(msg):
    mysel=libABCD.network_info["selector"]
    sock=libABCD.network_info["socket"]
    mysel.modify(sock, selectors.EVENT_READ | selectors.EVENT_WRITE)
    if type(msg) is dict:
        libABCD.network_info["outgoing"].append(json.dumps(msg).encode())
    else:
        if type(msg) is str:
            libABCD.network_info["outgoing"].append(msg.encode())
        else:
            libABCD.network_info["outgoing"].append(msg)

def close():
    mysel=libABCD.network_info["selector"]
    connection=libABCD.network_info["socket"]
    mysel.unregister(connection)
    connection.close()
    del libABCD.network_info["socket"]
    libABCD.network_info["isconnected"]=False

def handle(timeout=1):
    if not libABCD.network_info["isconnected"]:
        libABCD.logger.warning("Not connected to server, entering UDP listen")
        ANY = "0.0.0.0"
        MCAST_PORT = 7886
        #create a UDP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        #allow multiple sockets to use the same PORT number
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        #Bind to the port that we know will receive multicast data
        sock.bind((ANY, MCAST_PORT))
        while not libABCD.network_info["isconnected"]:
            try:
                data, addr = sock.recvfrom(1024)
                if data==b'IamABCD':
                    # server is back, connect to it after 0-3 seconds
                    time.sleep(3*random.random())
                    (libABCD.network_info["host"],udpport)=addr
                    connect(libABCD.network_info["name"])
            except socket.error:
                pass
    else:
        mysel=libABCD.network_info["selector"]
        sock=libABCD.network_info["socket"]
        if time.time()-libABCD.network_info["last_ping"]>10: # one ping every 10-13 seconds
            libABCD.addmessage('{"cmd":"_ping"}')
            libABCD.network_info["last_ping"]=time.time()+3*random.random() # use randomized time
        try:
            for key, mask in mysel.select(timeout=1):
                connection = key.fileobj
                client_address = connection.getpeername()
        
                if mask & selectors.EVENT_READ:
                    data = connection.recv(1024)
                    if data:
                        # A readable client socket has data
                        libABCD.logger.debug('received {!r}'.format(data))
                        libABCD.parsemsg(data,connection)
                    else:
                        # server probably dead...
                        libABCD.logger.critical('looks like server is down')
                        close()
        
                if mask & selectors.EVENT_WRITE:
                    if not libABCD.network_info["outgoing"]:
                        # no message left
                        libABCD.logger.debug('no messages in queue')
                        mysel.modify(sock, selectors.EVENT_READ)
                    else:
                        # Send the next message. Using pop(0) to get a proper FIFO
                        next_msg = libABCD.network_info["outgoing"].pop(0)
                        libABCD.logger.debug('sending {!r}'.format(next_msg))
                        sock.sendall(next_msg)
        except Exception as e:
            # assuming problem in network
            libABCD.logger.critical('Network error, shutting down connection')
            close()


