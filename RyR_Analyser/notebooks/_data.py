import pandas as pd
import sqlite3
import sys
sys.path.append("../tools/")
import _db_tools as db

def prepare_data(target):
    data = pd.read_excel(target)
    df = data.iloc[2:, 1:-2]
    df.reset_index(drop=True, inplace=True)
    dbh.store_df(df, "measures")
    dbh.consult_tables()
    dbh.close_conn()

dbh = db.SQLite_Data_Extractor("database.db")
prepare_data("../data/target.xlsx")

