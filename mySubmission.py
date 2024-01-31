import sys
import math

def euclidean_distance(point1, point2):
    return math.sqrt((point2[0] - point1[0]) ** 2 + (point2[1] - point1[1]) ** 2)

def total_drive_time(route, loads):
    total_time = 0
    for i in range(len(route) - 1):
        pickup_loc = loads[route[i]][1]
        dropoff_loc = loads[route[i]][2]
        next_pickup_loc = loads[route[i + 1]][1]
        total_time += euclidean_distance((0, 0), pickup_loc) + euclidean_distance(pickup_loc, dropoff_loc) + euclidean_distance(dropoff_loc, next_pickup_loc)
    return total_time

def clarke_wright_savings(loads):
    n = len(loads)
    savings = []

    for i in range(n):
        for j in range(i + 1, n):
            saving = total_drive_time([i, j], loads) - total_drive_time([i], loads) - total_drive_time([j], loads)
            savings.append((i, j, saving))

    savings.sort(key=lambda x: x[2], reverse=True)

    routes = [[i] for i in range(n)]
    
    #Comparing routes to see if routes can be combined
    for i, j, saving in savings:
        route_i = next((r for r in routes if i in r), None)
        route_j = next((r for r in routes if j in r), None)

        #Combine Routes if Possible
        if route_i and route_j and route_i != route_j:
            merged_route = route_i + route_j[::-1]
            if total_drive_time(merged_route, loads) <= 12 * 60:
                routes.remove(route_i)
                routes.remove(route_j)
                routes.append(merged_route)

    return routes

def print_solution(routes):
    for route in routes:
        print(route)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python mySubmission.py {path_to_problem}")
        sys.exit(1)

    path_to_problem = sys.argv[1]

    with open(path_to_problem, "r") as file:
        file.readline()
        loads = []
        for line in file:
            parts = line.split()
            load_number = int(parts[0])
            pickup_loc = tuple(map(float, parts[1][1:-1].split(',')))
            dropoff_loc = tuple(map(float, parts[2][1:-1].split(',')))
            loads.append((load_number, pickup_loc, dropoff_loc))

    routes = clarke_wright_savings(loads)
    print_solution(routes)
