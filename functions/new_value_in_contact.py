from tkinter import ttk, Entry
from tkinter import *
from tkinter import simpledialog  # Импортируем simpledialog
from tkinter import StringVar
import sqlite3 as sq
import settings
from tkinter.messagebox import askyesno, showinfo



# Глобальных переменных для базы данных больше нет
def on_tree_double_click(event, tree, root):
    # Дочернее окно для корректировки контакта
    son_root = Toplevel(root)
    ww = son_root.winfo_screenwidth()
    wh = son_root.winfo_screenheight()
    w = int(ww * 0.3)
    h = int(wh * 0.7)
    x = int(ww / 2 - w / 2)
    y = int(wh / 2 - h / 2)
    son_root.geometry(f"{w}x{h}+{x}+{y}")
    son_root.title("Корректировка контакта")
    son_root.resizable(False, False)
    son_root.focus()

    # Обработчик закрытия окна
    son_root.protocol("WM_DELETE_WINDOW", lambda: save_person(son_root, fields, tree, selected_item, item_values))

    # Получаем выбранный элемент
    selected_item = tree.selection()[0]
    item_values = tree.item(selected_item)['values']

    # Получаем name_id из значений TreeView
    name_id = item_values[1]

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
    but = ttk.Button(son_root, text="Сохранить", command=lambda: save_person(son_root, fields, tree, selected_item, item_values))
    but.pack(side=LEFT, padx=10, pady=15, anchor="sw")


    # Кнопка "Добавить контакт"
    delete_contact = ttk.Button(son_root, text="Удалить контакт", command=lambda: del_contact(root, son_root, item_values))
    delete_contact.pack(side=LEFT, padx=10, pady=15, anchor="sw")  # Отступ справа


def del_contact(root, son_root, item_values):

    result = askyesno(title="Подтвердите удаление", message="Вы уверены?")


    if result:
        showinfo("Результат", "Операция подтверждена")
        name_id_to_del = item_values[0]

        # Открываем соединение с базой данных
        with sq.connect("base/base_contacts.db") as con:
            cursor = con.cursor()

            # Удаление контакта по id_name
            cursor.execute("DELETE FROM bcontacts WHERE name_id = ?", (name_id_to_del,))

            # Фиксация изменений
            con.commit()

        print(f"Контакт с id {name_id_to_del} удален из базы данных.")

    else:
        showinfo("Результат", "Операция отменена")

    son_root.destroy()

    # сохранение в БД
    from functions.update_to_show import update_to_show
    #  Обноление
    update_to_show(root)










    pass





def save_person(son_root, fields, tree, selected_item, item_values):
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

    # Обновляем TreeView
    tree.item(selected_item, values=val_all)  # Обновляем строку в TreeView

    # сохранение в БД
    save_bd(tree, selected_item, val_all)

    # Закрываем окно
    son_root.destroy()

    print("Данные успешно обновлены в TreeView!")

def save_bd(tree, selected_item, saved_data):

    # print("SAVED_DATA:", saved_data[8])

    # Открываем временное соединение с базой данных
    with sq.connect("base/base_contacts.db") as con:
        cursor = con.cursor()

        # Получаем уникальный идентификатор записи из скрытого поля
        # record_id = int(selected_item[1:])
        # record_id = selected_item[1:]

        record_id = saved_data[0] # Прямое обращение к ID через первую колонку!!! Не через selected_item!!!

        record_id2 = selected_item

        # tree.set(item_id, column='Age', value=26)

        print("Record ID:", record_id)  # Проверка полученного идентификатора
        print("Record ID2:", record_id2)  # Проверка полученного идентификатора

        # Проверяем, существует ли запись с таким name_id
        cursor.execute("SELECT * FROM bcontacts WHERE name_id = ?", (record_id,))
        existing_record = cursor.fetchone()
        print("Existing Record:", existing_record)

        if existing_record is None:
            print("Запись с таким name_id не существует в базе данных.")
            return
        else:
            print("Запись с таким name_id СУЩЕСТВУЕТ в базе данных.")


        sql_update_query = f"""
            UPDATE bcontacts SET
                contact = ?,
                second_name = ?,
                first_name = ?,
                patronymic = ?,
                post = ?,
                company = ?,
                phone = ?,
                email = ?,
                inn = ?,
                comment = ?
            WHERE name_id = ?
        """


        # Собираем массив значений для обновления
        new_values = saved_data

        # Отладка массива
        print("Values from widgets:")
        for idx, value in enumerate(saved_data):
            print(f"Field {idx + 1}: {value}")

        id = new_values.pop(0)
        new_values.append(id)

        # # Убираем name_id из списка значений, так как он уже присутствует в условии WHERE
        # new_values = new_values[1:]  # Убираем первый элемент (name_id)



        print("New Values:", new_values)  # Проверка отправляемых данных
        print("sql_update_query:", sql_update_query)  # Проверка отправляемых данных

        # Выполняем запрос на обновление в базе данных
        try:

            cursor.execute(sql_update_query, new_values)
            con.commit()  # Обязательно фиксируем изменения
        except sq.Error as e:
            print("Ошибка при обновлении базы данных:", e)

        # Проверяем результат
        cursor.execute("SELECT * FROM bcontacts WHERE name_id = ?", (record_id,))
        # result = cursor.fetchone()

        result = list(map(list, cursor.fetchall()))

        print("Result after update:", result)

    print("Данные успешно обновлены в базе данных!")