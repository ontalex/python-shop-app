from tkinter import ttk

def windowCenter(window, app_w, app_h):
    screen_w = window.winfo_screenwidth()
    screen_h = window.winfo_screenheight()

    app_margin_left = (screen_w/2)-(app_w/2)
    app_margin_top = (screen_h/2)-(app_h/2)

    window.geometry('{}x{}+{}+{}'.format(app_w, app_h, int(app_margin_left), int(app_margin_top)))

def rewriteTable(target, table):
    if len(target.children) != 1:
        print("Обновление таблиц")
        listTables = target.children.keys()
        keys = list(listTables)

        target.children[keys[0]].destroy()
    else:
        print("Обновление не выполенно - только один дочений элемент")


def parseRow(row):
    goodRow = []

    for i in range(len(row)):
        goodRow.append(str(row[i]))

    return goodRow
