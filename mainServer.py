#!/usr/bin/env python3
import socket, threading

stack= ['9 0 22 8','17 9 2 7']

class ClientThread(threading.Thread):
    def __init__(self,clientAddress,clientsocket):
        threading.Thread.__init__(self)
        self.csocket = clientsocket
        print ("New connection added: ", clientAddress)
    def run(self):
        print ("Connection from : ", clientAddress)
        msg = ''
        while True:
            data = self.csocket.recv(2048)
            msg = data.decode()
            if msg=="Send String":
                try:
                    for fh in open("map","r"):
                        self.csocket.send(bytes(fh.encode('UTF8')))
                    break
                except:
                    self.csocket.send(bytes("No File".encode('UTF8')))
                    break
            elif msg=="pop":
                while True:
                    if len(stack)!=0:
                        a = stack[0]
                        stack.remove(a)
                        self.csocket.send(bytes(a.encode('UTF8')))
                        break
                    else:
                        continue
            elif msg=="peek":
                self.csocket.send(bytes(str(len(stack)).encode('UTF8')))
            else:
                if msg!="":
                    stack.append(msg)
                break
        print(stack)
        print ("Client at ", clientAddress , " disconnected...")
LOCALHOST = "192.168.43.91"
PORT = 8080
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((LOCALHOST, PORT))
print("Server started")
print("Waiting for client request..")
while True:
    server.listen(1)
    clientsock, clientAddress = server.accept()
    newthread = ClientThread(clientAddress, clientsock)
    newthread.start()
