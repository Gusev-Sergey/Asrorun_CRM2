from openpyxl import load_workbook
from tkinter.filedialog import askopenfilename  #Вызывает диалог на получения пути к файлу
import sqlite3 as sq

from tkinter import ttk, Entry
from tkinter import *
from tkinter.messagebox import showinfo

import settings

class Error(Exception):  # Базовый класс для других исключений
    pass

class Notfoundfile(Error):
    pass


def import_xlsx_clients_check(root):

    # Дочернее окно для ВЫБОРА И СВЯЗЫВАНИЯ контакта с КЛИЕНТОМ
    son_root_check = Toplevel(root)

    ww = son_root_check.winfo_screenwidth()
    wh = son_root_check.winfo_screenheight()
    w = int(ww * 0.9)
    h = int(wh * 0.4)
    x = int(ww / 2 - w / 2)
    y = int(wh / 2 - h / 2)
    son_root_check.geometry(f"{w}x{h}+{x}+{y}")
    son_root_check.title("Добавление контрагентов")
    son_root_check.resizable(False, False)
    son_root_check.focus()


    ######################
    # ВЫБОР файла xls
    ######################

    mypath_import = "."

    try:
        way = askopenfilename(title="Выберите файл", initialdir=mypath_import,
                          filetypes=[("Files *.xlsx", ".xlsx .xls")])

        if way == "":
            raise Notfoundfile

    except Notfoundfile:
        # print("ЗАШЛИ В ИСКЛЮЧЕНИЕ")

        way = askopenfilename(title="Файл .xls с данными не обнаружен. Выберите файл", initialdir=mypath_import,
                              filetypes=[("Files *.xlsx", ".xlsx .xls")])
        return
    import_xlsx_clients_check_next(son_root_check, way)

