import pandas as pd
import os
from globals import glob
from utilities import prepare_data, prepare_database
import configparser
import sys
sys.path.append("../tools/")
import _db_tools as db #Personal tool for managing sqlite databases in data science

####Helper Functions####
def mean_calculator(MEAS, lenses_per_nest=None):
    '''Calculate the desired means:
    Parameters:
    MEAS (DataFrame): The input DataFrame containing fiber measurements.
    lenses_per_nest (int, optional): The number of lenses per nest for specific means calculation. If None, global means are calculated.
    Returns:
    list: A list containing the mean values for fbx and fby. If lenses_per_nest is specified, it returns specific means for each position.
    If lenses_per_nest is None:
        - Calculates a global mean for fbx and fby.
        - Returns the mean values for both fbx and fby in a list.
        - Displays the mean values for fbx and fby.
    If lenses_per_nest is specified:
        - Calculates specific means for each position for fbx and fby based on the number of lenses per nest.
        - Returns a list containing specific mean values for fbx and fby for each position.
        - Displays the specific mean values for fbx and fby per position.'''
    resume = MEAS.transpose().describe() #Transpose the df first due to describe() working in columns.
    rough_means = list(resume.iloc[1, :].values)
    means = []; means_fbx = []; means_fby = [] #Preallocation
    if lenses_per_nest == None: #Calculates a global mean for fbx and for fby
        for i, mean in enumerate(rough_means): #Iterates and rounds every mean value
            mean = round(mean, 4)
            means_fbx.append(mean) if i % 2 == 0 else means_fby.append(mean)
            means.append(mean)
        abs_mean_fbx = sum(means_fbx) / len(means_fbx)
        abs_mean_fby = sum(means_fby) / len(means_fby)
        means = [abs_mean_fbx, abs_mean_fby]
        print("Means:") 
        print("Fiber x: " + str(round(abs_mean_fbx, 4)))
        print("Fiber y: " + str(round(abs_mean_fby, 4)))
    else: #Calculates specific means for each position for fbx and fby
        for i in range(lenses_per_nest*2):
            if i % 2 == 0:
                mean_fbx = rough_means[0::2] #Gets fbx values
                mean_fbx = mean_fbx[i::lenses_per_nest] #Gets the values of the specific lens
                abs_mean_fbx = sum(mean_fbx) / len(mean_fbx)
                means_fbx.append(abs_mean_fbx)
            else:
                mean_fby = rough_means[0::2] #Gets fby values
                mean_fby = mean_fby[i::lenses_per_nest] #Gets the values of the specific lens
                abs_mean_fby = sum(mean_fby) / len(mean_fby)
                means_fby.append(abs_mean_fby)
        means = [means_fbx + means_fby]
        print("Means per position:") 
        print("  Fiber x: ")
        print([round(value, 4) for value in means_fbx])
        print("  Fiber y: ")
        print([round(value, 4) for value in means_fby])
    return means


