import tkinter as tk
import tkinter.filedialog
import tkinter.messagebox
import os, time
import openpyxl as opxl #Read and write in xlsx
import pandas as pd #Import from csv and manipulate data
from file_number_checker import check_file_counts_2S, check_file_counts_4S
from intelligent_cameras import file_filter, data_loader
from light_guides import nest_filter, ndallocator, writer
from database import store_all, store_actual

##Default values init
source_dirname = ""
target_dirname = ""
frow = 5
lrow = 10
specific_rows = list(range(frow-1, lrow))

##Helper functions
def get_name(source_path: str) -> str:
    """Gets the name of the tooling by reading the first valid filename in the 
    input folder. Handles naming problems by giving a generic name.
    Returns:
    str: A string representing tooling name that appears in the report."""
    extension = "csv" #Extension to use. Add more in the future if necessary
    file_list = [filename for filename in os.listdir(source_path) if filename.endswith(extension)]
    if not file_list:  #Check if the file list is empty
        return "Generic_tooling"
    file_path = os.path.join(source_path, file_list[0])  #Use os.path.join to create the full file path
    _, filename = os.path.split(file_path)
    parts = filename.split('_')
    tooling_name = '_'.join(parts[:-4]) #Slice the parts to remove the last 4 elements
    if not tooling_name:  # Check if tooling_name is an empty string
        return "Generic_tooling"
    return tooling_name

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

def format_output(df: pd.DataFrame) -> pd.DataFrame:
    """Gives a correct format to the output"""
    columns_number = df.shape[1]
    df.columns = range(columns_number)  #Resets columns
    new_column_names = { #Create a dictionary for renaming
        0: "Guía de luz", 
        columns_number - 2: "LO_LIMIT", 
        columns_number - 1: "HI_LIMIT"
    }
    df.rename(columns=new_column_names, inplace=True)
    df.reset_index(drop=True, inplace=True) #Reset index
    return df

def generate_output(target_folderpath: str, data: pd.DataFrame, tooling_name="Generic_tooling", start_file=True):
    """Generates output files from the data and opens it for review.
    Parameters:
    - target_folderpath (str): The folder where the files will be saved.
    - data (pd.DataFrame): The DataFrame to be saved.
    - start_file (bool, optional): Whether to open the generated file for review. Defaults to True.
    Returns:
    None"""
    print(data)
    print(data.shape)
    target_filepath = os.path.join(os.path.abspath(target_folderpath), tooling_name) #Generic filepath
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
    elif selected_option.get() == options[2]: #Light guides: 2 nests
        final_output = pd.DataFrame()
        for nest in range(2):
            files = nest_filter(source, f"S{nest+1}")
            data = ndallocator(files, specific_rows)
            output = writer(files, data, source, specific_rows)
            final_output = pd.concat([final_output, output])
        #Checks the number of files to ensure two same sized dataframes are concat
        check_file_counts_2S(source_dirname)
        #Group all the results and write them in target
    elif selected_option.get() == options[3]: #Light guides: 4 nests
        final_output = pd.DataFrame()
        for nest in range(4):
            files = nest_filter(source, f"S{nest+1}")
            data = ndallocator(files, specific_rows)
            output = writer(files, data, source, specific_rows)
            final_output = pd.concat([final_output, output])
        #Checks the number of files to ensure two same sized dataframes are concat
        check_file_counts_4S(source_dirname)
        #Group all the results and write them in target
    elif selected_option.get() == options[4]: #Deep camera
        filtered_list = file_filter(source_dirname, "rsl")
        data = data_loader(filtered_list, specific_rows)
    df_name = get_name(source) + "_" + get_date()
    formatted_output = format_output(final_output) #Gives a correct format to the output
    generate_output(target, formatted_output, tooling_name=get_name(source)) #Generates the output files
    store_actual(df_name, "RyR_data.db", formatted_output) #Saves the RyR dataframe in the db

