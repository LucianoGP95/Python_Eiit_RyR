import os, sys, time
import pandas as pd
from globals import glob
import _db_tools as db

###Script
dbh_i = db.SQLite_Data_Extractor("input.db") #Allows for database management
dbh_o = db.SQLite_Data_Extractor("output.db")

###Helper functions
def prepare_database(db_name: str, df: pd.DataFrame, table_name: str, extra_term=None, add_index=False) -> str:
    '''Prepares the database from a ready-to-store df and returns the table name, getting it from the db'''
    _select_database(db_name)
    dbh.reconnect(db_name, verbose=False)
    dbh.set_rules(add_index=add_index) if add_index == True else None
    if extra_term is not None and isinstance(extra_term, str): #Renames files with the extra term 
        old_name = table_name
        parts = old_name.split("_")
        first_part = parts[:-6]
        date = parts[-6:]
        table_name = first_part + [extra_term] + date
        new_name = "_".join(table_name)
        dbh.rename_table(old_name, new_name, verbose=False)
        table_name = new_name
    dbh.store_df(df, table_name) #Store the dataframe in the connected database
    dbh.close_conn(verbose=False)
    return table_name

def consult_database(db_name: str, filter :str=None, verbose: bool=False) -> list[str]:
    _select_database(db_name)
    dbh.reconnect(db_name, verbose=False)
    table_list = dbh.consult_tables(filter=filter, verbose=verbose)
    dbh.close_conn(verbose=False)
    return table_list

def clear_databases(db_name: list[str]):
    '''Clears the specified databases'''
    db_name = [db_name] if isinstance(db_name,str) else db_name #Handle strings input
    confirmation = input(f"Warning: This action will clear all data from the databasesy.\nDo you want to continue? (y/n): ").strip().lower()
    if confirmation == 'y':
        for database in db_name:
            _select_database(database)
            dbh.reconnect(database, verbose=False)
            dbh.clear_database(override=True)
        dbh.close_conn(verbose=False) 

def retrieve_data(db_name: str, table_name: str) -> pd.DataFrame:
    _select_database(db_name)
    dbh.reconnect(db_name, verbose=False)
    df = None
    if isinstance(table_name, str):
        df = dbh.retrieve(table_name)
    dbh.close_conn(verbose=False) 
    return df if isinstance(df, pd.DataFrame) else None

def rename_table(db_name, old_name, new_name, extra_term=None):
    _select_database(db_name)
    dbh.reconnect(db_name, verbose=False)
    dbh.rename_table(old_name, new_name, verbose=False)
    dbh.close_conn(verbose=False) 

def show_table(db_name, table_name):
    _select_database(db_name)
    dbh.reconnect(db_name, verbose=False)
    dbh.examine_table([table_name])
    dbh.close_conn(verbose=False) 

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

def rename_limits_table(db_name: str, old_name: str) -> str:
    '''Renames a table name by adding a suffix before the date.'''
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

def rename_index(df: pd.DataFrame) -> pd.DataFrame:
    '''Renames the index of a dataframe of any size.'''
    new_index = 0
    for index in range(df.shape[0]):
        old_entry = index
        new_index += 1 if index % 2 == 0 else 0  # Increment new_index only on odd iterations
        axis = "X" if index % 2 == 0 else "Y"
        new_entry = f"Guia_Luz_Blanco_FB{new_index}_{axis}"
        df = df.rename(index={old_entry: new_entry})
    return df

def get_date() -> str:
    '''Gets the current date in a formatted string.
    Returns:
    str: A string representing the current date and time in the format "YYYY-MM-DD_HH-MM-SS".'''
    current_date = time.localtime()
    min = current_date.tm_min; sec = current_date.tm_sec
    day = current_date.tm_mday; hour = current_date.tm_hour
    year = current_date.tm_year; month = current_date.tm_mon
    current_date_format = f"{year}y-{month:02d}m-{day:02d}d_{hour}h-{min:02d}m-{sec:02d}s"
    return current_date_format

def get_sigma(sigma, verbose=False):
    dbhs = db.SQLite_Data_Extractor("sigma_values.db")
    dbhs.reconnect("sigma_values.db", verbose=False)
    dbhs.cursor.execute("""SELECT "Value" FROM sigma WHERE "Sigma" >= ?;""", (sigma,))
    result = dbhs.cursor.fetchone()[0]
    dbhs.close_conn(verbose=False)
    print("sigma value: " + str(result)) if verbose == True else None
    return result

###Hidden functions
def _select_database(db_name):
    '''Selects the desired database to work with based of their names'''
    global dbh
    if db_name == "input.db":
        dbh = dbh_i
    elif db_name == "output.db":
        dbh = dbh_o
    else: 
        raise ValueError("Unsupported database")

###test script
""" if __name__ == "__main__":
    df = prepare_data(os.path.join(os.path.abspath("../data/"), "target.xlsx"), filter="MEAS") #Load the output from RyR_Generator into a df
    prepare_database(df, glob.tooling) #Store a df inside the database of the project
    dbh = db.SQLite_Data_Extractor("database.db") #Connect to the database
    df = dbh.retrieve(glob.tooling) #Get the desired tooling data
    get_sigma(4)
    clear_databases(["input.db", "output.db"]) """