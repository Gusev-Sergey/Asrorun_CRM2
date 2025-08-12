from doctest import master

from tkinter import ttk, Entry
from tkinter import *
from xmlrpc.client import FastParser
import settings

from functions.import_xlsx_without import *
from functions.new_value_in_contact import *
from functions.enter_in_entry import *
from functions.add_new_contact import *
from tkinter.messagebox import showwarning

data_contact_to_show = []


def show_contacts_to_choose(root, str_entry, id_client, tree_contacts):

    # Дочернее окно для ВЫБОРА И СВЯЗЫВАНИЯ контакта с КЛИЕНТОМ
    son_root2 = Toplevel(root)
    ww = son_root2.winfo_screenwidth()
    wh = son_root2.winfo_screenheight()
    w = int(ww * 0.8)
    h = int(wh * 0.7)
    x = int(ww / 2 - w / 2)
    y = int(wh / 2 - h / 2)
    son_root2.geometry(f"{w}x{h}+{x}+{y}")
    son_root2.title("Выбор контакта")
    son_root2.resizable(False, False)
    son_root2.focus()
    show_contacts_to_choose_next(son_root2,root, str_entry, id_client, tree_contacts)

def show_contacts_to_choose_next(son_root2, root, str_entry, id_client, tree_contacts):

    global data_contact_to_show

    ################################################
    # проверка на существование фремов
    ################################################

    # Проверка существования фреймов. Если сущестуют, то удаляем
    if "frame_top" in son_root2.children:
        son_root2.nametowidget("frame_top").destroy()

    if "frame_main" in son_root2.children:
        son_root2.nametowidget("frame_main").destroy()


    #  ФРЕЙМЫ, виджеты==============================
    ################################################
    # Верхний фрейм
    ################################################

    frame = ttk.Frame(son_root2, name="frame_top", borderwidth=1, relief=SOLID, padding=[8, 8], width=600, height=60)
    name_label = ttk.Label(frame, text="Строка поиска")
    name_label.pack(anchor=NW)

    name_entry = ttk.Entry(frame, width=50)
    name_entry.insert(0, str_entry) # Вставка пустой строки или заполненной в предыдущем запросе
    name_entry.pack(side=LEFT, anchor=W)
    name_entry.focus_set()

    # Метка - сообщение "выбрать контакт"
    label_choose = ttk.Label(frame, text="Найдите и выберите контакт для связи с контрагентом")
    label_choose.pack(side=LEFT, anchor=W, padx=(20, 0))

    # but_add_contact = ttk.Button(frame, text="Добавить контакт", command=lambda: add_new_contact(root))
    # but_add_contact.pack(side=LEFT, anchor=W, padx=(20, 0))  # Отступ справа

    frame.pack(anchor=NW, fill=BOTH, padx=5, pady=5)
    frame.pack_propagate(0)


    ################################################
    # Нижний фрейм - блок с контактами
    ################################################

    frame_main = ttk.Frame(son_root2, name="frame_main", borderwidth=1, relief=SOLID, padding=[8, 8], width=300, height=2200)
    frame_main.pack(anchor=NW, fill=BOTH, padx=5, pady=5, expand=True)
    frame_main.pack_propagate(0)
    # input_entry = ttk.Entry(name="entry_to_search", font=font_style, style="My.TLabel")

    # определяем столбцы
    columns = ("name_id", "contact", "sername", "name", "patron", "post", "company", "phone", "email")
    tree = ttk.Treeview(master=frame_main, columns=columns, show="headings")
    tree.place(relheight=1.0, relwidth=0.995)


    # определяем заголовки столбцов
    tree.heading("name_id", text="name_id", anchor=W)
    tree.heading("contact", text="Контакт", anchor=W)
    tree.heading("sername", text="Фамилия", anchor=W)
    tree.heading("name", text="Имя", anchor=W)
    tree.heading("patron", text="Отчество", anchor=W)
    tree.heading("post", text="Должность", anchor=W)
    tree.heading("company", text="Компания", anchor=W)
    tree.heading("phone", text="Телефон", anchor=W)
    tree.heading("email", text="E-mail", anchor=W)

    # Вес колонок для задания ширины через него
    tree.column("#1", stretch=True, width=50, anchor='center')
    tree.column("#2", stretch=True, width=200)
    tree.column("#3", stretch=True, width=100)
    tree.column("#4", stretch=True, width=100)
    tree.column("#5", stretch=True, width=100)
    tree.column("#6", stretch=True, width=150)
    tree.column("#7", stretch=True, width=400)
    tree.column("#8", stretch=True, width=100)
    tree.column("#9", stretch=True, width=100)

    # загружаем БД по запросу
    enter_in_entry_clients(root, son_root2, name_entry)
    data_to_show = data_contact_to_show

    # добавляем данные
    for person in data_to_show:
        tree.insert("", END, values=person)

    # добавляем вертикальную прокрутку
    scrollbar = ttk.Scrollbar(master=frame_main, orient=VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.place(relheight=1.0, relwidth=0.02, relx=0.99)

    # Привязываем событие двойного клика мыши к изменению строки
    tree.bind("<Double-1>", lambda event: on_tree_double_click3(event, tree, son_root2, id_client, tree_contacts))
    tree.bind("<Return>", lambda event: on_tree_double_click3(event, tree, son_root2, id_client, tree_contacts))

    # Привязываем событие входа в Entry (СТРОКА ПОИСКА!!!) к изменению строки
    name_entry.bind("<Return>", lambda event: connector_contacts2(son_root2, root, name_entry, id_client, tree_contacts))

# пришлось создавать коннектор для передачи значения True  из функции enter_in_entry
def connector_contacts2(son_root2, root, name_entry, id_client, tree_contacts):
    x = False
    x = enter_in_entry_clients(root, son_root2, name_entry)
    if x == True:
        show_contacts_to_choose_next(son_root2, root, name_entry.get(), id_client, tree_contacts)
        # show_contacts_to_choose_next(son_root2, root, str_entry, id_client, tree_contacts)


# Создание пользовательской функции для сравнения без учета регистра
def lower_case(text):
    return text.lower()


def enter_in_entry_clients(root, son_root2, name_entry):

    global data_contact_to_show  # Глобальная переменная для передачи выборки КЛИЕНТОВ к показу

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
            "SELECT * FROM bcontacts WHERE lower_case(contact) LIKE ? OR lower_case(second_name) LIKE ? OR lower_case(first_name) LIKE ? OR lower_case(patronymic) LIKE ? OR lower_case(company) LIKE ? ORDER BY contact",
            (query_crm, query_crm, query_crm, query_crm, query_crm))

        data_contact_to_show = list(map(list, cur.fetchall()))

    con.commit()
    con.close()

    return True



