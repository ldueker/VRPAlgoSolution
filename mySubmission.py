import sys
import math


def total_drive_time(route, loads):
    totalTime = 0
    for i in range(len(route) - 1):
        pickupLocation = loads[route[i]][1]
        dropoffLocation = loads[route[i]][2]
        nextPickupLocation = loads[route[i + 1]][1]
        totalTime += euclideanDistance((0, 0), pickupLocation) + euclideanDistance(pickupLocation, dropoffLocation) + euclideanDistance(dropoffLocation, nextPickupLocation)
    return totalTime



def euclideanDistance(p1, p2):
    return math.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)

def optimizeRoutes(loads):
    numLoads = len(loads)
    savings = []
    for i in range(numLoads):
        for j in range(i + 1, numLoads):
            saving = total_drive_time([i, j], loads) - total_drive_time([i], loads) - total_drive_time([j], loads)
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
            mergedRoute = route1 + route2[::-1]
            if total_drive_time(mergedRoute, loads) <= 12 * 60:
                routes.remove(route1)
                routes.remove(route2)
                routes.append(mergedRoute)


    for i in range(len(routes)):
        current_route = routes[i]
        for j in range(1, len(current_route) - 1):
            test_route = current_route[:j] + current_route[j+1:]
            test_route.insert(j, current_route[j])
            if total_drive_time(test_route, loads) <= 12 * 60:
                routes[i] = test_route

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

