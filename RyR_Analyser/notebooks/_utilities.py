import pandas as pd
import sqlite3
import sys
sys.path.append("../tools/")
import _db_tools as db

def prepare_data(target):
    data = pd.read_excel(target) #Import the RyR generator output
    df = data.iloc[2:, 1:-2] #Slices the measures
    df.reset_index(drop=True, inplace=True) #Reset rows index
    df.columns = range(df.shape[1]) #Reset columns index
    dbh.store_df(df, "measures") #Store the dataframe in the connected database
    dbh.consult_tables() #Checks results

#test script
if __name__ == "__main__":
    dbh = db.SQLite_Data_Extractor("database.db")
    prepare_data("../data/target.xlsx")


test = [0, 1, 2]

test = [test]