import tkinter as tk
import tkinter.filedialog
from functions import askdirectory, asktarget

root = tk.Tk()

# create a frame for the widgets
frame = tk.Frame(root, width=300, height=200, bg='white')
frame.pack()

# create the button to select the reports folder and the associated text label
button1 = tk.Button(frame, text='Button 1', command=lambda: askdirectory(text1))
button1.grid(row=0, column=0, padx=5, pady=5)

text1 = tk.Entry(frame)
text1.grid(row=1, column=0, padx=50, pady=5)

# create the button to select the target file and the associated text label
button2 = tk.Button(frame, text='Button 2', command=lambda: asktarget(text2))
button2.grid(row=2, column=0, padx=5, pady=5)

text2 = tk.Entry(frame)
text2.grid(row=3, column=0, padx=50, pady=5)

# create a drop-down list to select the number of nests
options = ['Two nests', 'Four nests']
selected_option = tk.StringVar()
selected_option.set(options[0]) # set the default option
combo_box = tk.OptionMenu(frame, selected_option, *options)
combo_box.grid(row=4, column=0, padx=5, pady=5)



root.mainloop()