from dataclasses import dataclass, field
from functools import wraps
from enum import Enum
import uuid

class Board:
    pass
class Card:
    pass

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
    boards: dict[str,Board] = field(default_factory=dict)
    cards: list[str,Card] = field(default_factory=dict)

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
    board: Board

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
    url: str = None
    members: dict[str,User] = field(default_factory = dict)
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
    
    def user_exist(func):
        @wrapper(func)
        def wrapper(self, userId, *args, **kwargs):
            if userId not in self.users:
                return False
            return func(self, userId, *args, **kwargs)
        return wrapper

    def addUser(self, name, email):
        id = idGenerator.generate()
        tempUser = User(userId= id, name= name, email= email)
        self.users[id] = tempUser
        return tempUser
    
    @user_exist
    def removeUser(self, id):
        del self.users[id]

    @user_exist
    def findUser(self, id: str):
        return self.users[id]

class CardService:
    def __init__(self):
        self.cards :dict[str,Card] = {}
    
    def card_exists(func):
        @wraps(func)
        def wrapper(self, cardId, *args, **kwargs):
            if cardId not in self.lists:
                return False
            return func(self, cardId, *args, **kwargs)
        return wrapper

    def addCard(self, name):
        id = idGenerator.generate()
        tempCard = Card(id=id, name=name)
        self.cards[id] = tempCard
        return tempCard
    
    @card_exists
    def deleteCard(self, id):
        del self.cards[id]
    
    @card_exists
    def info(self, cardId):
        return self.cards[cardId]

class ListService:
    def __init__(self):
        self.lists :dict[str,List]= {}
    
    def list_exists(func):
        @wraps(func)
        def wrapper(self, listId, *args, **kwargs):
            if listId not in self.lists:
                return False
            return func(self, listId, *args, **kwargs)
        return wrapper

    def addList(self, name):
        id = idGenerator.generate()
        tempList = List(id=id, name=name)
        self.lists[id] = tempList
        return tempList
    
    @list_exists
    def deleteList(self, id):
        del self.lists[id]
    
    @list_exists
    def info(self, listId):
        return self.lists[listId].info()

class BoardService:
    def __init__(self):
        self.boards :dict[str,Board] = {}
    
    def board_exists(func):
        @wraps(func)
        def wrapper(self, boardId, *args, **kwargs):
            if boardId not in self.boards:
                return False
            return func(self, boardId, *args, **kwargs)
        return wrapper

    def addBoard(self, name):
        id = idGenerator.generate()
        tempBoard = Board(id=id, name=name)
        self.boards[id] = tempBoard
        return tempBoard
    
    @board_exists
    def deleteBoard(self, id):
        del self.boards[id]
    
    @board_exists
    def changeBoardPrivacyById(self, boardId, privacy):
        self.boards[boardId].privacy = privacy
    
    @board_exists
    def addMember(self, boardId, user: User):
        self.boards[boardId].members[user.userId] = user
    
    @board_exists
    def setUrl(self, boardId, url: str):
        self.boards[boardId].url = url
    
    @board_exists
    def setName(self, boardId, name: str):
        self.boards[boardId].name = name

    @board_exists
    def info(self, boardId):
        return self.boards[boardId].info()
    
    @board_exists
    def findBoard(self, boardId):
        return self.boards[boardId]
        
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
        self.listService = ListService()
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

    def createList(self, boardId, nameOfList):
        board = self.boardService.findBoard(boardId)
        if board is False:
            return False
        list = self.listService.addList(name=nameOfList)
        list.board = board
        board.lists[list.id] = list
    
    def setBoardName(self, boardId, name):
        self.boardService.setName(boardId=boardId, name=name)
    
    def setBoardPrivacy(self, boardId, privacy: str):
        temp = None
        if privacy.lower() == "private":
            temp = BoardPrivacy.PRIVATE
        elif privacy.lower() == "public":
            temp = BoardPrivacy.PUBLIC
        else:
            return False
        self.boardService.changeBoardPrivacyById(boardId=boardId, privacy=temp)
    
    def addUserToBoard(self, boardId, userId):
        user = self.userService.findUser(id=userId)
        if user is False:
            return False
        board = self.boardService.findBoard(boardId=boardId)
        if board is False:
            return False
        board.members[userId] = user
        user.boards[boardId] = board
    
     

