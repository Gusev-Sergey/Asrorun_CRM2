import sqlite3 as sq
import settings
def save_base(data_new): # ТОЛЬКО ДЛЯ ПЕРВОГО СОХРАНЕНИЯ ПОСЛЕ ЗАГРУЗКИ ИЗ XLS!!!
    print(" зашли в save base !!!!")
    print("se-.dict = ", data_new)

    with sq.connect(f"base/base_contacts.db") as con:
        cur = con.cursor()

        # Создаем таблицу заново, предварительно удаляя старую версию
        # cur.execute("DROP TABLE IF EXISTS bcontacts;")

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

        print(type(data_new))

        d = data_new[:]

        print("d = ", d)

        for i in range(len(d)):
            print("1:", d[i][0], d[i][1], d[i][2], d[i][3], d[i][4], (d[i][5]), d[i][6], d[i][7], d[i][8], d[i][9])

            for j in range(0, 8):
                if d[i][j] == None:
                    d[i][j] = ""

            print("2:", d[i][0], d[i][1], d[i][2], d[i][3], d[i][4], str(d[i][5]), d[i][6], d[i][7], d[i][8], d[i][9])
            print("2.", d[i])

            line = d[i].copy()

            # Не добавляем поле name_id при вставке данных
            cur.execute("INSERT INTO bcontacts (contact, second_name, first_name, patronymic, post, company, phone, email, inn, comment) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", line)

    con.commit()
    con.close()
    print(">> запись базы завершена")