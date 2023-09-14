import pandas as pd
import sqlite3
import os

class dbHandler:
    def __init__(self, source_name, db_name, table_name):
        self.source_path = "../references/" + source_name
        self.db_path = "../database/" + db_name
        self.table_name = table_name
        self.df = None
        self.conn = None
    def table_from_source(self):
        '''Creates a db connection and a table of the given name using data'''
        extension = self.source_path.split(".")[-1]
        match extension:
            case "xlsx":
                self._excel()
            case "csv":
                self._comma_separated_values()
            case other:
                raise Exception(f"Unsupported file format")
        try:
            if not self.conn:
                raise Exception("Database connection is not established.")
            if not self.table_name.isalnum(): #Validate the table_name here, e.g., check for valid characters
                raise Exception("Invalid table name.")
            self.table_name = self.table_name
            self.df.to_sql(self.table_name, self.conn, if_exists='replace', index=False)
            print(f'Data from {self.source_path} has been imported into the *{self.table_name}* table in {self.db_path}.')
            return self.conn
        except Exception as e:
            raise Exception(f"Error creating table in database: {str(e)}")
    def add_table(self, table_name):
        '''Adds a new table without touching the rest of the database'''
        try:
            if not self.conn:
                raise Exception("Database connection is not established.")
            if not table_name.isalnum():             
                raise Exception("Invalid table name.")
            self.df.to_sql(table_name, self.conn, if_exists='replace', index=False)
            print(f'Data from {self.source_path} has been imported into the *{table_name}* table in {self.db_path}.')
        except Exception as e:
            raise Exception(f"Error creating table in database: {str(e)}")
    def consult_tables(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        for table in tables:
            print(table[0])
    def examine_table(self, table_name):
        self.table_name = table_name
        cursor = self.conn.cursor()
        cursor.execute(f"SELECT * FROM {table_name};")
        rows = cursor.fetchall()
        for row in rows:
            print(row)
    '''Internal methods'''
    def _excel(self):
        try:
            self.df = pd.read_excel(self.source_path)
            self.conn = sqlite3.connect(self.db_path)  # Will create the db if it doesn't exist
        except Exception as e:
            raise Exception(f"Error connecting to database: {str(e)}")
    def _comma_separated_values(self):
        try:
            self.df = pd.read_csv(self.source_path)
            self.conn = sqlite3.connect(self.db_path)  # Will create the db if it doesn't exist
        except Exception as e:
            raise Exception(f"Error connecting to database: {str(e)}")

#Test script
if __name__ == '__main__':
    dbh = dbHandler("awg_sections.xlsx", "lookup_table.db", "awg")
    dbh.table_from_source()
    dbh.consult_tables()
    dbh.examine_table('awg')

