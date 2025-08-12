from tkinter import ttk, Entry
from tkinter import *
import sqlite3 as sq
import webbrowser
from functions.contacts_show_to_choose import show_contacts_to_choose
from tkinter.messagebox import askyesno, showinfo

data_clients_to_show = []

def clients_show(root, str_entry):


    # Проверка существования фреймов. Если сущестуют, то удаляем
    if "frame_top" in root.children:
        root.nametowidget("frame_top").destroy()

    if "frame_main" in root.children:
        root.nametowidget("frame_main").destroy()

    ################################################
    # Верхний фрейм
    ################################################

    frame = ttk.Frame(name="frame_top", borderwidth=1, relief=SOLID, padding=[8, 8], width=600, height=60)
    name_label = ttk.Label(frame, text="Строка поиска")
    name_label.pack(anchor=NW)

    name_entry = ttk.Entry(frame, width=50)
    name_entry.insert(0, str_entry)  # Вставка пустой строки или заполненной в предыдущем запросе
    name_entry.pack(side=LEFT, anchor=W)
    name_entry.focus_set()

    # Кнопка "Добавить контакт"
    but_add_contact = ttk.Button(frame, text="Добавить контрагента", command=lambda: add_new_client(root))
    but_add_contact.pack(side=LEFT, anchor=W, padx=(20, 0))  # Отступ справа

    frame.pack(anchor=NW, fill=BOTH, padx=5, pady=5)
    frame.pack_propagate(0)

    ################################################
    # Нижний фрейм - блок с контактами
    ################################################

    frame_main = ttk.Frame(name="frame_main", borderwidth=1, relief=SOLID, padding=[8, 8], width=300, height=2200)
    frame_main.pack(anchor=NW, fill=BOTH, padx=5, pady=5, expand=True)
    frame_main.pack_propagate(0)


    # определяем столбцы  short_name, long_name, inn, address, industry, comment, rez1, rez2, rez3
    columns = ("name_id", "short_name", "long_name",  "inn", "address", "industry")
    tree = ttk.Treeview(master=frame_main, columns=columns, show="headings")
    tree.place(relheight=1.0, relwidth=0.995)

    # определяем заголовки столбцов
    tree.heading("name_id", text="name_id", anchor=W)
    tree.heading("short_name", text="Короткое наименование", anchor=W)
    tree.heading("long_name", text="Длинное наименование", anchor=W)
    tree.heading("inn", text="ИНН", anchor=W)
    tree.heading("address", text="Адрес", anchor=W)
    tree.heading("industry", text="Отрасль", anchor=W)


    # Вес колонок для задания ширины через него
    tree.column("#1", stretch=False, width=50, anchor='center')
    tree.column("#2", stretch=True, width=100)
    tree.column("#3", stretch=True, width=350)
    tree.column("#4", stretch=False, width=100, anchor='center')
    tree.column("#5", stretch=True, width=150)
    tree.column("#6", stretch=True, width=1)

    ################################
    # Загружаем БД КЛИЕНТОВ
    ################################
    enter_in_entry_clients(root, frame_main, tree, name_entry)


    # with sq.connect(f"base/base_contacts.db") as con:
    #
    #     cur = con.cursor()
    #
    #     cur.execute("""SELECT * FROM clients ORDER BY short_name""")
    #
    #     # settings.data_dict = cur.fetchall()
    #     data_clients = list(map(list, cur.fetchall()))
    #
    #     print("settings data_ict после загрузки = ", data_clients)
    #
    # con.commit()
    # con.close()

    ################################ END

    # добавляем данные в TREE
    for client in data_clients_to_show:
        tree.insert("", END, values=client)

    # добавляем вертикальную прокрутку
    scrollbar = ttk.Scrollbar(master=frame_main, orient=VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.place(relheight=1.0, relwidth=0.02, relx=0.99)

    # Привязываем событие двойного клика мыши к изменению строки
    tree.bind("<Double-1>", lambda event: on_tree_double_click2(event, tree, root))
    tree.bind("<Return>", lambda event: on_tree_double_click2(event, tree, root))

    # Привязываем событие входа в Entry (СТРОКА ПОИСКА!!!) к изменению строки
    name_entry.bind("<Return>", lambda event: connector_client(event, root, frame_main, tree, name_entry))

    # пришлось создавать коннектор для передачи значения True  из функции enter_in_entry
    def connector_client(event, root, frame_main, tree, name_entry):
        x = False
        x = enter_in_entry_clients(root, frame_main, tree, name_entry)
        if x == True:
            clients_show(root, name_entry.get())

# Создание пользовательской функции для сравнения без учета регистра
def lower_case(text):
    return text.lower()


def enter_in_entry_clients(root, frame_main, tree, name_entry):

    global data_clients_to_show  # Глобальная переменная для передачи выборки КЛИЕНТОВ к показу

    # tree.destroy()
    # frame_main.destroy()

    # Считываем значение поля entry
    query_crm_get = name_entry.get()

    # name_entry.insert(1, query_crm_get)

    with sq.connect(f"base/base_contacts.db") as con:
        # Регистрация пользовательской функции
        con.create_function("lower_case", 1, lower_case)

        cur = con.cursor()

        query_crm = "%" + query_crm_get + "%"

        print(query_crm)

        cur.execute(
            "SELECT * FROM clients WHERE lower_case(short_name) LIKE ? OR lower_case(long_name) LIKE ? OR lower_case(inn) LIKE ? OR lower_case(address) LIKE ? OR lower_case(industry) LIKE ? OR lower_case(comment) LIKE ? ORDER BY short_name",
            (query_crm, query_crm, query_crm, query_crm, query_crm, query_crm))

        data_clients_to_show = list(map(list, cur.fetchall()))


    con.commit()
    con.close()

    return True

# Получаем выбранный элемент из Tree
def on_tree_double_click2(event, tree, root):
    # Получаем выбранный элемент
    selected_item = tree.selection()[0]
    item_values = tree.item(selected_item)['values']

    print("item_value = ", item_values)

    # Получаем name_id из значений TreeView
    name_id = item_values[0]
    print(name_id)
    on_tree_double_click2_1(root, name_id)


def on_tree_double_click2_1(root, name_id):

    # Создание дочернего окна
    # Дочернее окно для корректировки контакта
    son_root = Toplevel(root)
    ww = son_root.winfo_screenwidth()
    wh = son_root.winfo_screenheight()
    w = int(ww * 0.8)
    h = int(wh * 0.7)
    x = int(ww / 2 - w / 2)
    y = int(wh / 2 - h / 2)
    son_root.geometry(f"{w}x{h}+{x}+{y}")
    son_root.title("Карточка клиента")
    son_root.resizable(False, False)
    son_root.focus()

    # # Обработчик закрытия окна
    # son_root.protocol("WM_DELETE_WINDOW", lambda: save_person_one(son_root, fields, item_values))

    # # Получаем выбранный элемент
    # selected_item = tree.selection()[0]
    # item_values = tree.item(selected_item)['values']
    #
    # print("item_value = ", item_values)
    #
    # # Получаем name_id из значений TreeView
    # name_id = item_values[0]
    # print(name_id)

    # Загружаем из БД данные КЛИЕНТА по номеру name_id
    with sq.connect(f"base/base_contacts.db") as con:

        cur = con.cursor()
        cur.execute("""SELECT * FROM clients WHERE name_id = ?""", (name_id,))


        data_one_client0 = list(map(list, cur.fetchall())) #Получем список в списке [[,,,,,]]

        data_one_client = data_one_client0[0] # преобразуем в одномерный список типа [,,,,]

        print("   data_one_client = ", data_one_client)
        # data_one_client = list(map(list, cur.fetchall()))

    con.commit()
    con.close()


    ################################################
    # Верхний фрейм - КАРТОЧКА КЛИЕНТА
    ################################################

    frame = ttk.Frame(son_root, name="frame_top", borderwidth=1, relief=SOLID, padding=[8, 8], width=600)

    # Виджеты в одну строку
    id_label = ttk.Label(frame, text="ID:")
    id_label.pack(side=TOP, anchor=NW)

    id_name = ttk.Entry(frame, name="id_name", width=50)
    id_name.insert(0, data_one_client[0])
    id_name.pack(side=TOP, anchor=NW)
    id_name.config(state="readonly")

    print("data_one_client[0] = ", data_one_client[0])


    # Виджеты ниже один под другим
    short_name_label = ttk.Label(frame, text="Короткое наименование:")
    short_name_label.pack(anchor=NW)

    short_name_entry = ttk.Entry(frame, name="short_name", width=50)
    short_name_entry.insert(0, data_one_client[1])  # Вставка пустой строки или заполненной в предыдущем запросе
    short_name_entry.pack(anchor=NW)

    long_name_label = ttk.Label(frame, text="Длинное наименование:")
    long_name_label.pack(anchor=NW)

    long_name_entry = ttk.Entry(frame, name="long_name", width=len(data_one_client[2]) + 25, justify="left")
    long_name_entry.insert(0, data_one_client[2])  # Вставка пустой строки или заполненной в предыдущем запросе
    long_name_entry.pack(anchor=NW)

    inn_label = ttk.Label(frame, text="ИНН:")
    inn_label.pack(anchor=NW)

    inn_entry = ttk.Entry(frame, name="inn", width=len(data_one_client[3]) + 25, justify="left")
    inn_entry.insert(0, data_one_client[3])  # Вставка пустой строки или заполненной в предыдущем запросе
    inn_entry.pack(anchor=NW)

    address_label = ttk.Label(frame, text="Адрес:")
    address_label.pack(anchor=NW)

    address_entry = ttk.Entry(frame, name="address", width=len(data_one_client[4]) + 25, justify="left")
    address_entry.insert(0, data_one_client[4])  # Вставка пустой строки или заполненной в предыдущем запросе
    address_entry.pack(anchor=NW)

    industry_label = ttk.Label(frame, name="industry", text="Отрасль:")
    industry_label.pack(anchor=NW)

    industry_entry = ttk.Entry(frame, width=len(data_one_client[5]) + 25, justify="left")
    industry_entry.insert(0, data_one_client[5])  # Вставка пустой строки или заполненной в предыдущем запросе
    industry_entry.pack(anchor=NW)

    comment_label = ttk.Label(frame, text="Комментарий по клиенту:")
    comment_label.pack(anchor=NW)

    # Создание поля Text
    comment_client = Text(frame, name="comment", width=max(len(data_one_client[2]) + 25, 62),
                          height=5, wrap="word")
    comment_client.insert('1.0', data_one_client[6])

    # Создание полосы прокрутки
    scrollbar = ttk.Scrollbar(frame, orient=VERTICAL, command=comment_client.yview)
    comment_client.config(yscrollcommand=scrollbar.set)

    # Упаковка виджетов
    comment_client.pack(side=LEFT, fill=BOTH, expand=True)
    scrollbar.pack(side=RIGHT, fill=Y)

    frame.pack(anchor=NW, fill=BOTH, padx=5, pady=5)

    # Создание фрейма для кнопок


    # Создание фрейма для кнопок
    button_frame = ttk.Frame(son_root, name="button_frame", borderwidth=1, relief=SOLID)
    button_frame.pack(side=TOP, anchor=NW, fill=X, padx=4, pady=4)

    # Кнопки
    but_save = ttk.Button(button_frame, text="<Сохранить>", command=lambda: update_client(root, son_root, frame))
    but_save.pack(side=LEFT, anchor=W, padx=(8, 0))  # Отступ справа

    but_link = ttk.Button(button_frame, text="<Связать с контактами>", command=lambda : show_contacts_to_choose(root, "", data_one_client[0], tree_contacts))
    but_link.pack(side=LEFT, anchor=W, padx=(15, 0))

    but_net = ttk.Button(button_frame, text="<Поиск в Яндекс>", command=lambda: search_net(data_one_client))
    but_net.pack(side=LEFT, anchor=W, padx=(15, 0))

    but_delete = ttk.Button(button_frame, text="<Удалить контрагента>", command=lambda: delete_client(root, son_root, data_one_client))
    but_delete.pack(side=LEFT, anchor=W, padx=(15, 0))

    but_cancel = ttk.Button(button_frame, text="<Закрыть>", command=son_root.destroy)
    but_cancel.pack(side=RIGHT, anchor=W, padx=(0, 20))

    # Создание фрейма с контактами
    # contacts_client_frame = ttk.Frame(son_root, name="contacts_client_frame", borderwidth=1, relief=SOLID, height=300)
    #contacts_client_frame = ttk.Frame(son_root, name="contacts_client_frame", borderwidth=1, relief=SOLID)

    # Создание фрейма с контактами
    contacts_client_frame = ttk.Frame(son_root, name="contacts_client_frame", borderwidth=1, relief=SOLID)
    # contacts_client_frame.pack(side=TOP, anchor=NW, fill=X, padx=4, pady=4)  # Изменение размещения
    contacts_client_frame.pack(side=TOP, anchor=NW, fill=X, expand=True, padx=4, pady=4)
    # contacts_client_frame.pack_propagate(0)

    # определяем столбцы
    columns = ("name_id", "contact", "sername", "name", "patron", "post", "company", "phone", "email")

    # Создание Treeview для отображения контактов
    tree_contacts = ttk.Treeview(contacts_client_frame, columns=columns, show="headings")
    tree_contacts.pack(side=LEFT, fill=BOTH, expand=True)


    # Заголовки столбцов
    tree_contacts.heading("name_id", text="ID")
    tree_contacts.heading("contact", text="Контакт")
    tree_contacts.heading("sername", text="Фамилия")
    tree_contacts.heading("name", text="Имя")
    tree_contacts.heading("patron", text="Отчество")
    tree_contacts.heading("post", text="Должность")
    tree_contacts.heading("company", text="Компания")
    tree_contacts.heading("phone", text="Телефон")
    tree_contacts.heading("email", text="Email")

    # Вес колонок для задания ширины через него
    tree_contacts.column("#1", stretch=True, width=20, anchor='center')
    tree_contacts.column("#2", stretch=True, width=200)
    tree_contacts.column("#3", stretch=True, width=100)
    tree_contacts.column("#4", stretch=True, width=100)
    tree_contacts.column("#5", stretch=True, width=100)
    tree_contacts.column("#6", stretch=True, width=150)
    tree_contacts.column("#7", stretch=True, width=400)
    tree_contacts.column("#8", stretch=True, width=100)
    tree_contacts.column("#9", stretch=True, width=100)

    # Загрузка БД - выборка по id

    with sq.connect(f"base/base_contacts.db") as con:

        cur = con.cursor()

        id_search = data_one_client[0]

        cur.execute("""SELECT * FROM bcontacts WHERE link_to_client = ?""", (id_search,))



        # settings.data_dict = cur.fetchall()
        contacts_in_client = list(map(list, cur.fetchall()))

        print("contacts_in_client = ", contacts_in_client)

    con.commit()
    con.close()



    # добавляем данные
    for person in contacts_in_client:
        tree_contacts.insert("", END, values=person)

    # Обновление интерфейса
    tree_contacts.update_idletasks()

    # Установка высоты Treeview в зависимости от количества строк
    tree_contacts.config(height=len(contacts_in_client))



    # Создание стиля для полосы прокрутки
    style = ttk.Style()
    style.configure("Custom.Vertical.TScrollbar", gripcount=0, arrowsize=20, background="gray", bordercolor="black",
                    troughcolor="lightgray")

    # Добавление полосы прокрутки
    scrollbar = ttk.Scrollbar(contacts_client_frame, orient=VERTICAL, command=tree_contacts.yview,
                              style="Custom.Vertical.TScrollbar")
    scrollbar.pack(side=RIGHT, fill=Y, expand=True)

    tree_contacts.configure(yscrollcommand=scrollbar.set)


def add_new_client(root):
    #################################
    # Открываем существующий файл XLS  #
    #################################

    clients = []  # Массив

    ############################################
    # Открыть БД для работы
    ############################################

    with sq.connect(f"base/base_contacts.db") as con:
        cur = con.cursor()


    short_name = ""  # 1) Короткое название контрагента
    long_name = ""  # 2) Длинное наименование
    inn = ""  # 3) ИНН
    address = ""  # 4) Адрес
    industry = ""  # 5) Отрасль


    # создаем массив одномерный для записи "строки" в большой массив

    rez1 = ""  # поле резервное 1
    rez2 = ""  # поле резервное 2
    rez3 = ""  # поле резервное 3

    comment = ""  # поле для комментария 7) поле

    new_str = [short_name, long_name, inn, address, industry, comment, rez1, rez2, rez3]

    print("new_ str", new_str)

    ################################################
    # ДОБАВЛЯЕМ строку в БД!
    ################################################

    cur.execute(
        "INSERT INTO clients (short_name, long_name, inn, address, industry, comment, rez1, rez2, rez3) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
        new_str)
    last_id = cur.lastrowid

    con.commit()
    con.close()

    # showinfo("Результат", f"{i} Контрагентов добавлены в базу данных")

    on_tree_double_click2_1(root, last_id)





# Сохранение изменений контрагента
def update_client(root, son_root, frame):

    id_name = frame.nametowidget("id_name").get()
    short_name = frame.nametowidget("short_name").get()
    long_name = frame.nametowidget("long_name").get()
    inn = frame.nametowidget("inn").get()
    address = frame.nametowidget("address").get()
    comment = frame.nametowidget("comment").get("1.0", "end-1c")

    print(id_name, short_name, long_name, inn, address, comment)


    with sq.connect(f"base/base_contacts.db") as con:

        cur = con.cursor()
        cur.execute("""UPDATE clients SET short_name = ?,  long_name = ?, inn = ?, address = ?, comment = ? WHERE name_id = ?""", (short_name, long_name, inn, address, comment, id_name))


    con.commit()
    con.close()

    son_root.destroy()
    clients_show(root, "")

# Удалить контрагента
def delete_client(root, son_root, data_one_client):

    result = askyesno(title="Подтвердите удаление", message="Вы уверены?")

    if result:
        showinfo("Результат", "Операция подтверждена")
        name_id_client_to_del = data_one_client[0]

        # Открываем соединение с базой данных
        with sq.connect("base/base_contacts.db") as con:
            cursor = con.cursor()

            # Удаление контакта по id_name
            cursor.execute("DELETE FROM clients WHERE name_id = ?", (name_id_client_to_del,))

            # Фиксация изменений
            con.commit()

        print(f"Клиент с id {name_id_client_to_del} удален из базы данных.")

    else:
        showinfo("Результат", "Операция отменена")

    son_root.destroy()

    clients_show(root, "")




# Поиск в сети
def search_net(data_one_client):
    # Пример данных
    short_name = data_one_client[1]
    inn = data_one_client[3]

    # Формирование поискового запроса
    search_query = short_name + " ИНН " + inn

    # Открытие поисковой страницы в Яндекс
    webbrowser.open_new(f"https://yandex.ru/search/?text={search_query}")