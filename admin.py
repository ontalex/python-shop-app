from tkinter import *
import tkinter as tk
from tkinter import ttk

import pyodbc
from tkinter import messagebox

import lib


class App(tk.Tk):
    
    def __init__(self):
        super().__init__()

        # Базовая разметка
        self.title("Окно администратора")
        self.geometry("1260x720")
        self.resizable(False,False)

        # инициализация меню окна
        self.init_menu()
        
        # интициализация подключения
        self.conn = pyodbc.connect(r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=Z:\Developments\Python\shop_max\shop\shop1.accdb')
        self.cursor = self.conn.cursor()

        # получение введённого логина
        sql = "SELECT Логин FROM Пользователи WHERE Роль='Администратор'"
        self.cursor.execute(sql)
        admin_login = self.cursor.fetchone()[0]

        # отображение пометки о роли
        self.rule_label = Label(self, text="Вы вошли как "+str(admin_login), background="#333333", foreground="white", font="9")
        self.rule_label.pack(side="top", fill="x")

        # создание основного контейнера приложения
        self.app_box = Frame(self, background="yellow")
        self.app_box.pack(fill=BOTH, expand=True)

        # создание контейнера для формы
        self.form_frame = Frame(self.app_box)
        self.form_frame.pack(fill=BOTH, expand=True, padx=8, pady=8)

        # пометка для пользователя в контейнере форм
        self.label_alert = Label(self.form_frame, text="Здесь будет форма данных. \nВыберите таблицу из меню", foreground="red", font="8")
        self.label_alert.pack(fill=BOTH, expand=True)

        # создание контейнера для таблицы
        self.table = ttk.Treeview(self.app_box, height=20)
        self.table["columns"] = ()
        self.table.pack(fill=BOTH, expand=True, padx=8, pady=8)

        # глобальные переменные
        self.table_title = ""
        self.entries = []
        self.labels = []




    def init_menu(self):
        self.main_menu = tk.Menu(self)
        self.config(menu=self.main_menu)
            # Создаем меню "Управление"
        self.control_menu = tk.Menu(self.main_menu)
        
        # Добавляем подменю "Товары" и пункты "Добавить", "Просмотреть", "Изменить" и "Удалить"
        self.products_menu = tk.Menu(self.control_menu)
        self.products_menu.add_command(label="Добавить", command=lambda: self.products_table(create_form=True))
        self.products_menu.add_command(label="Просмотреть", command=self.products_table)
        self.products_menu.add_command(label="Изменить", command=lambda: self.products_table(edit_form=True))
        self.products_menu.add_command(label="Удалить", command=lambda: self.products_table(delete_form=True))
        self.control_menu.add_cascade(label="Товары", menu=self.products_menu)

        # Добавляем подменю "Продажи" и пункты "Добавить", "Просмотреть", "Изменить" и "Удалить"
        self.sales_menu = tk.Menu(self.control_menu)
        self.sales_menu.add_command(label="Добавить", command=lambda: self.sales_table(create_form=True))
        self.sales_menu.add_command(label="Просмотреть", command=self.sales_table)
        self.sales_menu.add_command(label="Изменить", command=lambda: self.sales_table(edit_form=True))
        self.sales_menu.add_command(label="Удалить", command=lambda: self.sales_table(delete_form=True))
        self.control_menu.add_cascade(label="Продажи", menu=self.sales_menu)

        # Добавляем подменю "Поставщики" и пункты "Добавить", "Просмотреть", "Изменить" и "Удалить"
        self.suppliers_menu = tk.Menu(self.control_menu)
        self.suppliers_menu.add_command(label="Добавить", command=lambda: self.suppliers_table(create_form=True))
        self.suppliers_menu.add_command(label="Просмотреть", command=self.suppliers_table)
        self.suppliers_menu.add_command(label="Изменить", command=lambda: self.suppliers_table(edit_form=True))
        self.suppliers_menu.add_command(label="Удалить", command=lambda: self.suppliers_table(delete_form=True))
        self.control_menu.add_cascade(label="Поставщики", menu=self.suppliers_menu)

        # Добавляем подменю "Поставки" и пункты "Добавить", "Просмотреть", "Изменить" и "Удалить"
        self.supply_menu = tk.Menu(self.control_menu)
        self.supply_menu.add_command(label="Добавить", command=lambda: self.supply_table(create_form=True))
        self.supply_menu.add_command(label="Просмотреть", command=self.supply_table)
        self.supply_menu.add_command(label="Изменить", command=lambda: self.supply_table(edit_form=True))
        self.supply_menu.add_command(label="Удалить", command=lambda: self.supply_table(delete_form=True))
        self.control_menu.add_cascade(label="Поставки", menu=self.supply_menu)

        # Добавляем подменю "Чеки" и пункты "Добавить", "Просмотреть", "Изменить" и "Удалить"
        self.check_menu = tk.Menu(self.control_menu)
        self.check_menu.add_command(label="Просмотреть", command=self.check_table)
        self.control_menu.add_cascade(label="Чеки", menu=self.check_menu)

        # Добавляем пункт меню "Управление"
        self.main_menu.add_cascade(label="Управление", menu=self.control_menu)
    

    # =============== Оброботчики таблиц ====================
    def render_table(self):
        table = self.table_title

        if table == "Товары":
            self.products_table()
        elif table == "Продано":
            self.sales_table()
        elif table == "Поставщики":
            self.suppliers_table()
        elif table == "Поставки":
            self.supply_table()
        elif table == "Чек":
            self.check_table()

    def update_table(self):
        # Очистить таблицу перед обновлением
        records = self.table.get_children()
        for record in records:
            self.table.delete(record)

        # Выполнить SQL-запрос для получения новых данных
        sql = "SELECT * FROM {};".format(self.table_title)
        self.cursor.execute(sql)
        result = self.cursor.fetchall()

        # Добавить новые записи в таблицу
        for row in result:
            self.table.insert(parent='', index='end', values=tuple(row))
    
    def create_table(self, columns):
        # self.table.destroy()
        self.table.delete()
        
        # self.form_frame.destroy() # заменить на обход объекта
        print(self.form_frame.winfo_children())
        for widget in self.form_frame.winfo_children():
            widget.destroy()
        
        self.table=ttk.Treeview(self) # increase font size
        self.table.bind("<>")
        self.table["columns"] = columns

        self.table.column('#0', width=0, stretch=tk.NO)
        self.table.heading('#0', text="", anchor=tk.CENTER)

        for column in columns:
            self.table.column(column, width=150, anchor=tk.CENTER)
            self.table.heading(column, text=column, anchor=tk.CENTER)

    def create_row(self):
        values = []
        for entry in self.entries:
            values.append(entry.get())
            entry.delete(0, tk.END) # очистить поле ввода после добавления записи
        sql = "INSERT INTO {} VALUES ({});".format(self.table_title, ",".join(["'{}'".format(value) for value in values]))
        self.cursor.execute(sql)
        self.conn.commit()
        self.update_table()




    # ============== инициаторы таблиц ==============
    def products_table(self, create_form = False, edit_form = False, delete_from = False):
        
        print("products_table")
        self.table_title = "Товары"

        # создание колон таблицы
        columns = ('Код', 'Наименование', 'Id_поставки', 'Количество', 'Срок_годности', 'Цена', 'Скидка')
        self.create_table(columns=columns)

        # запрос к базе на поучение текущих данных
        sql = "SELECT * FROM {}".format(self.table_title)
        self.cursor.execute(sql)
        result = self.cursor.fetchall()

        # заполнение таблицы
        for row in result:
            self.table.insert(parent='', index='end', values=tuple(row))

        # запуск формы для обработки таблицы
        if (create_form == True):
            print(">>> Open Create Form")
            self.create_form_open(columns=columns)
        elif (edit_form == True):
            print(">>> Open Edit Form")
            self.update_form_open(columns=columns)
        elif (delete_from == True):
            print(">>> Open Delete Form")
            self.delete_form_open(columns=columns)
        else:
            self.destroy_form()


    def sales_table(self, create_form = False, edit_form = False, delete_from = False):
        print("sales_table")

        self.table_title = "Товары"

        # создание колон таблицы
        columns = ('Код', 'Наименование', 'Id_поставки', 'Количество', 'Срок_годности', 'Цена', 'Скидка')
        self.create_table(columns=columns)

        # запрос к базе на поучение текущих данных
        sql = "SELECT * FROM {}".format(self.table_title)
        self.cursor.execute(sql)
        result = self.cursor.fetchall()

        # заполнение таблицы
        for row in result:
            self.table.insert(parent='', index='end', values=tuple(row))

        # запуск формы для обработки таблицы
        if (create_form == True):
            print(">>> Open Create Form")
            self.create_form_open(columns=columns)
        elif (edit_form == True):
            print(">>> Open Edit Form")
            self.update_form_open(columns=columns)
        elif (delete_from == True):
            print(">>> Open Delete Form")
            self.delete_form_open(columns=columns)
        else:
            self.destroy_form()




    def suppliers_table(self, create_form = False, edit_form = False, delete_from = False):
        print("suppliers_table")

        self.table_title = "Товары"

        # создание колон таблицы
        columns = ('Код', 'Наименование', 'Id_поставки', 'Количество', 'Срок_годности', 'Цена', 'Скидка')
        self.create_table(columns=columns)

        # запрос к базе на поучение текущих данных
        sql = "SELECT * FROM {}".format(self.table_title)
        self.cursor.execute(sql)
        result = self.cursor.fetchall()

        # заполнение таблицы
        for row in result:
            self.table.insert(parent='', index='end', values=tuple(row))

        # запуск формы для обработки таблицы
        if (create_form == True):
            print(">>> Open Create Form")
            self.create_form_open(columns=columns)
        elif (edit_form == True):
            print(">>> Open Edit Form")
            self.update_form_open(columns=columns)
        elif (delete_from == True):
            print(">>> Open Delete Form")
            self.delete_form_open(columns=columns)
        else:
            self.destroy_form()




    def supply_table(self, create_form = False, edit_form = False, delete_from = False):
        print("supply_table")

        self.table_title = "Товары"

        # создание колон таблицы
        columns = ('Код', 'Наименование', 'Id_поставки', 'Количество', 'Срок_годности', 'Цена', 'Скидка')
        self.create_table(columns=columns)

        # запрос к базе на поучение текущих данных
        sql = "SELECT * FROM {}".format(self.table_title)
        self.cursor.execute(sql)
        result = self.cursor.fetchall()

        # заполнение таблицы
        for row in result:
            self.table.insert(parent='', index='end', values=tuple(row))

        # запуск формы для обработки таблицы
        if (create_form == True):
            print(">>> Open Create Form")
            self.create_form_open(columns=columns)
        elif (edit_form == True):
            print(">>> Open Edit Form")
            self.update_form_open(columns=columns)
        elif (delete_from == True):
            print(">>> Open Delete Form")
            self.delete_form_open(columns=columns)
        else:
            self.destroy_form()




    def check_table(self):
        print("check_table")

        self.table_title = "Товары"

        # создание колон таблицы
        columns = ('Код', 'Наименование', 'Id_поставки', 'Количество', 'Срок_годности', 'Цена', 'Скидка')
        self.create_table(columns=columns)

        # запрос к базе на поучение текущих данных
        sql = "SELECT * FROM {}".format(self.table_title)
        self.cursor.execute(sql)
        result = self.cursor.fetchall()

        print(result)

        # заполнение таблицы
        for row in result:
            self.table.insert(parent='', index='end', values=tuple(row))

        self.destroy_form()



    # =============== Обработчик форм ===============
    def reset_form(self):
        for entry in self.entries:
            entry.delete(0, tk.END)

    def create_form_open(self, columns):

        # self.form_frame.destroy()
        self.destroy_form()
        self.form_frame = Frame(borderwidth=1, relief=tk.SOLID, width=1000, height=100)

        self.create_button = Button(self.form_frame, text="Создать", width=20, background="green", foreground="white", command=self.create_row)
        # self.create_button.place( x=64, y=110 )
        self.create_button.pack()
        

        ########################################################################################

        for entry in self.entries:
            entry.destroy()

        for label in self.labels:
            label.destroy()
        
        self.entries = []
        self.labels = []

        for i in range(0, len(columns)):
            entry = ttk.Entry(self)
            label = ttk.Label(self, text=columns[i])

            self.entries.append(entry)
            self.labels.append(label)

            entry.place(x = 64 + 150 * i, y=80)
            label.place(x = 64 + 150 * i, y = 60)

        ########################################################################################

        if len(self.entries) > 0:
            self.reset_button = Button(self.form_frame, text="Сброс", width=10, background="red", foreground="white", command=self.reset_form)
            self.reset_button.place(x=230,y=110)
            # self.reset_button.place( anchor=E )

    def update_form_open(self, columns):
        
        def update_form_data():
            ## Инициировать форму обновления данных
            print(">>> Update Form - Open")

            self.form_frame.destroy()
            self.form_frame = Frame(borderwidth=1, relief=tk.SOLID, width=1000, height=100)

            # форма для работы с данными

            # кнопка обновления введённых данных
            
            # кнопка сброса ввода


        def has_data():
            print("Check has data for Update Data")

            # выполнить запрос на поиск данных
            # если есть, то update_form_data, иначе сообщение об ошибки

            sql = "SELECT * FROM {} WHERE {}='{}'".format(self.table_title, columns[0], self.update_find_entry.get())
            print(">>> SQL STRING = ",sql)

            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            print(result)

            if result != []:
                update_form_data()
            else:
                print(">> RES is null")



        self.destroy_form()

        # Создать поле поиска данных
        self.update_find_entry = Entry(self.form_frame, width=40, font="arial 16",)

        # Создать кнопку
        self.update_find_btn = Button(self.form_frame, text="Найдти", width=10, background="blue", foreground="white", command=has_data, font="arial 12")

        self.update_find_entry.place(x=180, y=64)
        self.update_find_btn.place(x=64, y=64)

    def destroy_form(self):
        print(">>> Destroy form")
        print(self.entries)

        print(">>> Form Frame Object = ",self.form_frame)
        
        for entry in self.entries:
            entry.destroy()
        
        for label in self.labels:
            label.destroy()

        self.entries = []
        self.labels = []

        for widget in self.form_frame.winfo_children():
            widget.destroy()



if __name__ == "__main__":
    app = App()
    app.mainloop()
