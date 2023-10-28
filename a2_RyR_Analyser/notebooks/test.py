#% pip install openpyxl
import os, sys  ####Delete after debugging
os.chdir(os.path.dirname(os.path.realpath(__file__)))  ####Delete after debugging
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from globals import glob
from utilities import plot_scatter, prepare_database
import sys
sys.path.append("../tools/")
import _db_tools as db
####Helper Functions####
def RyR(df: pd.DataFrame) -> pd.DataFrame:
    """ Calculates the RyR values for both fibers and provides a qualitative evaluation for each value.
    Parameters:
    - df (pd.DataFrame): The input DataFrame containing fiber measurements.
    Returns:
    Tuple[pd.DataFrame, pd.DataFrame]: A tuple containing two DataFrames:
    - The first DataFrame (dfx) contains the RyR values for fiber x.
    - The second DataFrame (dfy) contains the RyR values for fiber y.
    For each fiber, the function calculates the RyR (Range-to-Range) values as a percentage of the standard deviation
    and the difference between the last and second-to-last columns in the input DataFrame. It then prints a qualitative
    evaluation of each RyR value for both fibers.
    Qualitative Evaluation:
    - "Correct" if RyR <= 10.
    - "Low fail" if 10 < RyR <= 25.
    - "High fail" if RyR > 25."""
    i = 0; df_RyR = [] #Preallocate a counter and an empty dataframe where to add the rows
    std = df.iloc[:, :-2].std(axis=1) #Standard deviation for each row, excluding limits
    for index in range(df.shape[0]):
        i+= 1
        RyR = (6*std.iloc[index]/(df.iloc[index,-1]-df.iloc[index,-2]))*100 #Calculates RyR for the whole dataframe
        df_RyR.append(float(RyR)) #Adds the values of RyR to a ndarray
    df_RyR = pd.DataFrame(df_RyR) #Builds a new dataframe with the RyR values
    x_fiber = df_RyR[df_RyR.index % 2 != 0] #Indexes the fiber x RyR values in a new dataframe
    y_fiber = df_RyR[df_RyR.index % 2 == 0] #Indexes the fiber y RyR values in a new dataframe
    dfx = pd.DataFrame(x_fiber).reset_index(drop=True) #Resets row index
    dfy = pd.DataFrame(y_fiber).reset_index(drop=True) #Resets row index
    for i, _ in enumerate(range(dfx.shape[0])): #Prints the dataframe for fiber x row by row indexing with the counter
        Pass = "Correct" if dfx.iloc[i, 0] <= 10 else ("Low fail" if 10 <= dfx.iloc[i, 0] <= 25 else "High fail")
        print(f'RyR Guide fbx {dfx.index[i]+1}: ' + str(dfx.iloc[i, 0]) +' %' + ' Status: ' + Pass)
    print("")
    for i, _ in enumerate(range(dfy.shape[0])): #Prints the dataframe for fiber y row by row
        Pass = "Correct" if dfy.iloc[i, 0] <= 10 else ("Low fail" if 10 <= dfy.iloc[i, 0] <= 25 else "High fail")
        print(f'RyR Guide fby {dfy.index[i]+1}: ' + str(dfy.iloc[i, 0]) +' %' + ' Status: ' + Pass)
    return dfx, dfy

def z_score_filter(df, threshold, minimun_std = 0.0001):
    """Applies a z-score filter to a DataFrame, removing values that do not meet the specified threshold.
    Parameters:
    - df (pd.DataFrame): The input DataFrame containing the measurements and limits.
    - threshold (float): The z-score threshold. Values exceeding this threshold will be replaced with NaN.
    Returns:
    pd.DataFrame: A new DataFrame with values that pass the z-score filter, while retaining the original limits columns.
    For each row in the input DataFrame, the function calculates the z-scores for the measurement values and
    replaces values with z-scores greater than the specified threshold with NaN. The original limits columns are retained.
    """
    rows = []
    measures = df.iloc[:, :-2] #Indexes the measurements
    limits = df.iloc[:, -2:]  #Indexes the limits  
    for row in range(measures.shape[0]): #Iterates over the rows
        row = measures.iloc[row, :]
        if row.std() > minimun_std:
            z_scores = (row - row.mean()) / row.std() #Calculates the z-score
            filtered_row = np.where(abs(z_scores) <= threshold, row, np.nan) #Applies the threshold as a filter
        else:
            filtered_row = row
        rows.append(filtered_row)
    filtered_df = pd.DataFrame(rows) #Builds a new dataframe
    filtered_df = pd.concat([filtered_df, limits], axis=1) #Adds again the columns
    return filtered_df

#Data preparation
dbh = db.SQLite_Data_Extractor("database.db") #Connect to the database
measurements = dbh.retrieve(glob.tooling) #Get the desired tooling data
limits = dbh.retrieve(glob.tooling+"_limits") #Get the desired tooling data
dbh.close_conn() 

measurements_and_limits = pd.concat([measurements, limits], axis=1) #Gets both the measure and limits
#Filter values by their row z-score
z_df = z_score_filter(measurements_and_limits, 1)
#Plot the filtered values
plot_scatter(z_df.iloc[:, :-2], 'Scatter Plot, fiber X', 'test', 'MEAS', 'Fiber: ', filter='x')
plot_scatter(z_df.iloc[:, :-2], 'Scatter Plot, fiber Y', 'test', 'MEAS', 'Fiber: ', filter='y')

