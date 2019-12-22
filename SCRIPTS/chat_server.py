#!/usr/bin/env python3
import select
import socket

# We include a header here which we send the size of the incoming message in.
HEADER = 10
IP_ADDRESS = "192.168.1.15"
PORT_ADDRESS = 6344

#Setup the server socket and add some options that lets it reconnect to client etc.
sock_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1) # read somewhere in stackoverflow you need this for macOS.


# Give it IP and Port and then make it 'listen' for calls to it from the internet.
sock_server.bind((IP_ADDRESS, PORT_ADDRESS))
sock_server.listen()

#list of the sockets it has and the clients connected to it.
connected_sockets = [sock_server]
connected_clients = {} # socket : username
# How to proccess incoming messages based on how long they are which the header tells.
def messaging(sock_client):

    try:
        head = sock_client.recv(HEADER)

        if not len(head):
            return False #This is a good tip to add that I found online.

        message_length = int(head.decode('utf-8').strip())
        return {'header': head, 'data': sock_client.recv(message_length)}

    except:
        return False


# The server/program loop.

while True:
    #gonna use select here to know when a socket gets modified
    rlist, wlist, xlist = select.select(connected_sockets, [], connected_sockets)

    for updated_socket in rlist: # aka if this is a connecting client

        if updated_socket == sock_server:
            sock_client, address_client = sock_server.accept()

            username = messaging(sock_client)

            if username is False:
                continue

            connected_sockets.append(sock_client)
            connected_clients[sock_client] = username

            print(f"New connection from {address_client[0]}:{address_client[1]} with username: {username['data'].decode('utf-8')}")

        else:
            message = messaging(updated_socket)
            username = connected_clients[updated_socket]

            if message is False: # If a user disc.
                print(f"Could not establish connection to {connected_clients[updated_socket]['data'].decode('utf-8')}")
                del connected_clients[updated_socket]
                connected_sockets.remove(updated_socket)
                continue

            print(f"{username['data'].decode('utf-8')} >> {message['data'].decode('utf-8')}") # print message sent from client to server console.

            for sock in connected_clients:
                if sock != updated_socket:
                    sock.send(username['header'] + username['data'] + message['header'] + message['data'])
