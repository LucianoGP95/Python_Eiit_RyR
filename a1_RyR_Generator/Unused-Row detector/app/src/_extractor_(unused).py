import os
import numpy as np
import pandas as pd
import sys
sys.path.append("../tools/")
import _db_tools

substrings = 4
first_row = 5
last_row = 10
specific_rows = last_row - first_row

def import_to_db(source_directory, database_name):
    for nest in range(substrings):
        nest = "S" + str(nest+1)
        nest_list = nest_filter(source_directory, nest)
        preallocated = ndallocator(nest_list)
        writer(nest_list, preallocated, source_directory)
"""     dbh = _db_tools.SQLite_Data_Extractor(database_name) 
    dbh.store_directory(source_directory)
    dbh.consult_tables() """

def nest_filter(source_dirname, substring):
    '''Filters each nest reports by reading a substring in the filename'''
    file_list = os.listdir(source_dirname)
    filtered_list = [filename for filename in file_list if substring in filename]
    return filtered_list

def ndallocator(nest):
    '''Allocates an empty ndarray of the size needed to hold the values of every nest'''
    size = enumerate(nest)
    size = len(list(size))
    preallocated = np.zeros([len(specific_rows), size])
    return preallocated

def writer(nest, data, source_dirname):
    '''Writes over the array column by column'''
    for i, filename in enumerate(nest):
        Source = pd.read_csv(source_dirname + "/" + nest[i], skiprows = lambda x: x not in specific_rows, header=None) #Open the csv and build a Dataframe with the target rows
        Text = Source.iloc[:, 2] #Indexes the test name column
        MEAS = np.zeros(len(specific_rows))
        for j in range(data.shape[0]):
            try:
                MEAS[j] = float(Source.iloc[j, 3])
            except (ValueError, TypeError):
                MEAS[j] = 0.0
        lo_limit = Source.iloc[:, 4] #Indexes the low limit value
        hi_limit = Source.iloc[:, 5] #Indexes the high limit value
        data[:, i] = MEAS #Writes the column on the array  
    Output = pd.DataFrame(data) #Makes a new Dataframe with the completed array
    Output = pd.concat([Text, Output, lo_limit, hi_limit], axis=1)
    return Output

#test script
if __name__ == "__main__":
    import_to_db("../1_Place_Reports_Here/", "database.db")

import os
import numpy as np
import pandas as pd
import sys
sys.path.append("../tools/")
import _db_tools

dbh = _db_tools.SQLite_Data_Extractor("database.db") 
dbh.store("PASSAT_B9_20230929_13h35m07s_S1_P.csv")
dbh.consult_tables()