# import socket module
from socket import *
import threading
from datetime import datetime

# In order to terminate the program
import sys

ADDR = ('127.0.0.1',8080)

# Prepare a sever socket
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
serverSocket.bind(('', 8081))
serverSocket.listen(1)

def handle(connectionSocket):
    message = connectionSocket.recv(4096)

    # Send one HTTP header line into socket
    serverConnection = socket(AF_INET, SOCK_STREAM)
    serverConnection.connect(ADDR)
    print(f"proxy-forward,server,{threading.get_ident()},{datetime.now()}")
    serverConnection.send(message)

    response = b""
    while more  := serverConnection.recv(4096):
        response += more
    

    # Send the content of the requested file into socket
    print(f"proxy-forward,client,{threading.get_ident()},{datetime.now()}")
    connectionSocket.send(response)

    # Close client socket
    connectionSocket.close()

while True:
    # Establish the connection

    connectionSocket, addr = serverSocket.accept()

    t = threading.Thread(target=handle,args=(connectionSocket,),daemon=True)
    t.start()

# Close server socket
serverSocket.close()

# Terminate the program after sending the corresponding data
sys.exit()

