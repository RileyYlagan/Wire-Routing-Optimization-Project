import sys
sys.path.append('../')
from src.input_processing import discretization as dz
import numpy as np
import pyvista as pv
from stl import mesh, main
import time

#import mesh and construct uniform grid
startTime = time.time()
my_mesh = mesh.Mesh.from_file('../../../data/first_iteration.STL')
SF = 5
grid = dz.construct_uniform_grid(my_mesh,SF)
# extract triangles and points
triangles,grid_points = dz.get_triangles_and_points(my_mesh,grid)
outside_points = dz.find_valid_points(triangles,grid_points)

node_dic = dz.all_node_neighbors(outside_points,grid_points)
print(node_dic)

executionTime = (time.time() - startTime)
print('Execution time in seconds: ' + str(executionTime))