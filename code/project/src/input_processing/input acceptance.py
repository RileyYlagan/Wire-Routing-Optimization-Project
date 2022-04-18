#Import Libraries
import numpy as np
import heapq
import pandas as pd
from collections import OrderedDict
import json
import ast


#Implementation of Class Structuring with xls Structuring

class wireClassDiagonal:
    def __init__(self,data,txtFile):
        self.xls = pd.ExcelFile(data)
        with open(txtFile) as json_file:
            self.node_dict = json.load(json_file)
        
    #Read in Data between sheets
    def processData(self):
        self.df1 = pd.read_excel(self.xls, 'Excel Input')
        self.df2 = pd.read_excel(self.xls, 'Adjacency Matrix')
        return self.df1,self.df2
    
    def heuristic(self,current, destination):
        return np.sqrt((destination[0] - current[0]) ** 2 + (destination[1] - current[1]) ** 2 + (destination[2] - current[2]) ** 2)

    def find_index_in_mesh(self,node_dict, current_node):
        values = list(node_dict.values())
        nodes = [x["node"] for x in values if x]
        mesh_index = nodes.index(current_node)
        return mesh_index

    def astar(self,start, goal):
        close_set = set() # closed list
        came_from = {} # parent node dict
        gscore = {start:0} # g-score dict
        fscore = {start:self.heuristic(start, goal)} #f score dict
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
            i = self.find_index_in_mesh(self.node_dict, current_node)
            neighbours = self.node_dict[str(i)]['neighbors'] #available_neighbours(current[0],current[1],current[2])

            if current == goal:
                data = []
                while current in came_from:
                    data.append(current)
                    current = came_from[current]
                return data
            close_set.add(current)
            for x, y, z in neighbours:
                neighbour = x, y, z

                r_max = 7
                Cost_r = 0

                if current in came_from: # avoid error since it doesn't store the start node
                    #print(current) # current
                    #print(came_from[current]) # previous
                    #print(neighbor) # possible next

                    # Calculate r_c, the current radius of curvature, using the Menger curvature eqn:
                    a = self.heuristic(current, came_from[current])
                    b = self.heuristic(current, neighbour)
                    c = self.heuristic(neighbour, came_from[current])
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

                tentative_g_score = gscore[current] + self.heuristic(current, neighbour) + Cost_r

                if neighbour in close_set and tentative_g_score >= gscore.get(neighbour, 0):
                    continue

                if tentative_g_score < gscore.get(neighbour, 0) or neighbour not in [i[1]for i in oheap]:
                    came_from[neighbour] = current
                    gscore[neighbour] = tentative_g_score
                    fscore[neighbour] = tentative_g_score + self.heuristic(neighbour, goal)
                    heapq.heappush(oheap, (fscore[neighbour], neighbour))

        return False
    
    def routeGenerator(self):
        for i in range(len(self.df1['Wire Number'])):
            #create a tuple of each wire's start/end points
            tupleStart = ast.literal_eval(self.df1['Start Point'][i])
            tupleEnd = ast.literal_eval(self.df1['End Point'][i])
            #call the astar function
            route = self.astar(tupleStart, tupleEnd)
            route = route + [tupleStart]
            route = route[::-1]
            #print the route with its associated wire number
            print('Optimized Route Wire: '+ str(self.df1['Wire Number'][i]))
            print(route)
            print(len(route))
            #STORE AS DICTIONARY key: wire number  value: a* route !!!        
              

#Instantiate Instance for Dataset
a = wireClassDiagonal('Wire Data Input.xlsx','node_dic_SF5_diagonals.txt')

#Process and Massage Data
a.processData()
#Utilize astar to find optimized wiring routes
a.routeGenerator()