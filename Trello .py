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

class UserDao:
    def __init__(self):
        self.users :dict[str,User] = {}
    
    def user_exist(func):
        @wrapper(func)
        def wrapper(self, userId, *args, **kwargs):
            if userId not in self.users:
                return None
            return func(self, userId, *args, **kwargs)
        return wrapper

    def createUser(self, user:User):
        userId = idGenerator.generate()
        user.userId = userId
        self.users[userId] = user
        return user
    
    @user_exist
    def findById(self, userId:str):
        return self.users[userId]
    
    @user_exist
    def deleteById(self, userId):
        user = self.users[userId]
        del self.users[userId]
        return user
    
    @user_exist
    def updateUserById(self, userId: str, user: User):
        self.users[userId] = user
        return self.users[userId]

class CardDao:
    def __init__(self):
        self.cards :dict[str,Card] = {}

    def card_exists(func):
        @wraps(func)
        def wrapper(self, cardId, *args, **kwargs):
            if cardId not in self.lists:
                return None
            return func(self, cardId, *args, **kwargs)
        return wrapper

    def createCard(self, card :Card):
        cardId = idGenerator.generate()
        card.id = cardId
        self.cards[cardId] = card
        return card
    
    @card_exists
    def findById(self, cardId):
        return self.cards[cardId]
    
    @card_exists
    def updateById(self, cardId, card: Card):
        self.cards[cardId] = card
        return self.cards[cardId]
    
    @card_exists
    def deleteById(self, cardId):
        card = self.cards[cardId]
        del self.cards[cardId]
        return card

class ListDao:
    def __init__(self):
        self.lists :dict[str,List] = {}
    
    def list_exists(func):
        @wraps(func)
        def wrapper(self, listId, *args, **kwargs):
            if listId not in self.lists:
                return None
            return func(self, listId, *args, **kwargs)
        return wrapper

    @list_exists
    def findById(self, listId):
        return self.lists[listId]
    
    def createList(self, list: List):
        listId = idGenerator.generate()
        list.id = listId
        self.lists[listId] = list
        return list
    
    @list_exists
    def updateById(self, listId, list: List):
        self.lists[listId] = list
        return self.lists[listId]
    
    @list_exists
    def deleteById(self, listId):
        list = self.lists[listId]
        del self.lists[listId]
        return list

class BoardDao:
    def __init__(self):
        self.boards :dict[str,Board] = {}
    
    def board_exists(func):
        @wraps(func)
        def wrapper(self, boardId, *args, **kwargs):
            if boardId not in self.boards:
                return False
            return func(self, boardId, *args, **kwargs)
        return wrapper


    def createBoard(self, board: Board):
        boardId = idGenerator.generate()
        board.id = boardId
        self.boards[boardId] = board
        return board
    
    @board_exists
    def findById(self, boardId):
        return self.boards[boardId]
    
    @board_exists
    def updateById(self, boardId: str, board: Board):
        self.boards[boardId] = board
        return self.boards[boardId]
    
    @board_exists
    def deleteById(self, boardId: str):
        board = self.boards[boardId]
        del self.boards[boardId]
        return board

userDao = UserDao()
cardDao = CardDao()
listDao = ListDao()
boardDao = BoardDao()

class UserService:
    def __init__(self):
        self.userDao = userDao

    def addUser(self, name, email):
        pass

    def removeUser(self, id):
        del self.users[id]

    def findUser(self, id: str):
        return self.users[id]

class CardService:
    def __init__(self):
        self.cards :dict[str,Card] = {}

    def addCard(self, name):
        pass
    
    def deleteCard(self, id):
        pass
    
    def info(self, cardId):
        pass

class ListService:
    def __init__(self):
        self.listDao = listDao

    def addList(self, name):
        pass
    
    def deleteList(self, id):
        pass
    
    def info(self, listId):
        pass

class BoardService:
    def __init__(self):
        self.boards :dict[str,Board] = {}

    def addBoard(self, name):
        pass

    def deleteBoard(self, boardId):    
        pass

    def changeBoardPrivacyById(self, boardId, privacy):
        pass

    def addMember(self, boardId, user: User):
        pass

    def addList(self, boardId, list: List):
        pass

    def setUrl(self, boardId, url: str):
        pass

    def setName(self, boardId, name: str):
        pass

    def info(self, boardId):
        pass

    def findBoard(self, boardId):
        pass

    def infoAllBoards(self):
        pass

class Trello:
    def __init__(self):
        self.boardService = BoardService()
        self.userService = UserService()
        self.listService = ListService()
        self.cardService = CardService()
    
    def show(self):
        return self.boardService.info()
    
    def showBoard(self, boardId):
        return self.boardService.info(boardId=boardId)
    
    def showList(self, listId):
        return self.ListService.info(listId=listId)
    
    def showCard(self, cardId):
        return self.cardService.info(cardId=cardId)

    def createBoard(self, name):
        board = self.boardService.addBoard(name=name)
        return board
    
    def createList(self, boardId, nameOfList):
        board = self.boardService.findBoard(boardId)
        if board is False:
            return False
        list = self.listService.addList(name=nameOfList)
        list.board = board
        self.boardService.addList(boardId=boardId, list=list)
    
    def setBoardName(self, boardId, name):
        return self.boardService.setName(boardId=boardId, name=name)
    
    def setBoardPrivacy(self, boardId, privacy: str):
        temp = None
        if privacy.lower() == "private":
            temp = BoardPrivacy.PRIVATE
        elif privacy.lower() == "public":
            temp = BoardPrivacy.PUBLIC
        else:
            return False
        return self.boardService.changeBoardPrivacyById(boardId=boardId, privacy=temp)
    
    def addUserToBoard(self, boardId, userId):
        user = self.userService.findUser(id=userId)
        if user is False:
            return False
        status = self.boardService.addMember(boardId=boardId, user=user)
        if status == False:
            return False
    
    def deleteBoard(self, boardId):
        return self.boardService.deleteBoard(boardId)
        
    
     

