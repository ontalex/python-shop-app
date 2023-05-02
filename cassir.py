from tkinter import *
import tkinter as tk
from tkinter import ttk

import pyodbc
from tkinter import messagebox

class App(tk.Tk):
    def __init__(self, ):
        super().__init__()

        # Базовая разметка
        self.title("Окно администратора")
        self.geometry("1260x720")
        self.resizable(False,False)


if __name__ == "__main__":
    app = App()
    app.mainloop()