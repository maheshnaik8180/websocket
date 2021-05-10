import os
import threading
import socket
import logging
from dotenv import *

#logger implementation
from log import logger

logger.setLevel(logging.INFO)

#load environment variables
load_dotenv(find_dotenv())

#Connection to server
host = os.getenv('HOST')
port = int(os.getenv('PORT'))
client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect((host,port))
alias = input('Enter Name: ')

#Function to receive messages from Server
def client_receive():
    """
    Function to receive messages from Server
    use while loop recive function
    """

    while(True):
        try:
            message = client.recv(1024).decode('utf-8')
            if message == 'name':
                client.send(alias.encode('utf-8'))
            else:
                print(message)
        except:
            logger.error('Error!')
            client.close()
            break

#Function to send messages to Server
def client_send():
    """
     Function to send messages to Server
    """
    while(True):
        message = f'{alias}: {input("")}'
        print(message)
        client.send(message.encode('utf-8'))

#Implementing multi threading for making it multi client
receive_thread = threading.Thread(target=client_receive)
receive_thread.start()

send_thread = threading.Thread(target=client_send)
send_thread.start()