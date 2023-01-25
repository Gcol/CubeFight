import socket
from _thread import *
from player import Player
import pickle
from config import server, port

import random

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen()
print(f"Waiting for a connection, Server Started {server} : {port}")

all_player = {}

def create_new_player(name):
    start_pos = random.randrange(255)
    new_color = (random.randrange(255), random.randrange(255), random.randrange(255))
    all_player[name] = (Player(x=start_pos, y=start_pos, color=new_color, name=name))
    print(f'create new player {name} : {new_color}')

def threaded_client(conn, name):
    if name not in all_player:
        create_new_player(name)

    conn.send(pickle.dumps(all_player[name]))
    while True:
        try:
            data = pickle.loads(conn.recv(2048))
            all_player[name] = data
            reply = all_player
            if not data:
                print("Disconnected")
                break
            else:
                print("Received: ", data)
                print("Sending : ", reply)

            conn.sendall(pickle.dumps(reply))
        except:
            break

    all_player.pop(name)
    print("Lost connection")
    conn.close()

currentPlayer = 0

try:
    while True:
        conn, addr = s.accept()
        print("Connected to:", addr)

        start_new_thread(threaded_client, (conn, currentPlayer))
        currentPlayer += 1
except:
    s.close()
    print('Serveur closed succeffuly')
    raise
