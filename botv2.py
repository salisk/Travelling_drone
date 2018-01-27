#   _____                    _ _ _               ____        _               _                        ____            _     _
#  |_   _| __ __ ___   _____| | (_)_ __   __ _  / ___|  __ _| | ___  ___  __| |_ __ ___  _ __   ___  |  _ \ _ __ ___ | |__ | | ___ _ __ ___
#    | || '__/ _` \ \ / / _ \ | | | '_ \ / _` | \___ \ / _` | |/ _ \/ __|/ _` | '__/ _ \| '_ \ / _ \ | |_) | '__/ _ \| '_ \| |/ _ \ '_ ` _ \
#    | || | | (_| |\ V /  __/ | | | | | | (_| |  ___) | (_| | |  __/\__ \ (_| | | | (_) | | | |  __/ |  __/| | | (_) | |_) | |  __/ | | | | |
#    |_||_|  \__,_| \_/ \___|_|_|_|_| |_|\__, | |____/ \__,_|_|\___||___/\__,_|_|  \___/|_| |_|\___| |_|   |_|  \___/|_.__/|_|\___|_| |_| |_|
#                                        |___/
botName='UOMSarunas-botv2'

import json
from random import randint, choice, shuffle
from math import hypot

# These are the only additional libraries available to you. Uncomment them
# to use them in your solution.
#
#import numpy    # Base N-dimensional array package
#import pandas   # Data structures & analysis


# =============================================================================
# This calculateMove() function is where you need to write your code. When it
# is first loaded, it will play a complete game for you.
#
def calculateMove(gameState):

    # remember data between moves using persistentData
    if "moveCount" not in persistentData:
      	persistentData["moveCount"] = 0
      	print(gameState)
    else:
      	persistentData["moveCount"] += 1

    # if "best_oder" not in persistentData:
    # Produces a list of all the city indexes
    a = [i for i in range(len(gameState["CityCoords"]))]

    # Randomly orders the list of cities
    #shuffle(a)
    #print(a)
    b = []
    current = a[0]
    b.append(current)
    a.remove(current)
    for i in range(len(gameState["CityCoords"]) - 1):
            current = find_closest_city(gameState["CityCoords"], current, a)
            b.append(current)
            a.remove(current)
    best_order = b
    #print(best_order)
    best_distance = route_distance(b, gameState)
        # persistentData["i"] = 0
        # persistentData["j"] = 0
    # else:
    #     best_order = persistentData["best_order"]
    #     best_distance = persistentData["best_distance"]

    improve = True

    # While route distance improves
    while improve:
        improve = False
        for i in range(len(best_order) - 1):
            #i + persistentData["i"]
            for j in range(i + 1, len(best_order)):
                #j + persistentData["j"]
                new_order = swap_paths(best_order, i, j)
                new_distance = route_distance(new_order, gameState)
                if new_distance < best_distance:
                    # persistentData["best_order"] = new_order
                    # persistentData["best_distance"] = new_distance
                    best_order = new_order
                    best_distance = new_distance
                    improve = True
                    break
            if improve:
                break
        # persistentData["best_order"] = best_order
        # persistentData["best_distance"] = best_distance
        # persistentData["i"] = i
        # persistentData["j"] = j
        # return {"Path":best_order}

    # print("Random distance: " + str(route_distance(a, gameState)))
    #print("Sorted distance: " + str(best_distance))

    # Sets move to be the random order of cities
    #move = {"Path":a}
    move = {"Path":best_order}
    print("Move: " + str(persistentData["moveCount"]) + " " + str(move))
    return move

# Swap the paths
def swap_paths(route, i, j):
    new_route = list(route)
    # print("----------------")
    # print(new_route)
    # print(new_route[i : j + 1])
    # print(route[i : j+ 1][::-1])
    # print("----------------")
    new_route[i : j + 1] = route[i : j+ 1][::-1]
    # if len(route) != len(new_route):
    #     print("SWAP_PATHS ERROR!")
    return new_route

# Get the full distance of the route
def route_distance(route, gameState):
    distance = 0
    previous = route[-1]
    for city in route:
        distance += get_distance(gameState["CityCoords"][city], gameState["CityCoords"][previous])
        previous = city
    return distance
# =============================================================================
# These functions are helper functions that show you examples of how to
# manipulate the gameState data you receive.

# Given two city coordinates of the form [x, y]
# returns the distance between them
#
def get_distance(origin, destination):
    distance = hypot(abs(origin[0]-destination[0]), abs(origin[1]-destination[1]))
    return distance


# Given the list of city coordinates, the current city index, and
# a list of available cities indexes to choose from
# calculates the closest city (from the list of available cities)
# to the current city and returns it.
# Ex: find_closest_city(gamestate["CityCoords"],0,[1,2,3,4,5,6,7,8,9])
#
def find_closest_city(coords, cur_city, available_cities):

    # initialise closest city so far to the first city in the list
    closest_city = available_cities[0]

    # Initialise the distance to the closest city as the distance to the first city in the list
    closest_distance = get_distance(coords[cur_city], coords[closest_city])

    # For all remaining cities
    for next_city in available_cities[1:]:
        # Calculate the distance to it from our current city
        next_distance = get_distance(coords[cur_city], coords[next_city])
        # If this distance is our new shortest
        if next_distance < closest_distance:
            # Update closest_distance
            closest_distance = next_distance
            # Update closest_city
            closest_city = next_city

    # Return the closest city we found
    return closest_city
