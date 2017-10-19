#!/usr/bin/env python3.5

import sys, os
import time
import socket
import json
import argparse
import npyscreen

GRIDSIZE = 3
EMPTY = 0
PLAYERX = 1
PLAYERY = 2

GRIDTOSTRING = {
        0: ' ',
        1: 'X', 
        2: 'Y' 
        }

theGame = None

class game:
    def __init__(self, sock, HOST, PORT, server=False):
        self.server = server
        self.doesPlayerPressedOK = False
        self.gameFinished = False
        self.host = HOST
        self.port = PORT
        self.sock = sock
        self.grid = [[EMPTY, EMPTY, EMPTY] for i in range(GRIDSIZE)]
        self.playingPlayer = PLAYERX
        self.startGame()

    def bind_cient(self):
        print('waiting client')
        sock.bind((self.host, self.port))
        sock.listen(1)
        conn, addr = sock.accept()
        self.sock = conn
        self.addr = addr
        print("Connected to client")
        

    def connect_to_server(self):
        print('waiting server')
        self.sock.connect((self.host, self.port))
        print('waiting server')


    def startGame(self):
        if self.server == True:
            self.currentPlayer = PLAYERX
            self.otherPlayer = PLAYERY
            self.bind_cient()
        else:
            self.currentPlayer = PLAYERY
            self.otherPlayer = PLAYERX
            self.connect_to_server()

        self.gameLoop()

    def gameLoop(self):
        while not self.gameFinished:
            print(self)
            if self.playingPlayer == self.currentPlayer:
                coord = input('coordinate of the grid (r,c):')
                self.addInput(coord)
            else:
                self.waitOtherPlayer()

    def addInput(self, coord, remote=False):
        coord = coord.split(',')
        print(coord)
        row = int(coord[0])
        col = int(coord[1])

        if not remote:
            self.grid[row][col] = self.currentPlayer
            self.playingPlayer = self.otherPlayer
            to_send = { 'coord': coord, 'player': self.currentPlayer}
            self.sendToPeer(to_send)
        else:
            self.grid[row][col] = self.otherPlayer
            self.playingPlayer = self.currentPlayer

        if self.doesSelfWin():
            print("YOU WIN!")
            sys.exit(1)

    def doesSelfWin(self):
        return False

    def sendToPeer(self, to_send):
        self.sock.sendall(json.dumps(to_send).encode('utf8'))

    def waitOtherPlayer(self):
        print(self)
        while True:
           data = self.sock.recv(1024)
           if not data: 
               time.sleep(0.2)
               pass
           else:
               data = json.loads(data.decode('utf8'))
               coord = data['coord']
               player = data['player']
               coordStr = coord[0] + ',' + coord[1]
               self.addInput(coordStr, remote=True)
               return

    def __repr__(self):
        to_ret = ''
        to_ret += '+---'*GRIDSIZE
        to_ret += '+\n'
        for row in self.grid:
            to_ret += '| '
            for v in row:
                to_ret += GRIDTOSTRING[v] + ' | '
            to_ret += '\n'
            to_ret += '+---'*GRIDSIZE
            to_ret += '+\n'

        os.system('clear')
        return to_ret

    def __str__(self):
        return self.__repr__()

    def getInstance(self):
        return self.grid

def getSock(HOST, PORT):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    return sock

    #with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    #    sock.bind((HOST, PORT))
    #    print('starting server at', (HOST, PORT))
    #    sock.listen(1)
    #    conn, addr = sock.accept()
    #    with conn:
    #        print('Connected by', addr)
    #        while True:
    #            data = conn.recv(1024)
    #            if not data: 
    #                break
    #            else:
    #                print('received', data)
    #            conn.sendall(data)


def client(HOST, PORT):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    sock.connect((HOST, PORT))
    return sock

    #with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    #    print('connecting to', (HOST, PORT))
    #    sock.connect((HOST, PORT))
    #    sock.sendall(b'Hello, world')
    #    data = sock.recv(1024)
    #print('Received', repr(data))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Tic Tac Toe Game')
    parser.add_argument('-s' '--server', dest='server', help='Is the server')
    parser.add_argument('-c', '--client', help='Is the client')
    parser.add_argument('-n', '--host', help='hostname', default='localhost')
    parser.add_argument('-p', '--port', help='port', default=9876, type=int)
    
    args = parser.parse_args()

    sock = getSock(args.host, args.port)
    if args.server is not None:
        g = game(sock, server=True, HOST=args.host, PORT=args.port)
    else:
        g = game(sock, server=False, HOST=args.host, PORT=args.port)
    theGame = g

    #App = MyApplication()
    #App.run()
    sock.close()
