import pandas as pd
import os
import sys
import db_tools as db #Personal tool for managing sqlite databases in data science
import os, sys  ####Delete after debugging

def limits_generators(tolerance, values):
    '''Generate the limit values for a list containing the means in a DataFrame.
    Calculates the total mean for each position and fiber axis and applies it to the
    corresponding rows.'''
    tol = 0.015
    val = [0.3467, 0.342, 0.3475, 0.3543]
    ave = sum(val)/len(val)
    print(f"average per position: {round(ave, 4)}")
    h = ave + tol / 2
    print(f"high limit: {round(h, 4)}")
    l = ave - tol / 2
    print(f"low limit: {round(l, 4)}")

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

