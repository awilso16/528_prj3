# import socket module
from socket import *
import threading
from datetime import datetime

# In order to terminate the program
import sys

# Prepare a sever socket
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
serverSocket.bind(('', 8080))
serverSocket.listen(1)

def handle(connectionSocket):
    try:
        message = connectionSocket.recv(4096)

        filename = message.split()[1]
        f = open(filename[1:])
        outputdata = f.read()

        # Send one HTTP header line into socket
        print(f"server-response,{threading.get_ident()},{datetime.now()}")
        connectionSocket.send(("HTTP/1.1 200 OK\r\n\r\n").encode())

        # Send the content of the requested file into socket
        for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i].encode())
        connectionSocket.send("\r\n".encode())

        # Close client socket
        connectionSocket.close()
    except IOError:
        # Send response message for file not found
        connectionSocket.send(("HTTP/1.1 404 Not Found\r\n\r\n").encode())

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

