import openpyxl as opxl #Read and write in xlsx
import pandas as pd #Import from csv and manipulate data
import numpy as np
import tkinter as tk
import tkinter.filedialog
from tkinter import messagebox
import inspect as ins
import os
##Tk and directory configuration
Root = tk.Tk()
Root.withdraw()
messagebox.showinfo("Importar", "Selecciona la carpeta que contiene los archivos de reporte")
source_dirname = tk.filedialog.askdirectory()
if source_dirname == "":
    exit()
messagebox.showinfo("Exportar", "Selecciona la hoja de calculo que va a generar el reporte")
target_dirname = tk.filedialog.askopenfilename()
if target_dirname == "":
    exit()
specific_rows = [4, 5, 6, 7, 8, 9]
## Helper Functions
#Filters each nest reports by reading a substring
def nest_filter(source_dirname, substring):
    file_list = os.listdir(source_dirname)
    filtered_list = [filename for filename in file_list if substring in filename]
    return filtered_list
#Creates a zeros np array to hold the values of every nest
def ndallocator(nest):
    size = enumerate(nest)
    size = len(list(size))
    data = np.zeros([len(specific_rows), size])
    return data
#Writes over the array column bu column
def writer(nest, data):
    for i, filename in enumerate(nest):
        Source = pd.read_csv(source_dirname + "/" + nest[i], skiprows = lambda x: x not in specific_rows, header=None) #Open the csv and build a Dataframe with the target rows
        Text = Source.iloc[:, 2] #Indexes the test name column
        MEAS = Source.iloc[:, 3] #Indexes the measure column
        lo_limit = Source.iloc[:, 4] #Indexes the low limit value
        hi_limit = Source.iloc[:, 5] #Indexes the high limit value
        data[:, i] = MEAS #Writes the column on the array  
    Output = pd.DataFrame(data) #Makes a new Dataframe with the completed array
    Output = pd.concat([Text, Output, lo_limit, hi_limit], axis=1)
    return Output
#Concatenates the data frames for each next
def compiler(Output_S1, Output_S2, Output_S3, Output_S4):
    Final = pd.concat([Output_S1, Output_S2, Output_S3, Output_S4])
    return Final
## Code execution per nest
#Nest 1
S1 = nest_filter(source_dirname, "S1")
data = ndallocator(S1)
Output = writer(S1, data)
Output_S1 = Output
#Nest 2
S2 = nest_filter(source_dirname, "S2")
data = ndallocator(S2)
Output = writer(S2, data)
Output_S2 = Output
#Nest 3
S3 = nest_filter(source_dirname, "S3")
data = ndallocator(S3)
Output = writer(S3, data)
Output_S3 = Output
#Nest 4
S4 = nest_filter(source_dirname, "S4")
data = ndallocator(S4)
Output = writer(S4, data)
Output_S4 = Output
## Data export
Final = compiler(Output_S1, Output_S2, Output_S3, Output_S4) #Concatenates all the nests data
Final.to_excel(target_dirname, index=False, startrow=3, startcol=0, header=None) #Writes the values in the excel file
os.startfile(target_dirname) #Opens the file for review

