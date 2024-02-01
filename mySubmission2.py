import sys
import math

def euclideanDistance(point1, point2):
    return math.sqrt((point2[0] - point1[0])**2 + (point2[1] - point1[1])**2)

def greedySolve(loads):
    drivers = []
    while loads:
        currentDriver = []
        currentTime = 0
        for load in loads:
            #Calculate time to drive
            pickupTime = euclideanDistance((0, 0), load[1])
            dropoffTime = euclideanDistance(load[1], load[2])
            toDepot = euclideanDistance(load[2],(0,0))
            #check that current route is less than 12 hours (given he needs to drive back to depot to end the shift)
            if currentTime + pickupTime + dropoffTime + toDepot <= 720:
                #Append load number
                currentDriver.append(load[0])
                #Add to total time for driver
                currentTime += pickupTime + dropoffTime
                #remove load from next list of possible loads
                loads.remove(load)
        #create another schedule
        drivers.append(currentDriver)

    return drivers

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python mySubmission.py {path_to_problem}")
        sys.exit(1)

    path_to_problem = sys.argv[1]
    with open(path_to_problem, "r") as file:
        #skip first line
        file.readline()
        loads = []
        for line in file:
            #splits each line into info columns
            column = line.split()
            #column1 is loadNumber, column2 is the point of pickup, and column3 is point of dropoff
            loadNum = int(column[0])
            pickupLocation = tuple(map(float, column[1][1:-1].split(',')))
            dropoffLocation = tuple(map(float, column[2][1:-1].split(',')))
            #create loads object from info
            loads.append((loadNum, pickupLocation, dropoffLocation))
    
    solution = greedySolve(loads)
    for driver_route in solution:
        print(driver_route)
