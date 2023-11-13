import os, sys
sys.path.append(os.path.abspath("../tools"))
import _db_tools as dbt

dbh = dbt.SQLite_Data_Extractor("RyR_data.db", rel_path="../../5_database")

def store_all(directory):
    dbh.reconnect("RyR_data.db")
    dbh.store(directory)
    dbh.close_conn()

store_all("3_Results")