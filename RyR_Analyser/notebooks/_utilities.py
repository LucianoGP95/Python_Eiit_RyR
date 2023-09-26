import pandas as pd
import sqlite3
import sys
sys.path.append("../tools/")
import _db_tools as db

#Helper functions
def prepare_data(target):
    '''Prepares the output data by extracting the measures in a df and storing them in the database'''
    data = pd.read_excel(target) #Import the RyR generator output
    df = data.iloc[2:, 1:-2] #Slices the measures
    df.reset_index(drop=True, inplace=True) #Reset rows index
    df.columns = range(df.shape[1]) #Reset columns index
    return df

def prepare_database(df, table_name):
    '''Prepares the database from a ready-to-store df and returns the same df, getting it from the db'''
    dbh = db.SQLite_Data_Extractor("database.db") #Allows for database management
    dbh.store_df(df, table_name) #Store the dataframe in the connected database
    dbh.consult_tables() #Checks results
    dbh.close_conn()

#test script
if __name__ == "__main__":
    prepare_data("../data/target.xlsx")

