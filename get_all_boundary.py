import matplotlib.pyplot as plt
import numpy as np
import random

from quadtree import Rectangle, QuadTree, Point

width = 500
height = 500

no_of_points = 300

boundary = Rectangle(0, 0, width, height)

qd = QuadTree(boundary)

for i in range(0, no_of_points):
    x = random.randint(0, width + 1)
    y = random.randint(0, height + 1)
    point = Point(x, y)
    qd.insert(point)

b = []
qd.getAllBoundaries(boundaries=b)
print(b)
qd.draw(plt)
plt.show()