from dataclasses import dataclass, field
from functools import wraps
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
    userId: str = None
    name: str = None
    email: str = None
    boards: dict[str, bool] = field(default_factory=dict)
    cards: dict[str, bool] = field(default_factory=dict)

    def info(self):
        temp = {
            "id": self.userId,
            "name": self.name,
            "email": self.email
        }
        return temp

@dataclass
class Card:
    id: str = None
    name: str = None
    description: str = None
    assignedUsers: dict[str, bool] = field(default_factory=dict)

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
    id: str = None
    name: str = None
    cards: dict[str, bool] = field(default_factory=dict)
    boardId: str = None

    def info(self):
        temp = {
            "id": self.id,
            "name": self.name,
            "cards": [cardDao.findById(cardId=cardId).info() for cardId, available in self.cards.items() if available is True]
        }
        return temp

@dataclass
class Board:
    id: str = None
    name: str = None
    privacy: BoardPrivacy = BoardPrivacy.PUBLIC
    url: str = None
    members: dict[str, bool] = field(default_factory=dict)
    lists: dict[str, bool] = field(default_factory=dict)

    def info(self):
        temp = {
            "id": self.id,
            "name": self.name,
            "privacy": self.privacy,
            "lists": [listDao.findById(listId).info() for listId, available in self.lists.items() if available is True]
        }
        return temp

class UserDao:
    def __init__(self):
        self.users :dict[str,User] = {}
    
    def user_exist(func):
        @wraps(func)
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
            if cardId not in self.cards:
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
        user = User(name=name, email=email)
        return self.userDao.createUser(user=user)

    def removeUser(self, id):
        return self.userDao.deleteById(userId=id)

    def findUser(self, id: str):
        return self.userDao.findById(userId=id)

class CardService:
    def __init__(self):
        self.cardDao = cardDao

    def addCard(self, name):
        card = Card(name=name)
        return self.cardDao.createCard(card=card)
    
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
        self.cardDao.updateById(cardId=cardId, card=card)
        return True

    def changeCardDescription(self, cardId, description: str):
        card = self.cardDao.findById(cardId=cardId)
        if card is None:
            return False
        card.description = description
        self.cardDao.updateById(cardId=cardId, card=card)
        return True

    def assign(self, cardId, userId):
        card = self.cardDao.findById(cardId=cardId)
        if card is None:
            return False
        user = userDao.findById(userId=userId)
        if user is None:
            return False
        card.assignedUsers[userId] = True
        self.cardDao.updateById(cardId=cardId, card=card)
        return True

    def unassign(self, cardId, userId):
        card = self.cardDao.findById(cardId=cardId)
        if card is None:
            return False
        if userId in card.assignedUsers:
            card.assignedUsers[userId] = False
            self.cardDao.updateById(cardId=cardId, card=card)
        return True

    def move(self, cardId, targetListId):
        card = self.cardDao.findById(cardId=cardId)
        if card is None:
            return False
        target = listDao.findById(listId=targetListId)
        if target is None:
            return False
        # find source list
        source_list = None
        for lst in listDao.lists.values():
            if cardId in lst.cards and lst.cards.get(cardId) is True:
                source_list = lst
                break
        if source_list is None:
            return False
        # ensure same board
        if source_list.boardId != target.boardId:
            return False
        # move
        source_list.cards[cardId] = False
        target.cards[cardId] = True
        listDao.updateById(listId=source_list.id, list=source_list)
        listDao.updateById(listId=target.id, list=target)
        return True

class ListService:
    def __init__(self):
        self.listDao = listDao
        self.cardDao = cardDao

    def addList(self, name):
        lst = List(name=name)
        return self.listDao.createList(list=lst)
    
    def createCard(self, listId , cardName):
        list = self.listDao.findById(listId=listId)
        if list is None:
            return False
        card = Card()
        card.name = cardName
        card = self.cardDao.createCard(card=card)
        list.cards[card.id] = True
        self.listDao.updateById(listId=listId, list=list)
        return card
    
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

    def changeListName(self, listId, name: str):
        lst = self.listDao.findById(listId=listId)
        if lst is None:
            return False
        lst.name = name
        self.listDao.updateById(listId=listId, list=lst)
        return True

class BoardService:
    def __init__(self):
        self.boardDao = boardDao
        self.listDao = listDao
        self.cardDao = cardDao
        self.userDao = userDao

    def addBoard(self, name):
        board = Board(name=name)
        board = self.boardDao.createBoard(board=board)
        if board is None:
            return None
        board.url = f"/board/{board.id}"
        self.boardDao.updateById(boardId=board.id, board=board)
        return board

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
        self.boardDao.updateById(boardId=boardId, board=board)
        return True

    def removeMember(self, boardId, userId):
        board = self.boardDao.findById(boardId=boardId)
        if board is None:
            return False
        if userId in board.members:
            board.members[userId] = False
            self.boardDao.updateById(boardId=boardId, board=board)
        return True

    def setUrl(self, boardId, url: str):
        board = self.boardDao.findById(boardId=boardId)
        if board is None:
            return False
        board.url = url
        self.boardDao.updateById(boardId=boardId, board=board)
        return True

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
        self.boardDao.updateById(boardId=boardId, board=board)
        return list

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

    def removeUserFromBoard(self, boardId, userId):
        return self.boardService.removeMember(boardId=boardId, userId=userId)

    def changeListName(self, listId, name):
        return self.listService.changeListName(listId=listId, name=name)

    def setCardName(self, cardId, name):
        return self.cardService.changeCardName(cardId=cardId, cardName=name)

    def setCardDescription(self, cardId, description):
        return self.cardService.changeCardDescription(cardId=cardId, description=description)

    def assignCard(self, cardId, userId):
        return self.cardService.assign(cardId=cardId, userId=userId)

    def unassignCard(self, cardId, userId):
        return self.cardService.unassign(cardId=cardId, userId=userId)

    def moveCard(self, cardId, targetListId):
        return self.cardService.move(cardId=cardId, targetListId=targetListId)
    
    def deleteBoard(self, boardId):
        return self.boardService.deleteBoard(boardId)
    
    def deleteList(self, listId):
        return self.listService.deleteList(listId = listId)

    def deleteCard(self, cardId):
        return self.cardService.deleteCard(cardId=cardId)
    
    def changeCardName(self, cardId, name):
        return self.cardService.changeCardName(cardId = cardId, cardName = name)
    