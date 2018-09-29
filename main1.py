import matplotlib.pyplot as plt
import numpy as np
import random

from quadtree import Rectangle, QuadTree, Point, Circle
from time import time

fig,ax = plt.subplots()

width = 360
height = 180

no_of_points = 1000

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
    print('point ',i,' inserted in ',time()-t,' seconds')
    all_points.append(point)
    
print(no_of_points,' points inserted in ',time()-start,' seconds')
    
rects = []
def findNeighbours(x,y,w,h,algo='quadtree'):
    area = Rectangle(x,y,w,h)
    rect = plt.Rectangle((area.x, area.y), area.w, area.h, color='black', linewidth='3',fill=False)
    for r in rects:
        r.remove()
    rects.clear()
    rects.append(rect)
    ax.add_patch(rect)
        
    
    found = []
    start = time()
    
    if algo == 'quadtree':
        qd.query(area,found)
    else:
        for point in all_points:
            if area.contains(point):
                found.append(point)
    
    print(('found %d points in %.20f seconds') % (len(found),time()-start))
    qd.draw(plt)

    for point in found:
        plt.scatter(point.x,point.y,color='black')
 
w = random.randint(25,101)
h = random.randint(25,101)
x = random.randint(-180,-180+width-w)
y = random.randint(-90,-90+height-h)
findNeighbours(x,y,w,h)

def onclick(event):
    w = random.randint(25,101)
    h = random.randint(25,101)
    findNeighbours(event.xdata,event.ydata,w,h)
    fig.canvas.draw()

fig.canvas.mpl_connect('button_press_event', onclick)
    
plt.show()

