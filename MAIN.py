'''
MAIN.py - control file that creates car objects, and 
          initiates timesteps within the road system
'''

# IMPORTS
from carClass import car
import numpy as np
import random as rd
import copy

# VARIABLES
roadLength = 500  # currently has to be changed in the class too!

# BODY


def genCars(N, random = True):
    # function returns a list of N cars with random
    # positions (between 1,200) sorted in ascending order
    # if random is false, then cars will be evenly distributed
    
    carMaxSpeed = 5
    carSpeed = 5
    
    if random == True:
        pos = []
        out = []
        while len(pos) < N:
            num = rd.randint(0,roadLength - 1)
            if num not in pos:
                pos.append(num)
        pos = sorted(pos)
        for j in pos:
            out.append(car(carSpeed, carMaxSpeed, j)) #(v, vMax, site#)
        return out
    else:
        out = []
        pos = np.linspace(0, roadLength - 1, N).astype(int)
        for j in pos:
            out.append(car(carSpeed,carMaxSpeed,j))
        return out
        
def oneTimeStep(listOfCars):
    # function takes a list of cars, and will apply
    # the four rules. No need to return, cars cant
    # overtake in this model currently
    
    # Rule 1
    for obj in listOfCars:
        obj.accel()
        
    #Rule 2
    c = 1
    for obj in listOfCars:
        nextCar = listOfCars[c]
        
        if obj.site > nextCar.site:
            lengthCondition = roadLength
        else:
            lengthCondition = 0
            
        dist = nextCar.site - obj.site + lengthCondition
        
        if obj.v >= dist:
            obj.v = dist  - 1
            
        c = c + 1
        if c == len(listOfCars):
            c = 0
        
    # Rule 3    
    for obj in listOfCars:
        obj.randomSlow() 
        
    # Rule 4   
    for obj in listOfCars:
        obj.newSite()
        
        obj.circleCondition()
        
    # Prepare flow data
    for obj in listOfCars:

        for i in range(1, obj.v + 1):
            if obj.site - i > 0:
                obj.prevSites(obj.site - i)
            else:
                obj.prevSites(obj.site - i + roadLength)
            
def timeStep(n, listOfCars, saveAnimData=False):
    animData = []
    for i in range(n):
        
        if saveAnimData == True:
            Datacopy = copy.deepcopy(listOfCars)
            animData.append(Datacopy)
            
        oneTimeStep(listOfCars)
    return animData
