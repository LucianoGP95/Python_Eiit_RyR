import os
import pandas as pd
import numpy as np

def nest_filter(source_dirname, substring):
    '''Filters each nest reports by reading a substring in the filename'''
    file_list = os.listdir(source_dirname)
    filtered_list = [filename for filename in file_list if substring in filename]
    return filtered_list
def ndallocator(nest, specific_rows):
    '''Allocates an empty ndarray of the size needed to hold the values of every nest'''
    size = enumerate(nest)
    size = len(list(size))
    data = np.zeros([len(specific_rows), size])
    return data
def writer(nest, data, source_dirname, specific_rows):
    '''Writes over the array column by column'''
    for i, filename in enumerate(nest):
        Source = pd.read_csv(source_dirname + "/" + nest[i], skiprows = lambda x: x not in specific_rows, header=None) #Open the csv and build a Dataframe with the target rows
        Text = Source.iloc[:, 2] #Indexes the test name column
        MEAS = np.zeros(len(specific_rows))
        for j in range(data.shape[0]):
            try:
                MEAS[j] = float(Source.iloc[j, 3])
            except (ValueError, TypeError):
                MEAS[j] = 0.0
        lo_limit = Source.iloc[:, 4] #Indexes the low limit value
        hi_limit = Source.iloc[:, 5] #Indexes the high limit value
        data[:, i] = MEAS #Writes the column on the array  
    Output = pd.DataFrame(data) #Makes a new Dataframe with the completed array
    Output = pd.concat([Text, Output, lo_limit, hi_limit], axis=1)
    return Output
def compiler_1(Output_S1, target):
    '''Concatenates the data frames for each nest'''
    Final = pd.concat([Output_S1])
    Final.to_excel(target, index=False, startrow=3, startcol=0, header=None) #Writes the values in the excel file
    os.startfile(target) #Opens the file for review
def compiler_2(Output_S1, Output_S2, target):
    '''Concatenates the data frames for each nest'''
    Final = pd.concat([Output_S1, Output_S2], ignore_index=True)
    Final.to_excel(target, index=False, startrow=3, startcol=0, header=None) #Writes the values in the excel file
    os.startfile(target) #Opens the file for review
def compiler_4(Output_S1, Output_S2, Output_S3, Output_S4, target):
    '''Concatenates the data frames for each nest'''
    Final = pd.concat([Output_S1, Output_S2, Output_S3, Output_S4])
    Final.to_excel(target, index=False, startrow=3, startcol=0, header=None) #Writes the values in the excel file
    os.startfile(target) #Opens the file for review