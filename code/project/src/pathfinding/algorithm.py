##############################################################################

# import packages

##############################################################################

import numpy as np
import heapq
import pandas as pd
import os
from collections import OrderedDict
import json

##############################################################################

# coordinate pairs

##############################################################################

print('current:'+ os.getcwd())
with open('test_dictionary_for_SF5.json', 'r') as read_file:
    node_dict = json.load(read_file)

##############################################################################

# specify start and goal positions

##############################################################################

start = tuple(node_dict['11']['node']) #(1,1,1)
goal = tuple(node_dict['89']['node']) #(3,3,3)
print('start:')
print(start)
print('end:')
print(goal)

##############################################################################

# a* path finding functions

##############################################################################

def heuristic(current, destination):
    return np.sqrt((destination[0] - current[0]) ** 2 + (destination[1] - current[1]) ** 2 + (destination[2] - current[2]) ** 2)

def find_index_in_mesh(node_dict, current_node):
    values = list(node_dict.values())
    nodes = [x["node"] for x in values if x]
    mesh_index = nodes.index(current_node)
    return mesh_index

def astar(start, goal):
    close_set = set() # closed list
    came_from = {} # parent node dict
    gscore = {start:0} # g-score dict
    fscore = {start:heuristic(start, goal)} #f score dict
    oheap = [] #open list
    #print('fscore:')
    #print(fscore)
    heapq.heappush(oheap, (fscore[start], start)) # put start node into open list
    #print(oheap)
    #iter = 0
    while oheap:
        #iter += 1
        #print(iter)
        current = heapq.heappop(oheap)[1]
        current_node = [current[0],current[1],current[2]]
        i = find_index_in_mesh(node_dict, current_node)
        neighbours = node_dict[str(i)]['neighbors'] #available_neighbours(current[0],current[1],current[2])

        if current == goal:
            data = []
            while current in came_from:
                data.append(current)
                current = came_from[current]
            return data
        close_set.add(current)
        for x, y, z in neighbours:
            neighbour = x, y, z
            tentative_g_score = gscore[current] + heuristic(current, neighbour)

            if neighbour in close_set and tentative_g_score >= gscore.get(neighbour, 0):
                continue

            if tentative_g_score < gscore.get(neighbour, 0) or neighbour not in [i[1]for i in oheap]:
                came_from[neighbour] = current
                gscore[neighbour] = tentative_g_score
                fscore[neighbour] = tentative_g_score + heuristic(neighbour, goal)
                heapq.heappush(oheap, (fscore[neighbour], neighbour))

    return False

##############################################################################

# calculate route

##############################################################################

route = astar(start, goal)
route = route + [start]
route = route[::-1]
print('route:')
print(route)

a_file = open("test_astar.xyz","w")
for row in route:
    np.savetxt(a_file, [row])
a_file.close()

##############################################################################

# visualise the path

##############################################################################



import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt


#extract x and y coordinates from route list
x_coords = []
y_coords = []
z_coords = []


for i in (range(0,len(route))):
    x = route[i][0]
    y = route[i][1]
    z = route[i][2]

    x_coords.append(x)
    y_coords.append(y)
    z_coords.append(z)

x_coords = np.array(x_coords)
y_coords = np.array(y_coords)
z_coords = np.array(z_coords)


