import pickle
import socket
from _thread import *
from players import Player
from game import Game
from network import RPSCP


server = "192.168.1.135"
port = 8080

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server Started")


connected = set()
games = {}
idCount = 0

def threaded_client(conn, player, gameId):
    global idCount
    conn.send(str.encode(str(player)))

    reply = ""
    while True:
        try:
            data = conn.recv(4096)
            command, value = RPSCP.decode(data)
            print(f"Server received from player {player}: {command}" + (f":{value}" if value else ""))

            if gameId in games:
                game = games[gameId]

                if command == "DISCONNECT":
                    print(f"Player {player} disconnected")
                    break
                elif command == "RESET":
                    game.resetWent()
                    print(f"Game {gameId} reset by player {player}")
                elif command == "MOVE":
                    game.play(player, value)
                    print(f"Player {player} made move: {value}")
                elif command == "GET_GAME":
                    print(f"Sending game state to player {player}")
                    pass

                response = pickle.dumps(game)
                conn.sendall(response)
                print(f"Server sent {len(response)} bytes to player {player}")
            else:
                break

        except:
            break

    print("Lost connection")
    try:
        del games[gameId]
        print("Closing Game", gameId)
    except:
        pass

    idCount -= 1
    conn.close()


while True:
    conn, addr = s.accept()
    print("Connected to ", addr)

    idCount += 1
    p = 0
    gameId = (idCount - 1)//2
    if idCount % 2 == 1:
        games[gameId] = Game(gameId)
        print("Creating a new game...")
    else:
        games[gameId].ready = True
        p = 1


    start_new_thread(threaded_client, (conn, p, gameId))




