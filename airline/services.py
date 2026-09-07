class PaymentService:
    def __init__(self):
        self.transactions = None
    def addTransaction(self):
        pass
    def doPayment(self,amount,source,destination)->str:
        pass
    def canclePayment(self,transactionId):
        pass

class FareCalculator:
    def __init__(self):
        pass
    def calculate(self):
        pass

class RefundCalculator:
    def __init__(self):
        pass
    def calculate(self):
        pass

class BookingService:
    def __init__(self):
        self.paymentService = None
    def bookTicket(self,seats):
        pass
    def cancelBooking(self,ticketId):
        pass

class AssignmentService:
    def __init__(self):
        pass
    def assignCrew(self):
        pass
    def assignAirCraft(self):
        pass
    
class UserService:
    def __init__(self):
        self.users = None
    def addUser(self):
        pass
    def removeUser(self):
        pass
    def updateUserDetails(self):
        pass

class SchedulerService:
    def __init__(self):
        pass
    def scheduleFlight(self,flight):
        pass
    def cancleFlight(self,flightId):
        pass

class BagageHandler:
    def __init__(self):
        pass

class RefundService:
    def __init__(self):
        pass