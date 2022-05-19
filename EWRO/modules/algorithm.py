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
from itertools import permutations
import math
import time
import logging


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
    start = tuple(node_dict[0]['node']) # first node
    goal = tuple(node_dict[len(node_dict)-1]['node']) # last node
    return start, goal

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

# local optimization
def lastar(start, goal, node_dict, r_max, separation_dists, prev_routes):
    # NB: ADD: this function must take in as a parameter a list of the previous routes
    # prev_routes is a dictionary:
    #{
    # 'a':{route}
    # 'b':{route}
    #   .....
    # }
    # separation is similar
    # {
    # 'a':{'b':x}
    # 'b':{'a':x}
    #    .....
    # }
    # Get the closest points to start and goal 
    start_mesh = tuple(closest_node(start,node_dict))
    goal_mesh = tuple(closest_node(goal,node_dict))
    close_set = set() # closed list
    came_from = {} # parent node dict
    gscore = {start_mesh:0} # g-score dict
    fscore = {start_mesh:heuristic(start_mesh, goal_mesh)} #f score dict
    oheap = [] #open list
    heapq.heappush(oheap, (fscore[start_mesh], start_mesh)) # put start node into open list
    while oheap:
        current = heapq.heappop(oheap)[1]
        current_node = [current[0],current[1],current[2]]
        i = find_index_in_mesh(node_dict, current_node)
        neighbours = node_dict[i]['neighbors'] #available_neighbours(current[0],current[1],current[2])

        if current == goal_mesh:
            data = []
            route_score = 0
            while current in came_from:
                data.append(current)
                current = came_from[current]
            
            data = data + [start_mesh]
            data = data[::-1]
            for node in data:
                route_score = route_score+fscore[node]
            return data , route_score

        close_set.add(current)
        for x, y, z in neighbours:
            neighbour = x, y, z
            Cost_r = 0
            Cost_sep = 0
            if current in came_from: # avoid error since it doesn't store the start node
                ### Separation Distance Cost Calculation
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

                Cost_r = r_c - r_max # Cost function for curvature constraint

                if Cost_r < 0: # if current radius is less than the max radius, don't add any cost
                    Cost_r = 0
                ### Separation Distance Cost Calculation
                if len(prev_routes) > 0:
                    Cost_sep = calc_sep_cost(current,prev_routes,separation_dists)

            tentative_g_score = gscore[current] + heuristic(current, neighbour) + Cost_r + Cost_sep

            if neighbour in close_set and tentative_g_score >= gscore.get(neighbour, 0):
                continue

            if tentative_g_score < gscore.get(neighbour, 0) or neighbour not in [i[1]for i in oheap]:
                came_from[neighbour] = current
                gscore[neighbour] = tentative_g_score
                fscore[neighbour] = tentative_g_score + heuristic(neighbour, goal_mesh)
                heapq.heappush(oheap, (fscore[neighbour], neighbour))

    return False

def gastar(wire_dict,node_dict): # global aka bi-level optimization
    # wires = [a,b,c] # list of all wire objects (in this case: a,b,c), each holding wire-specific info 
    # Wires is a dictionary of wire info:
    # Wire dictionary layout:
    # {name:{start, goal, max_curvature, separations},.....}
    # For every number of wires
    # prev_routes is a dictionary:
    #{
    # 'a':{route}
    # 'b':{route}
    #   .....
    # }
    # separation is similar
    # {
    # 'a':{'b':x}
    # 'b':{'a':x}
    #    .....
    # }
    wires_names = list(wire_dict.keys())
    perms = list(permutations(wires_names,len(wires_names)))

    all_possible = {} # holds permutation, fscore, routes of each wire for the permutation
    for permutation in perms:
        perm_fscore = 0
        all_routes = {}
        permutation_dict = {}
        prev_routes = {}
        for wire in permutation:
            route, fscore = lastar(wire_dict[wire]["start"], wire_dict[wire]["goal"],node_dict, wire_dict[wire]["max_curvature"], wire_dict[wire]["separations"], prev_routes) # FIX!!!
            perm_fscore += fscore
            all_routes[wire] = route
            prev_routes[wire] = route

        permutation_dict['fscore'] = perm_fscore
        permutation_dict['routes'] = all_routes
        all_possible[permutation] = permutation_dict 

    fscores = []
    for perm in list(all_possible.values()):
        fscores.append(perm['fscore']) # return list of fscores
    min_score_index = fscores.index(min(fscores))
    best_perm = all_possible[list(all_possible.keys())[min_score_index]]
    # Now, find the min_fscores's corresponding the permutation and list of routes.
    # then, return the permutation!

    return best_perm # return the correct permutation

def calc_sep_cost(p, prev_routes, separation_dict): 
    # A is a neighbor or a point
    # B is the route other wires
    # sep is the minimum separation between the wire that point A is one and the wire point B
    Cost_sep = 0
    for route_name in prev_routes:
        current_sep = separation_dict[route_name]
        for i in range(len(prev_routes[route_name])):
            current_node = prev_routes[route_name][i] # current node on current previous route
            distance_squared = ((p[0]-current_node[0])**2)+((p[1]-current_node[1])**2)+((p[2]-current_node[2])**2)
            distance = math.sqrt(distance_squared)
            if distance < current_sep:
                Cost_sep += current_sep - distance
  
    return 10*Cost_sep #returns cost associated with the input point and its separation from the previously routed routes

def closest_node(p,node_dict):
    nodes = []
    nodes_list=list(node_dict.values())
    for node in nodes_list:
        nodes.append(node["node"])
    dists = []
    for node in nodes:
        distance_squared = ((p[0]-node[0])**2)+((p[1]-node[1])**2)+((p[2]-node[2])**2)
        distance = math.sqrt(distance_squared)
        dists.append(distance)
    
    point_index = dists.index(min(dists))
    closest_node = node_dict[point_index]["node"]
    return closest_node #index of closest point in node dictionary

##############################################################################

# calculate route

##############################################################################

# Functionize this
def get_route(start,goal,node_dict):
    route = lastar(start, goal,node_dict,r_max)
    return route

## GET ROUTES
def main(wire_dict,node_dict,filename):
    logging.info("Finding Optimal Route...")
    route_time = time.time()
    best_perm = gastar(wire_dict,node_dict)
    routes = best_perm['routes']
    executionTime = (time.time() - route_time)
    logging.info('Finished in ' + str(executionTime) + ' seconds')
    for route_name in routes:
        save_path_to_STL(routes[route_name],filename+'_'+route_name,filename)
    
    for route in routes:
        spline, length = get_spline(routes[route])
        logging.info("Length of wire "+route+" is " +str(length))
    logging.info("Done")

##############################################################################

# visualise the path

##############################################################################

def save_path_to_STL(route,filename,dirname):
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

    spline = pv.Spline(points, 500).tube(radius=0.15)
    file = "output/"+dirname+"/"+filename+".stl"
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

    spline = pv.Spline(points, 500)
    length = spline.compute_arc_length()['arc_length'][-1]
    spline = spline.tube(radius=0.05)
    return spline, length

def get_spline_length(spline):
    length = spline.compute_arc_length()['arc_length'][-1]
    return length

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