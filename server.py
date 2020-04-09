import os
import sys
import threading
import socket
from colorama import Fore
from queue import Queue

HOST = "127.0.0.1"
PORT = 5000
s = None
job_queue = Queue()
connections = []
conn_addrs = []


def create_and_bind():
    """
    Create server port and bind
    """
    global s
    
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print(Fore.GREEN+"Socket created ..."+Fore.RESET)
        s.bind((HOST, PORT))
        print(Fore.GREEN+"Socket bound to {}:{}".format(HOST, PORT)+Fore.RESET)
        s.listen()
    except socket.error as err:
        print(Fore.RED+"ERROR: {}".format(err)+Fore.RESET)
        exit()

def close():
    """
    Util function to close server socket
    """
    global s
    s.close()

def client_list(idx=None):
    """
    A module that checks whether a particular connection (if idx is not none)
    is still live.
    id idx is none, it checks that for all connections.
    """    
    if idx is None:
        print("---------Client List------------")        
        for conn_id, conn in enumerate(connections):
            try:
                conn.sendall(bytes("000", "utf-8"))
                conn.recv(1024)
                print("Client id: {}, Address: {}".format(conn_id, conn_addrs[conn_id]))
            except:
                print(Fore.YELLOW+"Client #{}: {} is closed".format(conn_id, conn_addrs[conn_id])+Fore.RESET)
                del connections[conn_id]
                del conn_addrs[conn_id]
    else:
        try:
            print(type(idx))
            conn = connections[idx]
            conn.sendall(bytes("000", "utf-8"))
            conn.recv(1024)
            return 0
        except:
            del connections[idx]
            del conn_addrs[idx]

def accepting_connections():
    """
    we close all existing connections tht may exist.
    In this method we accept new connections and add to the list
    This consists of one permanent thread
    """
    global s
    global connections
    global conn_addrs

    for connection in connections:
        connection.close()
    del connections[:]
    del conn_addrs[:]

    #infinite loop to constantly accept connections
    while True:
        try:
            conn, addr = s.accept()
            s.setblocking(True)

            connections.append(conn)
            conn_addrs.append(addr)

            print(Fore.BLUE+"New connection estabilished with {}".format(addr)+Fore.RESET)

            client_list()

        except Exception as e:
            print(Fore.RED+"ERROR: Exception occured at accepting_connections: {}".format(e)+Fore.RESET)    
            break
        except KeyboardInterrupt:
            print(Fore.YELLOW+"Closing server"+Fore.RESET)
            break
    close()   
        


create_and_bind()
accepting_connections()
  

