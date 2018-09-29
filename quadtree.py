# -*- coding: utf-8 -*-
"""
Created on Sun Sep 23 10:19:52 2018

@author: Proshore
"""
import numpy as np

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, plt):
        plt.scatter(self.x, self.y)


class Rectangle:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def contains(self, point):
        return point.x >= self.x and point.x < self.x + self.w and point.y >= self.y and point.y < self.y + self.h

    def intersects(self, rect):
        return abs(self.x - rect.x) < (self.w + rect.w) or abs(self.y - rect.y) < (self.y + rect.y)

    def draw(self, plt):
        x = self.x
        y = self.y
        w = self.w
        h = self.h
        plt.plot([x, x + w, x + w, x, x], [y, y, y + h, y + h, y])
        
class Circle:
    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.r = r

    def contains(self, point):
        return (point.x - self.x)**2 + (point.y - self.y)**2 <= self.r ** 2

    def draw(self, plt):
        x = self.x
        y = self.y
        w = self.w
        h = self.h
        plt.plot([x, x + w, x + w, x, x], [y, y, y + h, y + h, y])


class QuadTree:
    def __init__(self, boundary, capacity=4):
        self.boundary = boundary
        self.capacity = capacity
        self.points = []
        self.divided = False


    def subdivide(self):
        x = self.boundary.x
        y = self.boundary.y
        w = self.boundary.w
        h = self.boundary.h

        nw = Rectangle(x, y + h / 2, w / 2, h / 2)
        ne = Rectangle(x + w / 2, y + h / 2, w / 2, h / 2)
        sw = Rectangle(x, y, w / 2, h / 2)
        se = Rectangle(x + w / 2, y, w / 2, h / 2)

        self.nw = QuadTree(nw)
        self.ne = QuadTree(ne)
        self.sw = QuadTree(sw)
        self.se = QuadTree(se)

        self.divided = True

    def insert(self, point):
        #print('incoming '+str(point.__dict__)+' in '+str(self.boundary.__dict__)+' points cout = ' +str(len(self.points))+' capactiy = ' + str(self.capacity))

        if not self.boundary.contains(point):
            #print('False')
            return
        
       
        if len(self.points) < self.capacity:
            #print('inserted '+str(point.__dict__)+' in '+str(self.boundary.__dict__))
            self.points.append(point)
            return True
        else:
            if not self.divided:
                #print('sub divide is called')
                self.subdivide()
                
            return self.nw.insert(point) or self.ne.insert(point) or self.sw.insert(point) or self.se.insert(point)

    def getPointsFromPointInRadius(self,point,radius):
        pass
        

    def getAllBoundaries(self,boundaries):
        if not self.divided:
            boundaries.append(self.boundary)
            return
        
        self.nw.getAllBoundaries(boundaries)
        self.ne.getAllBoundaries(boundaries)
        self.sw.getAllBoundaries(boundaries)
        self.se.getAllBoundaries(boundaries)
        
        
    def query(self, range, found):      
        if not self.boundary.intersects(range):
            return
   
        for p in self.points:
            if range.contains(p):
                found.append(p)
     
        if self.divided:
            self.nw.query(range, found)
            self.ne.query(range, found)
            self.sw.query(range, found)
            self.se.query(range, found)
    

    def draw(self, plt):
        self.boundary.draw(plt)

        for point in self.points:
            point.draw(plt)

        if self.divided:
            self.nw.draw(plt)
            self.ne.draw(plt)
            self.sw.draw(plt)
            self.se.draw(plt)
