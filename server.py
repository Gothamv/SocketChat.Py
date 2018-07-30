#!/usr/bin/env python3
"""Server for multithreaded (asynchronous) chat application."""
from socket import AF_INET, socket, SOCK_STREAM #TCP Connection : That's why we use AF_INET, SOCK_STREAM
from threading import Thread

def acceptIncomingConnections():
    """Handles the incoming client connections"""
    while True:
        client, client_address = SERVER.accept()
        print("%s : %s has connected" % client_address)
        client.send(bytes("Welcome to SocketChat!" + "Now type your name and hit enter!","utf8"))
        addresses[client] = client_address
        Thread(target=handleClient, args=(client,)).start()

def handleClient(client): #Takes in client socket as argument
    """Handles a single client connection"""
    name = client.recv(BUFSIZE).decode("utf8")
    welcome = "Welcome %s! If you want to exit chat, type {quit} to exit." % name
    client.send(bytes(welcome,"utf8"))
    msg = "%s has joined the conversation." % name
    broadcast(bytes(msg,"utf8"))
    clients[client] = name
    while True:
        msg = client.recv(BUFSIZE)
        if msg != bytes("{quit}","utf8"):
            broadcast(bytes(msg, name+": "))
        else:
            client.send(bytes("{quit}","utf8"))
            client.close()
            del clients[client]
            broadcast(bytes("%s has left the conversation." % name),"utf8")
            break
def broadcast(msg, prefix=""):  # prefix is for name identification.
    """Broadcasts a message to all the clients."""
    for sock in clients:
        sock.send(bytes(prefix,"utf8")+msg)

clients = {}
addresses = {}

HOST = ''
PORT = 33000
BUFSIZE = 1024
ADDR = (HOST,PORT)
SERVER = socket(AF_INET,SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
    SERVER.listen(5) # Listen for 5 connections at max
    print("waiting for connection...")
    ACCEPT_THREAD = Thread(target=acceptIncomingConnections)
    ACCEPT_THREAD.start() # Starts the infinite loop.
    ACCEPT_THREAD.join()
    SERVER.close()

#...


