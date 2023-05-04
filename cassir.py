from tkinter import *
import tkinter as tk
from tkinter import ttk

import pyodbc
from tkinter import messagebox

class App(tk.Tk):
    def __init__(self, login):
        super().__init__()

        # запоминаем логин сессии
        self.login = login
        self.cheque = 1
        self.sum = 0

        # интициализация подключения
        self.conn = pyodbc.connect(r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=Z:\Developments\Python\shop_max\shop_v2\python-shop-app\shop1.accdb')
        self.cursor = self.conn.cursor()

        # Базовая разметка
        self.title("Окно кассира")
        self.geometry("1260x720")
        self.resizable(False,False)

        # отображение пометки о роли
        self.rule_label = Label(self, text="Вы вошли как "+str(login), background="#333333", foreground="white", font="9")
        self.rule_label.pack(side="top", fill="x")

        # создание основного контейнера приложения
        self.app_box = Frame(self)
        self.app_box.pack(fill=BOTH, expand=True, padx=10, pady=10)
        
        # создаём обортку для таблицы с товарами
        self.product_wrapper = Frame(self.app_box)

        # создаём обортку для корзины
        self.basket_wrapper = Frame(self.app_box)

        # инициализация виджитов обёрток
        self.product_wrapper.pack(side="left", expand=True, anchor="center", padx=8)
        self.basket_wrapper.pack(side="right", expand=True, anchor="center", padx=8)

        # создаём виджет таблицы продуктов
        Label(self.product_wrapper, text="Товары", font="arial 14").pack(fill="x", pady=[0, 8])

        self.products_columns = ('Код', 'Наименование', 'Количество', 'Цена')

        self.product_table = ttk.Treeview(self.product_wrapper, height=16)
        self.product_table["columns"] = self.products_columns
        self.product_table.column('#0', width=0, stretch=tk.YES)
        self.product_table.heading('#0', text="", anchor=tk.CENTER)
        self.product_table.pack(fill="x")

        for column in self.products_columns:
            self.product_table.column(column, stretch=tk.YES, anchor=tk.CENTER)
            self.product_table.heading(column, text=column, anchor=tk.CENTER)

        # создаём виджет формы добавления в чек
        self.product_form = Frame(self.product_wrapper)
        self.product_code_label = Label(self.product_form, text="Штрихкод", font="arial 14")
        self.product_count_label = Label(self.product_form, text="Колличество", font="arial 14")
        self.product_code_ent = Entry(self.product_form, font="arial 14")
        self.product_count_ent = Entry(self.product_form, font="arial 14")
        self.product_enter_btn = Button(self.product_form, command=self.add_product, font="arial 14", text="Добавить", background="green", fg="white")
        self.product_clear_btn = Button(self.product_form, command=self.reset_form, font="arial 14", text="Сброс", background="red", fg="white")

        self.product_form.pack(expand=True, anchor="center", pady=8)

        self.product_code_label.grid( row=0, column=0, padx=[0, 16])
        self.product_count_label.grid(row=1, column=0, padx=[0, 16])
        
        self.product_code_ent.grid( row=0, column=1, columnspan=11)
        self.product_count_ent.grid(row=1, column=1, columnspan=11)

        self.product_enter_btn.grid(row=2, column=0, columnspan=4, sticky="nsew", pady=8, padx=[0, 16])
        self.product_clear_btn.grid(row=2, column=4, columnspan=8, sticky="nsew", pady=8)


        # создаём виджет таблицы корзины
        Label(self.basket_wrapper, text=f"Чек №{self.cheque}", font="arial 14").pack(fill="x", pady=[0, 8])

        self.basket_columns = ("Код", "Количество", "Цена")
        self.basket_table = ttk.Treeview(self.basket_wrapper)
        self.basket_table["columns"] = self.basket_columns
        print(self.basket_table["columns"])
        self.basket_table.column('#0', width=0, stretch=tk.YES)
        self.basket_table.heading('#0', text="", anchor=tk.CENTER)
        self.basket_table.pack(fill="x")

        for column in self.basket_columns:
            self.basket_table.column(column, stretch=tk.YES, anchor=tk.CENTER)
            self.basket_table.heading(column, text=column, anchor=tk.CENTER)

        # создаём виджет формы работы с чеком
        self.basket_form = Frame(self.basket_wrapper)

        self.basket_sum_label = Label(self.basket_form, font="arial 14", text=f"Сумма: {self.sum}")
        self.basket_sell_btn = Button(self.basket_form, font="arial 14", text="Продать", command=self.sell_products)
        self.basket_return_btn = Button(self.basket_form, font="arial 14", text="Вернуть ", command=self.return_product)

        self.basket_form.pack()
        self.basket_sum_label.pack()
        self.basket_sell_btn.pack()
        self.basket_return_btn.pack()

        # начальные вызовы
        self.update_product_table()

    def sell_products():
        print(">> CELL Products")

    def return_product():
        print(">> Return product")

    def update_product_table(self):
        # Очистить таблицу перед обновлением
        records = self.product_table.get_children()
        for record in records:
            self.product_table.delete(record)

        # Выполнить SQL-запрос для получения новых данных
        sql = "SELECT Код, Наименование, Количество, Цена FROM Товары"
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        print(result)

        # Добавить новые записи в таблицу
        for row in result:
            self.product_table.insert(parent='', index='end', values=tuple(row))
    
    def reset_form(self):
        print(">> RESET FORM ENTRIES")
        self.product_code_ent.delete(0, tk.END)
        self.product_count_ent.delete(0, tk.END)

    def add_product(self):
        print(">> Add product to table Cheke")

        code_product = self.product_code_ent.get()

        user_count = int(self.product_count_ent.get())
        db_count = int(self.get_count(id_product=code_product))

        end_count = db_count - user_count

        if end_count >= 0:

            db_cost = int(self.get_cost(id_product=code_product))

            end_cost = db_cost * user_count
            self.sum = self.sum + end_cost

            print(">> COST data = ", end_cost)

            self.basket_sum_label.configure(text=f"Сумма: {self.sum}")

            self.basket_table.insert(parent="" ,index="end", values=(code_product, user_count, end_cost))

            self.update_data(code_product, end_count)
        else:
            messagebox.showwarning(title="Внимание!", message=f"Нету нужного количества товара! Имеется: {db_count} шт.")
            print(">> Not enough")

    def update_data(self, product_id, count_product):
        print(">> UPDATE data DB")

        sql = f"UPDATE Товары SET Количество='{count_product}' WHERE Код='{product_id}'"
        self.cursor.execute(str(sql))

        self.update_product_table()

    def get_count(self, id_product):
        # функция получения колличества товара из БД
        print(">> Get count product from DB")

        sql = f"SELECT Количество FROM Товары WHERE [Код]=?"
        params = (id_product)

        self.cursor.execute(sql, params)
        res = int(self.cursor.fetchone()[0])
        print(">> GET count = ", res)

        return res
    
    def get_cost(self, id_product):
        # функция получения колличества товара из БД
        print(">> Get cost product from DB")

        sql = f"SELECT Цена FROM Товары WHERE [Код]=?"
        params = (id_product)

        self.cursor.execute(sql, params)
        res = int(self.cursor.fetchone()[0])
        print(">> GET cost = ", res)


        return res

if __name__ == "__main__":
    app = App()
    app.mainloop()