#on_tree_double_click3(event, tree, son_root2, id_client, tree_contacts)

def on_tree_double_click3(event, tree, son_root2, id_client, tree_contacts):
    # Получаем выбранный элемент из Tree

    print("tree_ = ", tree)

    selected_item = tree.selection()[0]
    item_values = tree.item(selected_item)['values']

    # Получаем name_id из значений TreeView (список контактов)
    name_id = item_values[0]

    print("name_id = ", name_id)
    print(type(name_id))

    # Внести правку - установить связь в контрагенте
    # cursor.execute('UPDATE users SET age = ? WHERE name = ?', (new_age, user_name))
    # Загружаем из БД данные КЛИЕНТА по номеру name_id
    with sq.connect(f"base/base_contacts.db") as con:
        cur = con.cursor()

        cur.execute("""UPDATE bcontacts SET link_to_client = ? WHERE name_id = ?""", (id_client, name_id,))
        # cursor.execute('UPDATE users SET age = ? WHERE name = ?', (new_age, user_name))

        data_to_show = list(map(list, cur.fetchall()))  # Получем список в списке [[,,,,,]]

    con.commit()
    con.close()

    son_root2.destroy()

    # Очистили Tree

    tree_contacts.delete(*tree_contacts.get_children())


    # print("name_id ",name_id)
    # a = input("1")


    # Загрузка БД - выборка по id

    with sq.connect(f"base/base_contacts.db") as con:

        cur = con.cursor()

        cur.execute("""SELECT * FROM bcontacts WHERE link_to_client = ?""", (id_client,))



        # settings.data_dict = cur.fetchall()
        contacts_in_client = list(map(list, cur.fetchall()))

        print("contacts_in_client = ", contacts_in_client)

    con.commit()
    con.close()

    # a = input("2")



    # добавляем данные
    for person in contacts_in_client:
        tree_contacts.insert("", END, values=person)

    # Обновление интерфейса
    tree_contacts.update_idletasks()

    # Установка высоты Treeview в зависимости от количества строк
    tree_contacts.config(height=len(contacts_in_client))



    # # Создание стиля для полосы прокрутки
    # style = ttk.Style()
    # style.configure("Custom.Vertical.TScrollbar", gripcount=0, arrowsize=20, background="gray", bordercolor="black",
    #                 troughcolor="lightgray")
    #
    # # Добавление полосы прокрутки
    # scrollbar = ttk.Scrollbar(cont, orient=VERTICAL, command=tree.yview,
    #                           style="Custom.Vertical.TScrollbar")
    # scrollbar.pack(side=RIGHT, fill=Y, expand=True)
    #
    # tree.configure(yscrollcommand=scrollbar.set)









