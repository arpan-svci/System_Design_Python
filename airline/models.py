from abc import ABC

class BankAccount:
    def __init__(self):
        self.users = None
        self.balances = None
        self.transactions = None
        self.accountNumber = None
        self.ifscCode = None
        self.onTransaction = False

class User(ABC):
    def __init__(self, name):
        self.name = name

class Passanger(User):
    def __init__(self, name):
        super().__init__(name)

class Admin(User):
    def __init__(self, name):
        super().__init__(name)

class AirlineStaff(User):
    def __init__(self, name):
        super().__init__(name)

class Flight:
    def __init__(self):
        self.aircraft = None
        self.departure = None
        self.arrival = None
        self.source = None
        self.Destination = None
        self.seats = None
        self.bagages = None
        self.bankAccount = None

class Aircraft:
    def __init__(self):
        self.modelName = None
        self.capacity = None
        self.flights = None

class Bagage:
    def __init__(self):
        self.weight = None
        self.serialNumber = None
        self.ticket = None

class Seat:
    def __init__(self):
        self.seatNumber = None
        self.ticket = None

class Ticket:
    def __init__(self):
        self.ticketId = None
        self.owner = None
        self.transaction = None

class Trasnsaction:
    def __init__(self):
        self.sourceBankAccount = None
        self.destinationBankAccount = None
        self.startTime = None
        self.endTime = None
        self.status = None