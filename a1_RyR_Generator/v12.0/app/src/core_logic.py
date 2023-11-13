import tkinter as tk
import tkinter.filedialog
import tkinter.messagebox
import os, time
import openpyxl as opxl #Read and write in xlsx
import pandas as pd #Import from csv and manipulate data
import file_number_checker as check
from intelligent_cameras import file_filter, data_loader
from light_guides import nest_filter, ndallocator, writer

##Default values init
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
    """Generates output files from the data and opens it for review.
    Parameters:
    - target_folderpath (str): The folder where the files will be saved.
    - data (pd.DataFrame): The DataFrame to be saved.
    - start_file (bool, optional): Whether to open the generated file for review. Defaults to True.
    Returns:
    None"""
    target_filepath = os.path.join(os.path.abspath(target_folderpath), "Data") #Generic filepath
    target_filepath_csv = target_filepath + "_" + get_date() + ".csv" #csv filepath
    data.to_csv(target_filepath_csv, index=False, header=None)
    target_filepath_xlsx = target_filepath + "_" + get_date() + ".xlsx" #xlsx filepath
    data.to_excel(target_filepath_xlsx, index=False, startrow=3, startcol=0, header=None)
    if start_file is True: #Condition to open the file
        try: #Manages trying to open the file in a PC without Excel
            os.startfile(target_filepath_xlsx)  #Opens the file for review
        except OSError as e:
            print(f"Excel error: {e}")

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
        S = nest_filter(source, "S")
        data = ndallocator(S, specific_rows)
        final_output = writer(S, data, source, specific_rows)
        #Group all the results and write them in target
        generate_output(target, final_output)
    elif selected_option.get() == options[2]: 
        #Nest 1
        S1 = nest_filter(source, "S1")
        data = ndallocator(S1, specific_rows)
        Output = writer(S1, data, source, specific_rows)
        Output_S1 = Output
        #Nest 2
        S2 = nest_filter(source, "S2")
        data = ndallocator(S2, specific_rows)
        Output = writer(S2, data, source, specific_rows)
        Output_S2 = Output
        #Checks the number of files to ensure two same sized dataframes are concat
        check.check_file_counts_2S(source_dirname)
        #Group all the results and write them in target
        final_output = pd.concat([Output_S1, Output_S2])
        generate_output(target, final_output)
    elif selected_option.get() == options[3]:
        #Nest 1
        S1_files = nest_filter(source, "S1")
        data = ndallocator(S1_files, specific_rows)
        Output = writer(S1_files, data, source, specific_rows)
        Output_S1 = Output
        #Nest 2
        S2_files = nest_filter(source, "S2")
        data = ndallocator(S2_files, specific_rows)
        Output = writer(S2_files, data, source, specific_rows)
        Output_S2 = Output
        #Nest 3
        S3_files = nest_filter(source, "S3")
        data = ndallocator(S3_files, specific_rows)
        Output = writer(S3_files, data, source, specific_rows)
        Output_S3 = Output
        #Nest 4
        S4_files = nest_filter(source, "S4")
        data = ndallocator(S4_files, specific_rows)
        Output = writer(S4_files, data, source, specific_rows)
        Output_S4 = Output
        #Checks the number of files to ensure two same sized dataframes are concat
        check.check_file_counts_4S(source_dirname)
        #Group all the results and write them in target
        final_output = pd.concat([Output_S1, Output_S2, Output_S3, Output_S4])
        generate_output(target, final_output)
    elif selected_option.get() == options[4]: #Implementation for camera testing
        filtered_list = file_filter(source_dirname, "rsl")
        data = data_loader(filtered_list, specific_rows)
        generate_output(target, data)

