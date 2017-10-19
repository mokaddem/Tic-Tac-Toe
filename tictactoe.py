#!/usr/bin/env python3.5

import sys, os
import time
import socket
import json
import argparse

GRIDSIZE = 3
EMPTY = 0
PLAYERX = 1
PLAYERY = 2
GRIDTOSTRING = {
        0: ' ',
        1: 'X', 
        2: 'O' 
        }

class game:
    def __init__(self, sock, HOST, PORT, server=False):
        self.server = server
        self.doesPlayerPressedOK = False
        self.gameFinished = False
        self.host = HOST
        self.port = PORT
        self.sock = sock
        self.grid = [[EMPTY for i in range(GRIDSIZE)] for i in range(GRIDSIZE)]
        self.playingPlayer = PLAYERX

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
            self.checkDraw()
            if self.playingPlayer == self.currentPlayer:
                coord = self.inputData()
                self.addInputToGrid(coord)
            else:
                self.waitOtherPlayer()

    def inputData(self):
        while True:
            coord = input('coordinate of the grid (r,c):')
            try:
                coordList = coord.split(',')
                row = int(coordList[0])
                col = int(coordList[1])
                if self.grid[row][col] != EMPTY:
                    print('Cell already taken')
                    continue
            except:
                print('bad input')
                continue
            return coord

    def addInputToGrid(self, coord, remote=False):
        coord = coord.split(',')
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
        self.checkVictory(row, col)

    def victory(self, me):
        if not me:
            print('Victory!')
            self.gameFinished = True
        else:
            print('Defeat...')
            self.gameFinished = True

    def checkDraw(self):
        flag_not_stuck = False
        for row in self.grid:
            for v in row:
                if v == EMPTY:
                    flag_not_stuck = True
        if not flag_not_stuck:
            print('Draw!')
            self.gameFinished = True

    def checkVictory(self, row, col):
        #check if previous move caused a win on vertical line 
        if self.grid[0][col] == self.grid[1][col] == self.grid[2][col]:
            print(self)
            self.victory(self.playingPlayer == self.currentPlayer)

        #check if previous move caused a win on horizontal line 
        if self.grid[row][0] == self.grid[row][1] == self.grid [row][2]:
            print(self)
            self.victory(self.playingPlayer == self.currentPlayer)

        #check if previous move was on the main diagonal and caused a win
        if row == col and self.grid[0][0] == self.grid[1][1] == self.grid [2][2]:
            print(self)
            self.victory(self.playingPlayer == self.currentPlayer)

        #check if previous move was on the secondary diagonal and caused a win
        if row + col == 2 and self.grid[0][2] == self.grid[1][1] == self.grid [2][0]:
            print(self)
            self.victory(self.playingPlayer == self.currentPlayer)

    def sendToPeer(self, to_send):
        self.sock.sendall(json.dumps(to_send).encode('utf8'))

    def waitOtherPlayer(self):
        print(self)
        print('Waiting for other player...')
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
               self.addInputToGrid(coordStr, remote=True)
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

        os.system('clear') #Clear terminal
        return to_ret

    def __str__(self):
        return self.__repr__()


def getSock(HOST, PORT):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    return sock

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Tic Tac Toe Game')
    parser.add_argument('-s' '--server', dest='server', help='Is the server', action='store_true')
    parser.add_argument('-n', '--host', help='hostname', default='localhost')
    parser.add_argument('-p', '--port', help='port', default=9876, type=int)
    args = parser.parse_args()

    sock = getSock(args.host, args.port)
    if args.server:
        g = game(sock, server=True, HOST=args.host, PORT=args.port)
    else:
        g = game(sock, server=False, HOST=args.host, PORT=args.port)
    g.startGame()
    sock.close()
