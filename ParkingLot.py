from dataclasses import dataclass

class VehicleType:
    Car = "CAR"
    Bike = "BIKE"
    Truck = "TRUCK"

class ParkingLot:
    def __init__(self, parkingLotId :str, numberOfFloors :int, numberOfSlots :int ):
        self.parkingLotId = parkingLotId
        self.VehicleTypes = {"CAR":VehicleType.Car,
                             "BIKE":VehicleType.Bike,
                             "TRUCK":VehicleType.Truck}
        self.numberOfFloors = numberOfFloors
        self.numberOfSlots = numberOfSlots
        self.floors = [ParkingFloor(numberOfSlots = numberOfSlots, floorNumber = i+1) for i in range(numberOfFloors)]
    
    def parkVehicle(self, vehicleType, regNumber, color):
        for floor in self.floors:
            if floor.freeSlotCount(vehicleType = vehicleType) > 0 :
                space = floor.parkVehicle(vehicleType = vehicleType, regNumber = regNumber, color = color)
                if space is not False:
                    return f"Parked Vehicle. Ticket ID: {self.parkingLotId+space}"
        else:
            return "Parking Lot Full"


    def unparkVehicle(self, ticketId: str):
        try:
            temp = ticketId.split('_')
            print(temp)
            floor = int(temp[1])
            slot = int(temp[2])
            if len(temp) != 3:
                return "Invalid Ticket"
            if temp[0] != self.parkingLotId:
                return "Invalid Ticket"
            if floor < 1 and floor > self.numberOfFloors:
                return "Invalid Ticket"
            if slot < 1 and slot > self.numberOfSlots:
                return "Invalid Ticket"
            details = self.floors[floor-1].unparkVehicle(slot = slot)
            if details == False:
                print("Hello")
                return "Invalid Ticket"
            return f"Unparked vehicle with Registration Number: {details["RegNumber"]} and Color: {details['color']}"

        except Exception as e:
            return "Invalid Ticket"

    def displayFreeCount(self, vehicleType):
        display = ""
        for floor in self.floors:
            count = floor.freeSlotCount(vehicleType=vehicleType)
            display += f"No. of free slots for {vehicleType} on Floor {floor.floorNumber}: {count}\n"
        return display

    def displayFreeSlots(self, vehicleType):
        display = ""
        for floor in self.floors:
            freeslots = floor.freeSlots(vehicleType=vehicleType)
            display += f"Free slots for {vehicleType} on Floor {floor.floorNumber}: {','.join(map(str,freeslots))}\n"
        return display

    def displayOccupiedSlots(self, vehicleType):
        display = ""
        for floor in self.floors:
            occupiedSlots = floor.occupiedSlot(vehicleType=vehicleType)
            display += f"Occupied slots for {vehicleType} on Floor {floor.floorNumber}: {','.join(map(str, occupiedSlots))}\n"
        return display

class ParkingFloor:
    def __init__(self,numberOfSlots,floorNumber):
        self.parkingSlots = [None for i in range(numberOfSlots)]
        self.floorNumber = floorNumber
        for i in range(numberOfSlots):
            if i == 0:
                self.parkingSlots[i] = ParkingSlot(isOccupied = False, vehicleType = VehicleType.Truck, vehicleColor = None, vehicleRegNumber = None, floor = floorNumber, slot = i+1 )
            elif i > 0 and i <= 2:
                self.parkingSlots[i] = ParkingSlot(isOccupied = False, vehicleType = VehicleType.Bike, vehicleColor = None, vehicleRegNumber = None, floor = floorNumber, slot = i+1 )
            else:
                self.parkingSlots[i] = ParkingSlot(isOccupied = False, vehicleType = VehicleType.Car, vehicleColor = None, vehicleRegNumber = None, floor = floorNumber , slot = i+1 )

    def parkVehicle(self, vehicleType, regNumber, color):
        freeSpot = self.findFirstFreeSpot(vehicleType = vehicleType)
        if freeSpot == False:
            return False
        else:
            freeSpot.vehicleRegNumber = regNumber
            freeSpot.vehicleColor = color
            freeSpot.isOccupied = True
            floor = freeSpot.floor
            slot = freeSpot.slot
            return f"_{floor}_{slot}"

    def unparkVehicle(self, slot):
        spot = self.parkingSlots[slot-1]
        if spot.isOccupied == False:
            return False
        currentRegNumber = spot.vehicleRegNumber
        currentVehicleColor = spot.vehicleColor
        spot.isOccupied = False
        spot.vehicleRegNumber =  None
        spot.vehicleColor = None
        return {"RegNumber":currentRegNumber,"color":currentVehicleColor}

    def freeSlotCount(self,vehicleType):
        count = 0
        for slot in self.parkingSlots:
            if slot.vehicleType == vehicleType and slot.isOccupied == False:
                count+=1
        return count

    def freeSlots(self,vehicleType):
        freeslots = []
        for slot in self.parkingSlots:
            if slot.vehicleType == vehicleType and slot.isOccupied == False:
                freeslots.append(slot.slot)
        return freeslots

    def occupiedSlot(self,vehicleType):
        occupiedSlots = []
        for slot in self.parkingSlots:
            if slot.vehicleType == vehicleType and slot.isOccupied == True:
                occupiedSlots.append(slot.slot)
        return occupiedSlots

    def findFirstFreeSpot(self, vehicleType):
        for slot in self.parkingSlots:
            if slot.isOccupied == False and slot.vehicleType == vehicleType:
                return slot
        else:
            return False

@dataclass
class ParkingSlot:
    isOccupied: bool
    vehicleType: str
    vehicleColor: str
    vehicleRegNumber: str
    floor: int
    slot: int

if __name__ == "__main__":
    try:
        while True:
            temp = input().split()
            print(temp)
            command = temp[0]
            match command:
                case "create_parking_lot":
                    parking_lot_id = temp[1]
                    floor_counts = int(temp[2])
                    slot_counts = int(temp[3])
                    parking = ParkingLot(parkingLotId = parking_lot_id, numberOfFloors = floor_counts, numberOfSlots = slot_counts)
                    print(f"Created parking lot with {floor_counts} floors and {slot_counts} slots per floor")

                case "park_vehicle":
                    vehicleType = temp[1]
                    regNumber = temp[2]
                    color = temp[3]
                    if vehicleType in parking.VehicleTypes.keys():
                        print(parking.parkVehicle(vehicleType, regNumber, color))
                    else:
                        print("Invalid Command")

                case "unpark_vehicle":
                    ticket_id = temp[1]
                    print(parking.unparkVehicle(ticket_id))

                case "display":
                    vehicleType = temp[2]
                    if vehicleType in parking.VehicleTypes.keys():
                        match temp[1]:
                            case "free_count":
                                print(parking.displayFreeCount(vehicleType))

                            case "free_slots":
                                print(parking.displayFreeSlots(vehicleType))

                            case  "occupied_slots":
                                print(parking.displayOccupiedSlots(vehicleType))

                            case _:
                                print("Invalid Command")
                    else:
                        print("Invalid Command")
                case _ :
                    print("Invalid Command")
    except KeyboardInterrupt as e:
        print("type exit to exit the application")
    except Exception  as e:
        print(e)
        print("Invalid Command")
    
        

        