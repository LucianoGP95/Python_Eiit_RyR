#% pip install openpyxl
import os, re, configparser
import pandas as pd
import numpy as np
from globals import glob
from utilities_database import prepare_data, prepare_database, consult_database, clear_databases, retrieve_data, rename_index, get_date, get_sigma, rename_limits_table
from utilities_analysis import mean_calculator, limits_generator, ini_generator_personalized, RyR, z_score_filter, reset_df
from utilities_plotting import plot_scatter
import _db_tools as db
import pandas as pd
from globals import glob
import matplotlib.pyplot as plt

os.chdir(os.path.dirname(os.path.realpath(__file__)))  ####Delete after debugging

def ini_generator(limits: pd.DataFrame, lenses_per_nest: int) -> None:
    '''Generates an ini file with personalized limits for every mean.
    Parameters:
    - limits (pd.DataFrame): DataFrame containing the personalized limits for each mean.
        The DataFrame is expected to have two columns, where the first column represents
        the lower limit and the second column represents the upper limit.
    - lenses_per_nest (int): Number of lenses per nest. Should be 3 or 4.
    Raises:
    ValueError: If lenses_per_nest is neither 3 nor 4.
    The function reads a template .ini file based on the lenses_per_nest parameter,
    updates the limits in the template with the provided limits DataFrame, and
    saves the modified data to a new .ini file.
    Example:
    >>> import pandas as pd
    >>> limits_data = {'LO_LIMIT': [10, 15, 20], 'HI_LIMIT': [30, 35, 40]}
    >>> limits_df = pd.DataFrame(limits_data)
    >>> ini_generator(limits_df, 3)
    '''
    class CaseSensitiveConfigParser(configparser.ConfigParser):
        '''
        A custom class to override optionxform and avoid uppercases being converted to lowercases.
        '''
        def optionxform(self, optionstr):
            return optionstr
    config = CaseSensitiveConfigParser()
    #Import a template based on the number of lenses per nest
    if lenses_per_nest == 3:
        config.read('../data/template_12_fibers.ini')
    elif lenses_per_nest == 4:
        config.read('../data/template_16_fibers.ini')
    else:
        raise ValueError("lenses_per_nest should be 3 or 4.")
    keys_list = []
    #Get a keys list with the correct uppercased keys
    for section_name in config.sections():
        section = config[section_name]
        keys_list.extend(section.keys())
    HI_LIMIT = limits.iloc[:, 1]
    LO_LIMIT = limits.iloc[:, 0]
    #Iterate through the sections and options in the .ini file
    for section in config.sections():
        keys_list = list(config[section].keys())
        j = 0
        for i in range(0, len(keys_list), 2):
            key1 = keys_list[i]
            key2 = keys_list[i + 1]
            col1 = str(limits.iloc[j, 1])
            col2 = str(limits.iloc[j, 0])
            j += 1
            config[section][key1] = col1
            config[section][key2] = col2
    #Print the five first elements of the .ini for a quick check
    for section in config.sections():
        print(f"[{section}]")
        i = 0
        for key, value in config.items(section):
            if i < 5:
                print(f"{key} = {value}")
                i += 1
            else:
                break
        print("...")
    #Save the modified data to a new .ini file
    save_path = os.path.abspath(f'../a2_output/{glob.tooling}.ini')
    with open(save_path, 'w') as configfile:
        for section in config.sections():
            configfile.write(f"[{section}]\n")
            keys = keys_list  #Recover the original keys to write them in the .ini file
            for i, key in enumerate(keys):
                configfile.write(f"{key} = {config[section][key]}\n")
                if (i + 1) % 4 == 0 and i < len(keys) - 1:  #Insert a blank line every four keys
                    configfile.write("\n")

limits_data = {'LO_LIMIT': [10, 15, 20], 'HI_LIMIT': [30, 35, 40]}
limits_df = pd.DataFrame(limits_data)
ini_generator(limits_df, 3)

import ipywidgets as widgets
from IPython.display import display, Javascript

# Create a SelectMultiple widget
options = ['Option 1', 'Option 2', 'Option 3', 'Option 4']
select_multiple = widgets.SelectMultiple(options=options, layout={'width': '200px'})

