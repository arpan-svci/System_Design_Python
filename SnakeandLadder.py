import random

class BoardState:
    def __init__(self,players):
        self.board = [Position(i) for i in range(101)]
        self.players = {player:Player(self,player=player) for player in players}
        self.won= False
    def addSnake(self,start,end):
        self.board[start].addSnake(end)
    def addLadder(self,start,end):
        self.board[start].addLadder(end)
    def move(self, start,postion):
        if self.won == True:
            return False
        pos = self.board[start+postion]
        if pos.isLadderStart == True:
            endPosition = pos.ladderEndPoint
        elif pos.isSnakeOpening == True:
            endPosition = pos.snakeEndPoint
        else:
            endPosition = start+postion
        self.board[endPosition].player = self.board[start].player
        self.board[start].player = None
        return endPosition
    def declareWin(self):
        self.won = True
        return "Reset"

class Position:
    def __init__(self,index):
        self.isSnakeOpening=False
        self.isLadderStart=False
        self.snakeEndPoint=None
        self.ladderEndPoint=None
        self.player = None
        self.positionIndex = index
    def addSnake(self,end):
        self.isSnakeOpening=True
        self.snakeEndPoint=end
    def addLadder(self,end):
        self.isLadderStart=True
        self.ladderEndPoint=end

class Player:
    def __init__(self,boardState,player):
        self.player = player
        self.curretPosition = 0
        self.boardState = boardState
    def move(self):
        pos = random.randint(1,6)
        if self.curretPosition + pos<=100:
            temp = self.boardState.move(self.curretPosition,pos)
            print(f"{self.player} rolled a {pos} and moved from {self.curretPosition} to {temp}")
            self.curretPosition = temp
        if self.curretPosition==100:
            self.win()
            return False
    def win(self):
        print(f"{self.player} win the game")
        self.boardState.declareWin()

if __name__=="__main__":
    try:
        numberOfPlayers = int(input())
        players = []
        for i in range(numberOfPlayers):
            players.append(input())
        boardState = BoardState(players=players)
        temp = int(input())
        for i in range(temp):
            command = input().split()
            start = int(command[0])
            end = int(command[1])
            boardState.addSnake(start,end)
        temp = int(input())
        for i in range(temp):
            command = input().split()
            start = int(command[0])
            end = int(command[1])
            boardState.addLadder(start,end)
        t = True
        while True:
            for i in players:
                state = boardState.players[i].move()
                if state == False:
                    t = False
                    break
            if t == False:
                break

    except Exception as e:
        print("Invalid Input")