def import_xlsx_clients_check_next(son_root_check, way):

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

    # with sq.connect(f"base/base_contacts.db") as con:
    #     cur = con.cursor()




    i = 1  # первая строка для перебора всех строк файла загрузки. Начинаем с первой строки
    while True:
        # Структура xls для загрузки клиентов

        short_name = sheet["A" + str(i)].value  # 1) Короткое название контрагента
        long_name = sheet["B" + str(i)].value   # 2) Длинное наименование
        inn = sheet["C" + str(i)].value         # 3) ИНН
        address = sheet["D" + str(i)].value     # 4) Адрес
        industry = sheet["E" + str(i)].value    # 5) Отрасль
        comment = sheet["F" + str(i)].value  # поле для комментария 7) поле

        rez1 = "" # поле резервное 1
        rez2 = "" # поле резервное 2
        rez3 = "" # поле резервное 3

        if long_name == None:
            long_name = ""

        if inn == None:
            inn = ""

        if address == None:
            address = ""

        if industry == None:
            industry = ""

        if comment == None:
            comment = ""

        if short_name == "" or short_name == None:
            showinfo(title="Информация по импорту контрагентов", message="Достигнут конец файла")
            son_root_check.destroy()
            break


        # создаем массив одномерный для записи "строки" в большой массив
        new_str = [short_name, long_name, inn, address, industry, comment, rez1, rez2, rez3]

        print("new_ str", new_str)

        ################################################
        # Ищем клиента в БД!
        ################################################

        # Загружаем из БД данные КЛИЕНТА по номеру name_id
        with sq.connect(f"base/base_contacts.db") as con:
            cur = con.cursor()
            cur.execute("""SELECT * FROM clients WHERE inn = ?""", (inn,))

            data_research = cur.fetchall()
            print("data_research ", data_research)

            data_one_client0 = list(map(list, data_research))  # Получем список в списке [[,,,,,]]

            print("data_one_client0 ", data_one_client0)

            con.commit()
            # con.close()



            if data_one_client0 == []:

                with sq.connect(f"base/base_contacts.db") as con2:
                    cursor = con2.cursor()

                    # Если нет клиента с таким ИНН, то делаем запись
                    cursor.execute(
                        "INSERT INTO clients (short_name, long_name, inn, address, industry, comment, rez1, rez2, rez3) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                        new_str)

                    con2.commit()
                    # con2.close()
                    i += 1
                    continue

            else:

                # data_one_client0 = list(map(list, cur.fetchall()))  # Получем список в списке [[,,,,,]]
                data_one_client = data_one_client0[0]  # преобразуем в одномерный список типа [,,,,]

                print("into db from xls: data_one_client = ", data_one_client)
                # data_one_client = list(map(list, cur.fetchall()))

                show_new_and_old_client(son_root_check, new_str, data_one_client, i)
                # Ожидаем закрытия окна son_root_check
                son_root_check.nametowidget("frame_top").wait_window()

                # con.commit()
                # con.close()





        # show_new_and_old_client(son_root_check, new_str, data_one_client, i)

        i += 1



        if not son_root_check.winfo_exists():
            break

        # son_root_check.destroy()

        # cur.execute(
        #     "INSERT INTO clients (short_name, long_name, inn, address, industry, comment, rez1, rez2, rez3) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
        #     new_str)
        # contacts.append(new_str)  # Добавление в массив новой строки-массива

    # con.commit()
    # con.close()
    # showinfo("Результат", f"{i} Контрагентов добавлены в базу данных")


def show_new_and_old_client(son_root_check, new_str, data_one_client, number_client):

    # Проверка существования фреймов. Если сущестуют, то удаляем
    if "frame_top" in son_root_check.children:
        son_root_check.nametowidget("frame_top").destroy()

    if "frame_bot" in son_root_check.children:
        son_root_check.nametowidget("frame_bot").destroy()


    frame_top = ttk.Frame(son_root_check, name="frame_top", borderwidth=1, relief=SOLID, padding=[8, 8], width=600, height=60)
    frame_top.pack(anchor=NW, fill=BOTH, padx=5, pady=5)
    frame_top.pack_propagate(0)

    button_frame = ttk.Frame(son_root_check, name="frame_bot", borderwidth=1, relief=SOLID, padding=[8, 8], width=600, height=60)
    button_frame.pack(anchor=NW, fill=BOTH, padx=5, pady=5)
    button_frame.pack_propagate(0)

    info_frame = ttk.Frame(son_root_check, name="info", borderwidth=1, relief=SOLID, padding=[8, 8], width=600, height=60)
    info_frame.pack(anchor=NW, fill=BOTH, padx=5, pady=5)

    son_root_check.focus()

    # ======================================================================================================

    label_left = ttk.Label(frame_top, width=50, text="Контрагент в базе данных", font="Tahoma 12 bold")
    label_left.grid(row=0, column=0, sticky="ew")

    label_right = ttk.Label(frame_top, width=50, text="Новый клиент из файла", font="Tahoma 12 bold")
    label_right.grid(row=0, column=1, sticky="ew")

    # Формируем поля ввода/ new_str = [short_name, long_name, inn, address, industry, comment, rez1, rez2, rez3]

    new_str.insert(0, "")

    for i in range(7):

        if i != 6:

            entry = ttk.Entry(frame_top, name=f"entry_left_{i}",
                              width=max(len(str(data_one_client[i])), len(str(new_str[i]))),
                              justify="left")
            entry.insert(0, data_one_client[i])
            entry.grid(row=i + 1, column=0, sticky="ew")

            entry = ttk.Entry(frame_top, name=f"entry_right_{i}",
                              width=max(len(str(data_one_client[i])), len(str(new_str[i]))),
                              justify="left")
            entry.insert(0, new_str[i])
            entry.grid(row=i + 1, column=1, sticky="ew")

        else:

            comment_client = Text(frame_top, name=f"entry_left_{i}", width=max(len(data_one_client[2]) + 25, 62),
                                  height=5, wrap="word")
            comment_client.insert('1.0', data_one_client[i])
            comment_client.grid(row=i + 1, column=0, sticky="ew")

            comment_client_right = Text(frame_top, name=f"entry_right_{i}", width=max(len(data_one_client[2]) + 25, 62),
                                  height=5, wrap="word")
            comment_client_right.insert('1.0', new_str[i])
            comment_client_right.grid(row=i + 1, column=1, sticky="ew")

    ########
    # Кнопки
    but_save = ttk.Button(button_frame, text="<Сохранить из старого>", command=lambda: update_client_2(son_root_check, frame_top))
    but_save.pack(side=LEFT, anchor=W, padx=(5, 0))  # Отступ справа

    but_link = ttk.Button(button_frame, text="<Добавить нового>", command=lambda: new_client(son_root_check, frame_top))
    but_link.pack(side=LEFT, anchor=W, padx=(10, 0))

    but_next = ttk.Button(button_frame, text="<Следующий>",
                          command=frame_top.destroy)
    but_next.pack(side=LEFT, anchor=W, padx=(10, 0))

    but_exit = ttk.Button(button_frame, text="<Прервать>", command=son_root_check.destroy)
    but_exit.pack(side=RIGHT, anchor=W, padx=(0, 10))

    info_label = ttk.Label(info_frame, width=50, text="Номер записи из файла xlsx: " + str(number_client))
    info_label.pack(side=LEFT, anchor=W, padx=(0, 10))

# Сохранить нового клиента
def new_client(son_root_check, frame_top):

    new_value = []
    for i in range(7):

        name_right = f"entry_right_{i}"

        if i != 6:

            new_one = frame_top.nametowidget(name_right).get()
            new_value.append(new_one)

        else:
            comment_get = frame_top.nametowidget(name_right).get("1.0", "end-1c")
            new_value.append((comment_get))

# ############################################
#     for i in range(7):
#
#         name_right = f"entry_right_{i}"
#
#         new_one = frame_top.nametowidget(name_right).get()
#         new_value.append(new_one)

    print("new_value ", new_value)

    new_str = [new_value[1], new_value[2], new_value[3],  new_value[4], new_value[5], new_value[6], "", "", ""]



########################################











    with sq.connect(f"base/base_contacts.db") as con:

        cur = con.cursor()

        # cur.execute("""UPDATE clients SET short_name = ?,  long_name = ?, inn = ?, address = ?, industry = ? WHERE name_id = ?""", (new_value[1], new_value[2], new_value[3], new_value[4], new_value[5], new_value[0]))

        cur.execute(
            "INSERT INTO clients (short_name, long_name, inn, address, industry, comment, rez1, rez2, rez3) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            new_str)

    con.commit()
    con.close()

    frame_top.destroy()


# Обновить данный у старого клиента
def update_client_2(son_root_check, frame_top):

    new_value = []

    for i in range(7):

        name_left = f"entry_left_{i}"

        if i !=6:


            new_one = frame_top.nametowidget(name_left).get()
            new_value.append(new_one)

        else:
            comment_get = frame_top.nametowidget(name_left).get("1.0", "end-1c")
            new_value.append((comment_get))


    print("new_value ", new_value)

    with sq.connect(f"base/base_contacts.db") as con:


        cur = con.cursor()
        cur.execute("""UPDATE clients SET short_name = ?,  long_name = ?, inn = ?, address = ?, industry = ?, comment = ? WHERE name_id = ?""", (new_value[1], new_value[2], new_value[3], new_value[4], new_value[5], new_value[6],new_value[0]))

    con.commit()
    con.close()

    frame_top.destroy()







