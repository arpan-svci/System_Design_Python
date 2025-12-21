import random
import time
import os

class Board:
    def __init__(self):
        self.board = [[None for j in range(4)] for i in range(4)]
        self.positions = [(i,j) for i in range(4) for j in range(4)]
        self.availablePositions = [True for i in range(4) for j in range(4)]
        self.Iswin = False
        for i in range(2):
            self.addTwo()
        print(self)
            
    def getRandomAvailablePosition(self):
        available = [i for i, val in enumerate(self.availablePositions) if val]
        if not available:
            return False
        steps = random.randint(0,len(available)-1)
        return available[steps]
    
    def compress(self, row):
        return [i for i in row if i is not None]
    
    def checkWinPossiblility(self):
        if any(self.board[i][j] == None for i in range(4) for j in range(4)):
            return True 
        possible = False
        for i in range(4):
            for j in range(4):
                if i-1>=0 and self.board[i-1][j]==self.board[i][j]:
                    possible = True
                    break
                if i+1<4 and self.board[i+1][j]==self.board[i][j]:
                    possible = True
                    break
                if j-1>=0 and self.board[i][j-1]==self.board[i][j]:
                    possible = True
                    break
                if j+1<4 and self.board[i][j+1]==self.board[i][j]:
                    possible = True
                    break
            if possible:
                break
        return possible
    
    def merge(self,row):
        row = self.compress(row)
        skip = False
        merged = []
        for i in range(len(row)):
            if skip:
                skip = False
            elif i+1<len(row) and row[i] == row[i+1]:
                merged.append(2*row[i])
                if 2*row[i] == 2048:
                    self.Iswin = True
                skip = True
            else:
                merged.append(row[i])
        return self.padding(merged)
    
    def padding(self, row: list):
        for i in range(4-len(row)):
            row.append(None)
        return row
            
    def moveDown(self):
        for i in range(4):
            row = [self.board[j][i] for j in range(4)]
            row = self.merge(list(reversed(row)))
            row = list(reversed(row))
            for j in range(4):
                self.board[j][i] = row[j]
        self.updateAvailablePositions()
        self.addTwo()

    def moveUp(self):
        for i in range(4):
            row = [self.board[j][i] for j in range(4)]
            row = self.merge(row)
            for j in range(4):
                self.board[j][i] = row[j]
        self.updateAvailablePositions()
        self.addTwo()

    def moveLeft(self):
        for i in range(4):
            row = self.board[i]
            row = self.merge(row = row)
            self.board[i] = row
        self.updateAvailablePositions()
        self.addTwo()

    def moveRight(self):
        for i in range(4):
            row = list(reversed(self.board[i]))
            row = self.merge(row)
            self.board[i] = list(reversed(row))
        self.updateAvailablePositions()
        self.addTwo()

    def updateAvailablePositions(self):
        for idx, (x, y) in enumerate(self.positions):
            self.availablePositions[idx] = (self.board[x][y] is None)
    
    def addTwo(self):
        freeIndex = self.getRandomAvailablePosition()
        self.availablePositions[freeIndex] = False
        x,y = self.positions[freeIndex]
        self.board[x][y] = 2

    def __str__(self):
        ret = "---------------------\n"
        for i in range(4):
            for j in range(4):
                ret += f"{self.board[i][j]}\t"
            ret += "\n"
        ret += "---------------------\n"
        return ret
    
    def executor(self, command):
        if self.Iswin:
            print("Game Over")
        match command:
            case 0:
                self.moveLeft()
            case 1:
                self.moveRight()
            case 2:
                self.moveUp()
            case 3:
                self.moveDown()
            case _:
                print("Invalid Move")
        print(self)


if __name__=="__main__":
    board = Board()
    while True:
        try:
            command = random.randint(0,3)
            time.sleep(0.5)
            board.executor(command)
            if board.checkWinPossiblility() == False:
                print("Lost the game")
                break
            if board.Iswin == True:
                print("Won the game")
                break
        except Exception as e:
            print("Invalid Command")