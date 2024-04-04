import os, sys
import db_connection._db_tools as dbt

RyR_data = dbt.SQLite_Data_Extractor("RyR_data.db", rel_path="../../../5_Database")
RyR_backup = dbt.SQLite_Backup("RyR_data.db", rel_path="../../../5_Database", backup_folder="../../../5_Database/backup", backup_time=86400)

def do_backup(db_name):
    RyR_backup.reconnect(db_name)
    RyR_backup.manual_backup()
    RyR_backup.close_conn()

def store_actual(df_name, db_name, data):
    do_backup(db_name)
    RyR_data.reconnect(db_name)
    RyR_data.store_df(data, table_name=df_name)
    RyR_data.close_conn()

def store_all(db_name, input_directory):
    do_backup(db_name)
    RyR_data.reconnect(db_name)
    RyR_data.store_directory(input_rel_path=input_directory)
    RyR_data.close_conn()

def generate_checkpoint(db_name):
    RyR_backup.reconnect(db_name)
    RyR_backup.create_checkpoint()
    RyR_backup.close_conn()

#Test script
if __name__ == "__main__":
    store_all("../../3_Results")

    RyR_data.consult_tables()

    RyR_data.clear_database()
    
    RyR_backup.check_backup("RyR_data.db")
