import os, sys, time  ####Delete after debugging
os.chdir(os.path.dirname(os.path.realpath(__file__)))  ####Delete after debugging
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
from globals import glob
import sys
sys.path.append("../tools/")
import _db_tools as db

dbh_i = db.SQLite_Data_Extractor("input.db") #Allows for database management
dbh_o = db.SQLite_Data_Extractor("output.db")

#Helper functions
def select_database(db_name):
    global dbh
    if db_name == "input.db":
        dbh = dbh_i
    elif db_name == "output.db":
        dbh = dbh_o
    else: 
        raise ValueError("Unsupported database")

def prepare_database(db_name, df, table_name):
    '''Prepares the database from a ready-to-store df and returns the same df, getting it from the db'''
    select_database(db_name)
    dbh.reconnect(db_name, verbose=False)
    dbh.store_df(df, table_name) #Store the dataframe in the connected database
    dbh.close_conn(verbose=False)

def consult_database(db_name):
    select_database(db_name)
    dbh.reconnect(db_name, verbose=False)
    dbh.consult_tables() #Checks results
    dbh.close_conn(verbose=False)

def clear_database(db_name):
    select_database(db_name)
    dbh.reconnect(db_name, verbose=False)
    dbh.clear_database()
    dbh.close_conn(verbose=False) 

def retrieve_data(db_name, table_name):
    select_database(db_name)
    dbh.reconnect(db_name, verbose=False)
    df = dbh.retrieve(table_name)
    dbh.close_conn(verbose=False) 
    return df

def prepare_data(target: (str, list[str]), filter=None):
    '''Prepares the output data by extracting the measures in a df and storing them in the database.
    Per default gets the measures and it can be used to get the limits'''
    data = pd.read_excel(target) #Import the RyR generator output
    if filter == None:
        df = data.iloc[2:, 1:] #Slices measures and limits
    elif filter == "measurements":
        df = data.iloc[2:, 1:-2] #Slices measures
    elif filter == "limits":
        df = data.iloc[2:, -2:] #Slices limits
    else:
        raise Exception("Specify a supported filter key: None, MEAS, limits.")
    df.reset_index(drop=True, inplace=True) #Reset rows index
    df.columns = range(df.shape[1]) #Reset columns index
    return df

def rename_limits_table(db_name, old_name):
    dbh.reconnect(db_name, verbose=False)
    parts = old_name.split("_")
    first_part = parts[:-7]
    date = parts[-7:-1]
    last_part = [parts[-1]]
    new_name = first_part + last_part + date
    new_name = "_".join(new_name)
    dbh.rename_table(old_name, new_name, verbose=False)
    dbh.close_conn(verbose=False) 
    return new_name

def rename_index(df):
    new_index = 0
    for index in range(df.shape[0]):
        old_entry = index
        new_index += 1 if index % 2 == 0 else 0  # Increment new_index only on odd iterations
        axis = "X" if index % 2 == 0 else "Y"
        new_entry = f"Guia_Luz_Blanco_FB{new_index}_{axis}"
        df = df.rename(index={old_entry: new_entry})
    return df

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

def plot_scatter(df, title=None, xlabel=None, ylabel=None, filter=None):
    ''' Plots a DataFrame as a scatter plot with optional filtering and customization.
    Parameters:
        df (DataFrame): The input DataFrame containing the data.
        title (str, optional): The title of the plot.
        xlabel (str, optional): The label for the x-axis.
        ylabel (str, optional): The label for the y-axis.
        legend_label (str, optional): The label for the legend.
        filter (str, int, list, tuple, optional): Filter for selecting specific data points.
            - 'x' plots rows with odd indices.
            - 'y' plots rows with even indices.
            - None plots all rows.
            - int, list, or tuple selects specific row(s) based on the provided filter.
    Returns:
        None '''
    i = 0 #Preallocation
    if filter is not None:
        filter = filter.upper() if isinstance(filter, str) else filter #Handles lower cases
    def labeler(filter, index, j, k):
        '''Small function to correctly label legends'''
        if filter in ["X", "Y"]:
            axis = filter
            label = f"Guia_Luz_Blanco_FB{k}_{axis}"
        elif isinstance(filter, (list, tuple)):
            axis = "Y" if filter[k-1] % 2 == 0 else "X"
            #Calculate exact number of fiber in future
            label = f"Guia_Luz_Blanco_FB_{'placeholder'}{axis}"
        elif filter == None:
            axis = "X" if index % 2 == 0 else "Y"
            label = f"Guia_Luz_Blanco_FB{j}_{axis}"
        return label
    #Determine the rows to plot based on the filter
    if filter == 'X':
        rows_to_plot = df.iloc[1::2] #Rows with odd indices
    elif filter == 'Y':
        rows_to_plot = df.iloc[::2]  #Rows with even indices
    elif filter is None:
        rows_to_plot = df #All rows
    elif isinstance(filter, (int)):
        filter = [filter]
        rows_to_plot = df.iloc[filter]
    elif isinstance(filter, (list, tuple)):
        rows_to_plot = df.iloc[filter]
    j = 0; k = 0
    for index, row in rows_to_plot.iterrows(): #Plot the selected rows
        j += 1 if index % 2 == 0 else 0  # Increment new_index only on odd iterations
        k += 1
        plt.scatter(
            list(range(1, df.shape[1] + 1)),
            row,
            label=labeler(filter, index, j, k)
        )
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.show()

#test script
if __name__ == "__main__":
    table_names = ['TOP_PASSAT_B9_2023y_11m_14d_17h_21m_03s', 'TOP_PASSAT_B9_limits_2023y_11m_14d_17h_21m_03s']
    measurements = retrieve_data("database.db", table_names[0])
    limits = retrieve_data("database.db", table_names[1])
    plot_scatter(measurements, title='Scatter Plot, fiber X', xlabel='test', ylabel='MEAS', filter=23)
    df = prepare_data(os.path.join(os.path.abspath("../data/"), "target.xlsx"), filter="MEAS") #Load the output from RyR_Generator into a df
    prepare_database(df, "PASSAT_B9_TOP") #Store a df inside the database of the project
    dbh = db.SQLite_Data_Extractor("database.db") #Connect to the database
    df = dbh.retrieve("PASSAT_B9_TOP") #Get the desired tooling data 