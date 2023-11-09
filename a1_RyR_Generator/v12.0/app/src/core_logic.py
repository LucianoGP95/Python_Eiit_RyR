import tkinter as tk
import tkinter.filedialog
import tkinter.messagebox
import os, time
import openpyxl as opxl #Read and write in xlsx
import pandas as pd #Import from csv and manipulate data
import file_number_checker as check
from intelligent_cameras import file_filter, data_loader
from light_guides import *

source_dirname = ""
target_dirname = ""
frow = 5
lrow = 10
specific_rows = list(range(frow-1, lrow))

##Helper functions
def get_date() -> str:
    """Gets the current date in a formatted string.
    Returns:
    str: A string representing the current date and time in the format "YYYY-MM-DD_HH-MM-SS"."""
    current_date = time.localtime()
    min = current_date.tm_min; sec = current_date.tm_sec
    day = current_date.tm_mday; hour = current_date.tm_hour
    year = current_date.tm_year; month = current_date.tm_mon
    current_date_format = f"{year}y-{month:02d}m-{day:02d}d_{hour}h-{min:02d}m-{sec:02d}s"
    return current_date_format

def generate_output(target_folderpath: str, data: pd.DataFrame, start_file=True):
    """Generates an Excel file from the data and opens it for review.
    Parameters:
    - target_folderpath (str): The folder where the Excel file will be saved.
    - data (pd.DataFrame): The DataFrame to be saved to the Excel file.
    - start_file (bool, optional): Whether to open the generated file for review. Defaults to True.
    Returns:
    None"""
    target_filepath = os.path.join(target_folderpath, "Data")
    target_filepath = target_filepath + "_" + get_date() + ".xlsx"
    data.to_excel(target_filepath, index=False, startrow=0, startcol=0, header=None)
    if start_file is True:
        os.startfile(target_filepath)  #Opens the file for review

##Row updater functions
def update_frow(event, first_r: int) -> list: 
    '''Refresh the first row selected in the UI'''
    global frow, specific_rows
    frow = int(first_r.get())
    specific_rows = list(range(frow-1, lrow))
    
def update_lrow(event, last_r: int) -> list: 
    '''Refresh the last row selected in the UI'''
    global lrow, specific_rows
    lrow = int(last_r.get())
    specific_rows = list(range(frow-1, lrow))

##Main function
def nest_number(selected_option, options, source, target, source_dirname):
    '''Determines the workflow of the data extraction for different numbers of nests'''
    if selected_option.get() == options[1]: #Nest unspecified. Can be used with PCB testing.
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
    elif selected_option.get() == options[4]: #Implementation for camera testing
        filtered_list = file_filter(source_dirname, "rsl")
        data = data_loader(filtered_list, specific_rows)
        generate_output(target, data)

