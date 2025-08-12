import settings
from functions.import_xlsx_without import import_xlsx_w
import sqlite3 as sq

def import_xls_add(add_data):

    add_data = []
    # Загрузка данных из xsl файла
    import_xlsx_w(add_data)

    xls_data = list(settings.data_dict)

    print("xls_data", xls_data)

    # Добавление в базу новых контактов из xls файла
    # settings.data_dict = [] # обнуляем на всякий случай
    # структура new_str = [contact, second_name, first_name, patronymic, post, company, phone, email, inn, comment]

    with sq.connect(f"base/base_contacts.db") as con:
        cur = con.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS bcontacts (
                name_id INTEGER PRIMARY KEY AUTOINCREMENT,
                contact TEXT,
                second_name TEXT,
                first_name TEXT,
                patronymic TEXT,
                post TEXT,
                company TEXT,
                phone TEXT,
                email TEXT,
                inn TEXT,
                comment TEXT
            )
        """)

        # print(type(data_new))

        d = xls_data[:]

        print("d2 = ", d)

        for i in range(len(d)):

            for j in range(0, 8):
                if d[i][j] == None:
                    d[i][j] = ""


            line = d[i].copy()

            # Не добавляем поле name_id при вставке данных
            cur.execute("INSERT INTO bcontacts (contact, second_name, first_name, patronymic, post, company, phone, email, inn, comment) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", line)

    con.commit()
    con.close()
    print(">> запись базы завершена")