# Create a custom JavaScript callback to handle right-click events
javascript_code = """
document.addEventListener('DOMContentLoaded', function() {
    var items = document.getElementsByClassName('p-SelectMultiple-option');
    
    Array.from(items).forEach(function(item) {
        item.addEventListener('contextmenu', function(event) {
            event.preventDefault();
            
            // Toggle the 'selected' class to simulate deselection
            if (item.classList.contains('selected')) {
                item.classList.remove('selected');
            } else {
                item.classList.add('selected');
            }
            
            // Trigger the change event to update the widget's value
            var widgetId = item.closest('.widget-select-multiple').id;
            var widget = document.getElementById(widgetId);
            widget.value = Array.from(widget.getElementsByClassName('selected')).map(function(selectedItem) {
                return parseInt(selectedItem.dataset.value);
            });
            widget.dispatchEvent(new Event('change'));
        });
    });
});
"""

# Display the JavaScript code using IPython's Javascript class
display(Javascript(javascript_code))

# Display the widget
display(select_multiple)

print(select_multiple.value)

string_list = ["Temperature measurements", "Pressure data", "Wind speed measurements", "Humidity readings"]

matching_string = next((string for string in string_list if "hello" in string), None)

if matching_string is not None and "measurements" in matching_string:
    print(f"The string containing 'measurements' is: {matching_string}")
else:
    print("No string contains the substring 'measurements'")


import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Replace this with your actual data
data = {
    'Guia_Luz_Blanco_FB1_X': [0.3226, 0.3225, 0.3225, 0.3225, 0.3223, 0.3223, 0.3223, 0.3221, 0.3222, 0.3222, 0.3222, 0.3220, 0.3222, 0.3221, 0.3221, 0.3220, 0.3221, 0.3221, 0.3222, 0.3223, 0.3222, 0.3222, 0.3222, 0.3221, 0.3221, 0.3222, 0.3222, 0.3221, 0.3221, 0.3222],
    'Guia_Luz_Blanco_FB1_Y': [0.3457, 0.3455, 0.3455, 0.3455, 0.3454, 0.3454, 0.3454, 0.3451, 0.3452, 0.3452, 0.3452, 0.3451, 0.3452, 0.3452, 0.3451, 0.3451, 0.3452, 0.3452, 0.3452, 0.3453, 0.3452, 0.3452, 0.3452, 0.3452, 0.3452, 0.3452, 0.3452, 0.3452, 0.3452, 0.3452],
    'Guia_Luz_Blanco_FB2_X': [0.3274, 0.3273, 0.3272, 0.3272, 0.3271, 0.3272, 0.3271, 0.3270, 0.3270, 0.3270, 0.3269, 0.3268, 0.3268, 0.3268, 0.3268, 0.3269, 0.3268, 0.3268, 0.3269, 0.3269, 0.3268, 0.3268, 0.3268, 0.3268, 0.3268, 0.3267, 0.3269, 0.3268, 0.3268, 0.3268],
    'Guia_Luz_Blanco_FB2_Y': [0.3490, 0.3490, 0.3489, 0.3489, 0.3489, 0.3489, 0.3488, 0.3487, 0.3487, 0.3487, 0.3486, 0.3486, 0.3486, 0.3486, 0.3486, 0.3486, 0.3485, 0.3486, 0.3486, 0.3486, 0.3486, 0.3485, 0.3486, 0.3485, 0.3485, 0.3485, 0.3486, 0.3485, 0.3485, 0.3485],
    'Guia_Luz_Blanco_FB3_X': [0.3239, 0.3239, 0.3238, 0.3238, 0.3238, 0.3238, 0.3237, 0.3236, 0.3235, 0.3237, 0.3237, 0.3235, 0.3236, 0.3236, 0.3236, 0.3235, 0.3235, 0.3235, 0.3236, 0.3236, 0.3235, 0.3235, 0.3236, 0.3236, 0.3237, 0.3237, 0.3236, 0.3237, 0.3236, 0.3236],
    'Guia_Luz_Blanco_FB3_Y': [0.3450, 0.3450, 0.3449, 0.3449, 0.3449, 0.3449, 0.3448, 0.3447, 0.3447, 0.3448, 0.3448, 0.3447, 0.3447, 0.3447, 0.3447, 0.3448, 0.3448, 0.3447, 0.3449, 0.3449, 0.3446, 0.3447, 0.3447, 0.3447, 0.3448, 0.3448, 0.3448, 0.3447, 0.3447, 0.3447],
    'Guia_Luz_Blanco_FB4_X': [0.3268, 0.3268, 0.3267, 0.3267, 0.3268, 0.3266, 0.3267, 0.3266, 0.3266, 0.3265, 0.3265, 0.3266, 0.3265, 0.3265, 0.3264, 0.3265, 0.3265, 0.3264, 0.3265, 0.3265, 0.3265, 0.3264, 0.3265, 0.3264, 0.3264, 0.3264, 0.3264, 0.3264, 0.3263, 0.3263],
    'Guia_Luz_Blanco_FB4_Y': [0.3502, 0.3501, 0.3501, 0.3501, 0.3501, 0.3500, 0.3500, 0.3500, 0.3499, 0.3499, 0.3499, 0.3499, 0.3499, 0.3498, 0.3498, 0.3498, 0.3498, 0.3498, 0.3499, 0.3498, 0.3498, 0.3498, 0.3498, 0.3498, 0.3498, 0.3498, 0.3498, 0.3498, 0.3497, 0.3497],
    # ... Add other columns as needed
}

