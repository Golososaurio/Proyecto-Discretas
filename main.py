from src.ui import UserInterface
from tkinter import *

if __name__ == "__main__":
    ventana = Tk()
    aplicacion = UserInterface(ventana)
    ventana.mainloop()