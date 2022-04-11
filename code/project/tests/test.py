import sys
sys.path.append('../')
from src.input_processing import discretization as dz
from src.pathfinding import algorithm as alg
import numpy as np
import pyvista as pv
from stl import mesh, main
import time
import random


startTime = time.time()
## All of Discretization
#import mesh and construct uniform grid
# This is the ordering for discretization
# STL name and SF will become user input
print("Gathering Input...")
input_time = time.time()
input_file = '../../../data/first_iteration.STL'
my_mesh = mesh.Mesh.from_file(input_file)
SF = 2
grid = dz.construct_uniform_grid(my_mesh,SF)
executionTime = (time.time() - input_time)
print('Finished in ' + str(executionTime) + ' seconds')

# extract triangles and points
print("Finding Valid Points...")
valid_points_time = time.time()
triangles,grid_points = dz.get_triangles_and_points(my_mesh,grid)
outside_points = dz.find_valid_points(triangles,grid_points)
node_dic = dz.all_node_neighbors(outside_points,grid_points)
executionTime = (time.time() - valid_points_time)
print('Finished in ' + str(executionTime) + ' seconds')
### Here is where Vincent's code with input acceptance comes in
## For sake of testing I will hard code start and end points
## Need to also create find_nearest_node thing
print("Finding Optimal Route...")
route_time = time.time()

num_wires = 3
meshes = []
poly_mesh = pv.PolyData(input_file)
meshes.append(poly_mesh)
#generate random start and end
for i in range(num_wires):
    p1 = random.randint(0,len(node_dic)-1)
    p2 = random.randint(0,len(node_dic)-1)
    start, goal = alg.start_and_end(node_dic,p1,p2)
    route = alg.get_route(start,goal,node_dic)
    spline = alg.get_spline(route)
    meshes.append(spline)

#Combine STL files together

alg.combine_route_and_mesh(meshes,"combined_test")

executionTime = (time.time() - route_time)
print('Finished in ' + str(executionTime) + ' seconds')


executionTime = (time.time() - startTime)
print('Execution time in seconds: ' + str(executionTime))