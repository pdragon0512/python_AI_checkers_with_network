import socket
import threading
import sys          # Import socket module
import socket
import threading
from checkers.constants import Dark_piece,Light_piece,BLACK, ROWS, RED, COLS,WHITE
from checkers.game import Game
from checkers.board import Board
from minimax.algorithm import minimax

class Client(threading.Thread):
    def __init__(self, socket, address, id, name, signal):
        threading.Thread.__init__(self)
        self.socket = socket
        self.address = address
        self.id = id
        self.name = name
        self.signal = signal

        game = Game()
        game.change_turn()

        self.socket.sendall(bytes(game.getBoardData()))


    def __str__(self):
        return str(self.id) + " " + str(self.address)
    def run(self):
        while self.signal:
            try:
                data = self.socket.recv(100)
            except:
                print("Client " + str(self.address) + " has disconnected")
                self.signal = False
                connections.remove(self)
                break
            if data != "":
                parsData=[]
                if len(data)>=ROWS*COLS:
                    for row in range(ROWS):
                        parsData.append([])
                        for col in range(COLS):
                            parsData[row].append(data[row*COLS+col]-0x10)
                game = Game(parsData)
                value, new_board = minimax(game.get_board(), 3, True, game)
                game.ai_move(new_board)
                game.board=new_board
                self.socket.sendall(bytes(game.getBoardData()))


# Wait for new connections
def newConnections(socket):
    while True:
        sock, address = socket.accept()
        global total_connections
        connections.append(Client(sock, address, total_connections, "Name", True))
        connections[len(connections) - 1].start()
        print("New connection at ID " + str(connections[len(connections) - 1]))
        total_connections += 1


def runmain():

    # host = input("Host: ")
    # port = int(input("Port: "))

    # Create new server socket
    ######################ipv4 part###############################
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("127.0.0.1",9999))
    ######################ipv6 part###############################
    # sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    # sock.bind(("::1", 9999))
    sock.listen(5)

    # Create new thread to wait for connections
    newConnectionsThread = threading.Thread(target=newConnections, args=(sock,))
    newConnectionsThread.start()






def receive(socket, signal):
    while signal:
        try:
            data = socket.recv(100)
            # print("printed here:"+str(data.decode("utf-8")))
            # if data!="":
            #
            #     socket.sendall(bytes(game.getBoardData()))
        except:
            signal = False
            break
def centralclient():
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(("127.0.0.1",5777))
        runmain()

##########Central server part############################
connections = []
total_connections = 0
centralclient()

