class State:
    Cross :str = 'X'
    Round :str = 'O'

class TicTacToe:
    def __init__(self, players):
        self.board = [[None for i in range(3)] for j in range(3)]
        self.players = players
        self.state = State.Cross
        self.isWin = False

    def getWinStatus(self):
        return self.isWin

    def play(self,x,y):
        if self.validateMove(x,y):
            self.board[x-1][y-1] = self.state
            if self.checkWin():
                self.isWin = True
                print(f"{self.players[self.state]} won the game")
            self.state = State.Cross if self.state == State.Round else State.Round
        else:
            print("Invalid Move")

    def validateMove(self, x,y):
        if self.board[x-1][y-1] is not None:
            return False
        else:
            return True
        
    def checkWin(self):
        # row
        for i in range(3):
            if all(self.board[i][j] == self.state for j in range(3)):
                return True

        # column
        for j in range(3):
            if all(self.board[i][j] == self.state for i in range(3)):
                return True

        # main diagonal
        if all(self.board[i][i] == self.state for i in range(3)):
            return True

        # anti diagonal
        if all(self.board[i][2-i] == self.state for i in range(3)):
            return True

        return False
    
    def checkavailability(self):
        return any(self.board[i][j]==None for i in range(3) for j in range(3))
        
    def __str__(self):
        ret = "----------------\n"
        for i in self.board:
            for j in i:
                ret += (j if j is not None else '-')+'\t'
            ret += '\n'
        ret += "\n----------------"

        return ret
    
if __name__=="__main__":
    players = {}
    x = input("X: ")
    o = input("O: ")
    players['X'] = x
    players['O'] = o
    game = TicTacToe(players)
    while not game.isWin:
        try:
            inp = input().split()
            x = int(inp[0])
            y = int(inp[1])
            if not game.checkavailability():
                print("Game Finished")
                break
            else:
                game.play(x,y)
                print(game)
        except Exception as e:
            print("Invalid Command") 
