import threading
import socket
import logging
import os
from dotenv import *
from log import logger
load_dotenv(find_dotenv())

host = os.getenv('HOST')
port = os.getenv('port')
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host,port))
alias = input('Choose an alias ')


logger.setLevel(logging.INFO)
class clientside:
    def client_receive(self):
        """
        recive the message and encode the message using utf-8
        :return: returns
        """
        while True:
            try:
                message = client.recv(1024).decode('utf-8')
                if message == "alias?":
                    client.send(alias.encode('utf-8'))
                else:
                    logger.info(message)
            except:
                logger.info('Error!')
                client.close()
                break


    def client_send(self):
        """
                give the input and send the message
                 :return: returns
                """
        while True:
            message = f'{alias}: {input("")}'
            client.send(message.encode('utf-8'))


    receive_thread = threading.Thread(target=client_receive)
    receive_thread.start()

    send_thread = threading.Thread(target=client_send)
    send_thread.start()

clients = clientside()
recive = clients.client_receive()

send = clients.client_send()
