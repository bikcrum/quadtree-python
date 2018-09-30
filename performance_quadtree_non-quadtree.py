import numpy as np
import random

from quadtree import Rectangle, QuadTree, Point, Circle
from time import time

import matplotlib.pyplot as plt

width = 360
height = 180

no_of_points = 100000

boundary = Rectangle(-180, -90, width, height)

qd = QuadTree(boundary)

all_points = []
start = time()
for i in range(0, no_of_points):
    lng = random.randint(-180, width + 1)
    lat = random.randint(-90, height + 1)
    point = Point(lng, lat)
    t = time()
    qd.insert(point)
   # print('point ',i,' inserted in ',time()-t,' seconds')
    all_points.append(point)
    
#print(no_of_points,' points inserted in ',time()-start,' seconds')
    
rects = []
def findNeighbours(x,y,w,h,algo='undefined'):
    area = Rectangle(x,y,w,h)
    
    found = []
    start = time()
    
    if algo == 'quadtree':
        qd.query(area,found)
    else:
        for point in all_points:
            if area.contains(point):
                found.append(point)
    
    time_taken = time() - start
    print(('found %d points in %.20f seconds') % (len(found),time_taken))
    
    return time_taken
 
time_taken_quadtree = []
time_taken_normal = []
indices = []
loops = 100
def main():
    for i in range(loops):         
        w = random.randint(25,101)
        h = random.randint(25,101)
        x = random.randint(-180,-180+width-w)
        y = random.randint(-90,-90+height-h)
        time_taken = findNeighbours(x,y,w,h,algo='quadtree')
        time_taken_quadtree.append(time_taken)
        time_taken = findNeighbours(x,y,w,h)
        time_taken_normal.append(time_taken)
        indices.append(i)
 
main()
plt.plot(indices,time_taken_quadtree,color='red',label='quadtree')
plt.plot(indices,time_taken_normal,color='blue',label='non-quadtree')

plt.show()        
    
        

