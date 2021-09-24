#!/usr/bin/python
from ast import Str
import socket
import select
import errno
import sys
import cprint


HEADER_LENGTH = 10

with open("port_info.txt", "r") as f:
    lines = f.readlines()

IP = lines[0].strip()
PORT = int(lines[1].strip())
"""
my_username = input("Username: ")
#my_colour = input("Colour: ")
# Create a socket
# socket.AF_INET - address family, IPv4, some otehr possible are AF_INET6, AF_BLUETOOTH, AF_UNIX
# socket.SOCK_STREAM - TCP, conection-based, socket.SOCK_DGRAM - UDP, connectionless, datagrams, socket.SOCK_RAW - raw IP packets
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to a given ip and port
client_socket.connect((IP, PORT))

# Set connection to non-blocking state, so .recv() call won;t block, just return some exception we'll handle
client_socket.setblocking(False)

# Prepare username and header and send them
# We need to encode username to bytes, then count number of bytes and prepare header of fixed size, that we encode to bytes as well
username = my_username.encode('utf-8')
username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')


#sending a colour for this users text and sending it to the server

"""
"""
colour = my_colour.encode('utf-8')
colour_header = f"{len(colour):<{HEADER_LENGTH}}".encode('utf-8')
"""
"""
#send infomation to the server
client_socket.send(username_header + username) #+ colour_header + colour)
"""

def close():
    send_message("close")
    client_socket.close()
    sys.exit()

def change_username(*args):
    global my_username, client_socket
    try:
        client_socket.close()
    except:
        pass

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((IP, PORT))
    client_socket.setblocking(False)
    if len(args) != 0:
        my_username = args[0]
    else:
        my_username = input("Username: ")
    username = my_username.encode('utf-8')
    username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
    client_socket.send(username_header + username)

def change_colour():
    pass

def get_message():
    commands = ["help", "close", "change username"]
    command_definitions = {"help":"return help", "close": close, "change username": change_username, "change colour":change_colour}
    # Wait for user to input a message
    
    message = input(f'{my_username} > ')
    
    if message.lower() in commands:
        to_send = False
        if command_definitions.get(message):
            if type(command_definitions.get(message)) == str:
                print(f">[HELP] {command_definitions.get(message)}")
            else:
                f = command_definitions.get(message)
                f()
        else:
            print(">message not sent")
            print(">Command not found")
        return False
        
    return message
def send_message(message):
    # If message is not empty - send it
    if message:

        # Encode message to bytes, prepare header and convert to bytes, like for username above, then send
        message = message.encode('utf-8')
        message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
        client_socket.send(message_header + message)

def recieve():
    try:
        # Now we want to loop over received messages (there might be more than one) and print them
        while True:

            # Receive our "header" containing username length, it's size is defined and constant
            username_header = client_socket.recv(HEADER_LENGTH)

            # If we received no data, server gracefully closed a connection, for example using socket.close() or socket.shutdown(socket.SHUT_RDWR)
            if not len(username_header):
                print('Connection closed by the server')
                sys.exit()

            # Convert header to int value
            username_length = int(username_header.decode('utf-8').strip())

            # Receive and decode username
            username = client_socket.recv(username_length).decode('utf-8')

            # Now do the same for message (as we received username, we received whole message, there's no need to check if it has any length)
            message_header = client_socket.recv(HEADER_LENGTH)
            message_length = int(message_header.decode('utf-8').strip())
            message = client_socket.recv(message_length).decode('utf-8')

                                    #receive and decode colour
            # Convert header to int value
            """
            colour_length = int(username_header.decode('utf-8').strip())
            recieved_colour = client_socket.recv(colour_length).decode('utf-8')

            print("Rec", recieved_colour)
            """

            # Print message
            #print(f'{username} > {message}')
            return {"user":username, "message":message}

    except IOError as e:
        # This is normal on non blocking connections - when there are no incoming data error is going to be raised
        # Some operating systems will indicate that using AGAI
        # N, and some using WOULDBLOCK error code
        # We are going to check for both - if one of them - that's expected, means no incoming data, continue as normal
        # If we got different error code - something happened
        """
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print('Reading error: {}'.format(str(e)))
            sys.exit()
        """
        # We just did not receive anything
        return
"""
    except Exception as e:
    # Any other exception - something happened, exit
    print('Reading error: '.format(str(e)))
    sys.exit()
"""
    
if __name__ ==  "__main__":
    change_username()
    while True:
        message = get_message()
        if not not message:
            send_message(message)
        recieve()