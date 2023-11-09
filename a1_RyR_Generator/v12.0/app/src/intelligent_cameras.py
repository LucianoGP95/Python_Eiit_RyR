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
    filtered_list = sorted(filtered_list, key=lambda x: int(x.split(".")[0]) if x.split(".")[0].isdigit() else float('inf')) #Orders the list just in case there are only numbers as filenames
    return filtered_list

def data_loader(filtered_list: list[str], specific_rows: list) -> pd.DataFrame:
    '''Loads the data into a DataFrame'''
    data_frames = []  # To store individual DataFrames for each file
    for file in filtered_list:
        df = pd.read_csv(file, header=None, names=['Value'])
        filtered_df = df.loc[specific_rows]
        data_frames.append(filtered_df)
    # Concatenate DataFrames horizontally
    data = pd.concat(data_frames, axis=1, ignore_index=True)
    # Create an index column
    index_array = [f"Light Point: {index+1}" for index in range(data.shape[0])]
    index_array = pd.DataFrame(index_array, columns=['Index'])
    data = data.reset_index(drop=True)
    index_array = index_array.reset_index(drop=True)
    # Concatenate the index column with the data
    data = pd.concat([index_array, data], axis=1)
    # Create a row of test numbers
    test_number_array = ["Test point"] + [f"Test Number: {index}" for index in range(1, data.shape[1])]
    test_number_array = pd.DataFrame([test_number_array], columns=data.columns)
    # Concatenate the row of test numbers with the data
    data = pd.concat([test_number_array, data], ignore_index=True)
    return data