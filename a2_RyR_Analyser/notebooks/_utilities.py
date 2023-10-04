import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
from __globals import *
import sys
sys.path.append("../tools/")
import _db_tools as db

#Helper functions
def prepare_data(target, filter=None):
    '''Prepares the output data by extracting the measures in a df and storing them in the database.
    Per default gets the measures and it can be used to get the limits'''
    data = pd.read_excel(target) #Import the RyR generator output
    if filter == None:
        df = data.iloc[2:, 1:] #Slices measures and limits
    elif filter == "MEAS":
        df = data.iloc[2:, 1:-2] #Slices measures
    elif filter == "limits":
        df = data.iloc[2:, -2:] #Slices limits
    else:
        raise Exception("Specify a supported filter key: None, MEAS, limits.")
    df.reset_index(drop=True, inplace=True) #Reset rows index
    df.columns = range(df.shape[1]) #Reset columns index
    return df

def prepare_database(df, table_name):
    '''Prepares the database from a ready-to-store df and returns the same df, getting it from the db'''
    dbh = db.SQLite_Data_Extractor("database.db") #Allows for database management
    dbh.store_df(df, table_name) #Store the dataframe in the connected database
    dbh.consult_tables() #Checks results

def plot_scatter(df, title=None, xlabel=None, ylabel=None, legend_label=None, filter=None):
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
    def labeler(filter, i, index):
        '''Small function to correctly label legends'''
        if filter == "x" or filter == "y":
            label = f"{legend_label} {i} {filter}"
        elif isinstance(filter, (int, list, tuple)):
            label = f"{legend_label} {index}"
        elif filter == None:
            label = f"Fiber: {index+1}"
        return label
    #Determine the rows to plot based on the filter
    if filter == 'x':
        rows_to_plot = df.iloc[1::2] #Rows with odd indices
    elif filter == 'y':
        rows_to_plot = df.iloc[::2]  #Rows with even indices
    elif filter is None:
        rows_to_plot = df #All rows
    elif isinstance(filter, (int)):
        filter = [filter]
        rows_to_plot = df.iloc[filter]
    elif isinstance(filter, (list, tuple)):
        rows_to_plot = df.iloc[filter]
    for index, row in rows_to_plot.iterrows(): #Plot the selected rows
        i += 1
        plt.scatter(
            list(range(1, df.shape[1] + 1)),
            row,
            label=labeler(filter, i, index)
        )
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    if legend_label:
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.show()

#test script
if __name__ == "__main__":
    df = prepare_data("../data/target.xlsx", filter="MEAS") #Load the output from RyR_Generator into a df
    prepare_database(df, "PASSAT_B9_TOP") #Store a df inside the database of the project
    dbh = db.SQLite_Data_Extractor("database.db") #Connect to the database
    df = dbh.retrieve("PASSAT_B9_TOP") #Get the desired tooling data 