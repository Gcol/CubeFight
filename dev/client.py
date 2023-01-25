import sys
import threading
import time
import socket
from config import HOST, PORT


if __name__ == "__main__":
    current_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    current_socket.connect((HOST, PORT))
    try:
        while True:
            new_message = input("Type text :  ")
            current_socket.send(new_message.encode('utf-8'))
            response = current_socket.recv(1024)
            print(response.decode('utf-8'))
    except:
        current_socket.close()
        raise
