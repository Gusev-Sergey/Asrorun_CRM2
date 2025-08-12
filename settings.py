data_dict = []

from dataclasses import fields
from tkinter import ttk, Entry
from tkinter import *
from tkinter import simpledialog  # Импортируем simpledialog
import settings
from tkinter import StringVar
import sqlite3 as sq


# # Подключение к базе данных (правильный путь к файлу)
# conn = sq.connect("base/base_contacts 04.db")
# cursor = conn.cursor()

# Глобальная переменная подключения к базе данных
global_conn = None



# entry_var = StringVar()

def on_tree_double_click(event, tree, root):

    # Дочернее окно для проверки правильности экспорта словаря
    son_root = Toplevel(root)
    ww = son_root.winfo_screenwidth()
    wh = son_root.winfo_screenheight()
    w = int(ww * 0.3)
    h = int(wh * 0.47)
    x = int(ww / 2 - w / 2)
    y = int(wh / 2 - h / 2)
    son_root.geometry(f"{w}x{h}+{x}+{y}")
    son_root.title("Корректировка контакта")
    son_root.resizable(False, False)
    son_root.focus()

    son_root.protocol("WM_DELETE_WINDOW", lambda: save_person(son_root, fields, entries_vars, tree, selected_item))  # Обработчик закрытия окна

    # Получаем выбранный элемент.
    selected_item = tree.selection()[0]
    item_values = tree.item(selected_item)['values']


    fields = ["Контакт", "Имя", "Фамилия", "Отчество", "Должность", "Компания", "Телефон", "Email"]

    entries_vars = []  # Список для хранения переменных каждого поля
    # Переменная StringVar для хранения текущего состояния поля ввода


    # Теперь будем создавать метки для каждого поля
    for field_name, value in zip(fields, item_values):
        label = ttk.Label(son_root, text=f"{field_name}", wraplength=int(w-15))

        # Отдельная переменная StringVar для каждого поля
        var = StringVar(value=value)
        entries_vars.append(var)


        entry = ttk.Entry(son_root, width=max(max([len(str(v)) for v in item_values]) + 5, 62), justify="left", textvariable=var)
        # entry.insert(0, value)

        label.pack(padx=10, pady=5, anchor="nw")
        entry.pack(padx=10, pady=0, anchor="nw")




    # Создаем кнопку для сохранения данных
    but = ttk.Button(son_root, text="Сохранить", command=lambda: save_person(son_root, fields, entries_vars, tree, selected_item))
    but.pack(padx=10, pady=15, anchor="sw")


def save_person(son_root, fields, entries_vars, tree, selected_item):
    """
    Сохраняет изменённые данные из полей ввода и обновляет дерево.
    :param son_root: дочернее окно
    :param fields: список названий полей
    :param entries_vars: список переменных StringVar
    :param tree: дерево TreeView
    :param selected_item: выбранный элемент
    """
    # Проверяем состояние соединения с базой данных и открываем его, если нужно
    open_connection()

    # Продолжаем с основным кодом
    saved_data = {}
    for field_name, var in zip(fields, entries_vars):
        value = var.get()
        saved_data[field_name.strip(':')] = value
        print(f"{field_name}: {value}")

    # Здесь обновляем дерево с новыми значениями
    update_tree_with_new_data(tree, selected_item, saved_data)

    # Закрываем окно после сохранения
    son_root.destroy()

    # Закрываем соединение с базой данных после выполнения операций
    close_connection()

def open_connection():
    """Открывает соединение с базой данных, если оно закрыто."""
    global global_conn
    if global_conn is None or test_connection(global_conn):  # Проверяем состояние соединения
        global_conn = sq.connect("base/base_contacts 04.db")
        print("Соединение с базой данных открыто.")
    else:
        print("Соединение уже активно.")

def close_connection():
    """Закрывает открытое соединение с базой данных."""
    global global_conn
    if global_conn is not None:
        global_conn.close()
        print("Соединение с базой данных закрыто.")

def test_connection(connection):
    """Проверяет, открыто ли соединение, выполняя простой запрос."""
    try:
        connection.execute("SELECT 1")
        return False  # Соединение открыто
    except sq.ProgrammingError:
        return True  # Соединение закрыто

def update_tree_with_new_data(tree, selected_item, saved_data):
    """
    Обновляет дерево с новыми значениями и одновременно обновляет базу данных.
    :param tree: дерево (TreeView)
    :param selected_item: выбранный элемент
    :param saved_data: словарь с новой информацией
    """
    # Получаем активный объект соединения с базой данных
    global global_conn

    # Проверяем, открыто ли соединение
    if global_conn is None or test_connection(global_conn):
        print("Ошибка: Нет активного соединения с базой данных.")
        return

    # Создаем курсор на основе текущего соединения
    cursor = global_conn.cursor()

    # Получаем уникальный идентификатор записи
    record_id = tree.item(selected_item, "text")  # Предполагается, что в тексте содержится ID записи

    # Формируем запрос на обновление данных
    sql_update_query = f"""
        UPDATE bcontacts SET
            contact = ?,
            first_name = ?,
            second_name = ?,
            patronymic = ?,
            post = ?,
            company = ?,
            phone = ?,
            email = ?
        WHERE name_id = ?
    """

    # Собираем массив значений для обновления
    new_values = [
        saved_data.get("Контакт"),
        saved_data.get("Имя"),
        saved_data.get("Фамилия"),
        saved_data.get("Отчество"),
        saved_data.get("Должность"),
        saved_data.get("Компания"),
        saved_data.get("Телефон"),
        saved_data.get("Email"),
        record_id
    ]

    # Выполняем запрос на обновление в базе данных
    cursor.execute(sql_update_query, new_values)
    global_conn.commit()  # Фиксируем изменения


