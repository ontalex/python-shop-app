from tkinter import *
import tkinter as tk
from tkinter import ttk

import time
import math
import pyodbc
from tkinter import messagebox

# // * =================================================== * #
# // ? Добавить новое поле баловой системы за покупки
# // * =================================================== * #

# // * =================================================== * #
# // ? Написать функцию добавления 10% от суммы покупки
# // * =================================================== * #

# * =================================================== * #
# ? Формировать список операций добавления в чек
# * =================================================== * #

# * =================================================== * #
# ? Отменять последнюю операцию
# * =================================================== * #

# // * =================================================== * #
# // ? Затирать сумму и таблицу про покупки
# // * =================================================== * #

class App(tk.Tk):
    def __init__(self, login):
        super().__init__()

        # запоминаем логин сессии
        self.login = login

        # стартовое значение общей суммы чека
        self.sum = 0

        # интициализация подключения
        self.conn = pyodbc.connect(
            r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=Z:\Developments\Python\shop_max\shop_v2\python-shop-app\shop1.accdb"
        )
        self.cursor = self.conn.cursor()

        # получаем размеры экрана для центрирования
        self.pad_w_screen = (self.winfo_screenwidth() - 1160) / 2
        self.pad_h_screen = (self.winfo_screenheight() - 720) / 3
        print(self.pad_w_screen, " - ", self.pad_h_screen)

        # Базовая разметка
        self.title("Касса самообслуживания")
        self.geometry("%dx%d+%d+%d" %(1160, 720,self.pad_w_screen, self.pad_h_screen))
        self.resizable(False, False)

        # отображение пометки о роли
        self.rule_label = Label(
            self,
            text="Вы вошли как " + str(login),
            background="#333333",
            foreground="white",
            font="9",
        )
        self.rule_label.pack(side="top", fill="x")

        # создание основного контейнера приложения
        self.app_wrapper = Frame(self)
        self.app_wrapper.pack(fill=BOTH, expand=True, padx=10, pady=10)

        # обёртка для таблицы корзины
        self.basket_wrapper = Frame(self.app_wrapper)
        self.basket_wrapper.pack(fill=BOTH, expand=True)

        self.basket_label = Label(self.basket_wrapper, text="Корзина", font="9")
        self.basket_label.pack(side="top", fill="x")

        self.basket_columns = ("Код", "Наименование", "Количество", "Цена")
        self.basket_treeview = ttk.Treeview(self.basket_wrapper)
        self.basket_treeview["columns"] = self.basket_columns
        self.basket_treeview.column("#0", width=0, stretch=tk.YES)
        self.basket_treeview.heading("#0", text="", anchor=tk.CENTER)
        self.basket_treeview.pack(fill="both", expand=True)
        for column in self.basket_columns:
            self.basket_treeview.column(column, stretch=tk.YES, anchor=tk.CENTER)
            self.basket_treeview.heading(column, text=column, anchor=tk.CENTER)

        # инициируем форму для работы с чеком
        self.basket_form = Frame(self.app_wrapper)
        self.basket_form.pack(pady=16)

        self.sum_label = Label(
            self.basket_form, text="Итого: " + str(self.sum), font="9"
        )
        self.sum_label.pack()

        self.add_form = Frame(self.basket_form)
        self.add_form.pack()

        self.add_entry = Entry(self.add_form, font="9")
        self.add_entry.grid(row=0, column=0, columnspan=4, ipady=5, ipadx=5)

        self.add_btn = Button(
            self.add_form,
            text="+",
            background="green",
            foreground="white",
            font="9",
            command=self.add_product,
        )
        self.add_btn.grid(row=0, column=4)

        self.buy_btns = Frame(self.basket_form)
        self.buy_btns.pack()

        self.buy_btn = Button(self.buy_btns, text="Оплата", font="9", command=self.add_to_db)
        self.buy_btn.grid(row=0, column=0)

        self.revert_btn = Button(self.buy_btns, text="Вернуть", font="9", command=self.admin_check)
        self.revert_btn.grid(row=0, column=1)

        # перевод фокусировки на форму работы с товарами
        self.add_entry.focus()

        self.data_set = []
        self.data_operations = []

    def add_bonuses(self):
        print(">> Calculate bonuses")
        
        sql = "SELECT Бонусы FROM Пользователи WHERE Логин = '{}'".format(self.login)
        self.cursor.execute(str(sql))
        data = self.cursor.fetchall()

        bonuses = (self.sum / 100) * 10 # 10% от текущей суммы
        bonuse_now = int(data[0][0])
        print("data = ", bonuse_now, " + ", bonuses)

        all_bonuses = math.ceil(bonuse_now + bonuses)

        sqlUpdate = "UPDATE Пользователи SET Бонусы = {} WHERE Логин = '{}'".format(all_bonuses, self.login)
        print(sqlUpdate)
        self.cursor.execute(str(sqlUpdate))
        self.conn.commit()

        messagebox.showinfo(title="Обновление бонусов!", message="Вам начисленно: {} бонусов".format(math.ceil(bonuses)))

        self.clear_table()
        self.update_sum()




    def add_product(self):
        ent_data = self.add_entry.get()

        sql = "SELECT Код, Наименование, Количество, Цена FROM Товары WHERE Код =  '{}'".format(
            ent_data
        )
        print(sql)
        self.cursor.execute(sql)
        res = self.cursor.fetchall()

        print(res)

        if res == []:
            messagebox.showwarning(
                title="Внимание!", message="Такого товара не существует!"
            )
            self.clear_entry()
            return True

        row_to_list = []

        for row in res:
            row_to_list = [elem for elem in row]

        row_to_list[2] = "1"

        def checkInclude(rowCheck, listCheck):
            for i in range(len(listCheck)):
                if listCheck[i][0] == rowCheck[0]:
                    return [True, i]
            return [False, 0]

        hasElem = checkInclude(rowCheck=row_to_list, listCheck=self.data_set)
        if not (hasElem[0]):
            self.data_set.append(row_to_list)
            self.basket_treeview.insert(parent="", index="end", values=row_to_list)
        else:
            index = hasElem[1]
            print("index = ", index)
            self.data_set[index][2] = str(int(self.data_set[index][2]) + 1)
            self.data_set[index][3] = str(
                int(self.data_set[index][2]) * int(row_to_list[3])
            )

            self.update_rows(index=index, row=self.data_set[index])

        print(self.data_set)

        self.update_sum()
        self.clear_entry()

    def revert_product(self):
        print(">> Revert last item")

        print("deleted item = ",self.data_set.pop())
        print(self.data_set)

        self.update_sum()
        self.clear_entry()

        self.hard_update_table()


    def clear_entry(self):
        self.add_entry.delete(0, END)

    def hard_update_table(self):
        for k in self.basket_treeview.get_children(""): 
            self.basket_treeview.delete(k)

        for i in range(len(self.data_set)): 
            self.basket_treeview.insert(parent="", index=END, values=tuple(self.data_set[i]))

    def update_sum(self):
        print(">> Upadte end sum")
        self.sum = 0
        for i in self.data_set:
            self.sum += int(i[3])

        self.sum_label.configure(text=f"Итог: {self.sum}")

    def update_rows(self, index, row):
        print(">> Update rows in treeview")

        id_row = self.basket_treeview.get_children("")[index]
        print(id_row)
        print(tuple(row))
        self.basket_treeview.item(id_row, values=tuple(row))
        self.clear_entry()

    def clear_table(self):
        for k in self.basket_treeview.get_children(""): self.basket_treeview.delete(k)
        self.data_set = []

    def update_count_product(self):
        print(">> Update count in table of product")

        sql = "update Товары set count{}"
        self.cursor.execute(sql)
        self.cursor.commit()

    def add_to_db(self):
        print(">> Add data to DB")

        self.add_bonuses()
        self.update_count_product()
        self.sum = 0


    def admin_check(self):
        winAdmin = tk.Toplevel(self)

        # получаем размеры экрана для центрирования
        pad_w_screen = (self.winfo_screenwidth() - 1160) / 2
        pad_h_screen = (self.winfo_screenheight() - 720) / 2

        # Базовая разметка
        winAdmin.title("Подтвердите")
        winAdmin.geometry("%dx%d+%d+%d" %(300, 300, pad_w_screen, pad_h_screen))
        winAdmin.resizable(False, False)

        def check():
            login = entry_login.get()
            password = entry_password.get()
            self.cursor.execute(
                f"SELECT * FROM Пользователи WHERE Логин = '{login}' AND Пароль = '{password}'"
            )
            result = self.cursor.fetchone()
            print(result)
            if result is None:
                messagebox.showerror(
                    "Ошибка",
                    "Неправильный логин или пароль",
                    icon="error",
                    type="ok",
                    parent=winAdmin,
                )
            elif result[2] == "Администратор":
                print(">> Delete last item of operations")
                self.revert_product()
                # отмена последнего действия (лист операций добавления)
                winAdmin.destroy()
            else:
                messagebox.showerror(
                    "Отказ в доступе",
                    "Отказ в доступе к удалению данных",
                    icon="error",
                    type="ok",
                    parent=winAdmin,
                )

        def reset():
            # стераем данные из полей ввода
            entry_login.delete(0, END)
            entry_password.delete(0, END)

        # Верхний заголовок
        text = Label(winAdmin, text="Проверка", justify=CENTER, font="Arial 16")

        # Создаем группу для поля "Логин"
        loginForm = Label(winAdmin, pady=32)
        text_log = Label(loginForm, text="Логин", width=8, font="Arial 12")
        entry_login = Entry(loginForm, width=20, font="Arial 12")

        # Создаем группу для поля "Пароль"
        passForm = Label(winAdmin, pady=1)
        text_password1 = Label(passForm, text="Пароль", width=8, font="Arial 12")
        entry_password = Entry(passForm, width=20, font="Arial 12")

        # Создаем группу кнопок
        buttonsForm = Label(winAdmin)
        button_signin = Button(
            buttonsForm,
            font="Arial 12",
            width=12,
            height=2,
            text="Войти",
            bg="green",
            fg="white",
            command=check
        )
        button_reset = Button(
            buttonsForm, 
            font="Arial 12", 
            width=12, 
            height=2, 
            text="Сброс",
            command=reset
        )

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

        winAdmin.mainloop()


if __name__ == "__main__":
    app = App()
    app.mainloop()
