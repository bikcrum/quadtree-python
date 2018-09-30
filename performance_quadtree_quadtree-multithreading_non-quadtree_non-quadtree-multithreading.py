import numpy as np
import random

from quadtree import Rectangle, QuadTree, Point, Circle
from time import time

import matplotlib.pyplot as plt

from threading import Thread

width = 360
height = 180

no_of_points = 10000

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

# print(no_of_points,' points inserted in ',time()-start,' seconds')

found_mt = []


def asyncFindNeighbours(points_chunk, area, found_points):
    for point in points_chunk:
        if area.contains(point):
            found_points.append(point)


def multithreadingFindNeighbours(area):
    total_points = len(all_points)
    numberOfThread = 10
    perThreadPoints = total_points // numberOfThread
    points_chunks = [all_points[i:i + perThreadPoints] for i in
                     range(0, total_points, perThreadPoints)]
    threads = []
    found_points_list = [[]] * numberOfThread
    for i in range(numberOfThread):
        found_points_list[i] = []
        thread = Thread(target=asyncFindNeighbours, args=(points_chunks[i], area, found_points_list[i],))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    result_points = []
    for i in range(numberOfThread):
        for point in found_points_list[i]:
            result_points.append(point)

    return result_points


rects = []


def findNeighbours(x, y, w, h, algo='undefined'):
    area = Rectangle(x, y, w, h)

    found = []
    start = time()

    if algo == 'quadtree':
        qd.query(area, found)
    elif algo == 'quadtree_multithreading':
        qd.query_async(area, found)
    elif algo == 'multithreading':
        found = multithreadingFindNeighbours(area)
    else:
        for point in all_points:
            if area.contains(point):
                found.append(point)

    time_taken = time() - start
    print(('found %d points in %.20f seconds. Algorithm=%s') % (len(found), time_taken, algo))

    return time_taken


time_taken_multithreading = []
time_taken_quadtree = []
time_taken_quadtree_multithreading = []
time_taken_normal = []
indices = []
loops = 3


def main():
    for i in range(loops):
        w = random.randint(25, 101)
        h = random.randint(25, 101)
        x = random.randint(-180, -180 + width - w)
        y = random.randint(-90, -90 + height - h)

        time_taken = findNeighbours(x, y, w, h, algo='multithreading')
        time_taken_multithreading.append(time_taken)

        time_taken = findNeighbours(x, y, w, h, algo='quadtree')
        time_taken_quadtree.append(time_taken)

        time_taken = findNeighbours(x, y, w, h, algo='quadtree_multithreading')
        time_taken_quadtree_multithreading.append(time_taken)

        time_taken = findNeighbours(x, y, w, h)
        time_taken_normal.append(time_taken)
        indices.append(i)


main()
plt.plot(indices, time_taken_multithreading, color='green')
plt.plot(indices, time_taken_quadtree, color='red')
plt.plot(indices, time_taken_normal, color='blue')
plt.plot(indices, time_taken_quadtree_multithreading, color='black')
plt.xlabel('interations')
plt.ylabel('time taken (sec)')

# time_taken_multithreading_avg = sum(time_taken_multithreading) / len(time_taken_multithreading)
# time_taken_quadtree_avg = sum(time_taken_quadtree) / len(time_taken_quadtree)
# time_taken_normal_avg = sum(time_taken_normal) / len(time_taken_normal)
# plt.plot([0, 1], [time_taken_multithreading_avg, time_taken_multithreading_avg], color='green')
# plt.plot([0, 1], [time_taken_quadtree_avg, time_taken_quadtree_avg], color='red')
# plt.plot([0, 1], [time_taken_normal_avg, time_taken_normal_avg], color='blue')
# plt.xlabel('interations')
# plt.ylabel('time taken avg (sec)')

plt.show()
