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
        self.conn = pyodbc.connect(r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=Z:\Developments\Python\shop_max\shop_v2\python-shop-app\shop1.accdb')
        self.cursor = self.conn.cursor()

        # получение введённого логина
        sql = "SELECT Логин FROM Пользователи WHERE Роль='Администратор'"
        self.cursor.execute(sql)
        admin_login = self.cursor.fetchone()[0]

        # отображение пометки о роли
        rule_label = Label(self, text="Вы вошли как "+str(admin_login), background="#333333", foreground="white", font="9")
        rule_label.pack(side="top", fill="x")

        # создание основного контейнера приложения
        self.app_box = Frame(self,)
        self.app_box.pack(fill=BOTH, expand=True)

        # создание контейнера для формы
        self.form_frame = Frame(self.app_box)
        self.form_frame.pack(fill=BOTH, expand=True, padx=16, pady=16)

        # пометка для пользователя в контейнере форм
        label_alert = Label(self.form_frame, text="Здесь будет форма данных. \nВыберите таблицу из меню", foreground="red", font="8")
        label_alert.pack(fill=BOTH, expand=1)

        # создание контейнера для таблицы
        self.table = ttk.Treeview(self.app_box)
        self.table["columns"] = ()
        self.table.pack(fill=BOTH, expand=True, padx=16, pady=16)

        # глобальные переменные
        self.table_title = ""
        self.entries = []
        self.labels = []

        def on_closing():
            if messagebox.askokcancel("Quit", "Do you want to quit?"):
                self.cursor.close()
                self.conn.close()
                self.destroy()

        self.protocol("WM_DELETE_WINDOW", on_closing)

    def init_menu(self):
        main_menu = tk.Menu(self)
        self.config(menu=main_menu)
            # Создаем меню "Управление"
        control_menu = tk.Menu(main_menu)
        
        # Добавляем подменю "Товары" и пункты "Добавить", "Просмотреть", "Изменить" и "Удалить"
        products_menu = tk.Menu(control_menu)
        products_menu.add_command(label="Добавить", command=lambda: self.products_table(create_form=True))
        products_menu.add_command(label="Просмотреть", command=self.products_table)
        products_menu.add_command(label="Изменить", command=lambda: self.products_table(edit_form=True))
        products_menu.add_command(label="Удалить", command=lambda: self.products_table(delete_form=True))
        control_menu.add_cascade(label="Товары", menu=products_menu)

        # Добавляем подменю "Продажи" и пункты "Добавить", "Просмотреть", "Изменить" и "Удалить"
        sales_menu = tk.Menu(control_menu)
        sales_menu.add_command(label="Добавить", command=lambda: self.sales_table(create_form=True))
        sales_menu.add_command(label="Просмотреть", command=self.sales_table)
        sales_menu.add_command(label="Изменить", command=lambda: self.sales_table(edit_form=True))
        sales_menu.add_command(label="Удалить", command=lambda: self.sales_table(delete_form=True))
        control_menu.add_cascade(label="Продажи", menu=sales_menu)

        # Добавляем подменю "Поставщики" и пункты "Добавить", "Просмотреть", "Изменить" и "Удалить"
        suppliers_menu = tk.Menu(control_menu)
        suppliers_menu.add_command(label="Добавить", command=lambda: self.suppliers_table(create_form=True))
        suppliers_menu.add_command(label="Просмотреть", command=self.suppliers_table)
        suppliers_menu.add_command(label="Изменить", command=lambda: self.suppliers_table(edit_form=True))
        suppliers_menu.add_command(label="Удалить", command=lambda: self.suppliers_table(delete_form=True))
        control_menu.add_cascade(label="Поставщики", menu=suppliers_menu)

        # Добавляем подменю "Поставки" и пункты "Добавить", "Просмотреть", "Изменить" и "Удалить"
        supply_menu = tk.Menu(control_menu)
        supply_menu.add_command(label="Добавить", command=lambda: self.supply_table(create_form=True))
        supply_menu.add_command(label="Просмотреть", command=self.supply_table)
        supply_menu.add_command(label="Изменить", command=lambda: self.supply_table(edit_form=True))
        supply_menu.add_command(label="Удалить", command=lambda: self.supply_table(delete_form=True))
        control_menu.add_cascade(label="Поставки", menu=supply_menu)

        # Добавляем подменю "Чеки" и пункты "Добавить", "Просмотреть", "Изменить" и "Удалить"
        check_menu = tk.Menu(control_menu)
        check_menu.add_command(label="Просмотреть", command=self.check_table)
        control_menu.add_cascade(label="Чеки", menu=check_menu)

        # Добавляем пункт меню "Управление"
        main_menu.add_cascade(label="Управление", menu=control_menu)
    
    # =============== Оброботчики таблиц ====================
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
        # self.table.delete()
        print("заголовки (1) = ",self.table.winfo_children())
        
        # self.form_frame.destroy() # заменить на обход объекта
        print(self.form_frame.winfo_children())
        for widget in self.form_frame.winfo_children():
            widget.destroy()
        
        # self.table=ttk.Treeview(self.app_box) # increase font size
        self.table.bind("<>")
        self.table["columns"] = columns

        self.table.column('#0', width=0, stretch=tk.YES)
        self.table.heading('#0', text="", anchor=tk.CENTER)

        for column in columns:
            self.table.column(column, stretch=tk.YES, anchor=tk.CENTER)
            self.table.heading(column, text=column, anchor=tk.CENTER)

        print("заголовки (2) = ",self.table.winfo_children())

    def create_row(self):
        values = []
        for entry in self.entries:
            values.append(entry.get())
            entry.delete(0, tk.END) # очистить поле ввода после добавления записи
        sql = "INSERT INTO {} VALUES ({})".format(self.table_title, ",".join(["'{}'".format(value) for value in values]))
        self.cursor.execute(sql)
        self.conn.commit()
        
        self.update_table()

    def update_row(self, columns, id_find):
        
        # забор данных из полей ввода
        values = []
        for i in range(0, len(self.entries)):
            values.append(self.entries[i].get())
            self.entries[i].delete(0, tk.END) # очистить поле ввода после добавления записи
        
        # сормирование запроса
        for i in range(0, len(values)):
            # решить проблемму с синтаксисом запроса (использовать другую контетенацию строк)
            # sql = "UPDATE " + self.table_title + " SET ['" + columns[i+1] + "']='" + values[i] + "' WHERE ['" + columns[0] + "']='" + id_find + "'"
            # sql = "UPDATE {} SET {} WHERE {}".format(self.table_title, "=".join([columns[i+1], self.entries[i].get()]), "=".join([columns[0], id_find]))
            sql = f"UPDATE {self.table_title} SET [{columns[i+1]}]='{values[i]}' WHERE [{columns[0]}]='{id_find}'"

            print(">>> UPDATE SQL STRING = ", sql)
            self.cursor.execute(sql)
            self.conn.commit()

        self.update_table()
        self.update_form_open(columns)

    def delete_row(self, columns, id):
        sql = f"SELECT * FROM [{self.table_title}] WHERE [{columns[0]}]='{id}'"
        self.cursor.execute(sql)
        row_alert = self.cursor.fetchall()

        res = messagebox.askquestion(title="подтверждение удаления", message=f"Вы хотите удалить данные?\nСтрока: {row_alert[0]}")

        if res == "yes":
            sql = f"DELETE FROM [{self.table_title}] WHERE [{columns[0]}]='{id}'"
            print("SQL STRING = ", sql)
            self.cursor.execute(sql)
            self.conn.commit()
            self.update_table()

            self.delete_elem_entry.delete(0, END)
        else:
            self.delete_elem_entry.delete(0, END)

    # ============== инициаторы таблиц ==============
    def products_table(self, create_form = False, edit_form = False, delete_form = False):
        
        print("products_table")
        self.table_title = "Товары"

        # создание колон таблицы
        columns = ('Код', 'Наименование', 'Id_поставки', 'Количество', 'Срок_годности', 'Цена', 'Скидка')
        self.update_table()
        self.create_table(columns=columns)

        self.update_table()

        # запуск формы для обработки таблицы
        if (create_form == True):
            print(">>> Open Create Form")
            self.create_form_open(columns=columns)
        elif (edit_form == True):
            print(">>> Open Edit Form")
            self.update_form_open(columns=columns)
        elif (delete_form == True):
            print(">>> Open Delete Form (from prod_table)")
            self.delete_form_open(columns=columns)
        else:
            self.destroy_form()

    def sales_table(self, create_form = False, edit_form = False, delete_form = False):
        print("sales_table")

        self.table_title = "Продано"

        # создание колон таблицы
        columns = ('Порядковый_номер', 'Штрих-код', "Количество", "Номер_чека", "Цена")
        self.update_table()
        self.create_table(columns=columns)

        self.update_table()

        # запуск формы для обработки таблицы
        if (create_form == True):
            print(">>> Open Create Form")
            self.create_form_open(columns=columns)
        elif (edit_form == True):
            print(">>> Open Edit Form")
            self.update_form_open(columns=columns)
        elif (delete_form == True):
            print(">>> Open Delete Form")
            self.delete_form_open(columns=columns)
        else:
            self.destroy_form()

    def suppliers_table(self, create_form = False, edit_form = False, delete_form = False):
        print("suppliers_table")

        self.table_title = "Поставщики"

        # создание колон таблицы
        columns = ("id_поставщика", "Наименование", "Телефон", "Адрес", "Почта")
        self.update_table()
        self.create_table(columns=columns)

        self.update_table()

        # запуск формы для обработки таблицы
        if (create_form == True):
            print(">>> Open Create Form")
            self.create_form_open(columns=columns)
        elif (edit_form == True):
            print(">>> Open Edit Form")
            self.update_form_open(columns=columns)
        elif (delete_form == True):
            print(">>> Open Delete Form")
            self.delete_form_open(columns=columns)
        else:
            self.destroy_form()


    def supply_table(self, create_form = False, edit_form = False, delete_form = False):
        print("supply_table")

        self.table_title = "Поставки"

        # создание колон таблицы
        columns = ('Номер_накладной', 'id_поставщика', "дата")
        self.update_table()
        self.create_table(columns=columns)

        self.update_table()

        # запуск формы для обработки таблицы
        if (create_form == True):
            print(">>> Open Create Form")
            self.create_form_open(columns=columns)
        elif (edit_form == True):
            print(">>> Open Edit Form")
            self.update_form_open(columns=columns)
        elif (delete_form == True):
            print(">>> Open Delete Form")
            self.delete_form_open(columns=columns)
        else:
            self.destroy_form()


    def check_table(self):
        print("check_table")

        self.table_title = "Чек"

        # создание колон таблицы
        columns = ("Номер_чека", "Дата", "Время", "Номер_кассира")
        self.update_table()
        self.create_table(columns=columns)

        self.update_table()

        self.destroy_form()

    # =============== Обработчик форм ===============
    def reset_form(self):
        for entry in self.entries:
            entry.delete(0, tk.END)

    def create_form_open(self, columns):

        self.destroy_form()

        # создание обёрток
        # обёртка для групп полей ввода-пометок пользователя
        self.form_params = Frame(self.form_frame)
        self.form_params.pack(expand=True)
        # обёртка для групп полей ввода-пометок пользователя
        self.form_buttons = Frame(self.form_frame)
        self.form_buttons.pack(expand=True)


        self.create_button = Button(self.form_buttons, text="Создать", width=20, background="green", foreground="white", command=self.create_row)
        self.create_button.grid(row=0, column=0, padx=5)

        self.reset_button = Button(self.form_buttons, text="Сброс", width=20, background="red", foreground="white", command=self.reset_form)
        self.reset_button.grid(row=0, column=1, padx=5)

        ########################################################################################

        for entry in self.entries:
            entry.destroy()

        for label in self.labels:
            label.destroy()
        
        self.entries = []
        self.labels = []

        for i in range(0, len(columns)):
            label = ttk.Label(self.form_params, font="arial 10", text=columns[i])
            entry = ttk.Entry(self.form_params, font="arial 10")

            self.entries.append(entry)
            self.labels.append(label)

            entry.grid(column=i, row=1, pady=1, padx=4)
            label.grid(column=i, row=0, pady=1, padx=4)

        ########################################################################################

        self.update_table()

    def update_form_open(self, columns):

        def update_form_data(id, tupe_data):
            ## Инициировать форму обновления данных
            print(">>> Update Form - Open")

            # self.form_frame.destroy()
            self.destroy_form()
            
            # создание обёрток
            # обёртка для групп полей ввода-пометок пользователя
            self.form_params = Frame(self.form_frame)
            self.form_params.pack(expand=True)
            # обёртка для групп полей ввода-пометок пользователя
            self.form_buttons = Frame(self.form_frame)
            self.form_buttons.pack(expand=True)

            # ****************** создать поля ввода (с пометками) ******************
            for entry in self.entries:
                entry.destroy()

            for label in self.labels:
                label.destroy()
            
            self.entries = []
            self.labels = []

            for i in range(1, len(columns)):
                label = ttk.Label(self.form_params, font="arial 10", text=columns[i])
                entry = ttk.Entry(self.form_params, font="arial 10")

                # отображаем тикущие данные в поле изменения
                entry.insert(0, tupe_data[i])

                self.entries.append(entry)
                self.labels.append(label)

                entry.grid(column=i, row=1, pady=1, padx=4)
                label.grid(column=i, row=0, pady=1, padx=4)

            # создать кнопку отправки
            self.create_button = Button(self.form_buttons, text="Обновить", width=20, background="green", foreground="white", font="arial 14", command=lambda: self.update_row(columns, id))
            self.create_button.grid(row=0, column=0, padx=5)

            # создать кнопку сброса данных
            self.reset_button = Button(self.form_buttons, text="Сброс", width=20, background="red", foreground="white", font="arial 14", command=self.reset_form)
            self.reset_button.grid(row=0, column=1, padx=5)

        def has_data():
            print("Check has data for Update Data")

            # выполнить запрос на поиск данных
            # если есть, то update_form_data, иначе сообщение об ошибки
            
            find_id = update_find_entry.get()

            sql = "SELECT * FROM {} WHERE {}='{}'".format(self.table_title, columns[0], find_id)
            print(">>> SQL STRING = ",sql)

            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            print(result)

            if result != []:
                update_form_data(find_id, result[0])
            else:
                print(">> RES is null")

        self.destroy_form()

        # пометка длял текстового поля
        update_find_label = Label(self.form_frame, text=f"Поле: '{columns[0]}'", font="arial 14")
        # Создать поле поиска данных
        update_find_entry = Entry(self.form_frame, width=94, font="arial 16")

        # Создать кнопку
        update_find_btn = Button(self.form_frame, text="Найти", width=10, background="blue", foreground="white", command=has_data, font="arial 12")

        update_find_label.grid(
            row=0,
            column=1
        )
        update_find_entry.grid(
            row=1,
            column=1,
            padx=5
        )
        update_find_btn.grid(
            row=1,
            column=0
        )

        self.update_table()

    def delete_form_open(self, columns):
        print(">>> Open Delete Form")

        self.destroy_form()

        # создаём обёртки

        # пометка для ввода
        delete_elem_label = Label(self.form_frame, text=f"Поле: '{columns[0]}'", font="arial 14")

        # поле ввода
        self.delete_elem_entry = Entry(self.form_frame, width=92, font="arial 16")

        # кнопка удаления
        delete_elem_btn = Button(
            self.form_frame, 
            text="Удалить", 
            width=10, 
            background="red", 
            foreground="white", 
            command=lambda: self.delete_row(columns, self.delete_elem_entry.get()), 
            font="arial 12"
        )

        # инициализация виджетов на удаление
        self.delete_elem_entry.grid(
            row=1,
            column=0,
            padx=5
        )
        delete_elem_btn.grid(
            row=1,
            column=1
        )
        delete_elem_label.grid(
            row=0,
            column=0
        )

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