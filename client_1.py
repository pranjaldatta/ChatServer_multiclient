import socket
import os

HOST = '127.0.0.1'
PORT = 5000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

s.connect((HOST, PORT))

try:    
    while True:        
        data = s.recv(1024)        
        if data.decode() == "000":
            print("sending alive response")            
            s.sendall(bytes('000', 'utf-8'))
        else:
            print(data.decode())
            #msg = input("Response>")
            #s.sendall(msg.encode())        
except KeyboardInterrupt:
    #s.sendall(bytes(" ", "utf-8"))
    print("Closing with : ", bytes(" ", "utf-8"))
    s.close()
