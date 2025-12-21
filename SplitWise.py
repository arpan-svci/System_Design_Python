from dataclasses import dataclass
from functools import reduce

@dataclass
class User:
    userID: str
    name: str
    email: str
    mobileNumber: str

class SplitWise:
    def __init__(self, users: list):
        self.users = [User(
            userID = user["userId"],
            name = user["userName"],
            email=user["email"],
            mobileNumber=user["mobileNumber"])
            for user in users]
        self.positions = {user.userID:index for index,user in enumerate(self.users)}
        self.paymentGraph = [[0 for j in range(len(users))] for i in range(len(users))]

    def makePaymentPercentages(self, paidBy :str, amount :float, paidBetween :list, listOfPercentage: list):
        sumOfPercentage = reduce(lambda x,y: x+y, listOfPercentage)
        if sumOfPercentage != 100:
            return False
        payments = []
        for i in range(len(paidBetween)):
            payments.append(round(amount * float(listOfPercentage[i])/100.0, 2))

        source = self.positions[paidBy]
        if source == None:
            return False
        destinations = []
        for i in paidBetween:
            destination = self.positions[i]
            destinations.append(destination)

        for i in range(len(payments)):
            self.paymentGraph[source][destinations[i]] += payments[i]

        print(self.paymentGraph)

    def makePaymentExact(self, paidBy :str, amount :float, paidBetween :list, listOfExactValues :list):
        sumOfMoney = reduce(lambda x,y: x+y, listOfExactValues)
        if sumOfMoney != amount:
            return False
        if paidBy not in self.positions.keys():
            return False
        source = self.positions[paidBy]
        destinations = []

        for i in paidBetween:
            if i not in self.positions.keys():
                return False
            destination = self.positions[i]
            destinations.append(destination)

        for i in range(len(paidBetween)):
            self.paymentGraph[source][destinations[i]] += round(listOfExactValues[i],2)
        
        print(self.paymentGraph)
        
    def makePaymentEquel(self, paidBy :str, amount :float, paidBetween :list):
        dividedValue = round(float(amount)/len(paidBetween),2)
        if paidBy not in self.positions.keys():
            return False
        source = self.positions[paidBy]
        destinations = []
        for i in paidBetween:
            if i not in self.positions.keys():
                return False
            destination = self.positions[i]
            destinations.append(destination)

        for destination in destinations:
            self.paymentGraph[source][destination] = dividedValue

        print(self.paymentGraph)

    def showBalancesForParticularUser(self, userId :str):
        ret = ""
        balances = {}
        if userId not in self.positions.keys():
            return False
        source = self.positions[userId]
        for i in range(len(self.paymentGraph)):
            if i != source:
                balances[i] = self.paymentGraph[source][i]
                balances[i] -= self.paymentGraph[i][source]
        for key, value in balances.items():
            if value < 0:
                ret += f"{self.users[source].name} owes {self.users[key].name}: {-value}\n"
            elif value > 0:
                ret += f"{self.users[key].name} owes {self.users[source].name}: {value}\n"
        return ret

    def showBalances(self):
        value = ""
        balances = {}
        visited = [[False for j in range(len(self.paymentGraph))] for i in range(len(self.paymentGraph[0]))]
        for i in range(len(self.paymentGraph)):
            for j in range(len(self.paymentGraph)):
                if i!=j and visited[i][j] == False:
                    balances[(i,j)] = self.paymentGraph[i][j]
                    balances[(i,j)] += self.paymentGraph[j][i]
                    visited[i][j] = True
                    visited[j][i] = True
        for key, val in balances.items():
            if val != 0:
                source = key[0]
                destination = key[1]
                value += f"{self.users[source].name} owes {self.users[destination].name}: {-val}\n" if val < 0 else f"{self.users[destination].name} owes {self.users[source].name}: {val}\n"
        return value
    
if __name__ == "__main__":
    users = [
        {"userId":"a","userName":"Arpan","email":"arpanmandal913@gmail.com","mobileNumber":"9064713044"},
        {"userId":"b","userName":"Satabda","email":"arpanmandal913@gmail.com","mobileNumber":"9064713044"},
        {"userId":"c","userName":"rahul","email":"arpanmandal913@gmail.com","mobileNumber":"9064713044"},
        {"userId":"d","userName":"Nirmalya","email":"arpanmandal913@gmail.com","mobileNumber":"9064713044"},
        {"userId":"e","userName":"Aniket","email":"arpanmandal913@gmail.com","mobileNumber":"9064713044"}
    ]
    splitwise = SplitWise(users=users)
    while(True):
        try:
            temp = input().split()
            command = temp[0]
            match command:
                case "SHOW":
                    if len(temp) == 1:
                        ret = splitwise.showBalances()
                        print(ret if len(ret)>0 else "No balances")
                    elif len(temp) == 2:
                        ret = splitwise.showBalancesForParticularUser(temp[1])
                        if ret == False:
                            print("User doesnot exist")
                        elif len(ret) == 0:
                            print("No balances")
                        else:
                            print(ret)
                    else:
                        print("Invalid Command")
                case "EXPENSE":
                    source = temp[1]
                    amount = float(temp[2])
                    number = int(temp[3])
                    start = 4
                    ls=[]
                    for i in range(number):
                        ls.append(temp[start + i])
                    next = start + number
                    match temp[next]:
                        case "EQUAL":
                            splitwise.makePaymentEquel(source, amount, ls)
                        case "EXACT":
                            temlist = []
                            start = next+1
                            for i in range(number):
                                temlist.append(float(temp[start + i]))
                            status = splitwise.makePaymentExact(source, amount, ls, temlist)
                            if status == False:
                                print("Invalid amount")
                        case "PERCENT":
                            temlist = []
                            start = next+1
                            for i in range(number):
                                temlist.append(temp[start + i])
                            status = splitwise.makePaymentPercentages(source, amount, ls, temlist)
                            if status == False:
                                print("Invalid percentage")
                case _ :
                    print("Invalid Command")
        except Exception as e:
            print("Invalid Command")

