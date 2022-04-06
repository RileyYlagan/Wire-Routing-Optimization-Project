#BASIC CODE FOR PERPENDICULAR DISTANCES - FROM A SET OF POINTS

import math

def per_dist(A, B): #takes sets of points A and B
    C = []
    if len(A)==len(B):
        for i in range(len(A)):
            distance_squared = ((A[i][0]-B[i][0])**2)+((A[i][1]-B[i][1])**2)+((A[i][2]-B[i][2])**2)
            distance = math.sqrt(distance_squared)
            C.append(distance)
        return C #returns a list of distances, indexed correspondingly
    else:
        print('error - missing values')

#DRIVER CODE

#A = [[2,4,6],[8,10,2],[4,6,8]] #set 1
#B = [[1,3,5],[7,9,11],[1,3,5]] #set 2
#Dist = per_dist(A,B)
#print(Dist)
