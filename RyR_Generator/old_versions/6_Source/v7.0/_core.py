import tkinter as tk
import tkinter.filedialog
import tkinter.messagebox
import os
import openpyxl as opxl #Read and write in xlsx
import pandas as pd #Import from csv and manipulate data
import numpy as np
import _filenumber_checker as check

source_dirname = ""
target_dirname = ""
frow = 5
lrow = 10
specific_rows = list(range(frow-1, lrow))

##Row updater functions
def update_frow(event, first_r): 
    '''Refresh the first row selected in the UI'''
    global frow, specific_rows
    frow = int(first_r.get())
    specific_rows = list(range(frow-1, lrow))
    
def update_lrow(event, last_r): 
    '''Refresh the last row selected in the UI'''
    global lrow, specific_rows
    lrow = int(last_r.get())
    specific_rows = list(range(frow-1, lrow))

def row_auto_updater(source_dirname):
    global frow, lrow, specific_rows
    file_list = os.listdir(source_dirname)
    first_file = None
    for file in file_list:
        if file.endswith(".csv"):
            first_file = file
            break
    import csv
    csv_file_path = os.path.join(source_dirname, first_file)
    csv_data = []
    with open(csv_file_path, 'r', newline='') as csv_file:
        csv_reader = csv.reader(csv_file)
        csv_data = [row[0] for row in csv_reader]
        for i, row in enumerate(csv_data):
            ctrl_text = row.split('-')[0].strip()
            if ctrl_text == "TEST":
                frow = i+2
            if ctrl_text == "CTRL":
                lrow = i
    specific_rows = list(range(frow, lrow+1))
    print(specific_rows)
    return frow, lrow

##Helper functions
def nest_filter(source_dirname, substring):
    '''Filters each nest reports by reading a substring in the filename'''
    file_list = os.listdir(source_dirname)
    filtered_list = [filename for filename in file_list if substring in filename]
    return filtered_list
def ndallocator(nest):
    '''Allocates an empty ndarray of the size needed to hold the values of every nest'''
    size = enumerate(nest)
    size = len(list(size))
    data = np.zeros([len(specific_rows), size])
    return data
def writer(nest, data, source_dirname):
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
    Final = pd.concat([Output_S1, Output_S2], ignore_index=True)
    Final.to_excel(target, index=False, startrow=3, startcol=0, header=None) #Writes the values in the excel file
    os.startfile(target) #Opens the file for review
def compiler_4(Output_S1, Output_S2, Output_S3, Output_S4, target):
    Final = pd.concat([Output_S1, Output_S2, Output_S3, Output_S4])
    Final.to_excel(target, index=False, startrow=3, startcol=0, header=None) #Writes the values in the excel file
    os.startfile(target) #Opens the file for review

## Main functions
def nest_number(selected_option, options, source, target, source_dirname):
    '''Determines the workflow of the data extraction for different numbers of nests'''
    if selected_option.get() == options[1]: #Can be used with PCB testing too 
        #Nest unspecified
        S1 = nest_filter(source, "S")
        data = ndallocator(S1)
        Output = writer(S1, data, source)
        Output_S1 = Output
        #Group all the results and write them in target
        compiler_1(Output_S1, target)
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
        #Checks the number of files to ensure two same sized dataframes are concat
        check.check_file_counts_2S(source_dirname)
        #Group all the results and write them in target
        compiler_2(Output_S1, Output_S2, target)
    elif selected_option.get() == options[3]:
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
        #Checks the number of files to ensure two same sized dataframes are concat
        check.check_file_counts_4S(source_dirname)
        #Group all the results and write them in target
        compiler_4(Output_S1, Output_S2, Output_S3, Output_S4, target)

