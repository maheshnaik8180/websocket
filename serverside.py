"""
date = '23/04/2021'
modified_date = '23/04/2021'
author = 'Mahesh Naik'
description = using socket programming create chat app and store chat in mysql database"""

import os
import threading
import socket
import time
import mysql.connector
import logging
from dotenv import *

from log import logger

load_dotenv(find_dotenv())
HOST = os.getenv('HOST')
PORT = int(os.getenv('PORT'))
db_host = os.getenv('DB_HOST')
db_user = os.getenv('DB_USER')
db_pass = os.getenv('DB_PASS')
db_name = os.getenv('DB')


server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((HOST,PORT))
server.listen()
clients = []
aliases = []

class Server:
    """
        create constructor for server class
        define variables
        use mysql connector for connection between python and sql
    """
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
            sql_query = "select * from clientA_clientB;;"
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
                client.send(message)

    # Function to handle clients'connections
    def handle_client(self,client):
        """
        handle client connection
        use buffer string
        decode the msg using utf -8

        """
        while(True):
            try:
                time_stamp = time.ctime()
                message = client.recv(1024)
                data = str(message.decode('utf-8'))
                self.logger.info(data)
                self.broadcast(message, client)
            except:
                index = self.cursor.index(client)
                self.clients.remove(client)
                client.close()
                alias = self.aliases[index]
                notify = f'{alias} left the room'
                self.broadcast(notify.encode('utf-8'))
                self.aliases.remove(alias)
                break
            else:

                sql_query = "INSERT INTO ClientA_ClientB (chat,time) VALUES('{}','{}');".format(data,time_stamp)

                try:
                    self.cursor.execute(sql_query)
                    self.conn.commit()
                except:
                    self.conn.rollback()
                self.display()
    # Main function to receive the clients connection

    # Function to receive messages from clients
    def receive(self):
        """
        Function to receive messages from clients
        connection establish with client
        client data receive and append data in list
        """
        while (True):
            logger.info('Server is running and listening ...')
            client,address = server.accept()
            # logger.info(f'connection is established with {str(address)}')
            client.send('alias?'.encode('utf-8'))
            alias = client.recv(1024).decode('utf-8')
            logger.info(f"Connected with {alias}")
            client.send("Connected to Server".encode('utf-8'))
            self.aliases.append(alias)
            self.clients.append(client)
            # logger.info(f'The alias of this client is {alias}'.encode('utf-8'))
            notify = f"{alias} has joined the chat room"
            self.broadcast(notify.encode('utf-8'),client)
            thread = threading.Thread(target=self.handle_client, args=(client,))
            thread.start()


if __name__ == "__main__":
    # function call
    dbconn = Server(db_host, db_user, db_pass, db_name, logger)
    logger.setLevel(logging.INFO)
    dbconn.receive()
    dbconn.close_conn()