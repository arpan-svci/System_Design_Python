from abc import abstractmethod, ABC

def getPositionIndex(position):
    """Convert algebraic position (e.g. 'e4') to board indices (px, py).

    - px: row index where 0 corresponds to top (rank 8) and 7 to bottom (rank 1)
    - py: column index where 0 corresponds to file 'a' and 7 to file 'h'

    Returns (px, py) on success, or False for invalid input.
    """
    try:
        if not isinstance(position, str) or len(position) != 2:
            return False
        col = position[0].lower()
        row = position[1]
        if col < 'a' or col > 'h':
            return False
        if row < '1' or row > '8':
            return False
        py = ord(col) - ord('a')
        px = 8 - int(row)
        return (px, py)
    except Exception:
        return False
    
def getPositionCode(px=None, py=None):
    """Convert board indices (px, py) back to algebraic notation like 'e4'.

    Returns the string like 'a1'..'h8' on success, or False for invalid input.
    """
    try:
        if px is None or py is None:
            return False
        if 0 <= px < 8 and 0 <= py < 8:
            col = chr(ord('a') + py)
            row = str(8 - px)
            return f"{col}{row}"
        else:
            return False
    except Exception:
        return False

class ChessBoard:
    def __init__(self):
        self.currentTurn = 'White'
        self.moveNumber = {'White': 0, 'Black': 0}
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self._initialize_pieces()
    
    def _initialize_pieces(self):
        """Initialize all chess pieces in their starting positions."""
        # White pawns on rank 2 (row 6)
        for col in range(8):
            pos = chr(ord('a') + col) + '2'
            self.board[6][col] = Pawn(pos, self, 'White')
        
        # Black pawns on rank 7 (row 1)
        for col in range(8):
            pos = chr(ord('a') + col) + '7'
            self.board[1][col] = Pawn(pos, self, 'Black')
        
        # White pieces on rank 1 (row 7)
        piece_order = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        for col, PieceClass in enumerate(piece_order):
            pos = chr(ord('a') + col) + '1'
            self.board[7][col] = PieceClass(pos, self, 'White')
        
        # Black pieces on rank 8 (row 0)
        for col, PieceClass in enumerate(piece_order):
            pos = chr(ord('a') + col) + '8'
            self.board[0][col] = PieceClass(pos, self, 'Black')
    
    def move(self, startPosition, endPosition):
        pos = getPositionIndex(startPosition)
        if pos == False:
            return False
        x, y = pos
        if self.board[x][y] is None:
            return False
        if self.board[x][y].validatemove(endPosition):
            self.board[x][y].move(endPosition)
            self.currentTurn = 'Black' if self.currentTurn == 'White' else 'White'
            return True
        return False
        
    def availableMoves(self, start):
        pos = getPositionIndex(start)
        if pos == False:
            return False
        x, y = pos
        piece = self.board[x][y]
        if piece is None:
            return False
        return piece.possiblemoves()
        
    def print(self):
        files = ' '.join([chr(ord('a') + i)+' ' for i in range(8)])
        print("   " + files)
        for i, row in enumerate(self.board):
            rank = 8 - i
            row_cells = ' '.join([cell.getCode() if cell is not None else '--' for cell in row])
            print(f"{rank} {row_cells} {rank}")
        print("   " + files)

class Piece(ABC):
    def __init__(self, position, board, color, piece):
        self.position = position
        pos = getPositionIndex(position)
        self.positionIndex = pos if pos != False else (0, 0)
        self.board = board
        self.color = color
        self.piece = piece
        self.moveNumber = 0
    @abstractmethod
    def getCode(self):
        pass
    def getOppositeColor(self):
        return 'Black' if self.color=='White' else 'White'
    
    @abstractmethod
    def possiblemoves(self):
        pass
    def validatemove(self, destination):
        return destination in self.possiblemoves()
    def move(self, destination):
        if not self.validatemove(destination):
            return False
        px, py = self.positionIndex
        self.board.board[px][py] = None
        self.position = destination
        pos = getPositionIndex(destination)
        self.positionIndex = pos if pos != False else (0, 0)
        curpx, curpy = self.positionIndex
        self.board.board[curpx][curpy] = self
        self.moveNumber += 1
        return True
        

class Pawn(Piece):
    def __init__(self, position, board, color):
        super().__init__(position=position, board=board, color=color, piece="Pawn")

    def getCode(self):
        return 'WP' if self.color == 'White' else 'BP'
    
    def possiblemoves(self):
        possibleMoves = []
        if self.board.currentTurn != self.color:
            return []
        direction = -1 if self.color == 'White' else 1
        px, py = self.positionIndex
        # Forward move (single step)
        if 0 <= px + direction < 8 and self.board.board[px + direction][py] is None:
            possibleMoves.append(getPositionCode(px + direction, py))
        # Forward move (double step on first move)
        if self.moveNumber == 0 and self.board.board[px + direction][py] is None and self.board.board[px + 2*direction][py] is None:
            possibleMoves.append(getPositionCode(px + 2*direction, py))
        # Capture moves
        if 0 <= px + direction < 8:
            if py > 0 and self.board.board[px + direction][py - 1] is not None and self.board.board[px + direction][py - 1].color != self.color:
                possibleMoves.append(getPositionCode(px + direction, py - 1))
            if py < 7 and self.board.board[px + direction][py + 1] is not None and self.board.board[px + direction][py + 1].color != self.color:
                possibleMoves.append(getPositionCode(px + direction, py + 1))
        return possibleMoves
    
