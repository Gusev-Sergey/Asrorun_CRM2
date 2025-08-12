import settings
import sqlite3 as sq
# from functions.connector_01 import *



# Создание пользовательской функции для сравнения без учета регистра
def lower_case(text):
    return text.lower()

def enter_in_entry(event, root, frame_main, tree, name_entry):
    tree.destroy()
    frame_main.destroy()

    print("Зашли в Enter_in_entry")
    print(settings.data_dict)

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

        settings.data_dict = list(map(list, cur.fetchall()))

        print("settings data_dict после загрузки = ", settings.data_dict)

    con.commit()
    con.close()

    print("Вышли из Enter_in_entry")

    return True