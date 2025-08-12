from tkinter import ttk, Entry
from tkinter import *
from tkinter import simpledialog  # Импортируем simpledialog
from tkinter import StringVar
import sqlite3 as sq
import settings
from functions.update_to_show import update_to_show


# Глобальных переменных для базы данных больше нет
def add_new_contact(root):
    # Дочернее окно для корректировки контакта
    son_root = Toplevel(root)
    ww = son_root.winfo_screenwidth()
    wh = son_root.winfo_screenheight()
    w = int(ww * 0.3)
    h = int(wh * 0.7)
    x = int(ww / 2 - w / 2)
    y = int(wh / 2 - h / 2)
    son_root.geometry(f"{w}x{h}+{x}+{y}")
    son_root.title("Новый контакт")
    son_root.resizable(False, False)
    son_root.focus()

    # Обработчик закрытия окна
    son_root.protocol("WM_DELETE_WINDOW", lambda: save_person_one(son_root, fields, item_values))

    # # Получаем выбранный элемент
    # selected_item = tree.selection()[0]
    # item_values = tree.item(selected_item)['values']

    # Все поля пустые
    item_values = ["", "", "", "", "", "", "", "", "", "", ""]

    fields = ["name_id", "Контакт", "Фамилия", "Имя", "Отчество", "Должность", "Компания", "Телефон", "Email", "ИНН", "Комментарий"]

    # Формируем поля ввода
    counter = 0  # Счётчик для именования виджетов
    for field_name, value in zip(fields, item_values):
        label = ttk.Label(son_root, text=f"{field_name}", wraplength=int(w - 15))
        label.pack(padx=10, pady=5, anchor="nw")

        if field_name == "Комментарий":
            comment_edit = Text(son_root, name=f"entry_{counter}",
                                width=max(max([len(str(v)) for v in item_values]) + 5, 62),
                                height=5, wrap="word")
            comment_edit.insert('1.0', str(value))
            comment_edit.pack(padx=10, pady=0, anchor="nw")
        else:
            entry = ttk.Entry(son_root, name=f"entry_{counter}",
                              width=max(max([len(str(v)) for v in item_values]) + 5, 62),
                              justify="left")
            entry.insert(0, str(value))

            if field_name == "name_id":
                entry.config(state="readonly")  # Устанавливаем состояние readonly после вставки текста
            else:
                entry.config(state="normal")

            entry.pack(padx=10, pady=0, anchor="nw")
        counter += 1

    # Кнопка "Сохранить"
    but = ttk.Button(son_root, text="Сохранить", command=lambda: save_person_one (root, son_root, fields, item_values))
    but.pack(side=LEFT, padx=10, pady=15, anchor="sw")

    # ====================

    # Кнопка "Добавить контакт"
    delete_contact = ttk.Button(son_root, text="Отмена",
                                command=lambda: reluctant_new_contact(root, son_root))
    delete_contact.pack(side=LEFT, padx=10, pady=15, anchor="sw")  # Отступ справа

def reluctant_new_contact(root, son_root):
    #  Обноление
    update_to_show(root)
    son_root.destroy()




def save_person_one(root, son_root, fields, item_values):
    val_all = []  # Массив для всех значений в строке

    # Получаем данные из полей и сохраняем их в массив val_all
    counter = 0  # Счётчик для сопоставления с именами виджетов
    for field_name in fields:
        widget_name = f"entry_{counter}"  # Получаем имя виджета по номеру
        widget = son_root.nametowidget(widget_name)  # Получаем виджет по имени

        # Специально обрабатываем комментарий
        if isinstance(widget, Text):
            # Если виджет — это Text, получаем текст особым образом
            value = widget.get("1.0", "end-1c")
        elif field_name == "name_id":
            # Для поля name_id используем исходное значение
            value = item_values[0]  # Используем оригинальный name_id
            print("!! VALUE =======", value)
        else:
            # Для остальных видов (Entry) берем значение обычным способом
            value = widget.get()

        val_all.append(value)  # Добавляем значение в массив
        counter += 1

    print("VAL ALL 2 =====", val_all)


    val_all.pop(0)
    print("VAL ALL 3 =====", val_all)

    # сохранение в БД
    save_new_person_in_bd(val_all)

    # Закрываем окно
    son_root.destroy()

    #  Обноление
    update_to_show(root)





def save_new_person_in_bd(saved_data):

    # Если поле контакт не заполнено, то берем значения из ФИО и суммируем в строку
    if saved_data[0] == "":
        saved_data[0] = saved_data[1] + " " + saved_data[2] + " " + saved_data [3]



    # Открываем временное соединение с базой данных
    with sq.connect("base/base_contacts.db") as con:
        cursor = con.cursor()

        cursor.execute(
            "INSERT INTO bcontacts (contact, second_name, first_name, patronymic, post, company, phone, email, inn, comment) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            saved_data)

        con.commit()
        # con.close()
    print(">> Новый контакт внесен!")














