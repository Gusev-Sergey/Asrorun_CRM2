from traceback import print_tb

import openpyxl
from openpyxl import Workbook
from openpyxl import load_workbook
from tkinter.filedialog import askopenfilename  #Вызывает диалог на получения пути к файлу
import settings

class Error(Exception):  # Базовый класс для других исключений
    pass

class Notfoundfile(Error):
    pass


def import_xlsx_w(contacts):



    ######################
    # октрытие файла xls
    ######################

    mypath_import = "."


    try:
        way = askopenfilename(title="Выберите файл", initialdir=mypath_import,
                          filetypes=[("Files *.xlsx", ".xlsx .xls")])

        print("way", way)

        if way == "":
            raise Notfoundfile

    except Notfoundfile:
        print("ЗАШЛИ В ИСКЛЮЧЕНИЕ")

        way = askopenfilename(title="Файл .xls с данными не обнаружен. Выберите файл", initialdir=mypath_import,
                              filetypes=[("Files *.xlsx", ".xlsx .xls")])
        return



    # Открываем существующий файл
    wb = load_workbook(way)
    # Получаем активный лист
    sheet = wb.active
    # Читаем значение ячейки A1
    value = sheet["C1"].value
    # print(f"Значение ячейки A1: {value}")

    contacts = []

    # dict_str = [en_word, transc_word_final, transl_word_final, 0, 0]
    # dict_all.append(dict_str)  # Включили в состав массива новый блок Слово-Транскрипция-Перевод-Признак учить или нет

    i = 1  # первая строка для перебора всех строк файла загрузки. Начинаем с первой строки
    while True:
        contact = sheet["A" + str(i)].value  # Контакт (полное ФИО одной строкой)
        second_name = sheet["B" + str(i)].value  # фамилия
        first_name = sheet["C" + str(i)].value  # имя
        patronymic = sheet["D" + str(i)].value  # отчество
        post = sheet["E" + str(i)].value  # Должность
        company = sheet["F" + str(i)].value  # Компания
        phone = sheet["G" + str(i)].value  # телефон
        email = sheet["H" + str(i)].value  # e-mail


        if contact == "" or contact == None:  # прерываем перебор и считывание как только пойдут пустые строки
            break

        # создали массив одномерный для записи "строки" в большой массив
        inn = "" # поле для ИНН
        comment = "" # поле для комментария
        new_str = [contact, second_name, first_name, patronymic, post, company, phone, email, inn, comment]

        # n_str = [post]

        # print("new str", new_str)
        # print("n_str", post)

        contacts.append(new_str)  # Добавление в массив новой строки-массива
        i += 1

    print(contacts)
    print("длина массива = ", len(contacts))

    settings.data_dict = list(contacts)


    return contacts

