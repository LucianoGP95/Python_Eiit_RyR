import os
import pandas as pd 

def file_filter(source_dirname: str, extension: str) -> list[str]:
    """Filters filenames in a directory based on a given file extension.
    Parameters:
    - source_dirname (str): The directory containing the files.
    - extension (str): The file extension to filter by.
    Returns:
    list[str]: A list of filenames with the specified extension, sorted numerically if applicable."""
    file_list = os.listdir(source_dirname)
    filtered_list = [os.path.join(source_dirname, filename) for filename in file_list if filename.endswith(extension)]
    filtered_list = sorted(filtered_list, key=lambda x: int(x.split(".")[0]) if x.split(".")[0].isdigit() else float('inf')) #Orders the list just in case there are only numbers as filenames
    return filtered_list

def data_loader(filtered_list: list[str], specific_rows: list) -> pd.DataFrame:
    """Loads data from a list of files into a DataFrame.
    Parameters:
    - filtered_list (list[str]): A list of file paths to be loaded.
    - specific_rows (list): The list of row indices to extract from each file.
    Returns:
    pd.DataFrame: A DataFrame containing the loaded data with index and test number columns."""
    data_frames = []  #To store individual DataFrames for each file
    for file in filtered_list: 
        df = pd.read_csv(file, header=None, names=['Value'])
        filtered_df = df.loc[specific_rows]
        data_frames.append(filtered_df) #Concatenate DataFrames horizontally
    data = pd.concat(data_frames, axis=1, ignore_index=True)
    index_array = [f"Light Point: {index+1}" for index in range(data.shape[0])]
    index_array = pd.DataFrame(index_array, columns=['Index'])
    data = data.reset_index(drop=True)
    index_array = index_array.reset_index(drop=True)
    data = pd.concat([index_array, data], axis=1)
    test_number_array = ["Test point"] + [f"Test Number: {index}" for index in range(1, data.shape[1])]
    test_number_array = pd.DataFrame([test_number_array], columns=data.columns)
    data = pd.concat([test_number_array, data], ignore_index=True)
    return data