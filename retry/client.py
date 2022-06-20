from checkers.constants import Dark_piece,Light_piece,BLACK, ROWS, RED, COLS,WHITE
from checkers.game import Game
from checkers.board import Board

import socket
import threading
import sys          # Import socket module


def receive(socket, signal,centralClientSocket):
    while signal:
        try:
            data = socket.recv(100)
            if data!="":
                parsData=[]
                if len(data)>=ROWS*COLS:
                    for row in range(ROWS):
                        parsData.append([])
                        for col in range(COLS):
                            parsData[row].append(data[row*COLS+col]-0x10)
                game = Game(parsData)
                game.board.draw_board()
                # print(parsData)
                game.turn = Light_piece
                while game.turn == Light_piece:
                    text = input("Your turn! Please input the pointers(ex: 1 2 3 4):")
                    list = text.split(" ");
                    posvalues = []
                    for listtext in list:
                        if listtext != "":
                            posvalues.append(int(listtext))



                    game.select(posvalues[0]-1,posvalues[1]-1)
                    game.select(posvalues[2]-1, posvalues[3]-1)
                    game.board.draw_board()

                    # if game.turn != Light_piece :
                        ######send part########
                    # senddata=b''
                    senddata=bytes([0x01])
                    senddata+=(bytes("127.0.0.1",'utf-8'))
                    senddata+=bytes([0x81])
                    senddata+=((int((posvalues[0]-1)*COLS/2+(posvalues[1]+1)/2)).to_bytes(1,'big'))
                    senddata+=((int((posvalues[2] - 1) * COLS/2 + (posvalues[3]+1)/2)).to_bytes(1, 'big'))
                    senddata+=bytes([0xB2])
                    print(senddata)
                    # senddata[len()]
                    centralClientSocket.sendall(senddata)


                socket.sendall(bytes(game.getBoardData()))
        except:
            signal = False
            break
def localClient(centralClientSocket):

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # sock.connect((host, port))
        sock.connect(("127.0.0.1",9999))
    except:
        print("Could not make a connection to the server")
        input("Press enter to quit")
        sys.exit(0)
    # Create new thread to wait for data
    receiveThread = threading.Thread(target=receive, args=(sock, True,centralClientSocket))
    receiveThread.start()
