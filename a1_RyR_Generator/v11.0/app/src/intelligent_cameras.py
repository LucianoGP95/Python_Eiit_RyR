import os
import tkinter as tk
import tkinter.filedialog
import tkinter.messagebox
import openpyxl as opxl #Read and write in xlsx
import pandas as pd #Import from csv and manipulate data
import numpy as np

def file_filter(source_dirname: str, extension: str) -> list[str]:
    '''Filters the desired filenames'''
    file_list = os.listdir(source_dirname)
    filtered_list = [os.path.join(source_dirname, filename) for filename in file_list if filename.endswith(extension)]
    filtered_list = sorted(filtered_list, key=lambda x: int(x.split(".")[0]) if x.split(".")[0].isdigit() else float('inf')) #Orders the list just in case there are only numbers
    return filtered_list

def data_loader(filtered_list: list[str], specific_rows: list) -> pd.DataFrame:
    '''Loads the data into a Dataframe'''
    data = pd.DataFrame()
    index_array = []
    for file in filtered_list: #Data extraction
        df = pd.read_csv(file, header=None, names=['Value'])
        filtered_df = df[df.index.isin(specific_rows)]
        data = pd.concat([data, filtered_df], axis=1)
    print(data)
    for index, point in enumerate(range(len(filtered_list))): #Index column creation
        point = f"Light Point: {index+1}"
        index_array.append(point)
    index_array = pd.DataFrame(index_array)
    print(index_array)
    data = pd.concat([index_array, data], axis=0)
    print(data)
    for index, test_number in data.shape[1]: #Test number row creation
        if index == 0:
            test_number = "Test point" #Row index header
        index =+ 1 #Starts in index == 1
        test_number = f"Test Number: {index}"
        row = pd.DataFrame()
        row = pd.concat([row, test_number], axis=1)
    data = pd.concat([row, data], axis=0)
    return data