import socket
from checkers.constants import Dark_piece,Light_piece,BLACK, ROWS, RED, COLS,WHITE
import threading
import sys          # Import socket module
from  client import localClient

def centralclient():

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(("127.0.0.1",5777))
        localClient(sock)
    except:
        print("Could not make a connection to the server")
        input("Press enter to quit")
        sys.exit(0)
##########Central server part############################
centralclient()


