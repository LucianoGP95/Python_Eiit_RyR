import pandas as pd
import os
import sys
sys.path.append("../tools/")
import _db_tools as db
import os, sys  ####Delete after debugging
from globals import glob

def limits_generator(tolerance: float, values: list) -> list:
    '''Generate the limit values for a list containing the means.
    Calculates the total mean for each position and fiber axis and applies it to the
    corresponding rows.'''
    average = sum(values)/len(values)
    print(f"Average: {round(average, 4)}")
    high_limit = average + tolerance / 2
    print(f"high limit: {round(high_limit, 4)}")
    low_limit = average - tolerance / 2
    print(f"low limit: {round(low_limit, 4)}")
    return [high_limit, low_limit]

#Data preparation
dbh = db.SQLite_Data_Extractor("database.db") #Connect to the database
MEAS = dbh.retrieve(glob.tooling) #Get the desired tooling data
dbh.close_conn() 

def mean_calculator_per_position(MEAS, lenses_per_nest):
    '''Calculate the absolute means per fiber. Returns an array with fbx and fby
    means per position, useful for longer light guides'''
    resume = MEAS.transpose().describe() #Transpose the df first due to describe() working in columns.
    rough_means = list(resume.iloc[1, :].values)
    means_fbx = []; means_fby = []
    for i in range(lenses_per_nest*2):
        if i % 2 == 0:
            mean_fbx = rough_means[0::2] #Gets fbx values
            mean_fbx = mean_fbx[i::lenses_per_nest] #Gets the values of the specific lens
            abs_mean_fbx = sum(mean_fbx) / len(mean_fbx)
            means_fbx.append(abs_mean_fbx)
        else:
            mean_fby = rough_means[0::2] #Gets fbx values
            mean_fby = mean_fby[i::lenses_per_nest] #Gets the values of the specific lens
            abs_mean_fby = sum(mean_fby) / len(mean_fby)
            means_fby.append(abs_mean_fby)
    means = [means_fbx + means_fby]
    print("Means:") 
    print("  Fiber x: ")
    print([round(value, 4) for value in means_fbx])
    print("  Fiber y: ")
    print([round(value, 4) for value in means_fby])
    return means

