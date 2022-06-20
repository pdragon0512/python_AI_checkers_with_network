import socket
import threading

connections = []
total_connections = 0

class Client(threading.Thread):
    def __init__(self, socket, address, id, name, signal):
        threading.Thread.__init__(self)
        self.socket = socket
        self.address = address
        self.id = id
        self.name = name
        self.signal = signal

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
            if len(data) > 0 :
                print(data)
                datalist=list(data)
                if datalist[0]==0x01:
                    print("I'm client");
                else:
                    print("I'm server");
                movestart=datalist.index(0x81)
                ipaddress=bytes(datalist[1:movestart]).decode()
                print("opponent Ip address:"+ ipaddress)
                print("move path:"+ str(datalist[movestart+1])+" X "+ str(datalist[movestart+2]))
                # parsData=[]
                # if len(data)>=ROWS*COLS:
                #     for row in range(ROWS):
                #         parsData.append([])
                #         for col in range(COLS):
                #             parsData[row].append(data[row*COLS+col]-0x10)
                # # print(parsData)
                # game = Game(parsData)
                # value, new_board = minimax(game.get_board(), 3, True, game)
                # game.ai_move(new_board)
                # game.board=new_board
                # # print(new_board.draw)
                # self.socket.sendall(bytes(game.getBoardData()))


# Wait for new connections
def newConnections(socket):
    while True:
        sock, address = socket.accept()
        global total_connections
        connections.append(Client(sock, address, total_connections, "Name", True))
        connections[len(connections) - 1].start()
        print("New connection at ID " + str(connections[len(connections) - 1]))
        total_connections += 1


def main():

    # host = input("Host: ")
    # port = int(input("Port: "))

    # Create new server socket
    ######################ipv4 part###############################
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("127.0.0.1",5777))
    ######################ipv6 part###############################
    # sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    # sock.bind(("::1", 5777))
    sock.listen(5)

    # Create new thread to wait for connections
    newConnectionsThread = threading.Thread(target=newConnections, args=(sock,))
    newConnectionsThread.start()


main()
