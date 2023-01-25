import socket
from _thread import *
from player import Player
import pickle

import random

server = "127.0.0.1"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen()
print("Waiting for a connection, Server Started")


players = [Player(0,0,50,50,(255,0,0)), Player(100,100, 50,50, (0,0,255))]
all_player = []

def create_new_player(player):
    start_pos = random.randrange(255)
    new_color = (random.randrange(255), random.randrange(255), random.randrange(255))
    all_player.append(Player(x=start_pos, y=start_pos, color=new_color, name='Test'))
    print(f'create new player {player} : {new_color}')

def threaded_client(conn, current_index_player):
    print(current_index_player, len(players))
    if current_index_player + 1 > len(all_player):
        create_new_player(current_index_player)

    while True:
        try:
            data = pickle.loads(conn.recv(2048))
            import pdb;
            pdb.set_trace()
            all_player[current_index_player] = data

            if not data:
                print("Disconnected")
                break
            else:
                reply = [player for player in all_player if all_player.index(player) != currentPlayer]
                print("Received: ", data)
                print("Sending : ", reply)

            conn.sendall(pickle.dumps(reply))
        except:
            break

    print("Lost connection")
    conn.close()

currentPlayer = 0

while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1
