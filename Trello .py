from dataclasses import dataclass, field
from enum import Enum
import uuid

class UUIDGenerator:
    @staticmethod
    def generate() -> str:
        return str(uuid.uuid4())

idGenerator = UUIDGenerator()

class BoardPrivacy(Enum):
    PUBLIC = "public"
    PRIVATE = "private"

@dataclass
class User:
    userId: str
    name: str = None
    email: str = None

    def info(self):
        temp = {
            "id": self.userId,
            "name": self.name,
            "email": self.email
        }
        return temp

@dataclass
class Card:
    id: str
    name: str = None
    description: str = None
    assignedUsers: dict[str,User] = field(default_factory = dict)

    def info(self):
        temp = {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "assigned Users": [user.info() for user in self.assignedUsers.values()]
        }
        return temp


@dataclass
class List:
    id :str
    name: str = None
    cards: dict[str,Card] = field(default_factory = dict)

    def info(self):
        temp = {
            "id": self.id,
            "name": self.name,
            "cards": [card.info() for card in self.cards.values()]
        }
        return temp

@dataclass
class Board:
    id: str
    name: str = None
    privacy: BoardPrivacy = None
    lists: dict[str,List] = field(default_factory = dict)

    def info(self):
        temp = {
            "id": self.id,
            "name": self.name,
            "privacy": self.privacy,
            "lists": [list.info() for list in self.lists.values()]
        }
        return temp

class UserService:
    def __init__(self):
        self.users :dict[str,User] = {}

    def addUser(self, name, email):
        id = idGenerator.generate()
        tempUser = User(userId= id, name= name, email= email)
        self.users[id] = tempUser
        return tempUser
    
    def removeUser(self, id):
        if id not in self.users:
            return False
        else:
            del self.users[id]

    def findUser(self, id: str):
        if id not in self.users.keys():
            return False
        else:
            return self.users[id]

class CardService:
    def __init__(self):
        self.cards :dict[str,Card] = {}

    def addCard(self, name):
        id = idGenerator.generate()
        tempCard = Card(id=id, name=name)
        self.cards[id] = tempCard
        return tempCard
    
    def deleteCard(self, id):
        if id in self.cards.keys():
            del self.cards[id]
        else:
            return False
        
    def info(self, cardId):
        if cardId in self.cards.keys():
            return self.cards[cardId]
        else:
            return False

class ListService:
    def __init__(self):
        self.lists :dict[str,List]= {}

    def addList(self, name):
        id = idGenerator.generate()
        tempList = List(id=id, name=name)
        self.lists[id] = tempList
        return tempList
    
    def deleteList(self, id):
        if id in self.lists.keys():
            del self.lists[id]
        else:
            return False
    
    def info(self, listId):
        if listId in self.lists.keys():
            return self.lists[listId].info()
        else:
            return False

class BoardService:
    def __init__(self):
        self.boards :dict[str,Board] = {}

    def addBoard(self, name):
        id = idGenerator.generate()
        tempBoard = Board(id=id, name=name)
        self.boards[id] = tempBoard
        return tempBoard
    
    def deleteBoard(self, id):
        if id in self.boards.keys():
            del self.boards[id]
        else:
            return False
        
    def info(self, boardId):
        if boardId in self.boards.keys():
            return self.boards[boardId].info()
        else:
            return False
        
    def infoAllBoards(self):
        temp = []
        for board in self.boards.values():
            temp.append(board.info())
        if len(temp) == 0:
            return False
        return temp

class Trello:
    def __init__(self):
        self.boardService = BoardService()
        self.userService = UserService()
        self.ListService = ListService()
        self.cardService = CardService()
    
    def createBoard(self, name):
        board = self.boardService.addBoard(name=name)
        return board
    
    def show(self):
        return self.boardService.info()
    
    def showBoard(self, boardId):
        return self.boardService.info(boardId=boardId)
    
    def showList(self, listId):
        return self.ListService.info(listId=listId)
    
    def showCard(self, cardId):
        return self.cardService.info(cardId=cardId)

