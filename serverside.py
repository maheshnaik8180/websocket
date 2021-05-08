"""
date = '4/05/2021'
modified_date = '5/05/2021'
author = 'Mahesh Naik'
description = '  using Websocket programming create client and server communication'
"""

import os
import threading
import socket
import mysql.connector
import logging
from dotenv import *

from log import logger

load_dotenv(find_dotenv())
HOST = os.getenv('HOST')
PORT = os.getenv('PORT')
db_host = os.getenv('DB_HOST')
db_user = os.getenv('DB_USER')
db_pass = os.getenv('DB_PASS')
db_name = os.getenv('DB')

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(bytearray(HOST,PORT))
server.listen()
clients = []
aliases = []

class server:
    # Constructor for Server class
    def __init__(self, db_host, db_user, db_pass, db_name, logger):
        self.conn = mysql.connector.connect(host=db_host, user=db_user, password=db_pass, database=db_name)
        self.cursor = self.conn.cursor()
        self.clients = []
        self.aliases = []
        self.logger = logger

        # Function to close database connection

    def close_conn(self):
        """
        parameter: conn =connection
        close connection
        """
        self.conn.close()

        # Function to display chat stored on database
    def display(self):
            """
            display function
            store chat in database
            using sql query display the data
            """
            sql_query = "SELECT * FROM chat_data;"
            try:
                self.cursor.execute(sql_query)
                result = self.cursor.fetchall()
                for i in result:
                    data = i[1]
                    print(data)
            except Exception:
                self.logger.error('Error:Unable to fetch data.')

    def broadcast(self,message,connection):
        """
                  broadcast the messasge given by clientside message
                  :return: returns
                  """
        for client in self.clients:
            if (client != connection):
                    client.send(message)

    # Function to handle clients'connections


    def handle_client(self,client):
        """
        handle client use buffer string
        """
        while(True):
            try:
                message = client.recv(1024)
                self.broadcast(message)
            except:
                index = self.cursor.index(client)
                clients.remove(client)
                client.close()
                alias = aliases[index]
                self.cursor(f'{alias} has left the chat room!'.encode('utf-8'))
                aliases.remove(alias)
                break
            else:
                sql_queery = "INSERT INTO clientA_clientB(chat) VALUES(' ');"

                try:
                    self.cursor.execute(sql_queery)
                    self.cursor.commit()
                except:
                    self.cursor.rollback()
                self.display()
    # Main function to receive the clients connection

    # Function to receive messages from clients
    def receive(self):
        while True:
            logger.info('Server is running and listening ...')
            client, address = server.accept()
            logger.info(f'connection is established with {str(address)}')
            client.send('alias?'.encode('utf-8'))
            alias = client.recv(1024)
            aliases.append(alias)
            clients.append(client)
            logger.info(f'The alias of this client is {alias}'.encode('utf-8'))
            self.display(f'{alias} has connected to the chat room'.encode('utf-8'))
            client.send('you are now connected!'.encode('utf-8'))
            thread = threading.Thread(target=self.display(), args=(client,))
            thread.start()


if __name__ == "__main__":
    dbconn = server(db_host, db_user, db_pass, db_name, logger)
    logger.setLevel(logging.INFO)
    dbconn.receive()