import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import os
from _core import nest_number, update_frow, update_lrow, row_auto_updater
# Helper functions
source_dirname = ""
target_dirname = ""

def validate_numeric_input(value):
    '''Ensure input values for rows are always numeric'''
    if value.isdigit():
        return True
    else:
        return False

def askdirectory(text_field):
    '''Opens a dialog window to select the source directory and auto updates the rows'''
    global source_dirname
    source_dirname = filedialog.askdirectory()
    text_field.delete(0, tk.END)
    text_field.insert(0, source_dirname)
    frow, lrow = row_auto_updater(source_dirname)
    first_r.insert(0, frow)
    last_r.insert(0, lrow)
    return source_dirname

def asktarget(text_field):
    '''Opens a dialog window to select the target excel file'''
    global target_dirname 
    target_dirname = filedialog.askopenfilename()
    text_field.delete(0, tk.END)
    text_field.insert(0, target_dirname)
    return target_dirname

def update_Go():
    '''Opens a dialog window to select the target excel file'''
    if source_dirname != "" and target_dirname != "" and selected_option.get() != options[0]:
        button3.configure(state='normal')
    else:
        button3.configure(state='disabled')

###UI Design
##Main window creation
root = tk.Tk()
root.title("RyR Generator")
frame = ttk.Frame(root, width=800, height=200)
frame.grid(column=0, row=0, padx=10, pady=10, sticky="nsew")
##Widgets creation
#Create the button to select the reports folder and the associated text label
button1 = ttk.Button(frame, text='Reports folder', command=lambda: askdirectory(text1))
button1.grid(row=0, column=0, padx=5, pady=5)
text1 = ttk.Entry(frame, width=100)
text1.grid(row=1, column=0, padx=50, pady=5)

#Create the button to select the target file and the associated text label
button2 = ttk.Button(frame, text='Target file', command=lambda: asktarget(text2))
button2.grid(row=2, column=0, padx=5, pady=5)
text2 = ttk.Entry(frame, width=100)
text2.grid(row=3, column=0, padx=50, pady=5)

#Create entries to select the first and last row
validation = root.register(validate_numeric_input)  #Restricts the input value to a number
label1 = ttk.Label(frame, text="First row:")
label1.grid(row=4, column=0, padx=50, pady=0)
first_r = ttk.Entry(frame, width=5, validate="key", validatecommand=(validation, '%P'))
first_r.insert(0, 5)  #Initial Value
first_r.grid(row=5, column=0, padx=50, pady=5)
first_r.bind("<KeyRelease>", lambda event: update_frow(event, first_r))  #Bind update of the number with an update function

label2 = ttk.Label(frame, text="Last row:")
label2.grid(row=6, column=0, padx=50, pady=0)
last_r = ttk.Entry(frame, width=5, validate="key", validatecommand=(validation, '%P'))
last_r.insert(0, 10)  #Initial Value
last_r.grid(row=7, column=0, padx=50, pady=5)
last_r.bind("<KeyRelease>", lambda event: update_lrow(event, last_r))  # Bind update of the number with an update function

#Create a drop-down list to select the number of nests
options = ['Select nests', 'All nests', 'Two nests', 'Four nests']
selected_option = tk.StringVar()  #Create an instance of the stringVar class that will hold the selected option
selected_option.set(options[0])  #Set the default option
combo_box = ttk.Combobox(frame, textvariable=selected_option, values=options)
combo_box.grid(row=8, column=0, padx=5, pady=5)

#Create the button to realize the extraction
button3 = ttk.Button(frame, text='Go', command=lambda: nest_number(selected_option, options, source_dirname, target_dirname, source_dirname), state='disabled')
button3.grid(row=9, column=0, padx=5, pady=5)

#Bind different actions to activate or deactivate the Go button if conditions ar met
text1.bind("<KeyRelease>", lambda event: update_Go())
text2.bind("<KeyRelease>", lambda event: update_Go())
selected_option.trace_add('write', lambda *args: update_Go())  # Dropdown menu using traces

root.mainloop()