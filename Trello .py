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
    boards: dict[str,bool] = field(default_factory=dict)
    cards: list[str,bool] = field(default_factory=dict)

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
    assignedUsers: dict[str,bool] = field(default_factory = dict)

    def info(self):
        temp = {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "assigned Users": [userDao.findById(userId=userId).info() for userId, available in self.assignedUsers.items() if available is True]
        }
        return temp

@dataclass
class List:
    id :str
    name: str = None
    cards: dict[str,bool] = field(default_factory = dict)
    boardId: str

    def info(self):
        temp = {
            "id": self.id,
            "name": self.name,
            "cards": [cardDao.findById(cardId=cardId).info() for cardId, available in self.cards.items() if available is True]
        }
        return temp

@dataclass
class Board:
    id: str
    name: str = None
    privacy: BoardPrivacy = None
    url: str = None
    members: dict[str,bool] = field(default_factory = dict)
    lists: dict[str,bool] = field(default_factory = dict)

    def info(self):
        temp = {
            "id": self.id,
            "name": self.name,
            "privacy": self.privacy,
            "lists": [boardDao.findById(listId).info() for listId, available in self.lists.items() if available is True]
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
    
    def findAll(self):
        return [board for board in self.boards.values()]

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
        self.cardDao = cardDao

    def addCard(self, name):
        pass
    
    def deleteCard(self, cardId):
        if self.cardDao.deleteById(cardId=cardId) is None:
            return False
        else:
            return True
    
    def info(self, cardId):
        return self.cardDao.findById(cardId=cardId).info()
    
    def changeCardName(self, cardId , cardName):
        card = self.cardDao.findById(cardId=cardId)
        if card is None:
            return False
        card.name = cardName
        return True

class ListService:
    def __init__(self):
        self.listDao = listDao
        self.cardDao = cardDao

    def addList(self, name):
        pass
    
    def createCard(self, listId , cardName):
        list = self.listDao.findById(listId=listId)
        if list is None:
            return False
        card = Card()
        card.name = cardName
        card = self.cardDao.createCard(card=card)
        list.cards[card.id] = True
        return True
    
    def deleteList(self, listId):
        list = self.listDao.findById(listId=listId)
        if list is None:
            return False
        for cardId in list.cards.keys():
            self.cardDao.deleteById(cardId=cardId)
        self.listDao.deleteById(listId=listId)
        return True
    
    def info(self, listId):
        return self.listDao.findById(listId=listId).info()

class BoardService:
    def __init__(self):
        self.boardDao = boardDao
        self.listDao = listDao
        self.cardDao = cardDao
        self.userDao = userDao

    def addBoard(self, name):
        board = Board(name = name)
        if self.boardDao.createBoard(board = board) is not None:
            return True
        else:
            return False

    def deleteBoard(self, boardId):    
        board = self.boardDao.findById(boardId=boardId)
        if board is None:
            return False
        
        for listId in board.lists.keys():
            list = self.listDao.findById(listId=listId)
            for cardId in list.cards.keys():
                cardDao.deleteById(cardId=cardId)
            self.listDao.deleteById(listId=listId)
        self.boardDao.deleteById(boardId=boardId)
        return True


    def changeBoardPrivacyById(self, boardId, privacy):
        board = self.boardDao.findById(boardId=boardId)
        if board is None:
            return False
        board.privacy = privacy
        self.boardDao.updateById(boardId=boardId, board=board)
        return True

    def addMember(self, boardId, userId):
        user = self.userDao.findById(userId=userId)
        if user is None:
            return False
        board = self.boardDao.findById(boardId=boardId)
        if board is None:
            return False
        board.members[userId] = True

    def setUrl(self, boardId, url: str):
        pass

    def setName(self, boardId, name: str):
        board = self.boardDao.findById(boardId=boardId)
        if board is None:
            return False
        board.name = name
        self.boardDao.updateById(boardId=boardId, board=board)
        return True

    def info(self, boardId):
        return self.boardDao.findById(boardId=boardId).info()

    def findBoard(self, boardId):
        return self.boardDao.findById(boardId=boardId)

    def infoAllBoards(self):
        return [board.info() for board in self.boardDao.findAll()]
    
    def createList(self, boardId, nameOfList):
        board = self.boardDao.findById(boardId=boardId)
        if board is None:
            return False
        list = List(name=nameOfList)
        list = self.listDao.createList(list=list)
        board.lists[list.id] = True
        list.boardId = boardId
        return True

class Trello:
    def __init__(self):
        self.boardService = BoardService()
        self.userService = UserService()
        self.listService = ListService()
        self.cardService = CardService()
    
    def show(self):
        return self.boardService.infoAllBoards()
    
    def showBoard(self, boardId):
        return self.boardService.info(boardId=boardId)
    
    def showList(self, listId):
        return self.listService.info(listId=listId)
    
    def showCard(self, cardId):
        return self.cardService.info(cardId=cardId)

    def createBoard(self, name):
        return self.boardService.addBoard(name=name)
    
    def createList(self, boardId, nameOfList):
        return self.boardService.createList(boardId=boardId, nameOfList=nameOfList)
    
    def createCard(self, listId, cardName):
        return self.listService.createCard(listId = listId, cardName = cardName)
    
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
        return self.boardService.addMember(boardId=boardId, userId=userId)
    
    def deleteBoard(self, boardId):
        return self.boardService.deleteBoard(boardId)
    
    def deleteList(self, listId):
        return self.listService.deleteList(listId = listId)

    def deleteCard(self, cardId):
        return self.cardService.deleteCard(cardId=cardId)
    
    def changeCardName(self, cardId, name):
        return self.cardService.changeCardName(cardId = cardId, cardName = name)
    