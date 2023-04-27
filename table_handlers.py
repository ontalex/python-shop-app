    # Оброботчики таблиц
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
    
    def create_row(self):
        values = []
        for entry in self.entries:
            values.append(entry.get())
            entry.delete(0, tk.END) # очистить поле ввода после добавления записи
        sql = "INSERT INTO {} VALUES ({});".format(self.table_title, ",".join(["'{}'".format(value) for value in values]))
        self.cursor.execute(sql)
        self.conn.commit()
        self.update_table()