class Knight(Piece):
    def __init__(self, position, board, color):
        super().__init__(position, board, color, piece='Knight')
    
    def getCode(self):
        return 'WN' if self.color == 'White' else 'BN'
    
    def possiblemoves(self):
        possibleMoves = []
        directions = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (-1, 2), (1, -2), (-1, -2)]
        px, py = self.positionIndex
        for dx, dy in directions:
            mx, my = px + dx, py + dy
            if 0 <= mx < 8 and 0 <= my < 8:
                target = self.board.board[mx][my]
                if target is None or target.color != self.color:
                    possibleMoves.append(getPositionCode(mx, my))
        return possibleMoves

class Rook(Piece):
    def __init__(self, position, board, color):
        super().__init__(position, board, color, piece='Rook')
    
    def getCode(self):
        return 'WR' if self.color == 'White' else 'BR'

    def possiblemoves(self):
        possibleMoves = []
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        px, py = self.positionIndex
        for dx, dy in directions:
            k = 1
            while True:
                mx, my = px + k*dx, py + k*dy
                if not (0 <= mx < 8 and 0 <= my < 8):
                    break
                target = self.board.board[mx][my]
                if target is None:
                    possibleMoves.append(getPositionCode(mx, my))
                else:
                    if target.color != self.color:
                        possibleMoves.append(getPositionCode(mx, my))
                    break
                k += 1
        return possibleMoves

class Bishop(Piece):
    def __init__(self, position, board, color):
        super().__init__(position, board, color, piece="Bishop")
    
    def getCode(self):
        return 'WB' if self.color == 'White' else 'BB'
    
    def possiblemoves(self):
        possibleMoves = []
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        px, py = self.positionIndex
        for dx, dy in directions:
            k = 1
            while True:
                mx, my = px + k*dx, py + k*dy
                if not (0 <= mx < 8 and 0 <= my < 8):
                    break
                target = self.board.board[mx][my]
                if target is None:
                    possibleMoves.append(getPositionCode(mx, my))
                else:
                    if target.color != self.color:
                        possibleMoves.append(getPositionCode(mx, my))
                    break
                k += 1
        return possibleMoves
    
class Queen(Piece):
    def __init__(self, position, board, color):
        super().__init__(position, board, color, piece="Queen")
    
    def getCode(self):
        return 'WQ' if self.color == 'White' else 'BQ'
    
    def possiblemoves(self):
        possibleMoves = []
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1), (0, 1), (0, -1), (1, 0), (-1, 0)]
        px, py = self.positionIndex
        for dx, dy in directions:
            k = 1
            while True:
                mx, my = px + k*dx, py + k*dy
                if not (0 <= mx < 8 and 0 <= my < 8):
                    break
                target = self.board.board[mx][my]
                if target is None:
                    possibleMoves.append(getPositionCode(mx, my))
                else:
                    if target.color != self.color:
                        possibleMoves.append(getPositionCode(mx, my))
                    break
                k += 1
        return possibleMoves
        
class King(Piece):
    def __init__(self, position, board, color):
        super().__init__(position, board, color, piece="King")
    
    def getCode(self):
        return 'WK' if self.color == 'White' else 'BK'
    
    def possiblemoves(self):
        possibleMoves = []
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1), (0, 1), (0, -1), (1, 0), (-1, 0)]
        px, py = self.positionIndex
        for dx, dy in directions:
            mx, my = px + dx, py + dy
            if 0 <= mx < 8 and 0 <= my < 8:
                target = self.board.board[mx][my]
                if target is None or target.color != self.color:
                    possibleMoves.append(getPositionCode(mx, my))
        return possibleMoves


class ChessController():
    def __init__(self):
        self.board = ChessBoard()
    
    def move(self,startPosition,endPosition):
        if self.board.move(startPosition,endPosition) == True:
            self.print()
            return True
        else:
            return False

    def availableMoves(self,start):
        return self.board.availableMoves(start)

    def print(self):
        self.board.print()

if __name__=="__main__":
    controller = ChessController()
    while True:
        try:
            temp = input().split()
            match temp[0]:
                case 'MOVE':
                    if controller.move(temp[1],temp[2]):
                        print("Moved The Piece")
                case 'SHOW':
                    controller.print()
                case 'GET':
                    res = controller.availableMoves(temp[1])
                    print("Availavle Moves: "+str(res) if res != False else "No Piece in the position")
                case 'EXIT':
                    print("Exited")
        except Exception as e:
            print("Invalid Command")