# Загрузка базы контактов


import sqlite3 as sq
import settings

def load_base():


    print("Зашли в LOAD base")
    print(settings.data_dict)

    with sq.connect(f"base/base_contacts.db") as con:

        cur = con.cursor()

        cur.execute("""SELECT * FROM bcontacts ORDER BY contact""")


        # settings.data_dict = cur.fetchall()
        settings.data_dict = list(map(list, cur.fetchall()))

        print("settings data_ict после загрузки = ", settings.data_dict)

    con.commit()
    con.close()

    print(">> Вышли из LOAD BASE")



