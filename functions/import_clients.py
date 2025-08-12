from traceback import print_tb

import openpyxl
from openpyxl import Workbook
from openpyxl import load_workbook
from tkinter.filedialog import askopenfilename  #Вызывает диалог на получения пути к файлу
import sqlite3 as sq
from tkinter.messagebox import showinfo

import settings

class Error(Exception):  # Базовый класс для других исключений
    pass

class Notfoundfile(Error):
    pass


def import_xlsx_clients():

    ######################
    # ВЫБОР файла xls
    ######################

    mypath_import = "."

    try:
        way = askopenfilename(title="Выберите файл", initialdir=mypath_import,
                          filetypes=[("Files *.xlsx", ".xlsx .xls")])

        # print("way", way)

        if way == "":
            raise Notfoundfile

    except Notfoundfile:
        # print("ЗАШЛИ В ИСКЛЮЧЕНИЕ")

        way = askopenfilename(title="Файл .xls с данными не обнаружен. Выберите файл", initialdir=mypath_import,
                              filetypes=[("Files *.xlsx", ".xlsx .xls")])
        return

    #################################
    # Открываем существующий файл XLS  #
    #################################

    wb = load_workbook(way)
    # Получаем активный лист
    sheet = wb.active

    contacts = []

    clients = [] # Массив

    ############################################
    # Открыть БД для работы
    ############################################

    with sq.connect(f"base/base_contacts.db") as con:
        cur = con.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS clients (
                name_id INTEGER PRIMARY KEY AUTOINCREMENT,
                short_name TEXT,
                long_name TEXT,
                inn TEXT,
                address TEXT,
                industry TEXT,
                comment TEXT,
                rez1 TEXT,
                rez2 TEXT,
                rez3 TEXT)
        """)


    i = 1  # первая строка для перебора всех строк файла загрузки. Начинаем с первой строки
    while True:
        # Структура xls для загрузки клиентов

        short_name = sheet["A" + str(i)].value  # 1) Короткое название контрагента
        long_name = sheet["B" + str(i)].value   # 2) Длинное наименование
        inn = sheet["C" + str(i)].value         # 3) ИНН
        address = sheet["D" + str(i)].value     # 4) Адрес
        industry = sheet["E" + str(i)].value    # 5) Отрасль



        if short_name == "" or short_name == None:  # прерываем перебор и считывание как только пойдут пустые строки
            break

        # создаем массив одномерный для записи "строки" в большой массив

        rez1 = "" # поле резервное 1
        rez2 = "" # поле резервное 2
        rez3 = "" # поле резервное 3

        comment = "" # поле для комментария 7) поле

        new_str = [short_name, long_name, inn, address, industry, comment, rez1, rez2, rez3]

        print("new_ str", new_str)

        ################################################
        # ДОБАВЛЯЕМ строку в БД!
        ################################################

        cur.execute(
            "INSERT INTO clients (short_name, long_name, inn, address, industry, comment, rez1, rez2, rez3) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            new_str)


        contacts.append(new_str)  # Добавление в массив новой строки-массива
        i += 1

    con.commit()
    con.close()

    showinfo("Результат", f"{i} Контрагентов добавлены в базу данных")



