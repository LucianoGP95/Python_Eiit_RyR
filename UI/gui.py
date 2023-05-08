from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\luciano.galan\Desktop\Code\1_Repositories\Python_RyR\build\assets\frame0")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()

window.geometry("728x488")
window.configure(bg = "#7A7DCD")


canvas = Canvas(
    window,
    bg = "#7A7DCD",
    height = 488,
    width = 728,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
canvas.create_rectangle(
    55.0,
    46.0,
    143.0,
    91.0,
    fill="#000000",
    outline="")
window.resizable(False, False)
window.mainloop()
