import tkinter as tk
from tkinter import *
from tkinter import messagebox
import pyodbc
from admin import App
from cassir import App as appCassir
from clientV2 import App as appClient

from lib import *


# Connect to the database
conn = pyodbc.connect(r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=Z:\Developments\Python\shop_max\shop_v2\python-shop-app\shop1.accdb')
cursor = conn.cursor()


# Подготавливаем окно входа
root = Tk()
windowCenter(root, 420, 240)
root.title("Вход в систему")
# root.iconbitmap(r'D:\Py dev\prGUI\prGUIpart9\basket.ico')


# напишим функции для двух кнопок "Сброс" и "Войти"
def reset(event):
    # стераем данные из полей ввода
    entry_login.delete(0, END)
    entry_password.delete(0, END)


# Define the event handlers
def check(event):
    login = entry_login.get()
    password = entry_password.get()
    cursor.execute(f"SELECT * FROM Пользователи WHERE Логин = '{login}' AND Пароль = '{password}'")
    result = cursor.fetchone()
    if result is None:
        messagebox.showerror("Ошибка", "Неправильный логин или пароль", icon="error", type="ok", parent=root)
    elif result[2] == "Администратор":
        root.destroy()
        app = App()
        app.mainloop()
    elif result[2] == "Кассир":
        root.destroy()
        app = appCassir(login=login)
        app.mainloop()
    elif result[2] == "Клиент":
        root.destroy()  
        app = appClient(login=login)
        app.mainloop()
    else:
        messagebox.showerror("Ошибка", "Неправильный логин или пароль", icon="error", type="ok", parent=root)


# Верхний заголовок
text = Label(root, text='Авторизация', justify=CENTER, font="Arial 16")

# Создаем группу для поля "Логин"
loginForm = Label(root, pady=32)
text_log = Label(loginForm,text='Логин', width=8, font="Arial 12")
entry_login = Entry(loginForm, width=20, font="Arial 12")

# Создаем группу для поля "Пароль"
passForm = Label(root, pady=1)
text_password1 = Label(passForm,text='Пароль', width=8, font="Arial 12")
entry_password = Entry(passForm, width=20, font="Arial 12")

# Создаем группу кнопок
buttonsForm = Label(root)
button_signin = Button(buttonsForm, font="Arial 12", width=12, height=2, text='Войти', bg="green", fg="white")
button_reset = Button(buttonsForm, font="Arial 12", width=12, height=2, text="Сброс")

# Создаём Canvas
canvas = Canvas(root, width=75, height=32, background="white")
canvas.place(x=345, y=208)

# Создаём "б"
canvas.create_line(
    20, 5,
    5, 5
)
canvas.create_line(
    5, 5,
    5, 28
)
canvas.create_line(
    5, 10,
    20, 19
)
canvas.create_line(
    20, 19,
    5, 28
)

# Создаём "А"
canvas.create_line(
    30, 28,
    37, 5
)
canvas.create_line(
    37, 5,
    45, 29
)
canvas.create_line(
    32, 22,
    44, 22
)

# Создаём "О"
canvas.create_rectangle(
    55, 5,
    70, 28
)

# Добавим привязку событий к кнопкам интерфейса входа
button_signin.bind("<Button-1>", check)
button_reset.bind("<Button-1>", reset)

# Привязывем все виджеты к ROOT
text_log.pack(side=LEFT)
entry_login.pack(side=RIGHT)
text_password1.pack(side=LEFT)
entry_password.pack(side=RIGHT, pady=4)
button_signin.pack(side=LEFT, padx=4)
button_reset.pack(side=LEFT, padx=4)

text.pack(pady=24)
loginForm.pack()
passForm.pack()
buttonsForm.pack(pady=16)

root.mainloop()
