import tkinter as tk
import tkinter.filedialog
import os
import openpyxl as opxl #Read and write in xlsx
import pandas as pd #Import from csv and manipulate data
import numpy as np

source_dirname = ""
target_dirname = ""
frow = 5
lrow = 18
specific_rows = list(range(frow-1, lrow))

#Row updater function
def update_frow(event, first_r): 
    global frow, specific_rows
    frow = int(first_r.get())
    specific_rows = list(range(frow-1, lrow))
    
def update_lrow(event, last_r): 
    global lrow, specific_rows
    lrow = int(last_r.get())
    specific_rows = list(range(frow-1, lrow))

## Helper functions
#Filters each nest reports by reading a substring
def nest_filter(source_dirname, substring):
    file_list = os.listdir(source_dirname)
    filtered_list = [filename for filename in file_list if substring in filename]
    return filtered_list
#Creates a zeros np array to hold the values of every nest
def ndallocator(nest):
    size = enumerate(nest)
    size = len(list(size))
    data = np.zeros([len(specific_rows), size])
    return data
#Writes over the array column bu column
def writer(nest, data, source_dirname):
    for i, filename in enumerate(nest):
        Source = pd.read_csv(source_dirname + "/" + nest[i], skiprows = lambda x: x not in specific_rows, header=None) #Open the csv and build a Dataframe with the target rows
        Text = Source.iloc[:, 2] #Indexes the test name column
        MEAS = Source.iloc[:, 3] #Indexes the measure column
        lo_limit = Source.iloc[:, 4] #Indexes the low limit value
        hi_limit = Source.iloc[:, 5] #Indexes the high limit value
        data[:, i] = MEAS #Writes the column on the array  
    Output = pd.DataFrame(data) #Makes a new Dataframe with the completed array
    Output = pd.concat([Text, Output, lo_limit, hi_limit], axis=1)
    return Output
#Concatenates the data frames for each next
def compiler_2(Output_S1, Output_S2, target):
    Final = pd.concat([Output_S1, Output_S2])
    Final.to_excel(target, index=False, startrow=3, startcol=0, header=None) #Writes the values in the excel file
    os.startfile(target) #Opens the file for review
def compiler_4(Output_S1, Output_S2, Output_S3, Output_S4, target):
    Final = pd.concat([Output_S1, Output_S2, Output_S3, Output_S4])
    Final.to_excel(target, index=False, startrow=3, startcol=0, header=None) #Writes the values in the excel file
    os.startfile(target) #Opens the file for review

## Main functions
def nest_number(selected_option, options, source, target):
    if selected_option.get() == options[1]: 
        #Nest 1
        S1 = nest_filter(source, "S1")
        data = ndallocator(S1)
        Output = writer(S1, data, source)
        Output_S1 = Output
        #Nest 2
        S2 = nest_filter(source, "S2")
        data = ndallocator(S2)
        Output = writer(S2, data, source)
        Output_S2 = Output
        #Group all the results and write them in target
        compiler_2(Output_S1, Output_S2, target)
    elif selected_option.get() == options[2]:
        #Nest 1
        S1 = nest_filter(source, "S1")
        data = ndallocator(S1)
        Output = writer(S1, data, source)
        Output_S1 = Output
        #Nest 2
        S2 = nest_filter(source, "S2")
        data = ndallocator(S2)
        Output = writer(S2, data, source)
        Output_S2 = Output
        #Nest 3
        S3 = nest_filter(source, "S3")
        data = ndallocator(S3)
        Output = writer(S3, data, source)
        Output_S3 = Output
        #Nest 4
        S4 = nest_filter(source, "S4")
        data = ndallocator(S4)
        Output = writer(S4, data, source)
        Output_S4 = Output
        #Group all the results and write them in target
        compiler_4(Output_S1, Output_S2, Output_S3, Output_S4, target)

