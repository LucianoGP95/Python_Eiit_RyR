import tkinter as tk
from tkinter import ttk

class CustomEntryWidget(ttk.Entry):
    def __init__(self, master=None, default_text="", **kwargs):
        super().__init__(master, **kwargs)
        self.default_text = default_text
        self.insert(0, self.default_text)
        self.bind("<FocusIn>", self.on_focus_in)
        self.bind("<FocusOut>", self.on_focus_out)

    def on_focus_in(self, event):
        if self.get() == self.default_text:
            self.delete(0, tk.END)
            self.config(foreground='black')  #Set text color to black

    def on_focus_out(self, event):
        if not self.get():
            self.insert(0, self.default_text)
            self.config(foreground='gray')  #Set text color to gray

#Test Script
if __name__ == '__main__':
    root = tk.Tk()
    frame = ttk.Frame(root)
    frame.pack(padx=10, pady=10)
    text1 = CustomEntryWidget(frame, default_text="Enter default text", width=30)
    text1.grid(row=0, column=0, padx=5, pady=5)
    root.mainloop()