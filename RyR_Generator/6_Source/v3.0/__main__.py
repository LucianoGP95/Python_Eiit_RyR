import tkinter as tk
import tkinter.filedialog
from _functions import nest_number, update_frow, update_lrow

source_dirname = ""
target_dirname = ""

def validate_numeric_input(value):
    if value.isdigit():
        return True
    else:
        return False

def askdirectory(text_field):
    global source_dirname
    source_dirname = tk.filedialog.askdirectory()
    text_field.delete(0, tk.END)
    text_field.insert(0, source_dirname)
    return source_dirname

def asktarget(text_field):
    global target_dirname 
    target_dirname = tk.filedialog.askopenfilename()
    text_field.delete(0, tk.END)
    text_field.insert(0, target_dirname)
    return target_dirname

def update_Go():
    if source_dirname != "" and target_dirname != "" and selected_option.get() != options[0]:
        button3.configure(state='normal')
    else:
        button3.configure(state='disabled')

root = tk.Tk()

# create a frame for the widgets
frame = tk.Frame(root, width=800, height=200, bg='white')
frame.pack()

# create the button to select the reports folder and the associated text label
button1 = tk.Button(frame, text='Reports folder', command=lambda: askdirectory(text1))
button1.grid(row=0, column=0, padx=5, pady=5)

text1 = tk.Entry(frame, width=100)
text1.grid(row=1, column=0, padx=50, pady=5)

# create the button to select the target file and the associated text label
button2 = tk.Button(frame, text='Target file', command=lambda: asktarget(text2))
button2.grid(row=2, column=0, padx=5, pady=5)

text2 = tk.Entry(frame, width=100)
text2.grid(row=3, column=0, padx=50, pady=5)

# create entries to select the first and last row
validation = root.register(validate_numeric_input) #Restricts the input value to a number
label1 = tk.Label(frame, text="First row:")
label1.grid(row=4, column=0, padx=50, pady=5)
first_r = tk.Entry(frame, width=5, validate="key", validatecommand=(validation, '%P'))
first_r.insert(0, 5) #Initial Value
first_r.grid(row=5, column=0, padx=50, pady=5)
first_r.bind("<KeyRelease>", lambda event: update_frow(event, first_r),) #Bind update of the number with an update function

label2 = tk.Label(frame, text="Last row:")
label2.grid(row=6, column=0, padx=50, pady=5)
last_r = tk.Entry(frame, width=5, validate="key", validatecommand=(validation, '%P'))
last_r.insert(0, 18) #Initial Value
last_r.grid(row=7, column=0, padx=50, pady=5)
last_r.bind("<KeyRelease>", lambda event: update_lrow(event, last_r)) #Bind update of the number with an update function

# create a drop-down list to select the number of nests
options = ['Select nests', 'Two nests', 'Four nests']
selected_option = tk.StringVar()
selected_option.set(options[0]) # set the default option
combo_box = tk.OptionMenu(frame, selected_option, *options)
combo_box.grid(row=8, column=0, padx=5, pady=5)

# create the button to realize the extraction
button3 = tk.Button(frame, text='Go', command=lambda: nest_number(selected_option, options, source_dirname, target_dirname), state='disabled')
button3.grid(row=9, column=0, padx=5, pady=5)

# Bind different actions to activate or deactivate the Go button if conditions ar met
text1.bind("<KeyRelease>", lambda event: update_Go())
text2.bind("<KeyRelease>", lambda event: update_Go())
selected_option.trace_add('write', lambda *args: update_Go()) #Dropdown menu using traces


root.mainloop()