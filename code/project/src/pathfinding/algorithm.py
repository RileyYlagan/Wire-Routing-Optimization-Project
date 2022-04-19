##############################################################################

# import packages

##############################################################################

import numpy as np
import heapq
import pandas as pd
from collections import OrderedDict
import json
import sys
import pyvista as pv

##############################################################################

# coordinate pairs

##############################################################################

#with open('test_dictionary_for_SF2.txt', 'r') as read_file:
 #   node_dict = json.load(read_file)

##############################################################################

# specify start and goal positions

##############################################################################
# Hard Coded for testing purposes for now
def start_and_end(node_dict,p1,p2):
    # Hard code nodes for sake of testing
    start = tuple(node_dict[p1]['node']) # first node
    goal = tuple(node_dict[p2]['node']) # last node
    return start, goal

##############################################################################

# a* path finding functions

##############################################################################

def test():
    print("Hello, Riley")

def heuristic(current, destination):
    return np.sqrt((destination[0] - current[0]) ** 2 + (destination[1] - current[1]) ** 2 + (destination[2] - current[2]) ** 2)

def find_index_in_mesh(node_dict, current_node):
    values = list(node_dict.values())
    nodes = [x["node"] for x in values if x]
    mesh_index = nodes.index(current_node)
    return mesh_index

def astar(start, goal, node_dict):
    close_set = set() # closed list
    came_from = {} # parent node dict
    gscore = {start:0} # g-score dict
    fscore = {start:heuristic(start, goal)} #f score dict
    oheap = [] #open list
    heapq.heappush(oheap, (fscore[start], start)) # put start node into open list
    while oheap:
        current = heapq.heappop(oheap)[1]
        current_node = [current[0],current[1],current[2]]
        i = find_index_in_mesh(node_dict, current_node)
        neighbours = node_dict[i]['neighbors'] #available_neighbours(current[0],current[1],current[2])

        if current == goal:
            data = []
            route_score = 0
            while current in came_from:
                data.append(current)
                current = came_from[current]
            data = data + [start]
            data = data[::-1]
            #for node in data:
                #route_score = route_score fscore[node]
            return data#, route_score

        close_set.add(current)
        for x, y, z in neighbours:
            neighbour = x, y, z

            r_max = 7 # 3.5355339059327378
            Cost_r = 0

            if current in came_from: # avoid error since it doesn't store the start node
                #print(current) # current
                #print(came_from[current]) # previous
                #print(neighbor) # possible next

                # Calculate r_c, the current radius of curvature, using the Menger curvature eqn:
                a = heuristic(current, came_from[current])
                b = heuristic(current, neighbour)
                c = heuristic(neighbour, came_from[current])
                p = 0.5 * (a + b + c) # half the perimeter
                # Using heron's formula for area of a triangle
                area = np.sqrt(p*(p-a)*(p-b)*(p-c))
                r_c = 0 # stays 0 if the line is straight (not curving at all across the 3 points)
                if area != 0:
                    r_c = (a*b*c)/(4*area)

                #print(r_c)

                Cost_r = r_c - r_max # Cost function for curvature constraint

                if Cost_r < 0: # if current radius is less than the max radius, don't add any cost
                    Cost_r = 0

            tentative_g_score = gscore[current] + heuristic(current, neighbour) + Cost_r

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

def global_optimization():

    
    return 0

# Functionize this
def get_route(start,goal,node_dict):
    route = astar(start, goal,node_dict)

    # Writes to file
    #a_file = open("test_astar.xyz","w")
    #for row in route:
    #    np.savetxt(a_file, [row])
    #a_file.close()
    return route

##############################################################################

# visualise the path

##############################################################################

def save_path_to_STL(route,filename):
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
    # Plot path as STL
    points = np.column_stack((x_coords, y_coords, z_coords))

    spline = pv.Spline(points, 500).tube(radius=0.05)
    file = filename+".stl"
    spline.save(file)

def get_spline(route):
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
    # Plot path as STL
    points = np.column_stack((x_coords, y_coords, z_coords))

    spline = pv.Spline(points, 500).tube(radius=0.1)
    return spline

def save_path_to_STL_poly(route,filename):
    poly = pv.PolyData()
    poly.points = route
    the_cell = np.arange(0, len(route), dtype=np.int_)
    the_cell = np.insert(the_cell, 0, len(route))
    poly.lines = the_cell
    poly["scalars"] = np.arange(poly.n_points)
    tube = poly.tube(radius=0.1)
    file = filename+".stl"
    tube.save(file)

def combine_route_and_mesh(meshes,filename):
    # Here meshes is an array of the original input mesh and all of the wire meshes
    merged = pv.PolyData()
    for mesh in meshes:
        merged += mesh
    file = filename+".stl"
    merged.save(file)