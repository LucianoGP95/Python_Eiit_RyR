import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
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
    '''Plots a dataframe into a scatter plot using one of the dimensions of the colous measurement. 
    Optionally filters the plot by fiber axis values and specific fiber(s) axis.'''
    i = 0  #Counter used for the fiber number in the legend
    if filter == 'x':  #Guide selector (filter) using strings
        for index, row in df.iterrows():
            if index % 2 != 0:
                i += 1
                plt.scatter(
                    list(element + 1 for element in list(range(df.shape[1]))),
                    df.iloc[index],
                    label=legend_label + f'{i}' if legend_label else None,
                )
    elif filter == 'y':
        for index, row in df.iterrows():
            if index % 2 == 0:
                i += 1
                plt.scatter(
                    list(element + 1 for element in list(range(df.shape[1]))),
                    df.iloc[index],
                    label=legend_label + f'{i}' if legend_label else None,
                )
    elif filter == None: #Plots all fibers
        for index, row in df.iterrows():
            i += 1
            plt.scatter(
                list(element + 1 for element in list(range(df.shape[1]))),
                df.iloc[index],
                label=legend_label + f'{i}' if legend_label else None,
            )
    elif isinstance(filter, (int, list, tuple)): #Specific fiber filtering
        if isinstance(filter, int):
            fibers = [filter]
        else:
            fibers = filter
        for fiber in fibers:
            plt.scatter(
            list(element + 1 for element in list(range(df.shape[1]))),
            df.iloc[fiber-1],
            label=legend_label + f'{fiber}' if legend_label else None,
            )
    plt.title(title) if title else None
    plt.xlabel(xlabel) if xlabel else None
    plt.ylabel(ylabel) if ylabel else None
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left') if legend_label else None
    plt.show()

#test script
if __name__ == "__main__":
    df = prepare_data("../data/target.xlsx", filter="MEAS") #Load the output from RyR_Generator into a df
    prepare_database(df, "PASSAT_B9_TOP") #Store a df inside the database of the project
    dbh = db.SQLite_Data_Extractor("database.db") #Connect to the database
    df = dbh.retrieve("PASSAT_B9_TOP") #Get the desired tooling data 

