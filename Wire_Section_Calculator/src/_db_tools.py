import pandas as pd
import sqlite3
import os
#Secondary requirements: pip install openpyxl

class SQlite_Data_Extractor:
    '''Extracts structured data from different sources and turn it into a table in a database for quick deployment'''
    def __init__(self, source_name, db_name):
        self.source_path = "../references/" + source_name
        self.db_path = "../database/" + db_name
        self.df = None
        self.conn = None
        if os.path.exists(self.db_path): #Preventive connection to an existing base
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
    def table_from_source(self):
        '''Creates a db connection and a table of the given name using data for different sources'''
        extension = self.source_path.split(".")[-1] #Gets the extension of the file
        match extension:
            case "xlsx":
                try:
                    self.df = pd.read_excel(self.source_path, sheet_name=None)
                except Exception as e:
                    raise Exception(f"Error importing data into pandas: {str(e)}")
                self._datasheet()
            case "csv":
                try:
                    self.df = pd.read_csv(self.source_path, sheet_name=None)
                except Exception as e:
                    raise Exception(f"Error importing data into pandas: {str(e)}")
                self._datasheet()
            case other:
                raise Exception(f"Unsupported file format")
    def add_table(self, table_name):
        '''Adds a new table without touching the rest of the database'''
        try:
            if not self.conn:
                raise Exception("Database connection is not established.")
            print(f'Data from {self.source_path} has been imported into the *{table_name}* table in {self.db_path}.')
        except Exception as e:
            raise Exception(f"Error creating table in database: {str(e)}")
    def rename_table(self, og_table_name):
        ...
    def consult_tables(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        for table in tables:
            print(table)
    def examine_table(self, table_name):
        self.table_name = table_name
        cursor = self.conn.cursor()
        cursor.execute(f"SELECT * FROM {table_name};")
        rows = cursor.fetchall()
        for row in rows:
            print(row)
    def close_conn(self):
        self.conn.close()  #Close the database connection when done
    def clear_database(self, db_name):
        self.db_path = "../database/" + db_name
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';") #Get a list of all tables in the database
            tables = cursor.fetchall()
            print("Warning: This action will clear all data from the database.")
            confirmation = input("Do you want to continue? (y/n): ").strip().lower()
            if confirmation == 'y':
                # Loop through the tables and delete them
                for table in tables:
                    table_name = table[0]
                    cursor.execute(f"DROP TABLE IF EXISTS {table_name};")
                conn.commit()
                conn.close()
                print("Database cleared successfully.")
            else:
                print("Operation canceled.")
        except Exception as e:
            print(f"Error clearing the database: {str(e)}")
    '''Internal methods'''
    def _datasheet(self):
        try:
            self.conn = sqlite3.connect(self.db_path)  # Will create the db if it doesn't exist
            print(f'Data from {self.source_path} has been imported in {self.db_path}.')
            print(f"Sheet(s) imported to db as table(s) with name(s):")
            for sheet_name, sheet in self.df.items():
                print(f"{sheet_name}s")
                if not sheet_name.isalnum():
                    raise Exception(f"Invalid table name for sheet: {sheet_name}")
                table_name = sheet_name
                sheet.to_sql(table_name, self.conn, if_exists='replace', index=False)
        except Exception as e:
            raise Exception(f"Error connecting to database: {str(e)}")

#Test script
if __name__ == '__main__':
    dbh = SQlite_Data_Extractor("awg_sections.xlsx", "lookup_table.db")
    dbh.table_from_source()
    dbh.consult_tables()
    dbh.examine_table("test")
    dbh.close_conn()
    
    ###WARNING###
    dbh.clear_database("lookup_table.db")



