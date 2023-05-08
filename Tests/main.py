import tkinter as tk
import pathlib as ph
import functions

#Root and frame creation
root = tk.Tk()
frame = tk.Frame(root, width=500, height=300, bg='white')
frame.pack()

#Widgets placement
button1 = tk.Button(frame, text='Select Reports', command=lambda: askdirectory(text1))
button1.grid(row=0, column=0, padx=5, pady=5)

text1 = tk.Entry(frame)
text1.grid(row=1, column=0, padx=5, pady=5)

button2 = tk.Button(frame, text='Set Target File', command=lambda: asktarget(text2))
button2.grid(row=2, column=0, padx=5, pady=5)

text2 = tk.Entry(frame)
text2.grid(row=3, column=0, padx=5, pady=5)

root.mainloop()