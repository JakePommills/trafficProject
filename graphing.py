'''
graphing.py - file containing graphing functions to produce
              different plots of the system.
'''

# IMPORTS
from MAIN import timeStep, genCars, roadLength
from matplotlib.animation import FuncAnimation
from statistics import mean
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import time

np.random.seed(4294967295)

def prepareData(listOfCars, filler):
    # changes carslist  to a list of sites, where
    # car objects are stored, and 0 if site empty
    out = [filler for i in range(roadLength)]
    
    for obj in listOfCars:
        out[obj.site] = obj
    
    return out

def position(n, nCars):
    
    # output positions of cars at nth timestep
    
    carsList = genCars(nCars) # fill the road will cars
    timeStep(n, carsList)
    myList = prepareData(carsList, 0)
    for i in range(len(myList)):
        if myList[i] != 0:
            myList[i] = 1
    plt.bar( [i for i in range(roadLength)], myList )
    

def positionHeatmap(n, nCars):
    # Demonstrates jams move backwards
    
    carsList = genCars(nCars, random=False) # fill the road will cars
    anim = timeStep(n, carsList, saveAnimData = True)
    
    data = []
    np.array(data)
    
    for i in range(len(anim)):
        myList = prepareData(anim[i], None)
        for j in range(len(myList)):
            if myList[j] != None:
                myList[j] = myList[j].v
        data.append(myList)
        df = pd.DataFrame(data)
        # Print an extract of myList    
        #(''.join([str(elem) for elem in myList[50:200]]))
    # Generate the plot
    df.fillna(value=np.nan, inplace=True)
    cmap = sns.mpl_palette("Blues", 5)
    ax = sns.heatmap(df, cmap=cmap)
    ax.set_xlabel("Site")
    ax.set_ylabel("Timestep Number")
    ax.set_yticklabels([])
    ax.set_xticklabels([])

    plt.show()
        
def getFlow(n, nCars, useAvg=False):
    #get flow and density of a system
    
    carsList = genCars(nCars, random=False) # fill the road will cars
    timeStep(n, carsList)
    
    myBin = [0 for x in range(roadLength)]
    for i in carsList:
        for j in i.passedSites:
            myBin[j-1] = myBin[j -1] + 1

    avg = mean(myBin)
    flow = myBin[-1]/n # get flow of last site
    density = nCars/roadLength
    
    if useAvg == True:
        flow = avg/n

    return flow, density

def flowDensityPlot(t = 100, plot=True):
    flowL, densityL = [],[]
      
    for i in np.linspace(0,roadLength, num=100).astype(int): # i is iterating over number of cars used to sample a density
        flow, density = getFlow(t, i, useAvg = True)
        flowL.append(flow)
        densityL.append(density)
    
    if plot == True:
        plt.xlabel("Density")
        plt.ylabel("Flow")
        plt.plot(densityL, flowL)
        # plt.axvline(x=0.08, color='gray', linestyle='-')
    return densityL, flowL

def flowDensityMulti(iterations, t = 100):
    flow = []
    for i in range(iterations):
        densityOUT, flowOUT = flowDensityPlot(plot=False)
        flow.append(flowOUT)

    avgs, stds = [],[]
    
    for i in range(len(flow[0])):
        vals = [j[i] for j in flow]
        avgs.append( mean(vals) )
        stds.append( np.std(vals) )# error in y

    plt.xlabel("Density")
    plt.ylabel("Flow")
    
    sub = [a - b for a, b in zip(avgs, stds)]    
    add = [a + b for a, b in zip(avgs, stds)] 
 
    plt.plot(densityOUT, avgs, color="#1f77b4")    
    plt.fill_between(densityOUT, sub, add, alpha=0.2, color='#1f77b4')    

def getAvgSpeed(n, nCars):
    # get average speed and density of a system

    carsList = genCars(nCars, random=False) # fill the road will cars
    timeStep(n, carsList)
    
    speeds = []
    density = nCars/roadLength
    
    for i in carsList:
        
        speeds.append(i.v)
        
    if len(speeds) == 0:
        return 0, density # first var to reuturn is Vmax

    avg = sum(speeds) / len(speeds)
    
    return avg, density

def densitySpeedPlot(t = 100, plot=True):
    # Plot average speeds against density.
    
    speeds, densityL = [], []
        
    for i in np.linspace(0,roadLength, num=200).astype(int): # i is sampling densities
        avgSpeed, densityOUT = getAvgSpeed(t, i)
        speeds.append(avgSpeed)
        densityL.append(densityOUT)
    if plot == True:
        plt.xlabel("Density")
        plt.ylabel("Average speed $V$")
        plt.plot(densityL, speeds)
    return speeds, densityL

def densitySpeedMulti(iterations, t = 100):
    # Error band plot for density-speed
    speeds = []

    for i in range(iterations):
        avgSpeed, densityOUT = densitySpeedPlot(plot=False)
        speeds.append(avgSpeed)
        
    avgs, stds = [],[]
    
    for i in range(len(speeds[1])):
        vals = [j[i] for j in speeds]
        avgs.append( mean(vals) )
        stds.append( np.std(vals) )# error in y
    
    plt.xlabel("Density")
    plt.ylabel("Average Speed")

    sub = [a - b for a, b in zip(avgs, stds)]    
    add = [a + b for a, b in zip(avgs, stds)] 
 
    plt.plot(densityOUT, avgs, color="#1f77b4")    
    plt.fill_between(densityOUT, sub, add, alpha=0.2, color='#1f77b4')