# Create a DataFrame
df = pd.DataFrame(data)

# Transpose the DataFrame
df_transposed = df.transpose()

# Rename the columns
df_transposed.columns = [f'Test {i}' for i in range(1, df_transposed.shape[1] + 1)]

# Plot the boxplot
plt.figure(figsize=(12, 6))
sns.boxplot(data=df_transposed, orient='v', palette='Set3')
plt.title('Boxplot of Measurements')
plt.xlabel('Test Number')
plt.ylabel('Measurement Value')
plt.show()

display(df_transposed)

import pandas as pd
import matplotlib.pyplot as plt
import pdfkit

# Create a sample DataFrame
data = {'Name': ['John', 'Alice', 'Bob'],
        'Age': [25, 30, 22],
        'City': ['New York', 'San Francisco', 'Seattle']}
df = pd.DataFrame(data)

# Plot DataFrame as a table
fig, ax = plt.subplots(figsize=(8, 4)) 
ax.axis('tight')
ax.axis('off')
ax.table(cellText=df.values, colLabels=df.columns, cellLoc = 'center', loc='center')

# Save the plot as an image
plt.savefig('table.png')

# Convert the image to PDF using pdfkit
pdfkit.from_file('table.png', 'output.pdf')

# Optionally, you can remove the temporary image file
import os
os.remove('table.png')

import pandas as pd

# Example DataFrame
data = {'A': [1, 2, 3], 'B': [4, 5, 6]}
df = pd.DataFrame(data, index=['X', 'Y', 'Z'])

# Get the row number (index) for a specific index label
index_label = 'Y'
row_number = df.index.get_loc(index_label)

print(f"The row number for index label '{index_label}' is: {row_number}")


import sqlite3
import pandas as pd
# Replace 'your_database.db' with the desired SQLite database file name
db_file = 'your_database.db'
# Sample data
data = {
    'Tooling name': ['MID_GOLF_PA'],
    'Lenses per nest': ['3'],
    'number of nests': ['4'],
    'x-axis tolerance': ['0.0125'],
    'y-axis tolerance': ['0.0165'],
    'lower tolerance': ['0.02'],
    'higher tolerance': ['0.03']
}
# Create a DataFrame
df = pd.DataFrame(data)
# Create a connection to the SQLite database
conn = sqlite3.connect(db_file)
# Create a cursor object to execute SQL queries
cursor = conn.cursor()
# Define the table creation query
table_creation_query = '''
CREATE TABLE IF NOT EXISTS your_table_name (
    "index" INTEGER PRIMARY KEY AUTOINCREMENT,
    "Tooling name" TEXT,
    "Lenses per nest" TEXT,
    "number of nests" TEXT,
    "x-axis tolerance" TEXT,
    "y-axis tolerance" TEXT,
    "lower tolerance" TEXT,
    "higher tolerance" TEXT
);
'''
# Execute the table creation query
cursor.execute(table_creation_query)
# Insert the data into the table
df.to_sql('your_table_name', conn, if_exists='replace', index=False)
display(df.transpose())
query = f"SELECT * FROM 'your_table_name'"
df = pd.read_sql(query, conn, index_col=None)
# Commit the changes and close the connection
conn.commit()
conn.close()
# Display the resulting DataFrame
display(df.transpose())

import seaborn as sns
import matplotlib.pyplot as plt

# Example data
tips = sns.load_dataset("tips")

# Vertical box plot
sns.boxplot(x="day", y="total_bill", data=tips, orient='v')
plt.show()

# Horizontal box plot
sns.boxplot(x="total_bill", y="day", data=tips, orient='h')
plt.show()



