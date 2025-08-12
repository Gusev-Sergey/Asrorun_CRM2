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




def show_contacts_in_window(root, str_entry):

    data_to_show = settings.data_dict # это и есть список основной базы...
    print("data_to_show",data_to_show)

    font_style = ("Tahoma", 12)

    label_style = ttk.Style()
    label_style.configure("My.TLabel",  # имя стиля
                          font="Tahoma 12",  # шрифт
                          foreground="black",  # цвет текста
                          padding=1,  # отступы
                          background="#D9DCE0",# фоновый цве
                          borderwidth=1)

    ################################################
    # проверка на существование фремов
    ################################################

    # Проверка существования фреймов. Если сущестуют, то удаляем
    if "frame_top" in root.children:
        root.nametowidget("frame_top").destroy()

    if "frame_main" in root.children:
        root.nametowidget("frame_main").destroy()




    if data_to_show == []:
        print("База контактов должна быть загружена")
        data_to_show = ["", "", "", "", "", "", "", "", "", "", ""]
        # showwarning(title="Предупреждение", message="База контактов должна быть сначала загружена")
        # return



    ################################################
    # Верхний фрейм
    ################################################

    frame = ttk.Frame(name="frame_top", borderwidth=1, relief=SOLID, padding=[8, 8], width=600, height=60)
    name_label = ttk.Label(frame, text="Строка поиска")
    name_label.pack(anchor=NW)

    name_entry = ttk.Entry(frame, width=50)
    name_entry.insert(0, str_entry) # Вставка пустой строки или заполненной в предыдущем запросе
    name_entry.pack(side=LEFT, anchor=W)
    name_entry.focus_set()

    # Кнопка "Добавить контакт"
    but_add_contact = ttk.Button(frame, text="Добавить контакт", command=lambda: add_new_contact(root))
    but_add_contact.pack(side=LEFT, anchor=W, padx=(20, 0))  # Отступ справа

    frame.pack(anchor=NW, fill=BOTH, padx=5, pady=5)
    frame.pack_propagate(0)


    ################################################
    # Нижний фрейм - блок с контактами
    ################################################

    frame_main = ttk.Frame(name="frame_main", borderwidth=1, relief=SOLID, padding=[8, 8], width=300, height=2200)
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
    tree.column("#1", stretch=True, width=20, anchor='center')
    tree.column("#2", stretch=True, width=200)
    tree.column("#3", stretch=True, width=100)
    tree.column("#4", stretch=True, width=100)
    tree.column("#5", stretch=True, width=100)
    tree.column("#6", stretch=True, width=150)
    tree.column("#7", stretch=True, width=400)
    tree.column("#8", stretch=True, width=100)
    tree.column("#9", stretch=True, width=100)


    # добавляем данные
    for person in data_to_show:
        tree.insert("", END, values=person)

    # добавляем вертикальную прокрутку
    scrollbar = ttk.Scrollbar(master=frame_main, orient=VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.place(relheight=1.0, relwidth=0.02, relx=0.99)

    # Привязываем событие двойного клика мыши к изменению строки
    tree.bind("<Double-1>", lambda event: on_tree_double_click(event, tree, root))
    tree.bind("<Return>", lambda event: on_tree_double_click(event, tree, root))

    # Привязываем событие входа в Entry (СТРОКА ПОИСКА!!!) к изменению строки
    name_entry.bind("<Return>", lambda event: connector01(event, root, frame_main, tree, name_entry))

# пришлось создавать коннектор для передачи значения True  из функции enter_in_entry
def connector01(event, root, frame_main, tree, name_entry):
    x = False
    x = enter_in_entry(event, root, frame_main, tree, name_entry)
    if x == True:
        show_contacts_in_window(root, name_entry.get())




