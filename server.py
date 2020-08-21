import socket
from _thread import *


handle = open('settings.txt', 'r')
addr=handle.read()
handle.close()
server = addr
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen()
print("Waiting for a connection, Server Started")
global movesdict,players
movesdict={}
players=0

def threaded_client(conn, player,gameid):
    global movesdict,players
    moves=movesdict[gameid]
    conn.send(str.encode(str(player)))
    reply = ""
    r=False
    moves[player]=None
    while True:
        try:
            data = (conn.recv(2048)).decode()
            if data=="ready":
                if moves[1-player]==None:
                    reply="y"
                    r=True
                else:
                    reply="n"
            else:
                #players[player] = data
                if not data:
                    print("Disconnected")
                    break

                #print("Received: ", data)
                #print("Sending : ", reply)
                #print(moves)
                if data!="GET":
                    reply="recieved"
                    moves[1-player]=None
                    moves[player]=data
                else:
                    if moves[1-player]!=None:
                        reply=moves[1-player]

                    else:
                        reply="waiting"
            #conn.sendall(pickle.dumps(reply))
            if r==True and moves[1-player]=="not ready":
                reply="left"
            conn.sendall(str.encode(reply))
        except:
            break

    print("Lost connection")
    conn.close()
    players-=1
    moves[0]="not ready"
    moves[1]="not ready"
currentPlayer = 0
while True:
    conn, addr = s.accept()
    print("Connected to:", addr)
    if currentPlayer==0:
        movesdict[players//2]=["not ready","not ready"]
    start_new_thread(threaded_client, (conn, currentPlayer,players//2))
    players += 1
    currentPlayer = (players)%2