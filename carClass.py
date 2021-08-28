'''
CAR.py - contains the car class used for storing
         information about each car, and their methods
         for movement.
'''

# IMPORTS
import random as rd

# BODY
class car:
    '''
    "car" is an class which sits on the "sites" of the road and with
    properties of speed, maxspeed, probability of not accelerating (p)
    for a size 200 road
    '''
    
    def __init__(self, v, vMax, site):
        # object constructor
        
        self.v = v
        self.vMax = vMax
        self.site = site
        self.passedSites = []
        
        self.p = 0
        self.L = 500

    def accel(self):
        # increase v by 1, if not at max speed already

        if self.v < self.vMax:
            self.v = self.v + 1
        return
    
    def newSite(self):
        # move car v sits ahead
        
        self.site = self.v + self.site
        return
        
    def circleCondition(self):
        # changes car site positions to match a site within
        # the road length L

        if self.site >= self.L: 
            self.site = self.site - self.L
        if self.site < 0:
            self.site = self.site + self.L
        return
            
    def randomSlow(self):
        # will reduce v by 1, with probability p
        
        if self.v > 0:
            if rd.random() < self.p: #p value
                self.v = self.v - 1
        return
    
    def prevSites(self, theSite):
        #store all sites that each car object has passed (expensive)
        self.passedSites.append(theSite)