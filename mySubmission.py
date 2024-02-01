import sys
import math


def totalDriveTime(route, loads):
    totalTime = 0
    for i in range(len(route) - 1):
        pickupLocation = loads[route[i]][1]
        dropoffLocation = loads[route[i]][2]
        nextPickupLocation = loads[route[i + 1]][1]
        #Calculate total time for both of the loa
        totalTime += euclideanDistance((0, 0), pickupLocation) + euclideanDistance(pickupLocation, dropoffLocation) + euclideanDistance(dropoffLocation, nextPickupLocation)
    return totalTime

#Calculates number of minutes to drive between two given points
def euclideanDistance(p1, p2):
    return math.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)

def optimizeRoutes(loads):
    numLoads = len(loads)
    savings = []
    for i in range(numLoads):
        for j in range(i + 1, numLoads):
            #creating route-savings groupings
            saving = totalDriveTime([i, j], loads) - totalDriveTime([i], loads) - totalDriveTime([j], loads)
            savings.append((i, j, saving))
    
    #Sorting my routes
    savings.sort(key=lambda x: x[2], reverse=True)
    
    #constructing route number
    routes = [[i] for i in range(numLoads)]
    
    #Comparing routes to see if routes can be combined
    for i, j, saving in savings:
        route1 = next((r for r in routes if i in r), None)
        route2 = next((r for r in routes if j in r), None)

        #Combine Routes if Possible
        if route1 and route2 and route1 != route2:
            #Create merged route
            mergedRoute = route1 + route2[::-1]
            #Add merged route to schedule if time to drive
            if totalDriveTime(mergedRoute, loads) <= 12 * 60:
                routes.remove(route1)
                routes.remove(route2)
                routes.append(mergedRoute)

    return routes


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python mySubmission.py {path_to_problem}")
        sys.exit(1)

    path_to_problem = sys.argv[1]

    with open(path_to_problem, "r") as file:
        file.readline()
        loads = []
        for line in file:
            column = line.split()
            loadNum = int(column[0])
            pickupLocation = tuple(map(float, column[1][1:-1].split(',')))
            dropoffLocation = tuple(map(float, column[2][1:-1].split(',')))
            loads.append((loadNum, pickupLocation, dropoffLocation))

    routes = optimizeRoutes(loads)
    routes = [[n+1 for n in sub] for sub in routes]
    for route in routes:
        print(route)



