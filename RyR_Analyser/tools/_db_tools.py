#V1.0 21/09/2023
import pandas as pd
import sqlite3
import os
from urllib.parse import urlparse
#Secondary requirements: pip install openpyxl

class SQLite_Handler:
    '''SQLite custom handler'''
    def __init__(self, db_name):
        self.db_path = "../database/" + db_name
        self.df = None
        self.conn = None
        self.cursor = None
        self.conn = sqlite3.connect(self.db_path) #Preventive connection/creation to the database
        self.cursor = self.conn.cursor()
        if not os.path.exists(self.db_path): 
            print(f"{self.db_path} created.")
        else: 
            print(f"{self.db_path} found.")

    def rename_table(self, old_name, new_name):
        try:
            self.cursor.execute(f"ALTER TABLE {old_name} RENAME TO {new_name};")
            self.conn.commit()
            print(f"Table *{old_name}* renamed to *{new_name}*")
        except Exception as e:
            raise Exception(f"Error while renaming table: {str(e)}")

    def delete_table(self, table_name):
        try:
            print(f"Warning: This action will drop the table {table_name}.")
            confirmation = input("Do you want to continue? (y/n): ").strip().lower()
            if confirmation == 'y':
                self.cursor.execute(f"DROP TABLE {table_name};")
                self.conn.commit()
                print(f"{table_name} dropped successfully.")
                print(f"Table *{table_name}* deleted")
                self.consult_tables()
            else:
                print("Operation canceled.")
        except Exception as e:
            raise Exception(f"Error while deleting table: {str(e)}")

    def consult_tables(self):
        '''Shows all the tables in the database'''
        cursor = self.conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print(f"{self.db_path} actual contents:")
        for table in tables:
            print(f"    {table[0]}")

    def examine_table(self, table_name):
        '''Prints the desired table or tables if given in list or tuple format'''
        if isinstance(table_name, str):
            print(f"table: {table_name}")
            cursor = self.conn.cursor()
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            rows = cursor.fetchone()[0]
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            columns = len(columns)
            print(f"    Rows: {rows}\n    Columns: {columns}")
            cursor.execute(f"SELECT * FROM {table_name};")
            rows = cursor.fetchall()
            for row in rows:
                print(row)
        if isinstance(table_name, (list, tuple)):
            cursor = self.conn.cursor()
            for i, table in enumerate(table_name):
                print(f"table {i+1}: {table}")
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                rows = cursor.fetchone()[0]
                cursor.execute(f"PRAGMA table_info({table})")
                columns = cursor.fetchall()
                columns = len(columns)
                print(f"    Rows: {rows}\n    Columns: {columns}")
                cursor.execute(f"SELECT * FROM {table};")
                rows = cursor.fetchall()
                for row in rows:
                    print(f"    {row}")

    def close_conn(self):
        '''Closes the database connection when done'''
        try:
            self.conn.close()  
            print(f"Closed connection to: {self.db_path}")
        except Exception as e:
            print(f"Error clearing the database: {str(e)}")

    def reconnect(self, *argv):
        '''Connects to the either the same database or other database. *argv[0] holds the new database name'''
        if argv and len(argv) > 0 and argv[0] is not None: #Checks if the new database was passed as an argument
            try:
                self.conn.close() 
            except Exception as e:
                pass
            self.db_path = "../database/" + argv[0]
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
            print(f"Connected to {self.db_path}")
        else:
            try:
                self.conn.close() 
            except Exception as e:
                pass
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
            print(f"Connected to {self.db_path}")

    def clear_database(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';") #Get a list of all tables in the database
            tables = cursor.fetchall()
            print(f"Warning: This action will clear all data from the database {self.db_path}.")
            confirmation = input("Do you want to continue? (y/n): ").strip().lower()
            if confirmation == 'y':
                for table in tables: #Loop through the tables and delete them
                    table_name = table[0]
                    cursor.execute(f"DROP TABLE IF EXISTS {table_name};")
                self.conn.commit()
                print("Database cleared successfully.")
            else:
                print("Operation canceled.")
        except Exception as e:
            print(f"Error clearing the database: {str(e)}")

class SQLite_Data_Extractor(SQLite_Handler):
    '''Extracts structured data from different sources and turns it into a table in a database for quick deployment. Creates a db 
    from raw data or adds tables to it from raw data'''
    def __init__(self, db_name):
        super().__init__(db_name)  #Calls the parent class constructor
        self.source_name = None

    def store(self, source):
        '''Generates table(s) of the given name using data from different sources'''
        self.source_name = source
        self._inputhandler() #Handles the source input format
        for i, source in enumerate(self.source_path):
            self._filetypehandler(source) #Handles the filetype
            if self.extension == "excel":
                self._datasheet_excel(i, source)
            if self.extension == "csv":
                self._datasheet_csv(i, source)
        try: #Incase there is a problem with the parent method
            self.consult_tables()
        except Exception as e:
            pass

    def store_directory(self, *argv):
        '''Generates table(s) for all the compatible files inside the custom directory. If the directory isn't given it uses 
        ../data/'''
        self.source_path = ["../data/" + name for name in os.listdir("../data/")]
        if argv and len(argv) > 0:
            try:
                self.source_path = [argv[0] + name for name in os.listdir(argv[0])]
            except Exception as e:
                print("    Unrecognized directory. Using default one.")
        for i, source in enumerate(self.source_path):
            self._filetypehandler(source) #Handles the filetype
            if self.extension == "excel":
                self._datasheet_excel(i, source)
            if self.extension == "csv":
                self._datasheet_csv(i, source)
        try: #Incase there is a problem with the parent method
            self.consult_tables()
        except Exception as e:
            pass

    def store_df(self, df, table_name):
        '''Stores the desired dataframe as a table in connected the database.'''
        try:
            self.df = df
            self.df.to_sql(table_name, self.conn, if_exists='replace', index=False)
            self.conn.commit()
            print(f"Dataframe stored as {table_name}")
        except Exception as e:
            print(f"Error storing the dataframe: {str(e)}")

    def retrieve(self, table_name):
        '''Retrieves a table from the database as a dataframe object. If the arg. is a list or tuple it will try to concatenate
        all the tables'''
        if isinstance(table_name, str):
            try:
                self.cursor = self.conn.cursor()
                query = f"SELECT * FROM {table_name}"
                self.df = pd.read_sql(query, self.conn)
                print(f"Table {table_name} retrieved succesfully.")
                return self.df
            except Exception as e:
                print(f"Error retrieving table as dataframe: {str(e)}")
                return None
        if isinstance(table_name, (list, tuple)):
            dataframes = []
            for table in table_name:
                try:
                    self.cursor = self.conn.cursor()
                    query = f"SELECT * FROM {table}"
                    df = pd.read_sql(query, self.conn)
                    dataframes.append(df)
                    print(f"Table {table} retrieved succesfully.")
                except Exception as e:
                    print(f"Error retrieving table as dataframe: {str(e)}")
                    return None
            try:
                self.df = pd.concat(dataframes, ignore_index=True)
            except Exception as e:
                print(f"Error concatenating dataframes: {str(e)}")
        return self.df

    def rename_table(self, old_name, new_name):
        super().rename_table(old_name, new_name) 

    def delete_table(self, table_name):
        super().delete_table(table_name)  

    def consult_tables(self):
        super().consult_tables()

    def examine_table(self, table_name):
        super().examine_table(table_name) 

    def close_conn(self):
        super().close_conn()  

    def reconnect(self):
        super().reconnect() 

    def clear_database(self):
        super().clear_database() 

    '''Internal methods'''
    def _inputhandler(self):
        '''Handles variable quantity of elements. It accepts: 
            - A list or tuple indicating the desired files in ../data/
            - A string indicating a single file in ../data/
            - An url with a supported filetype'''
        self.flag = self._is_url(self.source_name) #Determines if the given source is an url
        if self.flag == True: 
            self.source_path = [self.source_name] #Converts the string to list to allow iteration with 1 element.
            print("url detected")
        else:
            if isinstance(self.source_name, str): 
                self.source_path = "../data/" + self.source_name
                self.source_path = [self.source_path] #Converts the string to list to allow iteration with 1 element.
            elif isinstance(self.source_name, (list, tuple)):
                self.source_path = ["../data/" + name for name in self.source_name]
            else:
                raise Exception(f"Error importing data: Data mas be specified in str, list or tuple format") 

    def _filetypehandler(self, source):
        '''Handles all the supported filetypes. Currently supported:
        - .csv
        - .xlsx (Excel)
        - Aun url pointing to a file of the above'''
        self.extension = source.split(".")[-1] #Gets the extension of the file
        match self.extension:
            case "xlsx":
                try:
                    self.df = pd.read_excel(source, sheet_name=None)
                except Exception as e:
                    raise Exception(f"Error importing data into pandas: {str(e)}")
            case "csv":
                try:
                    self.df = pd.read_csv(source, header=None)
                except Exception as e:
                    raise Exception(f"Error importing data into pandas: {str(e)}")
            case _:
                print(f"Unsupported file format: {source}, skipping file.")

    def _datasheet_excel(self, i, source):
        '''Specific method for sending .xlsx files with all their sheets as tables in the db'''
        try:
            print(f'Data from {source} has been imported to {self.db_path}.')
            print(f"Sheet(s) imported to db as table(s) with name(s):")
            for sheet_name, sheet in self.df.items():
                table_name = sheet_name
                if not sheet_name.isalnum(): #Ensures all tables always have legal characters (letters and numbers)
                    table_name = f"table{i+1}"
                    print(f"Invalid table name for sheet: {sheet_name}, adding it as table{i+1}")
                print(f"    {table_name}")
                sheet.to_sql(table_name, self.conn, if_exists='replace', index=False)
        except Exception as e:
            raise Exception(f"Error connecting to database: {str(e)}")

    def _datasheet_csv(self, i, source):
        '''Specific method for sending .csv files as tables in the db'''
        try:
            table_name = source.split(".")[-2].split("/")[-1]
            if not table_name.isalnum(): #Ensures all tables always have legal characters (letters and numbers)
                table_name = f"table{i+1}"
                print(f"Invalid table name: Adding it as table{i+1}")
            print(f'Data from {source} has been imported to {self.db_path}.')
            print(f"    {table_name}")
            self.df.to_sql(table_name, self.conn, if_exists='replace', index=False)
        except Exception as e:
            raise Exception(f"Error connecting to database: {str(e)}")

    def _is_url(self, string):
        '''Determines whether the given argument is an url or not'''
        try:
            result = urlparse(string)
            return all([result.scheme, result.netloc])
        except ValueError:
            return False

###File Structure
#-Project root
#---data (raw data)
#
#---database (database location)
#
#---tools (script location)
#------_db_tools.py
#
###Test script
if __name__ == '__main__':
    dbh = SQLite_Data_Extractor("database.db") 
    dbh.store("data_2.xlsx")
    dbh.consult_tables()
    dbh.examine_table(["test1", "test2"])
    dbh.rename_table("test1", "new_test")
    dbh.retrieve("new_test")
    dbh.close_conn()
    
    ###WARNING zone###
    #Delete a single table
    dbh.delete_table("new_test")
    #Clear the database
    dbh.clear_database()


